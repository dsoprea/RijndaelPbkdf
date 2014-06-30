#!/usr/bin/env python2.7

import sys
import os.path
dev_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, dev_path)

import io
import os.path
import hashlib

import rijndael

if __name__ == '__main__':
    filepath = 'supervisord.conf'
    passphrase = 'password'
    salt = 'q3468fxmq'
    block_size = 16
    key_size = 32

    key = rijndael.pbkdf2(passphrase, salt, key_size)

    def source_gen():
        with open(filepath, 'rb') as f:
            while 1:
                block = f.read(block_size)
                len_ = len(block)

                if len_ > 0:
                    yield block

                if len_ < block_size:
                    break

    encrypted_gen = rijndael.rjindael_encrypt_gen(key, source_gen(), block_size)

    s = io.BytesIO()
    ends_at = 0
    for block in rijndael.rjindael_decrypt_gen(key, encrypted_gen, block_size):
        ends_at += block_size
        if ends_at >= os.path.getsize(filepath):
            block = rijndael.trim_pkcs7_padding(block)

        s.write(block)

    decrypted = s.getvalue().decode('ASCII')
    print(hashlib.md5(decrypted.encode('ASCII')).hexdigest())
