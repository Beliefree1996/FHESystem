# -*- coding: utf-8 -*-

import sympy
from Crypto.Random import random
from Crypto.Util.number import getPrime


def findModReverse(a, m):  # 扩展欧几里得算法求模逆 ax=1mod m
    a = int(a)
    if gcd(a, m) != 1 and gcd(a, m) != -1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def gcd(a, b):  # 欧几里得求a和b的最大公因数
    if a % b == 0:
        return b
    else:
        return gcd(b, a % b)


def lcm(a, b):
    return a // gcd(a, b) * b


def L(u, n):
    if (u - 1) % n > 0:
        return None
    return (u - 1) // n

def powmod(a, b, c):
    a = a % c
    ans = 1
    b = int(b)
    while b != 0:
        if int(b) & 1:
            ans = (ans * a) % c
        b >>= 1
        a = (a * a) % c
    return ans

def paillier_encryption(m, g, r, n):  # 加密运算
    c = powmod(g, m, n ** 2) * powmod(r, n, n ** 2) % (n ** 2)
    return c


def paillier_decryption(c, g, lamda, n, u):
    m = L(powmod(c, lamda, n ** 2), n) * u % n
    return m


def key_generation():
    p = getPrime(512)
    q = getPrime(512)
    if p == q:
        q = getPrime(128)
    n = p * q
    lamda = lcm(p - 1, q - 1)
    # print(lamda)

    while gcd(n, lamda) > 1:
        q = getPrime(512)
        if p == q:
            q = getPrime(128)
        n = p * q
        lamda = lcm(p - 1, q - 1)

    g = n + 1
    r = random.randint(1, n)

    u = findModReverse(L(powmod(g, lamda, n ** 2), n), n)
    # print(g)
    return n, g, r, lamda, u


def paillier_generation():
    n, g, r, lamda, u = key_generation()
    return n, g, r, lamda, u


# if __name__ == "__main__":
#     n, g, r, lamda, u = paillier_generation()  # 密钥生成 n,g公钥 lamda，v私钥
#
#     m = 10001
# print("n", n)
# print("g", g)
# print("r", r)
# print("lamda", lamda)
# print("u", u)
# c = paillier_encryption(m, r, n)  # 加密函数
# m = paillier_decryption(c, g, lamda, n, u)  # 解密函数
# print(c)
# print(m)
