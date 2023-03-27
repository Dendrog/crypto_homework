import os
import random
import time
import hashlib
import base58check
from Crypto.Hash import RIPEMD160
from binascii import unhexlify

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = [0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8]
a = 0
b = 7

def generate_private_key():
    while(True):
        result = int(hashlib.sha256(os.urandom(32)+bytes(str(random.random())+str(time.time()),'utf-8')).digest().hex(),16)
        if(result < p):
            break
    return result

def Ex_euclidean(n,b):
    r1 = n
    if(b<0):
        b+=n
    r2 = b
    t1 = 0
    t2 = 1
    while(r2>0):
        q = r1//r2
        r = r1-q*r2
        r1 = r2
        r2 = r
        t = t1 - q *t2
        t1 = t2
        t2 = t
    if r1 != 1:
        return None
    if t1 < 0:
        t1 = n + t1
    return t1

def daa(k):
    bin_num = bin(k)[3:]
    K = G
    for i in bin_num:
        if(i=='1'):
            K = add(add(K,K),G)
        else:
            K = add(K,K)
    return K
            
def add(first,second):
    if(first != second):
        w = (second[1]-first[1]) * Ex_euclidean(p,(second[0]-first[0])) %p
    else:
        w = (3*first[0]**2+a)*Ex_euclidean(p,(2*first[1])) %p
    
    if (w < 0):
        w += p 
    x3 = (w**2-first[0]-second[0]) %p
    y3 = (w*(first[0]-x3)-first[1]) %p
    if x3 < 0:
        x3 += p
    if y3 < 0:
        y3 += p
    result = [x3,y3]
    return result

def bitcoin_addr():
    p_k = int(input('개인키 입력? '),16)
    pub = daa(p_k)
    if(pub[1]%2):
        pre_y = '0x03'
    else:
        pre_y = '0x02'
    public_key = pre_y+hex(pub[0])[2:]
    public_key_hash = hashlib.sha256(bytes.fromhex(public_key[2:])).digest()
    h = RIPEMD160.new()
    h.update(public_key_hash)
    ripemd160 = bytes(h.hexdigest(),'utf-8')
    plus_ver = unhexlify(b'00'+ripemd160)
    print("공개키 hash : {}".format(plus_ver.hex()))
    double_hash = hashlib.sha256(hashlib.sha256(plus_ver).digest()).digest()
    checksum = double_hash[0:4]
    before_base58 = base58check.b58encode(plus_ver+checksum)
    print("비트코인 주소 = {}".format(before_base58.decode('utf-8')))

bitcoin_addr()
