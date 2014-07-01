#!/usr/bin/env python3.3

import sys

import os.path
dev_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, dev_path)

import io
import os.path
import hashlib

import pprp
import pprp.config

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
key_size = 32
data = "this is a test" * 100

key = pprp.pbkdf2(passphrase, salt, key_size)

# Create a source from available data.
sg = pprp.data_source_gen(data)

# Feed the source into the encryptor.
eg = pprp.rjindael_encrypt_gen(key, sg)

#encrypted = pprp.encrypt_sink(eg)

#with open('/tmp/encrypt.sink', 'wb') as f:
#    pprp.encrypt_to_file_sink(f, eg)

# Feed the encryptor into the decryptor.
dg = pprp.rjindael_decrypt_gen(key, eg)

# Sink the output into an IO-stream.
decrypted = pprp.decrypt_sink(dg)

#with open('/tmp/decrypt.sink', 'wb') as f:
#    pprp.decrypt_to_file_sink(f, dg)
#
#with open('/tmp/decrypt.sink', 'rb') as f:
#    decrypted = f.read()

assert data == decrypted.decode('ASCII')
