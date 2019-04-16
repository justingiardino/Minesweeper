#!/usr/bin/env python3
#from math import floor
import random

class Board(object):

    def __init__(self, game_height, game_width, game_bombs):
        self.game_height = game_height
        self.game_width = game_width
        self.game_bombs = game_bombs
        self.game_board = []
        self.display_board = []
        self.view_board = []
        self.game_over = False
        self.correct_bomb_count = 0
        self.hint_count = 0
        self.correct_hint_count = 0
        self.bomb_found = False
        self.game_over_message = "Initial Value of game_over_message"
        self.build_empty()
        self.fill_board()
        #may need to remove this print_board later to get rid of console
        self.print_board()

    def build_empty(self):
        for i in range(0,self.game_height):
            self.game_board.append([])
            self.display_board.append([])
            self.view_board.append([])
            for j in range(0,self.game_width):
                self.game_board[i].append('.')
                self.view_board[i].append('.')
                self.display_board[i].append(False)


    def print_board(self):
        print('*---Key----------------*')
        if(self.game_height > 9):
            print("   ", end='')
        else:
            print("  ", end='')
        for j in range(0,self.game_width):
            print("{}".format(j), end = ' ')
        print("")
        for i in range(0,self.game_height):
            for j in range(0,self.game_width):
                if j == 0:
                    #Double digit i and height
                    if i > 9 and self.game_height > 9:
                        print("{}".format(i),end=' ')
                    #Single digit i and double digit height
                    elif self.game_height > 9:
                        print("{}".format(i),end='  ')
                    #Single digit i and height
                    else:
                        print("{}".format(i),end=' ')

                print(self.game_board[i][j] ,end=' ')
            print("")

    def print_board_game(self):
        print('*--Game---------------*')
        if(self.game_height > 9):
            print("   ", end='')
        else:
            print("  ", end='')
        for j in range(0,self.game_width):
            print("{}".format(j), end = ' ')
        print("")
        for i in range(0,self.game_height):
            for j in range(0,self.game_width):
                if j == 0:
                    #Double digit i and height
                    if i > 9 and self.game_height > 9:
                        print("{}".format(i),end=' ')
                    #Single digit i and double digit height
                    elif self.game_height > 9:
                        print("{}".format(i),end='  ')
                    #Single digit i and height
                    else:
                        print("{}".format(i),end=' ')
                if self.display_board[i][j]:
                    print(self.view_board[i][j] ,end=' ')
                else:
                    print('.', end = ' ')
            print("")

    def fill_board(self):
        #randomly picks num_bombs number of coordinates for places to put bombs
        self.bomb_locations = random.sample(range(0,self.game_width * self.game_height), self.game_bombs)
        #print("Temporarily setting to static list for testing")
        #self.bomb_locations = [71,28,36,37,34,11,50,47,66,21]
        for i in range(0,self.game_height):
            for j in range(0, self.game_width):
                #turn 2d array into 1d
                curr_val = (i * self.game_width) + j
                if curr_val in self.bomb_locations:
                    #print('Bomb placed at i:{} j:{}\nWhere curr_val:{}'.format(i, j, curr_val ))
                    self.game_board[i][j] = 'X'

        #print(self.bomb_locations)
        #now need to fill all other places on the board with a number showing how many bombs are near by
        for i in range(0,self.game_height):
            for j in range(0, self.game_width):
                if self.game_board[i][j] != 'X':
                    temp_count = 0
                    #print("i: {}\nj: {}".format(i,j))
                    #input("Press a key to continue\n")
                    #upper left
                    if (i-1 > -1) and (j-1 > -1):
                        #print("i-1: {}\nj-1: {}".format((i-1), (j-1)))
                        if self.game_board[i-1][j-1] == 'X':
                            temp_count += 1
                    #upper middle
                    if (i-1 > -1):
                        if self.game_board[i-1][j] == 'X':
                            temp_count += 1
                    #upper right
                    if (i-1 > -1) and (j+1 < self.game_width):
                        if self.game_board[i-1][j+1] == 'X':
                            temp_count += 1
                    #middle left
                    if (j-1 > -1):
                        if self.game_board[i][j-1] == 'X':
                            temp_count += 1
                    #middle right
                    if (j+1 < self.game_width):
                        if self.game_board[i][j+1] == 'X':
                            temp_count += 1
                    #bottom left
                    if (i+1 < self.game_height) and (j-1 > -1):
                        if self.game_board[i+1][j-1] == 'X':
                            temp_count += 1
                    #bottom middle
                    if (i+1 < self.game_height):
                        if self.game_board[i+1][j] == 'X':
                            temp_count += 1
                    #bottom right
                    if (i+1 < self.game_height) and (j+1 < self.game_width):
                        if self.game_board[i+1][j+1] == 'X':
                            temp_count += 1
                    #print("temp_count: {}".format(temp_count))
                    #end of j iteration
                    if temp_count > 0:
                        #print("temp_count: {}".format(temp_count))
                        self.game_board[i][j] = str(temp_count)
                        self.hint_count += 1
                        #print("\n\n==============\nhint_count: {}\n==============\n\n".format(self.hint_count))


    def check_bomb(self, i_check, j_check):
        temp_val = (i_check * self.game_width + j_check)
        #print(temp_val)
        if temp_val in self.bomb_locations:
            #print("Bomb found!")
            self.view_board[i_check][j_check] = 'X'
            self.display_board[i_check][j_check] = True
            self.bomb_found = True
        else:
            #print("No bomb there")
            #self.display_board[y_check][x_check] = True
            self.flood_fill(i_check, j_check)
            self.corner_display()
        # self.print_board()
        # self.print_board_game()
        # self.check_game_over()

    def flood_fill(self, i_check, j_check):

        if self.game_board[i_check][j_check] != '.':
            if self.game_board[i_check][j_check] != 'X':
                if self.display_board[i_check][j_check] == False:
                    self.display_board[i_check][j_check] = True
                    self.correct_hint_count += 1
                    self.view_board[i_check][j_check] = self.game_board[i_check][j_check]
            return
        self.game_board[i_check][j_check] = '-'
        self.view_board[i_check][j_check] = '-'
        self.display_board[i_check][j_check] = True

        #right
        if j_check + 1 < self.game_width:
            self.flood_fill(i_check, j_check + 1)
        #left
        if j_check - 1 > -1:
            self.flood_fill(i_check, j_check -1)
        #down
        if i_check + 1 < self.game_height:
            self.flood_fill(i_check + 1, j_check)
        #up
        if i_check - 1 > -1:
            self.flood_fill(i_check - 1, j_check)

    def corner_display(self):
        for i in range(0,self.game_height):
            for j in range(0, self.game_width):
                if self.view_board[i][j] == '-':
                    #upper left
                    if (i-1 > -1) and (j-1 > -1):
                        if self.display_board[i-1][j-1] == False:
                            self.view_board[i-1][j-1] = self.game_board[i-1][j-1]
                            self.correct_hint_count += 1
                            self.display_board[i-1][j-1] = True
                    #upper right
                    if (i-1 > -1) and (j+1 < self.game_width):
                        if self.display_board[i-1][j+1] == False:
                            self.view_board[i-1][j+1] = self.game_board[i-1][j+1]
                            self.correct_hint_count += 1
                            self.display_board[i-1][j+1] = True
                    #bottom left
                    if (i+1 < self.game_height) and (j-1 > -1):
                        if self.display_board[i+1][j-1] == False:
                            self.view_board[i+1][j-1] = self.game_board[i+1][j-1]
                            self.correct_hint_count += 1
                            self.display_board[i+1][j-1] = True
                    #bottom right
                    if (i+1 < self.game_height) and (j+1 < self.game_width):
                        if self.display_board[i+1][j+1] == False:
                            self.view_board[i+1][j+1] = self.game_board[i+1][j+1]
                            self.correct_hint_count += 1
                            self.display_board[i+1][j+1] = True
    def check_game_over(self):
        #Flagged all correct bombs
        if self.correct_bomb_count == self.game_bombs:
            self.game_over = True
            self.game_over_message = "All bombs flagged! You win!"

        #cleared all hint squares, only bombs remain
        if self.correct_hint_count == self.hint_count:
            self.game_over = True
            self.game_over_message = "Cleared all hints, only bombs remain! You win!"

        #hit a bomb
        if self.bomb_found == True:
            self.game_over = True
            self.game_over_message = "You hit a bomb! You lose!"






