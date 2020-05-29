# -*- coding: utf-8 -*-

import sympy
from Crypto.Random import random




def MatrixModP(A, ms, ns, mods):  # m行#n列的矩阵A每个元素模p
    for i in range(0,ms):
        for j in range(0,ns):
            A[i][j] =  A[i][j] % mods
    return A

def gcd(a, b):   #欧几里得求a和b的最大公因数
    if a % b == 0:
        return b
    else:
        return gcd(b, a % b)

def findModReverse(a, m):  # 扩展欧几里得算法求模逆 ax=1mod m
    a=int(a)
    if gcd(a, m) != 1 and gcd(a, m) != -1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def CreatBigRandomMatrix(a,b,M,N): #生成M*N的大数随机矩阵，元素范围是[a,b)
    sequence=[]
    for i in range(a,b):
        sequence.append(i)
    Matrix = [[] for i in range(M)]  # 创建的是M行的二维列表
    for i in range(0,M):
        for j in range(0,N):
            Matrix[i].append(random.choice(sequence))
    return Matrix

def MatrixDot(A,B,ms,o,ns,mods):#计算矩阵乘法,A是m*o的矩阵，B是o*n的矩阵
    Matrix = [[] for i in range(ms)]  # 创建的是M行的二维列表
    for i in range(0, ms):
        for j in range(0, ns):
            Matrix[i].append(0)
    for i in range(0,ms):
        for j in range(0,ns):
            for k in range(0,o):
                Matrix[i][j]=Matrix[i][j]+A[i][k]*B[k][j]
    Matrix = MatrixModP(Matrix, ms, ns, mods)
    return Matrix

def MatrixAdd(A,B,ms,ns,mods):  #代替np,add做矩阵加法
    Matrix = [[] for i in range(ms)]  # 创建的是M行的二维列表
    for i in range(0, ms):
        for j in range(0, ns):
            Matrix[i].append(0)
    for i in range(0, ms):
        for j in range(0, ns):
            Matrix[i][j]=A[i][j]+B[i][j]
    Matrix = MatrixModP(Matrix, ms, ns, mods)
    return Matrix

def MatrixSub(A,B,ms,ns,mods):  #矩阵减法
    Matrix = [[] for i in range(ms)]  # 创建的是M行的二维列表
    for i in range(0, ms):
        for j in range(0, ns):
            Matrix[i].append(0)
    for i in range(0, ms):
        for j in range(0, ns):
            Matrix[i][j]=A[i][j]-B[i][j]
    Matrix = MatrixModP(Matrix, ms, ns, mods)
    return Matrix

def MatrixConcatenate(A,B,ns):  #代替np.concatenate((left,right),axis=1)组合两个矩阵
    Matrix = [[] for i in range(ns)]  # 创建的是M行的二维列表
    for i in range(0, ns):
        for j in range(0, 2*ns):
            Matrix[i].append(0)
    for i in range(0, ns):
        for j in range(0, ns):
            Matrix[i][j]=A[i][j]
    for i in range(0, ns):
        for j in range(ns, 2*ns):
            Matrix[i][j]=B[i][j-ns]
    return Matrix

def matrix_inv(Matrix2,N,mods):  #mod mods求逆
    Matrix = [[] for i in range(N)]  # 创建的是N行的二维列表
    for i in range(N):
        for j in range(N):
            Matrix[i].append(Matrix2[i][j])
    Matrix = MatrixModP(Matrix, N, N, mods)
    E = CreatBigRandomMatrix(0, mods, N, N)
    for i in range(0,N):
        for j in range(0, N):
            if i==j:
                E[i][j]=1
            else:
                E[i][j]=0
    Matrix1=MatrixConcatenate(Matrix,E,N)
    Invert=calculate_parameter(Matrix1,N,mods)  #高斯消元求逆，返回的是[E|A^-1]
    for i in range(0,N):
        for j in range(0, N):
            Matrix[i][j]=Invert [i] [ j+N ]  # 截取 [E|A-1] 中的A-1
    return Matrix

