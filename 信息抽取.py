# coding=utf-8
import pandas as pd
import numpy as np
import sys
import warnings
from LAC import LAC
from sklearn.tree import DecisionTreeClassifier
import re

warnings.filterwarnings(action='ignore', category=DeprecationWarning)
# sys.path.extend(['D:\\清华大数据\\pytorch\\pytorch', 'D:/清华大数据/pytorch/pytorch'])
path = 'D:/清华大数据/pytorch/pytorch/cys/河南/'

# 装载词语重要性模型
lac = LAC(mode='rank')


# def judge_phone_number(account):
#     a = re.findall('(13\d{9}|14[5|7]\d{8}|15\d{9}|166{\d{8}|17[3|6|7]{\d{8}|18\d{9})', account)
#     return a


def loc_e():
    try:
        d = pd.read_csv(path + '新乡暴雨求助07231.csv')

    except UnicodeDecodeError:
        print('请将csv转换为utf-8形式')
        sys.exit(0)
    data = d
    ret = []
    dic2 = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    for j in range(len(data)):
        dic = {'LOC': {}, 'n': {}, 'f': {}, 's': {}, 'nw': {}, 'nz': {}, 'v': {}, 'vd': {}, 'vn': {}, 'a': {}, 'ad': {},
               'an': {}, 'd': {},
               'm': {}, 'q': {}, 'r': {}, 'p': {}, 'c': {}, 'u': {}, 'xc': {}, 'w': {}, 'PER': {}, 'ORG': {},
               'TIME': {}, '': {}}
        time = data.loc[j]['time']
        temp = lac.run(data.loc[j]['txt'])
        rank1 = temp[0]
        rank2 = temp[1]
        rank3 = temp[2]
        # i = 0
        # while 1:
        #     if rank2[i] == '':
        #         rank1.remove(rank1[i])
        #         rank2.remove(rank2[i])
        #         rank3.remove(rank3[i])
        #         if i + 1 >= len(rank1):
        #             break
        #     else:
        #         i += 1
        #         if i == len(rank1):
        #             break
        #     # if rank1[i] == ['/n']:
        #     #     rank1.remove(rank1[i])
        #     #     rank2.remove(rank2[i])
        #     #     rank3.remove(rank3[i])
        #     #     if i + 1 >= len(rank1):
        #     #         break
        #     # else:
        #     #     i += 1
        #     #     if i == len(rank1):
        #     #         break
        i = 0
        for word in rank1:
            if word not in dic[rank2[i]]:
                dic[rank2[i]][word] = [1, rank3[i]]
            else:
                dic[rank2[i]][word][0] += 1
                if rank3[i] > dic[rank2[i]][word][0]:
                    dic[rank2[i]][word][0] = rank3[i]
            i += 1
        loc = []
        for key in dic['LOC']:
            loc.append(key)
        # loc = dic['LOC']
        tel = []
        moby = []
        txt = data.loc[j]['txt']
        temp1 = ''
        for i in range(len(txt)):
            if txt[i] in dic2:
                temp1 = temp1 + txt[i]
            elif txt[i] == ' ':
                continue
            else:
                temp1 = ''
            if len(temp1) == 11 and temp1[0] == '1':
                moby.append(temp1)
                temp1 = ''
            elif len(temp1) in [7, 8] or len(temp1) >= 8 and temp1[0] == '0':
                if not i == len(txt) - 1:
                    if txt[i + 1] not in dic2 and not txt[i + 1] == ' ':
                        tel.append(temp1)
                        temp1 = ''
                else:
                    tel.append(temp1)
                    temp1 = ''
                if len(temp1) in [7, 8]:
                    if not i == len(txt) - 1:
                        if not temp1[0] == '1' and not txt[i + 1] in dic2:
                            tel.append(temp1)
                            temp1 = ''
        # punctuation = '!,;:?"\'、，；。 '
        # for te in enumerate(dic['n']):
        #     text = re.sub(r'[{}]+'.format(punctuation), ' ', te[1])
        #     temp = text.strip()
        #     if len(temp) == 11:
        #         moby.append(temp)
        #     if len(temp) == 8 or len(temp) == 7:
        #         tel.append(temp)
        #     else:
        #         try:
        #             if not judge_phone_number(temp) == []: moby.append(judge_phone_number(te[1]))
        #         except AttributeError:
        #             continue
        # for te in enumerate(dic['m']):
        #     text = re.sub(r'[{}]+'.format(punctuation), ' ', te[1])
        #     temp = text.strip()
        #     if len(temp) == 11:
        #         moby.append(temp)
        #     if len(temp) == 8 or len(temp) == 7:
        #         tel.append(te[1])
        #     else:
        #         try:
        #             if not judge_phone_number(temp) == []: moby.append(judge_phone_number(temp))
        #         except AttributeError:
        #             continue
        ret.append({'信息发布时间': time,
                    'loc': loc, '电话': {'moby': moby, 'tel': tel}, '内容': data.loc[j]['txt'],
                    '信息来源': {'微博话题': '新乡暴雨求助'},
                    '收集人': '小白、牛奶奶'})
    ret = pd.DataFrame(data=ret)
    ret.to_csv('D:/清华大数据/pytorch/pytorch/cys/07231.csv')

