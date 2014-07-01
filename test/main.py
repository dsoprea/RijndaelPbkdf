#!/usr/bin/env python3.3

import sys

import os.path
dev_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, dev_path)

import io
import os.path
import hashlib

import pprp

def _configure_logging():
    import logging
    import os

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(FMT)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

_configure_logging()

def trans(text):
    return text.encode('ASCII') if sys.version_info[0] >= 3 else text

passphrase = trans('password')
salt = trans('salt')
block_size = 16
key_size = 32
data = "this is a test" * 100

key = pprp.pbkdf2(passphrase, salt, key_size)

# Create a source from available data.
sg = pprp.data_source_gen(data, block_size)

# Feed the source into the encryptor.
eg = pprp.rjindael_encrypt_gen(key, sg, block_size)

# Feed the encryptor into the decryptor.
dg = pprp.rjindael_decrypt_gen(key, eg, block_size)

# Run, and sink the output into an IO stream. Trim the padding off the last 
# block.

s = io.BytesIO()
ends_at = 0
for block in dg:
    ends_at += block_size
    if ends_at >= len(data):
        block = pprp.trim_pkcs7_padding(block)

    s.write(block)

decrypted = s.getvalue()
assert data == decrypted.decode('ASCII')
