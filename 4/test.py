import hashlib
import base58

def public_key_to_address(public_key):
    # Step 1: SHA-256
    sha256 = hashlib.sha256()
    sha256.update(public_key.encode())
    hash1 = sha256.digest()

    # Step 2: RIPEMD-160
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hash1)
    hash2 = ripemd160.digest()

    # Step 3: Add version byte in front of RIPEMD-160 hash (0x00 for Main Network)
    hash3 = b'\x00' + hash2

    # Step 4: Perform SHA-256 hash on the extended RIPEMD-160 result
    sha256 = hashlib.sha256()
    sha256.update(hash3)
    hash4 = sha256.digest()

    # Step 5: Perform SHA-256 hash on the result of the previous SHA-256 hash
    sha256 = hashlib.sha256()
    sha256.update(hash4)
    hash5 = sha256.digest()

    # Step 6: Take the first 4 bytes of the second SHA-256 hash. This is the address checksum
    checksum = hash5[:4]

    # Step 7: Add the 4 checksum bytes from stage 7 at the end of extended RIPEMD-160 hash from stage 3.
    hash6 = hash3 + checksum

    # Step 8: Convert to Base58 encoding
    address = base58.b58encode(hash6)

    return address.decode('utf-8')
'''
pubkey = 'public_key'
address_uncompressed = public_key_to_address(pubkey)
print('Uncompressed Address:', address_uncompressed)

compress_key = True
if compress_key:
    pubkey_compressed = '02' + pubkey[-64:] if int(pubkey[-1], 16) % 2 == 0 else '03' + pubkey[-64:]
else:
    pubkey_compressed = pubkey
'''
pubkey_compressed = input()
address_compressed = public_key_to_address(pubkey_compressed)
print('Compressed Address:', address_compressed)