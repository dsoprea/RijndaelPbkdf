# This will be assigned from the top of the "rijndael" package.
rijndael_cls = None

def rjindael_encrypt_gen(key, s, block_size):
    r = rijndael_cls(key, block_size=block_size)

    padded = False
    for block in s:
        len_ = len(block)
        if len_ < block_size:
            padding_size = block_size - len_
            block += (chr(padding_size) * padding_size).encode('ASCII')
            padded = True

        yield r.encrypt(block)

    if padded is False:
        yield r.encrypt(chr(block_size) * block_size).encode('ASCII')

def rjindael_decrypt_gen(key, s, block_size):
    r = rijndael_cls(key, block_size=block_size)

    for block in s:
        yield r.decrypt(block)
