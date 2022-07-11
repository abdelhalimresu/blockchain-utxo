import random
import math


def isPrime(n):
	for i in range(2, int(math.sqrt(n)+1)):
		if n % i == 0: 
			return False
	return n > 1

def nextPrime(n):
	while not isPrime(n):
		n += 1
	return n

def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)

def modinv(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		return 0
	else:
		return x % m

def encrypt(m, keyPair):
	return pow(m, keyPair[0], keyPair[1])

def decrypt(c, keyPair=None):
	return pow(c, keyPair[0], keyPair[1])

def generateKeys(size):
	p = nextPrime(random.randint(0, 2 ** size))
	q = nextPrime(random.randint(0, 2 ** size))

	n = p * q
	phi = (p - 1) * (q - 1)
	d = 0
	while not d:
		e = nextPrime(random.randint(0, 10 * size))
		d = modinv(e, phi)

	return (e, n), (d, n)
