import socket
import os
import logging
from logging.handlers import RotatingFileHandler
import json
import protocol
from random import randrange
import random

import sys

from PhantomGame import PhantomGame as Game
from NNet import NNetWrapper as NNet
from MCTS import MCTS
import numpy as np

host = "localhost"
port = 12000
# HEADERSIZE = 10

"""
set up fantom logging
"""
fantom_logger = logging.getLogger()
fantom_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s :: %(levelname)s :: %(message)s", "%H:%M:%S")
# file
if os.path.exists("./logs/fantom.log"):
    os.remove("./logs/fantom.log")
file_handler = RotatingFileHandler('./logs/fantom.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
fantom_logger.addHandler(file_handler)
# stream
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
fantom_logger.addHandler(stream_handler)


class dotdict(dict):
    def __getattr__(self, name):
        return self[name]

class Player():

    def __init__(self):

        self.end = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.g = Game()
        self.n1 = NNet(self.g)
        #self.n1.load_checkpoint('../pretrained_models/phantom/keras/','6x6 checkpoint_145.pth.tar')
        self.args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
        self.mcts1 = MCTS(self.g, self.n1, self.args1)
        self.n1p = lambda x: np.argmax(self.mcts1.getActionProb(x, temp=0)).item()

    def connect(self):
        self.socket.connect((host, port))

    def reset(self):
        self.socket.close()

    def answer(self, question):
        response_index = self.n1p(question)
        return response_index

    def handle_json(self, data):
        data = json.loads(data)
        response = self.answer(data)
        # send back to server
        bytes_data = json.dumps(response).encode("utf-8")
        protocol.send_json(self.socket, bytes_data)

    def run(self):

        self.connect()

        while self.end is not True:
            received_message = protocol.receive_json(self.socket)
            if received_message:
                self.handle_json(received_message)
            else:
                print("no message, finished learning")
                self.end = True


p = Player()

p.run()
