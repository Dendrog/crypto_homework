
vi_cipher = ""
vi_decrypt = ""
auto_cipher = ""
auto_decrypt = ""

plain_text = input("평문 입력: ").upper().replace(' ','')
vigenere_key = input("Vigenere 암호? ").upper()

count = 0
for i in plain_text:
    vi_cipher += chr((((ord(i)-65)+(ord(vigenere_key[count])-65))%26)+65)
    count = (count+1)%len(vigenere_key)
count = 0
for i in vi_cipher:
    vi_decrypt += chr((((ord(i)-65)-(ord(vigenere_key[count])-65))%26)+65)
    count = (count+1)%len(vigenere_key)
    
print('\t* 암호문: {}'.format(vi_cipher))
print('\t* 평문: {}'.format(vi_decrypt))

auto_key = int(input("자동 키 암호? "))
count = -1
for i in plain_text:
    if(count == -1):
        auto_cipher += chr((((ord(i)-65)+auto_key)%26)+65)
        count = (count+1)%len(plain_text)
    else:
        auto_cipher += chr((((ord(i)-65)+(ord(plain_text[count])-65))%26)+65)
        count = (count+1)%len(plain_text)
        
count = -1
for i in auto_cipher:
    if(count == -1):
        auto_decrypt += chr((((ord(i)-65)-auto_key)%26)+65)
        count = (count+1)%len(plain_text)
    else:
        auto_decrypt += chr((((ord(i)-65)-(ord(plain_text[count])-65))%26)+65)
        count = (count+1)%len(plain_text)

print('\t* 암호문: {}'.format(auto_cipher))
print('\t* 평문: {}'.format(auto_decrypt))