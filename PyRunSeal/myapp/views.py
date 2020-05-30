from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.utils.six import BytesIO
import requests
import json
import time
import os
import psutil
# import face_recognition
import hashlib
import base64
# 引入Seal包
#from . import paillier


# Create your views here.

def test(request):
    if request.method == "GET":
        a = request.GET.get("a")
        b = request.GET.get("b")
        c = a + b
    return JsonResponse({
        "status_code": 0,
        "data": c
    })
'''
from seal import *
from seal_helper import *


def BFV_kengen():
# 返回公钥public_key，relin_keys，密钥secret_key和context。
# 其中算法的任何操作都要用到这个context。一组钥匙对应一个context。计算时需要用到relin_keys
# 可以把context和relin_keys也理解为公钥
    parms = EncryptionParameters(scheme_type.BFV)
    poly_modulus_degree = 4096
    parms.set_poly_modulus_degree(poly_modulus_degree)
    parms.set_coeff_modulus(CoeffModulus.BFVDefault(poly_modulus_degree))
    parms.set_plain_modulus(256)
    context = SEALContext.Create(parms)
    keygen = KeyGenerator(context)
    public_key = keygen.public_key()
    secret_key = keygen.secret_key()
    relin_keys = keygen.relin_keys()
    return  public_key,relin_keys,secret_key,context


def BFV_Encrypt(x,public_key,context):  # x是要加密的明文,应该是int型整数，public_key是公钥，返回x对应的密文类
    x = str(x)
    encryptor = Encryptor(context, public_key)
    x_encrypted = Ciphertext()
    x_plain = Plaintext(x)
    encryptor.encrypt(x_plain, x_encrypted)
    return x_encrypted


def BFV_Decrypt(x_encrypted,secret_key, context):  # x_encrypted是明文x对应的密文类，secret_key是密钥，返回x_encrypted对应的明文
    decryptor = Decryptor(context, secret_key)
    x_decrypted = Plaintext()
    decryptor.decrypt(x_encrypted, x_decrypted)
    return x_decrypted.to_string()


def BFV_add(x_encrypted, y_encrypted, relin_keys, context):  # x_encrypted,y_encrypted是明文x，y对应的密文类，返回x+y对应的密文类
    evaluator = Evaluator(context)
    add_encrypted = Ciphertext()
    plain_zero = Plaintext("0")
    evaluator.add_plain(x_encrypted, plain_zero, add_encrypted)
    evaluator.add_inplace(add_encrypted, y_encrypted)
    evaluator.relinearize_inplace(add_encrypted, relin_keys)
    return add_encrypted


def BFV_mul(x_encrypted, y_encrypted, relin_keys, context):  # x_encrypted,y_encrypted是明文x，y对应的密文类，返回x*y对应的密文类
    evaluator = Evaluator(context)
    mul_encrypted = Ciphertext()
    plain_zero = Plaintext("0")
    evaluator.add_plain(x_encrypted, plain_zero, mul_encrypted)
    evaluator.multiply_inplace(mul_encrypted, y_encrypted)
    evaluator.relinearize_inplace(mul_encrypted, relin_keys)
    return mul_encrypted



def CKKS_kengen():
# 返回公钥public_key，relin_keys，密钥secret_key和context。
# 其中BFV算法的任何操作都要用到这个context。一组钥匙对应一个context。计算时需要用到relin_keys
# 可以把context和relin_keys也理解为公钥
    parms = EncryptionParameters(scheme_type.CKKS)
    poly_modulus_degree = 8192
    parms.set_poly_modulus_degree(poly_modulus_degree)
    parms.set_coeff_modulus(CoeffModulus.Create(
        poly_modulus_degree, [40, 40, 40, 40, 40]))
    context = SEALContext.Create(parms)
    keygen = KeyGenerator(context)
    public_key = keygen.public_key()
    secret_key = keygen.secret_key()
    relin_keys = keygen.relin_keys()
    return public_key, relin_keys, secret_key, context


def CKKS_Encrypt(x, public_key, context):  # x是要加密的明文，public_key是公钥，返回x对应的密文类
    encryptor = Encryptor(context, public_key)
    encoder = CKKSEncoder(context)
    inputs = DoubleVector([x])
    plain = Plaintext()
    scale = pow(2.0, 30)
    encoder.encode(inputs, scale, plain)
    encrypted = Ciphertext()
    encryptor.encrypt(plain, encrypted)
    return encrypted

def CKKS_Decrypt(x_encrypted,secret_key,context):  # x_encrypted是明文x对应的密文类，secret_key是密钥，返回x_encrypted对应的明文
    decryptor = Decryptor(context, secret_key)
    encoder = CKKSEncoder(context)
    x_decrypted = Plaintext()
    output = DoubleVector()
    decryptor.decrypt(x_encrypted, x_decrypted)
    encoder.decode(x_decrypted, output)
    return output[0]

def CKKS_add(x_encrypted, y_encrypted,relin_keys, context):  # x_encrypted,y_encrypted是明文x，y对应的密文类，返回x+y对应的密文类
    evaluator = Evaluator(context)
    add_encrypted = Ciphertext()
    evaluator.add(x_encrypted, y_encrypted, add_encrypted)
    evaluator.relinearize_inplace(add_encrypted, relin_keys)
    return add_encrypted


def CKKS_mul(x_encrypted, y_encrypted, relin_keys, context):  # x_encrypted,y_encrypted是明文x，y对应的密文类，返回x*y对应的密文类
    evaluator = Evaluator(context)
    mul_encrypted = Ciphertext()
    evaluator.multiply(x_encrypted, y_encrypted, mul_encrypted)
    evaluator.relinearize_inplace(mul_encrypted, relin_keys)
    return mul_encrypted


if __name__ == '__main__':
    pub1, rel1, sec1, con1 = BFV_kengen()
    pub2, rel2, sec2, con2 = CKKS_kengen()
    x = 6
    y = 11
    print("BFV:")
    Cipher_x = BFV_Encrypt(x, pub1, con1)
    Cipher_y = BFV_Encrypt(y, pub1, con1)
    Cipher_add = BFV_add(Cipher_x, Cipher_y, rel1, con1)
    Cipher_mul = BFV_mul(Cipher_x, Cipher_y, rel1, con1)
    print(BFV_Decrypt(Cipher_x, sec1, con1), "+", BFV_Decrypt(Cipher_y, sec1, con1), "=",
          BFV_Decrypt(Cipher_add, sec1, con1))
    print(BFV_Decrypt(Cipher_x, sec1, con1), "*", BFV_Decrypt(Cipher_y, sec1, con1), "=",
          BFV_Decrypt(Cipher_mul, sec1, con1))

    print("CKKS:")
    Cipher_x = CKKS_Encrypt(x, pub2, con2)
    Cipher_y = CKKS_Encrypt(y, pub2, con2)
    Cipher_add = CKKS_add(Cipher_x, Cipher_y, rel2, con2)
    Cipher_mul = CKKS_mul(Cipher_x, Cipher_y, rel2, con2)
    print(CKKS_Decrypt(Cipher_x, sec2, con2), "+", CKKS_Decrypt(Cipher_y, sec2, con2), "=",
          CKKS_Decrypt(Cipher_add, sec2, con2))
    print(CKKS_Decrypt(Cipher_x, sec2, con2), "*", CKKS_Decrypt(Cipher_y, sec2, con2), "=",
          CKKS_Decrypt(Cipher_mul, sec2, con2))
    CKKS_Decrypt(Cipher_x, sec2, con2)

'''
