!pip3 install Crypto
!pip3 install pycryptodome

from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

def generate_dsa_key():
  key = DSA.generate(2048)
  return key

def sign_message(message, private_key):
  hash_object = SHA256.new(message.encode())
  signer = DSS.new(private_key, 'fips-186-3')
  signature = signer.sign(hash_object)
  return signature

def verify_signature(message, signature, public_key):
  hash_object = SHA256.new(message.encode())
  verifier = DSS.new(public_key, 'fips-186-3')
  try:
    verifier.verify(hash_object, signature)
    print("Signature is valid.")
    return True
  except ValueError:
    print("Invalid signature.")
    return False

# Generate DSA key pair
private_key = generate_dsa_key()
public_key = private_key.publickey()

# Message to be signed
message = "IT"

# Sign the message
signature = sign_message(message, private_key)
print("Generated Signature:", signature.hex())

# Verify the signature
verify_signature(message, signature, public_key)
