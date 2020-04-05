#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Shining'
__email__ = 'mrshininnnnn@gmail.com'


#public
import torch
from torch.utils import data as torch_data

import random
import numpy as np

# private
from ..models import (gru_rnn, lstm_rnn, 
    bi_gru_rnn, bi_lstm_rnn, 
    bi_gru_rnn_att, bi_lstm_rnn_att)


class OfflineEnd2EndDataset(torch_data.Dataset):
    """docstring for OfflineEnd2EndDataset"""
    def __init__(self, data_dict):
        super(OfflineEnd2EndDataset, self).__init__()
        self.xs = data_dict['xs']
        self.ys = data_dict['ys']
        self.data_size = len(self.xs)

    def __len__(self): 
        return self.data_size

    def __getitem__(self, idx): 
        return self.xs[idx], self.ys[idx]


class OnlineEnd2EndDataset(torch_data.Dataset):
    """docstring for OnlineEnd2EndDataset"""
    def __init__(self, data_dict, data_src):
        super(OnlineEnd2EndDataset, self).__init__() 
        self.data_src = data_src
        self.xs = data_dict['xs']
        self.ys = data_dict['ys']
        self.data_size = len(self.xs)

    def __len__(self): 
        return self.data_size

    def __getitem__(self, idx): 
        if self.data_src == 'aoi':
            return self.ys[idx]
        elif self.data_src == 'nss':
            return self.xs[idx], self.ys[idx]


class OfflineRecursionDataset(torch_data.Dataset):
      """Custom data.Dataset compatible with data.DataLoader."""
      def __init__(self, data_dict):
            super(OfflineRecursionDataset, self).__init__()
            self.xs = data_dict['xs']
            self.ys_ = data_dict['ys_']
            self.data_size = len(self.xs)

      def __len__(self):
            return self.data_size

      def __getitem__(self, idx):
            return self.xs[idx], self.ys_[idx]

class OnlineRecursionDataset(torch_data.Dataset):
      """Custom data.Dataset compatible with data.DataLoader."""
      def __init__(self, data_dict, data_src):
            super(OnlineRecursionDataset, self).__init__()
            self.data_src = data_src
            self.xs = data_dict['xs']
            self.ys = data_dict['ys']
            self.data_size = len(self.xs)

      def __len__(self):
            return self.data_size

      def __getitem__(self, idx):
        if self.data_src == 'aoi':
            return self.ys[idx]
        elif self.data_src == 'nss':
            return self.xs[idx]


class OfflineTaggingDataset(torch_data.Dataset):
      """Custom data.Dataset compatible with data.DataLoader."""
      def __init__(self, data_dict):
            super(OfflineTaggingDataset, self).__init__()
            self.xs = data_dict['xs']
            self.ys_ = data_dict['ys_']
            self.data_size = len(self.xs)

      def __len__(self):
            return self.data_size

      def __getitem__(self, idx):
            return self.xs[idx], self.ys_[idx]

class OnlineTaggingDataset(torch_data.Dataset):
      """Custom data.Dataset compatible with data.DataLoader."""
      def __init__(self, data_dict):
            super(OnlineTaggingDataset, self).__init__()
            self.ys = data_dict['ys']
            self.data_size = len(self.ys)

      def __len__(self):
            return self.data_size

      def __getitem__(self, idx):
            return self.ys[idx]

def pick_model(config, method):
    if config.model_name == 'gru_rnn':
        if method == 'end2end':
            return gru_rnn.End2EndModelGraph(config).to(config.device)
        elif method == 'recursion':
            return gru_rnn.RecursionModelGraph(config).to(config.device)
    elif config.model_name == 'lstm_rnn':
        if method == 'end2end':
            return lstm_rnn.End2EndModelGraph(config).to(config.device)
        elif method == 'recursion':
            return lstm_rnn.RecursionModelGraph(config).to(config.device)
    elif config.model_name == 'bi_gru_rnn':
        if method == 'end2end':
            return bi_gru_rnn.End2EndModelGraph(config).to(config.device)
        elif method == 'recursion':
            return bi_gru_rnn.RecursionModelGraph(config).to(config.device)
    elif config.model_name == 'bi_lstm_rnn':
        if method == 'end2end':
            return bi_lstm_rnn.End2EndModelGraph(config).to(config.device)
        elif method == 'recursion':
            return bi_lstm_rnn.RecursionModelGraph(config).to(config.device)
    elif config.model_name =='bi_gru_rnn_att':
        if method == 'end2end':
            return bi_gru_rnn_att.End2EndModelGraph(config).to(config.device)
        if method == 'recursion':
            return bi_gru_rnn_att.RecursionModelGraph(config).to(config.device)
    elif config.model_name =='bi_lstm_rnn_att':
        if method == 'end2end':
            return bi_lstm_rnn_att.End2EndModelGraph(config).to(config.device)
        if method == 'recursion':
            return bi_lstm_rnn_att.RecursionModelGraph(config).to(config.device)

