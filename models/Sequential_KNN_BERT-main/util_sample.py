from __future__ import print_function
from collections import defaultdict
import random
import pandas as pd

USER_KEY = "UserId"
ITEM_KEY = "ItemId"

def data_partition(fname, original_setting, sample_percentage=5):
    User = defaultdict(list)
    user_train = {}
    user_valid = {}
    user_test = {}
    train_elems = {}
    # assume user/item index starting from 1

    header_list = ["UserId", "ItemId"]
    data = pd.read_csv(fname, sep=' ', names=header_list)
    # data = pd.read_csv(fname, sep=' ')

    print("sample data: "+str(sample_percentage)+"%\n")
    data = sample(data, sample_percentage)
    usernum = data[USER_KEY].nunique()
    itemnum = data[ITEM_KEY].nunique()

    # sequences
    interactions_per_user = data.groupby(USER_KEY).size()
    avg_seq_len = interactions_per_user.mean()

    # print('--------------------- Sampled---')
    print('Sampled data set\n\tEvents: {}\n\tUsers: {}\n\tItems: {}\n\tAvg_seq_len: {}\n\n'.
          format(len(data), usernum, itemnum, avg_seq_len))


    # f = open(fname, 'r')
    # for line in f:
    #     u, i = line.rstrip().split(' ')
    #     u = int(u)
    #     i = int(i)
    #     usernum = max(u, usernum)
    #     itemnum = max(i, itemnum)
    #     User[u].append(i)


    for index, row in data.iterrows():
        # row[0]: userId, row[1]: ItemId
        u = row[0]  # int(u)
        i = row[1]  # int(i)
        # usernum = max(u, usernum)
        # itemnum = max(i, itemnum)
        User[u].append(i)


    for user in User:
        nfeedback = len(User[user])
        if nfeedback < 3:
            user_train[user] = User[user]
            user_valid[user] = []
            user_test[user] = []
        else:
            user_train[user] = User[user][:-2]  # training set: all interactions of each user, except the last two
            user_valid[user] = []
            user_valid[user].append(User[user][-2])  # validation set: the second last interactions of each user
            user_test[user] = []
            user_test[user].append(User[user][-1])  # test set: the last interactions of each user

        if not original_setting:
            # Add all elements in train and validation to train_elems
            for i in user_train[user]+user_valid[user]:
                train_elems[i] = 1

    if not original_setting:
        # Remove test information for the users if item not in train_elems
        for user in User:
            if len(user_test[user]) > 0:
                if user_test[user][0] not in train_elems:
                    #del user_test[user]  # 
                    user_test[user] = []

    return [user_train, user_valid, user_test, usernum, itemnum]



def sample(data, sample_percentage):
    users = list(set(data[USER_KEY]))
    random.seed(10)
    sample_size = len(users) * (sample_percentage / 100)
    users_sampled = random.sample(users, int(sample_size))
    data = data[data[USER_KEY].isin(users_sampled)]
    return data
