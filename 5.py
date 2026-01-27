def execution_logger(fact):
    def wrapper(*args, **kwargs):
        print("Starting function")
        print("Ending function")

        return fact(*args, **kwargs)

    return wrapper


@execution_logger
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


print(f"Result: {factorial(3)}")
