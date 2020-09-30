values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
          '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
t = 0
for i in range(6):
    t += values[input()]

print(t / 6)