def main():
    print("Welcome to Minesweeper!\n")
    #beginner: 9, 9, 10
    #intermediate: 16, 16, 40
    #expert: 16, 30, 99
    game_height = 9
    game_width = 9
    game_bombs = 10

    main_board = Board(game_height, game_width, game_bombs)
    while not main_board.game_over:
        #no error checking for now

        print("\n===============\ngame_bombs: {}\ncorrect_bomb_count: {}\nhint_count: {}\ncorrect_hint_count: {}\n===============\n".format(main_board.game_bombs,main_board.correct_bomb_count,main_board.hint_count,main_board.correct_hint_count))

        print("What would you like to do?\n1)Clear Square\n2)Flag Bomb\n3)Exit")
        user_choice = int(input("> "))
        if user_choice == 1:
            print("Select a location to check(horizontal,vertical)")
            locations = input("> ").split(',')
            print(locations)
            main_board.check_bomb(int(locations[1]),int(locations[0]))
            main_board.print_board()
            main_board.print_board_game()
            main_board.check_game_over()
        elif user_choice == 2:
            print("Select a location to place a flag(horizontal,vertical)")
            locations = input("> ").split(',')
            #print(locations)
            main_board.view_board[int(locations[1])][int(locations[0])] = '^'
            #Check to see if this was a correct guess, will need to clean up this logc later
            if main_board.game_board[int(locations[1])][int(locations[0])] == 'X':
                main_board.correct_bomb_count += 1
            main_board.display_board[int(locations[1])][int(locations[0])] = True
            main_board.print_board()
            main_board.print_board_game()
            main_board.check_game_over()
        else:
            print("Good bye\n")
            main_board.game_over = True
    print(main_board.game_over_message)




if __name__ == '__main__':
    main()