def get_list_mean(l: list) -> float:
    return sum(l) / len(l)

def init_parameters(model): 
    for name, parameters in model.named_parameters(): 
        if 'weight' in name: 
            torch.nn.init.normal_(parameters.data, mean=0, std=0.01)
        else:
            torch.nn.init.constant_(parameters.data, 0)

def count_parameters(model): 
    # get total size of trainable parameters 
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def show_config(config, model):
    # general information
    general_info = '\n*Configuration*'
    general_info += '\nmodel: {}'.format(config.model_name)
    general_info += '\ntrainable parameters:{:,.0f}'.format(config.num_parameters)
    model_info = '\nmodel state_dict:'
    for parameters in model.state_dict():
        model_info += '\n{}\t{}'.format(parameters, model.state_dict()[parameters].size())
    general_info += model_info
    general_info += '\ndevice: {}'.format(config.device)
    general_info += '\nuse gpu: {}'.format(config.use_gpu)
    general_info += '\ntrain size: {}'.format(config.train_size)
    general_info += '\nval size: {}'.format(config.val_size)
    general_info += '\ntest size: {}'.format(config.test_size)
    general_info += '\nsource vocab size: {}'.format(config.src_vocab_size)
    general_info += '\ntarget vocab size: {}'.format(config.tgt_vocab_size)
    general_info += '\nbatch size: {}'.format(config.batch_size)
    general_info += '\ntrain batch: {}'.format(config.train_batch)
    general_info += '\nval batch: {}'.format(config.val_batch)
    general_info += '\ntest batch: {}'.format(config.test_batch)
    general_info += '\nif load check point: {}'.format(config.load_check_point)
    if config.load_check_point:
        general_info += '\nModel restored from {}'.format(config.LOAD_POINT)
    general_info += '\n'
    print(general_info)

    return general_info

def translate(seq: list, trans_dict: dict) -> list: 
    return [trans_dict[token] for token in seq]

def rm_pad(seq, pad_idx):
    return [i for i in seq if i != pad_idx]

def rm_pads(srcs, tgts, preds, pad_idx): 
    srcs = [rm_pad(src, pad_idx) for src in srcs] 
    tgts = [rm_pad(tgt, pad_idx) for tgt in tgts] 
    preds = [rm_pad(pred, pad_idx) for pred in preds] 
    return srcs, tgts, preds

def save_check_point(step, epoch, model_state_dict, opt_state_dict, path):
    # save model, optimizer, and everything required to keep
    checkpoint_to_save = {
        'step': step, 
        'epoch': epoch, 
        'model': model_state_dict(), 
        'optimizer': opt_state_dict()}
    torch.save(checkpoint_to_save, path)
    print('Model saved as {}.'.format(path))

def rand_sample(srcs, tars, preds, src_dict, tar_dict, pred_dict): 
    src, tar, pred = random.choice([(src, tar, pred) for src, tar, pred in zip(srcs, tars, preds)])
    src = translate(src, src_dict)
    tar = translate(tar, tar_dict)
    pred = translate(pred, pred_dict)
    return ' '.join(src), ' '.join(tar), ' '.join(pred)

def find_next_step_in_bubble_sort(seq): 
    n = len(seq) 
    for j in range(0, n-1):
        if seq[j] > seq[j+1]:
            return j
    return -1

def bubble_sort_step(seq, j): 
    # perform one bubble sort step
    seq[j], seq[j+1] = seq[j+1], seq[j] 
    return seq

def convert_to_int(seq:list) -> list:
    return [int(str_number) for str_number in seq]

