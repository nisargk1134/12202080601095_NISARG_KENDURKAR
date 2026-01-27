def even_numbers(n):
    result = []
    for i in range(n + 1):
        if i % 2 == 0:
            result.append(i)
    return result


en = even_numbers(30)
num = list(filter(lambda x: x > 10, en))
print(num)
