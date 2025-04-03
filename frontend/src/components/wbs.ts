/*
################### WBS LOGIC IN PYTHON ###################

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

###########################################################
*/

import { table } from "table";

const levels: number[] = [1, 2, 2, 1, 2, 3, 2, 3, 3, 4, 3, 1, 2, 2];
const items: number[][] = [[1]];

for (let index = 1; index < levels.length; index++) {
  const lastItem = items[items.length - 1];
  if (levels[index] > levels[index - 1]) {
    items.push([...lastItem, 1]);
  } else {
    const slot = lastItem.length - (levels[index - 1] - levels[index]) - 1;
    items.push([...lastItem.slice(0, slot), lastItem[slot] + 1]);
  }
}

const formattedItems = items.map((item) => item.join("."));

const data = [
  ["Level", ...levels],
  ["Item", ...formattedItems],
];

console.log(table(data));
