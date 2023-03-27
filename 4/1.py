import os
import random
import time
import hashlib

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
    print("공개키 (16) x: "+hex(pub[0]))
    if(pub[1]%2):
        pre_y = '0x03'
    else:
        pre_y = '0x02'
    public_key = pre_y+hex(pub[0])[2:]
    print("공개키+홀짝 : "+public_key)
    public_key_hash = hashlib.sha256(public_key.encode()).digest()
    print("public key hash : {}".format(public_key_hash.hex()))
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(public_key_hash)
    hash2 = ripemd160.digest()
    print("ripemd160 : {}".format(hash2.hex()))

bitcoin_addr()

'''
p_k = generate_private_key()
#p_k = 53872441058844996679977158571737064850247033767869768697312274424220201917752
print("개인키 (16) : "+hex(p_k))
print("개인키 (10) : {}".format(p_k))
#print("개인키 (16) : "+hex(generate_private_key()))
pub = daa(p_k)
print("공개키 (16) x: "+hex(pub[0]))
print("공개키 (16) y: "+hex(pub[1]))
print(pub)
'''