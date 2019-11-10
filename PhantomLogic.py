

from threading import Thread, Lock

import time
import socket
import json
import protocol
import numpy as np

POSITION_CARLOTTA_STRING = "position_carlotta"
EXIT_STRING = "exit"
NUM_TOUR_STRING = "num_tour"
SHADOW_STRING = "shadow"
BLOCKED_STRING = "blocked"

color_order = ['blue', 'red', 'pink', 'black', 'white', 'purple', 'brown', 'grey']
msg_queue = []
answ_queue = []
has_ended = 0
msq_q_lock = Lock()
answ_q_lock = Lock()
has_ended_lock = Lock()

class ThreadedSocket(Thread):

    def __init__(self, player_id, msg_queue):
        Thread.__init__(self)
        self.id = player_id
        self.queue = msg_queue
        print("new socket: ", player_id)
        self.end = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        self.socket.connect(("localhost", 12000))
        while self.end is not True:
            received_message = protocol.receive_json(self.socket)
            if received_message:
                self.handle_json(received_message)
            else:
                print("no message, finished learning")
                self.end = True
                return
            self.send_answer()

    def send_answer(self):
        while 42:    
            with answ_q_lock:     
                print(self.id, " waiting for: ", len(answ_queue), answ_queue[0]['player_id'] if len(answ_queue) else '')
                if len(answ_queue) != 0 and answ_queue[0]['player_id'] == self.id:
                    bytes_data = json.dumps(answ_queue[0]['data']).encode("utf-8")
                    answ_queue.pop(0)
                    print('sending')
                    protocol.send_json(self.socket, bytes_data)
                    return
            time.sleep(1)

    def handle_json(self, data):
        global has_ended_lock
        global msg_q_lock
        global msg_queue
        data = json.loads(data)
        print('received data ', data, self.id)
        if 'winner' in data.keys():
            with has_ended_lock:
                has_ended = self.id
        with msq_q_lock:
            msg_queue += [{"data": data, "player_id": self.id}]
        return

    def send_json(self, response):
        bytes_data = json.dumps(response).encode("utf-8")
        protocol.send_json(self.socket, bytes_data)
        return


