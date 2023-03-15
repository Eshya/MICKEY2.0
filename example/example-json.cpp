#include "mickey.h"
#include <iostream>
#include <cstring>
#include <iomanip>
#include <cstdio>

int main() {
  // Contoh penggunaan Mickey cipher
  uint8_t key[] = {0x01, 0x02, 0x03, 0x04, 0x05};
  uint8_t iv[] = {0x06, 0x07, 0x08, 0x09, 0x0A};
  const char* message = "{\"message\":\"hello world\"}";
  size_t messageLength = strlen(message);
  uint8_t* data = new uint8_t[messageLength + 1];
  memcpy(data, message, messageLength);
  data[messageLength] = '\0';


  std::cout << "Source data: " << message << std::endl;
  std::cout << "Source hex: ";
  for (size_t i = 0; i < messageLength + 1; i++) {
    std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(data[i]);
  }
  std::cout << std::endl;

  // Buat objek dari kelas Mickey
  Mickey mickey(key, sizeof(key), iv, sizeof(iv));

  // Enkripsi data
  mickey.encrypt(data, messageLength + 1);

  // Cetak data hasil enkripsi dalam bentuk byte
  std::cout << "Encrypted hex: ";
  for (size_t i = 0; i < messageLength + 1; i++) {
    std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(data[i]);
  }
  std::cout << std::endl;

  Mickey mickey2(key, sizeof(key), iv, sizeof(iv));
  // Dekripsi data
  mickey2.decrypt(data, messageLength + 1);

  // Cetak data hasil dekripsi dalam bentuk hexademisal
  std::cout << "Decrypted hex: ";
  for (size_t i = 0; i < messageLength + 1; i++) {
    std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(data[i]);
  }
  std::cout << std::endl;

  char convertedChar[messageLength + 1];
  for (size_t i = 0; i < messageLength + 1; i++) {
    convertedChar[i] = static_cast<char>(data[i]);
  }
  std::cout << "Decrypted data: " << convertedChar << std::endl;

  delete[] data;
  return 0;
}
