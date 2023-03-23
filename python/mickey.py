import struct

MICKEY_IV_SIZE = 10

class Mickey:
    def __init__(self, key, keyLen, iv, ivLen):
        # Initialize the state
        self.state = [0] * 5

        # Set the IV and IV index
        self.iv = [0] * (MICKEY_IV_SIZE)
        for i in range(ivLen):
            self.iv[i] = iv[i]
        self.ivIndex = 0

        # Initialize the last element of the IV to 0x00
        # self.iv[ivLen] = 0x00

        # Initialize the state using the key and IV
        self.init(key, keyLen)

    def init(self, key, keyLen):
        # Initialize the state using the key and IV
        for i in range(keyLen):
            self.state[i >> 2] |= (key[i] << (8 * (i & 3)))
        self.state[4] |= 0x80  # Set the top bit of state[4] to 1
        self.generateKeystreamByte()  # Generate the first keystream byte

    def generateKeystreamByte(self):
        # Generate a keystream byte using the Mickey 2.0 algorithm
        tmp = 0
        keystream = 0

        # Step 1
        tmp = self.state[0] + self.state[3]
        self.state[0] = ((self.state[1] ^ self.state[2]) + tmp) << 7 | ((self.state[1] ^ self.state[2]) + tmp) >> 25

        # Step 2
        tmp = self.state[1] + self.state[4]
        self.state[1] = ((self.state[2] ^ self.state[3]) + tmp) << 9 | ((self.state[2] ^ self.state[3]) + tmp) >> 23

        # Step 3
        tmp = self.state[2] + self.state[0]
        self.state[2] = ((self.state[3] ^ self.state[4]) + tmp) << 13 | ((self.state[3] ^ self.state[4]) + tmp) >> 19

        # Step 4
        tmp = self.state[3] + self.state[1]
        self.state[3] = ((self.state[4] ^ self.state[0]) + tmp) << 18 | ((self.state[4] ^ self.state[0]) + tmp) >> 14

        # Step 5
        tmp = self.state[4] + self.state[2]
        self.state[4] = ((self.state[0] ^ self.state[1]) + tmp) << 7 | ((self.state[0] ^ self.state[1]) + tmp) >> 25

        # Step 6
        tmp = self.state[0] + self.state[1]
        self.state[0] = ((self.state[1] ^ self.state[2]) + tmp) << 9 | ((self.state[1] ^ self.state[2]) + tmp) >> 23

        # Step 7
        tmp = self.state[1] + self.state[2]
        self.state[1] = ((self.state[2] ^ self.state[3]) + tmp) << 13 | ((self.state[2] ^ self.state[3]) + tmp) >> 19

        # Step 8
        tmp = self.state[2] + self.state[3]
        self.state[2] = ((self.state[3] ^ self.state[4]) + tmp) << 18 | ((self.state[3] ^ self.state[4]) + tmp) >> 14

        # Step 9
        tmp = self.state[3] + self.state[4]
        self.state[3] = ((self.state[4] ^ self.state[0]) + tmp) << 7 | ((self.state[4] ^ self.state[0]) + tmp) >> 25

        # Step 10
        tmp = self.state[4] + self.state[0]
        self.state[4] = ((self.state[0] ^ self.state[1]) + tmp) << 9 | ((self.state[0] ^ self.state[1]) + tmp) >> 23

        # Step 11
        tmp = self.state[0] + self.state[1]
        self.state[0] = ((self.state[1] ^ self.state[2]) + tmp) << 13 | ((self.state[1] ^ self.state[2]) + tmp) >> 19

        # Step 12
        tmp = self.state[1] + self.state[2]
        self.state[1] = ((self.state[2] ^ self.state[3]) + tmp) << 18 | ((self.state[2] ^ self.state[3]) + tmp) >> 14

        # Step 13
        keystream = (self.state[0] >> 24) & 0xFF

        
        # Step 14
        self.state[0] = (self.state[0] << 8) | ((self.state[1] >> 24) & 0xFF)
        self.state[1] = (self.state[1] << 8) | ((self.state[2] >> 24) & 0xFF)
        self.state[2] = (self.state[2] << 8) | ((self.state[3] >> 24) & 0xFF)
        self.state[3] = (self.state[3] << 8) | ((self.state[4] >> 24) & 0xFF)
        # print(self.ivIndex)
        # print(self.iv[self.ivIndex-1])
        self.state[4] = (self.state[4] << 8) | (keystream ^ self.iv[self.ivIndex])
        # self.state[4] = (self.state[4] << 8) | (keystream & 255)

        self.ivIndex += 1
        # print(self.ivIndex)
        if self.ivIndex >= MICKEY_IV_SIZE:
            self.ivIndex = 0
            
        return keystream
    
    def encrypt(self,data: bytes) -> bytes:
        dataLen = len(data)
        encrypted_data = bytearray(dataLen)
        for i in range(dataLen):
            # Generate a keystream byte
            keystream =  self.generateKeystreamByte()
            # XOR the plaintext byte with the keystream byte to produce the ciphertext byte
            encrypted_data[i] = data[i] ^ keystream
        return bytes(encrypted_data)

    def decrypt(self,data: bytes) -> bytes:
        # Decryption is the same as encryption for a stream cipher
        return  self.encrypt(data)