def convert_to_str(seq:list) -> str:
    return [str(int_number) for int_number in seq]

def end2end_online_generator(data_src: str, data) -> list:
    # online training data generation
    # for Arithmetic Operators Insertion (AOI)
    if data_src == 'aoi':
        # make a copy
        y = data.copy() # list
        x = y.copy()
        # get operator indexes
        operator_idxes = [i for i, token in enumerate(y) if not token.isdigit()][::-1]
        # decide how many operators to remove
        num_idxes = np.random.choice(range(len(operator_idxes)+1))
        if num_idxes == 0:
            return x, y
        else:
            # decide operators to remove
            idxes_to_remove = operator_idxes[:num_idxes]
            x = [x[i] for i in range(len(x)) if i not in idxes_to_remove]
            return x, y
    # for Number Sequence Sorting (NSS)
    elif data_src == 'nss':
        x, y = data # tuple of list
        x = convert_to_int(x)
        xs = [x.copy()]
        while True:
            j = find_next_step_in_bubble_sort(x)
            if j == -1:
                break
            x = bubble_sort_step(x, j)
            xs.append(x.copy())
        index = np.random.choice(range(len(xs)))
        x = convert_to_str(xs[index])
        return x, y

def recursion_online_generator(data_src: str, data: list) -> list:
    # online training data generation
    # for Arithmetic Operators Insertion (AOI)
    if data_src == 'aoi':
        # make a copy
        y = data.copy() # list
        x = y.copy()
        # get operator indexes
        operator_idxes = [i for i, token in enumerate(y) if not token.isdigit()][::-1]
        # decide how many operators to remove
        num_idxes = np.random.choice(range(len(operator_idxes)+1))
        if num_idxes == 0:
            return x, ['<completion>', '<none>', '<none>']
        else:
            # decide operators to remove
            idxes_to_remove = operator_idxes[:num_idxes]
            # generat label
            y = ['<insertion>', str(idxes_to_remove[-1]), x[idxes_to_remove[-1]]]
            # generate sample
            x = [x[i] for i in range(len(x)) if i not in idxes_to_remove]
            return x, y
    # for Number Sequence Sorting (NSS)
    elif data_src == 'nss':
        # make a copy
        x = data.copy()
        x = convert_to_int(x)
        xs = [x.copy()]
        ys_ = []
        while True:
            y_ = find_next_step_in_bubble_sort(x)
            ys_.append(y_)
            if y_ == -1:
                break
            x = bubble_sort_step(x, y_)
            xs.append(x.copy())
        index = np.random.choice(range(len(xs)))
        x = convert_to_str(xs[index])
        y_ = [str(ys_[index])]
        return x, y_

def tagging_online_generator(y: list) -> list:
    # make a copy
    x = y.copy()
    # get operator indexes
    operator_idxes = [i for i, token in enumerate(y) if not token.isdigit()][::-1]
    # decide how many operators to remove
    num_idxes = np.random.choice(range(len(operator_idxes)+1))
    if num_idxes == 0:
        return x, ['<keep>']*len(y)
    else:
        # decide operators to remove
        idxes_to_remove = operator_idxes[:num_idxes]
        x = [x[i] for i in range(len(x)) if i not in idxes_to_remove]
        # generate tagging label
        x_ = x.copy()
        y_ = []
        x_token = x_.pop(0)
        for i in range(len(y)):
            y_token = y[i]
            if x_token == y_token: 
                y_.append('<keep>')
                if len(x_) == 0:
                    break
                x_token = x_.pop(0)
            else:
                y_.append('<add_{}>'.format(y_token))

        return x, y_

def preprocess(xs, ys, src_vocab2idx_dict, tgt_vocab2idx_dict, end_idx=None): 
    # vocab to index
    xs = [translate(x, src_vocab2idx_dict) for x in xs]
    ys = [translate(y, tgt_vocab2idx_dict) for y in ys]
    if end_idx is not None:
        # add end symbol and save as tensor
        xs = [torch.Tensor(x + [end_idx]) for x in xs]
        ys = [torch.Tensor(y + [end_idx]) for y in ys] 
    else:
        # convert to tensor
        xs = [torch.Tensor(x) for x in xs]
        ys = [torch.Tensor(y) for y in ys] 

    return xs, ys

