#include "mickey.h"
// this code made by eshya
Mickey::Mickey(uint8_t *key, uint8_t keyLen, uint8_t *iv, uint8_t ivLen) {
  // Initialize the state
  state[0] = 0;
  state[1] = 0;
  state[2] = 0;
  state[3] = 0;
  state[4] = 0;

  // Set the IV and IV index
  for (int i = 0; i < ivLen; i++) {
    this->iv[i] = iv[i];
  }
  ivIndex = 0;

  // Initialize the state using the key and IV
  init(key, keyLen);
}
void Mickey::init(uint8_t *key, uint8_t keyLen) {
  // Initialize the state using the key and IV
  for (int i = 0; i < keyLen; i++) {
    state[i >> 2] |= (key[i] << (8 * (i & 3)));
  }
  state[4] |= 0x80; // Set the top bit of state[4] to 1
  generateKeystreamByte(); // Generate the first keystream byte
}

uint8_t Mickey::generateKeystreamByte() {
// Generate a keystream byte using the Mickey 2.0 algorithm
    uint32_t tmp;
    uint8_t keystream;
    
    // Step 1
    tmp = state[0] + state[3];
    state[0] = ((state[1] ^ state[2]) + tmp) << 7 | ((state[1] ^ state[2]) + tmp) >> 25;
    
    // Step 2
    tmp = state[1] + state[4];
    state[1] = ((state[2] ^ state[3]) + tmp) << 9 | ((state[2] ^ state[3]) + tmp) >> 23;
    
    // Step 3
    tmp = state[2] + state[0];
    state[2] = ((state[3] ^ state[4]) + tmp) << 13 | ((state[3] ^ state[4]) + tmp) >> 19;
    
    // Step 4
    tmp = state[3] + state[1];
    state[3] = ((state[4] ^ state[0]) + tmp) << 18 | ((state[4] ^ state[0]) + tmp) >> 14;
    
    // Step 5
    tmp = state[4] + state[2];
    state[4] = ((state[0] ^ state[1]) + tmp) << 7 | ((state[0] ^ state[1]) + tmp) >> 25;
    
    // Step 6
    tmp = state[0] + state[1];
    state[0] = ((state[1] ^ state[2]) + tmp) << 9 | ((state[1] ^ state[2]) + tmp) >> 23;
    
    // Step 7
    tmp = state[1] + state[2];
    state[1] = ((state[2] ^ state[3]) + tmp) << 13 | ((state[2] ^ state[3]) + tmp) >> 19;
    
    // Step 8
    tmp = state[2] + state[3];
    state[2] = ((state[3] ^ state[4]) + tmp) << 18 | ((state[3] ^ state[4]) + tmp) >> 14;
    
    // Step 9
    tmp = state[3] + state[4];
    state[3] = ((state[4] ^ state[0]) + tmp) << 7 | ((state[4] ^ state[0]) + tmp) >> 25;
    
    // Step 10
    tmp = state[4] + state[0];
    state[4] = ((state[0] ^ state[1]) + tmp) << 9 | ((state[0] ^ state[1]) + tmp) >> 23;
    
    // Step 11
    tmp = state[0] + state[1];
    state[0] = ((state[1] ^ state[2]) + tmp) << 13 | ((state[1] ^ state[2]) + tmp) >> 19;
    
    // Step 12
    tmp = state[1] + state[2];
    state[1] = ((state[2] ^ state[3]) + tmp) << 18 | ((state[2] ^ state[3]) + tmp) >> 14;
    
    // Step 13
    keystream = (state[0] >> 24) & 0xFF;
    
    // Step 14
    state[0] = (state[0] << 8) | ((state[1] >> 24) & 0xFF);
    state[1] = (state[1] << 8) | ((state[2] >> 24) & 0xFF);
    state[2] = (state[2] << 8) | ((state[3] >> 24) & 0xFF);
    state[3] = (state[3] << 8) | ((state[4] >> 24) & 0xFF);
    state[4] = (state[4] << 8) | (keystream ^ iv[ivIndex]);
    
    // Step 15
    ivIndex++;
    if (ivIndex >= MICKEY_IV_SIZE) {
    ivIndex = 0;
    }
    
    return keystream;
}

void Mickey::encrypt(uint8_t *data, uint8_t dataLen) {
    for (int i = 0; i < dataLen; i++) {
    // Generate a keystream byte
    uint8_t keystream = generateKeystreamByte();
    
    // XOR the plaintext byte with the keystream byte to produce the ciphertext byte
    data[i] ^= keystream;
    }
}

void Mickey::decrypt(uint8_t *data, uint8_t dataLen) {
    // Decryption is the same as encryption for a stream cipher
    encrypt(data, dataLen);
}

void Mickey::setIV(uint8_t *iv, uint8_t ivLen) {
      for (int i = 0; i < ivLen; i++) {
        this->iv[i] = iv[i];
      }
      this->ivIndex = 0;
      generateKeystreamByte(); // Generate the first keystream byte using the new IV
}

void Mickey::setKey(uint8_t *key, uint8_t keyLen) {
      // Initialize the state using the key and IV
      for (int i = 0; i < keyLen; i++) {
        state[i >> 2] |= (key[i] << (8 * (i & 3)));
      }
      state[4] |= 0x80; // Set the top bit of state[4] to 1
      generateKeystreamByte(); // Generate the first keystream byte
}