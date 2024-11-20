import random


# Simplified TEA Encryption (reduced rounds for demonstration purposes)
def tea_encrypt(plain_text, key, rounds):
    v0, v1 = plain_text
    k0, k1, k2, k3 = key
    delta = 0x9E3779B9
    sum_value = 0
    for _ in range(rounds):  # reduced rounds for demo
        sum_value = (sum_value + delta) & 0xFFFFFFFF
        v0 = (
            v0 + (((v1 << 4) + k0) ^ (v1 + sum_value) ^ ((v1 >> 5) + k1))
        ) & 0xFFFFFFFF
        v1 = (
            v1 + (((v0 << 4) + k2) ^ (v0 + sum_value) ^ ((v0 >> 5) + k3))
        ) & 0xFFFFFFFF
    return v0, v1


# Related-Key Differential Attack function
def related_key_differential_attack(
    original_key, related_key, input_diff, num_trials=100000000, rounds=2
):
    successful_pairs = []
    successful_count = 0

    print(f"Original Key: {original_key}")
    print(f"Related Key : {related_key}")

    for _ in range(num_trials):
        # Generate random plaintext pair with input differential
        p1_left, p1_right = random.randint(0, 0xFFFFFFFF), random.randint(0, 0xFFFFFFFF)
        p2_left = p1_left
        p2_right = p1_right ^ input_diff

        # Encrypt with original and related keys
        c1_left, c1_right = tea_encrypt((p1_left, p1_right), original_key, rounds)
        c2_left, c2_right = tea_encrypt((p2_left, p2_right), related_key, rounds)

        # Check for successful pairs (using relaxed condition)
        left_diff = c1_left ^ c2_left
        right_diff = c1_right ^ c2_right

        if left_diff == 0 or right_diff == 0:  # Relaxed success condition
            successful_pairs.append(
                (
                    (p1_left, p1_right),
                    (p2_left, p2_right),
                    (c1_left, c1_right),
                    (c2_left, c2_right),
                )
            )
            successful_count += 1

    probability = successful_count / num_trials

    print(f"Total successful pairs found: {len(successful_pairs)}")
    print(f"Empirical Probability of Differential Characteristic: {probability:.10f}")
    return successful_pairs


# Parameters for attack
original_key = (0x00000000, 0x00000000, 0x00000000, 0x00000000)
related_key = (
    0x00000000,
    0x00000000,
    0x40000000,
    0x40000000,
)  # Example related key difference
input_diff = 0x00000010  # Chosen input differential
num_trials = 1000000


# Reduced number of plaintext pairs for demo

# Conduct related-key differential attack
successful_pairs = related_key_differential_attack(
    original_key, related_key, input_diff, num_trials
)
print(f"Sample of successful pairs: {successful_pairs[:5]}")
