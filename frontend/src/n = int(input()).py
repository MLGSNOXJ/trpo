a = float(input())
s = 1
while a > 0:
    s *= a
    a = float(input())
print(f'{s:.6f}')