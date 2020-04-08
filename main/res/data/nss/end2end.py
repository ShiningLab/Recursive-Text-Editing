#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Shining'
__email__ = 'mrshininnnnn@gmail.com'


# dependency
# public
import os
import argparse
import numpy as np
from collections import Counter
# private
from utils import *


class End2EndDataPreprocess(object):
    """docstring for End2EndDataPreprocess"""
    def __init__(self, num_size, seq_len, data_size):
        super(End2EndDataPreprocess, self).__init__()
        self.num_size = num_size
        self.seq_len = seq_len
        self.data_size = data_size
        self.init_paths()
        self.data_preprocess()
        self.save()

    def init_paths(self):
        # load path
        self.data_src = 'nss'
        self.indir = os.path.join(self.data_src, 
            'num_size_{}'.format(self.num_size), 
            'seq_len_{}'.format(self.seq_len), 
            'data_size_{}'.format(self.data_size))
        # save path
        outdir = 'end2end'
        self.outdir = os.path.join(outdir, 'num_size_{}'.format(self.num_size), 
            'seq_len_{}'.format(self.seq_len), 
            'data_size_{}'.format(self.data_size))
        if not os.path.exists(self.outdir): os.makedirs(self.outdir)

    def data_preprocess(self):
        # load raw dataset
        raw_train_xs = load_txt(os.path.join(self.indir, 'train_x.txt'))
        raw_train_ys = load_txt(os.path.join(self.indir, 'train_y.txt'))
        raw_val_xs = load_txt(os.path.join(self.indir, 'val_x.txt'))
        raw_val_ys = load_txt(os.path.join(self.indir, 'val_y.txt'))
        raw_test_xs = load_txt(os.path.join(self.indir, 'test_x.txt'))
        raw_test_ys = load_txt(os.path.join(self.indir, 'test_y.txt'))
        # check data size
        print('train sample size', len(raw_train_xs))
        print('train label size', len(raw_train_ys))
        print('val sample size', len(raw_val_xs))
        print('val label size', len(raw_val_ys))
        print('test sample size', len(raw_test_xs))
        print('test label size', len(raw_test_ys))
        # train
        # white space tokenization
        train_xs = white_space_tokenizer(raw_train_xs)
        train_ys = white_space_tokenizer(raw_train_ys)
        # vocabulary frequency distribution
        counter = Counter()
        for x in train_xs:
            counter.update(x)
        src_vocab_list = sorted(counter.keys())
        # soruce vocabulary dictionary
        src_vocab2idx_dict = dict()
        src_vocab2idx_dict['<pad>'] = 0 # to pad sequence length

        i = len(src_vocab2idx_dict)
        for token in src_vocab_list:
            src_vocab2idx_dict[token] = i
            i += 1
        # target vocabulary frequency distribution
        counter = Counter()
        for y in train_ys:
            counter.update(y)
        tgt_vocab_list = sorted(counter.keys())
        # target vocabulary dictionary
        tgt_vocab2idx_dict = dict()
        tgt_vocab2idx_dict['<pad>'] = 0 # to pad sequence length
        tgt_vocab2idx_dict['<s>'] = 1 # to mark the start of a sequence
        tgt_vocab2idx_dict['</s>'] = 2 # to mark the end of a sequence

        i = len(tgt_vocab2idx_dict)
        for token in tgt_vocab_list:
            tgt_vocab2idx_dict[token] = i
            i += 1
        # val
        # white space tokenization
        val_xs = white_space_tokenizer(raw_val_xs)
        val_ys = white_space_tokenizer(raw_val_ys)
        # test
        # white space tokenization
        test_xs = white_space_tokenizer(raw_test_xs)
        test_ys = white_space_tokenizer(raw_test_ys)
        # combine data sets to a dict
        train_dict = {}
        train_dict['xs'] = train_xs
        train_dict['ys'] = train_ys

        val_dict = {}
        val_dict['xs'] = val_xs
        val_dict['ys'] = val_ys

        test_dict = {}
        test_dict['xs'] = test_xs
        test_dict['ys'] = test_ys

        self.data_dict = dict()
        self.data_dict['train'] = train_dict
        self.data_dict['val'] = val_dict
        self.data_dict['test'] = test_dict

        self.vocab_dict = dict()
        self.vocab_dict['src'] = src_vocab2idx_dict
        self.vocab_dict['tgt'] = tgt_vocab2idx_dict

    def save(self):
        # save output as json
        data_path = os.path.join(self.outdir, 'data.json')
        vocab_path = os.path.join(self.outdir, 'vocab.json')

        save_json(data_path, self.data_dict)
        save_json(vocab_path, self.vocab_dict)

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
    # data preprocess
    E2EDP = End2EndDataPreprocess(
        num_size=args.num_size, 
        seq_len=args.seq_len, 
        data_size=args.data_size) 
    
if __name__ == '__main__':
      main()