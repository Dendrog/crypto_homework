from bitmap import BitMap
import hashlib

class BloomFilter:
    m = 0
    k = 0
    n = 0
    
    def __init__(self,m,k):
        self.m = m
        self.k = k
        self.bf = BitMap(m)
    
    def getPositions(self,item):
        result = []
        for i in range(1,self.k+1):
            st_num = bytes(str(i),'utf-8')
            result.append(int(hashlib.sha256(bytes(item,'utf-8')+st_num).digest().hex(),16) % self.m)
        return result
        
    def add(self,item):
        bits = self.getPositions(item)
        for i in bits:
            self.bf.set(i)
        self.n += 1
        
    def contains(self,item):
        bits = self.getPositions(item)
        for i in bits:
            if (self.bf.test(i)==False):
                return False
        return True
    
    def reset(self):
        for i in range(self.m):
            self.bf.reset(i)
        self.n = 0
    
    def __repr__(self):
        st = "M = {}. F = {}\nBitMap = {}\n항목의 수 = {}, 1인 비트수 = {}".format(self.m,self.k,self.bf,self.n,self.bf.count())
        return st
            
if __name__ == "__main__":
    bf = BloomFilter(53, 3)
    for ch in "AEIOU":
        bf.add(ch)
    print(bf)
    for ch in "ABCDEFGHIJ":
        print(ch, bf.contains(ch))