#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Shining'
__email__ = 'mrshininnnnn@gmail.com'


# public
import torch
import torch.nn as nn
import random
# private
from .encoder import *
from .decoder import *


class End2EndModelGraph(nn.Module): 
    """docstring for End2EndModelGraph""" 
    def __init__(self, config): 
        super(End2EndModelGraph, self).__init__() 
        self.config = config
        self.encoder = BiLSTMRNNEncoder(config)
        self.decoder = AttBiLSTMRNNDecoder(config)

    def forward(self, xs, x_lens, ys, teacher_forcing_ratio=0.5):
        # xs: batch_size, max_xs_seq_len
        # x_lens: batch_size
        # ys: batch_size, max_ys_seq_len
        batch_size = xs.shape[0]
        max_ys_seq_len = ys.shape[1]
        # encoder_output: batch_size, max_xs_seq_len, en_hidden_size
        # decoder_hidden: (h, c)
        # h, c: 1, batch_size, en_hidden_size
        encoder_output, decoder_hidden = self.encoder(xs)
        # batch_size
        decoder_input = torch.empty(
            batch_size, 
            dtype=torch.int64, 
            device=self.config.device)
        decoder_input.fill_(self.config.start_idx)
        # max_ys_seq_len, batch_size, vocab_size
        decoder_outputs = torch.zeros(
            max_ys_seq_len, 
            batch_size, 
            self.config.tgt_vocab_size, 
            device=self.config.device)
        # greedy search with teacher forcing
        for i in range(max_ys_seq_len):
            # decoder_output: batch_size, vocab_size
            # decoder_hidden: (h, c)
            # h, c: 1, batch_size, en_hidden_size
            decoder_output, decoder_hidden = self.decoder(
                decoder_input, decoder_hidden, encoder_output, x_lens)
            # batch_size, vocab_size
            decoder_outputs[i] = decoder_output
            # 1, batch_size
            decoder_input = ys[:, i] if random.random() < teacher_forcing_ratio \
            else decoder_output.max(1)[1]
        # batch_size, max_ys_seq_len, vocab_size
        return decoder_outputs.transpose(0, 1)


# class RecursionModelGraph(nn.Module): 
#     """docstring for RecursionModelGraph""" 
#     def __init__(self, config): 
#         super(RecursionModelGraph, self).__init__() 
#         self.config = config
#         self.encoder = GRURNNEncoder(config)
#         self.decoder = GRURNNDecoder(config)

#     def forward(self, xs):
#         # xs: batch_size, max_xs_seq_len
#         batch_size, max_xs_seq_len = xs.shape
#         max_ys_seq_len = 4 # action, position, token, EOS
#         # max_xs_seq_len, batch_size, en_hidden_size
#         encoder_outputs = torch.zeros(
#             max_xs_seq_len, 
#             batch_size, 
#             self.config.en_hidden_size, 
#             device=self.config.device)
#         # 1, batch_size, en_hidden_size
#         encoder_hidden = self.encoder.init_hidden(batch_size)
#         for i in range(max_xs_seq_len):
#             # 1, batch_size, en_hidden_size
#             # num_layers*num_directions, batch_size, en_hidden_size
#             encoder_output, encoder_hidden = self.encoder(xs[None, :, i], encoder_hidden)
#             # batch_size, en_hidden_size
#             encoder_outputs[i] = encoder_output
#         # 1, batch_size
#         decoder_input = torch.empty(
#             1, 
#             batch_size, 
#             dtype=torch.int64, 
#             device=self.config.device)
#         decoder_input.fill_(self.config.start_idx)
#         # 1, batch_size, en_hidden_size
#         decoder_hidden = encoder_hidden
#         # max_ys_seq_len, batch_size, vocab_size
#         decoder_outputs = torch.zeros(
#             max_ys_seq_len, 
#             batch_size, 
#             self.config.tgt_vocab_size, 
#             device=self.config.device)
#         # greedy search with teacher forcing
#         for i in range(max_ys_seq_len):
#             # batch_size, vocab_size
#             # num_layers*num_directions, batch_size, de_hidden_size
#             decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden)
#             # batch_size, vocab_size
#             decoder_outputs[i] = decoder_output
#             # 1, batch_size
#             decoder_input = decoder_output.max(1)[1].unsqueeze(0)
#         # batch_size, max_ys_seq_len, vocab_size
#         return decoder_outputs.transpose(0, 1)