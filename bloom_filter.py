# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 18:11:45 2022

@author: snourashrafeddin
"""
import mmh3
from bitarray import bitarray

class Bloomfilter():
    
    def __init__(self, mask_size, hash_num):
        self.mask_size = mask_size
        self.hash_num = hash_num
        self.mask = bitarray(self.mask_size)
        self.mask.setall(0)
        
    def add_word(self, word):
        for i in range(self.hash_num):
            bit = mmh3.hash128(word, i, signed=False)%self.mask_size
            self.mask[bit] = 1
            
    def exist_word(self, word):
        for i in range(self.hash_num):
            bit = mmh3.hash128(word, i, signed=False)%self.mask_size
            if self.mask[bit] == 0:
                return False
        return True
        
        