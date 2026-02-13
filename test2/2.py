a = input("Enter numbers: ")
b = []

for items in a.split(','):
    b.append(int(items.strip()))

tup = tuple(b)
sets = set(b)

sum = 0
for items in b:
    sum = sum + items

print("The Tuple of enetered numbers: ",tup)
print("The Unique numbers: ",sets)

print(list(sorted(b)))