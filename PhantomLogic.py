import Game from PhantomServer
import Player from PhantomPlayer

from threading import Thread, RLock

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
msq_q_lock = RLock()
answ_q_lock = RLock()
has_ended_lock = RLock()

class ThreadedSocket(Thread, player_id):

    def __init__(self):
        Thread.__init__(self)
        self.id = player_id
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

    def send_answer():
        while 42:
            with answ_queue:
                if len(answ_queue) != 0 and answ_queue[0]['dest_id'] == self.id:
                    bytes_data = json.dumps(answ_queue[0]['data']).encode("utf-8")
                    answ_queue.pop(0)
                    protocol.send_json(self.socket, bytes_data)
                    return

    def handle_json(self, data):
        data = json.loads(data)
        if 'winner' in data.keys():
            with has_ended_lock:
                has_ended = self.id
        with msq_q_lock:
            msg_queue += {data: data, player_id: self.id}

    def send_json(self, response):
        bytes_data = json.dumps(response).encode("utf-8")
        protocol.send_json(self.socket, bytes_data)


class Board:

    def __init__(self, n)bv   -> None:
        self.clients = [ThreadedSocket(1), ThreadedSocket(-1)]
        self.clients[0].start()
        self.clients[1].start()
        self.current_question = ""
        self.action_size = len(color_order)
        self.valid_actions = 0
        self.pieces = self.update_board()
        self.question_to_board = lambda question: return [ord(x) for x in list(question)]

    def set_answer(self, answ_index, player_id):
        with answ_q_lock:
            answ_queue.append({'data': answ_index, 'id': 0 if player_id == 1 else 1})

    def has_game_ended():
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

    def _update_game_state(self, data):

        self.current_question = data["question_type"]
        state = data["game_state"]
        question_data = data["data"]
        pieces = [ord(x) for x in self.current_question] + [-1] * (30 - len(self.current_question))]
            + [state. position_carlotta, state.exit, state.num_tour, state.shadow]
            + state.blocked
            + [int(state.characters['blue']).suspect, state.characters['blue'].position, int(state.characters['blue'].power)]
            + [int(state.characters['red']).suspect, state.characters['red'].position, int(state.characters['red'].power)]
            + [int(state.characters['pink']).suspect, state.characters['pink'].position, int(state.characters['pink'].power)]
            + [int(state.characters['black']).suspect, state.characters['black'].position, int(state.characters['black'].power)]
            + [int(state.characters['white']).suspect, state.characters['white'].position, int(state.characters['white'].power)]
            + [int(state.characters['purple']).suspect, state.characters['purple'].position, int(state.characters['purple'].power)]
            + [int(state.characters['brown']).suspect, state.characters['brown'].position, int(state.characters['brown'].power)]
            + [int(state.characters['grey']).suspect, state.characters['grey'].position, int(state.characters['grey'].power)]
            + [-1] if len(question_data) <= 0 or type(question_data[0]) == 'int' else [color_order.index(data[0]['color'])]
            + [-1] if len(question_data) <= 1 or type(question_data[1]) == 'int' else [color_order.index(question_data[1]['color'])]
            + [-1] if len(question_data) <= 2 or type(question_data[2]) == 'int' else [color_order.index(question_data[2]['color'])]
            + [-1] if len(question_data) <= 3 or type(question_data[3]) == 'int' else [color_order.index(question_data[3]['color'])]
            + [-1] if len(question_data) <= 4 or type(question_data[4]) == 'int' else [color_order.index(question_data[4]['color'])]
            + [-1] if len(question_data) <= 5 or type(question_data[5]) == 'int' else [color_order.index(question_data[5]['color'])]
            + [-1] if len(question_data) <= 6 or type(question_data[6]) == 'int' else [color_order.index(question_data[6]['color'])]
            + [-1] if len(question_data) <= 7 or type(question_data[7]) == 'int' else [color_order.index(question_data[7]['color'])]
            + [-1] if len(question_data) <= 0 or type(question_data[0]) != 'int' else [question_data[0]]
            + [-1] if len(question_data) <= 1 or type(question_data[1]) != 'int' else [question_data[1]]
            + [-1] if len(question_data) <= 2 or type(question_data[2]) != 'int' else [question_data[2]]
            + [-1] if len(question_data) <= 3 or type(question_data[3]) != 'int' else [question_data[3]]
            + [-1] if len(question_data) <= 4 or type(question_data[4]) != 'int' else [question_data[4]]
            + [-1] if len(question_data) <= 5 or type(question_data[5]) != 'int' else [question_data[5]]
            + [-1] if len(question_data) <= 6 or type(question_data[6]) != 'int' else [question_data[6]]
            + [-1] if len(question_data) <= 7 or type(question_data[7]) != 'int' else [question_data[7]]
            + [-1] if 'fantom' not in state.keys() else color_order.index(state['fantom'])
        self.pieces = np.array(pieces)
        self.valid_actions = len(question_data)

    def get_next_question(self):
        ret = {}
        while ret == {}:
            with msq_q_lock:
                if len(msg_queue) != 0:
                    ret = msg_queue.pop(0)
        _update_game_state(ret.data)
        return ret.player_id, self.pieces


    def _add_pieces_to_board(pieces):
        find_color = lambda (array, color): for i, v in enumerate(pieces)
        sorted_pieces = [pieces[index] for index in range(len(sorted_pieces)) if pieces[index].color == color[index]]
        board_with_pieces = [[int(elem.suspect), elem.position, int(elem.power)]]
        return board_with_pieces