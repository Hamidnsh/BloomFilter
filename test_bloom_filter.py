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
    
    def __init__(self, wordlist='wordlist.txt', plot_dir='./plots/'):
        self.wordlist = wordlist
        self._dir = plot_dir
        self.dic_words = self.read_dic_words()
    
    def read_dic_words(self):
        with open(self.wordlist, 'r') as fin:
            dic_words = [word.strip().rstrip('\n').lower() for word in fin]
        dic_words = set(dic_words)
        return dic_words
    
    
    def add_words(self, bloom_filter_obj):
        for word in self.dic_words:
            bloom_filter_obj.add_word(word)
    
            
    def check_added_words(self, bloom_filter_obj):
        FN = 0
        TP = 0
        for word in self.dic_words:
            if bloom_filter_obj.exist_word(word) == False:
                print('Hashing is not working ...')
                FN += 1
            else:
                TP += 1
        return FN, TP
    
    
    def run_initial_test(self):
        mask_size = 200
        hash_num = 5
        bloom_filter_obj = BloomFilter(mask_size=mask_size, hash_num=hash_num)
        self.add_words(bloom_filter_obj=bloom_filter_obj)
        FN, TP = self.check_added_words(bloom_filter_obj=bloom_filter_obj)
        print(f'number of dic_words is {len(self.dic_words)}')
        print(f'FN is {FN}')
        print(f'TP is {TP}')
   
    
    def run_with_random_words(self, word_len=5):
        word_num = len(self.dic_words)
        rand_words = [''.join([random.choice(string.ascii_lowercase) for x in range(word_len)]) for i in range(word_num)]
        rand_words = [word for word in rand_words if word not in self.dic_words]
        res = []
        for hash_num in range(1, 21):
            print(f'____________________________hash number: {hash_num}________________________')
            
            for ratio in range(10, 21):
                print(f'______________ratio: {ratio}__________')
                
                mask_size = int(ratio*word_num)
                bloom_filter_obj = BloomFilter(mask_size=mask_size, hash_num=hash_num)
                self.add_words(bloom_filter_obj)
                
                FP = 0
                for rand_word in rand_words:
                    if bloom_filter_obj.exist_word(rand_word):
                        FP += 1
                res.append([ratio, FP/len(rand_words), hash_num])
                print(f'ratio, fp_ratio, hash_num: [{ratio}, {FP/len(rand_words)}, {hash_num}]')
                         
        return pd.DataFrame(res, columns=['m/n', 'FP_ratio', 'hash_num'])
            
    
    def plot_line_charts(self, df):
        fig = px.line(df.loc[df['hash_num']<=10], x='m/n', y='FP_ratio', color='hash_num')
        fig.show()
        pio.write_image(fig, self._dir + 'fig1.jpeg', width=1000, height=800)
        
        groups = df.groupby(by='m/n')
        for key, grp in groups:
            fig = px.line(grp, x='hash_num', y='FP_ratio')
            fig.show()
            pio.write_image(fig, self._dir + f'm_over_n={key}.jpeg', width=1000, height=800)
    

if __name__ == '__main__':
    test_obj = TestBloomFilter()
    test_obj.run_initial_test()
    df = test_obj.run_with_random_words()
    test_obj.plot_line_charts(df)
