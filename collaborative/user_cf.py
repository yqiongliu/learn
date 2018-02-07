# coding=UTF-8

import numpy as np
import datetime
import utils

# 用户数
NumOfUsers = 1000


# 惩罚了对于共同喜欢的物品的影响
def get_weight(train):
    '''
    :param train:
    :return: 返回用户的相似度矩阵W，W[u][v]表示u和v的相似度
    :return: 返回用户的相关用户user_related_users字典，key为用户id，value为和用户有共同电影的用户集合
    '''

    # 建立电影-用户倒排表
    item_users = dict()
    for u, items in train.items():
        for i in items:
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    # co_like[u][v]表示u和v之间的共同电影
    co_like = np.zeros([NumOfUsers, NumOfUsers], dtype=np.float16)
    # N[u]表示u评价的电影数目
    user_n = np.zeros([NumOfUsers], dtype=np.int32)

    # user_related_users[u]表示u的相关用户(共同电影不为零的用户)
    user_related_users = dict()
    # 对于每个电影，把它对应的用户组合co_like[u][v]加一
    for item, users in item_users.items():
        for u in users:
            user_n[u] += 1  # 该用户出现的次数
            for v in users:
                if u == v:  # 自己和自己去重
                    continue
                if u not in user_related_users:
                    user_related_users[u] = set()
                user_related_users[u].add(v)
                # 对于当前的uv可能是只出现一次，但是对于item_users表，会出现很多次，并且被各自缘由的产品热度惩罚
                co_like[u][v] += (1 / np.math.log(1 + len(users) * 1.0))  # 热度就是喜欢这个产品的人数

    # 用户相似度矩阵
    weight = np.zeros([NumOfUsers, NumOfUsers], dtype=np.float16)
    for u in range(1, NumOfUsers):
        if u in user_related_users:
            for v in user_related_users[u]:
                weight[u][v] = co_like[u][v] / np.sqrt(user_n[u] * user_n[v])

    return weight, user_related_users


def recommend(user, train, weight, related_users, k, N):
    '''
    通过相似度矩阵W得到和user相似的rank字典
    :param user: 用户ID
    :param train: 训练集
    :param weight: 相似度矩阵
    :param k: 决定了从相似用户中取出多少个进行计算
    :param related_users:
    :return: rank字典，包含了所有兴趣程度不为零的项目，按照从大到小排序
    '''

    # 取前k个用户
    k_users = dict()
    try:
        for v in related_users[user]:
            k_users[v] = weight[user][v]
    except KeyError:
        print("User " + str(user) + " doesn't have any related users in train set")

    k_users = sorted(k_users.items(), key=lambda x: x[1], reverse=True)
    k_users = k_users[0:k]  # 取前k个用户

    # 用户喜欢的东西，i应该是代表用户喜欢的商品。
    rank = dict()
    for i in range(1, 1700):
        rank[i] = 0
    for i in range(1700):
        for v, wuv in k_users:
            if i in train[v] and i not in train[user]:  # 防止已经被用户评价过的物品再次进入推荐
                rank[i] += wuv * 1

    return sorted(rank.items(), key=lambda d: d[1], reverse=True)


def get_recommendation(user, train, top_n, k, weight, related_users):
    '''.
    获得N个推荐
    :param user: 用户
    :param train: 训练集
    :param weight: 相似度矩阵
    :param top_n: 推荐数目top_n
    :param k: 决定了从相似用户中取出多少个进行计算
    :param related_users:
    :return: recommend字典，key是movie id，value是兴趣程度
    '''
    rank = recommend(user, train, weight, related_users, k, top_n)
    recommend_top_n = dict()
    for i in range(top_n):
        recommend_top_n[rank[i][0]] = rank[i][1]
    return recommend_top_n


def evaluate(train, test, top_n, k):
    recommends = dict()
    weight, related_users = get_weight(train)
    for user in test:
        recommends[user] = get_recommendation(user, train, top_n, k, weight, related_users)

    return utils.evaluate_sub(train, test, top_n, k, recommends)


def test1():
    top_n = int(input("Input the number of recommendations\n"))
    k = int(input("Input the number of related users\n"))
    data = utils.get_data()
    train, test = utils.split_data(data, 2, 1, 1)
    del data

    user = int(input("Input the user id \n"))
    print("The train set contains the movies of the user: ")
    print(train[user])

    start_time = datetime.datetime.now()
    weight, related_users = get_weight(train)
    end_time = datetime.datetime.now()
    print("it takes ", (end_time - start_time).seconds, " seconds to get W")

    start_time = datetime.datetime.now()
    rec = get_recommendation(user, train, top_n, k, weight, related_users)
    end_time = datetime.datetime.now()
    print("it takes ", (end_time - start_time).seconds, " seconds to get recommend for one user")

    print(rec)
    for item in rec:
        print(item),
        if item in test[user]:
            print("  True")
        else:
            print("  False")


def test2():
    top_n = int(input("Input the number of recommendations: \n"))
    k = int(input("Input the number of related users: \n"))
    data = utils.get_data()
    train, test = utils.split_data(data, 2, 1, 1)
    del data
    recall, precision, coverage, popularity = evaluate(train, test, top_n, k)
    print("recall: ", recall)
    print("precision: ", precision)
    print("coverage: ", coverage)
    print("popularity: ", popularity)


def recall(train, test, N, k):
    '''
    :param train: 训练集
    :param test: 测试集
    :param N: TopN推荐中的N数目
    :return: 返回召回率
    '''
    hit = 0  # 预测准确的数目
    total = 0  # 所有的行为总数
    W, related_users = get_weight(train)
    for user in train.keys():
        tu = test[user]
        rank = get_recommendation(user, train, N, k, W, related_users)
        for item in rank:
            if item in tu:
                hit += 1
        total += len(tu)
    return hit / (total * 1.0)  # 把结果转化成小数


def precision(train, test, N, k):
    '''
    :param train: 训练集
    :param test: 测试集
    :param N: topN推荐中的数目N
    :return: 返回准确率
    '''
    hit = 0
    total = 0
    W, related_users = get_weight(train)
    for user in train.keys():
        tu = test[user]
        rank = get_recommendation(user, train, N, k, W, related_users)
        for item in rank:
            if item in tu:
                hit += 1
        total += N
    return hit / (total * 1.0)


def coverage(train, test, N, k):
    '''
    计算覆盖率
    :param train: 训练集，字典user->items
    :param test: 测试集,字典user->items
    :param N: topN推荐中的N
    :return: 覆盖率
    '''
    recommend_items = set()
    all_items = set()
    W, related_users = get_weight(train)
    for user in train.keys():
        for item in train[user]:
            all_items.add(item)
        rank = get_recommendation(user, train, N, k, W, related_users)
        for item in rank:
            recommend_items.add(item)
    return len(recommend_items) / (len(all_items) * 1.0)


def popularity(train, test, N, k):
    '''
    计算新颖度
    :param train: 训练集,字典user->items
    :param test: 测试集,字典user->items
    :param N: topN推荐中的推荐数目N
    :return: 新颖度
    '''
    item_popularity = dict()
    W, related_users = get_weight(train)
    for user, items in train.items():
        for item in items:
            if item not in item_popularity:
                item_popularity[item] = 0
            item_popularity[item] += 1
    ret = 0
    n = 0
    for user in train.keys():
        rank = get_recommendation(user, train, N, k, W, related_users)
        for item in rank:
            if item != 0:
                ret += np.math.log(1 + item_popularity[item])
                n += 1
    ret /= n * 1.0
    return ret
