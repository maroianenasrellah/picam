
def int_to_bytes(x):
    #return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    return x.to_bytes(2, 'big')

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

def to_bytes(n, length):
    return bytes( (n >> i*8) & 0xff for i in reversed(range(length)))
##print("int to bytes")
##y=int_to_bytes(20)
##print(y)
##print("int from bytes")
##z=int_from_bytes(y)
##print(z)
a = to_bytes(0, 1)
print(a)