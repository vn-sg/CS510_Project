import torch
import torchtext
import os
import re
import gensim.downloader
import numpy as np
from torchtext.data import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from torch.utils.data import DataLoader
from torchtext.data.functional import to_map_style_dataset

MAX_LENGTH = 0

class vectorize_batch:
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, batch):
      X, Y = list(zip(*batch))
      X = [self.vocab(tokenizer(sample)) for sample in X]
      X = [sample + ([0] * (MAX_LENGTH - len(sample))) for sample in X]
      Y = [int(sample) for sample in Y]
      return torch.tensor(X, dtype = torch.float), torch.tensor(Y)

def glove_sentence_vectorize(sentence, vocab):
  words = tokenizer(sentence)
  sum = 0
  for word in words:
    if word in vocab: sum += vocab[word]
  return sum / len(words)

class glove_batch:
  def __init__(self, vocab):
    self.vocab = vocab

  def __call__(self, batch):
    X, Y = list(zip(*batch))
    X = np.array([glove_sentence_vectorize(sample, self.vocab) for sample in X])
    Y = [int(sample) for sample in Y]
    return torch.tensor(X, dtype = torch.float), torch.tensor(Y)

def tokenizer(inp_str): ## This method is one way of creating tokenizer that looks for word tokens
    return re.findall(r"\w+", inp_str)

def build_vocab(datasets):
  global MAX_LENGTH
  for dataset in datasets:
    for text, _ in dataset:
      tokens = tokenizer(text)
      MAX_LENGTH = max(MAX_LENGTH, len(tokens))
      yield tokens

def read_raw_data(filename):
  data = []
  with open(filename) as f:
    first = True
    for line in f:
      if first: 
        first = False
        continue
      else:
        topic, tweet_id, tweet_url, tweet_text, class_label = line.strip().lower().split('\t')
        data.append((tweet_text, class_label))
  return data

def get_dataset_v0(args):
    raw_train = read_raw_data(os.path.join(args.data_dir, 'CT22_english_1A_checkworthy_train.tsv'))
    raw_test = read_raw_data(os.path.join(args.data_dir, 'CT22_english_1A_checkworthy_dev.tsv'))
    vocab = build_vocab_from_iterator(build_vocab([raw_train, raw_test]), specials=["<UNK>"])
    vocab.set_default_index(vocab["<UNK>"])
    train_dataset, test_dataset = to_map_style_dataset(raw_train), to_map_style_dataset(raw_test)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, collate_fn=vectorize_batch(vocab), shuffle = True)
    test_loader  = DataLoader(test_dataset, batch_size=args.batch_size, collate_fn=vectorize_batch(vocab), shuffle = False)
    return train_loader, test_loader, vocab

def get_dataset_using_glove_50(train_path, test_path):
    # data_dir = 'data/subtasks-english/CT22_english_1A_checkworthy'
    raw_train = read_raw_data(train_path)
    raw_test = read_raw_data(test_path)
    vocab = gensim.downloader.load('glove-twitter-50')
    tokenizer = get_tokenizer("basic_english") ## We'll use tokenizer available from PyTorch
    train_dataset, test_dataset = to_map_style_dataset(raw_train), to_map_style_dataset(raw_test)
    train_loader = DataLoader(train_dataset, batch_size=len(train_dataset), collate_fn=glove_batch(vocab))
    test_loader  = DataLoader(test_dataset, batch_size=len(test_dataset), collate_fn=glove_batch(vocab))
    return train_loader, test_loader, vocab


def get_dataset_using_glove_25(train_path, test_path):
    # data_dir = 'data/subtasks-english/CT22_english_1A_checkworthy'
    raw_train = read_raw_data(train_path)
    raw_test = read_raw_data(test_path)
    vocab = gensim.downloader.load('glove-twitter-25')
    tokenizer = get_tokenizer("basic_english") ## We'll use tokenizer available from PyTorch
    train_dataset, test_dataset = to_map_style_dataset(raw_train), to_map_style_dataset(raw_test)
    train_loader = DataLoader(train_dataset, batch_size=len(train_dataset), collate_fn=glove_batch(vocab))
    test_loader  = DataLoader(test_dataset, batch_size=len(test_dataset), collate_fn=glove_batch(vocab))
    return train_loader, test_loader, vocab

if __name__ == '__main__':
    data_dir = 'data/subtasks-english/CT22_english_1A_checkworthy'
    raw_train = read_raw_data(os.path.join(data_dir, 'CT22_english_1A_checkworthy_train.tsv'))
    raw_test = read_raw_data(os.path.join(data_dir, 'CT22_english_1A_checkworthy_dev_test.tsv'))
    tokenizer = get_tokenizer("basic_english") ## We'll use tokenizer available from PyTorch
    MAX_LENGTH = 0
    vocab = build_vocab_from_iterator(build_vocab([raw_train, raw_test]), specials=["<UNK>"])
    vocab.set_default_index(vocab["<UNK>"])
    train_dataset, test_dataset = to_map_style_dataset(raw_train), to_map_style_dataset(raw_test)
    train_loader = DataLoader(train_dataset, batch_size=len(train_dataset), collate_fn=vectorize_batch(vocab))
    test_loader  = DataLoader(test_dataset, batch_size=len(test_dataset), collate_fn=vectorize_batch(vocab))
    for X, Y in test_loader:
        print(X, Y)
