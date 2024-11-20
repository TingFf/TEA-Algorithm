import struct  # It's used here for packing and unpacking binary data.


def tea_encode(v, k):
    v0, v1 = struct.unpack(">II", v)
    k0, k1, k2, k3 = struct.unpack(">IIII", k)
    sum = 0
    delta = 0x9E3779B9
    for _ in range(4):
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
    for _ in range(4):
        v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3)
        v1 &= 0xFFFFFFFF
        v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1)
        v0 &= 0xFFFFFFFF
        sum = (sum - delta) & 0xFFFFFFFF
    return struct.pack(">II", v0, v1)


def main():
    # Plaintext
    v = struct.pack(">II", 0x03500080, 0x00000023)
    print("\n\n\nInput Data:")
    print(f" v = 0x{v.hex()}")

    # Convert bytes to letters
    plaintext = "".join(
        chr((struct.unpack(">I", v[i : i + 4])[0]) & 0xFFFFFFFF)
        for i in range(0, len(v), 4)
        if (struct.unpack(">I", v[i : i + 4])[0]) < 0x110000
    )
    print(f"Plaintext as letters: {plaintext}")

    # Key
    k = struct.pack(
        ">IIII", 0x41241428, 0x31537241, 0x64336853 ^ (1 << 29), 0x35326435 ^ (1 << 29)
    )
    print(f"\nKey = 0x{k.hex()}")

    # Encode
    encoded = tea_encode(v, k)

    print(f"\nEncoded data = 0x{encoded.hex()}")

    # Decode
    decoded = tea_decode(encoded, k)
    print(f"\nDecoded data = 0x{decoded.hex()}")


if __name__ == "__main__":
    main()
