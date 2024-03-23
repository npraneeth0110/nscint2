!pip3 install Crypto
!pip3 install pycryptodome

def hash_function(message):
  hashed = sha1(message.encode("UTF-8")).hexdigest()
  return hashed

def mod_inverse(a, m) :
  a=a%m;
  for x in range(1,m) :
    if((a*x)%m==1) :
     return(x)

  return(1)

from random import randint
from sympy import mod_inverse
import hashlib

def hash_function(text):
    # Using SHA-256 for hashing
    return hashlib.sha256(text.encode()).hexdigest()

def getPrime(bits):
    # You need to implement this function or import it from a library
    # For instance, using sympy library:
    from sympy import primerange
    primes = list(primerange(2**(bits-1), 2**bits))
    return primes[randint(0, len(primes)-1)]

def parameter_generation():
    q = getPrime(5)
    p = getPrime(10)
    while (p - 1) % q != 0:
        p = getPrime(10)
        q = getPrime(5)
    print("Prime divisor (q): ", q)
    print("Prime modulus (p): ", p)
    flag = True
    while flag:
        h = int(input("Enter integer between 1 and p-1(h): "))
        if 1 < h < (p - 1):
            g = 1
            while g == 1:
                g = pow(h, int((p - 1) / q)) % p
            flag = False
        else:
            print("Wrong entry")
    print("Value of g is : ", g)
    return p, q, g

def per_user_key(p, q, g):
    x = randint(1, q - 1)
    print("Randomly chosen x(Private key) is: ", x)
    y = pow(g, x) % p
    print("Randomly chosen y(Public key) is: ", y)
    return x, y

def signature(name, p, q, g, x):
    with open(name) as file:
        text = file.read()
    hash_component = hash_function(text)
    print("Hash of document sent is: ", hash_component)
    r = 0
    s = 0
    while s == 0 or r == 0:
        k = randint(1, q - 1)
        r = ((pow(g, k)) % p) % q
        i = mod_inverse(k, q)
        hashed = int(hash_component, 16)
        s = (i * (hashed + (x * r))) % q
    return r, s, k

def verification(name, p, q, g, r, s, y):
    with open(name) as file:
        text = file.read()
    hash_component = hash_function(text)
    print("Hash of document received is: ", hash_component)
    w = mod_inverse(s, q)
    hashed = int(hash_component, 16)
    u1 = (hashed * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1) * pow(y, u2)) % p) % q
    print("Value of u1 is: ", u1)
    print("Value of u2 is: ", u2)
    print("Value of v is : ", v)
    if v == r:
        print("The signature is valid!")
    else:
        print("The signature is invalid!")

file_path = '/content/check.txt'

with open(file_path, 'r') as file:
    content = file.read()

print(content)

global_var = parameter_generation()

keys = per_user_key(global_var[0], global_var[1], global_var[2])

print()
file_name = input("Enter the name of the document to sign: ")
components = signature(file_name, global_var[0], global_var[1], global_var[2], keys[0])
print("r (Component of signature) is:", components[0])
print("k (Randomly chosen number) is:", components[2])
print("s (Component of signature) is:", components[1])

print()
file_name = input("Enter the name of the document to verify: ")
verification(file_name, global_var[0], global_var[1], global_var[2], components[0], components[1], keys[1])

