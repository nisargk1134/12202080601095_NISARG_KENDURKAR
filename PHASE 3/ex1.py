
import os
import csv
import shutil
import mysql.connector
from concurrent.futures import ThreadPoolExecutor, as_completed




BASE_DIR = os.getcwd()

FOLDERS = ["incoming", "inprocess", "processed", "errored", "generated"]

CHUNK_SIZE = 150
MAX_THREADS = 5
TABLE_NAME = "person_businessentity"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",   
    "database": "testdb"      
}


def setup_folders():
    for folder in FOLDERS:
        os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_table(headers):
    conn = get_db_connection()
    cursor = conn.cursor()

    columns = ", ".join([f"`{h}` VARCHAR(255)" for h in headers])
    sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {columns}
    )
    """

    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def insert_rows(headers, rows):
    conn = get_db_connection()
    cursor = conn.cursor()

    cols = ", ".join([f"`{h}`" for h in headers])
    placeholders = ", ".join(["%s"] * len(headers))

    sql = f"INSERT INTO {TABLE_NAME} ({cols}) VALUES ({placeholders})"
    cursor.executemany(sql, rows)

    conn.commit()
    cursor.close()
    conn.close()


def process_chunk(chunk_id, headers, rows):

    csv_path = os.path.join(
        BASE_DIR, "generated", f"generated_chunk_{chunk_id}.csv"
    )

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


    insert_rows(headers, rows)


def process_csv(filename):
    incoming_path = os.path.join(BASE_DIR, "incoming", filename)
    inprocess_path = os.path.join(BASE_DIR, "inprocess", filename)

    if not os.path.exists(incoming_path):
        return

    shutil.move(incoming_path, inprocess_path)

    try:
        with open(inprocess_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)

   
        create_table(headers)

       
        chunks = [
            rows[i:i + CHUNK_SIZE]
            for i in range(0, len(rows), CHUNK_SIZE)
        ]

       
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = [
                executor.submit(process_chunk, idx, headers, chunk)
                for idx, chunk in enumerate(chunks)
            ]

            for future in as_completed(futures):
                future.result()  

       
        shutil.move(
            inprocess_path,
            os.path.join(BASE_DIR, "processed", filename)
        )

        print(f"SUCCESS: {filename} processed")

    except Exception as e:
        print(f"ERROR: {filename} failed -> {e}")

        if os.path.exists(inprocess_path):
            shutil.move(
                inprocess_path,
                os.path.join(BASE_DIR, "errored", filename)
            )


if __name__ == "__main__":
    setup_folders()

    files = [
        f for f in os.listdir("incoming")
        if f.lower().endswith(".csv")
    ]

    for file in files:
        process_csv(file)
