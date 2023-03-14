from ctypes import *
libc = CDLL("./mickey2-0.so")
import array
import binascii


key = array.array('B', [0x01, 0x02, 0x03, 0x04, 0x05])
iv = array.array('B', [0x06, 0x07, 0x08, 0x09, 0x0A])
data = array.array('B', [ord(c) for c in 'Hello World'])

mickey = libc.Mickey(key, len(key), iv, len(iv))

# Encrypt data
encrypted_data = data.copy()
mickey.encrypt(encrypted_data, len(encrypted_data))

# Print encrypted data as hex string
print("Encrypted data: {}".format(binascii.hexlify(encrypted_data).decode()))

# Create new instance of Mickey cipher
mickey2 = libc.Mickey(key, len(key), iv, len(iv))

# Decrypt data
decrypted_data = encrypted_data.copy()
mickey2.decrypt(decrypted_data, len(decrypted_data))

# Convert decrypted data back to string
decrypted_data = ''.join([chr(c) for c in decrypted_data])

# Print decrypted data as string
print("Decrypted data: {}".format(binascii.hexlify(decrypted_data).decode()))