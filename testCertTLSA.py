#!/usr/bin/env python3
import hashlib
import configparser
import os

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


current_path = os.path.dirname(os.path.abspath(__file__)) + "/"
config = configparser.ConfigParser()
config.read(current_path + 'conf_tlsa-ovh.ini')
cert = config['default']['cert']

with open(cert, 'r') as f:
    mx_pem_cert = f.read()
mx_cert = x509.load_pem_x509_certificate(mx_pem_cert.encode('ascii'), default_backend())

mx_pubkey = mx_cert.public_key()
mx_pubkey_bytes = mx_pubkey.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
digest = hashlib.sha256(mx_pubkey_bytes).hexdigest()
print(f'_25._tcp.example.com TLSA 3 0 1 {digest}')

mx_der_certbytes = mx_cert.public_bytes(Encoding.DER)
digest2 = hashlib.sha256(mx_der_certbytes).hexdigest()
print(f'_25._tcp.example.com TLSA 3 1 1 {digest2}')

