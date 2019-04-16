#!/usr/bin/env python3

## BUG: corner display either shouldn't show corners where there isn't a hint or clear that whole area too
## BUG: Game over should only be when you clear all hints, not find all bombs, shouldn't let self.bombs_guess be less than 0 

### TODO: If you hit a bomb display where the bombs are that you haven't flagged

import sys
import gameplay
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QApplication, QWidget, QApplication, QVBoxLayout, QGroupBox, QAction, QCheckBox, QDockWidget, QLabel, QHBoxLayout, QLineEdit, qApp, QStatusBar
from PyQt5.QtCore import Qt, QTimer, QSize
#from PyQt5.QtGui import QDrag

class PopUpWindow(QWidget):
    def __init__(self, pop_height, pop_width, pop_bombs):
        super().__init__()
        self.pop_height = pop_height
        self.pop_width = pop_width
        self.pop_bombs = pop_bombs
        self.valid_int = True
        self.pref_status = QStatusBar()
        self.pref_status_label = QLabel()
        self.pref_status.addWidget(self.pref_status_label)
        self.pref_status.hide()
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

        #Hbox for two buttons on bottom, Hbox for three buttons on top for difficulty, in Vbox put difficulty on top, grid in the middle and button box on bottom
        difficulty_box = QHBoxLayout()
        beg_button = QPushButton("Beginner")
        beg_button.clicked.connect(self.beg_push)
        int_button = QPushButton("Intermediate")
        int_button.clicked.connect(self.int_push)
        adv_button = QPushButton("Advanced")
        adv_button.clicked.connect(self.adv_push)
        difficulty_box.addWidget(beg_button)
        difficulty_box.addWidget(int_button)
        difficulty_box.addWidget(adv_button)

        button_box = QHBoxLayout()
        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.ok_push)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_push)
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)

        self.final_display = QVBoxLayout()
        self.final_display.addLayout(difficulty_box)
        self.final_display.addLayout(self.pref_grid)
        self.final_display.addLayout(button_box)
        self.final_display.addWidget(self.pref_status)

        #self.setLayout(self.pref_grid)
        self.setLayout(self.final_display)

    def ok_push(self):
        #print("Ok was clicked")
        #reset flag to true, then recheck all values before submitting
        self.valid_int = True
        self.check_int(self.height_edit.text())
        self.check_int(self.width_edit.text())
        self.check_int(self.bombs_edit.text())
        if self.valid_int:
            #Make sure there are less bombs than number of squares
            if int(self.bombs_edit.text()) < (int(self.width_edit.text()) * int(self.height_edit.text())):
                if (int(self.width_edit.text()) in range(1,51)) and (int(self.height_edit.text()) in range(1,51)):
                    self.pop_height = int(self.height_edit.text())
                    self.pop_width = int(self.width_edit.text())
                    self.pop_bombs = int(self.bombs_edit.text())
                    self.pref_status_label.setText("")
                    self.pref_status.hide()
                    #print("\n\n=================\npop_height:{}\npop_width:{}\npop_bombs:{}\n=================\n\n".format(self.pop_height, self.pop_width, self.pop_bombs))
                    self.close()
                else:
                    self.pref_status.show()
                    self.pref_status_label.setText("Error: Board must have dimensions less than 50x50")
            else:
                self.pref_status.show()
                self.pref_status_label.setText("Error: Too many bombs")


    def cancel_push(self):
        #print("Cancel was clicked")
        self.pref_status.hide()
        self.close()

        '''
        Beginner:     H:9  W:9  B:10
        Intermediate: H:16 W:16 B:40
        Advanced:     H:16 W:30 B:99
        '''
    def beg_push(self):
        #print("Beginner")
        self.pref_status.hide()
        self.height_edit.setText("9")
        self.width_edit.setText("9")
        self.bombs_edit.setText("10")

    def int_push(self):
        #print("Intermediate")
        self.pref_status.hide()
        self.height_edit.setText("16")
        self.width_edit.setText("16")
        self.bombs_edit.setText("40")

    def adv_push(self):
        #print("Advanced")
        self.pref_status.hide()
        self.height_edit.setText("16")
        self.width_edit.setText("30")
        self.bombs_edit.setText("99")


