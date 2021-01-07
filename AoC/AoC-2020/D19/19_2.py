import re
from functools import lru_cache
from pprint import pprint

with open("inputPt2.txt") as fin:
    data = fin.read().split("\n")

# Variable to keep track of rules
rules = {}

# Get all the rules
line = 0
while data[line] != "":
    number = int(data[line][:data[line].index(":")])
    rule = data[line][data[line].index(":") + 2:]
    rules[number] = rule
    line += 1

# Variable to keep track of regexes

def get_regex(number):
    # Gets regex based on id
    if number == 8:
        return r8

    if number == 11:
        return r11

    ans = to_regex(rules[number])
    return ans

def to_regex(rule):
    # Converts "rule" to regex

    if "|" in rule:
        part1 = [int(i) for i in rule[:rule.index("|") - 1].split(" ")]
        part2 = [int(i) for i in rule[rule.index("|") + 2:].split(" ")]

        regex1 = "(" + ")(".join([get_regex(i) for i in part1]) + ")"
        regex2 = "(" + ")(".join([get_regex(i) for i in part2]) + ")"

        ans =  f"({regex1})|({regex2})"

    elif '"' in rule:
        ans =  rule[1]

    else:
        parts = [int(i) for i in rule.split(" ")]
        ans = "(" + ")(".join([get_regex(i) for i in parts]) + ")"

    return ans

r42 = get_regex(42)
r31 = get_regex(31)

r8 = f"({r42})+"

r11s = []
for n in range(1, 20):
    r11s.append(f"({r42}){{{n}}}({r31}){{{n}}}")
r11 = "(" + ")|(".join([i for i in r11s]) + ")"
print(r11)

# Verify!
count = 0
line += 1

while line < len(data):
    matches = bool(re.fullmatch(get_regex(0), data[line]))
    count += matches
    line += 1

print(count)