import string
import random
import time
from hashlib import sha256


def pow(message, treshold):
    """
    Keep calculating a hash with a nonce until we get '0' * treshold at the beginning of the hash
    """
    nonce = 0
    sha256_hash = sha256((message + str(nonce)).encode('utf-8'))
    while sha256_hash.hexdigest()[:treshold] != '0' * treshold:
        nonce += 1
        sha256_hash = sha256((message + str(nonce)).encode('utf-8'))
    return nonce


if __name__ == '__main__':
    # Generate random string with random length 
    message = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(1, 1000)))
    for treshold in range(1, 10):
        start_time = time.time()
        print("Looking for nonce for treshold {}".format(treshold))
        nonce = pow(message, treshold)
        sha256_hash = sha256((message + str(nonce)).encode('utf-8'))
        print("==> Found nonce: {}".format(nonce))
        print("==> Hash: {}".format(sha256_hash.hexdigest()))
        print("==> Execution time: {} seconds".format(time.time() - start_time) + "\n" + "*"*74)


"""Output
Looking for nonce for treshold 1
==> Found nonce: 40
==> Hash: 0eb57624f7a83513173da7b099159bfdb6135957cdabcb25b269c34172373b6f
==> Execution time: 0.00010085105895996094 seconds
**************************************************************************
Looking for nonce for treshold 2
==> Found nonce: 125
==> Hash: 002e5598263d63bf417d54f7a6f58b56f8f0d1050d7df6382c15b179b86f524c
==> Execution time: 0.00021600723266601562 seconds
**************************************************************************
Looking for nonce for treshold 3
==> Found nonce: 12722
==> Hash: 00066b7cae745e670c5bfc6fa6c092765e46c8f9b952f59b1260b75230d38a70
==> Execution time: 0.019775867462158203 seconds
**************************************************************************
Looking for nonce for treshold 4
==> Found nonce: 66918
==> Hash: 00004f5cbb6a6f478148c53032da1730b972110bd2ebdbc71b5951ebc70ef21f
==> Execution time: 0.07697200775146484 seconds
**************************************************************************
Looking for nonce for treshold 5
==> Found nonce: 1752656
==> Hash: 000007a5fc9d24d888ca6e0caa27efdf2b97e53883bc9f8f16d12b5069b2ad71
==> Execution time: 1.9449889659881592 seconds
**************************************************************************
Looking for nonce for treshold 6
==> Found nonce: 35743161
==> Hash: 000000a76fa6355d67169f6f34b80b6971dc3054b049b9d247ee30a39c118fff
==> Execution time: 39.81222081184387 seconds
**************************************************************************
Looking for nonce for treshold 7
==> Found nonce: 622971941
==> Hash: 000000024aa164f626c2ac7346108d92fc314aaf112c570bb24d155c47262748
==> Execution time: 707.8721668720245 seconds
**************************************************************************
Looking for nonce for treshold 8
==> Found nonce: 10116871784
==> Hash: 0000000045c70255a6f98f5c398de640c1d1131f0b9422fc7e555af5d095a7d9
==> Execution time: 25046.94068789482 seconds
"""