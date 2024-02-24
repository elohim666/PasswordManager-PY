import hashlib
from cryptography.fernet import Fernet


#Hashing the master password
def hash_pass(Pass):
    sha256 = hashlib.sha256()
    sha256.update(Pass.encode())
    return sha256.hexdigest()


#Generating a secret symetric key
def generate_key():
   return Fernet.generate_key()


#Initilizing Fernet cipher with provided key
def initialize_cipher(key):
   return Fernet(key)


#Encrypting our passwords
def encrypt_password(cipher, Pass):
   return cipher.encrypt(Pass.encode()).decode()


#Decrypting our passwords
def decrypt_password(cipher, encrypted_Pass):
   return cipher.decrypt(encrypted_Pass.encode()).decode()