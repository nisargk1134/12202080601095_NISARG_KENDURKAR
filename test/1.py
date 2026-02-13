n = int(input("Enter the value of n: "))

for i in range(1, n + 1):
    s = str(i)

    result = sum(int(a) for a in s) % 3 == 0
    result1 = s[-1] == "0" or s[-1] == "5"

    if result and result1:
        print("FizzBuzz")
    elif result:
        print("Fizz")
    elif result1:
        print("Buzz")
    else:
        print(i)
