import os

# Required we're acting as AES.
DEFAULT_BLOCK_SIZE = int(os.environ.get('PPRP_BLOCK_SIZE', str(128 // 8)))
