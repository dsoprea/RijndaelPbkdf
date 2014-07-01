import logging

import pprp.config

_logger = logging.getLogger(__name__)

# This will be assigned from the top of the "rijndael" package.
rijndael_cls = None

def rjindael_encrypt_gen(key, s, block_size=pprp.config.DEFAULT_BLOCK_SIZE):
    r = rijndael_cls(key, block_size=block_size)

    padded = False
    i = 0
    for block in s:
        len_ = len(block)
        if len_ < block_size:
            padding_size = block_size - len_
            block += (chr(padding_size) * padding_size).encode('ASCII')
            padded = True

        _logger.debug("Encrypting and yielding encrypted block: (%d)", i)
        yield r.encrypt(block)
        i += 1

    if padded is False:
        yield r.encrypt(chr(block_size) * block_size).encode('ASCII')

def rjindael_decrypt_gen(key, s, block_size=pprp.config.DEFAULT_BLOCK_SIZE):
    r = rijndael_cls(key, block_size=block_size)

    i = 0
    for block in s:
        _logger.debug("Decrypting and yielding decrypted block: (%d)", i)
        yield r.decrypt(block)
        i += 1
