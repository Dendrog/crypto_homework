from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet

with open("private_key.pem",'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password = None,
        backend=default_backend()
    )

with open("public_key.pem","rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

plain_text = bytes(input("평문 입력 : "),'utf-8')

max_len = int((public_key.key_size/8)-(2*256/8)-2)
if(len(plain_text)<=max_len):
    print("\n[일반적인 RSA]\n")
    encrypted = public_key.encrypt(
        plain_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("암호문 : {}".format(encrypted))
    
    original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("복호화 : {}".format(original_message.decode('utf-8')))

else:
    print("\n[긴 문자열 RSA]\n")
    key = Fernet.generate_key()
    f = Fernet(key)
    enc_msg = f.encrypt(plain_text)
    print("암호문 : {}".format(enc_msg))
    
    enc_key = public_key.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # 수신자 전달 완료되었다고 가정
    
    aes_key = private_key.decrypt(
        enc_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    f2 = Fernet(aes_key)
    d = f2.decrypt(enc_msg)
    print("복호화 : {}".format(d.decode('utf-8')))
    
    
    