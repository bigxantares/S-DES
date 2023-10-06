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

#  第五关：封闭测试




