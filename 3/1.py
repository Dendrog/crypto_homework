import os
import random
import time
import hashlib

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = [0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8]
a = 0
b = 7
e1 = [0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8]
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

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

def generate_public_key(k):
    bin_num = bin(k)[3:]
    K = G
    for i in bin_num:
        if(i=='1'):
            K = add(add(K,K),G)
        else:
            K = add(K,K)
    return K
            
def mul(k,g):
    bin_num = bin(k)[3:]
    K = g
    for i in bin_num:
        if(i=='1'):
            K = add(add(K,K),g)
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



def sign(M,d):
    while(True):
        r = random.randrange(1,q-1)
        if(r > 1):
            break
    s1 = (mul(r,e1)[0]) % q
    s2 = (int(hashlib.sha256(bytes(M,'utf-8')).digest().hex(),16)+d*s1)*Ex_euclidean(q,r) % q
    return s1,s2

def verify(M,s1,s2,e2):
    A = int(hashlib.sha256(bytes(M,'utf-8')).digest().hex(),16)*Ex_euclidean(q,s2) % q
    B = s1 * Ex_euclidean(q,s2) % q
    T = add(mul(A,e1),mul(B,e2))
    print("\tA = "+hex(A))
    print("\tB = "+hex(B))
    if(T[0] % q == s1 % q):
        return True
    else:
        return False
    
if __name__ == "__main__":
    d = generate_private_key() # 2주차 과제에서 작성한 함수
    e2 = generate_public_key(d) # 2주차 과제에서 작성한 함수
    
    M = input("메시지? ")
    S1, S2 = sign(M, d)
    print("1. Sign:")
    print("\tS1 =", hex(S1))
    print("\tS2 =", hex(S2))
    
    print("2. 정확한 서명을 입력할 경우:")
    if verify(M, S1, S2, e2) == True:
        print("검증 성공")
    else:
        print("검증 실패")
    
    print("3. 잘못된 서명을 입력할 경우:")
    if verify(M, S1-1, S2-1, e2) == True:
        print("검증 성공")
    else:
        print("검증 실패")