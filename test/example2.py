#!/usr/bin/env python3.3

"""Example of how to completely encrypt and then completely decrypt."""

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
data = ("this is a test" * 100).encode('ASCII')

key = pprp.pbkdf2(passphrase, salt, key_size)

# Encrypt.

sg = pprp.data_source_gen(data)
eg = pprp.rjindael_encrypt_gen(key, sg)
encrypted = pprp.encrypt_sink(eg)

# Decrypt.

sg = pprp.data_source_gen(encrypted)
dg = pprp.rjindael_decrypt_gen(key, sg)
decrypted = pprp.decrypt_sink(dg)

assert data == decrypted
