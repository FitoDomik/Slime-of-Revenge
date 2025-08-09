import pygame
import math
import sys
import ast
import os
from win32api import GetSystemMetrics
pygame.font.init()

lol = os.path.dirname(os.path.abspath(__file__))
# directory = lol+"/maps"
# files = os.listdir(directory)

WIDTH = 889
HEIGHT = 500
# цвета
BLACK = (0, 0, 0)
BLUE = (71, 153, 192)
WHITE = (225, 225, 225)
GREEN = (50, 150, 50)
GREEN2 = (150, 220, 150)
GREEN_d = (2, 199, 143)
GREEN_d2 = (151, 204, 190)
PURPLE = (171, 100, 237)
PURPLE2 = (192, 181, 196)
colorGG = GREEN
colorGG2 = GREEN2
menuColor = (33, 57, 94)
# цвета для заднего фона
backRED = (163, 95, 95)
backGREEN = (54, 64, 40)
backGRAY = (158, 158, 158)
backBROWN = (115, 91, 76)
backYELLOW = (184, 183, 141)
backPURPLE = (196, 183, 201)
backColor = [backRED, backGREEN, backGRAY, backBROWN, backYELLOW, backPURPLE]
createColor = backColor[0]
# шрифты
font = pygame.font.SysFont("Calibri", 23, 1)
menuFont = pygame.font.SysFont("Calibri", 20, 1)
fontMENU = pygame.font.SysFont("Calibri", 50, 1)
# хз
minY = HEIGHT-50

# корды
TrueX = WIDTH//2
TrueY = HEIGHT//2
x = TrueX
y = TrueY
spawnX = x
spawnY = y
xO = x
yO = y
surfX = 0
surfY = 0
spawnSX = surfX
spawnSY = surfY
mouseX = 0
mouseY = 0
firstMouseX = 0
firstMouseY = 0
# блоки
map = {"block": [[], [], [], []], "spikes": [[], [], [], []], "spring": [[], [], [], []],
       "rollback": [[], [], 8, 8, []], "background": [[], [], [], [], []], "spawnpoint": [[], [], 20, 20, -1]}
'''
with open('map.txt', 'r') as file:
    text = file.read()
map = ast.literal_eval(text)
'''
letMap = "none"
createType = "block"
correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [], "background": [], "spawnpoint": []}
draw = 0
# размеры
Size = 21*4
pixel = 3
surf = 34
# действия
motionU = "stop"
motionD = "stop"
motionL = "stop"
motionR = "stop"
jump = "stop"
jumpWallL = "stop"
jumpWallR = "stop"
dash = "stop"
# направления
lastButton = "right"
NDash = lastButton
# коэффициенты
kG = 0.81
# скорости
maxSpeed = 4
speed = 0
J = 10 * math.sqrt(kG)
SpringJ = 15 * math.sqrt(kG)
speedJ = J
maxSpeedG = 10
speedG = 0
speedSX = 0
speedSY = 0
speedDash = 10
# ускорения
g = 0.5 * kG
surfG = 0.4
# вспомогательные
grav = 1
canJump = False
canJumpWallL = False
canJumpWallR = False
canDash = False
gameMode = "surv"
stopRun = 0
spring = 0
# таймеры
maxTimeDash = 15
timeDash = 0
timeRollback = 600
# меню
menu = "menu"
buttonMenu = ["Ластик", "Копировать", "Вставить", "Сохранить", "Проверить",  "Выйти"]
canCreate = False
# клавиши
UP = pygame.K_w
DOWN = pygame.K_s
LEFT = pygame.K_a
RIGHT = pygame.K_d
JUMP = pygame.K_SPACE
DASH = pygame.K_RSHIFT
gameButton = ""

FPS = 60
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen0 = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
current_size = (GetSystemMetrics(0), GetSystemMetrics(1))
print(current_size)
screen = pygame.Surface((WIDTH, HEIGHT))
screen0 = pygame.display.set_mode(current_size)
k_posX = WIDTH/GetSystemMetrics(0)
k_posY = HEIGHT/GetSystemMetrics(1)
fullScreen = False

