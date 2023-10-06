import pandas as pd
import GenerateKeys

table1 = { '00': ['01', '11', '00', '11'], '01': ['00', '10', '10', '01'], '10': ['11', '01', '01', '00'], '11': ['10', '00', '11', '10']}
table2 = { '00': ['00', '10', '11', '10'], '01': ['01', '11', '00', '01'], '10': ['10', '01', '01', '00'], '11': ['11', '00', '10', '11']}
rowIndex1 = ['00', '01', '10', '11']
rowIndex2 = ['00', '01', '10', '11']
IP_box = [2, 6, 3, 1, 4, 8, 5, 7]
EP_box = [4, 1, 2, 3, 2, 3, 4, 1]
SP_box= [2, 4, 3, 1]
FP_box = [4, 1, 3, 5, 7, 2, 8, 6]
EPBox = [4, 1, 2, 3, 2, 3, 4, 1]
SBox1 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 0, 2]]
SBox2 = [[0, 1, 2, 3], [2, 3, 1, 0], [3, 0, 1, 0], [2, 1, 0, 3]]

#encrypt  加密部分

S_box1 = pd.DataFrame(table1, index=rowIndex1)
S_box2 = pd.DataFrame(table2, index=rowIndex2)

    #明文转换函数
def PlainTextTransfer(plaintext:str, form):
    if form == 'Binary':
        return plaintext
    else:
        res = str()
        for i in plaintext:
            res += format(ord(i), '08b')
        return res

    # 密文转换函数
def CipherTextTransfer(ciphertext:str, form):
    if form == 'Binary':
        return ciphertext
    else:
        res = str()
        for i in range(0, len(ciphertext),8):
            res += chr(int(ciphertext[i:i+8],2))
        return res

def Transfers(ciphertext: str):
    res = str()
    for i in range(0, len(ciphertext), 8):
         res += chr(int(ciphertext[i:i + 8], 2))
    return res
    
    #加密操作
class Cipher:
    def __init__(self, plaintext, keys):
        # 导入子密钥列表
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

        subs_value = ''
        for i in range(0, len(subplaintext), 8):
            temp_right = []
        for j in EP_box:
            temp_right.append(subplaintext[i + 4 + j - 1])
        temp_right = ''.join(temp_right)
        temp_text = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(temp_right, self.keys[flag_key]))
        subs_value += S_box1.loc[temp_text[0] + temp_text[3], temp_text[1] + temp_text[2]] + S_box2.loc[
            temp_text[4] + temp_text[7], temp_text[5] + temp_text[6]]

        value_lst = list(subs_value)
        temp = []
        for i in SP_box:
            temp.append(value_lst[i-1])
        temp = ''.join(temp)
        left = ''.join(left)
        en_left = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(temp, left))
        right = ''.join(right)
        #判断
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
        # print(pt_lst)
        res = []
        for i in pt_lst:
            i = self.IP(i)
            i = self.funcionEncrypt(i, 0)
            i = self.funcionEncrypt(i, 1)
            i = self.FP(i)
            res.append(i)
        res = ''.join(res)
        return res


# decrypt  解密部分
    
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
    return format(sbox[row][col], '02b')  # 以二进制格式返回

# 输入函数
def F(right_half, key):
    # 从4bit扩展为8bit
    expanded_half = ''.join([right_half[i - 1] for i in EPBox])

    # 异或操作
    xored_half = xor_bits(expanded_half, key)

    # 分为两部分
    left_xored_half = xored_half[:4]
    right_xored_half = xored_half[4:]

    # S-盒替换
    sbox_output_left = sbox_substitution(left_xored_half, SBox1)
    sbox_output_right = sbox_substitution(right_xored_half, SBox2)

    # SPBox置换
    SPBox_output = permute_SPBox(sbox_output_left + sbox_output_right)

    return SPBox_output

# 解密函数
def decrypt(ciphertext, key1, key2):

    initial_permuted = initial_permutation(ciphertext)

    left_half = initial_permuted[:4]
    right_half = initial_permuted[4:]

    f1_output = F(right_half, key2)

    left_output = xor_bits(left_half, f1_output)

    left_half, right_half = right_half, left_output

    f2_output = F(right_half, key1)
    left_output2 = xor_bits(left_half, f2_output)

    merged_half = left_output2 + right_half

    # 初始逆置换
    plaintext = final_permutation_inv(merged_half)

    return plaintext

 #选择返回结果函数
def user_decryption(symbol,ciphertext, key):
    if symbol=="Binary":
        return Bdecrypt(ciphertext, key)
    else:
        return Adecrypt(ciphertext, key)


# 对ASCII字符串进行解密
def Adecrypt(cipher, key):
    key1, key2 = GenerateKeys.generate_keys(key)
    TEXT = ""
    for char in cipher:
        ciphertext = format(ord(char), '08b')
        TEXT_1 = decrypt(ciphertext, key1, key2)
        Char = chr(int(TEXT_1, 2))
        TEXT = TEXT + Char

    return TEXT

# 对二进制字符串进行解密
def Bdecrypt(cipher, key):
    length=len(cipher)
    key1, key2 = GenerateKeys.generate_keys(key)
    number = length // 8
    TEXT = ""
    for i in range(0, length, 8):
        group = cipher[i:i + 8]
        pGroup = decrypt(group, key1, key2)
        TEXT = TEXT + pGroup
    return TEXT



        
