# coding=UTF-8

import numpy as np
import datetime
import utils

NumOfItems = 1690


def get_weight(train):
    # train本身已经是用户-物品倒排表

    # C[u][v]表示喜欢u又喜欢v的用户有多少个
    co_like = np.zeros([NumOfItems, NumOfItems], dtype=np.float16)
    # N[u]表示有多少用户喜欢u
    item_n = np.zeros([NumOfItems], dtype=np.int32)

    item_related_items = dict()
    for user, items in train.items():
        for item1 in items:
            item_n[item1] += 1
            for item2 in items:
                if item1 == item2:
                    continue
                if item1 not in item_related_items:
                    item_related_items[item1] = set()
                item_related_items[item1].add(item2)
                co_like[item1][item2] += (1 / np.math.log(1 + len(items) * 1.0))

    # W[u][v]表示u和v物品的相似度
    weight = np.zeros([NumOfItems, NumOfItems], dtype=np.float16)
    for item1 in range(1, NumOfItems):
        if item1 in item_related_items:
            for item2 in item_related_items[item1]:
                weight[item1][item2] = co_like[item1][item2] / np.sqrt(item_n[item1] * item_n[item2])

    return weight, item_related_items


def k_similar_item(weight, item_related_items, k):
    '''
    返回一个字典，key是每个item，value是item对应的k个最相似的物品
    '''
    begin = datetime.datetime.now()

    k_similar = dict()
    for i in range(1, NumOfItems):
        related_items = dict()
        try:
            for x in item_related_items[i]:
                related_items[x] = weight[i][x]
            related_items = sorted(related_items.items(), key=lambda x: x[1], reverse=True)
            k_similar[i] = set(dict(related_items[0:k]))
        except KeyError:
            print(i, " doesn't have any related_items")
            k_similar[i] = set()
            for x in range(1, k + 1):
                k_similar[i].add(x)

    end = datetime.datetime.now()
    print("it takes ", (end - begin).seconds, " seconds to get k_similar_item for all items.")
    return k_similar


def get_recommendation(user, train, weight, related_items, k, top_n, k_similar_items):
    rank = dict()  # key是电影id，value是兴趣大小

    for i in range(NumOfItems):
        rank[i] = 0

    possible_recommend = set()
    for item in train[user]:
        possible_recommend = possible_recommend.union(related_items[item])

    for item in possible_recommend:
        k_items = k_similar_items[item]
        # k_items=dict()
        # if item in related_items:
        #     for item2 in related_items[item]:
        #         if item2==item:
        #             continue
        #         k_items[item2]=W[item][item2]
        # k_items=sorted(k_items.items(),key=lambda x:x[1],reverse=True)[0:k]

        # k_items=dict(k_items)

        for i in k_items:
            if i in train[user]:
                rank[item] += 1.0 * weight[item][i]

    for rank_key in rank:
        if rank_key in train[user]:
            rank[rank_key] = 0
    return dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:top_n])


def evaluate(train, test, top_n, k):
    recommends = dict()
    weight, related_items = get_weight(train)
    k_similar = k_similar_item(weight, related_items, k)
    for user in test:
        recommends[user] = get_recommendation(user, train, weight, related_items, k, top_n, k_similar)

    return utils.evaluate_sub(train, test, top_n, k, recommends)


def test1():
    top_n = int(input("input the number of recommendations\n"))
    k = int(input("input the number of related items\n"))
    data = utils.get_data()
    train, test = utils.split_data(data, 2, 1, 1)
    del data

    user = int(input("input the user id \n"))
    print("the train set contains the movies of the user: \n")
    print(train[user])

    start_time = datetime.datetime.now()
    weight, related_items = get_weight(train)
    end_time = datetime.datetime.now()
    print("it takes ", (end_time - start_time).seconds, " seconds to get W")

    k_similar = k_similar_item(weight, related_items, k)
    start_time = datetime.datetime.now()
    recommend = get_recommendation(user, train, weight, related_items, k, top_n, k_similar)
    end_time = datetime.datetime.now()
    print("it takes ", (end_time - start_time).seconds, " seconds to get recommend for one user")
    print(recommend)
    for item in recommend:
        print(item),
        if item in test[user]:
            print("   True")
        else:
            print("   False")


def test2():
    top_n = int(input("input the number of recommendations: \n"))
    k = int(input("input the number of related items: \n"))
    data = utils.get_data()
    train, test = utils.split_data(data, 2, 1, 1)
    del data
    recall, precision, coverage, popularity = evaluate(train, test, top_n, k)
    print("Recall: ", recall)
    print("Precision: ", precision)
    print("Coverage: ", coverage)
    print("popularity: ", popularity)


if __name__ == '__main__':
    test1()
