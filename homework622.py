# -*- coding:utf-8 -*-
import random
import string


def string_reverse(s):
    '''
    目标：实现字符串的逆序排列
    思路：用循环做，构建一个新的字符串，从末尾向头取字符串，每次取一个然后添加到后面。
    :param s:字符串
    :return:
    '''
    newString = ''
    for i in range(len(s) - 1, -1, -1):
        newString += s[i]
    return newString


def string_reverse1(s):
    '''
    思路：也是用循环，不能构造新的字符串，通过交换实现。(先把字符串转换成list，然后交换实现，最后再转换成字符串)
    :param s:字符串
    :return:
    '''
    s = list(s)
    s.reverse()
    return ''.join(s)


def reverse_str(s):
    return s[::-1]


def randomStr(n=10):
    '''
    产生随机字符串
    :param n: 字符串长度
    :return: 随机字符串
    '''
    s = ''
    chars = list(string.ascii_letters)
    for i in range(n):
        s += random.choice(chars)
    return s


def test(time=20):
    for i in range(time):
        randomstring = randomStr(8)
        print('test:', randomstring, 'time:', i)
        assert reverse_str(randomstring) == string_reverse1(randomstring)


if __name__ == '__main__':
    print(string_reverse('abcd1234'))
    print(string_reverse1('abcd1234'))
    test(20)
