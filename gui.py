#!/usr/bin/env python3

import sys
import gameplay
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QApplication, QWidget, QApplication, QVBoxLayout, QGroupBox, QAction, QCheckBox, QDockWidget, QLabel
from PyQt5.QtCore import Qt
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
        self.main_board = gameplay.Board(self.game_height, self.game_width, self.game_bombs)
        self.initUI()

    def initUI(self):

        self.flag_mode = QCheckBox('Flag Mode', self)
        self.flag_mode.toggled.connect(self.flag_change)
        #create grid for display
        self.create_grid_layout()

        main_layout = QVBoxLayout()
        #top row is where I can put more displays, just need an hbox instead of flag_moder
        main_layout.addWidget(self.flag_mode)
        #add grid display
        main_layout.addWidget(self.horizontalGroupBox)
        self.display.setLayout(main_layout)
        self.setCentralWidget(self.display)

        # menubar =self.menuBar()
        # self.fileMenu =  menubar.addMenu('File')
        # self.refreshAct = QAction('Refresh', self)
        # self.fileMenu.addAction(self.refreshAct)
        self.show()

    def create_grid_layout(self):

        self.horizontalGroupBox = QGroupBox("Game")

        for i in range(0,self.game_height):
            for j in range(0,self.game_width):
                #self.grid_buttons[(i,j)] = QPushButton("{}".format(self.main_board.game_board[i][j]))
                if self.main_board.display_board[i][j]:
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
                else:
                    self.grid_buttons[(i,j)] = QPushButton(" ")
                    self.grid_buttons[(i,j)].clicked.connect(self.buttonClicked)
                    self.grid_buttons[(i,j)].setObjectName("{},{}".format(i,j))
                    self.grid.addWidget(self.grid_buttons[(i,j)],i,j)

    def clear_grid_layout(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

    def buttonClicked(self):
        #determine the source of the signal
        sender = self.sender()
        print(sender.objectName())
        self.statusBar().showMessage(sender.objectName() + ' was pressed.')
        if self.flag_mode.isChecked():
            pass
        else:
            locations = sender.objectName().split(',')
            self.main_board.check_bomb(int(locations[0]),int(locations[1]))
            self.clear_grid_layout()
            self.update_grid_layout()

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