# '''
# If the value can become an int, need to verify that
# 1) The number is positive
# 2) There are more squares than bombs: bombs < h * w
# 3) Max board size?
# May need to collapse check_int into
# '''
    def check_int(self, check_val):
        try:
            int(check_val)
        except ValueError:
            #print('{} is not able to become an int'.format(check_val))
            self.valid_int = False
            #self.statusBar.showMessage("{} is not a valid entry.".format())
            self.pref_status_label.setText("{} is not a valid entry.".format(check_val))
            self.pref_status.show()
        else:
            pass
            #check dimensions
            #print('{} is now an integer'.format(check_val))

class DisplayMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Minesweeper'
        self.setWindowTitle(self.title)

        #default start parameters
        self.game_height = 9
        self.game_width = 9
        self.game_bombs = 10

        #create pop up window object
        self.pref_widget = PopUpWindow(self.game_height, self.game_width, self.game_bombs)

        #menus - Only need to be created once
        menubar =self.menuBar()
        menubar.setNativeMenuBar(False) #This fixes an issue with the mac display
        self.fileMenu =  menubar.addMenu('&File')
        self.editMenu = menubar.addMenu('&Edit')

        #actions
        self.newAct = QAction('New Game', self)
        self.prefAct = QAction('Preferences', self)
        self.leaveAct = QAction('Leave', self)

        #action events
        self.newAct.triggered.connect(self.initUI)
        self.prefAct.triggered.connect(self.edit_preferences)
        self.leaveAct.triggered.connect(self.leave_game)

        #add action to menu
        self.fileMenu.addAction(self.newAct)
        self.editMenu.addAction(self.prefAct)
        self.fileMenu.addAction(self.leaveAct)

        #initialize display
        self.grid_size = QSize(20,20)
        self.initUI()

    def initUI(self):
        #print("\n\n=================\npref_widget.pop_height:{}\npref_widget.pop_width:{}\npref_widget.pop_bombs:{}\n=================\n\n".format(self.pref_widget.pop_height, self.pref_widget.pop_width, self.pref_widget.pop_bombs))
        #Check to see if the preferences have been updated
        self.game_height = self.pref_widget.pop_height
        self.game_width = self.pref_widget.pop_width
        self.game_bombs = self.pref_widget.pop_bombs
        #print("\n\n=================\ngame_height:{}\ngame_width:{}\ngame_bombs:{}\n=================\n\n".format(self.game_height, self.game_width, self.game_bombs))
        self.new_game = True #used to start clock on first button click
        self.grid_buttons = {}
        self.grid = QGridLayout() #
        self.display = QWidget() #Widget to place grid and top row of game information
        self.statusBar()
        self.bomb_guess = self.game_bombs #counter for number of bombs remaining
        self.main_board = gameplay.Board(self.game_height, self.game_width, self.game_bombs)
        self.game_time = QTimer() #create timer to show how long it took to finish the game
        self.time_display = 0
        self.flag_mode = QCheckBox('Flag Mode', self) #change mode that user is playing in
        #self.flag_mode.toggled.connect(self.flag_change)
        self.bomb_label = QLabel('Bombs Remaining: {}'.format(self.bomb_guess))
        self.time_label = QLabel('Time: 00{}'.format(self.time_display))
        self.game_time.timeout.connect(self.update_time) #time start is called on the first button click
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(self.flag_mode) #Left
        temp_layout.addWidget(self.time_label) #middle
        temp_layout.addWidget(self.bomb_label) #right
        #create grid for display
        self.create_grid_layout()
        self.grid.setSpacing(2)

        main_layout = QVBoxLayout()
        main_layout.addLayout(temp_layout)
        main_layout.addWidget(self.horizontalGroupBox)
        self.display.setLayout(main_layout)
        self.setCentralWidget(self.display)
        self.adjustSize()

        self.show()

    def create_grid_layout(self):

        self.horizontalGroupBox = QGroupBox("Game")
        for i in range(0,self.game_height):
            for j in range(0,self.game_width):
                #This shouldn't ever be true, may not need it
                if self.main_board.display_board[i][j]:
                    self.grid.addWidget(QLabel(str(self.main_board.view_board[i][j])))
                else:
                    self.grid_buttons[(i,j)] = QPushButton(" ")
                    self.grid_buttons[(i,j)].clicked.connect(self.buttonClicked)
                    self.grid_buttons[(i,j)].setObjectName("{},{}".format(i,j))
                    self.grid_buttons[(i,j)].setFixedSize(self.grid_size)
                    self.grid.addWidget(self.grid_buttons[(i,j)],i,j)

        self.horizontalGroupBox.setLayout(self.grid)

    def update_grid_layout(self):
        for i in range(0,self.game_height):
            for j in range(0,self.game_width):
                #if display board is true at these coordinates display the hint at that value
                if self.main_board.display_board[i][j]:
                    label = QLabel(str(self.main_board.view_board[i][j]))
                    label.setStyleSheet("QLabel { background-color : silver; color : black; }")
                    label.setFixedSize(self.grid_size)
                    self.grid.addWidget(label,i,j)
                #display flag
                elif self.main_board.view_board[i][j] == "^":
                    self.grid_buttons[(i,j)] = QPushButton("^")
                    self.grid_buttons[(i,j)].clicked.connect(self.buttonClicked)
                    #Use objectName later to get coordinates of button that was clicked
                    self.grid_buttons[(i,j)].setObjectName("{},{}".format(i,j))
                    self.grid_buttons[(i,j)].setFixedSize(self.grid_size)
                    self.grid.addWidget(self.grid_buttons[(i,j)],i,j)
                #display regular flag
                else:
                    self.grid_buttons[(i,j)] = QPushButton(" ")
                    self.grid_buttons[(i,j)].clicked.connect(self.buttonClicked)
                    self.grid_buttons[(i,j)].setObjectName("{},{}".format(i,j))
                    self.grid_buttons[(i,j)].setFixedSize(self.grid_size)
                    self.grid.addWidget(self.grid_buttons[(i,j)],i,j)

    def clear_grid_layout(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

    def buttonClicked(self):
        #determine the source of the signal
        if self.new_game:
            self.new_game = False
            #Every 1000 ms will update the clock
            self.game_time.start(1000)

        if self.game_time.isActive():
            sender = self.sender()
            #print(sender.objectName())
            locations = sender.objectName().split(',')
            #self.statusBar().showMessage(sender.objectName() + ' was pressed.')
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
                #flag mode is disabled, but they click on a place where there is a flag do nothing
                if sender.text() == " ":
                    self.main_board.check_bomb(int(locations[0]),int(locations[1]))

            self.clear_grid_layout()
            self.update_grid_layout()
            #print("\n===============\ngame_bombs: {}\ncorrect_bomb_count: {}\nhint_count: {}\ncorrect_hint_count: {}\n===============\n".format(self.main_board.game_bombs,self.main_board.correct_bomb_count,self.main_board.hint_count,self.main_board.correct_hint_count))
            self.main_board.check_game_over()
            if self.main_board.game_over:
                self.game_time.stop()
                self.statusBar().showMessage(self.main_board.game_over_message)
                print(self.main_board.game_over_message)
        else:
            print("Clock is not running")


    def update_time(self):
        self.time_display += 1
        if len(str(self.time_display)) == 1:
            self.time_label.setText('Time: 00{}'.format(self.time_display))
        elif len(str(self.time_display)) == 2:
            self.time_label.setText('Time: 0{}'.format(self.time_display))
        else:
            self.time_label.setText('Time: {}'.format(self.time_display))

    def edit_preferences(self):
        #print("Edit Preferences")
        #create labels
        self.pref_widget.setGeometry(300, 300, 250, 150)
        self.pref_widget.setWindowTitle('Preferences')
        self.pref_widget.show()

    def leave_game(self):
        qApp.quit()


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
