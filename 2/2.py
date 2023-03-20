import os
import random
import time
import hashlib

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = [0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8]

def generate_private_key():
    while(True):
        result = int(hashlib.sha256(os.urandom(32)+bytes(str(random.random())+str(time.time()),'utf-8')).digest().hex(),16)
        if(result < p):
            break
    return result

def generate_public_key():

print(hex(generate_private_key()))