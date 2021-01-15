# Chess
# Bill Wang
# Mr. Hunter
# 14/1/2020

from graphics import *
import random
import time

knight1 = [(1, 2), (-1, 2), (2, -1), (2, 1), (-2, 1), (-2, -1), (-1, -2), (1, -2)]
kingMoves = [(1, 1), (1, -1), (-1, -1), (-1, 1), (0, 1), (0, -1), (-1, 0), (1, 0)]
icons = {'White': {'P': '\u2659', 'R': '\u2656', 'B': '\u2657', 'N': '\u2658', 'K': '\u2654', 'Q': '\u2655'},
         'Black': {'P': '\u265F', 'R': '\u265C', 'B': '\u265D', 'N': '\u265E', 'K': '\u265A', 'Q': '\u265B'}}


def directional1(board, a, b, x, y, color):
    for i in range(1, 8):
        if 0 <= x + i * a < 8 and 0 <= y + i * b < 8:
            if board[x + i * a][y + i * b] is None:
                continue
            elif board[x + i * a][y + i * b].color != color:
                return x + i * a, y + i * b
            elif board[x + i * a][y + i * b].sname == 'K':
                continue
            else:
                return


def inCheck(x, y, color, board, isteam=None):
    for i in knight1:
        if 0 <= x + i[0] < 8 and 0 <= y + i[1] < 8 and board[x + i[0]][y + i[1]] is not None and board[x + i[0]][
            y + i[1]].color != color and board[x + i[0]][y + i[1]].sname == 'N':
            return True, x + i[0], y + i[1]
    for i in range(8):
        moves = []
        if i < 4:
            moves.append(directional1(board, kingMoves[i][0], kingMoves[i][1], x, y, color))
            for j in moves:
                if j is None:
                    continue
                elif board[j[0]][j[1]].sname == 'Q' or board[j[0]][j[1]].sname == 'B':
                    return True, j[0], j[1]
            moves = []
            if 0 <= x + kingMoves[i][0] < 8 and 0 <= y + kingMoves[i][1] < 8 and board[x + kingMoves[i][0]][
                y + kingMoves[i][1]] is not None and board[x + kingMoves[i][0]][
                y + kingMoves[i][1]].color != color and board[x + kingMoves[i][0]][
                y + kingMoves[i][1]].sname == 'P':
                if board[x + kingMoves[i][0]][y + kingMoves[i][1]].color == 'White':
                    if i >= 2:
                        return True, x + kingMoves[i][0], y + kingMoves[i][1]
                else:
                    if i < 2:
                        return True, x + kingMoves[i][0], y + kingMoves[i][1]
        else:
            moves.append(directional1(board, kingMoves[i][0], kingMoves[i][1], x, y, color))
            for j in moves:
                if j is None:
                    continue
                if board[j[0]][j[1]].sname == 'Q' or board[j[0]][j[1]].sname == 'R':
                    return True, j[0], j[1]
        if 0 <= x + kingMoves[i][0] < 8 and 0 <= y + kingMoves[i][1] < 8 and board[x + kingMoves[i][0]][
            y + kingMoves[i][1]] is not None and board[x + kingMoves[i][0]][
            y + kingMoves[i][1]].color != color and board[x + kingMoves[i][0]][
            y + kingMoves[i][1]].sname == 'K':
            if isteam is None:
                return True, x + kingMoves[i][0], y + kingMoves[i][1]
            return False, x, x
    return False, x, x


def clear(win):
    for item in win.items[:]:
        item.undraw()


def drawImage(win, x, y, f):
    P1 = Image(Point(x, y), f)
    P1.draw(win)


def drawRec(win, x, y, x2, y2, r, g, b, r2=None, g2=None, b2=None):
    R1 = Rectangle(Point(x, y), Point(x2, y2))
    R1.setFill(color_rgb(r, g, b))
    if r2 is not None:
        R1.setOutline(color_rgb(r2, g2, b2))
    R1.draw(win)


def drawCircle(win, x, y, rad, r, g, b, r2=None, b2=None, g2=None):
    C1 = Circle(Point(x, y), rad)
    C1.setFill(color_rgb(r, g, b))
    if r2 is not None:
        C1.setOutline(color_rgb(r2, g2, b2))
    C1.draw(win)


def drawText(win, x, y, text, c, size=None, style=None):
    T1 = Text(Point(x, y), text)
    T1.setTextColor(c)
    if size is not None:
        T1.setSize(size)
    if style is not None:
        T1.setStyle(style)
    T1.draw(win)


