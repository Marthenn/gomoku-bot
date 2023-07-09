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
        print(value)
        x = value // 8
        y = value % 8
        return x, y
    
    def is_diagonal(self, val1, val2):
        x1, y1 = self.value_to_coordinate(val1)
        x2, y2 = self.value_to_coordinate(val2)
        return abs(x1 - x2) == abs(y1 - y2)
    
    def is_horizontal(self, val1, val2):
        x1, y1 = self.value_to_coordinate(val1)
        x2, y2 = self.value_to_coordinate(val2)
        return x1 == x2
    
    def is_vertical(self, val1, val2):
        x1, y1 = self.value_to_coordinate(val1)
        x2, y2 = self.value_to_coordinate(val2)
        return y1 == y2
    
    def get_adjacents(self, board, value):
        diag = []
        hor = []
        ver = []
        for x in board.states:
            if x == value:
                if self.is_diagonal(x, value):
                    diag.append(x)
                if self.is_horizontal(x, value):
                    hor.append(x)
                if self.is_vertical(x, value):
                    ver.append(x)
        return diag, hor, ver
    
    def not_blocked(self, board, adj, val, type):
        # sort adj list
        adj.sort()
        start = adj[0]
        end = adj[-1]
        a = None # left or up
        b = None # right or down
        if type == 0:
            # check whether it's a / or \ diagonal
            _, start_y = self.value_to_coordinate(start)
            _, end_y = self.value_to_coordinate(end)
            if start_y > end_y:
                # it's a /, check for the bottom left and top right
                start_x, start_y = self.value_to_coordinate(start)
                end_x, end_y = self.value_to_coordinate(end)
                if start_x != 0 and start_y != 0:
                    if start-9 not in board.states:
                        a = start-9
                if end_x != 7 and end_y != 7:
                    if end+9 not in board.states:
                        b = end+9
            else:
                # it's a \, check for the top left and bottom right
                start_x, start_y = self.value_to_coordinate(start)
                end_x, end_y = self.value_to_coordinate(end)
                if start_x != 0 and start_y != 7:
                    if start-7 not in board.states:
                        a = start-7
                if end_x != 7 and end_y != 0:
                    if end+7 not in board.states:
                        b = end+7
        elif type == 1:
            # check left and right of the horizontal
            _, start_y = self.value_to_coordinate(start)
            _, end_y = self.value_to_coordinate(end)
            if start_y != 0:
                if start-1 not in board.states:
                    a = start-1
            if end_y != 7:
                if end+1 not in board.states:
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
        return a, b
    
    def longest_unblocked(self, board, player):
        enemy = 1 if player == 2 else 2
        val = self.player if player else enemy
        max_len = 0
        adj = []
        type = -1 # 0 = diag, 1 = hor, 2 = ver
        for x in board.states:
            if x == val:
                diag, hor, ver = self.get_adjacents(board, x)
                if len(diag) > max_len:
                    a, b = self.not_blocked(board, diag, val, 0)
                    if a is not None or b is not None:
                        max_len = len(diag)
                        adj = diag
                        type = 0
                if len(hor) > max_len:
                    a, b = self.not_blocked(board, hor, val, 1)
                    if a is not None or b is not None:
                        max_len = len(hor)
                        adj = hor
                        type = 1
                if len(ver) > max_len:
                    a, b = self.not_blocked(board, ver, val, 2)
                    if a is not None or b is not None:
                        max_len = len(ver)
                        adj = ver
                        type = 2
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
        if board.states == {}:
            return "3,3" # kalau kosong, ambil tengah
        return f"{x},{y}"

# kalau udah tengah, ambil diagonal kiri atas
# ambil yang bawah kiri abis itu
# potong tengah bawah
# potong tengah kiri
# potong jangan sampai memanjang 
# kalau ada tiga potong
# kalau ada empat halang