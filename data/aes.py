#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Shining'
__email__ = 'mrshininnnnn@gmail.com'


# dependency
# public
import os
import argparse
import numpy as np
from tqdm import tqdm
# private
from utils import *


# class for data generation of the Arithmetic Equation Simplification (AES) problem 
class ArithmeticEquationSimplification(): 
    """docstring for ArithmeticEquationSimplification"""
    def __init__(self, operators, num_size):
        super().__init__()
        self.operators = operators
        self.pos_digits = np.arange(2, num_size+2).tolist()
        self.neg_digits = np.arange(-num_size, -1).tolist()
        self.digits = self.pos_digits + self.neg_digits
    
    def gen_base_dict(self):
        return {str(i):[] for i in self.pos_digits}
    
    def expand_base_dict(self):
        for a in self.digits:
            for o in self.operators:
                for b in self.pos_digits:
                    try:
                        e = [str(a), o, str(b)]
                        v = str(eval(''.join(e)))
                        e[0] = e[0].replace('-', '- ')
                        e = ' '.join(list(e))
                        if v in self.base_dict:
                            self.base_dict[v].append('( {} )'.format(e))
                    except:
                        pass
    
    def gen_operation(self, seq_len):
        if seq_len == 1:
            a = np.random.choice(self.digits)
            return [str(a)]
        else:
            left_side  = self.gen_operation(seq_len-1)
            o = np.random.choice(self.operators)
            b = np.random.choice(self.pos_digits)
            return left_side + [o, str(b)]
    
    def gen_operation_list(self, seq_len, data_size):
        # to control the data size
        operations_pool = set()
        for i in tqdm(range(data_size)):
            while True: 
                # to avoid duplicates
                operation = self.gen_operation(seq_len) 
                if ''.join(operation) in operations_pool: 
                    continue
                else:
                    operations_pool.add(''.join(operation)) 
                # to avoid zero division error
                try: 
                    # flost to int to string
                    value = eval(''.join(operation))
                    if value % 1 != 0.: 
                        continue
                    else:
                        value = str(int(value))
                        # to keep vocab size
                        if value in self.value_dict: 
                            self.value_dict[value].append(operation)
                            break
                except: 
                    pass
    
    def gen_equation_list(self):
        ys = []
        for v in self.value_dict:
            for y in self.value_dict[v]:
                y = y[0].replace('-', '- ').split() + y[1:]
                y += ["=="] + [v]
                ys.append(' '.join(y))
        return ys
    
    def replace_numbers(self, ys):
        xs = []
        for y in ys:
            y = y.split()
            num_idx = [i for i, token in enumerate(y) if token.isdigit()]
            num_to_replace = np.random.choice(range(len(num_idx)+1))
            idx_to_replace = np.random.choice(num_idx, num_to_replace, False)
            for i in idx_to_replace:
                y[i] = np.random.choice(self.base_dict[y[i]])
            xs.append(' '.join(y))
        return xs
                
    def generate(self, seq_len, data_size):
        # input sequences, output sequences
        xs, ys = [], []
        self.base_dict = self.gen_base_dict()
        self.value_dict = self.gen_base_dict()
        self.expand_base_dict()
        self.gen_operation_list(
            seq_len=seq_len, 
            data_size=data_size)
        ys = self.gen_equation_list()
        xs = self.replace_numbers(ys)
        
        return xs, ys

def train_test_split(xs, ys): 
    # train val test split
    dataset = np.array([(x, y) for x, y in zip(xs, ys)])
    data_size = dataset.shape[0]
    indices = np.random.permutation(data_size)
    train_size = int(0.7*data_size)
    val_size = int(0.15*data_size)
    test_size = data_size - train_size - val_size
    train_idxes = indices[:train_size]
    val_idxes = indices[train_size: train_size+val_size]
    test_idxes = indices[train_size+val_size:]
    trainset = dataset[train_idxes]
    valset = dataset[val_idxes]
    testset = dataset[test_idxes]
    print('train size', train_size, trainset.shape)
    print('val size', val_size, valset.shape)
    print('test size', test_size, testset.shape)

    return trainset, valset, testset

def save_dataset(trainset, valset, testset, args): 
    outdir = 'aes' 
    outdir = os.path.join(
        outdir, 
        'num_size_{}'.format(args.num_size), 
        'seq_len_{}'.format(args.seq_len), 
        'data_size_{}'.format(args.data_size))
    
    if not os.path.exists(outdir): 
        os.makedirs(outdir)

    save_txt(os.path.join(outdir, 'train_x.txt'), trainset[:, 0])
    save_txt(os.path.join(outdir, 'train_y.txt'), trainset[:, 1])
    save_txt(os.path.join(outdir, 'val_x.txt'), valset[:, 0])
    save_txt(os.path.join(outdir, 'val_y.txt'), valset[:, 1])
    save_txt(os.path.join(outdir, 'test_x.txt'), testset[:, 0])
    save_txt(os.path.join(outdir, 'test_y.txt'), testset[:, 1])

    print("find output from", outdir)

def main():
    # parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_size', 
        type=int, 
        required=True, 
        help='define the number of real digits to involve')
    parser.add_argument('--seq_len', 
        type=int, 
        required=True, 
        help='define the sequence length of inputs')
    parser.add_argument('--data_size', 
        type=int, 
        required=True, 
        help='define the total data size')
    args = parser.parse_args()
    # data generation 
    operators = ['+', '-', '*', '/'] #TODO
    aes = ArithmeticEquationSimplification(operators, args.num_size) 
    xs, ys = aes.generate(
        seq_len=args.seq_len-1, 
        data_size=args.data_size)
    trainset, valset, testset = train_test_split(xs, ys)
    save_dataset(trainset, valset, testset, args)

if __name__ == '__main__': 
    main()