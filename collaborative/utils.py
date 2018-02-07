# coding=UTF-8
import random
import math
import numpy as np


def get_data(datafile='u.data'):
    # 把datafile文件中的数据读出来，返回data对象
    # :param datafile: 数据源文件名称
    # return: 一个列表data，每一项是一个元组，元组第一项是用户，第二项是电影
    data = []
    try:
        file = open(datafile)
    except:
        print("No such file named " + datafile)
        return
    for line in file:
        line = line.split('\t')
        try:
            data.append((int(line[0]), int(line[1])))
        except:
            pass
    file.close()
    return data


def split_data(data, m, k, seed):
    '''
    train/data=1/M
    :param data: 传入的数据
    :param m: 测试集占比
    :param k: 一个任意的数字，用来随机筛选出测试集和训练集
    :param seed: 随机数种子
    :return: train:训练集  test:测试集 都是字典，key是用户id，value是电影集合
    '''
    test = dict()
    train = dict()
    random.seed(seed)
    # 在M次实验里面我们需要相同的随机数种子，这样生成的随机序列是相同的
    for user, item in data:
        if random.randint(0, m) != k:
            # 相等的概率是1/M，所以M决定了测试集在所有数据中的比例
            if user not in test.keys():
                test[user] = set()
            test[user].add(item)
        else:
            if user not in train.keys():
                train[user] = set()
            train[user].add(item)
    return train, test


def evaluate_sub(train, test, top_n, k, recommends):
    hit = 0  # 预测准确的数目
    total_recall = 0  # 所有的行为总数
    total_precision = 0
    for user in train.keys():
        tu = test[user]
        rank = recommends[user]
        for item in rank:
            if item in tu:
                hit += 1
        total_recall += len(tu)
        total_precision += top_n

    recall = hit / (total_recall * 1.0)  # 把结果转化成小数
    precision = hit / (total_precision * 1.0)  # 把结果转化成小数

    recommend_items = set()
    all_items = set()
    for user in train.keys():
        for item in train[user]:
            all_items.add(item)
        rank = recommends[user]
        for item in rank:
            recommend_items.add(item)
    coverage = len(recommend_items) / (len(all_items) * 1.0)

    item_popularity = dict()
    for user, items in train.items():
        for item in items:
            if item not in item_popularity:
                item_popularity[item] = 0
            item_popularity[item] += 1
    ret = 0
    n = 0
    for user in train.keys():
        rank = recommends[user]
        for item in rank:
            ret += np.math.log(1 + item_popularity[item])
            n += 1
    ret /= n * 1.0
    popularity = ret

    return recall, precision, coverage, popularity


def cosine_similarity(train):
    '''
    计算训练集中每两个用户的余弦相似度
    这个函数没有实际价值，复杂度相当高，而且容易Out Of Memory，即在训练集大的时候容易产生内存不足的错误
    但是这个函数比较容易看出公式的原型，可以借此理解公式运用
    :param train: 训练集,字典user->items
    :return: 返回相似度矩阵
    '''
    W = dict()
    print(len(train.keys()))
    for u in train.keys():
        for v in train.keys():
            if u == v:
                continue  # 如果u和v是同样的用户，那么跳过
            W[(u, v)] = len(train[u] & train[v])
            W[(u, v)] /= math.sqrt(len(train[u]) * len(train[v]) * 1.0)
            W[(v, u)] = W[(u, v)]
    return W