def padding(seqs, max_len=None):
    # zero padding
    seq_lens = [len(seq) for seq in seqs]
    if max_len is None:
        max_len = max(seq_lens)
    # default pad index is 0
    padded_seqs = torch.zeros([len(seqs), max_len]).long()
    for i, seq in enumerate(seqs): 
        seq_len = seq_lens[i]
        padded_seqs[i, :seq_len] = seq[:seq_len]
    return padded_seqs, seq_lens

def one_step_infer(xs, ys_, src_idx2vocab_dict, src_vocab2idx_dict, tgt_idx2vocab_dict, config): 
    # detach from devices
    xs = xs.cpu().detach().numpy() 
    ys_ = torch.argmax(ys_, dim=2).cpu().detach().numpy() 
    # remove padding
    xs = [rm_pad(x, config.pad_idx) for x in xs] 
    # convert index to vocab
    xs = [translate(x, src_idx2vocab_dict) for x in xs]
    ys_ = [translate(y_, tgt_idx2vocab_dict) for y_ in ys_]
    # inference function for Arithmetic Operators Insertion (AOI)
    if config.data_src == 'aoi':
        if np.array_equal(np.array(ys_)[:, 0], np.array(['<completion>']*len(ys_))):
            done = True
        else:
            done = False
            for x, y_ in zip(xs, ys_): 
                if y_[0] == '<insertion>' and y_[1].isdigit() and y_[2] in set(['+', '-', '*', '/', '==']): 
                    x.insert(int(y_[1]), y_[2]) 
        xs = [torch.Tensor(translate(x, src_vocab2idx_dict)) for x in xs]
        # TODO: why padding leads to an incorrect prediction
        xs, x_lens = padding(xs, config.seq_len*2)
        # xs, x_lens = padding(xs)
    # inference function for Number Sequence Sorting (NSS)
    elif config.data_src == 'nss': 
        if np.array_equal(np.array(ys_), np.full(np.array(ys_).shape, -1).astype(str)):
            done = True
        else:
            done = False
            for i in range(len(xs)):
                y_ = ys_[i]
                if y_[0].isdigit():
                    idx = int(y_[0])
                    xs[i][idx], xs[i][idx+1] = xs[i][idx+1], xs[i][idx]
        xs = [torch.Tensor(translate(x, src_vocab2idx_dict)) for x in xs]
        xs, x_lens = padding(xs)
    return xs.to(config.device), torch.Tensor(x_lens).to(config.device), done

def recursive_infer(xs, x_lens, model, max_infer_step, 
    src_idx2vocab_dict, src_vocab2idx_dict, tgt_idx2vocab_dict, config, done=False):
    # recursive inference in valudation and testing
    # for Arithmetic Operators Insertion (AOI)
    if max_infer_step == 0:
        return xs, x_lens, False
    else:
        xs, x_lens, done = recursive_infer(xs, x_lens, model, max_infer_step-1, 
            src_idx2vocab_dict, src_vocab2idx_dict, tgt_idx2vocab_dict, config, done) 
        if done:
            return xs, x_lens, done
        else:
            ys_ = model(xs, x_lens) 
            xs, x_lens, done = one_step_infer(xs, ys_, 
                src_idx2vocab_dict, src_vocab2idx_dict, tgt_idx2vocab_dict, config)
            return xs, x_lens, done

def tagging_execution(x, y_):
    p = []
    x_ = x.copy()
    x_token = x_.pop(0)
    for y_token in y_:
        if y_token == '<keep>':
            # keep symbol
            p.append(x_token)
            if len(x_) == 0:
                break
            x_token = x_.pop(0)
        elif 'add' in y_token:
            # add symbol
            y_token = y_token.split('<add_')[1].split('>')[0]
            p.append(y_token)
        else:
            # end symbol
            p.append(y_token)
    return p

def tagging_infer(xs, ys_, src_idx2vocab_dict, src_vocab2idx_dict, tgt_idx2vocab_dict):
    # convert index to vocab
    xs = [translate(x, src_idx2vocab_dict) for x in xs]
    ys_ = [translate(y_, tgt_idx2vocab_dict) for y_ in ys_]
    preds = [tagging_execution(x, y_) for x, y_ in zip(xs, ys_)]
    # convert vocab to index
    return [translate(p, src_vocab2idx_dict) for p in preds]

