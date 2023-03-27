import hashlib
import base58
import ecdsa

def private_key_to_public_key(private_key):
    private_key = bytes.fromhex(private_key)
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    x, y = vk.pubkey.point.x(), vk.pubkey.point.y()
    return (x, y)

def compress_public_key(x, y):
    if y % 2 == 0:
        return '02' + format(x, 'x')
    else:
        return '03' + format(x, 'x')

def public_key_to_hash(compressed_public_key):
    sha = hashlib.sha256(bytes.fromhex(compressed_public_key)).digest()
    print(sha.hex())
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha)
    return '00' + ripemd160.hexdigest()

def base58_check_encoding(hex_value):
    checksum = hashlib.sha256(hashlib.sha256(bytes.fromhex(hex_value)).digest()).hexdigest()[:8]
    return base58.b58encode(bytes.fromhex(hex_value + checksum))

private_key = input("개인키 입력? ")
x, y = private_key_to_public_key(private_key)
compressed_public_key = compress_public_key(x, y)
print(compressed_public_key)
public_key_hash = public_key_to_hash(compressed_public_key)
bitcoin_address = base58_check_encoding(public_key_hash)

print("공개키 hash =", public_key_hash)
print("비트코인 주소 =", bitcoin_address.decode('utf-8'))