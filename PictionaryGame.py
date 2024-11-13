from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QDockWidget, QPushButton, QVBoxLayout, \
    QLabel, QMessageBox, QLineEdit, QHBoxLayout
from PyQt6.QtGui import QIcon, QPainter, QPen, QAction, QPixmap, QFont
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QRect
import sys
import csv, random

# constructor, getter, setter
class GameCenter:
    def __init__(self, mode, word, turn, score1, score2):
        self._mode = mode
        self._word = word
        self._turn = turn
        self._score1 = score1
        self._score2 = score2

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        self._mode = new_mode

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, new_word):
        self._word = new_word

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, new_turn):
        self._turn = new_turn

    @property
    def score1(self):
        return self._score1

    @score1.setter
    def score1(self, new_score):
        self._score1 = new_score

    @property
    def score2(self):
        return self._score2

    @score2.setter
    def score2(self, new_score):
        self._score2 = new_score

class PictionaryGame(QMainWindow):
    '''
    Painting Application class
    '''

    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("Pictionary Game")

        self.self_obj = self # create an instance of itself

        self.startDetail = None # set word window close

        # set the windows dimensions
        top = 400
        left = 400
        width = 800
        height = 600
        self.setGeometry(top, left, width, height)

        # set the icon
        self.setWindowIcon(QIcon("./icons/paint-brush.png"))

        # image settings (default)
        self.image = QPixmap("./icons/canvas.png")
        self.image.fill(Qt.GlobalColor.white)
        mainWidget = QWidget()
        mainWidget.setMaximumWidth(300)

        # draw settings (default)
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black
        self.drawingMode = "free"

        # reference to start and last point recorded by mouse
        self.startPoint = QPoint()
        self.lastPoint = QPoint()

        # set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        mainMenu.setStyleSheet("QMenuBar { background-color: white; }")
        fileMenu = mainMenu.addMenu(" File")
        helpMenu = mainMenu.addMenu((" Help"))
        brushSizeMenu = mainMenu.addMenu(" Brush Size")
        brushColorMenu = mainMenu.addMenu(" Brush Colour")
        shapeMenu = mainMenu.addMenu(" Shape")

        # save menu item
        saveAction = QAction(QIcon("./icons/save.png"), "Save", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        # clear
        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        # open
        openAction = QAction(QIcon("./icons/open.png"), "Open", self)
        openAction.setShortcut("Ctrl+O")
        fileMenu.addAction(openAction)
        openAction.triggered.connect(self.open)

        # exit
        exitAction = QAction(QIcon("./icons/exit.png"), "Exit", self)
        exitAction.setShortcut("Ctrl+Z")
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exit)

        # rules
        ruleAction = QAction(QIcon("./icons/help.png"), "Rule", self)
        ruleAction.setShortcut("Ctrl+H")
        helpMenu.addAction(ruleAction)
        ruleAction.triggered.connect(self.rule)

        # brush thickness
        threepxAction = QAction(QIcon("./icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")
        brushSizeMenu.addAction(threepxAction)  # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # brush colors
        blackAction = QAction(QIcon("./icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColorMenu.addAction(blackAction);
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon("./icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColorMenu.addAction(redAction);
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon("./icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColorMenu.addAction(greenAction);
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("./icons/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColorMenu.addAction(yellowAction);
        yellowAction.triggered.connect(self.yellow)

        whiteAction = QAction(QIcon("./icons/white.png"), "White", self)
        whiteAction.setShortcut("Ctrl+W")
        brushColorMenu.addAction(whiteAction);
        whiteAction.triggered.connect(self.white)

        # shape
        normalAction = QAction(QIcon("./icons/paint-brush.png"), "Normal", self)
        shapeMenu.addAction(normalAction);
        normalAction.triggered.connect(lambda: self.setMode("free"))

        fillAction = QAction(QIcon("./icons/fill.png"), "Fill Background", self)
        shapeMenu.addAction(fillAction);
        fillAction.triggered.connect(lambda: self.fillCanvas())

        rectangleAction = QAction(QIcon("./icons/rectangle.png"), "Rectangle", self)
        shapeMenu.addAction(rectangleAction);
        rectangleAction.triggered.connect(lambda: self.setMode("rectangle"))

        circleAction = QAction(QIcon("./icons/circle.png"), "Circle", self)
        shapeMenu.addAction(circleAction);
        circleAction.triggered.connect(lambda: self.setMode("circle"))

        # Side Dock for player
        self.dockInfo = QDockWidget()
        self.dockInfo.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockInfo)

        #widget inside the Dock
        playerInfo = QWidget()
        self.vbdock = QVBoxLayout()
        playerInfo.setLayout(self.vbdock)
        playerInfo.setMaximumSize(200, self.height())
        #add controls to custom widget
        self.turnLabel = QLabel(f"Current Turn: {game_center.turn}")
        self.score1Label = QLabel(f"Player 1: {game_center.score1}")
        self.score2Label = QLabel(f"Player 2: {game_center.score2}")
        self.modeLabel = QLabel(f"Mode : {game_center.mode}")
        self.vbdock.addWidget(self.turnLabel)
        self.vbdock.addSpacing(20)
        self.vbdock.addWidget(QLabel("Scores:"))
        self.vbdock.addWidget(self.score1Label)
        self.vbdock.addWidget(self.score2Label)
        self.vbdock.addSpacing(20)
        self.vbdock.addWidget(self.modeLabel)
        self.vbdock.addStretch(1)
        start = QPushButton("Start")
        self.vbdock.addWidget(start) #change
        start.clicked.connect(self.startGame)

        #Setting colour of dock to gray
        playerInfo.setAutoFillBackground(True)
        p = playerInfo.palette()
        p.setColor(playerInfo.backgroundRole(), Qt.GlobalColor.gray)
        playerInfo.setPalette(p)

        #set widget for dock
        self.dockInfo.setWidget(playerInfo)

    def updateUI(self):  # update score and turn
        self.turnLabel.setText(f"Current Turn: {game_center.turn}")
        self.score1Label.setText(f"Player 1: {game_center.score1}")
        self.score2Label.setText(f"Player 2: {game_center.score2}")
        self.modeLabel.setText(f"Mode : {game_center.mode}")

    def setMode(self, mode): # show drawing mode
        self.drawingMode = mode
        print(f"Mode: {mode}")

    # event handlers
    def mousePressEvent(self, event):  # when the mouse is pressed
        if event.button() == Qt.MouseButton.LeftButton:  # if the pressed button is the left button
            self.drawing = True  # enter drawing mode
            self.startPoint = event.pos()
            self.lastPoint = event.pos()  # save the location of the mouse press as the lastPoint

    def mouseMoveEvent(self, event):  # when the mouse is moved
        if self.drawing and self.drawingMode == "free":
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type.
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.startPoint, event.pos())  # draw a line from the point of the oroiginal press to the point to where the mouse was dragged to
            self.startPoint = event.pos()  # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
            self.update()  # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(self, event):  # when the mouse is released
        if event.button() == Qt.MouseButton.LeftButton:  # if the released button is the left button
            self.drawing = False  # exit drawing mode
            self.lastPoint = event.pos()
            if self.drawingMode == "rectangle":
                self.rectangle()
            elif self.drawingMode == "circle":
                self.circle()

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(self)  # create a new QPainter object
        canvasPainter.drawPixmap(self.rect(), self.image, self.image.rect())  # draw the image

    # resize event - this function is called
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "","PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.image.save(filePath)  # save file image to the file path

    def clear(self):
        self.image.fill(Qt.GlobalColor.white)  # fill the image with white
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    # open a file
    def open(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "","PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if not file is selected exit
            return
        with open(filePath, 'rb') as f:  # open the file in binary mode for reading
            content = f.read()  # read the file
        self.image.loadFromData(content)  # load the data into the file
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)  # scale the image from file and put it in your QImage
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    # exit
    def exit(self):
        QApplication.instance().closeAllWindows()


    def rule(self): # show the rules
        ruleBox = QMessageBox()
        ruleBox.setWindowIcon(QIcon("./icons/rule.png"))
        ruleBox.setIcon(QMessageBox.Icon.Information)
        ruleBox.setWindowTitle("Rules")
        ruleBox.setText("Rules")
        ruleBox.setInformativeText("1. First to reach 5 points to win\n\n"
                                   "2. When Guesser get the answer, 2 points for guesser and 1 point for drawer\n\n"
                                   "3. Only 3 chances for guesser to guess \n\n"
                                   "4. Drawer can skip turn anytime")
        ruleBox.setStandardButtons(QMessageBox.StandardButton.Ok)

        ruleBox.exec()

    def threepx(self):  # the brush size is set to 3
        self.brushSize = 3

    def fivepx(self):
        self.brushSize = 5

    def sevenpx(self):
        self.brushSize = 7

    def ninepx(self):
        self.brushSize = 9

    def black(self):  # the brush color is set to black
        self.brushColor = Qt.GlobalColor.black

    def red(self):
        self.brushColor = Qt.GlobalColor.red

    def green(self):
        self.brushColor = Qt.GlobalColor.green

    def yellow(self):
        self.brushColor = Qt.GlobalColor.yellow

    def white(self):
        self.brushColor = Qt.GlobalColor.white

    def rectangle(self): # drawing rectangle
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine))
        rect = QRect(self.startPoint, self.lastPoint)
        painter.drawRect(rect)
        self.update()

    def circle(self): # drawing circle
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine))
        radius = (self.startPoint - self.lastPoint).manhattanLength() // 2
        center = (self.startPoint + self.lastPoint) / 2
        painter.drawEllipse(center, radius, radius)
        self.update()

    def fillCanvas(self): # fill whole background
        self.image.fill(self.brushColor)
        self.update()

    def startGame(self):
        # check if the second window is already open
        if self.startDetail is None:
            self.startDetail = StartDetail(self.self_obj)
            self.startDetail.show()

        # bring the window to the front if it's already open
        elif not self.startDetail.isVisible():
            self.startDetail.show()
        else:
            self.startDetail.raise_()

    #Get a random word from the list read from file
    def getWord(self):
        randomWord = random.choice(self.wordList)
        game_center.word = randomWord
        print(game_center.word)
        return randomWord

    #read word list from file
    def getList(self):
        with open(game_center.mode + 'mode.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                self.wordList = row
                line_count += 1

# window then user click start button
class StartDetail(QMainWindow):
    modeChanged = pyqtSignal(str) # signal

    def __init__(self, pictionary):
        super().__init__()
        self.p = pictionary
        self.modeChanged.connect(self.p.updateUI)
        self.setWindowTitle("Start Detail")

        font = QFont("Arial", 24, QFont.Weight.Bold) # font style

        # set the icon
        self.setWindowIcon(QIcon("./icons/start.png"))

        self.self_obj = self

        # centralize my widget
        central = QWidget()
        self.setCentralWidget(central)

        # setting button
        easy = QPushButton("Easy")
        easy.setFixedSize(200,100)
        easy.setFont(font)
        easy.clicked.connect(self.easy)
        hard = QPushButton("Hard")
        hard.setFixedSize(200, 100)
        hard.setFont(font)
        hard.clicked.connect(self.hard)

        layout = QVBoxLayout()

        layout.addWidget(easy)
        layout.addWidget(hard)

        layout.addStretch(1)

        central.setLayout(layout)

    def easy(self):
        self.setupGame("Easy")

    def hard(self):
        self.setupGame("Hard")

    def setupGame(self, difficulty):
        game_center.mode = difficulty.lower()
        game_center.turn = 1
        game_center.score1 = 0
        game_center.score2 = 0
        self.modeChanged.emit(game_center.mode)  # connect the signal

        self.wordDetail = WordDisplay(self.p)
        self.wordDetail.show()
        self.answerBox = AnsSheet(self.wordDetail, self.p, self.self_obj)
        self.answerBox.show()

        self.close()

class WordDisplay(QMainWindow): # class to display the word for drawer
    turnChange = pyqtSignal(int) # signal

    def __init__(self, pictionary):
        super().__init__()

        self.p = pictionary # assign class
        self.turnChange.connect(self.p.updateUI) # connect method

        font1 = QFont("Comic Sans MS", 15) # font style
        font2 = QFont("Courier New", 12)  # font style

        self.setWindowTitle("Word Detail")

        # set the icon
        self.setWindowIcon(QIcon("./icons/word.png"))

        # centralize my widget
        central = QWidget()
        self.setCentralWidget(central)

        self.move(200,400) # generate on left

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        self.updatePlayerInfo()

        self.player = QLabel(f"{self.activePlayer} Turn, please get your word and draw") # show current player who need to draw
        self.player.setFont(font1)
        self.warning = QLabel(f"{self.warningPlayer} is not allow to watch!!")
        self.warning.setFont(font1)
        self.warning.setStyleSheet("color: red;")
        self.p = PictionaryGame()
        self.p.getList()  # get the list
        self.currentWord = self.p.getWord()
        self.wordLabel = QLabel("Current Word: *********")
        self.wordLabel.setFont(font2)
        self.showButton = QPushButton("Show Word") # method for hiding the word
        self.showButton.pressed.connect(self.wordShow)
        self.showButton.released.connect(self.wordHiding)
        skipTurn = QPushButton("Skip Turn")
        skipTurn.clicked.connect(self.nextTurn)
        hlayout.addWidget(self.showButton)
        hlayout.addWidget(skipTurn)

        layout.addWidget(self.player)
        layout.addSpacing(10)
        layout.addWidget(self.warning)
        layout.addSpacing(30)
        layout.addWidget(self.wordLabel)
        layout.addSpacing(10)
        layout.addLayout(hlayout)
        layout.addStretch(1)

        central.setLayout(layout)

    def wordHiding(self):
        self.wordLabel.setText("Current Word: *********")

    def wordShow(self):
        self.wordLabel.setText(f"Current Word: {self.currentWord}")

    def nextTurn(self):
        game_center.turn += 1
        self.turnChange.emit(game_center.turn)
        self.updateUI()
        print(game_center.turn)

    def updatePlayerInfo(self):
        if  game_center.turn % 2 == 1:
            self.activePlayer = "Player 1"
            self.warningPlayer = "Player 2"
        else:
            self.activePlayer = "Player 2"
            self.warningPlayer = "Player 1"

    def updateUI(self):
        self.updatePlayerInfo()
        self.player.setText(f"{self.activePlayer} Turn, please get your word and draw")  # show current player who need to draw
        self.warning.setText(f"{self.warningPlayer} is not allow to watch!!")
        self.currentWord = self.p.getWord()
        self.wordLabel.setText("Current Word: *********")

class AnsSheet(QMainWindow): # class for the player to answer
    turnChange = pyqtSignal(int)

    def __init__(self, word_display, pictionary, start):
        super().__init__()
        self.w = word_display # class WordDisplay
        self.p = pictionary # class PictionaryGame
        self.s = start # class StartDetail
        self.turnChange.connect(self.w.updateUI) # connect signal to method
        self.turnChange.connect(self.p.updateUI)

        self.setWindowTitle("Answer")

        # set the icon
        self.setWindowIcon(QIcon("./icons/answer.png"))

        # centralize my widget
        central = QWidget()
        self.setCentralWidget(central)

        self.move(1400,400) # generate on right

        layout = QVBoxLayout()
        self.hlayout = QHBoxLayout()

        self.answerBox = QLineEdit()
        self.answerBox.setPlaceholderText("Enter your answer")

        submitButton = QPushButton("submit")
        submitButton.clicked.connect(self.ansChecking)

        self.ansCorrection = ""
        self.correctionLabel = QLabel(f"{self.ansCorrection}")

        self.chances = 3
        self.chanceLabel = QLabel("Chances: ")
        self.hlayout.addWidget(self.chanceLabel)

        # hp display
        self.iconPath = "./icons/hp.png"
        self.iconList = []
        self.updateUI("")

        layout.addWidget(self.answerBox)
        layout.addWidget(submitButton)
        layout.addSpacing(20)
        layout.addLayout(self.hlayout)
        layout.addSpacing(10)
        layout.addWidget(self.correctionLabel)

        central.setLayout(layout)

    def ansChecking(self):
        if self.answerBox.text().lower() == game_center.word.lower():
            self.ansCorrect()
            self.victoryChecking()
            self.nextTurn()
            self.answerBox.clear()
            self.chances = 3
            self.ansCorrection = "Correct Answer"
            self.updateUI("color: green;")
        else:
            if self.chances != 0:
                self.chances -=1
                self.answerBox.clear()
                self.ansCorrection = "Wrong Answer"
                self.updateUI("color: red;")
            else:
                self.chances = 3
                self.nextTurn()
                self.answerBox.clear()
                self.ansCorrection = "No chances"
                self.updateUI("color: red;")

    def updateUI(self, color):
        for icon in self.iconList: # clear list
            self.hlayout.removeWidget(icon)
            icon.deleteLater()
        self.iconList.clear()

        self.chanceLabel.setText("Chances: ")
        self.correctionLabel.setText(f"{self.ansCorrection}")
        self.correctionLabel.setStyleSheet(color)

        for i in range(self.chances):
            self.icon = QIcon(self.iconPath)
            self.pixmap = self.icon.pixmap(20, 20)  # size

            self.iconLabel = QLabel()
            self.iconLabel.setPixmap(self.pixmap)
            self.hlayout.addWidget(self.iconLabel)
            self.iconList.append(self.iconLabel)

    def ansCorrect(self):
        if game_center.turn % 2 == 1: # drawing player get 1 mark, answer player get 2 marks
            game_center.score1 += 1
            game_center.score2 += 2
        else:
            game_center.score1 += 2
            game_center.score2 += 1

    def nextTurn(self):
        game_center.turn += 1
        self.turnChange.emit(game_center.turn)
        print(game_center.turn)

    def victoryChecking(self):
        if game_center.score1 >= 5:
            self.v1 = Victory("Player 1", self.p)
            self.w.close()
            self.close()
            self.v1.show()
        elif game_center.score2 >= 5:
            self.v2 = Victory("Player 2", self.p)
            self.w.close()
            self.close()
            self.v2.show()

class Victory(QMainWindow):
    def __init__(self, winner, pictionary):
        super().__init__()
        self.p = pictionary

        self.setWindowTitle("Victory")

        # icon setting
        iconPath = "./icons/win.png"
        icon = QIcon(iconPath)
        pixmap = icon.pixmap(30, 30)  # size

        iconLabel = QLabel()
        iconLabel.setPixmap(pixmap)

        # set the icon
        self.setWindowIcon(QIcon("./icons/victory.png"))

        font = QFont("Comic Sans MS", 18) # font style

        # centralize my widget
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()

        victory = QLabel(f"{winner} Win")
        victory.setFont(font)

        hlayout.addWidget(iconLabel)
        hlayout.addWidget(victory)

        restart = QPushButton("Restart")
        restart.setFixedSize(200, 100)
        restart.setStyleSheet("font-size: 16px;")
        restart.clicked.connect(self.restart)

        exit = QPushButton("Exit")
        exit.setFixedSize(200, 100)
        exit.setStyleSheet("font-size: 16px;")
        exit.clicked.connect(self.exit)

        layout.addLayout(hlayout)
        layout.addSpacing(20)
        layout.addWidget(restart)
        layout.addWidget(exit)

        central.setLayout(layout)

    def restart(self):
        self.s = StartDetail(self.p)
        self.s.show()
        self.close()

    def exit(self):
        self.p.close()
        self.close()

if __name__ == "__main__":
    # predefine value
    game_center = GameCenter(mode="Waiting to Start", word="", turn=0, score1=0, score2=0)

    app = QApplication(sys.argv)
    window = PictionaryGame()
    window.show()
    app.exec()