import mickey_cpp
import struct
import ctypes

def encrypt(key, iv, plaintext):
    # Inisialisasi objek Mickey
    m = mickey_cpp.Mickey(key, len(key), iv, len(iv))
    
    # Enkripsi plaintext
    ciphertext = bytearray()
    for i in range(len(plaintext)):
        keystream = m.generateKeystreamByte()
        ciphertext.append(keystream ^ plaintext[i])
    
    return bytes(ciphertext)

def decrypt(key, iv, ciphertext):
    # Inisialisasi objek Mickey
    m = mickey_cpp.Mickey(key, len(key), iv, len(iv))
    
    # Dekripsi ciphertext
    plaintext = bytearray()
    for i in range(len(ciphertext)):
        keystream = m.generateKeystreamByte()
        plaintext.append(keystream ^ ciphertext[i])
    
    return bytes(plaintext)

# Contoh penggunaan
key = (ctypes.c_uint8 * 5)(0x01, 0x02, 0x03, 0x04, 0x05)
iv = (ctypes.c_uint8 * 5)(0x06, 0x07, 0x08, 0x09, 0x0A)
plaintext = b'Tes enkripsi dan dekripsi menggunakan Mickey'
# print("Plaintext:", plaintext.decode('utf-8', errors='replace'))
print("Original:", plaintext.hex())
# Enkripsi plaintext
ciphertext = encrypt(key, iv, plaintext)
print("Ciphertext:", ciphertext.hex())

# Dekripsi ciphertext
plaintext_result = decrypt(key, iv, ciphertext)
# print("Decrypt Hex:", plaintext.hex())
print("Plaintext:", plaintext.decode('utf-8', errors='replace'))
