# TEA-Cryptography Algorithm

A school project on vulnerability of TEA cryptography algorithm.

TEA (Tiny Encryption Algorithm) is a symmetric-key block cipher that encrypts 64-bit block of data using a 128-bit key. It uses a feistal structure (Total up to 32 cycles), each cycle consist of two rounds and each round have three operations - bitwise shifting, XOR, and addition. A constant delta is use to introduce non-linerity and improves diffusion where one bit difference in plaintext will result 32 bit difference in ciphertext. The key point of the algorithm is that its small, compact and lightweight with only few lines of code hence its more suitable for embedded system or IOT devices that uses little mememory. However, due to its simple key sceduling algorithm which only splits the key into four section, its result in vulnerabilities such as equivalent key and differential related-key attack hence leading to the development of the improved version XTEA.



Slides used during presentation:
https://docs.google.com/presentation/d/1Tml7thveb5kvFNWufVTG-B7yUzN0sIf25N8xgZCn2ck/edit?usp=sharing