def calculate_parameter(data,N,mods):  #高斯消元
    data = MatrixModP(data, N, 2*N, mods)
    line_size = len(data)
    rol_size = len(data[0])
    for i in range(0, line_size):
        if data[i][i] != 0:
            flag = i
        else:
            flag = -1
            for j in range(i + 1, line_size):
                if data[j][i] != 0:
                    flag = j
                    break
        if flag == -1:
            return None
        else:
            t = data[i]
            data[i] = data[flag]
            data[flag] = t
        data = MatrixModP(data, N, N, mods)
        for j in range(i + 1, line_size):
            for k in range(0, rol_size):
                if k != i and data[i][i] != 0:
                    data[j][k] = ((data[j][k] - data[i][k] * data[j][i] * findModReverse(data[i][i], mods)) % mods + mods) % mods
            data[j][i] = ((data[j][i] - data[i][i] * data[j][i] * findModReverse(data[i][i], mods)) % mods + mods) % mods

    # data已经变为上三角矩阵，接下来吧上三角化为对角矩阵
    i = line_size - 1  #消元的那一行
    while i >= 0:
        for x in range(i+1,line_size):
            tmp = ((data[i][x] * findModReverse(data[x][x],mods)%mods)%mods+mods)%mods
            data[i][x]=0
            for y in range(line_size,rol_size):
                data[i][y]=((data[i][y]-data[x][y]*tmp)%mods+mods)%mods
        i -= 1
    #对角矩阵化为单位矩阵
    data=MatrixModP(data,N,N,mods)
    for i in range(0,line_size):
        for j in range(line_size,rol_size):
            data[i][j]=(data[i][j]*findModReverse(data[i][i],mods)%mods+mods)%mods
    return data

def CanInvert(data1,N,mods):   #判断N*N的矩阵是否可逆，可上三角化即可逆
    data1 = MatrixModP(data1, N, N, mods)
    data = [[] for i in range(N)]  # 创建的是N行的二维列表
    for i in range(N):
        for j in range(N):
            data[i].append(data1[i][j])
    line_size = len(data)
    rol_size = len(data[0])
    for i in range(0,line_size):
        if data[i][i]!=0:
            flag=i
        else:
            flag=-1
            for j in range(i+1,line_size):
                if data[j][i]!=0:
                    flag=j
                    break
        if flag==-1:
            return 0
        else:
            t=data[i]
            data[i]=data[flag]
            data[flag]=t
        data=MatrixModP(data,N,N,mods)
        for j in range(i+1,line_size):
            for k in range(0,rol_size):
                if k!=i and data[i][i]!=0:
                    data[j][k]=((data[j][k]-data[i][k]*data[j][i]*findModReverse(data[i][i],mods))%mods+mods)%mods
            data[j][i] = ((data[j][i] - data[i][i] * data[j][i] * findModReverse(data[i][i], mods)) % mods + mods) % mods
    return 1

def CreatDhard(N,mods):
    Dhard = CreatBigRandomMatrix(-1, 1, N, N)
    for i in range(N):
        for j in range(N):
            #Dhard[i][j]=1
            if Dhard[i][j] == 0:
                Dhard[i][j] = 1
            if i==j:
                Dhard[i][j]=mods
    return Dhard

def CreatDsoft(N,n):
    Dsoft=list()
    for k in range(n):
        #Dsofti=np.random.randint(-1,1,(N,N))
        Dsofti=CreatBigRandomMatrix(-1, 1, N, N)#n次复用
        for i in range(N):
            for j in range(N):
                if Dsofti[i][j]==0:
                    Dsofti[i][j]=1
        Dsoft.append(Dsofti)
    return Dsoft

def CreatDeta(N,mods):  #可逆
    #Deta= np.random.randint(0, p, (N, N))
    Deta=CreatBigRandomMatrix(0, mods, N, N)
    #while np.linalg.matrix_rank(Deta) != N:
        #Deta = np.random.randint(0, p, (N, N))
    while CanInvert(Deta,N,mods)==0:
        Deta=CreatBigRandomMatrix(0, mods, N, N)
    return Deta

def CreatA(N,mods):  #可逆
    #A = np.random.randint(0, p, (N, N))
    #while np.linalg.matrix_rank(A) != N:
        #A = np.random.randint(0, p, (N, N))
    A=CreatBigRandomMatrix(0, mods, N, N)
    while CanInvert(A,N,mods)==0:
        A=CreatBigRandomMatrix(0, mods, N, N)
    return A

def CreatB(N,mods):
    #B = np.random.randint(0, p, (N, N))
    B=CreatBigRandomMatrix(0, mods, N, N)
    return B

def CreatPhard(N,mods):
    Phards=CreatBigRandomMatrix(0, mods, N, N)
    while CanInvert(Phards,N,mods)==0:
        Phards=CreatBigRandomMatrix(0, mods, N, N)
    return Phards

def CreatPsoft(N,ns,mods):
    Psoftss=list()
    for k in range(ns):
        Psoftssi = CreatBigRandomMatrix(0, mods, N, N)
        while CanInvert(Psoftssi,N, mods) == 0:
            Psoftssi = CreatBigRandomMatrix(0, mods, N, N)
        Psoftss.append(Psoftssi)
    return Psoftss

