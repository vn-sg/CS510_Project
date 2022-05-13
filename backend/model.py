import torch
from torch import nn


class TwitterDetector(nn.Module):
    def __init__(self, args):
        super(TwitterDetector, self).__init__()
        self.args = args
        self.input_channel = args.input_dim
        self.model = self.build_model(args.model_type)

    def forward(self, X):
        return self.model(X)
        
    def build_model(self, model_type):
        if model_type == 'linear':
            return LinearModel(self.args, self.input_channel)


class LinearModel(nn.Module):
    def __init__(self, args, input_channel, output_channel = 1):
        super().__init__()
        self.layer_num = args.layer_num
        self.hidden_states = args.hidden_states
        self.init_layer = nn.Linear(input_channel, self.hidden_states)
        self.layer = nn.Linear(self.hidden_states, self.hidden_states)
        self.output_layer = nn.Linear(self.hidden_states, output_channel)
        self.sigmoid = nn.Sigmoid()
        self.relu = nn.ReLU()

    def forward(self, X):
        X = self.init_layer(X)
        for _ in range(self.layer_num - 2):
            X = self.layer(X)
        X = self.output_layer(X)
        X = self.sigmoid(X)
        return X
        