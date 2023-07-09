import random
from game import Board
import globals as globals

class Bot13521144(object):
    """
    Bot player
    """

    def __init__(self):
        self.player = None

        self.NIM = "13521144"

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board, return_var):

        try:
            location = self.get_input(board)
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1

        while move == -1 or move not in board.availables:
            if globals.stop_threads:
                return
            try:
                location = self.get_input(board)
                if isinstance(location, str):  # for python3
                    location = [int(n, 10) for n in location.split(",")]
                move = board.location_to_move(location)
            except Exception as e:
                move = -1
        return_var.append(move) 

    def __str__(self):
        return "{} a.k.a Player {}".format(self.NIM,self.player)
    
    def value_to_coordinate(self, value : int) -> tuple:
        x = value // 8
        y = value % 8
        return x, y

    def is_diagonal_leftright(self, val1, val2, board): # \ diagonal
        x1, y1 = self.value_to_coordinate(val1)
        x2, y2 = self.value_to_coordinate(val2)
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        if y2 != y1:
            m = (x2 - x1) / (y2 - y1)
        else:
            m = -1 if x2 == x1 else 2
        return m == -1 and board.states[val1] == board.states[val2]
    
    def is_diagonal_rightleft(self, val1, val2, board): # / diagonal
        x1, y1 = self.value_to_coordinate(val1)
        x2, y2 = self.value_to_coordinate(val2)
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        if y2 != y1:
            m = (x2 - x1) / (y2 - y1)
        else:
            m = 1 if x2 == x1 else 2
        return m == 1 and board.states[val1] == board.states[val2]
    
    def is_horizontal(self, val1, val2, board):
        # print("is horizontal")
        x1, y1 = self.value_to_coordinate(val1)
        x2, y2 = self.value_to_coordinate(val2)
        return x1 == x2 and board.states[val1] == board.states[val2]
    
    def is_vertical(self, val1, val2, board):
        # print("is vertical")
        x1, y1 = self.value_to_coordinate(val1)
        x2, y2 = self.value_to_coordinate(val2)
        return y1 == y2 and board.states[val1] == board.states[val2]
    
    def get_adjacents(self, board, value):
        diag_leftright = []
        diag_rightleft = []
        hor = []
        ver = []
        for x in board.states:
            if board.states[x] == 0:
                continue
            value_val = board.states[value]
            x_val = board.states[x]
            if x_val == value_val:
                if self.is_diagonal_leftright(x, value, board):
                    diag_leftright.append(x)
                if self.is_diagonal_rightleft(x, value, board):
                    diag_rightleft.append(x)
                if self.is_horizontal(x, value, board):
                    hor.append(x)
                if self.is_vertical(x, value, board):
                    ver.append(x)
        return diag_leftright, diag_rightleft, hor, ver
    
    def not_blocked(self, board, adj, val, type):
        # sort adj list
        adj.sort()
        # print("adj: ", adj)
        start = adj[0]
        end = adj[-1]
        # print("start: ", start)
        # print("end: ", end)
        a = None
        b = None
        if type == 0: # diagonal \
            start_x, start_y = self.value_to_coordinate(start)
            end_x, end_y = self.value_to_coordinate(end)
            if start_x != 0 and start_y != 7:
                if start-7 not in board.states or board.states[start-7] == 0:
                    a = start-7
            if end_x != 7 and end_y != 0:
                if end+7 not in board.states or board.states[end+7] == 0:
                    b = end+7
        elif type == 3: # diagonal /
            start_x, start_y = self.value_to_coordinate(start)
            end_x, end_y = self.value_to_coordinate(end)
            if start_y != 0 and start_x != 0:
                if start-9 not in board.states or board.states[start-9] == 0:
                    a = start-9
            if end_y != 7 and end_x != 7:
                if end+9 not in board.states or board.states[end+9] == 0:
                    b = end+9
        elif type == 1:
            # check left and right of the horizontal
            _, start_y = self.value_to_coordinate(start)
            _, end_y = self.value_to_coordinate(end)
            if start_y != 0:
                if start-1 not in board.states or board.states[start-1] == 0:
                    a = start-1
            if end_y != 7:
                if end+1 not in board.states or board.states[end+1] == 0:
                    b = end+1
        else:
            # check up and down of the vertical
            start_x, _ = self.value_to_coordinate(start)
            end_x, _ = self.value_to_coordinate(end)
            if start_x != 0:
                if start-8 not in board.states:
                    a = start-8
            if end_x != 7:
                if end+8 not in board.states:
                    b = end+8
        # print("adj: ", adj)
        # print("type: ", type)
        # print("a: ", a)
        # print("b: ", b)
        return a, b
    
    def longest_unblocked(self, board, player):
        enemy = 1 if self.player == 2 else 2
        val = self.player if player else enemy
        # print("val: ", val)
        # print("enemy: ", enemy)
        max_len = 0
        adj = []
        type = -1 # 0 = diag, 1 = hor, 2 = ver
        a = None
        b = None
        for x in board.states:
            x_val = board.states[x]
            if x_val == val:
                diag_leftright, diag_rightleft, hor, ver = self.get_adjacents(board, x)
                # print("diag_leftright: ", diag_leftright)
                # print("diag_rightleft: ", diag_rightleft)
                # print("hor: ", hor)
                # print("ver: ", ver)
                a_diaglr, b_diaglr = self.not_blocked(board, diag_leftright, val, 0)
                a_diagrl, b_diagrl = self.not_blocked(board, diag_rightleft, val, 3)
                a_hor, b_hor = self.not_blocked(board, hor, val, 1)
                a_ver, b_ver = self.not_blocked(board, ver, val, 2)

                len_diaglr = len(diag_leftright)
                len_diagrl = len(diag_rightleft)
                len_hor = len(hor)
                len_ver = len(ver)

                # print("diag_lr: ", diag_leftright)
                # print("diag_rl: ", diag_rightleft)
                # print("hor: ", hor)
                # print("ver: ", ver)

                if a_diaglr is not None:
                    len_diaglr += 1
                if b_diaglr is not None:
                    len_diaglr += 1
                
                if a_diagrl is not None:
                    len_diagrl += 1
                if b_diagrl is not None:
                    len_diagrl += 1
                
                if a_hor is not None:
                    len_hor += 1
                if b_hor is not None:
                    len_hor += 1
                
                if a_ver is not None:
                    len_ver += 1
                if b_ver is not None:
                    len_ver += 1
                
                if len_diaglr > max_len and (a_diaglr is not None or b_diaglr is not None):
                    max_len = len_diaglr
                    adj = diag_leftright
                    type = 0
                    a = a_diaglr
                    b = b_diaglr
                if len_diagrl > max_len and (a_diagrl is not None or b_diagrl is not None):
                    max_len = len_diagrl
                    adj = diag_rightleft
                    type = 3
                    a = a_diagrl
                    b = b_diagrl
                if len_hor > max_len and (a_hor is not None or b_hor is not None):
                    max_len = len_hor
                    adj = hor
                    type = 1
                    a = a_hor
                    b = b_hor
                if len_ver > max_len and (a_ver is not None or b_ver is not None):
                    max_len = len_ver
                    adj = ver
                    type = 2
                    a = a_ver
                    b = b_ver
        # print("max_len: ", max_len)
        # print("adj: ", adj)
        # print("type: ", type)
        # print("a: ", a)
        # print("b: ", b)
        return adj, a, b, type

    def get_input(self, board : Board) -> str:
        """
            Parameter board merepresentasikan papan permainan. Objek board memiliki beberapa
            atribut penting yang dapat menjadi acuan strategi.
            - board.height : int (x) -> panjang papan
            - board.width : int (y) -> lebar papan
            Koordinat 0,0 terletak pada kiri bawah

            [x,0] [x,1] [x,2] . . . [x,y]                               
            . . . . . . . . . . . . . . .  namun perlu diketahui        Contoh 4x4: 
            . . . . . . . . . . . . . . .  bahwa secara internal        11 12 13 14 15
            . . . . . . . . . . . . . . .  sel-sel disimpan dengan  =>  10 11 12 13 14
            [2,0] [2,1] [2,2] . . . [2,y]  barisan interger dimana      5  6  7  8  9
            [1,0] [1,1] [1,2] . . . [1,y]  kiri bawah adalah nol        0  1  2  3  4
            [0,0] [0,1] [0,2] . . . [0,y]          
                                 
            - board.states : dict -> Kondisi papan. 
            Key dari states adalah integer sel (0,1,..., x*y)
            Value adalah integer 1 atau 2:
            -> 1 artinya sudah diisi player 1
            -> 2 artinya sudah diisi player 2

            TODO: Tentukan x,y secara greedy. Kembalian adalah sebuah string "x,y"
        """
        temp = list(board.states.keys())
        if len(temp) > 1:
            temp = None
        else:
            temp = temp[0]
        if board.states == {} or temp == 36:
            return "3,3" # kalau kosong, ambil tengah
        if temp == 27:
            return "4,4"
        if temp == 35:
            return "3,4"
        if temp == 28:
            return "4,3"

        enemy = 1 if self.player == 2 else 2
        
        # check for the longest enemy unblocked
        enemy_adj, enemy_a, enemy_b, enemy_type = self.longest_unblocked(board, False)
        # print("enemy_adj: ", enemy_adj)
        # print("enemy_a: ", enemy_a)
        # print("enemy_b: ", enemy_b)
        # print("enemy_type: ", enemy_type)

        # block the enemy if it's 2 or more to prevent unblocked 3 in a row
        # multiple unblocked 3 in a row = lose
        if len(enemy_adj) >= 3:
            # check for a and b which have more enemy pieces adjacent
            adj_enemy_a_0 = []
            adj_enemy_a_1 = []
            adj_enemy_a_2 = []
            adj_enemy_a_3 = []
            adj_enemy_b_0 = []
            adj_enemy_b_1 = []
            adj_enemy_b_2 = []
            adj_enemy_b_3 = []

            if enemy_a is not None:
                board.states[enemy_a] = enemy
                adj_enemy_a_0, adj_enemy_a_1, adj_enemy_a_2, adj_enemy_a_3 = self.get_adjacents(board, enemy_a)
                board.states[enemy_a] = 0

            if enemy_b is not None:
                board.states[enemy_b] = enemy
                adj_enemy_b_0, adj_enemy_b_1, adj_enemy_b_2, adj_enemy_b_3 = self.get_adjacents(board, enemy_b)
                board.states[enemy_b] = 0
            
            adj_enemy_a = adj_enemy_a_1 + adj_enemy_a_2 + adj_enemy_a_3 + adj_enemy_a_0
            adj_enemy_a = list(set(adj_enemy_a))
            adj_enemy_b = adj_enemy_b_1 + adj_enemy_b_2 + adj_enemy_b_3 + adj_enemy_b_0
            adj_enemy_b = list(set(adj_enemy_b))

            # print("adj_enemy_a: ", adj_enemy_a)
            # print("adj_enemy_b: ", adj_enemy_b)

            if len(adj_enemy_a) >= len(adj_enemy_b):
                x, y = self.value_to_coordinate(enemy_a)
            else:
                x, y = self.value_to_coordinate(enemy_b)
            if x is not None and y is not None:
                return f"{x},{y}"

        # check for the longest player unblocked
        player_adj, player_a, player_b, player_type = self.longest_unblocked(board, True)
        # print("Player:")
        # print(player_adj, player_a, player_b, player_type)

        adj_player_a_0 = []
        adj_player_a_1 = []
        adj_player_a_2 = []
        adj_player_a_3 = []
        adj_player_b_0 = []
        adj_player_b_1 = []
        adj_player_b_2 = []
        adj_player_b_3 = []

        if player_a is not None:
            board.states[player_a] = self.player
            adj_player_a_0, adj_player_a_1, adj_player_a_2, adj_player_a_3 = self.get_adjacents(board, player_a)
            board.states[player_a] = 0

        if player_b is not None:
            board.states[player_b] = self.player
            adj_player_b_0, adj_player_b_1, adj_player_b_2, adj_player_b_3 = self.get_adjacents(board, player_b)
            board.states[player_b] = 0
        
        adj_player_a = adj_player_a_1 + adj_player_a_2 + adj_player_a_3 + adj_player_a_0
        adj_player_a = list(set(adj_player_a))
        adj_player_b = adj_player_b_1 + adj_player_b_2 + adj_player_b_3 + adj_player_b_0
        adj_player_b = list(set(adj_player_b))

        if len(adj_player_a) >= len(adj_player_b):
            x, y = self.value_to_coordinate(player_a)
        else:
            x, y = self.value_to_coordinate(player_b)
        return f"{x},{y}"

# kalau udah tengah, ambil diagonal kiri atas
# ambil yang bawah kiri abis itu
# potong tengah bawah
# potong tengah kiri
# potong jangan sampai memanjang 
# kalau ada tiga potong
# kalau ada empat halang