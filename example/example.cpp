#include "mickey.h"
#include <iostream>
#include <cstring>
#include <iomanip>
#include <cstdio>


int main() {
  // Contoh penggunaan Mickey cipher
  uint8_t key[] = {0x01, 0x02, 0x03, 0x04, 0x05};
  uint8_t iv[] = {0x06, 0x07, 0x08, 0x09, 0x0A};
  uint8_t data[] = {'H','e','l','l','o',' ','W','o','r','l','d'};
  size_t dataLength = sizeof(data)/sizeof(*data);

  // Buat objek dari kelas Mickey
  Mickey mickey(key, sizeof(key), iv, sizeof(iv));

  // Enkripsi data
  mickey.encrypt(data, dataLength);

  // Cetak data hasil enkripsi dalam bentuk byte
  std::cout << "Encrypted data: ";
  for (size_t i = 0; i < dataLength; i++) {
    std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(data[i]);
  }
  std::cout << std::endl;

  Mickey mickey2(key, sizeof(key), iv, sizeof(iv));
  // Dekripsi data
//   mickey2.setIV(iv, sizeof(iv));
//   mickey2.setKey(key, sizeof(key));
  mickey2.decrypt(data, dataLength);

  // Cetak data hasil dekripsi dalam bentuk hexademisal

  
  std::cout << "Decrypted data: ";
  for (size_t i = 0; i < dataLength; i++) {
    std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(data[i]);
  }
  std::cout << std::endl;

  char convertedChar[dataLength + 1];
  for (size_t i = 0; i < dataLength; i++) {
    convertedChar[i] = static_cast<char>(data[i]);
  }
  convertedChar[dataLength] = '\0';
  std::cout << "Decrypted data: " << convertedChar << std::endl;
  return 0;
}
