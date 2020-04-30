import unittest

import pprp
import pprp.pbkdf2


class TestCrypto(unittest.TestCase):
    def test_full(self):
        passphrase = 'password'.encode('ASCII')
        salt = 'salt'.encode('ASCII')

        key_size = 32
        data = "this is a test" * 100
        data_bytes = data.encode('ASCII')

        key = pprp.pbkdf2(passphrase, salt, key_size)

        # Create a source from available data.
        sg = pprp.data_source_gen(data_bytes)

        # Feed the source into the encryptor.
        eg = pprp.rijndael_encrypt_gen(key, sg)

        # Feed the encryptor into the decryptor.
        dg = pprp.rijndael_decrypt_gen(key, eg)

        # Sink the output into an IO-stream.
        decrypted = pprp.decrypt_sink(dg)

        self.assertEquals(data_bytes, decrypted)
