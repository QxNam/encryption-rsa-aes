import random

def random_p_q(max_prime=100):
    num_prime = [i for i in range(2, max_prime) if all([i%j!=0 for j in range(2, int(i**0.5+1))])]
    p = random.choice(num_prime)
    num_prime.remove(p)
    q = random.choice(num_prime)
    return p, q

def is_prime(num):
    if num < 2:
        return False
    if all([num%j!=0 for j in range(2, int(num**0.5+1))]):
        return True
    return False

def random_prime(min_value=2, max_value=1000):
    while True:
        num = random.randint(min_value, max_value)
        if is_prime(num):
            return num

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generate_e(phi):
    while True:
        num = random.randint(2, phi-1)
        if gcd(num, phi) == 1:
            return num

def generate_d(e, phi):
    while True:
        d = random.randint(1, 2*phi)
        if (d*e)%phi == 1 and d!=e:
            return d

def generate_key_pair():
    p, q = random_p_q()
    n = p*q
    phi = (p-1)*(q-1)
    # print(f'{p=}, {q=}')
    # print(f'{n=}, {phi=}')
    e = generate_e(phi)
    d = generate_d(e, phi)
    print(f'Public key (n, e): {n, e}')
    print(f'Private key (n, d): {n, d}')
    return (n, e), (n, d)

def encrypt(public_key, message):
    n, e = public_key
    return ''.join([chr(pow(ord(char), e, n)) for char in message])

def decrypt(private_key, ciphertext):
    n, d = private_key
    return ''.join([chr(pow(ord(char), d, n)) for char in ciphertext])

if __name__ == '__main__':
    u_key, r_key = generate_key_pair()
    message = 'hello'
    ciphertext = encrypt(u_key, message)
    print(f'Encrypted `{message}`:', ciphertext)
    print(f'Decrypt `{ciphertext}`:', decrypt(r_key, ciphertext))