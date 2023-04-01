from bitmap import BitMap
import hashlib

a = hex(int(hashlib.sha256(bytes("a",'utf-8')).digest().hex(),16))
print(a)
bm = BitMap(32)
bm.set(1)

print(bm.test(0))