# def txt2vec(data):
#     new_data = []
#
#     for i in range(len(data)):
#         temp = data.loc[i]
#         time = temp[0]
#         # 单个样本输入，输入为Unicode编码的字符串
#         text = temp
#         rank2 = lac.run(text)[1]
#         while '' in rank2:
#             rank2.remove('')
#             # print(rank2)
#         dic2 = {'n': 0, 'f': 0, 's': 0, 'nw': 0, 'nz': 0, 'v': 0, 'vd': 0, 'vn': 0, 'a': 0, 'ad': 0, 'an': 0, 'd': 0,
#                 'm': 0, 'q': 0, 'r': 0, 'p': 0, 'c': 0, 'u': 0, 'xc': 0, 'w': 0, 'PER': 0, 'LOC': 0, 'ORG': 0,
#                 'TIME': 0}
#         for word in rank2:
#             if word not in dic2:
#                 dic2[word] = 1
#             else:
#                 dic2[word] += 1
#
#         vec = np.zeros(24)
#         i = 0
#         for k in dic2:
#             vec[i] = dic2[k]
#             i += 1
#         # new_data.append({'time': time, 'text': temp[0], 'vec': vec})
#         new_data.append(vec)
#         # print(vec)
#     return new_data
#
#
# if __name__ == '__main__':
#     # 读取已经排序按utf-8编码的entities/relation
#     try:
#         d = pd.read_csv(path + '新乡暴雨求助(1).csv')
#
#     except UnicodeDecodeError:
#         print('请将csv转换为utf-8形式')
#         sys.exit(0)
#     data = txt2vec(d['txt'])
#     label = d['label']
#     clf = DecisionTreeClassifier(random_state=3)  # 初始化
#     # t_d = data[0:400]
#     # t_l = data[0:400]
#     clf = clf.fit(data[:100], label[:100])  # 拟合
#
#     score_ = clf.score(data[:100], label[:100])
#     print(score_)
#     # 可以输入数据送到训练好的模型里，输出预测的类
#     y_pred = clf.predict(data)
#     new_data = []
#     for i in range(len(data)):
#         if y_pred[i] == 1:
#             new_data.append(d.iloc[i])
#     test = pd.DataFrame(data=new_data)
#     test.to_csv('clean_data11.csv')
#     # test_data = pd.read_csv(path + '河南暴雨救援(2).csv')
#     # vec = txt2vec(test_data['txt'])
#     # test = clf.predict(vec)
#     # np.savetxt("label.csv", y_pred, delimiter=',')
