x = 0
print(x)
for i in range(50000000):
    x += 1
    if x == 1000000:
        print("hey")
    if x == 2000000:
        print("oka")
    if x == 3000000:
        print("my")
print(x)