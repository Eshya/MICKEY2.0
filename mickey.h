#ifndef MICKEY_H
#define MICKEY_H

#include <stdint.h>

#define MICKEY_IV_SIZE 10

class Mickey {
  private:
    uint32_t state[5];
    uint8_t iv[MICKEY_IV_SIZE];
    uint8_t ivIndex;

    void init(uint8_t *key, uint8_t keyLen);

  public:
    Mickey(uint8_t *key, uint8_t keyLen, uint8_t *iv, uint8_t ivLen);

    void encrypt(uint8_t *data, uint8_t dataLen);
    void decrypt(uint8_t *data, uint8_t dataLen);
    void setIV(uint8_t *iv, uint8_t ivLen);
    void setKey(uint8_t *key, uint8_t keyLen);
    uint8_t generateKeystreamByte();
};

#endif /*MICKEY_H*/