class Game:
    def __init__(self):
        self.pturn = "White"
        self.board = [[None for i in range(8)] for x in range(8)]
        self.pointS = {'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 0, 'Pass': 1}
        self.wPoints = 0
        self.bPoints = 0
        self.movesDone = 0
        self.startmoves = 0
        self.blackAI = False
        self.win = GraphWin("Chess", 620, 620, autoflush=False)
        self.titleScreen()

    def titleScreen(self):
        while True:
            self.blackAI = False
            self.startmoves = 0
            self.drawMainMenu()
            mouse = self.win.checkMouse()
            if mouse is not None:
                if 240 <= mouse.getX() <= 380 and 268 <= mouse.getY() <= 331:
                    self.blackAI = True
                    self.initializePieces(False)
                    self.initializeWindow(self.board)
                    self.main()
                elif 235 <= mouse.getX() <= 384 and 339 <= mouse.getY() <= 401:
                    self.initializePieces(False)
                    self.initializeWindow(self.board)
                    self.main()
                elif 213 <= mouse.getX() <= 405 and 415 <= mouse.getY() <= 465:
                    self.initializePieces(True)
                    self.initializeWindow(self.board)
                    self.main()
                elif 261 <= mouse.getX() <= 359 and 485 <= mouse.getY() <= 535:
                    self.showRules()

    def drawMainMenu(self):
        clear(self.win)
        drawImage(self.win, 310, 310, "background.png")
        drawImage(self.win, 310, 160, "chess.png")
        drawImage(self.win, 310, 300, "1P.png")
        drawImage(self.win, 310, 370, "2P.png")
        drawImage(self.win, 310, 440, "LD.png")
        drawImage(self.win, 310, 510, "rules.png")
        update(60)

    def showRules(self):
        self.win.bind_all("<MouseWheel>", self._on_mousewheel)
        while True:
            clear(self.win)
            drawImage(self.win, 310, 2410, 'rpicture.png')
            mouse = self.win.checkMouse()
            if mouse is not None:
                if 13 <= self.win.canvasx(mouse.getX()) <= 607 and 4745 <= self.win.canvasy(mouse.getY()) <= 4773:
                    break

        self.win.unbind_all("<MouseWheel>")
        self.win.xview_moveto(0)
        self.win.yview_moveto(0)
        self.titleScreen()

    def _on_mousewheel(self, event):
        self.win.configure(scrollregion=(0, 0, 620, 4800))
        self.win.yview_scroll(int(-1 * (event.delta / 120)), "units")
        update(60)

    def drawOptions(self):
        clear(self.win)
        drawImage(self.win, 310, 310, "background2.png")
        drawImage(self.win, 310, 100, "options.png")
        drawImage(self.win, 310, 250, "mainmenu.png")
        drawImage(self.win, 310, 350, "savegame.png")
        drawImage(self.win, 310, 450, "back.png")

    def options(self):
        self.drawOptions()
        e = 0
        r = 0
        while True:
            mouse = self.win.getMouse()
            if 160 <= mouse.getX() <= 460 and 220 <= mouse.getY() <= 280:
                e = 0
                self.drawOptions()
                update(60)
                drawText(self.win, 310, 560, "Warning! If GAME has not been saved, you will LOSE ALL PROGRESS.",
                         'White')
                drawText(self.win, 310, 580, "If this is what you want, press 'Main Menu' again.", 'White')
                r += 1
                if r == 2:
                    return 1
            elif 160 <= mouse.getX() <= 460 and 320 <= mouse.getY() <= 380:
                r = 0
                self.drawOptions()
                update(60)
                drawText(self.win, 310, 560, "Warning! Saving the game will override past save.",
                         'White')
                drawText(self.win, 310, 580, "If this is what you want, press 'Save' again.", 'White')

                e += 1
                if e == 2:
                    save = open("save.txt", "w")
                    for i in self.board:
                        for piece in i:
                            if piece is None:
                                save.write('x ')
                            elif piece.sname == 'Pass':
                                save.write('x ')
                            elif piece.color == 'White':
                                save.write('w' + piece.sname + ' ')
                            else:
                                save.write('b' + piece.sname + ' ')
                        save.write('\n')
                    save.write(self.pturn + ' ')
                    save.write(str(self.bPoints) + ' ')
                    save.write(str(self.wPoints) + ' ')
                    save.write(str(self.startmoves) + ' ')
                    save.write(str(self.blackAI))
                    save.close()
                    drawText(self.win, 310, 600, "Game Saved.", 'White')
                    update(60)
                    time.sleep(1)
                    self.options()
            elif 235 <= mouse.getX() <= 385 and 420 <= mouse.getY() <= 480:
                break

    def initializePieces(self, save):
        self.board = [[None for i in range(8)] for x in range(8)]
        if save is False:
            for i in range(8):
                self.board[1][i] = Pawn(Pawn, 'P', 'White', 1, i, True)
                self.board[6][i] = Pawn(Pawn, 'P', 'Black', 6, i, True)

            tempPiece = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
            tempsname = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

            for i in range(8):
                if tempsname[i] == 'R' or tempsname[i] == 'K':
                    self.board[0][i] = tempPiece[i](tempPiece[i], tempsname[i], 'White', 0, i, True)
                    self.board[7][i] = tempPiece[i](tempPiece[i], tempsname[i], 'Black', 7, i, True)
                else:
                    self.board[0][i] = tempPiece[i](tempPiece[i], tempsname[i], 'White', 0, i)
                    self.board[7][i] = tempPiece[i](tempPiece[i], tempsname[i], 'Black', 7, i)
            self.pturn = 'White'
        else:
            save = [i.strip('\n') for i in open('save.txt', 'r').readlines()]
            save = [i.split(' ') for i in save]
            pieceDict = {'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King, 'P': Pawn}
            colorDict = {'w': 'White', 'b': 'Black'}
            for x in range(8):
                for y in range(8):
                    if save[x][y] != 'x':
                        if save[x][y][1] == 'P' or save[x][y][1] == 'R' or save[x][y][1] == 'K':
                            self.board[x][y] = pieceDict[save[x][y][1]](pieceDict[save[x][y][1]], save[x][y][1],
                                                                        colorDict[save[x][y][0]], x, y, True)
                        else:
                            self.board[x][y] = pieceDict[save[x][y][1]](pieceDict[save[x][y][1]], save[x][y][1],
                                                                        colorDict[save[x][y][0]], x, y)
            self.pturn = save[8][0]
            self.bPoints = int(save[8][1])
            self.wPoints = int(save[8][2])
            self.startmoves = int(save[8][3])
            self.blackAI = save[8][4]
            if self.blackAI == 'True':
                self.blackAI = True
            else:
                self.blackAI = False

    def initializeWindow(self, board):
        clear(self.win)

        drawImage(self.win, 310, 310, "background2.png")
        drawRec(self.win, 100, 100, 520, 520, 120, 81, 169)
        drawImage(self.win, 30, 30, "option.png")

        for i in range(4):
            for j in range(4):
                # Black

                drawRec(self.win, 150 + 100 * i, 110 + 100 * j, 210 + 100 * i, 160 + 100 * j, 26, 17, 0)
                drawRec(self.win, 110 + 100 * i, 160 + 100 * j, 160 + 100 * i, 210 + 100 * j, 26, 17, 0)

                # White

                drawRec(self.win, 110 + 100 * i, 110 + 100 * j, 160 + 100 * i, 160 + 100 * j, 255, 230, 230)
                drawRec(self.win, 160 + 100 * i, 160 + 100 * j, 210 + 100 * i, 210 + 100 * j, 255, 230, 230)

        for row in board:
            for i in row:
                if i is not None and i.sname != 'Pass':
                    if i.color == 'Black':
                        drawCircle(self.win, 135 + 50 * i.y, 485 - 50 * i.x, 20, 0, 0, 0, 255, 255, 255)
                        drawText(self.win, 136 + 50 * i.y, 485 - 50 * i.x, icons[i.color][i.sname], "White", 25)
                    elif i.color == 'White':
                        drawCircle(self.win, 135 + 50 * i.y, 485 - 50 * i.x, 20, 255, 255, 255)
                        drawText(self.win, 136 + 50 * i.y, 485 - 50 * i.x, icons[i.color][i.sname], "Black", 25)

        alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in range(8):
            drawText(self.win, 85, 485 - 50 * i, i + 1, "White", None, "bold")
            drawText(self.win, 135 + 50 * i, 535, alpha[i], "White", None, "bold")

        update(60)

    def moveChange(self, moves, x, y):
        for i in moves:
            if self.board[i[0]][i[1]] is not None and self.board[i[0]][i[1]].sname != "Pass":
                drawRec(self.win, 120 + 50 * i[1], 470 - 50 * i[0], 150 + 50 * i[1], 500 - 50 * i[0], 230, 0, 0, 230, 0,
                        0)
            elif self.board[i[0]][i[1]] is not None and self.board[x][y].sname == 'P':
                drawRec(self.win, 120 + 50 * i[1], 470 - 50 * i[0], 150 + 50 * i[1], 500 - 50 * i[0], 230, 0, 0, 230, 0,
                        0)
            else:
                drawRec(self.win, 120 + 50 * i[1], 470 - 50 * i[0], 150 + 50 * i[1], 500 - 50 * i[0], 80, 54, 255, 80,
                        54, 255)
        if self.board[x][y].color == 'White':
            drawCircle(self.win, 135 + 50 * y, 485 - 50 * x, 20, 162, 148, 255)
            drawText(self.win, 136 + 50 * y, 485 - 50 * x,
                     icons[self.board[int(x)][int(y)].color][self.board[int(x)][int(y)].sname], "Black", 25)
        else:
            drawCircle(self.win, 135 + 50 * y, 485 - 50 * x, 20, 12, 17, 166, 255, 255, 255)
            drawText(self.win, 136 + 50 * y, 485 - 50 * x,
                     icons[self.board[int(x)][int(y)].color][self.board[int(x)][int(y)].sname], "White", 25)

    def changeTurn(self):
        return 'Black' if self.pturn == 'White' else 'White'

    def pieceEaten(self, x2, y2):
        if self.board[x2][y2] is not None:
            self.movesDone = 0
            if self.pturn == 'Black' and self.board[x2][y2].name != self.pturn:
                self.bPoints += self.pointS[self.board[x2][y2].sname]
            elif self.pturn == 'White' and self.board[x2][y2].name != self.pturn:
                self.wPoints += self.pointS[self.board[x2][y2].sname]

    def inPromotion(self, x2, y2):
        if self.board[x2][y2].sname == 'P' and (x2 == 7 or x2 == 0):
            if self.blackAI is True and self.pturn == 'Black':
                cp = random.randint(1, 4)
                if cp == 1:
                    self.board[x2][y2] = Rook(Rook, 'R', self.pturn, x2, y2, False)
                elif cp == 2:
                    self.board[x2][y2] = Queen(Queen, 'Q', self.pturn, x2, y2)
                elif cp == 3:
                    self.board[x2][y2] = Bishop(Bishop, 'B', self.pturn, x2, y2)
                else:
                    self.board[x2][y2] = Knight(Knight, 'N', self.pturn, x2, y2)
            else:
                drawText(self.win, 310, 560, "Promotion! Please choose a piece to promote to.", 'White')
                promotions = ['R', 'Q', 'B', 'N']
                for i in range(4):
                    if self.pturn == 'White':
                        drawCircle(self.win, 220 + i * 60, 595, 20, 255, 255, 255)
                        drawText(self.win, 221 + i * 60, 595, icons[self.pturn][promotions[i]], "Black", 25)
                    else:
                        drawCircle(self.win, 220 + i * 60, 595, 20, 0, 0, 0, 255, 255, 255)
                        drawText(self.win, 221 + i * 60, 595, icons[self.pturn][promotions[i]], "White", 25)

                while True:
                    mouse = self.win.getMouse()
                    if 200 <= mouse.getX() <= 240 and 575 <= mouse.getY() <= 615:
                        self.board[x2][y2] = Rook(Rook, 'R', self.pturn, x2, y2, False)
                        break
                    elif 260 <= mouse.getX() <= 300 and 575 <= mouse.getY() <= 615:
                        self.board[x2][y2] = Queen(Queen, 'Q', self.pturn, x2, y2)
                        break
                    elif 320 <= mouse.getX() <= 360 and 575 <= mouse.getY() <= 615:
                        self.board[x2][y2] = Bishop(Bishop, 'B', self.pturn, x2, y2)
                        break
                    elif 380 <= mouse.getX() <= 420 and 575 <= mouse.getY() <= 615:
                        self.board[x2][y2] = Knight(Knight, 'N', self.pturn, x2, y2)
                        break
                    else:
                        continue

    def checkEnemy(self, color):
        for row in self.board:
            for piece in row:
                if piece is not None and piece.sname == 'K' and piece.color == color:
                    king = piece
        if inCheck(king.x, king.y, king.color, self.board)[0] is False:
            return False
        return True

    def main(self):
        check = False
        self.movesDone = 0
        endGame = 0
        self.bPoints = 0
        self.wPoints = 0

        def move(x, y, x2, y2):
            self.movesDone += 1
            self.pieceEaten(x2, y2)
            if self.board[x2][y2] is not None and self.board[x2][y2].sname == 'Pass' and self.board[x][y].sname == 'P':
                self.board[x2 + self.board[x2][y2].color][y2] = None
            elif self.board[x2][y2] is not None and self.board[x2][y2].sname == 'Pass':
                if self.pturn == 'Black':
                    self.bPoints -= 1
                else:
                    self.wPoints -= 1
            if self.board[x][y].sname == 'P' or self.board[x][y].sname == 'K' or self.board[x][y].sname == 'R':
                if self.board[x][y].sname == 'P':
                    self.movesDone = 0
                    if x2 - x == 2:
                        self.board[x2 - 1][y2] = Pieces(self.pturn, 'Pass', 1, x2 - 1, y2)
                    elif x2 - x == -2:
                        self.board[x2 + 1][y2] = Pieces(self.pturn, 'Pass', -1, x2 + 1, y2)

                elif self.board[x][y].sname == 'K':
                    if y2 - y == 2:
                        rook = directional1(self.board, 0, 1, x, y, color)
                        self.board[x2][y2 - 1] = self.board[rook[0]][rook[1]].name(self.board[rook[0]][rook[1]].name,
                                                                                   self.board[rook[0]][rook[1]].sname,
                                                                                   self.board[rook[0]][rook[1]].color,
                                                                                   x2, y2 - 1, False)
                        self.board[rook[0]][rook[1]] = None
                    elif y2 - y == -2:
                        rook = directional1(self.board, 0, -1, x, y, color)
                        self.board[x2][y2 + 1] = self.board[rook[0]][rook[1]].name(self.board[rook[0]][rook[1]].name,
                                                                                   self.board[rook[0]][rook[1]].sname,
                                                                                   self.board[rook[0]][rook[1]].color,
                                                                                   x2, y2 + 1, False)
                        self.board[rook[0]][rook[1]] = None

                self.board[x2][y2] = self.board[x][y].name(self.board[x][y].name, self.board[x][y].sname,
                                                           self.board[x][y].color, x2, y2, False)
            else:
                self.board[x2][y2] = self.board[x][y].name(self.board[x][y].name, self.board[x][y].sname,
                                                           self.board[x][y].color, x2, y2)
            self.board[x][y] = None
            self.initializeWindow(self.board)
            self.inPromotion(x2, y2)
            print('White:', self.wPoints, 'Black:', self.bPoints)
            self.pturn = self.changeTurn()
            self.initializeWindow(self.board)

        def aiMove():
            PieceSquare = {'P': [[0, 0, 0, 0, 0, 0, 0, 0],
                                 [50, 50, 50, 50, 50, 50, 50, 50],
                                 [10, 10, 20, 30, 30, 20, 10, 10],
                                 [5, 5, 10, 25, 25, 10, 5, 5],
                                 [0, 0, 0, 20, 20, 0, 0, 0],
                                 [5, -5, -10, 0, 0, -10, -5, 5],
                                 [5, 10, 10, -20, -20, 10, 10, 5],
                                 [0, 0, 0, 0, 0, 0, 0, 0]],
                           'R': [[0, 0, 0, 0, 0, 0, 0, 0],
                                 [5, 10, 10, 10, 10, 10, 10, 5],
                                 [-5, 0, 0, 0, 0, 0, 0, -5],
                                 [-5, 0, 0, 0, 0, 0, 0, -5],
                                 [-5, 0, 0, 0, 0, 0, 0, -5],
                                 [-5, 0, 0, 0, 0, 0, 0, -5],
                                 [-5, 0, 0, 0, 0, 0, 0, -5],
                                 [0, 0, 0, 5, 5, 0, 0, 0]],
                           'B': [[-20, -10, -10, -10, -10, -10, -10, -20],
                                 [-10, 0, 0, 0, 0, 0, 0, -10],
                                 [-10, 0, 5, 10, 10, 5, 0, -10],
                                 [-10, 5, 5, 10, 10, 5, 5, -10],
                                 [-10, 0, 10, 10, 10, 10, 0, -10],
                                 [-10, 10, 10, 10, 10, 10, 10, -10],
                                 [-10, 5, 0, 0, 0, 0, 5, -10],
                                 [-20, -10, -10, -10, -10, -10, -10, -20]],
                           'N': [[-50, -40, -30, -30, -30, -30, -40, -50],
                                 [-40, -20, 0, 0, 0, 0, -20, -40],
                                 [-30, 0, 10, 15, 15, 10, 0, -30],
                                 [-30, 5, 15, 20, 20, 15, 5, -30],
                                 [-30, 0, 15, 20, 20, 15, 0, -30],
                                 [-30, 5, 10, 15, 15, 10, 5, -30],
                                 [-40, -20, 0, 5, 5, 0, -20, -40],
                                 [-50, -40, -30, -30, -30, -30, -40, -50]],
                           'Q': [[-20, -10, -10, -5, -5, -10, -10, -20],
                                 [-10, 0, 0, 0, 0, 0, 0, -10],
                                 [-10, 0, 5, 5, 5, 5, 0, -10],
                                 [-5, 0, 5, 5, 5, 5, 0, -5],
                                 [0, 0, 5, 5, 5, 5, 0, -5],
                                 [-10, 5, 5, 5, 5, 5, 0, -10],
                                 [-10, 0, 5, 0, 0, 0, 0, -10],
                                 [-20, -10, -10, -5, -5, -10, -10, -20]],
                           'K': [[-30, -40, -40, -50, -50, -40, -40, -30],
                                 [-30, -40, -40, -50, -50, -40, -40, -30],
                                 [-30, -40, -40, -50, -50, -40, -40, -30],
                                 [-30, -40, -40, -50, -50, -40, -40, -30],
                                 [-20, -30, -30, -40, -40, -30, -30, -20],
                                 [-10, -20, -20, -20, -20, -20, -20, -10],
                                 [20, 20, 0, 0, 0, 0, 20, 20],
                                 [20, 30, 10, 0, 0, 10, 30, 20]]}
            weight = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 100}

            if self.blackAI is True:
                eat = None
                eatPoints = 0
                piece = None
                if self.pturn == 'Black':
                    allMoves = {}
                    for row in self.board:
                        for piece in row:
                            if piece is not None and piece.color == 'Black':
                                if piece.pos_moves(self.board):
                                    allMoves[(piece.x, piece.y)] = piece.pos_moves(self.board)
                    for a in allMoves:
                        for j, w in allMoves[a]:
                            newPoints = -(PieceSquare[self.board[a[0]][a[1]].sname][a[0]][a[1]])
                            newPoints += (PieceSquare[self.board[a[0]][a[1]].sname][j][w])
                            if inCheck(a[0], a[1], 'Black', self.board)[0] is True:  # if current in check move
                                newPoints += weight[self.board[a[0]][a[1]].sname]
                            if self.board[j][w] is not None and self.board[j][w].sname != 'Pass':  # if move to kill, add kill value
                                newPoints += weight[self.board[j][w].sname] + 1
                                if inCheck(j, w, 'Black', self.board) is False: # if will not be in check from kill add
                                    newPoints += weight[self.board[j][w].sname] + 1
                            p1 = self.board[a[0]][a[1]]
                            p2 = self.board[j][w]
                            self.board[j][w] = p1
                            self.board[a[0]][a[1]] = None
                            selfCheck = inCheck(j, w, 'Black', self.board)
                            if selfCheck[0] is True:  # if piece die minus value
                                newPoints -= weight[p1.sname]
                            else:
                                newPoints += 50
                            teamCheck = inCheck(j, w, 'White', self.board)
                            if teamCheck[0] is True:  # check if piece is protected
                                newPoints += weight[p1.sname] ** 0.5
                                if self.checkEnemy('White') is True:  # check if move will check enemy
                                    newPoints += 300
                            self.board[j][w] = p2
                            self.board[a[0]][a[1]] = p1
                            if eatPoints <= newPoints:
                                eat = [j, w]
                                eatPoints = newPoints
                                piece = a
                    if self.startmoves <= 3:
                        x, y = random.choice([w for w in allMoves])
                        x2, y2 = random.choice(allMoves[x, y])
                        self.startmoves += 1
                    else:
                        x, y = piece
                        x2, y2 = eat[0], eat[1]

                    move(x, y, x2, y2)

        while True:
            if self.pturn == 'White':
                color = 'Black'
            else:
                color = 'White'
            moves = []
            for row in self.board:  # this loop checks for Check and checkmate
                for element in row:
                    if element is not None and element.sname == 'Pass':
                        if element.name == self.pturn:
                            self.board[element.x][element.y] = None
                    if element is not None and element.color == self.pturn and element.sname != 'Pass':
                        if element.pos_moves(self.board):
                            moves.append(element.pos_moves(self.board))
                    if element is not None and element.sname == 'K':
                        if inCheck(element.x, element.y, element.color, self.board)[0] is True:
                            check = True
                            element.canCastle = False
                            if moves:
                                pass
                            else:
                                drawText(self.win, 310, 60, "Checkmate. " + color + " wins!", 'White')
                                drawText(self.win, 310, 80, "Click to go to main menu!", 'White')
                                drawText(self.win, 310, 560, "Points (based on pieces captured):", 'White')
                                drawText(self.win, 310, 580,
                                         "White: " + str(self.wPoints) + ' Black: ' + str(self.bPoints), 'White')

                                self.win.getMouse()
                                endGame = 1
                            drawText(self.win, 310, 60, element.color + " is in check!", 'White')
                        else:
                            check = False
            if self.movesDone == 50 or moves == [] and check is False:
                drawText(self.win, 310, 60, "Stalemate", 'White')
                drawText(self.win, 310, 80, "Click to go to main menu!", 'White')
                drawText(self.win, 310, 560, "Points (based of pieces captured):", 'White')
                drawText(self.win, 310, 580, "White: " + str(self.wPoints) + ' Black: ' + str(self.bPoints), 'White')

                self.win.getMouse()
                endGame = 1
            if endGame == 1:
                break
            if self.blackAI is True and self.pturn == 'Black':
                aiMove()
            else:
                mouse = self.win.getMouse()
                x = int(8 - (mouse.getY() - 60) // 50)
                y = int((mouse.getX() - 60) // 50) - 1

                if -1 < x < 8 and -1 < y < 8 and self.board[x][y] is not None and self.pturn == self.board[x][y].color:
                    moves = self.board[x][y].pos_moves(self.board)
                    self.moveChange(moves, x, y)
                    mouse = self.win.getMouse()
                    x2 = int(8 - (mouse.getY() - 60) // 50)
                    y2 = int((mouse.getX() - 60) // 50) - 1
                    if (x2, y2) in moves:
                        check = False
                        move(x, y, x2, y2)
                        self.initializeWindow(self.board)
                    else:
                        self.initializeWindow(self.board)
                elif 6 <= mouse.getX() <= 52 and 5 <= mouse.getY() <= 51:
                    if self.options() == 1:
                        break
                    self.initializeWindow(self.board)


class Pieces:
    def __init__(self, name=None, sname=None, color=None, x=None, y=None):
        self.name = name
        self.sname = sname
        self.color = color
        self.x = x
        self.y = y

    def directional(self, moves, board, a, b):
        for i in range(1, 8):
            if 0 <= self.x + i * a < 8 and 0 <= self.y + i * b < 8:
                if self.moveInCheck(board, self.x, self.y, self.x + i * a, self.y + i * b) is False:
                    if board[self.x + i * a][self.y + i * b] is None:
                        moves.append((self.x + i * a, self.y + i * b))
                    elif board[self.x + i * a][self.y + i * b].sname == 'Pass':
                        moves.append((self.x + i * a, self.y + i * b))
                    elif board[self.x + i * a][self.y + i * b].color != self.color:
                        moves.append((self.x + i * a, self.y + i * b))
                        break
                    else:
                        break
                else:
                    break
        return

    def moveInCheck(self, board, x, y, x2, y2):
        for row in board:
            for piece in row:
                if piece is not None and piece.sname == 'K' and piece.color == self.color:
                    king = piece
        p1 = board[x][y]
        p2 = board[x2][y2]
        board[x2][y2] = p1
        board[x][y] = None
        if inCheck(king.x, king.y, king.color, board)[0] is False:
            board[x2][y2] = p2
            board[x][y] = p1
            return False
        board[x2][y2] = p2
        board[x][y] = p1
        return True


class Pawn(Pieces):
    def __init__(self, name, sname, color, x, y, fTurn):
        super().__init__(name, sname, color, x, y)
        self.fTurn = fTurn

    def pos_moves(self, board):
        moves = []
        if self.color == 'White':
            d = 1
        else:
            d = -1
        for i in range(1, 3):
            if 0 <= self.x + (d * i) < 8 and 0 <= self.y < 8 and board[self.x + (d * i)][
                self.y] is None and self.moveInCheck(board, self.x, self.y, self.x + (d * i), self.y) is False:
                if self.fTurn is True or i == 1:
                    moves.append((self.x + (d * i), self.y))
            else:
                break
        if 0 <= self.x + d < 8 and 0 <= self.y + d < 8 and self.moveInCheck(board, self.x, self.y, self.x + d,
                                                                            self.y + d) is False:
            if board[self.x + d][self.y + d] is not None and board[self.x + d][self.y + d].name != self.color and \
                    (board[self.x + d][self.y + d].sname == 'Pass' or board[self.x + d][
                        self.y + d].color != self.color):
                moves.append((self.x + d, self.y + d))
        if 0 <= self.x + d < 8 and 0 <= self.y - d < 8 and self.moveInCheck(board, self.x, self.y, self.x + d,
                                                                            self.y - d) is False:
            if board[self.x + d][self.y - d] is not None and board[self.x + d][self.y - d].name != self.color and \
                    (board[self.x + d][self.y - d].sname == 'Pass' or board[self.x + d][
                        self.y - d].color != self.color):
                moves.append((self.x + d, self.y - d))

        return moves


class Rook(Pieces):

    def __init__(self, name, sname, color, x, y, canCastle):
        super().__init__(name, sname, color, x, y)
        self.canCastle = canCastle

    def pos_moves(self, board):
        moves = []
        super().directional(moves, board, 1, 0)
        super().directional(moves, board, -1, 0)
        super().directional(moves, board, 0, 1)
        super().directional(moves, board, 0, -1)
        return moves


class Knight(Pieces):
    def __init__(self, name, sname, color, x, y):
        super().__init__(name, sname, color, x, y)

    def pos_moves(self, board):
        moves = []
        for i in knight1:
            if 0 <= self.x + i[0] < 8 and 0 <= self.y + i[1] < 8 and board[self.x + i[0]][
                self.y + i[1]] is None and self.moveInCheck(board, self.x, self.y, self.x + i[0],
                                                            self.y + i[1]) is False:
                moves.append((self.x + i[0], self.y + i[1]))
            elif 0 <= self.x + i[0] < 8 and 0 <= self.y + i[1] < 8 and board[self.x + i[0]][
                self.y + i[1]] is not None and board[self.x + i[0]][
                self.y + i[1]].color != self.color and self.moveInCheck(board, self.x, self.y, self.x + i[0],
                                                                        self.y + i[1]) is False:
                moves.append((self.x + i[0], self.y + i[1]))
        return moves


class Bishop(Pieces):
    def __init__(self, name, sname, color, x, y):
        super().__init__(name, sname, color, x, y)

    def pos_moves(self, board):
        moves = []
        super().directional(moves, board, 1, 1)
        super().directional(moves, board, 1, -1)
        super().directional(moves, board, -1, 1)
        super().directional(moves, board, -1, -1)
        return moves


class Queen(Pieces):
    def __init__(self, name, sname, color, x, y):
        super().__init__(name, sname, color, x, y)

    def pos_moves(self, board):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                else:
                    super().directional(moves, board, i, j)
        return moves


class King(Pieces):
    def __init__(self, name, sname, color, x, y, canCastle):
        super().__init__(name, sname, color, x, y)
        self.canCastle = canCastle

    def pos_moves(self, board):
        moves = []
        for i in kingMoves:
            if 0 <= self.x + i[0] < 8 and 0 <= self.y + i[1] < 8 and board[self.x + i[0]][self.y + i[1]] is None:
                if inCheck(self.x + i[0], self.y + i[1], self.color, board)[0] is False:
                    moves.append((self.x + i[0], self.y + i[1]))
            elif 0 <= self.x + i[0] < 8 and 0 <= self.y + i[1] < 8 and board[self.x + i[0]][
                self.y + i[1]] is not None and board[self.x + i[0]][self.y + i[1]].color != self.color:
                if inCheck(self.x + i[0], self.y + i[1], self.color, board)[0] is False:
                    moves.append((self.x + i[0], self.y + i[1]))
        if self.canCastle:
            if self.color == 'White':
                color = 'Black'
            else:
                color = 'White'
            rook = directional1(board, 0, 1, self.x, self.y, color)
            if rook is not None and board[rook[0]][rook[1]].sname == 'R' and board[rook[0]][rook[1]].canCastle is True:
                if inCheck(self.x, self.y + 2, self.color, board)[0] is False:
                    moves.append((self.x, self.y + 2))
            rook = directional1(board, 0, -1, self.x, self.y, color)
            if rook is not None and board[rook[0]][rook[1]].sname == 'R' and board[rook[0]][rook[1]].canCastle is True:
                if inCheck(self.x, self.y - 2, self.color, board)[0] is False:
                    moves.append((self.x, self.y - 2))
        return moves


Game()
