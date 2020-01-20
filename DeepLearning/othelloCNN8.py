import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import torchvision

import numpy as np
import pandas as pd

import time
import math
import WThorParser


class OthelloCNN8(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(in_channels=2, out_channels=64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
        self.conv5 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1)
        self.conv6 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1)
        self.conv7 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1)
        self.conv8 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1)

        self.fc1 = nn.Linear(in_features=256*8*8, out_features=128)
        self.out = nn.Linear(in_features=128, out_features=60)

    def forward(self, t):
        # convolutional layers
        t = self.conv1(t)
        t = F.relu(t)

        t = self.conv2(t)
        t = F.relu(t)

        t = self.conv3(t)
        t = F.relu(t)

        t = self.conv4(t)
        t = F.relu(t)

        t = self.conv5(t)
        t = F.relu(t)

        t = self.conv6(t)
        t = F.relu(t)

        t = self.conv7(t)
        t = F.relu(t)

        t = self.conv8(t)
        t = F.relu(t)

        # fully connected layers

        t = t.reshape(-1, 128*8*8)
        t = self.fc1(t)
        t = F.relu(t)

        t = self.out(t)
        t = F.relu(t)
        # softmaxer = nn.Softmax(dim=1)
        
        # t = softmaxer(t)
        # print(t)

        return t


def getNumberCorrectGuesses(predictions, moves):
    return predictions.argmax(dim=1).eq(moves).sum().item()


if __name__=='__main__':

    print('Initilaising variables...')

    ## hyperparamters

    lr = 0.01
    sgd_momentum = 0.95
    batch_size = 100
    num_epochs = 25

    ## set up devices, NN and optimiser

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network = OthelloCNN8().to(device)
    optimiser = optim.SGD(network.parameters(), lr=lr, momentum=sgd_momentum)

    ## prepare data

    boards_data, moves = WThorParser.loadTrainingData()


    train_data = []
    test_data = []

    test_percentile = 0.95

    number_boards_to_train = math.floor(len(boards_data)*test_percentile)

    for i in range(number_boards_to_train):
        train_data.append([boards_data[i], moves[i]])

    for i in range(number_boards_to_train, len(boards_data)):
        test_data.append([boards_data[i], moves[i]])


    training_loader = torch.utils.data.DataLoader(
        train_data,
        batch_size=batch_size,
        shuffle=True
    )

    testing_loader = torch.utils.data.DataLoader(
        test_data,
        batch_size=batch_size,
        shuffle=True
    )


    ## training

    print('Length of training data:', len(train_data))

    for epoch in range(num_epochs):
        total_loss = 0
        total_correct = 0
        start_time = time.time()

        for batch in training_loader:
            boards = batch[0].to(device)
            moves = batch[1].to(device)

            predictions = network(boards)

            loss = F.cross_entropy(predictions, moves)

            optimiser.zero_grad()
            loss.backward()
            optimiser.step()

            total_loss += loss.item()
            total_correct += getNumberCorrectGuesses(predictions, moves)

        finish_time = time.time()
        total_time = round(finish_time - start_time, 5)

        print(
            'Epoch:', epoch, '|',
            'Percentage correct:', round(total_correct/len(train_data) * 100, 4), '%', '|',
            'Total loss:', total_loss, '|',
            'Time taken:', total_time, '|'
        )

    ## testing

    with torch.no_grad():
        total_correct = 0
        for batch in testing_loader:
            boards = batch[0].to(device)
            moves = batch[1].to(device)

            predictions = network(boards)

            total_correct += getNumberCorrectGuesses(predictions, moves)
        percentage_correct = round(total_correct / len(test_data) * 100, 2)
        print(
            'Testing results:\n',
            'Number of correctly guessed moves:', total_correct, '\n',
            'Percentage correct:', percentage_correct
        )

    ## saving model 
    print('Saving model...')
    torch.save(network.state_dict(), './DeepLearning/models/' + str(int(percentage_correct)))