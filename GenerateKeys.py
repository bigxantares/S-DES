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



    