def CreatShard(Phard,A,B,Dhard,Deta,N,mods):
    left=MatrixDot(Phard,A,N,N,N,mods)
    right = MatrixDot(Phard, B, N, N, N,mods)
    right=MatrixAdd(right,Dhard,N,N,mods)
    Shard=MatrixConcatenate(left,right,N)
    Shard=MatrixDot(Shard, Deta, N, 2 * N, 2 * N,mods)
    return Shard

def CreatSsoft(Psoft,A,B,Dsoft,Deta,N,n,mods):
    Ssoft=list()
    for i in range(n):
        left = MatrixDot(Psoft[i], A, N, N, N, mods)
        right = MatrixDot(Psoft[i], B, N, N, N, mods)
        right = MatrixAdd(right, Dsoft[i], N, N, mods)
        ans = MatrixConcatenate(left, right, N)
        ans = MatrixDot(ans, Deta, N, 2 * N, 2 * N, mods)
        Ssoft.append(ans)
    return Ssoft

def CreatMhard(Shard):
    Mhard = Shard
    return Mhard

def CreatMsoft(Ssoft):
    return Ssoft

def CreatRandomNumbers(N,ns,maxx):
    random_numberss=list()
    for i in range(ns):
        ans=CreatBigRandomMatrix(0, maxx, 1, N)
        random_numberss.append(ans)
    return random_numberss

def lattice_encryption(plaintext, Mhard, Msoft,random_numbers, N, ns,mods): #加密运算
    temp=list()
    temp.append(plaintext)
    ciphertext=MatrixDot(temp,Mhard,1,N,2*N,mods)
    for i in range(ns):
        add=MatrixDot(random_numbers[i],Msoft[i],1,N,2*N,mods)
        ciphertext=MatrixAdd(ciphertext,add,1,2*N,mods)
    return ciphertext #Deta,A,B

