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
from bloom_filter import BloomFilter

class TestBloomFilter():
    
    def __init__(self,  words_list=['a', 'b', 'c'], wordlist_file='wordlist.txt', plot_dir='./plots/', read_from_file=True):
        self.wordlist_file = wordlist_file
        self.plot_dir = plot_dir
        if read_from_file:
            self.dic_words = self.__read_dic_words()
        else:
            self.dic_words = set(words_list)
        
        if len(self.dic_words) == 0:
            print('Dictionary is empty!')
    
    def __read_dic_words(self):
        with open(self.wordlist_file, 'r') as fin:
            dic_words = [word.strip().rstrip('\n').lower() for word in fin]
        dic_words = set(dic_words)
        return dic_words
    
    def __add_words(self, bloom_filter_obj):
        for word in self.dic_words:
            bloom_filter_obj.add_word(word)
    
    def __check_added_words(self, bloom_filter_obj):
        FN = 0
        TP = 0
        for word in self.dic_words:
            if bloom_filter_obj.exist_word(word) == False:
                print('Hashing is not working ...')
                FN += 1
            else:
                TP += 1
        return FN, TP
    
    def test_filter(self, filter_size=200, hash_num=5):
        bloom_filter_obj = BloomFilter(filter_size=filter_size, hash_num=hash_num)
        self.__add_words(bloom_filter_obj=bloom_filter_obj)
        FN, TP = self.__check_added_words(bloom_filter_obj=bloom_filter_obj)
        print(f'number of dic_words is {len(self.dic_words)}')
        print(f'FN is {FN}')
        print(f'TP is {TP}')
        return bloom_filter_obj, FN, TP
        
    
    def analyse_with_random_words(self, word_len=5, hash_range=[1, 21], ratio_range=[10, 21]):
        word_num = len(self.dic_words)
        rand_words = [''.join([random.choice(string.ascii_lowercase) for x in range(word_len)]) for i in range(word_num)]
        rand_words = [word for word in rand_words if word not in self.dic_words]
        res = []
        for hash_num in range(hash_range[0], hash_range[1]):
            print(f'____________________________hash number: {hash_num}________________________')
            
            for ratio in range(ratio_range[0], ratio_range[1]):
                                
                filter_size = int(ratio*word_num)
                bloom_filter_obj = BloomFilter(filter_size=filter_size, hash_num=hash_num)
                self.__add_words(bloom_filter_obj)
                
                FP = 0
                for rand_word in rand_words:
                    if bloom_filter_obj.exist_word(rand_word):
                        FP += 1
                res.append([ratio, FP/len(rand_words), hash_num])
                print(f'ratio, fp_ratio, hash_num: [{ratio}, {FP/len(rand_words)}, {hash_num}]')
        
        df_res = pd.DataFrame(res, columns=['m/n', 'FP_ratio', 'hash_num'])
        self.__plot_line_charts(df_res)                 
        return df_res
            
    
    def __plot_line_charts(self, df):
        fig = px.line(df.loc[df['hash_num']<=10], x='m/n', y='FP_ratio', color='hash_num')
        fig.show()
        pio.write_image(fig, self.plot_dir + 'fig1.jpeg', width=1000, height=800)
        
        groups = df.groupby(by='m/n')
        for key, grp in groups:
            fig = px.line(grp, x='hash_num', y='FP_ratio')
            fig.show()
            pio.write_image(fig, self.plot_dir + f'm_over_n={key}.jpeg', width=1000, height=800)
    

if __name__ == '__main__':
    test_obj = TestBloomFilter()
    bloom_filter_obj, FN, TP = test_obj.test_filter()
    df_result = test_obj.analyse_with_random_words()
    
