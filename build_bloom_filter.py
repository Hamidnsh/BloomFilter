# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 10:57:57 2022

@author: snourashrafeddin
"""

from bloom_filter import BloomFilter

class BloomFilterWrapper():
    def __init__(self, filter_size=200, hash_num=5):
        self.filter_size = filter_size
        self.hash_num = hash_num
        self.filter = BloomFilter(filter_size=filter_size, hash_num=hash_num)
    
    def get_filter(self):
        return self.filter
    
    def get_filter_size(self):
        return self.filter_size
    
    def get_filter_hash_num(self):
        return self.hash_num
    
    def rest_filter(self):
        self.filter = BloomFilter(filter_size=self.filter_size, hash_num=self.hash_num)
    
    def reset_new_filter(self, filter_size, hash_num):
        self.filter_size = filter_size
        self.hash_num = hash_num
        self.filter = BloomFilter(filter_size=filter_size, hash_num=hash_num)
    
    def add_word(self, word):
        self.filter.add_word(word.strip().lower())
    
    def add_word_form_list(self, word_list):
        for word in word_list:
            self.add_word(word)
    
    def add_word_form_file(self, file):
        with open(file, 'r') as fin:
            dic_words = [word.strip().rstrip('\n') for word in fin]
        self.add_word_form_list(dic_words)
        return len(dic_words)
        
    def exist_word(self, word):
        return int(self.filter.exist_word(word.strip().lower()))
    
    def exist_word_from_list(self, word_list):
        return [self.exist_word(word) for word in word_list]
    
    def exist_word_from_file(self, file):
        with open(file, 'r') as fin:
            dic_words = [word.strip().rstrip('\n') for word in fin]
        return self.exist_word_from_list(dic_words)

if __name__ == '__main__':
    build_obj = BloomFilterWrapper(20000000000,12)
    words = ['bloom', 'Filter', 'BuiLD']
    build_obj.add_word_form_list(words)
    print(build_obj.exist_word_from_list(words))
    build_obj.add_word('Hamid')
    print(build_obj.exist_word(' hAMid'))
    print(build_obj.exist_word('blo om'))
    word_num = build_obj.add_word_form_file('wordlist.txt')
    print(f'{word_num} words added!')
    res = build_obj.exist_word_from_file('wordlist.txt')
    print(f'{sum(res)} words exist!')
    
    
   