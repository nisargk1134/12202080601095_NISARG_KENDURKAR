a = input("Enter numbers: ")
b = [int(item.strip()) for item in a.split(",")]


tup = tuple(b)
sets = set(b)

result = sum(b)


print("\nSum of numbers: ", result)
print("Unique numbers: ", sets)

print(list(sorted(b)))
