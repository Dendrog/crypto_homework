import hashlib
import time

def POW(msg,target_bit):
    exp = int(target_bit[0:2],16)
    coe = int(target_bit[2:],16)
    target = coe * 2**(8*(exp-3))
    start = time.time()
    while(True):
        now = time
        extra = now.time()
        for i in range(0xffffffff+1):
            data = bytes(msg+str(int(extra))+str(i),'utf-8')
            test = int(hashlib.sha256(data).digest().hex(),16)
            if(test<target):
                end = time.time()
                ex_time = str(end - start)
                hex_target = '0x'+'0'*(64-len(hex(target)[2:]))+hex(target)[2:]
                hex_test = '0x'+'0'*(64-len(hex(test)[2:]))+hex(test)[2:]
                return [hex_target,msg,str(int(extra)),str(i),ex_time,hex_test]
            
            
    
msg = input('메세지의 내용? ')
target_bit = input('Target bits? ')

result = POW(msg,target_bit)
print("Target : {}".format(result[0]))
print("메시지: {}, Extra nonce: {}, nonce: {}".format(result[1],result[2],result[3]))
print("실행 시간: {}초".format(result[4]))
print("Hash result: {}".format(result[5]))
