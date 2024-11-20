import struct  # It's used here for packing and unpacking binary data.


def tea_encode(v, k):
    v0, v1 = struct.unpack(">II", v)
    k0, k1, k2, k3 = struct.unpack(">IIII", k)
    sum = 0
    delta = 0x9E3779B9
    for _ in range(32):
        sum = (sum + delta) & 0xFFFFFFFF
        v0 += ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1)
        v0 &= 0xFFFFFFFF
        v1 += ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3)
        v1 &= 0xFFFFFFFF
    return struct.pack(">II", v0, v1)


def tea_decode(v, k):
    v0, v1 = struct.unpack(">II", v)
    k0, k1, k2, k3 = struct.unpack(">IIII", k)
    sum = (0x9E3779B9 << 5) & 0xFFFFFFFF
    delta = 0x9E3779B9
    for _ in range(32):
        v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3)
        v1 &= 0xFFFFFFFF
        v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1)
        v0 &= 0xFFFFFFFF
        sum = (sum - delta) & 0xFFFFFFFF
    return struct.pack(">II", v0, v1)


def main():
    # Plaintext
    p1 = struct.pack(">II", 0x412FA45B, 0x7DE13A5B)
    p2 = struct.pack(">II", 0x412FA45B, 0x7DE13A5A)

    print(f"\nInput_p1 = 0x{p1.hex()}")
    print(f"Input_p2 = 0x{p2.hex()}")

    # Key
    k = struct.pack(">IIII", 0x00000000, 0x80000000, 0x00000000, 0x00000000)
    print(f"\nKey = 0x{k.hex()}")

    # Encode
    encoded_p1 = tea_encode(p1, k)
    encoded_p2 = tea_encode(p2, k)

    print(f"\nEncoded_p1 = 0x{encoded_p1.hex()}")
    print(f"Encoded_p2 = 0x{encoded_p2.hex()}")

    # Decode
    decoded_p1 = tea_decode(encoded_p1, k)
    decoded_p2 = tea_decode(encoded_p2, k)

    print(f"\nDecoded_p1 = 0x{decoded_p1.hex()}")
    print(f"Decoded_p2 = 0x{decoded_p2.hex()}")


if __name__ == "__main__":
    main()
