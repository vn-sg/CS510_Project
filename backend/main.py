import torch
from torch import nn, optim
import torchtext
import os
import argparse

import pandas as pd
import random

from dataloader import tokenizer, get_dataset_using_glove_50, get_dataset_using_glove_25, glove_sentence_vectorize, get_dataset_v0
from model import TwitterDetector
from loss import F1_Loss

from scorer.subtask_1 import evaluate
from format_checker.subtask_1 import check_format


seed = 123
torch.manual_seed(seed)
random.seed(seed)


def train(args):
    #train_loader, test_loader, vocab = get_dataset_v0(args)
    train_loader, test_loader, vocab = get_dataset_using_glove_25(os.path.join(args.data_dir, 'CT22_english_1A_checkworthy_train.tsv'), os.path.join(args.data_dir, 'CT22_english_1A_checkworthy_dev.tsv'))
    model = TwitterDetector(args)
    F1_criterion = F1_Loss()
    BCE_criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    for iteration in range(args.epoch + 1):
        train_loss = 0.0
        train_size = 0
        for i, (X, y) in enumerate(train_loader):
            model.train()
            optimizer.zero_grad()
            yhat = model(X)
            y_bce = y.type(torch.float).reshape(-1, 1)
            #loss = F1_criterion(yhat, y) * 100 + BCE_criterion(yhat, y_bce)
            #loss = F1_criterion(yhat, y)
            loss = BCE_criterion(yhat, y_bce)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()
            train_size += X.shape[0]
        print("Epoch %d:, train_loss: %f" % (iteration, train_loss/train_size))

        if iteration % 5 == 0:
            val_loss = 0.0
            val_size = 0
            for i, (X, y) in enumerate(test_loader):
                model.eval()
                yhat = model(X)
                y_bce = y.type(torch.float).reshape(-1, 1)
                #loss = F1_criterion(yhat, y) * 100 + BCE_criterion(yhat, y_bce)
                #loss = F1_criterion(yhat, y)
                loss = BCE_criterion(yhat, y_bce)
                val_loss += loss.item()
                val_size += X.shape[0]
            print("Epoch %d:, val_loss: %f" % (iteration, val_loss/val_size))

        
        torch.save(model.state_dict(), 'models/' + args.model_name + '.pt')
    return model, vocab


def generate_resultfile_v0(model, test_fpath, results_fpath, model_name, vocab):
    model.eval()
    test_df = pd.read_csv(test_fpath, sep='\t')
    with open(results_fpath, "w") as results_file:
        results_file.write("topic\ttweet_id\tclass_label\trun_id\n")
        for i, line in test_df.iterrows():
            vectorized = vocab(tokenizer(line['tweet_text']))
            vectorized = vectorized + ([0] * (93 - len(vectorized)))
            label = model(torch.tensor(vectorized, dtype = torch.float))
            label = label >= 0.5
            results_file.write("{}\t{}\t{}\t{}\n".format(line['topic'], line['tweet_id'], int(label.item()), model_name))
    return


def generate_resultfile_glove(model, test_fpath, results_fpath, model_name, vocab):
    model.eval()
    test_df = pd.read_csv(test_fpath, sep='\t')
    with open(results_fpath, "w") as results_file:
        results_file.write("topic\ttweet_id\tclass_label\trun_id\n")
        for i, line in test_df.iterrows():
            vectorized = glove_sentence_vectorize(line['tweet_text'], vocab)
            label = model(torch.tensor(vectorized, dtype = torch.float))
            label = label > 0.5
            results_file.write("{}\t{}\t{}\t{}\n".format(line['topic'], line['tweet_id'], int(label.item()), model_name))
    return


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
    
    model, vocab = train(cfg)

    '''
    test_fpath = os.path.join(cfg.data_dir, 'CT22_english_1A_checkworthy_dev_test.tsv')
    results_fpath = 'baselines/data/subtask_checkworthy_english_' + cfg.model_name
    generate_resultfile_glove(model, test_fpath, results_fpath, cfg.model_name, vocab)

    test_fpath = os.path.join(cfg.data_dir, 'CT22_english_1A_checkworthy_dev_test.tsv')
    results_fpath = 'baselines/data/subtask_checkworthy_english_' + cfg.model_name
    if check_format(results_fpath):
        acc, precision, recall, f1 = evaluate(test_fpath, results_fpath)
        print("Model_name:", cfg.model_name, "Acc:", acc, "F1:", f1)
    '''

    ######################################  Print baseline result ################################################
    '''
    results_fpath = 'baselines/data/subtask_checkworthy_majority_baseline_english_CT22_english_1A_checkworthy_dev_test.tsv'
    if check_format(results_fpath):
        acc, precision, recall, f1 = evaluate(test_fpath, results_fpath)
        print("Model_name: majority Acc:", acc, "F1:", f1)

    results_fpath = 'baselines/data/subtask_checkworthy_ngram_baseline_english_CT22_english_1A_checkworthy_dev_test.tsv'
    if check_format(results_fpath):
        acc, precision, recall, f1 = evaluate(test_fpath, results_fpath)
        print("Model_name: ngram Acc:", acc, "F1:", f1)

    results_fpath = 'baselines/data/subtask_checkworthy_random_baseline_english_CT22_english_1A_checkworthy_dev_test.tsv'
    if check_format(results_fpath):
        acc, precision, recall, f1 = evaluate(test_fpath, results_fpath)
        print("Model_name: random Acc:", acc, "F1:", f1)
    '''
    