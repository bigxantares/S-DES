import queue
import pandas as pd
import itertools  
import time 
import itertools  
import time  
import threading  
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

 # 密钥操作

# P10置换表
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
# P8置换表
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
# P_box_10置换表
P_box_10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
# P_box_8置换表
P_box_8 = [6, 3, 7, 4, 8, 5, 10, 9]


# 得到子密钥key1,key2
def generate_keys(key):

    # 循环左移函数
    def left_shift(lst,n):
        return lst[n:] + lst[:n]

    permuted_key = ['0'] * 10
    for i, pos in enumerate(P10):
        permuted_key[i] = key[pos - 1]

    # 密钥分割，循环左移一位后合并
    left_half = permuted_key[:5]
    right_half = permuted_key[5:]
    left_half = left_shift(left_half,1)
    right_half = left_shift(right_half,1)
    merged_key = left_half + right_half

    # 进行P8置换
    key1 = ''.join([merged_key[i - 1] for i in P8])

    # 循环左移1位+合并
    left_half = left_shift(left_half,1)
    right_half = left_shift(right_half,1)
    merged_key = left_half + right_half

    key2 = ''.join([merged_key[i - 1] for i in P8])
    #返回key1，key2
    return key1, key2






# 将10-bit母密钥拓展成两个8-bit子密钥
class expandKeys:

    def __init__(self, key):
        self.key = key

    def P_10(self):
        key_list = list(self.key)
        tempkey = []
        for i in P_box_10:
            tempkey.append(key_list[i-1])
        res_key = ''.join(tempkey)
        return res_key

    #堆栈操作
    def LeftShift(self, key):
        key_list = list(key)
        left = key_list[:5]
        right = key_list[5:]
        left.append(left[0])
        left.pop(0)
        right.append(right[0])
        right.pop(0)
        tempkey = left + right
        res_key = ''.join(tempkey)
        return res_key

    # 堆栈操作
    def P_8(self, key):
        key_list = list(key)
        tempkey = []
        for i in P_box_8:
            tempkey.append(key_list[i-1])
        res_key = ''.join(tempkey)
        return res_key

# 获取子密钥
def get_keys(mKey):
    keys = expandKeys(mKey)
    key_10 = keys.P_10()
    key_shift1 = keys.LeftShift(key_10)
    childKey1 = keys.P_8(key_shift1)
    key_shift2 = keys.LeftShift(key_shift1)
    childKey2 = keys.P_8(key_shift2)
    cipherKey = [childKey1, childKey2]
    return cipherKey 
  

  
 
  
# 多线程暴力破解实现  
def brute_force_key_worker(ciphertext, plaintext, start, end, result_queue):  
    for key in itertools.product(range(256), repeat=10):  
        key_str = "".join(str(x) for x in key)  
        if start <= int(key_str, 2) < end: 
        
            if Cipher(plaintext, get_keys(key_str)).transfer() == ciphertext:  
                result_queue.put(key_str)  
                return  
    result_queue.put(None)  
  
def brute_force_key(ciphertext, plaintext, num_threads=100):  
    start_time = time.time()  
    result_queue = queue.Queue()  
    thread_pool = []  
    key_range = range(2**10)  
    chunk_size = (2**10) // num_threads  
    for i in range(num_threads):  
        start = i * chunk_size  
        end = (i+1) * chunk_size if i != num_threads-1 else 2**10  
        thread = threading.Thread(target=brute_force_key_worker, args=(ciphertext, plaintext, start, end, result_queue))  
        thread.start()  
        thread_pool.append(thread)  
    for thread in thread_pool:  
        thread.join()  
    end_time = time.time()  
    print(f"用时：{end_time - start_time}秒")  
    while not result_queue.empty():  
        key = result_queue.get()  
        if key is not None:  
            print(f"找到密钥：{key}")  
            return key  
    print("未找到有效密钥")  
    return None  
 
# 单线程暴力破解实现  
def brute_force_1key(ciphertext, plaintext):  
    start_time = time.time()  
    for key in itertools.product(range(256), repeat=10):  
        key_str = "".join(str(x) for x in key) 
        if Cipher(plaintext, get_keys(key_str)).transfer() == ciphertext:  
            end_time = time.time()  
            print(f"找到密钥：{key}，用时：{end_time - start_time}秒")  
            return key  
    print("未找到有效密钥")  
    return None  
  
ciphertext = "00011100"  # 加密后的密文  
plaintext = "11111101"  # 明文  
# 测试多线程暴力破解
key = brute_force_key(ciphertext, plaintext)
# 测试暴力破解
key = brute_force_1key(ciphertext, plaintext) 

