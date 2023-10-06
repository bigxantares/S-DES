# S-DES

## 第一关：基本测试

### 1.1 GUI界面设计：

使用PYQT5技术设计gui界面，具有明文，密文，密钥的输入框和结果的输出框，同时具有二进制的加密解密和ASCII的加密解密按钮，同时具有将结果转化为ASCII码和16进制的功能。

![2 QCLSPCYLCEEDV3@1)1CCP](https://github.com/bigxantares/S-DES/assets/116985680/67c7cbb8-0e0e-47c6-b7ca-3d64b426c207)

### 1.2 使用测试用例进行测试：

测试明文：10111001 

密钥：1000101010

测试密文：01011000

加密测试结果为：

![1](https://github.com/bigxantares/S-DES/assets/116985680/51482888-454b-4ac9-acfd-b0c2f67db0d6)

解密测试结果为：

![2](https://github.com/bigxantares/S-DES/assets/116985680/e81aa43f-075d-493b-8dd8-439c43260612)

### 1.3 输入输出扩充功能 

如果输入多组8位二进制明文或密文，则会在结果对应体现：

多位二进制：

![`H8 2OWB6MX%MD$R@7S21 7](https://github.com/bigxantares/S-DES/assets/116985680/b418df87-3ad1-4d10-a926-c81fcada318b)

![DT6%1DE7L7M~WCL43T1~}}R](https://github.com/bigxantares/S-DES/assets/116985680/d8830d90-cd82-412e-87bc-9d5510510a43)

多位ASCII码解密功能：

![BVQNG~6AFAEX ZYPB0Z2HW0](https://github.com/bigxantares/S-DES/assets/116985680/ea28ee5f-c490-402d-8445-ace24cb41934)

如果输入不是二进制，使用二进制加密解密会报错：

![SGG~PTD9SX@OKO `G J1N 9](https://github.com/bigxantares/S-DES/assets/116985680/92359d8c-3d79-4be5-b058-7a3fab964af2)


### 1.4 加密解密结果转换

生成二进制结果：

![ZT4PLE0)GQL1J)BN$F@IN{B](https://github.com/bigxantares/S-DES/assets/116985680/79d94e04-a82e-40df-bb40-179ec345b205)

转换ASCII：

![51RV%3} UEP(7{ YA~_86 S](https://github.com/bigxantares/S-DES/assets/116985680/f9cfcf5f-defd-4069-9fa4-f1ec1a083bd6)

转换十六进制（ASCII中有些控制字符无法在文本框显示）：

![ZGD1~}S 6KC@XZYVYK8MR(G](https://github.com/bigxantares/S-DES/assets/116985680/97909e60-0a7c-4c18-8972-ba9c6afa53ed)

如果结果文本框不是二进制会报错：

![QBG8D)E96{3X`Y@ _5LZARM](https://github.com/bigxantares/S-DES/assets/116985680/a713410f-e3f8-428b-b664-ba1a4dcfc4d8)


#  第二关：交叉测试

对测试明文：10101010

密钥：1111100000

测试密文：00011011

我们通过参考 o.O小组的程序来进行交叉测试，他们的密钥和明文加密结果如下图：

![3ZD{%E XQNBVT%)CFHLBU7U](https://github.com/bigxantares/S-DES/assets/116985680/63807270-6c9a-49aa-962e-d43e9d2c2c68)


我们的结果如下：

![3](https://github.com/bigxantares/S-DES/assets/116985680/13b1abe9-c347-48f5-aff8-f1a9b1140a3c)


#  第三关：扩展功能

在交互界面中，选择ASCII字符加密解密按钮，则可输入ASCII编码字符串进行使用，具体显示与第一关相似。

加密：

![4](https://github.com/bigxantares/S-DES/assets/116985680/5b1071d6-e04f-4d23-8e64-0f020b8de1f6)


解密：

![5](https://github.com/bigxantares/S-DES/assets/116985680/f0e2f156-2ac6-4847-b460-ff2319c2c9a1)


#  第四关：暴力破解

## 假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用暴力破解的方法找到正确的密钥Key

已找到明文：

已找到密文：

![image](https://github.com/bigxantares/S-DES/assets/116985680/d69b713d-4374-4d32-9c89-4900fc8accbe)

![image](https://github.com/bigxantares/S-DES/assets/116985680/f40a52f7-8e5c-4fbd-8ba9-f1a0ef1e4cb6)

## 暴力破解

实现单线程暴力破解
brute_force_1key函数使用itertools.product函数生成所有可能的10位二进制密钥，然后逐个尝试加密明文，直到找到与给定密文匹配的密钥。函数返回找到的密钥，或者在未找到有效密钥时返回None

![image](https://github.com/bigxantares/S-DES/assets/116985680/81229119-03f4-4d9a-8c3a-f9c2b32ce025)

实现多线程暴力破解

brute_force_key函数首先创建一个队列result_queue，用于存储找到的密钥。然后，函数根据指定的线程数将密钥空间分成若干块，并为每个线程创建一个brute_force_key_worker函数来执行暴力破解的工作。brute_force_key_worker函数接受一个密钥范围的起始和结束值，以及一个结果队列作为参数，然后在指定的密钥范围内尝试加密明文，并将找到的密钥存入结果队列中。最后，brute_force_key函数等待所有线程执行完毕，然后从结果队列中取出找到的密钥并返回

![image](https://github.com/bigxantares/S-DES/assets/116985680/8ae3264d-76b7-4652-aa53-e4ca2ef02c11)

测试结果：

多线程暴力破解未能找到有效密钥，用时0.25943922996520996秒

单线程暴力破解用时过久无结果
 
单线程暴力破解结果图

![image](https://github.com/bigxantares/S-DES/assets/116985680/c1ea9a1e-b538-4c8d-92b8-2035b27cf750)

多线程暴力破解结果图

![无标题视频——使用Clipchamp制作](https://github.com/bigxantares/S-DES/assets/116985680/3cf400aa-c2e7-466a-912a-3583e9b80c40)

#  第五关：封闭测试

## 根据第4关的结果，进一步分析，对于你随机选择的一个明密文对，是不是有不止一个密钥Key？进一步扩展，对应明文空间任意给定的明文分组P_{n}，是否会出现选择不同的密钥K_{i}\ne K_{j}加密得到相同密文C_n的情况？

由于加密算法的复杂性和暴力测试算法优化不够导致并未能成功暴力破解密钥，所以进行封闭性检测。
测试结果：通过封闭性测试

封闭性测试函数 test_closure()会生成随机密钥和明文，然后使用 S-DES 算法对明文进行加密，并检查是否存在不同密钥产生相同密文或相同密钥产生相同密文的情况。运行该函数时没有触发断言错误，说明 S-DES 算法通过了封闭性测试。

![image](https://github.com/bigxantares/S-DES/assets/116985680/1f9cc41c-0d25-47de-b264-8ac3ea4f0856)

test_closure函数首先生成随机的密钥和明文，然后使用S-DES算法加密明文得到密文。接着，函数生成另一个随机的密钥，并使用该密钥对相同的明文进行加密，检查是否存在不同密钥产生相同密文的情况。最后，函数生成另一个随机的明文，并使用相同的密钥对该明文进行加密，检查是否存在相同密钥产生相同密文的情况。如果两种情况都不存在，那么说明S-DES算法在封闭性测试中通过了

![image](https://github.com/bigxantares/S-DES/assets/116985680/470d15a0-3066-4159-9944-23d37cacccb3)

封闭性测试结果图

![image](https://github.com/bigxantares/S-DES/assets/116985680/364972e2-7a1d-483d-860e-c30672984b8c)

多次封闭性测试结果图


