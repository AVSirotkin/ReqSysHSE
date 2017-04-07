#!/usr/bin/env python3
'''
Baseline solution for the ACM Recsys Challenge 2017
using XGBoost

by Daniel Kohlsdorf
'''



import numpy as np
import xgboost as xgb
'''
from model import Interaction, Item, User
from parser import InteractionBuilder, select
'''
from model import *
from parser import *
from recommendation_worker import *
# import random
import pickle
print(" --- Recsys Challenge 2017 Baseline --- ")




'''
1) Parse the challenge data, exclude all impressions
   Exclude all impressions
'''


with open('/students/iamishalkin/shared/ReqSys/data/pickle/users.pickle', 'rb') as handle:
    users = pickle.load(handle)
with open('/students/iamishalkin/shared/ReqSys/data/pickle/header_users.pickle', 'rb') as handle:
    header_users = pickle.load(handle)

with open('/students/iamishalkin/shared/ReqSys/data/pickle/items.pickle', 'rb') as handle:
    items = pickle.load(handle)

with open('/students/iamishalkin/shared/ReqSys/data/pickle/header_items.pickle', 'rb') as handle:
    header_items = pickle.load(handle)

with open('/students/iamishalkin/shared/ReqSys/data/pickle/interactions.pickle', 'rb') as handle:
    interactions = pickle.load(handle)

with open('/students/iamishalkin/shared/ReqSys/data/pickle/header_interactions.pickle', 'rb') as handle:
    header_interactions = pickle.load(handle)
'''
2) Build recsys training data
'''
data = np.array([interactions[key].features() for key in interactions.keys()])
labels = np.array([interactions[key].label() for key in interactions.keys()])
dataset = xgb.DMatrix(data, label=labels)
dataset.save_binary("recsys2017.buffer")


'''
3) Train XGBoost regression model with maximum tree depth of 2 and 25 trees
'''
evallist = [(dataset, 'train')]
param = {'bst:max_depth': 2,
         'bst:eta': 0.1,
         'silent': 1,
         'objective': 'reg:linear',
         }

param.update({
    'nthread': 4,
    'eval_metric': 'rmse',
    'base_score': 0.0
})
print(param)
num_round = 25
bst = xgb.train(param, dataset, num_round, evallist)
bst.save_model('recsys2017.model')


'''
4) Create target sets for items and users
'''
target_users = []
with open(TARGET_USERS) as f:
    next(f)
    for line in f:
#for line in open(TARGET_USERS):
      target_users += [int(line.strip())]
target_users = set(target_users)

target_items = []
for line in open(TARGET_ITEMS):
    target_items += [int(line.strip())]


'''
5) Schedule classification
'''
bst = xgb.Booster({'nthread': 4})
bst.load_model('recsys2017.model')
bucket_size = len(target_items) / N_WORKERS
print(bucket_size)
# import ipdb; ipdb.set_trace()
start = 0
jobs = []
# print(items[:5])
# print(users[:5])
# print(target_items)
# print(target_users)
for i in range(0, N_WORKERS):
    stop = int(min(len(target_items), start + bucket_size))
    filename = "solution_" + str(i) + ".csv"
    process = multiprocessing.Process(target=classify_worker, args=(
        target_items[start:stop], target_users, items, users, filename, bst))
    jobs.append(process)
    start = stop

for j in jobs:
    j.start()

for j in jobs:
    j.join()

