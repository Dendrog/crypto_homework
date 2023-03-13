import random
list = []
E = {}
D = {}
cipher = ""
decrypt = ""

for i in range(0x61,0x7b):
    list.append(chr(i))
random.shuffle(list)

start = 0x61
for i in list:
    E[chr(start)] = i
    D[i]=chr(start)
    start += 1
    
plain_text = input('평문 입력: ')

for i in plain_text:
    if(E.get(i)):
        cipher += E.get(i)
    else:
        cipher += i

for i in cipher:
    if(D.get(i)):
        decrypt += D.get(i)
    else:
        decrypt += i
        
print("암호문: {}".format(cipher))
print("복호문: {}".format(decrypt))
