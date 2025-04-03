from tabulate import tabulate

levels = [1, 2, 2, 1, 2, 3, 2, 3, 3, 4, 3, 1, 2, 2]
items = [[1]]
for index in range(len(levels)):
    if index > 0:
        if levels[index] > levels[index - 1]:
            item = items[-1] + [1]

        else:
            slot = -1 * (levels[index - 1] - levels[index]) - 1
            item = items[-1][:slot] + [items[-1][slot] + 1]

        items.append(item)

items = [".".join(map(str, item)) for item in items]

table = [levels, items]
print(tabulate(table))
