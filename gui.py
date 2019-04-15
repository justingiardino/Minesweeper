#!/usr/bin/env python3

## BUG: corner display either shouldn't show corners where there isn't a hint or clear that whole area too

import sys
import gameplay
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QApplication, QWidget, QApplication, QVBoxLayout, QGroupBox, QAction, QCheckBox, QDockWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
#from PyQt5.QtGui import QDrag

class DisplayMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Main Window'
        self.grid_buttons = {}
        self.grid = QGridLayout()
        self.display = QWidget()
        self.statusBar()
        self.game_height = 9
        self.game_width = 9
        self.game_bombs = 10
        self.bomb_guess = self.game_bombs
        self.main_board = gameplay.Board(self.game_height, self.game_width, self.game_bombs)
        self.game_time = QTimer()
        self.game_time.timeout.connect(self.update_time)
        self.time_display = 0
        self.initUI()

    def initUI(self):

        self.flag_mode = QCheckBox('Flag Mode', self)
        self.flag_mode.toggled.connect(self.flag_change)
        self.bomb_label = QLabel('Bombs Remaining: {}'.format(self.bomb_guess))
        self.time_label = QLabel('Time: {}'.format(self.time_display))
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(self.flag_mode)
        temp_layout.addWidget(self.time_label)
        temp_layout.addWidget(self.bomb_label)
        #create grid for display
        self.create_grid_layout()

        main_layout = QVBoxLayout()
        #top row is where I can put more displays, just need an hbox instead of flag_moder
        #main_layout.addWidget(self.flag_mode)
        main_layout.addLayout(temp_layout)
        #add grid display
        main_layout.addWidget(self.horizontalGroupBox)
        self.display.setLayout(main_layout)
        self.setCentralWidget(self.display)

        # menubar =self.menuBar()
        # self.fileMenu =  menubar.addMenu('File')
        # self.refreshAct = QAction('Refresh', self)
        # self.fileMenu.addAction(self.refreshAct)
        #1000 ms will update the clock
        self.game_time.start(1000)
        self.show()

    def create_grid_layout(self):

        self.horizontalGroupBox = QGroupBox("Game")
        #self.grid.setColumnStretch(0,1)

        for i in range(0,self.game_height):
            for j in range(0,self.game_width):
                #self.grid_buttons[(i,j)] = QPushButton("{}".format(self.main_board.game_board[i][j]))
                if self.main_board.display_board[i][j]:
                    #add QLabel to grid_buttons array?
                    self.grid.addWidget(QLabel(str(self.main_board.view_board[i][j])))
                else:
                    self.grid_buttons[(i,j)] = QPushButton(" ")
                    self.grid_buttons[(i,j)].clicked.connect(self.buttonClicked)
                    self.grid_buttons[(i,j)].setObjectName("{},{}".format(i,j))
                    self.grid.addWidget(self.grid_buttons[(i,j)],i,j)

        self.horizontalGroupBox.setLayout(self.grid)

    def update_grid_layout(self):
        for i in range(0,self.game_height):
            for j in range(0,self.game_width):
                #self.grid_buttons[(i,j)] = QPushButton("{}".format(self.main_board.game_board[i][j]))
                if self.main_board.display_board[i][j]:
                    label = QLabel(str(self.main_board.view_board[i][j]))
                    label.setStyleSheet("QLabel { background-color : silver; color : black; }")
                    self.grid.addWidget(label,i,j)
                elif self.main_board.view_board[i][j] == "^":
                    self.grid_buttons[(i,j)] = QPushButton("^")
                    self.grid_buttons[(i,j)].clicked.connect(self.buttonClicked)
                    self.grid_buttons[(i,j)].setObjectName("{},{}".format(i,j))
                    self.grid.addWidget(self.grid_buttons[(i,j)],i,j)
                else:
                    self.grid_buttons[(i,j)] = QPushButton(" ")#production
                    #self.grid_buttons[(i,j)] = QPushButton(self.main_board.game_board[i][j])#test
                    self.grid_buttons[(i,j)].clicked.connect(self.buttonClicked)
                    self.grid_buttons[(i,j)].setObjectName("{},{}".format(i,j))
                    self.grid.addWidget(self.grid_buttons[(i,j)],i,j)

    def clear_grid_layout(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

    def buttonClicked(self):
        #determine the source of the signal
        if self.game_time.isActive():
            sender = self.sender()
            #print(sender.objectName())
            locations = sender.objectName().split(',')
            self.statusBar().showMessage(sender.objectName() + ' was pressed.')
            if self.flag_mode.isChecked():
                #Add flag to square
                if sender.text() == " ":
                    self.main_board.view_board[int(locations[0])][int(locations[1])] = '^'
                    self.bomb_guess -= 1
                    self.bomb_label.setText('Bombs Remaining: {}'.format(self.bomb_guess))
                    if self.main_board.game_board[int(locations[0])][int(locations[1])] == 'X':
                        self.main_board.correct_bomb_count += 1
                #remove flag from square
                else:
                    self.main_board.view_board[int(locations[0])][int(locations[1])] = self.main_board.game_board[int(locations[0])][int(locations[1])]
                    self.bomb_guess += 1
                    self.bomb_label.setText('Bombs Remaining: {}'.format(self.bomb_guess))
                    if self.main_board.game_board[int(locations[0])][int(locations[1])] == 'X':
                        self.main_board.correct_bomb_count -= 1
            else:
                #add a condition when flag mode is disabled, but they click on a place where there is a flag
                #print(locations)
                self.main_board.check_bomb(int(locations[0]),int(locations[1]))

            self.clear_grid_layout()
            self.update_grid_layout()
            print("\n===============\ngame_bombs: {}\ncorrect_bomb_count: {}\nhint_count: {}\ncorrect_hint_count: {}\n===============\n".format(self.main_board.game_bombs,self.main_board.correct_bomb_count,self.main_board.hint_count,self.main_board.correct_hint_count))
            self.main_board.check_game_over()
            if self.main_board.game_over:
                self.game_time.stop()
                print(self.main_board.game_over_message)
        else:
            print("Clock is not running")

    def update_time(self):
        self.time_display += 1
        self.time_label.setText('Time: {}'.format(self.time_display))


    #might not need this, when doing a click action I can just use self.flag_mode.isChecked()
    def flag_change(self):
        if self.flag_mode.isChecked():
            print("Flag mode enabled")
        else:
            print("Flag mode disabled")


if __name__ == '__main__':
    #main_menu()
    #gameplay.main()
    app = QApplication(sys.argv)
    temp = DisplayMain()
    sys.exit(app.exec_())
