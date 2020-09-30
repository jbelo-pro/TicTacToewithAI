walks
t = 0
for day in walks:
    t += day.get('distance', 0)

print(int(t/len(walks)))
