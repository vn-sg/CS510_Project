from flask import Flask, jsonify, request
from flask_cors import CORS
import random

import torch
from torch import nn, optim
import torchtext
import os
import argparse

import pandas as pd
import random

from dataloader import tokenizer, get_dataset_using_glove_50, get_dataset_using_glove_25, glove_sentence_vectorize, \
    get_dataset_v0
from model import TwitterDetector
from loss import F1_Loss
import json

app = Flask(__name__)
CORS(app)
model = None
vocab = None

@app.route('/')
def main_JSON():
    if (request.method == 'GET'):
        return jsonify(
            res='Hello World'
        )


@app.route('/quit')
def end():
    res = {
        'res': 'Bye, World!'
    }
    return jsonify(res)


@app.route('/getScore', methods=['POST'])
def getScore():
    if (request.method == 'POST'):
        content = request.json
        # content = content.text
        print(f"\n<INPUT>\n{content}\n</INPUT>")
        print(model)
        model.eval()
        vectorized = glove_sentence_vectorize(content, vocab)
        score = model(torch.tensor(vectorized, dtype=torch.float))
        score = score.item()
        print(f"SCORE for \"{content}\":\t{score}")
        res = {
            'score': score
        }
        return jsonify(res)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default='data/subtasks-english/CT22_english_1A_checkworthy', type=str)
    parser.add_argument('--model_type', default='linear', type=str)
    parser.add_argument('--model_name', default='nn_linear_glove', type=str)
    parser.add_argument('--batch_size', default=128, type=int)
    parser.add_argument('--layer_num', default=3, type=int)
    parser.add_argument('--hidden_states', default=64, type=int)
    parser.add_argument('--epoch', default=60, type=int)
    parser.add_argument('--input_dim', default=25, type=int)
    parser.add_argument('--lr', default=0.01, type=float)
    cfg = parser.parse_args()
    _, _, vocab = get_dataset_using_glove_25(
        os.path.join('data/subtasks-english/CT22_english_1A_checkworthy', 'CT22_english_1A_checkworthy_train.tsv'),
        os.path.join('data/subtasks-english/CT22_english_1A_checkworthy', 'CT22_english_1A_checkworthy_dev.tsv'))
    model = TwitterDetector(cfg)
    model.load_state_dict(torch.load('models/nn_linear_glove.pt'))
    app.run(host="localhost", port=35678)
