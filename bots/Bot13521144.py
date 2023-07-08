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

        self.number = -1

        self.board_score = [
            [0, 0, 0, 0, 0, 0, 0, 0],  # 0
            [0, 0, 0, 0, 0, 0, 0, 0],  # 1
            [0, 0, 0, 0, 0, 0, 0, 0],  # 2
            [0, 0, 0, 1024, 1024, 0, 0, 0],  # 3
            [0, 0, 0, 0, 0, 0, 0, 0],  # 4
            [0, 0, 0, 0, 0, 0, 0, 0],  # 5
            [0, 0, 0, 0, 0, 0, 0, 0],  # 6
            [0, 0, 0, 0, 0, 0, 0, 0]  # 7
        ]

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
        return (x, y)
    
    def update_board_score(self, board : Board):
        # update all blocked cells value to -1
        for cells in board.states:
            print(cells)

        # check if there's any 5 in a row that are not blocked
        # the 5 in a row can be horizontal, vertical, or diagonal
        # if there's any, then the score of the cell is 1024
        print(self.board_score)
    
    def get_best_move(self):
        # max_val = -10000
        # max_x = -1
        # max_y = -1
        # for i in range(8):
        #     for j in range(8):
        #         if self.board_score[i][j] > max_val:
        #             max_val = self.board_score[i][j]
        #             max_x = i
        #             max_y = j
        # return max_x, max_y
        x = random.randint(0,7)
        y = random.randint(0,7)
        return x, y

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
        # update_board_score(board)
        # x, y = get_best_move(board)
        for cells in board.states:
            a, b = self.value_to_coordinate(cells)
            print(a, b)
        x = random.randint(0,7)
        y = random.randint(0,7)
        return f"{x},{y}"

# kalau udah tengah, ambil diagonal kiri atas
# ambil yang bawah kiri abis itu
# potong tengah bawah
# potong tengah kiri
# potong jangan sampai memanjang 
# kalau ada tiga potong
# kalau ada empat halang