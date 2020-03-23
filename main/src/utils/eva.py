#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Shining'
__email__ = 'ning.shi@learnable.ai'

import numpy as np

class Evaluate():
    """a class to process evaluation"""
    def __init__(self, config, targets, predictions, idx2vocab_dict): 
        self.config = config
        self.idx2vocab_dict = idx2vocab_dict
        self.tars = targets
        self.preds = predictions
        self.size = len(targets)
        # if hold equation
        self.acc = self.get_acc()
        # token-level accuracy
        self.token_acc = self.get_token_acc()
        # sequence-level accuracy
        self.seq_acc = self.get_seq_acc()

    def check_equation(self, pred): 
        pred = [self.idx2vocab_dict[i] for i in pred][:-1]
        try:
            right_side = pred[-1]
            left_side = pred[:-2]
            if eval(' '.join(pred)) and float(eval(' '.join(left_side))) == float(right_side):
                return 1
            else:
                return 0
        except:
            return 0
        return 0

    def check_token(self, tar, pred):
        min_len = min([len(tar), len(pred)])
        return np.float32(sum(np.equal(tar[:min_len], pred[:min_len]))/len(tar))

    def check_seq(self, tar, pred): 
        min_len = min([len(tar), len(pred)]) 
        if sum(np.equal(tar[:min_len], pred[:min_len])) == len(tar): 
            return 1
        return 0

    def get_acc(self):
        a = 0
        for i in range(self.size):
            pred = self.preds[i]
            a += self.check_equation(pred)
        return np.float32(a/self.size)

    def get_token_acc(self):
        a = 0
        for i in range(self.size):
            tar = self.tars[i]
            pred = self.preds[i]
            a += self.check_token(tar, pred)
        return np.float32(a/self.size)

    def get_seq_acc(self): 
        a = 0
        for i in range(self.size):
            tar = self.tars[i]
            pred = self.preds[i]
            a += self.check_seq(tar, pred)
        return np.float32(a/self.size)