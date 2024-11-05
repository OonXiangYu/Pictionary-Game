from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QDockWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtGui import QIcon, QPainter, QPen, QAction, QPixmap, QFont
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
import sys
import csv, random

# constructor, getter, setter
class GameCenter:
    def __init__(self, mode, word, turn, score1, score2, isGameActive):
        self._mode = mode
        self._word = word
        self._turn = turn
        self._score1 = score1
        self._score2 = score2
        self._isGameActive = isGameActive

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

    @property
    def isGameActive(self):
        return self._isGameActive

    @isGameActive.setter
    def isGameActive(self, active_status):
        self._isGameActive = active_status

class PictionaryGame(QMainWindow):
    '''
    Painting Application class
    '''

    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("Pictionary Game")

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

        # reference to last point recorded by mouse
        self.lastPoint = QPoint()

        # set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(" File")
        brushSizeMenu = mainMenu.addMenu(" Brush Size")
        brushColorMenu = mainMenu.addMenu(" Brush Colour")

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
        self.vbdock.addWidget(QPushButton("Skip Turn"))

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

    # event handlers
    def mousePressEvent(self, event):  # when the mouse is pressed
        if event.button() == Qt.MouseButton.LeftButton:  # if the pressed button is the left button
            self.drawing = True  # enter drawing mode
            self.lastPoint = event.pos()  # save the location of the mouse press as the lastPoint
            print(self.lastPoint)  # print the lastPoint for debugging purposes

    def mouseMoveEvent(self, event):  # when the mouse is moved
        if self.drawing:
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type.
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())  # draw a line from the point of the oroiginal press to the point to where the mouse was dragged to
            self.lastPoint = event.pos()  # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
            self.update()  # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(self, event):  # when the mouse is released
        if event.button() == Qt.MouseButton.LeftButton:  # if the released button is the left button
            self.drawing = False  # exit drawing mode

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(self)  # create a new QPainter object
        canvasPainter.drawPixmap(QPoint(), self.image)  # draw the image

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

    def black(self):
        self.brushColor = Qt.GlobalColor.black

    def red(self):
        self.brushColor = Qt.GlobalColor.red

    def green(self):
        self.brushColor = Qt.GlobalColor.green

    def yellow(self):
        self.brushColor = Qt.GlobalColor.yellow

    def startGame(self):
        # check if the second window is already open
        if self.startDetail is None:
            self.startDetail = StartDetail()
            self.startDetail.modeChanged.connect(self.onModeChanged)
            self.startDetail.show()

        # bring the window to the front if it's already open
        elif not self.startDetail.isVisible():
            self.startDetail.show()
        else:
            self.startDetail.raise_()

    def onModeChanged(self, new_mode):
        game_center.mode = new_mode
        self.updateUI()

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

# window then user click start button
class StartDetail(QMainWindow):
    modeChanged = pyqtSignal(str) # signal

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Start Detail")

        # centralize my widget
        central = QWidget()
        self.setCentralWidget(central)

        # setting button
        easy = QPushButton("Easy")
        easy.setFixedSize(200,100)
        easy.setStyleSheet("font-size: 16px;")
        easy.clicked.connect(self.easy)
        hard = QPushButton("Hard")
        hard.setFixedSize(200, 100)
        hard.setStyleSheet("font-size: 16px;")
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
        newMode = difficulty.lower()
        game_center.turn = 1
        game_center.score1 = 0
        game_center.score2 = 0
        self.modeChanged.emit(newMode)  # connect the signal

        if not game_center.isGameActive:
            self.wordDetail = WordDisplay()
            self.wordDetail.show()
            game_center.isGameActive = True

        self.close()


class WordDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word Detail")
        # centralize my widget
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        if  game_center.turn % 2 == 1:
            self.activePlayer = "Player 1"
            self.warningPlayer = "Player 2"
        else:
            self.activePlayer = "Player 2"
            self.warningPlayer = "Player 1"
        player = QLabel(f"{self.activePlayer} Turn, please get your word and draw") # show current player who need to draw
        warning = QLabel(f"{self.warningPlayer} is not allow to watch!!")
        warning.setStyleSheet("color: red;")
        layout.addWidget(player)
        layout.addSpacing(10)
        layout.addWidget(warning)
        layout.addSpacing(30)
        p = PictionaryGame()
        p.getList() # get the list
        currentWord = p.getWord()
        wordLabel = QLabel(f"Current Word: {currentWord}")
        layout.addWidget(wordLabel)
        layout.addStretch(1)

        central.setLayout(layout)

if __name__ == "__main__":
    # predefine value
    game_center = GameCenter(mode="Waiting to Start", word="", turn=0, score1=0, score2=0, isGameActive=False)

    app = QApplication(sys.argv)
    window = PictionaryGame()
    window.show()
    app.exec()