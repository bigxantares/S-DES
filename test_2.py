import pandas as pd
import itertools  
import time 

table1 = { '00': ['01', '11', '00', '11'], '01': ['00', '10', '10', '01'], '10': ['11', '01', '01', '00'], '11': ['10', '00', '11', '10']}
table2 = { '00': ['00', '10', '11', '10'], '01': ['01', '11', '00', '01'], '10': ['10', '01', '01', '00'], '11': ['11', '00', '10', '11']}
rowIndex1 = ['00', '01', '10', '11']
rowIndex2 = ['00', '01', '10', '11']
IP_box = [2, 6, 3, 1, 4, 8, 5, 7]
EP_box = [4, 1, 2, 3, 2, 3, 4, 1]
SP_box = [2, 4, 3, 1]
FP_box = [4, 1, 3, 5, 7, 2, 8, 6]
SBox1 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 0, 2]]
SBox2 = [[0, 1, 2, 3], [2, 3, 1, 0], [3, 0, 1, 0], [2, 1, 0, 3]]

# 加密部分

S_box1 = pd.DataFrame(table1, index=rowIndex1)
S_box2 = pd.DataFrame(table2, index=rowIndex2)



# 加密操作
class Cipher:
    def __init__(self, plaintext, keys):
        self.plaintext = plaintext
        self.keys = keys

    # 分裂函数
    def split(self, plaintext):
        pt_list = []     # 分组列表: 存储每一个8-bit子串
        length = len(plaintext)
        if length % 8 == 0:
            for i in range(0, length, 8):
                pt_list.append(plaintext[i:i+8])
        else:
            for i in range(0, length - 8, 8):
                pt_list.append(plaintext[i:i+8])
            rest = length % 8
            pt_list.append('0' * (8-rest) + plaintext[length - rest:])
        return pt_list

    # 初始置换函数
    def IP(self, subplaintext):
        text_lst = list(subplaintext)
        tmp_text = []
        for i in IP_box:
            tmp_text.append(text_lst[i-1])
        res_text = ''.join(tmp_text)
        return res_text

    # 8-bit分组加密函数
    def funcionEncrypt(self, subplaintext, flag_key):
        text_list = list(subplaintext)
        left = text_list[:4]
        right = text_list[4:]

        temp_right = []
        for i in EP_box:
            temp_right.append(right[i-1])
        temp_right = ''.join(temp_right)
        temp_text = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(temp_right, self.keys[flag_key]))
       
        subs_value = S_box1.loc[temp_text[0]+temp_text[3], temp_text[1:3]] + S_box2.loc[temp_text[4]+temp_text[7], temp_text[5:7]]

        value_lst = list(subs_value)
        temp = []
        for i in SP_box:
            temp.append(value_lst[i-1])
        temp = ''.join(temp)
        left = ''.join(left)
        en_left = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(temp, left))
        right = ''.join(right)
        if flag_key == 0:
            return right + en_left
        else:
            return en_left + right

    # 最终置换函数
    def FP(self, subplaintext):
        text_lst = list(subplaintext)
        temp_text = []
        for i in FP_box:
            temp_text.append(text_lst[i-1])
        res_text = ''.join(temp_text)
        return res_text

    # 处理加密结果
    def transfer(self):
        pt_lst = self.split(self.plaintext)
        res = []
        for i in pt_lst:
            i = self.IP(i)
            i = self.funcionEncrypt(i, 0)
            i = self.funcionEncrypt(i, 1)
            i = self.FP(i)
            res.append(i)
        res = ''.join(res)
        return res

# 逐位异或操作函数
def xor_bits(a, b):
    result = ""
    for i in range(len(a)):
        result += str(int(a[i]) ^ int(b[i]))
    return result

# 初始逆置换函数
def initial_permutation(ciphertext):
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    return ''.join(ciphertext[i - 1] for i in IP)

# 最终逆置换函数
def final_permutation_inv(ciphertext):
    IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
    return ''.join([ciphertext[i - 1] for i in IP_inv])

# SPBox置换函数
def permute_SPBox(input_text):
    SPBox = [2, 4, 3, 1]
    return ''.join([input_text[i - 1] for i in SPBox])

# S-盒替换函数
def sbox_substitution(input_text, sbox):
    row = int(input_text[0] + input_text[3], 2)
    col = int(input_text[1] + input_text[2], 2)
    return format(sbox[row][col], '02b')

  
  
# 生成随机密钥和明文  
import random  
def generate_random_key():  
    return "".join(str(random.randint(0, 1)) for _ in range(10))  
  
def generate_random_plaintext():  
    return "".join(str(random.randint(0, 1)) for _ in range(8))  
  
# 测试封闭性  
def test_closure():  
    # 生成随机密钥和明文  
    key = generate_random_key()  
    plaintext = generate_random_plaintext()  
    ciphertext = Cipher(plaintext, key).transfer  
      
    # 使用不同密钥加密明文，检查是否存在不同密钥产生相同密文的情况  
    key2 = generate_random_key()  
    while key2 == key:  
        key2 = generate_random_key()  
    ciphertext2 = Cipher(plaintext, key2).transfer  
    if ciphertext != ciphertext2:
        print ('k1',key)
        print('k2',key2)
        print("不同密钥产生了相同的密文！"  )
      
    # 使用相同密钥加密不同明文，检查是否存在相同密钥产生相同密文的情况  
    plaintext2 = generate_random_plaintext()  
    while plaintext2 == plaintext:  
        plaintext2 = generate_random_plaintext()  
    ciphertext3 = Cipher(plaintext2, key).transfer  
    if ciphertext != ciphertext3:
        print('明文1',plaintext)
        print('明文2',plaintext2)
        print("相同密钥产生了相同的密文！"  )
  
# 运行封闭性测试  
test_closure()