anime = [[[], [], []]]
copyAnime = "none"
cadr = 0
x = WIDTH//2-Size//2
y = HEIGHT//2-Size//2
R = 0
G = 0
B = 0
RGB = [["R", R], ["G", G], ["B", B]]
drawColor = (RGB[0][1], RGB[1][1], RGB[2][1])
pen = True
play = False
timeCadr = 0
second = 1
hitbox = True
N = input()
if N != "":
    with open('textures/' + N, 'r') as file:
        text1 = file.readline()
        anime = ast.literal_eval(text1)
        try:
            text2 = file.readline()
            second = ast.literal_eval(text2)
        except:
            pass
def list_deepcopy(l):
    return [
        elem if not isinstance(elem, list) else list_deepcopy(elem)
        for elem in l
    ]

lastMenuButton = ""
clock = pygame.time.Clock()
while True:
    screen.fill(menuColor)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                pygame.quit()
            if i.key == pygame.K_DELETE:
                if len(anime) > 1:
                    anime.pop(cadr)
                    if cadr != 0:
                        cadr -= 1
            if i.key == 61:
                if cadr+1 == len(anime):
                    cadr = 0
                else:
                    cadr += 1
            if i.key == pygame.K_p:
                anime.insert(cadr+1, list_deepcopy(anime[cadr]))
                cadr += 1
            if i.key == pygame.K_h:
                hitbox = not hitbox
            if i.key == 45:
                if cadr > 0:
                    cadr -= 1
                else:
                    cadr = len(anime)-1
            if i.key == pygame.K_F11:
                if fullScreen:
                    screen0 = pygame.display.set_mode(current_size)
                else:
                    screen0 = pygame.display.set_mode((current_size), pygame.FULLSCREEN)
                fullScreen = not fullScreen
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                if pen:
                    if i.pos[0] * k_posX > 150 and i.pos[0] * k_posX < WIDTH-100:
                        if len(anime[cadr][0]) == 0:
                            anime[cadr][0].append(int(i.pos[0] * k_posX - x) // 4 - int(i.pos[0] * k_posX - x) // 4 % pixel)
                            anime[cadr][1].append(int(i.pos[1] * k_posY - y) // 4 - int(i.pos[1] * k_posY - y) // 4 % pixel)
                            anime[cadr][2].append(drawColor)
                        FlagA = 0
                        for j in range(len(anime[cadr][0])):
                            if int(i.pos[0] * k_posX - x) // 4 - int(i.pos[0] * k_posX - x) // 4 % pixel == anime[cadr][0][j] \
                                    and int(i.pos[1] * k_posY - y) // 4 - int(i.pos[1] * k_posY - y) // 4 % pixel == anime[cadr][1][j]:
                                anime[cadr][2][j] = drawColor
                                print(anime)
                                FlagA = 1
                                break
                        if FlagA == 0:
                            anime[cadr][0].append(int(i.pos[0] * k_posX - x)//4 - int(i.pos[0] * k_posX - x)//4 % pixel)
                            anime[cadr][1].append(int(i.pos[1] * k_posY - y)//4 - int(i.pos[1] * k_posY - y)//4 % pixel)
                            anime[cadr][2].append(drawColor)
                            print(anime)
                else:
                    for j in range(len(anime[cadr][0])):
                        if int(i.pos[0] * k_posX - x) // 4 - int(i.pos[0] * k_posX - x) // 4 % pixel == anime[cadr][0][j] \
                                and int(i.pos[1] * k_posY - y) // 4 - int(i.pos[1] * k_posY - y) // 4 % pixel == anime[cadr][1][j]:
                            anime[cadr][0].pop(j)
                            anime[cadr][1].pop(j)
                            anime[cadr][2].pop(j)
                            print(anime)
                            break
            if i.button == 3:
                for j in range(len(anime[cadr][0])):
                    if int(i.pos[0] * k_posX - x) // 4 - int(i.pos[0] * k_posX - x) // 4 % pixel == anime[cadr][0][j] \
                            and int(i.pos[1] * k_posY - y) // 4 - int(i.pos[1] * k_posY - y) // 4 % pixel == anime[cadr][1][j]:
                        drawColor = anime[cadr][2][j]
                        RGB[0][1] = anime[cadr][2][j][0]
                        RGB[1][1] = anime[cadr][2][j][1]
                        RGB[2][1] = anime[cadr][2][j][2]
                        pass
            if i.button == 4:
                for j in range(len(RGB)):
                    for j in range(len(RGB)):
                        text = menuFont.render(RGB[j][0] + ": " + str(RGB[j][1]), 1, WHITE)
                        if i.pos[0] * k_posX > WIDTH - 5 - textCadr.get_width() \
                                and i.pos[0] * k_posX < WIDTH - 5 - textCadr.get_width() + text.get_width() \
                                and i.pos[1] * k_posY > 10 + textCadr.get_width() + textCadr.get_height() + text.get_height() * j \
                                and i.pos[1] * k_posY < 10 + textCadr.get_width() + textCadr.get_height() + text.get_height() * j + text.get_height() - 5:
                            if RGB[j][1] < 255:
                                RGB[j][1] += 5
                                drawColor = (RGB[0][1], RGB[1][1], RGB[2][1])
                textSecond = menuFont.render("sec: " + str(second), 1, WHITE)
                if i.pos[0] * k_posX > WIDTH - 5 - textCadr.get_width() \
                        and i.pos[0] * k_posX < WIDTH - 5 - textCadr.get_width() + textSecond.get_width() \
                        and i.pos[1] * k_posY > 10 + textCadr.get_width() + textCadr.get_height() + textSecond.get_height() * (j + 1) \
                        and i.pos[1] * k_posY < 10 + textCadr.get_width() + textCadr.get_height() + textSecond.get_height() * (j + 1) + textSecond.get_height() - 5:
                    second += 0.25
            if i.button == 5:
                for j in range(len(RGB)):
                    text = menuFont.render(RGB[j][0] + ": " + str(RGB[j][1]), 1, WHITE)
                    if i.pos[0] * k_posX > WIDTH - 5 - textCadr.get_width() \
                            and i.pos[0] * k_posX < WIDTH - 5 - textCadr.get_width() + text.get_width() \
                            and i.pos[1] * k_posY > 10 + textCadr.get_width() + textCadr.get_height() + text.get_height() * j \
                            and i.pos[1] * k_posY < 10 + textCadr.get_width() + textCadr.get_height() + text.get_height() * j + text.get_height() - 5:
                        if RGB[j][1] > 0:
                            RGB[j][1] -= 5
                            drawColor = (RGB[0][1], RGB[1][1], RGB[2][1])
                textSecond = menuFont.render("second: " + str(second), 1, WHITE)
                if i.pos[0] * k_posX > WIDTH - 5 - textCadr.get_width() \
                        and i.pos[0] * k_posX < WIDTH - 5 - textCadr.get_width() + textSecond.get_width() \
                        and i.pos[1] * k_posY > 10 + textCadr.get_width() + textCadr.get_height() + textSecond.get_height() * (j + 1) \
                        and i.pos[1] * k_posY < 10 + textCadr.get_width() + textCadr.get_height() + textSecond.get_height() * (j + 1) + textSecond.get_height() - 5:
                    if second > 0.25:
                        second -= 0.25
        if i.type == pygame.MOUSEMOTION:
            mouseX = i.pos[0] * k_posX
            mouseY = i.pos[1] * k_posY
        if i.type == pygame.MOUSEBUTTONUP:
            if i.button == 1:
                for j in range(len(buttonMenu)):
                    text = menuFont.render(buttonMenu[j], 1, WHITE)
                    if i.pos[0] * k_posX > 5 \
                            and i.pos[0] * k_posX <5+text.get_width() \
                            and i.pos[1] * k_posY > 5+j*(text.get_height()+5)+5 \
                            and i.pos[1] * k_posY < 5 + j * (text.get_height() + 5) + text.get_height()-5:
                        if buttonMenu[j] == "Выйти":
                            pygame.quit()
                        elif buttonMenu[j] == "Сохранить":
                            print("ИТОГ:", anime)
                        elif buttonMenu[j] == "Проверить":
                            buttonMenu = ["Ластик", "Копировать", "Вставить", "Сохранить", "Стоп", "Выйти"]
                            play = True
                            pen = True
                        elif buttonMenu[j] == "Стоп":
                            buttonMenu = ["Ластик", "Копировать", "Вставить", "Сохранить", "Проверить", "Выйти"]
                            play = False
                            pen = True
                            timeCadr = 0
                        elif buttonMenu[j] == "Ластик":
                            pen = False
                            buttonMenu = ["Ручка", "Копировать", "Вставить", "Сохранить", "Проверить", "Выйти"]
                        elif buttonMenu[j] == "Ручка":
                            pen = True
                            buttonMenu = ["Ластик", "Копировать", "Вставить", "Сохранить", "Проверить",  "Выйти"]
                        elif buttonMenu[j] == "Копировать":
                            copyAnime = list_deepcopy(anime[cadr])
                            print(list_deepcopy(anime[cadr]))
                        elif buttonMenu[j] == "Вставить":
                            if copyAnime != "none":
                                anime[cadr] = list_deepcopy(copyAnime)
                                print(anime[cadr])
    if play:
        timeCadr += 1
        if timeCadr == FPS*second // len(anime):
            if cadr + 1 < len(anime):
                cadr += 1
            else:
                cadr = 0
            timeCadr = 0
    for i in range(len(buttonMenu)):
        colorButton = WHITE
        text = menuFont.render(buttonMenu[i], 1, colorButton)
        if mouseX > 5 \
                and mouseX < 5 + text.get_width() \
                and mouseY > 5 + i * (text.get_height() + 5) +5 \
                and mouseY < 5 + i * (text.get_height() + 5) + text.get_height() -5:
            if lastMenuButton != buttonMenu[i]:
                lastMenuButton = buttonMenu[i]
            colorButton = (255, 0, 0)
        text = menuFont.render(buttonMenu[i], 1, colorButton)
        screen.blit(text, (5, 5+i*(text.get_height()+5)))
    textCadr = menuFont.render("cadr: " + str(cadr+1) + "/" + str(len(anime)), 1, WHITE)
    screen.blit(textCadr, (WIDTH-5-textCadr.get_width(), 5))
    pygame.draw.rect(screen, drawColor, (WIDTH-5-textCadr.get_width(), textCadr.get_height()+5, textCadr.get_width(), textCadr.get_width()))
    if pen == False:
        pygame.draw.line(screen, pygame.Color("red"), (WIDTH - 5 - textCadr.get_width(), textCadr.get_height() + 5), (WIDTH - 5, textCadr.get_width()+textCadr.get_height() + 5), 5)
        pygame.draw.line(screen, pygame.Color("red"), (WIDTH - 5, textCadr.get_height() + 5),(WIDTH - 5 - textCadr.get_width(), textCadr.get_width() + textCadr.get_height() + 5), 5)
    for i in range(len(RGB)):
        textRGB = menuFont.render(RGB[i][0]+": "+str(RGB[i][1]), 1, WHITE)
        screen.blit(textRGB, (WIDTH - 5 - textCadr.get_width(), 10+textCadr.get_width()+textCadr.get_height()+textRGB.get_height()*i))
    textSecond = menuFont.render("sec: "+str(second), 1, WHITE)
    screen.blit(textSecond, (WIDTH - 5 - textCadr.get_width(), 10 + textCadr.get_width() + textCadr.get_height() + textSecond.get_height() * i + textCadr.get_height()))
    for i in range(len(anime[cadr][0])):
        pygame.draw.rect(screen, anime[cadr][2][i], (anime[cadr][0][i]*4 + x, anime[cadr][1][i]*4 + y, pixel*4, pixel*4))
    if hitbox:
        pygame.draw.rect(screen, GREEN, (x, y, Size, Size), 1)
    virtual_display = pygame.transform.scale(screen, current_size)
    screen0.blit(virtual_display, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()