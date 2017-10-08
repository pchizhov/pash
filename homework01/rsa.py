def is_prime(n):
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    for i in range(1, n):
        if n % i == 0:
            divisor = i
    if divisor == 1:
        return True
    else:
        return False

def gcd(a, b):
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while a % b != 0:
        c = a % b
        a = b
        b = c
    return b

def multiplicative_inverse(e, phi):
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    table = []
    while True:
        table.append([phi, e, phi % e, phi // e])
        phi, e = e, table[-1][2]
        if table[-1][2] == 0:
            break
    table[-1].extend([0, 1])
    for i in range(len(table) - 2, -1, -1):
        x = table[i + 1][-1]
        y = table[i + 1][-2] - table[i + 1][-1] * table[i][3]
        table[i].extend([x, y])
    d = table[0][-1] % table[0][0]
    return d


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    # n = pq
    n = p*q

    # phi = (p-1)(q-1)
    phi = (p-1)*(q-1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))
