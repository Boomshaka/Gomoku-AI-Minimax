import tkinter as tk
import math
from game import Game


class Canvas(tk.Canvas):

    def __init__(self, master=None, height=0, width=0):

        tk.Canvas.__init__(self, master, height=height, width=width, background='#FFDD88')
        self.draw_board()
        self.game = Game()


    def draw_board(self):
        '''Draw the gomoku gameboard'''
        # vertical lines
        for i in range(1, 16):
            start_pixel_x = i * 30
            start_pixel_y = 30
            end_pixel_x = i * 30
            end_pixel_y = 450
            self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)

        # horizontal lines
        for i in range(1,16):
            start_pixel_x = 30
            start_pixel_y = i * 30
            end_pixel_x = 450
            end_pixel_y = i * 30
            self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)



    def draw_piece(self, row, col):
        '''
            Draw a black or white piece depending on current player.
            Black is player and White is AI
        '''
        start_pixel_x = (row + 1) * 30 - 13
        start_pixel_y = (col + 1) * 30 - 13
        end_pixel_x = (row + 1) * 30 + 13
        end_pixel_y = (col + 1) * 30 + 13

        if self.game.player_turn() == 1:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')

        elif self.game.player_turn() == 2:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')



    def gomoku_game(self, event):
        """
            The main game of gomoku.
            event is the position where the player clicked
        """
        while True:
            invalid_pos = True
            #Find closest spot to where the user clicked to determine the spot to fill
            for i in range(self.game.size()):
                for j in range(self.game.size()):
                    pixel_x = (i + 1) * 30
                    pixel_y = (j + 1) * 30
                    square_x = math.pow((event.x - pixel_x), 2)
                    square_y = math.pow((event.y - pixel_y), 2)
                    distance =  math.sqrt(square_x + square_y)
                    boundary = math.sqrt(2) * self.game.size()

                    #Boundary determines the maximum distance away from an intersection that can still be identified into that intersection
                    #Once the user's mouse click distance is closer than boundary, we can confirm the intersection to identify to
                    if (distance < boundary and (self.game.board()[i][j] == 0)):
                        invalid_pos = False
                        row, col = i, j
                        self.draw_piece(i,j)

                        break	# break out of loop
                else:
                    continue
                break			

            if invalid_pos:
                print('Invalid position.\n')
                break
            break

        # Make a move into the game board
        self.game.make_move(row,col)
        # Once player clicks a slot to make move, unbind mouse click so that AI can make a move
        self.unbind('<Button-1>')

        # Check if player won the game
        if self.game.check() == 2:
            self.create_text(250, 450, text = 'You Win!')
            self.unbind('<Button-1>')
            return 0


        #AI will decide its optimal move to make
        val = self.game.choose_move()
        row = val.get('choice')[0]
        col = val.get('choice')[1]

        #draw the stone then make its move
        self.draw_piece(row,col)
        self.game.make_move(row,col)

        # Once AI makes a move, re-bind mouse click so that player can make a move
        self.bind('<Button-1>', self.gomoku_game)

        # Check if AI won the game
        if self.game.check() == 1:
            self.create_text(250, 475, text = 'AI wins!')
            self.unbind('<Button-1>')
            return 0


class BoardFrame(tk.Frame):

    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.create_widgets()

    def create_widgets(self):
        self.Canvas = Canvas(height = 500, width = 500)
        self.Canvas.bind('<Button-1>', self.Canvas.gomoku_game)
        self.Canvas.pack()
