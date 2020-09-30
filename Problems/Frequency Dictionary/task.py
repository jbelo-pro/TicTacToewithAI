# put your python code here
words = [n.lower() for n in input().split()]
counter = dict()
for word in words:
    counter[word] = counter.get(word, 0) + 1

for k, v in counter.items():
    print(k, v)