class Board:

    def __init__(self):
        #self.clients = [ThreadedSocket(-1, msg_queue), ThreadedSocket(1, msg_queue)]
        #self.clients[0].start()
        #self.clients[1].start()
        self.next_player = 0
        self.current_question = ""
        self.action_size = 10
        self.valid_actions = 0
        self.pieces = []

    def set_answer(self, answ_index, player_id):
        global answ_queue
        print('a')
        with answ_q_lock:
            answ_queue += [{'data': answ_index, 'player_id': 1 if player_id == 1 else -1 }]
            print(answ_queue)        
        print('b')
        return

    def has_game_ended(self):
        with has_ended_lock:
            ended = has_ended
        return ended

    # Board state:
    # [
    # 0 - 30: ord() of each char of question, filled with 0s
    # 31: position_carlotta
    # 32: exit
    # 33: num_tour
    # 34: shadow
    # 35: position_carlotta
    # 36 - 37: blocked
    # 38 - 40: [suspect?, position, power?]: color_order[0]
    # 41 - 43: [suspect?, position, power?]: color_order[1]
    # 44 - 46: [suspect?, position, power?]: color_order[2]
    # 47 - 49: [suspect?, position, power?]: color_order[3]
    # 50 - 52: [suspect?, position, power?]: color_order[4]
    # 53 - 55: [suspect?, position, power?]: color_order[5]
    # 56 - 58: [suspect?, position, power?]: color_order[6]
    # 59 - 61: [suspect?, position, power?]: color_order[7]
    # 62: data_color[0] index if color else -1
    # 63: data_color[1] index if color else -1
    # 64: data_color[2] index if color else -1
    # 65: data_color[3] index if color else -1
    # 66: data_color[4] index if color else -1
    # 67: data_color[5] index if color else -1
    # 68: data_color[6] index if color else -1
    # 69: data_color[7] index if color else -1
    # 70: data_choice[0] int if data else -1
    # 71: data_choice[1] int if data else -1
    # 72: data_choice[2] int if data else -1
    # 73: data_choice[3] int if data else -1
    # 74: data_choice[4] int if data else -1
    # 75: data_choice[5] int if data else -1
    # 76: data_choice[6] int if data else -1
    # 77: data_choice[7] int if data else -1
    # ]

    # Actions: [0 - 7]
    # Valid Actions: len(data)

    def _get_char_array(self, state):
        chars = list(state["characters"])
        cpt = 0
        ret = []
        for color in color_order:
            ret += [[int(x["suspect"]), x["position"], int(x["power"])] for x in chars if x["color"] == color]
        ret = np.append([], ret)
        print(ret.astype(int).tolist())
        return ret.astype(int).tolist()
            
    def chunk_it(self, seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0

        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg

        return out  
    
    def _update_game_state(self, data):
        self.current_question = data["question type"]
        state = data["game state"]
        question_data = data["data"]
        print(len(question_data), type(question_data[0]) is int)
        print([-1] if len(question_data) <= 0 or type(question_data[0]) is not int else [question_data[0]])
        print([-1] if len(question_data) <= 7 or type(question_data[7]) is not int else [question_data[7]])
        pieces = [ord(x) for x in list(self.current_question)] + [-1] * (30 - len(self.current_question)) \
            + [state["position_carlotta"], state["exit"], state["num_tour"], state["shadow"]] \
            + state["blocked"] \
            + self._get_char_array(state) \
            + ([-1] if len(question_data) <= 0 or type(question_data[0]) is int else [color_order.index(question_data[0]['color'])]) \
            + ([-1] if len(question_data) <= 1 or type(question_data[1]) is int else [color_order.index(question_data[1] ['color'])]) \
            + ([-1] if len(question_data) <= 2 or type(question_data[2]) is int else [color_order.index(question_data[2]['color'])]) \
            + ([-1] if len(question_data) <= 3 or type(question_data[3]) is int else [color_order.index(question_data[3]['color'])]) \
            + ([-1] if len(question_data) <= 4 or type(question_data[4]) is int else [color_order.index(question_data[4]['color'])]) \
            + ([-1] if len(question_data) <= 5 or type(question_data[5]) is int else [color_order.index(question_data[5]['color'])]) \
            + ([-1] if len(question_data) <= 6 or type(question_data[6]) is int else [color_order.index(question_data[6]['color'])]) \
            + ([-1] if len(question_data) <= 7 or type(question_data[7]) is int else [color_order.index(question_data[7]['color'])]) \
            + ([-1] if len(question_data) <= 0 or type(question_data[0]) is not int else [question_data[0]]) \
            + ([-1] if len(question_data) <= 1 or type(question_data[1]) is not int else [question_data[1]]) \
            + ([-1] if len(question_data) <= 2 or type(question_data[2]) is not int else [question_data[2]]) \
            + ([-1] if len(question_data) <= 3 or type(question_data[3]) is not int else [question_data[3]]) \
            + ([-1] if len(question_data) <= 4 or type(question_data[4]) is not int else [question_data[4]]) \
            + ([-1] if len(question_data) <= 5 or type(question_data[5]) is not int else [question_data[5]]) \
            + ([-1] if len(question_data) <= 6 or type(question_data[6]) is not int else [question_data[6]]) \
            + ([-1] if len(question_data) <= 7 or type(question_data[7]) is not int else [question_data[7]]) \
            + ([-1] if len(question_data) <= 8 or type(question_data[8]) is not int else [question_data[8]]) \
            + ([-1] if len(question_data) <= 9 or type(question_data[9]) is not int else [question_data[9]]) \
            + ([-1] if 'fantom' not in state.keys() else [color_order.index(state['fantom'])])
        pieces += [0] * (81 - len(pieces))
        
        self.pieces = np.copy(self.chunk_it(pieces, 9))
        print("pieces: ", self.pieces)
        self.valid_actions = len(question_data)

    def get_next_question(self):
        ret = {}
        while ret == {}:
            with msq_q_lock:
                if len(msg_queue) != 0:
                    ret = msg_queue.pop(0)
        print(ret)
        self._update_game_state(ret["data"])
        self.next_player = ret["player_id"]
        return self.pieces, ret["player_id"]
