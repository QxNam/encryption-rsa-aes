import random
from test_rsa import random_p_q

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


def generate_key_pair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    # n = pq
    n = p * q

    # Phi is the totient of n
    phi = (p-1) * (q-1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return both public and private keys
    return ((e, n), (d, n))

def split_blocks(blocks):
    # Loại bỏ các dấu ngoặc vuông và dấu phẩy, sau đó chuyển đổi chuỗi thành danh sách số nguyên
    cleaned_blocks = blocks.replace("[", "").replace("]", "").replace(",", "").split()
    return [int(block) for block in cleaned_blocks]
def join_blocks(blocks):
    return ' '.join(str(block) for block in blocks)

def encrypt(pk, plaintext):
    # Unpack the key into it's components
    print(pk)
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = ''.join([chr(pow(ord(char), key, n)) for char in plaintext])
    # Return the array of bytes
    return cipher


def decrypt(private_key, ciphertext):
    d, n = private_key
    decrypted_blocks = [pow(block, d, n) for block in ciphertext]
    decrypted_text = ''.join([chr(block) for block in decrypted_blocks])
    return decrypted_text
def input_private_key():
    d = int(input(" - Enter your private key 'd': "))
    n = int(input(" - Enter your private key 'n': "))
    return d, n
def split_message(message, block_size):
    return [message[i:i+block_size] for i in range(0, len(message), block_size)]

if __name__ == '__main__':
    print("===========================================================================================================")
    print("================================== RSA Encryptor / Decrypter ==============================================")
    print(" ")

    # p = int(input(" - Enter a prime number (17, 19, 23, etc): "))
    # q = int(input(" - Enter another prime number (Not one you entered above): "))
    p, q = random_p_q()

    print(" - Generating your public / private key-pairs now . . .")
    public, private = generate_key_pair(p, q)

    print(" - Your public key is ", public, " and your private key is ", private)

    # choice = input(" - Do you want to encrypt or decrypt a message? (enc/dec): ")
    message = 'hello'
    block_size = len(str(public[1])) - 1  # Chia thông điệp thành các khối nhỏ hơn giá trị của n
    blocks = split_message(message, block_size)
    encrypted_blocks = []
    for block in blocks:
        encrypted_block = encrypt(public, block)
        encrypted_blocks.extend(encrypted_block)
    encrypted_message = join_blocks(encrypted_blocks)
    print(" - Your encrypted message is:", encrypted_message)

    # private_key = input_private_key()
    # encrypted_message = input(" - Enter the encrypted message: ")
    encrypted_blocks = split_blocks(encrypted_message)
    decrypted_message = decrypt(private_key, encrypted_blocks)
    print(" - Your decrypted message is:", decrypted_message)

    # if choice.lower() == 'enc':
    #     message = input(" - Enter a message to encrypt with your public key: ")
    #     block_size = len(str(public[1])) - 1  # Chia thông điệp thành các khối nhỏ hơn giá trị của n
    #     blocks = split_message(message, block_size)
    #     encrypted_blocks = []
    #     for block in blocks:
    #         encrypted_block = encrypt(public, block)
    #         encrypted_blocks.extend(encrypted_block)
    #     encrypted_message = join_blocks(encrypted_blocks)
    #     print(" - Your encrypted message is:", encrypted_message)
    # elif choice.lower() == 'dec':
    #     private_key = input_private_key()
    #     encrypted_message = input(" - Enter the encrypted message: ")
    #     encrypted_blocks = split_blocks(encrypted_message)
    #     decrypted_message = decrypt(private_key, encrypted_blocks)
    #     print(" - Your decrypted message is:", decrypted_message)
    # else:
    #     print("Invalid choice. Please enter 'enc' or 'dec'.")

    # print(" ")
    # print("============================================ END ==========================================================")
    # print("===========================================================================================================")