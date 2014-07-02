--------
Overview
--------

This package was a remedy to there being no PyPI-published, pure-Python 
Rijndael (AES) implementations, and that nothing available, in general, was 
compatible with both Python2 *and* Python3. The same is true of the PBKDF2 
key-expansion algorithm.

The encryptor takes a source generator (which yields individual blocks). There 
are source-generators provided for both data from a variable and data from a 
file. It is trivial if you'd like to write your own. The encryptor and 
decryptor functions are written as generators. Decrypted data has PKCS7
padding. A utility function is provided to trim this (*trim_pkcs7_padding*).

The implementation includes Python2 and Python3 implementations of both 
Rijndael and PBKDF2, and chooses the version when loaded.

The default block-size is 128-bits in order to be compatible with AES.

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

    import sys
    import io
    import os.path
    import hashlib

    import pprp
    import pprp.config

    # Make the strings the right type for the current Python version.
    def trans(text):
        return text.encode('ASCII') if sys.version_info[0] >= 3 else text

    passphrase = trans('password')
    salt = trans('salt')
    key_size = 32
    data = ("this is a test" * 100).encode('ASCII')

Do the key-expansion::

    key = pprp.pbkdf2(passphrase, salt, key_size)

Create a source from available data::

    sg = pprp.data_source_gen(data)

Feed the source into the encryptor::

    eg = pprp.rjindael_encrypt_gen(key, sg)

Feed the encryptor into the decryptor::

    dg = pprp.rjindael_decrypt_gen(key, eg)

Sink the output to a variable (and automatically trim the padding)::

    decrypted = pprp.decrypt_sink(dg)

There is also a *decrypt_to_file_sink* sink that takes a file-object as the 
first argument.

Check the result::

    assert data == decrypted

The following is a portion of the output of the example script 
(*test/example.py*). Notice that, due to this being an efficient, 
generator-based design, the encryption of each block is followed by a 
decryption::

    2014-07-01 12:24:13,182 - pprp.source - DEBUG - Yielding [data] source block: (0)-(0)
    2014-07-01 12:24:13,182 - pprp.adapters - DEBUG - Encrypting and yielding encrypted block: (0)
    2014-07-01 12:24:13,183 - pprp.adapters - DEBUG - Decrypting and yielding decrypted block: (0)
    2014-07-01 12:24:13,183 - pprp.source - DEBUG - Yielding [data] source block: (1)-(16)
    2014-07-01 12:24:13,183 - pprp.adapters - DEBUG - Encrypting and yielding encrypted block: (1)
    2014-07-01 12:24:13,183 - pprp.adapters - DEBUG - Decrypting and yielding decrypted block: (1)
    2014-07-01 12:24:13,183 - pprp.source - DEBUG - Yielding [data] source block: (2)-(32)
    2014-07-01 12:24:13,183 - pprp.adapters - DEBUG - Encrypting and yielding encrypted block: (2)
    2014-07-01 12:24:13,183 - pprp.adapters - DEBUG - Decrypting and yielding decrypted block: (2)
    2014-07-01 12:24:13,184 - pprp.source - DEBUG - Yielding [data] source block: (3)-(48)
    2014-07-01 12:24:13,184 - pprp.adapters - DEBUG - Encrypting and yielding encrypted block: (3)
    2014-07-01 12:24:13,184 - pprp.adapters - DEBUG - Decrypting and yielding decrypted block: (3)
    ...


-----
Notes
-----

The generators can take a block-size in the event that you don't want the 
default. The default block-size can also be changed via the PPRP_BLOCK_SIZE 
environment variable.
