class A:
    pass


class B(A):
    pass


a = A
b = B

print(a == A)
print(a is A)
print(b == A)
print(b is A)


A = B

print(a == A)
print(a is A)
print(b == A)
print(b is A)
