from cryptography.fernet import Fernet
key = Fernet.generate_key()
f = Fernet(key)
file = open('./data.txt','r')
plain_text = file.read()
file.close()

token = f.encrypt(bytes(plain_text, 'utf-8'))
save = open('./encrypted.txt','w')
save.write(token.decode('utf-8'))
save.close()

cipher = open('./encrypted.txt','r')
cipher_text = cipher.read()
print(f.decrypt(bytes(cipher_text,'utf-8')).decode('utf-8'))
