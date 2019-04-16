#!/usr/bin/env python3

## BUG: corner display either shouldn't show corners where there isn't a hint or clear that whole area too

import sys
import gameplay
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QApplication, QWidget, QApplication, QVBoxLayout, QGroupBox, QAction, QCheckBox, QDockWidget, QLabel, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QTimer
#from PyQt5.QtGui import QDrag

class PopUpWindow(QWidget):
    def __init__(self, pop_height, pop_width, pop_bombs):
        super().__init__()
        self.pop_height = pop_height
        self.pop_width = pop_width
        self.pop_bombs = pop_bombs
        self.getVals()

    def getVals(self):
        self.height_label = QLabel("Height:")
        self.width_label = QLabel("Width:")
        self.bombs_label = QLabel("Bombs:")

        #create line edit objects
        self.height_edit = QLineEdit(str(self.pop_height))
        self.width_edit = QLineEdit(str(self.pop_width))
        self.bombs_edit = QLineEdit(str(self.pop_bombs))

        #create a grid
        self.pref_grid = QGridLayout()
        self.pref_grid.setSpacing(10)

        #add widgets to grid
        self.pref_grid.addWidget(self.height_label, 1, 0)
        self.pref_grid.addWidget(self.height_edit, 1, 1)
        self.pref_grid.addWidget(self.width_label, 2, 0)
        self.pref_grid.addWidget(self.width_edit, 2, 1)
        self.pref_grid.addWidget(self.bombs_label, 3, 0)
        self.pref_grid.addWidget(self.bombs_edit, 3, 1)

        #Hbox for two buttons on bottom, in Vbox put grid on top and button box on bottom
        button_box = QHBoxLayout()
        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.ok_push)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_push)
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)

        self.final_display = QVBoxLayout()
        self.final_display.addLayout(self.pref_grid)
        self.final_display.addLayout(button_box)

        #self.setLayout(self.pref_grid)
        self.setLayout(self.final_display)

    def ok_push(self):
        print("Ok was clicked")
        self.close()

    def cancel_push(self):
        print("Cancel was clicked")
        self.close()

class DisplayMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Main Window'
        #Will default to this game setting, will need to be able to change in preferences later
        self.new_game_height = 9
        self.new_game_width = 9
        self.new_game_bombs = 10
        self.initUI()

    def initUI(self):
        self.game_height = self.new_game_height
        self.game_width = self.new_game_width
        self.game_bombs = self.new_game_bombs
        self.grid_buttons = {}
        self.grid = QGridLayout()
        self.display = QWidget()
        self.statusBar()
        self.bomb_guess = self.game_bombs
        self.main_board = gameplay.Board(self.game_height, self.game_width, self.game_bombs)
        self.game_time = QTimer()
        self.time_display = 0
        self.flag_mode = QCheckBox('Flag Mode', self)
        self.flag_mode.toggled.connect(self.flag_change)
        self.bomb_label = QLabel('Bombs Remaining: {}'.format(self.bomb_guess))
        self.time_label = QLabel('Time: {}'.format(self.time_display))
        self.game_time.timeout.connect(self.update_time)
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(self.flag_mode) #Left
        temp_layout.addWidget(self.time_label) #middle
        temp_layout.addWidget(self.bomb_label) #right
        #create grid for display
        self.create_grid_layout()

        main_layout = QVBoxLayout()
        main_layout.addLayout(temp_layout)
        main_layout.addWidget(self.horizontalGroupBox)
        self.display.setLayout(main_layout)
        self.setCentralWidget(self.display)

        #menu bar
        menubar =self.menuBar()

        #menus
        self.fileMenu =  menubar.addMenu('File')
        self.editMenu = menubar.addMenu('Edit')

        #actions
        self.newAct = QAction('New Game', self)
        self.prefAct = QAction('Preferences', self)

        #action events
        self.newAct.triggered.connect(self.initUI)
        self.prefAct.triggered.connect(self.edit_preferences)

        #add action to menu
        self.fileMenu.addAction(self.newAct)
        self.editMenu.addAction(self.prefAct)

        #Every 1000 ms will update the clock
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
                self.statusBar().showMessage(self.main_board.game_over_message)
                print(self.main_board.game_over_message)
        else:
            print("Clock is not running")

    def update_time(self):
        self.time_display += 1
        self.time_label.setText('Time: {}'.format(self.time_display))

    def edit_preferences(self):
        print("Edit Preferences")
        #create labels
        self.pref_widget = PopUpWindow(self.game_height, self.game_width, self.game_bombs)
        self.pref_widget.setGeometry(300, 300, 250, 150)
        self.pref_widget.setWindowTitle('Preferences')
        self.pref_widget.show()



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
