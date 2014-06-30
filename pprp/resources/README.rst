--------
Overview
--------

This package was a remedy to there being no PyPI-published, pure-Python 
Rijndael (AES) implementations, and that nothing available, in general, was 
compatible with both Python2 *and* Python3. The same is true of the PBKDF2 
key-expansion algorithm.

The encrypter expects a source generator (which yields individual blocks). The 
encrypter and decrypter functions are written as generators. Decrypted data has 
PKCS7 padding. A utility function is provided to trim this 
(*trim_pkcs7_padding*).

The implementation includes Python2 and Python3 implementations of both 
Rijndael and PBKDF2, and chooses the version when loaded.

This project is also referred to as *pprp*, which stands for "Pure Python 
Rijndael and PBKDF2".


------------
Installation
------------

Install via *pip*::

    $ sudo pip install pprp


-------
Example
-------

Encrypt and decrypt the data, and compare the results. This example works in 
both Python 2 and 3.

Top imports and defines::

    import io
    import os.path
    import hashlib

    import pprp

    # Make the strings the right type for the current Python version.
    def trans(text):
        return text.encode('ASCII') if sys.version_info[0] >= 3 else text

    passphrase = trans('password')
    salt = trans('salt')
    block_size = 16
    key_size = 32
    data = "this is a test" * 100

Do the key-expansion::

    key = pprp.pbkdf2(passphrase, salt, key_size)

Define the source generator (we'll give this to the encrypter)::

    def source_gen():
        for i in range(0, len(data), block_size):
            block = data[i:i + block_size]
            len_ = len(block)

            if len_ > 0:
                yield block.encode('ASCII')

            if len_ < block_size:
                break

Connect the encryptor to the decryptor::

    encrypted_gen = pprp.rjindael_encrypt_gen(key, source_gen(), block_size)

Run, sink the output into an IO stream, and trim the padding off the last 
block::

    s = io.BytesIO()
    ends_at = 0
    for block in pprp.rjindael_decrypt_gen(key, encrypted_gen, block_size):
        ends_at += block_size
        if ends_at >= len(data):
            block = pprp.trim_pkcs7_padding(block)

        s.write(block)

    decrypted = s.getvalue()

Check the result::

    assert data == decrypted.decode('ASCII')
