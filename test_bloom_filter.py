# -*- coding: utf-8 -*-
'''
Created on Thu Mar 10 18:21:04 2022

@author: snourashrafeddin
'''



import random
import string
import plotly.express as px
import plotly.io as pio
import pandas as pd
from bloom_filter import Bloomfilter


def read_dic_words(wordlist):
    with open(wordlist, 'r') as fin:
        dic_words = [word.strip().rstrip('\n').lower() for word in fin]
    dic_words = set(dic_words)
    return dic_words


def add_words(bloom_filter_obj, dic_words):
    for word in dic_words:
        bloom_filter_obj.add_word(word)

        
def check_added_words(bloom_filter_obj, dic_words):
    FN = 0
    TP = 0
    for word in dic_words:
        if bloom_filter_obj.exist_word(word) == False:
            print('Hashing is not working ...')
            FN += 1
        else:
            TP += 1
    return FN, TP


def run_initial_test(dic_words):
    mask_size = 200
    hash_num = 5
    bloom_filter_obj = Bloomfilter(mask_size=mask_size, hash_num=hash_num)
    add_words(bloom_filter_obj=bloom_filter_obj, dic_words=dic_words)
    FN, TP = check_added_words(bloom_filter_obj=bloom_filter_obj, dic_words=dic_words)
    print(f'number of dic_words is {len(dic_words)}')
    print(f'FN is {FN}')
    print(f'TP is {TP}')
    

def check_random_words(dic_words, word_len=5):
    res = []
    word_num = len(dic_words)
    rand_words = [''.join([random.choice(string.ascii_lowercase) for x in range(word_len)]) for i in range(word_num)]
    rand_words = [word for word in rand_words if word not in dic_words]
    
    for hash_num in range(1, 50):
        print(f'____________________________hash number: {hash_num}________________________')
        for ratio in range(10, 21):
            print(f'______________ratio: {ratio}__________')
            mask_size = int(ratio*word_num)
            bloom_filter_obj = Bloomfilter(mask_size=mask_size, hash_num=hash_num)
            add_words(bloom_filter_obj, dic_words)
            FP = 0
            for rand_word in rand_words:
                if bloom_filter_obj.exist_word(rand_word):
                    FP += 1
            res.append([ratio, FP/len(rand_words), hash_num])
                     
    return pd.DataFrame(res, columns=['m/n', 'FP_ratio', 'hash_num'])
        

def plot_line_charts(df):
    _dir = './plots/'
    fig = px.line(df.loc[df['hash_num']<=10], x='m/n', y='FP_ratio', color='hash_num')
    fig.show()
    pio.write_image(fig, _dir + 'fig1.jpeg', width=1000, height=800)
    
    groups = df.groupby(by='m/n')
    for key, grp in groups:
        fig = px.line(grp, x='hash_num', y='FP_ratio')
        fig.show()
        pio.write_image(fig, _dir + f'm_over_n={key}.jpeg', width=1000, height=800)
        
        

if __name__ == '__main__':
    wordlist = 'wordlist.txt'
    dic_words = read_dic_words(wordlist)
    run_initial_test(dic_words)
    df = check_random_words(dic_words)
    plot_line_charts(df)