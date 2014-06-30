#!/usr/bin/env python3.3

import sys
import os.path
dev_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, dev_path)

import io
import os.path
import hashlib

import pprp

def trans(text):
    return text.encode('ASCII') if sys.version_info[0] >= 3 else text

passphrase = trans('password')
salt = trans('salt')
block_size = 16
key_size = 32
data = "this is a test" * 100

key = pprp.pbkdf2(passphrase, salt, key_size)

def source_gen():
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        len_ = len(block)

        if len_ > 0:
            yield block.encode('ASCII')

        if len_ < block_size:
            break

# Pump the encrypter output into the decrypter.
encrypted_gen = pprp.rjindael_encrypt_gen(key, source_gen(), block_size)

# Run, and sink the output into an IO stream. Trim the padding off the last 
# block.

s = io.BytesIO()
ends_at = 0
for block in pprp.rjindael_decrypt_gen(key, encrypted_gen, block_size):
    ends_at += block_size
    if ends_at >= len(data):
        block = pprp.trim_pkcs7_padding(block)

    s.write(block)

decrypted = s.getvalue()
assert data == decrypted.decode('ASCII')