def lattice_decryption(ciphertexts, Deta, A, B, N, mods, qq):
    m = []
    ciphertexts = MatrixDot(ciphertexts,matrix_inv(Deta,2*N, mods), 1, 2*N, 2*N,mods)
    ciphertext = ciphertexts[0]
    CD = []
    CU = []
    for i in range(N,2*N):
        CD.append(ciphertext[i])
    for i in range(0, N):
        CU.append(ciphertext[i])
    temp1=list()
    temp1.append(CU)
    temp2 = list()
    temp2.append(CD)
    e = MatrixDot(MatrixDot(temp1,matrix_inv(A,N,mods),1,N,N,mods),B,1,N,N,mods)
    e = MatrixSub(temp2,e,1,N,mods)
    for i in  range(0,N):
        # 注意负数部分
        if e[0][i] % mods > mods - qq/2: # 这里只有为明文为0才会得到走这一步.
            e[0][i] = e[0][i] % mods - mods
        #开始处理
        linshi = e[0][i] % qq
        if linshi < qq / 2:
            m.append((e[0][i]- linshi)//qq)
        else:
            m.append((e[0][i] + qq - linshi) // qq)
    return m

def lattice_generation(N,n,p,q,sigema_max):
    #一些参数初始化#
    Deta=CreatDeta(2*N,p)
    A=CreatA(N,p)
    B=CreatB(N,p)
    Dhard=CreatDhard(N,q)
    Dsoft=CreatDsoft(N,n)
    Phard=CreatPhard(N,p)
    Psoft=CreatPsoft(N,n,p)
    Shard=CreatShard(Phard,A,B,Dhard,Deta,N,p)
    Ssoft=CreatSsoft(Psoft,A,B,Dsoft,Deta,N,n,p)
    Mhard=CreatMhard(Shard)
    Msoft=CreatMsoft(Ssoft)
    random_numbers=CreatRandomNumbers(N,n,sigema_max)
    return Mhard,Msoft,random_numbers,Deta,A,B

def key_generartion():
    r = 2  # 明文每一维属于[0,r-1] #其实可以把r改成3,则r-2上运算即可,
    # 运算一定2进制,明文的范围不是[0,r-1]而是[0,1], 而最多的加法运算次数只有r次.
    N = 20  # 明文维度
    n = 4  # 噪声的个数/参与者的个数
    sigema_max = 1024
    l_0 = n * N * sigema_max + (N - 1) * r
    l = pow(2, 4)  # 最大同态计算次数
    q = 2 * l_0
    p = sympy.nextprime(q * r * (2 * l + 1))
    sigma = p - q * r * (2 * l + 1)  # sigma < l_0

    Mhard, Msoft, random_numbers, Deta, A, B = lattice_generation(N, n, p, q, sigema_max)  # 从这里调用 Deta A  B

    return N, l, Mhard, Msoft, random_numbers, p, Deta, A, B, q , n, sigema_max, l_0, sigma, r

def  long_to_two(plaintextnum,N):
    plaintext=[]
    for i in range(N):
        if plaintextnum==0:
            plaintext.append(0)
        else:
            if plaintextnum%2==1:
                plaintext.append(1)
                plaintextnum = (plaintextnum-1) // 2
            else:
                plaintext.append(0)
                plaintextnum = plaintextnum // 2
    plaintext.reverse()
    return  plaintext

def  two_to_long(plaintext,N):
    plaintextnum = 0
    for i in range(N):
        if plaintext[i] == 0:
            plaintextnum = plaintextnum * 2
        else:
            plaintextnum = plaintextnum * 2 + plaintext[i]
    return plaintextnum

def jiemijinwei(plaintext,r):#用来对最后的计算向量进行进位的
    jinwei = 0
    for i in range(N-1, -1, -1):
        plaintext[i] = (int)(plaintext[i] + jinwei)
        if plaintext[i] >= r:
            jinwei = plaintext[i] - plaintext[i] % r
            jinwei = jinwei/ r
            plaintext[i] = plaintext[i] % r
        else:
            jinwei = 0
    return plaintext

# if __name__ == "__main__":
#     N, l, Mhard, Msoft, random_numbers, p, Deta, A, B, q, n, sigema_max, l_0, sigma, r = key_generartion()#密钥生成
#     #N,l,Mhard,Msoft,random_numbers,p是公钥
#     # Deta, A, B, N, q是私钥
#
#     #print("q=",q)
#     #print("sigma=",p-q*r*(2*l+1))
#     #print("l_0=", l_0)
#
#
#
#     # 数据输入测试模块
#     plaintextnum1 = 0#420
#     plaintextnum2 = 1021
#     plaintextnum3 = 101
#     plaintextnum4 = 592
#
#     plaintext1 = long_to_two(plaintextnum1,N)
#     plaintext2 = long_to_two(plaintextnum2,N)
#     plaintext3 = long_to_two(plaintextnum3,N)
#     plaintext4 = long_to_two(plaintextnum4,N)
#
#     print('未加密的明文是', plaintext1)
#     print('未加密的明文是', plaintext2)
#     print('未加密的明文是', plaintext3)
#     print('未加密的明文是', plaintext4)
#
#     ciphertext1 = lattice_encryption(plaintext1, Mhard, Msoft,random_numbers, N,n, p)
#     print("加密的密文是:", ciphertext1)
#     plaintext1 = lattice_decryption(ciphertext1, Deta, A, B, N, p, q)
#     print("解密的明文是:", plaintext1)
#
#     ciphertext2 = lattice_encryption(plaintext2, Mhard, Msoft,random_numbers, N,n, p)
#     print("加密的密文是:", ciphertext2)
#     plaintext2 = lattice_decryption(ciphertext2, Deta, A, B, N, p, q)
#     print("解密的明文是:", plaintext2)
#
#     ciphertext3 = lattice_encryption(plaintext3, Mhard, Msoft,random_numbers, N,n, p)
#     print("加密的密文是:", ciphertext3)
#     plaintext3 = lattice_decryption(ciphertext3, Deta, A, B, N, p, q)
#     print("解密的明文是:", plaintext3)
#
#     ciphertext4 = lattice_encryption(plaintext4, Mhard, Msoft,random_numbers, N,n, p)
#     print("加密的密文是:", ciphertext4)
#     plaintext4 = lattice_decryption(ciphertext4, Deta, A, B, N, p, q)
#     print("解密的明文是:", plaintext4)
#
#     ######同态调试
#     print("明文和为",plaintextnum3+plaintextnum4)
#     sum = plaintextnum3 + plaintextnum4
#     sum_plaintext = long_to_two(sum,N)
#     sum_ciphertext = lattice_encryption(sum_plaintext, Mhard, Msoft, random_numbers, N, n, p)
#     print("明文3和4之和的密文是:", sum_ciphertext)
#     sum_plaintext = lattice_decryption(sum_ciphertext, Deta, A, B, N, p, q)
#     print("其解密的明文是:", sum_plaintext)
#
#
#     sum_plaintext = lattice_decryption(MatrixAdd(ciphertext3,ciphertext4,1,2*N,p), Deta, A, B, N, p, q)
#     #进位一次
#     sum_plaintext = jiemijinwei(sum_plaintext,r)
#     print("密文3和4之和解密的明文是:",sum_plaintext )
#     print("密文3和4之和解密的明文是:", two_to_long(sum_plaintext,N))