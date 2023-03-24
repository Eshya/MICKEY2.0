import struct
import numpy as np
MICKEY_IV_SIZE = 5

class Mickey:
    def __init__(self, key, keyLen, iv, ivLen):
        # Initialize the state
        self.state = np.zeros(5, dtype=np.uint32)

        # Set the IV and IV index
        self.iv = np.zeros(MICKEY_IV_SIZE, dtype=np.uint8)
        # self.iv = [0] * (MICKEY_IV_SIZE)
        for i in range(ivLen):
            self.iv[i] = iv[i]
        self.ivIndex =  np.uint8(0)
        

        
        # Initialize the last element of the IV to 0x00
        # self.iv[ivLen] = 0x00

        # Initialize the state using the key and IV
        self.init(key, keyLen)

    def init(self, key, keyLen):
        # Initialize the state using the key and IV
        key = np.frombuffer(key, dtype=np.uint8)
        for i in range(keyLen):
            self.state[i >> 2] |= (key[i] << (8 * (i & 3)))
        self.state[4] |= 0x80  # Set the top bit of state[4] to 1
        self.generateKeystreamByte()  # Generate the first keystream byte

    def generateKeystreamByte(self):
        # Generate a keystream byte using the Mickey 2.0 algorithm
        # tmp = 0
        tmp =  np.uint32(0)
        keystream =  np.uint8(0)
       
        for i in range(5):
            tmp = np.uint32(np.uint64(tmp)+np.uint64(self.state[i]))
            self.state[i] = np.uint32(self.state[(i + 1) % 5] ^ ((tmp << 13) | (tmp >> 19)))
       
        keystream = np.uint8((np.uint64(self.state[0]) >> np.uint64(24)) & np.uint64(255))
        # print("state0: ",format(self.state[0],'02X')," keystream: ",format(keystream,'02X'),"\n")
        

        # Step 14
        self.state[0] = np.uint32((np.uint64(self.state[0]) << np.uint64(8)) | ((np.uint64(self.state[1]) >> np.uint64(24)) & np.uint64(0xFF)))
        self.state[1] = np.uint32((np.uint64(self.state[1]) << np.uint64(8)) | ((np.uint64(self.state[2]) >> np.uint64(24)) & np.uint64(0xFF)))
        self.state[2] = np.uint32((np.uint64(self.state[2]) << np.uint64(8)) | ((np.uint64(self.state[3]) >> np.uint64(24)) & np.uint64(0xFF)))
        self.state[3] = np.uint32((np.uint64(self.state[3]) << np.uint64(8)) | ((np.uint64(self.state[4]) >> np.uint64(24)) & np.uint64(0xFF)))
        self.state[4] = np.uint32((np.uint64(self.state[4]) << np.uint64(8)) | (np.uint64(keystream) ^ np.uint64(self.iv[self.ivIndex])))
        
        
       
        self.ivIndex += 1
        # print(self.ivIndex)
        if self.ivIndex >= MICKEY_IV_SIZE:
            self.ivIndex = 0
        
        # print(keystream)
        return keystream
    
    def encrypt(self,data: bytes) -> bytes:
        dataLen = len(data)
        encrypted_data = bytearray(dataLen)
        for i in range(dataLen):
            # Generate a keystream byte
            keystream = self.generateKeystreamByte()
            # XOR the plaintext byte with the keystream byte to produce the ciphertext byte
            encrypted_data[i] = np.uint8(data[i]) ^ keystream
        return bytes(encrypted_data)

    def decrypt(self,data: bytes) -> bytes:
        # Decryption is the same as encryption for a stream cipher
        return  self.encrypt(data)