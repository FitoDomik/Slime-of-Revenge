import pygame
import math
import sys
import ast
import os
from PIL import Image, ImageDraw
import io
from random import randint
try:
    from win32api import GetSystemMetrics
except Exception:
    try:
        import ctypes
        def GetSystemMetrics(index: int) -> int:
            try:
                return ctypes.windll.user32.GetSystemMetrics(index)
            except Exception:
                try:
                    info = pygame.display.Info()
                    return info.current_w if index == 0 else info.current_h
                except Exception:
                    return 800 if index == 0 else 600
    except Exception:
        def GetSystemMetrics(index: int) -> int:
            return 800 if index == 0 else 600
from enum import Enum
import json
pygame.font.init()
def get_base_path():
    if getattr(sys, 'frozen', False):
        try:
            return sys._MEIPASS
        except Exception:
            return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))
BASE_PATH = get_base_path()
try:
    if getattr(sys, 'frozen', False):
        os.chdir(BASE_PATH)
except Exception:
    pass
def get_settings_dir():
    appdata = os.environ.get('APPDATA') or os.path.expanduser('~')
    path = os.path.join(appdata, 'Slime_of_Revenge')
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass
    return path
SETTINGS_FILE = os.path.join(get_settings_dir(), 'settings.json')
directory = BASE_PATH
def load_settings():
    default_settings = {
        "fullscreen": False,
        "keys": {
            "UP": pygame.K_w,
            "DOWN": pygame.K_s,
            "LEFT": pygame.K_a,
            "RIGHT": pygame.K_d,
            "JUMP": pygame.K_SPACE,
            "DASH": pygame.K_LSHIFT,
            "SHOOT": "MOUSE_1"
        },
        "sound": {
            "music_volume": 15,
            "sfx_volume": 100,
            "musicTheme": "Roundabout.mp3"
        },
        "display": {
            "show_fps": True,
            "parallax_background": True,
            "background_type": "night"
        },
        "statistics": {
            "level_times": {},
            "level_deaths": {},
            "current_level_start_time": 0,
            "current_level_pause_on": 0,
            "current_level_deaths": 0,
            "current_level_name": ""
        }
    }
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            for key in default_settings:
                if key not in settings:
                    settings[key] = default_settings[key]
                elif isinstance(default_settings[key], dict):
                    for subkey in default_settings[key]:
                        if subkey not in settings[key]:
                            settings[key][subkey] = default_settings[key][subkey]
            return settings
    except (FileNotFoundError, json.JSONDecodeError):
        return default_settings
def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка сохранения настроек: {e}")
def get_key_name(key):
    key_names = {
        pygame.K_w: "W", pygame.K_s: "S", pygame.K_a: "A", pygame.K_d: "D",
        pygame.K_SPACE: "SPACE", pygame.K_RSHIFT: "RSHIFT", pygame.K_LSHIFT: "LSHIFT",
        pygame.K_RETURN: "ENTER", pygame.K_ESCAPE: "ESC", pygame.K_TAB: "TAB",
        pygame.K_BACKSPACE: "BACKSPACE", pygame.K_DELETE: "DELETE",
        pygame.K_LEFT: "LEFT", pygame.K_RIGHT: "RIGHT", pygame.K_UP: "UP", pygame.K_DOWN: "DOWN",
        pygame.K_LCTRL: "LCTRL", pygame.K_RCTRL: "RCTRL", pygame.K_LALT: "LALT", pygame.K_RALT: "RALT",
        pygame.K_q: "Q", pygame.K_e: "E", pygame.K_r: "R", pygame.K_t: "T", pygame.K_y: "Y",
        pygame.K_u: "U", pygame.K_i: "I", pygame.K_o: "O", pygame.K_p: "P", pygame.K_f: "F",
        pygame.K_g: "G", pygame.K_h: "H", pygame.K_j: "J", pygame.K_k: "K", pygame.K_l: "L",
        pygame.K_z: "Z", pygame.K_x: "X", pygame.K_c: "C", pygame.K_v: "V", pygame.K_b: "B",
        pygame.K_n: "N", pygame.K_m: "M", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3",
        pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8",
        pygame.K_9: "9", pygame.K_0: "0", pygame.K_BACKQUOTE: "`"
    }
    mouse_names = {
        "MOUSE_1": "ЛКМ",
        "MOUSE_2": "СКМ",
        "MOUSE_3": "ПКМ",
        "MOUSE_4": "МЫШЬ_4",
        "MOUSE_5": "МЫШЬ_5"
    }
    if isinstance(key, str) and key.startswith("MOUSE_"):
        return mouse_names.get(key, key)
    return key_names.get(key, f"KEY_{key}")
settings = load_settings()
UP = None
DOWN = None
LEFT = None
RIGHT = None
JUMP = None
DASH = None
SHOOT = None
def is_key_pressed(key_bind, event):
    if isinstance(key_bind, str) and key_bind.startswith("MOUSE_"):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button = int(key_bind.split("_")[1])
            return event.button == mouse_button
        return False
    else:
        if event.type == pygame.KEYDOWN:
            return event.key == key_bind
        return False
def is_key_released(key_bind, event):
    if isinstance(key_bind, str) and key_bind.startswith("MOUSE_"):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button = int(key_bind.split("_")[1])
            return event.button == mouse_button
        return False
    else:
        if event.type == pygame.KEYUP:
            return event.key == key_bind
        return False
def init_keys():
    global UP, DOWN, LEFT, RIGHT, JUMP, DASH, SHOOT
    UP = settings["keys"]["UP"]
    DOWN = settings["keys"]["DOWN"]
    LEFT = settings["keys"]["LEFT"]
    RIGHT = settings["keys"]["RIGHT"]
    JUMP = settings["keys"]["JUMP"]
    DASH = settings["keys"]["DASH"]
    SHOOT = settings["keys"]["SHOOT"]
init_keys()
gameButton = ""
waitingForKey = False
selectedKeyAction = ""
dragging_slider = False
dragging_type = ""
notification_text = ""
notification_time = 0
notification_duration = 3000
def update_sound_volumes():
    pygame.mixer.music.set_volume(settings["sound"]["music_volume"] / 100.0)
    sfx_vol = settings["sound"]["sfx_volume"] / 100.0
    clickSound.set_volume(1 * sfx_vol)
    scrollSound.set_volume(3 * sfx_vol)
    runSound.set_volume(0.2 * sfx_vol)
    jumpSound.set_volume(1 * sfx_vol)
    dropSound.set_volume(0.8 * sfx_vol)
    dashSound.set_volume(0.5 * sfx_vol)
    saveSound.set_volume(0.2 * sfx_vol)
    rollbackSound.set_volume(3 * sfx_vol)
    dieSound.set_volume(1 * sfx_vol)
    shootSound.set_volume(0.2 * sfx_vol)
    misfireSound.set_volume(0.6 * sfx_vol)
    chargerSound.set_volume(2 * sfx_vol)
    stopEnemyFlySound.set_volume(0.5 * sfx_vol)
    startEnemyFlySound.set_volume(4 * sfx_vol)
    hitWallSound.set_volume(0.4 * sfx_vol)
    hitEnemSound.set_volume(0.2 * sfx_vol)
    dieEnemySound.set_volume(0.8 * sfx_vol)
    finishSound.set_volume(0.7 * sfx_vol)
def start_level_timer(level_name):
    settings["statistics"]["current_level_name"] = level_name
    settings["statistics"]["current_level_start_time"] = pygame.time.get_ticks()
    settings["statistics"]["current_level_deaths"] = 0
    save_settings(settings)
def pause_on():
    settings["statistics"]["current_level_pause_on"] = pygame.time.get_ticks()
    save_settings(settings)
def pause_off():
    settings["statistics"]["current_level_start_time"] += pygame.time.get_ticks() - settings["statistics"]["current_level_pause_on"]
    save_settings(settings)
def add_death():
    if settings["statistics"]["current_level_name"]:
        settings["statistics"]["current_level_deaths"] += 1
        save_settings(settings)
def finish_level():
    if settings["statistics"]["current_level_name"]:
        level_name = settings["statistics"]["current_level_name"]
        current_time = pygame.time.get_ticks()
        level_time = (current_time - settings["statistics"]["current_level_start_time"]) / 1000.0
        is_new_record = False
        if level_name not in settings["statistics"]["level_times"] or level_time < settings["statistics"]["level_times"][level_name]:
            settings["statistics"]["level_times"][level_name] = level_time
            is_new_record = True
        settings["statistics"]["level_deaths"][level_name] = settings["statistics"]["current_level_deaths"]
        save_settings(settings)
        return [is_new_record, level_time]
def get_current_level_time():
    if settings["statistics"]["current_level_start_time"] > 0:
        current_time = pygame.time.get_ticks()
        return (current_time - settings["statistics"]["current_level_start_time"]) / 1000.0
    return 0
def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 100)
    return f"{minutes:02d}:{secs:02d}.{millisecs:02d}"
def show_notification(text):
    global notification_text, notification_time
    notification_text = text
    notification_time = pygame.time.get_ticks()
WIDTH = 889
HEIGHT = 500
BLACK = (0, 0, 0)
BLUE = (71, 153, 192)
WHITE = (225, 225, 225)
GREEN = (0, 250, 0)
GREEN2 = (150, 220, 150)
GREEN_d = (0, 255, 221)
GREEN_d2 = (151, 204, 190)
PURPLE = (171, 100, 237)
PURPLE2 = (192, 181, 196)
colorGG = GREEN
colorGG2 = GREEN2
menuColor = (33, 57, 94)
colorBullets1 = (116, 247, 40)
colorBullets2 = (60, 120, 135)
colorBullets = colorBullets2
backRED = (163, 95, 95)
backGREEN = (54, 64, 40)
backGRAY = (158, 158, 158)
backBROWN = (115, 91, 76)
backYELLOW = (184, 183, 141)
backPURPLE = (196, 183, 201)
backColor = [backRED, backGREEN, backGRAY, backBROWN, backYELLOW, backPURPLE]
createColor = backColor[0]
font_path = directory+"/textures/Faithful.ttf"
font = pygame.font.Font(font_path, 23)
menuFont = pygame.font.Font(font_path, 33)
fontMENU = pygame.font.Font(font_path, 50)
minY = HEIGHT-50
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
map = {"block": [[], [], [], []], "spikes": [[], [], [], []], "spring": [[], [], [], []],
        "rollback": [[], [], 8, 8, []], "background": [[], [], [], [], []],
        "spawnpoint": [[], [], 21, 21, -1], "bullets": [[], [], 16, 16, [], []],
       "enemyFly": [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []], "finish": [[], [], 24, 24, []]}
'''
with open('map.txt', 'r') as file:
    text = file.read()
map = ast.literal_eval(text)
'''
letMap = "none"
createType = "block"
correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [], "background": [],
                 "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}
createMenu = ["block", "spikes", "spring", "rollback", "spawnpoint", "bullets", "enemyFly", "finish"]
draw = 0
Size = 21
surf = 34
bullets = 0
bulletsMax = 16
inventory = [20, HEIGHT-80]
bulletsCadr = bullets * 2
bulletTime = 0
flyBullets = [[], [], [], []]
speedBullets = 30
lengthBullets = 20
motionU = "stop"
motionD = "stop"
motionL = "stop"
motionR = "stop"
jump = "stop"
jumpWallL = "stop"
jumpWallR = "stop"
dash = "stop"
shoot = "stop"
lastButton = "right"
NDash = lastButton
kG = 0.81
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
g = 0.5 * kG
surfG = 0.4
grav = 1
canJump = False
canJumpWallL = False
canJumpWallR = False
canDash = False
canShoot = True
gameMode = "surv"
stopRun = 0
spring = 0
hitbox = False
maxTimeDash = 15
timeDash = 0
timeShoot = 0
timeRollback = 600
Coyote = 6
timeCoyoteL = Coyote
timeCoyoteR = Coyote
menu = "menu"
buttonMenu = ["Играть", "Карты", "Создать", "Настройки", "Выйти"]
canCreate = False
'''UP = pygame.K_w
DOWN = pygame.K_s
LEFT = pygame.K_a
RIGHT = pygame.K_d
JUMP = pygame.K_SPACE
DASH = 3 
SHOOT = 1'''
gameButton = ""
FPS = 60
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen0 = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
current_size = (GetSystemMetrics(0), GetSystemMetrics(1))
print(current_size)
screen = pygame.Surface((WIDTH, HEIGHT))
screen0 = pygame.display.set_mode((current_size), pygame.FULLSCREEN)
k_posX = WIDTH/GetSystemMetrics(0)
k_posY = HEIGHT/GetSystemMetrics(1)
fullScreen = True
musicPlaylist = []
filesMusic = os.listdir(directory+"/music")
for mus in filesMusic:
    musicPlaylist.append(mus)
print(musicPlaylist)
'''if "They all" in settings["statistics"]["level_times"]:
    musicPlaylist.append("All star.mp3")
if "OnlyUp" in settings["statistics"]["level_times"]:
    musicPlaylist.append("Bring Me To Life.mp3")
if "Going down" in settings["statistics"]["level_times"]:
    musicPlaylist.append("It's Going Down Now.mp3")
if "Feel a little pain" in settings["statistics"]["level_times"]:
    musicPlaylist.append("Monster.mp3")
musicPlaylist.append("Roundabout.mp3")
if "Torn by katana" in settings["statistics"]["level_times"]:
    musicPlaylist.append("The Only Thing I Know For Real.mp3")
if "DOOM" in settings["statistics"]["level_times"]:
    musicPlaylist.append("The Only Thing They Fear Is You.mp3")'''
musicIndex = musicPlaylist.index(settings['sound']['musicTheme'])
pygame.mixer.music.load(directory+f"\music\{settings['sound']['musicTheme']}")
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1, 1)
clickSound = pygame.mixer.Sound(directory+'\sounds\click.ogg')
clickSound.set_volume(1)
scrollSound = pygame.mixer.Sound(directory+'\sounds\scroll.ogg')
scrollSound.set_volume(3)
runSound = pygame.mixer.Sound(directory+'\sounds\Run.ogg')
runSound.set_volume(0.2)
runSo = -1
playSoundRun = 1
playSoundSlide = 1
jumpSound = pygame.mixer.Sound(directory+'\sounds\jump.ogg')
jumpSound.set_volume(1)
dropSound = pygame.mixer.Sound(directory+'\sounds\drop.ogg')
dropSound.set_volume(0.8)
dashSound = pygame.mixer.Sound(directory+'\sounds\dash.ogg')
dashSound.set_volume(0.5)
saveSound = pygame.mixer.Sound(directory+'\sounds\save.ogg')
saveSound.set_volume(0.2)
rollbackSound = pygame.mixer.Sound(directory+'\sounds\Rollback.ogg')
rollbackSound.set_volume(3)
dieSound = pygame.mixer.Sound(directory+'\sounds\die.ogg')
dieSound.set_volume(1)
shootSound = pygame.mixer.Sound(directory+'\sounds\Shoot.ogg')
shootSound.set_volume(0.3)
misfireSound = pygame.mixer.Sound(directory+'\sounds\misfire.ogg')
misfireSound.set_volume(0.7)
chargerSound = pygame.mixer.Sound(directory+'\sounds\charger.ogg')
chargerSound.set_volume(2)
stopEnemyFlySound = pygame.mixer.Sound(directory+'\sounds\StartEnemy.ogg')
stopEnemyFlySound.set_volume(0.5)
startEnemyFlySound = pygame.mixer.Sound(directory+'\sounds\StoptEnemy.ogg')
startEnemyFlySound.set_volume(4)
hitWallSound = pygame.mixer.Sound(directory+'\sounds\hitWall.ogg')
hitWallSound.set_volume(0.6)
hitEnemSound = pygame.mixer.Sound(directory+'\sounds\hitEnem.ogg')
hitEnemSound.set_volume(0.4)
dieEnemySound = pygame.mixer.Sound(directory+'\sounds\dieEnemy.ogg')
dieEnemySound.set_volume(0.7)
finishSound = pygame.mixer.Sound(directory+'\sounds\Finish.ogg')
finishSound.set_volume(1)
lastMenuButton = ""
update_sound_volumes()
def fixColor(f, k):
    if k <= 0:
        k = 10**(-9)
    if isinstance(f[0][0], int):
        new = []
        for i in range(len(f[2])):
            newColor = []
            my_list = list(f[2][i])
            for j in range(3):
                newColor.append(min(int(my_list[j] / k), 255))
            new.append(tuple(newColor))
        f[2] = new
    else:
        for q in range(len(f)):
            new = []
            for i in range(len(f[q][2])):
                newColor = []
                my_list = list(f[q][2][i])
                for j in range(3):
                    newColor.append(int(my_list[j] / k))
                new.append(tuple(newColor))
            f[q][2] = new
    return f
def drawLight(R, Color, a):
    wImg = 2*max(R)
    hImg = 2*max(R)
    img = Image.new('RGBA', (wImg, hImg), (0, 0, 0, 0))
    drawTexture = ImageDraw.Draw(img)
    center = max(R)
    for i in range(len(R)):
        drawTexture.ellipse((center-R[i], center-R[i], center+R[i], center+R[i]), fill=(*Color, a[i]))
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")
    image_bytes.seek(0)
    downloadImg = pygame.image.load(image_bytes)
    return downloadImg
def drawingTextures(textures, pixels, transp):
    pixels -= 1
    if isinstance(textures[0][0], list):
        result = []
        for i in range(len(textures)):
            if isinstance(transp, int):
                aSc = transp
            else:
                if i > len(textures)//2:
                    kaSc = len(textures) / (i * 2)
                else:
                    kaSc = i*2/len(textures)
                aSc = int(transp[0]+(transp[1]-transp[0])*kaSc)
            wImg = max(textures[i][0])+pixels+1 - min(textures[i][0])
            hImg = max(textures[i][1])+pixels+1 - min(textures[i][1])
            img = Image.new('RGBA', (wImg, hImg), (0, 0, 0, 0))
            drawTexture = ImageDraw.Draw(img)
            for drImg in range(len(textures[i][0])):
                xImg = textures[i][0][drImg] - min(textures[i][0])
                yImg = textures[i][1][drImg] - min(textures[i][1])
                drawTexture.rectangle(((xImg, yImg), (xImg + pixels, yImg + pixels)), fill=(*textures[i][2][drImg], aSc))
            image_bytes = io.BytesIO()
            img.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            downloadImg = pygame.image.load(image_bytes)
            result.append(downloadImg)
    else:
        wImg = max(textures[0]) + pixels+1 - min(textures[0])
        hImg = max(textures[1]) + pixels+1 - min(textures[1])
        img = Image.new('RGBA', (wImg, hImg), (0, 0, 0, 0))
        drawTexture = ImageDraw.Draw(img)
        for drImg in range(len(textures[0])):
            xImg = textures[0][drImg] - min(textures[0])
            yImg = textures[1][drImg] - min(textures[1])
            drawTexture.rectangle(((xImg, yImg), (xImg + pixels, yImg + pixels)), fill=(*textures[2][drImg], transp))
        image_bytes = io.BytesIO()
        img.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        result = pygame.image.load(image_bytes)
    return result
def appStars(surf, N, size, Bul):
    if Bul:
        result = [[], [], []]
    else:
        result = [[], []]
    for i in range(N):
        xStar = randint(0, int(surf[0])-size)
        result[0].append(xStar)
        yStar = randint(0, int(surf[1]) - size)
        result[1].append(yStar)
        if len(result) == 3:
            light = randint(0, 1)
            if light == 0:
                result[2].append(False)
            else:
                result[2].append(True)
    return result
def transformWidth(textures, k):
    if isinstance(textures, list):
        result = []
        for i in range(len(textures)):
            result.append(pygame.transform.scale(textures[i], (textures[i].get_width()*k, textures[i].get_height()*k)))
    else:
        result = pygame.transform.scale(textures, (textures.get_width()*k, textures.get_height()*k))
    return result
with open(directory+'/textures/GGStop.txt', 'r') as file:
    text1 = file.readline()
    GGStop = ast.literal_eval(text1)
    text2 = file.readline()
    GGStopSec = ast.literal_eval(text2)
with open(directory+'/textures/GGRun.txt', 'r') as file:
    text1 = file.readline()
    GGRun = ast.literal_eval(text1)
    text2 = file.readline()
    GGRunSec = ast.literal_eval(text2)
with open(directory+'/textures/GGJump.txt', 'r') as file:
    text1 = file.readline()
    GGJump = ast.literal_eval(text1)
    text2 = file.readline()
    GGJumpSec = ast.literal_eval(text2)
with open(directory+'/textures/GGJumpRun.txt', 'r') as file:
    text1 = file.readline()
    GGJumpRun = ast.literal_eval(text1)
    text2 = file.readline()
    GGJumpRunSec = ast.literal_eval(text2)
with open(directory+'/textures/GGDash.txt', 'r') as file:
    text1 = file.readline()
    GGDash = ast.literal_eval(text1)
    text2 = file.readline()
    GGDashSec = ast.literal_eval(text2)
with open(directory+'/textures/GGDashRun.txt', 'r') as file:
    text1 = file.readline()
    GGDashRun = ast.literal_eval(text1)
    text2 = file.readline()
    GGDashRunSec = ast.literal_eval(text2)
timeCadrRoll = 0
cadrRoll = 0
with open(directory+'/textures/RollBack.txt', 'r') as file:
    text1 = file.readline()
    RollBackTexture = ast.literal_eval(text1)
    text2 = file.readline()
    RollBackSec = ast.literal_eval(text2)
with open(directory+'/textures/RollBack2.txt', 'r') as file:
    text1 = file.readline()
    RollBackTexture2 = ast.literal_eval(text1)
    text2 = file.readline()
    RollBackSec2 = ast.literal_eval(text2)
RollBackTextureimg = drawingTextures(RollBackTexture, 2, 255)
RollBackTexture2img = drawingTextures(RollBackTexture2, 2, 255)
with open(directory+'/textures/Gun.txt', 'r') as file:
    text1 = file.readline()
    GUN = ast.literal_eval(text1)
    text2 = file.readline()
    GunSec = ast.literal_eval(text2)
Gun = GUN[0]
GunSurf = pygame.Surface((max(Gun[0])+2, max(Gun[1])+2), pygame.SRCALPHA)
GunSurfR = GunSurf
pivotGun = [int(-surfX + x + Size//2), int(-surfY + y + Size//2)]
offsetGun = pygame.math.Vector2(7, -3)
with open(directory+'/textures/Bullets.txt', 'r') as file:
    text1 = file.readline()
    BULLETS = ast.literal_eval(text1)
with open(directory+'/textures/BulletsMAX.txt', 'r') as file:
    text1 = file.readline()
    BULLETSMAX = ast.literal_eval(text1)
with open(directory+'/textures/BulletTextureNew.txt', 'r') as file:
    text1 = file.readline()
    BulletTexture = ast.literal_eval(text1)
BulletTextureimg = drawingTextures(BulletTexture, 2, 255)
with open(directory+'/textures/enemyFlyStan.txt', 'r') as file:
    text1 = file.readline()
    ENEMYSTAN1 = ast.literal_eval(text1)
with open(directory+'/textures/dieEnemyFly.txt', 'r') as file:
    text1 = file.readline()
    ENEMYDIE1 = ast.literal_eval(text1)
with open(directory+'/textures/enemyFly.txt', 'r') as file:
    text1 = file.readline()
    ENEMY1 = ast.literal_eval(text1)
    text2 = file.readline()
    enemyFlySec = ast.literal_eval(text2)
ENEMY1img = drawingTextures(ENEMY1, 3, 255)
ENEMYDIE1img = drawingTextures(ENEMYDIE1, 3, 255)
ENEMYSTAN1img = drawingTextures(ENEMYSTAN1, 3, 255)
enemyFly = ENEMY1img[0]
lengthSmell = HEIGHT//2 + 50
lengthFallSmell = WIDTH//2 + 50
speedEnemy = 3.5
hpEnemyFly = 100
timerStan = 3 * FPS
helpEnemy = 0
damage = 15
with open(directory+'/textures/Finish2.txt', 'r') as file:
    text1 = file.readline()
    FINISH2 = ast.literal_eval(text1)
with open(directory+'/textures/Finish2dis.txt', 'r') as file:
    text1 = file.readline()
    FINISH2dis = ast.literal_eval(text1)
with open(directory+'/textures/Finish.txt', 'r') as file:
    text1 = file.readline()
    FINISH = ast.literal_eval(text1)
    text2 = file.readline()
    finishSec = ast.literal_eval(text2)
FINISHimg = drawingTextures(FINISH, 3, 255)
FINISH2img = drawingTextures(FINISH2, 3, 255)
FINISH2disimg = drawingTextures(FINISH2dis, 3, 255)
finishTex = FINISHimg[0]
finishTimeCadr = 0
finishPacifist = True
RollTex = RollBackTexture[cadrRoll]
RollTex2 = RollBackTexture2[cadrRoll]
def rotate1(surface, angle, pivot, offset):
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  
    rotated_offset = offset.rotate(angle)  
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  
timeCadrSpawn = 0
timeCadrSpawn2 = 0
cadrSpawn = 0
cadrSpawn2 = 0
with open(directory+'/textures/SpawnAnime.txt', 'r') as file:
    text1 = file.readline()
    SpawnTexture = ast.literal_eval(text1)
    text2 = file.readline()
    SpawnSec = ast.literal_eval(text2)
with open(directory+'/textures/SpawnAnime2.txt', 'r') as file:
    text1 = file.readline()
    SpawnTexture2 = ast.literal_eval(text1)
    text2 = file.readline()
    SpawnSec2 = ast.literal_eval(text2)
SpawnTextureimg = drawingTextures(SpawnTexture, 3, 255)
SpawnTexture2img = drawingTextures(SpawnTexture2, 3, 255)
SpawnTex = SpawnTextureimg[cadrSpawn]
SpawnTex2 = SpawnTexture2img[cadrSpawn]
timeCadrSpikes = 0
cadrSpikes = 0
with open(directory+'/textures/Spikes.txt', 'r') as file:
    text1 = file.readline()
    SpikesTexture = ast.literal_eval(text1)
    text2 = file.readline()
    SpikesSec = ast.literal_eval(text2)
SpikesTextureimg = drawingTextures(SpikesTexture, 2, 255)
SpikesTex = SpikesTextureimg[cadrSpikes]
with open(directory+'/textures/Cassette.txt', 'r') as file:
    text1 = file.readline()
    PLATE = ast.literal_eval(text1)
    text2 = file.readline()
    plateSec = ast.literal_eval(text2)
plateTex = PLATE[0]
plateTime = 0
with open(directory+'/textures/CassetteEmpty.txt', 'r') as file:
    text1 = file.readline()
    CASSETTE = ast.literal_eval(text1)
with open(directory+'/textures/PlanetBackground2.txt', 'r') as file:
    text1 = file.readline()
    PlanetBackground = ast.literal_eval(text1)
kBlack = 4 
PlanetBackground = fixColor(PlanetBackground, 1 * kBlack)
PlanetBackgroundimg = drawingTextures(PlanetBackground, 2, 255)
PlanetBackgroundimg = pygame.transform.scale(PlanetBackgroundimg, (PlanetBackgroundimg.get_width()*3, PlanetBackgroundimg.get_height()*3))
colorPlanetLight = fixColor([[0], [0], [(80, 100, 95)]], 0.5 * kBlack)[2][0]
PlanetLight = drawLight([17, 13, 9], colorPlanetLight, [20, 60, 120])
PlanetLight = pygame.transform.scale(PlanetLight, (PlanetLight.get_width()*6, PlanetLight.get_height()*6))
kbackground1 = 30
xBackground = (x - PlanetBackgroundimg.get_width()//2) * kbackground1
yBackground = (y - PlanetBackgroundimg.get_height()//2) * kbackground1
with open(directory+'/textures/bigStar.txt', 'r') as file:
    text1 = file.readline()
    BigStar = ast.literal_eval(text1)
    text2 = file.readline()
    BigStarSec = ast.literal_eval(text2)
BigStar = fixColor(BigStar, 1.5 * kBlack)
BigStarimg = drawingTextures(BigStar, 2, 255)
surfStarsBig = [WIDTH*2, HEIGHT*2]
bigStarsPos = appStars(surfStarsBig, 30, BigStarimg[0].get_width(), True)
kbackground2 = 40
timeBlinkStar = 0
with open(directory+'/textures/smallStar.txt', 'r') as file:
    text1 = file.readline()
    SmallStar = ast.literal_eval(text1)
SmallStar = fixColor(SmallStar, 2.5 * kBlack)
SmallStarimg = drawingTextures(SmallStar, 1, 255)
surfStarsSmall = [int(WIDTH*1.5), int(HEIGHT*1.5)]
smallStarsPos = appStars(surfStarsSmall, 40, SmallStarimg.get_width(), False)
kbackground3 = 60
with open(directory+'/textures/shootingStarBig.txt', 'r') as file:
    text1 = file.readline()
    ShootingStarBig = ast.literal_eval(text1)
    text2 = file.readline()
    ShootingStarBigSec = ast.literal_eval(text2)
kShSt = 2
ShootingStarBig = fixColor(ShootingStarBig, 1.5 * kBlack)
ShootingStarSmall = fixColor(ShootingStarBig, 1.7)
ShootingStarBigimg = drawingTextures(ShootingStarBig, 1, [80, 255])
ShootingStarBigimg = transformWidth(ShootingStarBigimg, kShSt)
ShootingStarSmallimg = drawingTextures(ShootingStarSmall, 1, [80, 255])
sizeShStB = 70 * kShSt
ShootingStarBigTSp = [1, 10]
timeToFallStar = randint(ShootingStarBigTSp[0], ShootingStarBigTSp[1])
shootingStarBigTime = 0
starSizeBig = randint(1, 2)
xShSB = 0
yShSB = 0
timeCadr = 0
cadr = 0
GG = GGStop[cadr]
GGRIGHT = True
DROP = False
drawX = 0
drawY = 0
anime = 0
rotate = "none"
FlagWall = False
SpringAllY = 0
timeCadrMenu = 0
cadrMenu = 0
GGMenu = GGStop[cadr]
def list_deepcopy(l):
    return [
        elem if not isinstance(elem, list) else list_deepcopy(elem)
        for elem in l
    ]
def napravl(NDash, x, y, speedG, speed):
    if NDash == "right":
        x += speedDash
        speed = maxSpeed
    elif NDash == "left":
        x -= speedDash
        speed = maxSpeed
    elif NDash == "up":
        y -= speedDash
    elif NDash == "down":
        y += speedDash
        speedG = maxSpeedG
    elif NDash == "upright":
        x += speedDash * 0.7
        y -= speedDash * 0.7
        speed = maxSpeed
    elif NDash == "upleft":
        x -= speedDash * 0.7
        y -= speedDash * 0.7
        speed = maxSpeed
    elif NDash == "downright":
        y += speedDash * 0.7
        x += speedDash * 0.7
        speedG = maxSpeedG * 0.7
        speed = maxSpeed
    elif NDash == "downleft":
        y += speedDash * 0.7
        x -= speedDash * 0.7
        speedG = maxSpeedG * 0.7
        speed = maxSpeed
    return x, y, speedG, speed
scroll = 0
victoryTime = 2 * FPS
win = False
clock = pygame.time.Clock()
while True:
    if menu == "menu":
        if buttonMenu[0] == "Играть" and letMap != "none":
            buttonMenu = ["Играть", "Карты", "Редактировать", "Создать", "Настройки", "Выйти"]
        screen.fill(menuColor)
        timeCadrMenu += 1
        if timeCadrMenu >= FPS * GGStopSec // len(GGStop):
            if cadrMenu + 1 < len(GGStop):
                cadrMenu += 1
            else:
                cadrMenu = 0
            timeCadrMenu = 0
        if cadrMenu + 1 >= len(GGStop):
            cadrMenu = 0
        GGMenu = GGStop[cadrMenu]
        for j in range(len(GGMenu[0])):
            drawX = WIDTH // 2 - Size * 10 // 2 + GGMenu[0][j] * 10
            drawY = HEIGHT // 2 - Size * 10 // 2 + GGMenu[1][j] * 10
            lol = GGMenu[2][j]
            if GGMenu[2][j] == (0, 190, 0):
                lol = (50, 120, 80)
            elif GGMenu[2][j] == (0, 95, 0):
                lol = (10, 45, 20)
            pygame.draw.rect(screen, lol, (drawX, drawY, 30, 30))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    if buttonMenu[0] == "Продолжить":
                        menu = "game"
                        pygame.mixer.music.set_volume(settings["sound"]["music_volume"] / 100.0 * 0.4)
                        clickSound.play()
                    else:
                        pygame.quit()
                        sys.exit()
                if i.key == pygame.K_F11 or i.key == pygame.K_F10:
                    if fullScreen:
                        screen0 = pygame.display.set_mode(current_size)
                    else:
                        screen0 = pygame.display.set_mode((current_size), pygame.FULLSCREEN)
                    fullScreen = not fullScreen
            if i.type == pygame.MOUSEMOTION:
                mouseX = i.pos[0] * k_posX
                mouseY = i.pos[1] * k_posY
            if i.type == pygame.MOUSEBUTTONUP:
                if i.button == 1:
                    for j in range(len(buttonMenu)):
                        text = menuFont.render(buttonMenu[j], 1, WHITE)
                        if i.pos[0] * k_posX > WIDTH//2-text.get_width()//2 \
                                and i.pos[0] * k_posX < WIDTH//2-text.get_width()//2+text.get_width() \
                                and i.pos[1] * k_posY > HEIGHT//2-50+j*(text.get_height()+5)+5 \
                                and i.pos[1] * k_posY < HEIGHT // 2 - 50 + j * (text.get_height() + 5) + text.get_height()-5:
                            clickSound.play()
                            if buttonMenu[j] == "Играть":
                                menu = "game"
                                canCreate = False
                                gameMode = "surv"
                                victoryTime = 2 * FPS
                                pygame.mixer.music.set_volume(settings["sound"]["music_volume"] / 100.0 * 0.4)
                                start_level_timer(letMap.split(".")[0])
                                break
                            elif buttonMenu[j] == "Продолжить":
                                menu = "game"
                                pygame.mixer.music.set_volume(settings["sound"]["music_volume"] / 100.0 * 0.4)
                                pause_off()
                                break
                            elif buttonMenu[j] == "Карты":
                                menu = "maps"
                                lol = os.path.dirname(os.path.abspath(__file__))
                                directory = lol+"/maps"
                                files = os.listdir(directory)
                                print(files)
                                break
                            elif buttonMenu[j] == "Сохранить":
                                if "enemyFly" in map:
                                    for ret in range(len(map["enemyFly"][0])):
                                        map["enemyFly"][-1][ret] = 0
                                        map["enemyFly"][4][ret] = 0
                                        map["enemyFly"][5][ret] = 0
                                        map["enemyFly"][6][ret] = False
                                        map["enemyFly"][0][ret] = map["enemyFly"][7][0][ret]
                                        map["enemyFly"][1][ret] = map["enemyFly"][7][1][ret]
                                        map["enemyFly"][7][2][ret] = 0
                                        map["enemyFly"][7][3][ret] = 0
                                        map["enemyFly"][8][ret] = 0
                                        map["enemyFly"][9][ret] = hpEnemyFly
                                if "bullets" in map:
                                    for ret in range(len(map["bullets"][0])):
                                        map["bullets"][0][ret] = map["bullets"][4][ret]
                                        map["bullets"][1][ret] = map["bullets"][5][ret]
                                lol = os.path.dirname(os.path.abspath(__file__))
                                directory = lol + "/maps"
                                files = os.listdir(directory)
                                my_file = open(directory+"/map"+str(len(files)+1)+".txt", "w+")
                                my_file.write(str(map)+"\n"+str(spawnX)+"\n"+str(spawnY)+"\n"+str(spawnSX)+"\n"+str(spawnSY))
                                break
                            elif buttonMenu[j] == "Настройки":
                                menu = "settings"
                                buttonMenu = ["Управление", "Музыка и звуки", "Сбросить настройки", "Назад"]
                                break
                            elif buttonMenu[j] == "Редактировать":
                                victoryTime = 2 * FPS
                                pygame.mixer.music.set_volume(settings["sound"]["music_volume"] / 100.0 * 0.4)
                                menu = "game"
                                canCreate = True
                                gameMode = "surv"
                                createType = "block"
                                correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [],
                                                 "background": [], "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}
                                break
                            elif buttonMenu[j] == "Создать":
                                victoryTime = 2 * FPS
                                pygame.mixer.music.set_volume(settings["sound"]["music_volume"] / 100.0 * 0.4)
                                menu = "game"
                                gameMode = "surv"
                                canCreate = True
                                x = spawnX
                                y = spawnY
                                xO = x
                                yO = y
                                surfX = spawnSX
                                surfY = spawnSY
                                motionL = 'stop'
                                motionR = 'stop'
                                motionU = 'stop'
                                motionD = 'stop'
                                dash = 'stop'
                                jump = 'stop'
                                jumpWallL = "stop"
                                jumpWallR = "stop"
                                speed = 0
                                speedG = 0
                                timeDash = 0
                                canJump = False
                                canJumpWallR = False
                                canJumpWallL = False
                                canDash = False
                                map = {"block": [[], [], [], []], "spikes": [[], [], [], []], "spring": [[], [], [], []],
                                      "rollback": [[], [], 8, 8, []], "background": [[], [], [], [], []],
                                      "spawnpoint": [[], [], 21, 21, -1], "bullets": [[], [], 16, 16, [], []],
                                       "enemyFly": [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []], "finish": [[], [], 24, 24, []]}
                                correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [],
                                                 "background": [], "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}
                                letMap = "none"
                                createType = "block"
                                break
                            elif buttonMenu[j] == "Покинуть уровень":
                                victoryTime = 2 * FPS
                                shootingStarBigTime = 0
                                menu = "menu"
                                buttonMenu = ["Играть", "Карты", "Создать", "Настройки", "Выйти"]
                                canCreate = True
                                spawnX = TrueX
                                spawnY = TrueY
                                x = spawnX
                                y = spawnY
                                xO = x
                                yO = y
                                surfX = 0
                                surfY = 0
                                spawnSX = surfX
                                spawnSY = surfY
                                motionL = 'stop'
                                motionR = 'stop'
                                motionU = 'stop'
                                motionD = 'stop'
                                dash = 'stop'
                                jump = 'stop'
                                jumpWallL = "stop"
                                jumpWallR = "stop"
                                speed = 0
                                maxSpeed = 4
                                speedG = 0
                                timeDash = 0
                                canJump = False
                                canJumpWallR = False
                                canJumpWallL = False
                                canDash = False
                                canShoot = True
                                timeShoot = 0
                                bullets = 0
                                bulletsCadr = bullets * 2
                                bulletTime = 0
                                colorBullets = colorBullets2
                                map = {"block": [[], [], [], []], "spikes": [[], [], [], []], "spring": [[], [], [], []],
                                      "rollback": [[], [], 8, 8, []], "background": [[], [], [], [], []],
                                      "spawnpoint": [[], [], 21, 21, -1], "bullets": [[], [], 16, 16, [], []],
                                       "enemyFly": [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []], "finish": [[], [], 24, 24, []]}
                                correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [],
                                                 "background": [], "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}
                                letMap = "none"
                                createType = "block"
                                break
                            elif buttonMenu[j] == "Выйти":
                                pygame.quit()
                                sys.exit()
        textMENU = fontMENU.render('МЕНЮ', 1, GREEN_d)
        screen.blit(textMENU, (WIDTH//2-textMENU.get_width()//2, HEIGHT//4))
        if buttonMenu[0] == "Карты":
            if win[0]:
                colorWin = (0, 255, 0)
                textWinGame = "НОВЫЙ РЕКОРД:"
                textWinGame += f" {format_time(win[1])}"
            else:
                colorWin = (255, 0, 0)
                textWinGame = ""
                textWinGame += f"Время: {format_time(win[1])}"
            textWin = menuFont.render(textWinGame, 1, colorWin)
            screen.blit(textWin, (WIDTH // 2 - textWin.get_width() // 2, HEIGHT // 4 - 50))
        for i in range(len(buttonMenu)):
            colorButton = WHITE
            text = menuFont.render(buttonMenu[i], 1, colorButton)
            if mouseX > WIDTH // 2 - text.get_width() // 2 \
                    and mouseX < WIDTH // 2 - text.get_width() // 2 + text.get_width() \
                    and mouseY > HEIGHT // 2 - 50 + i * (text.get_height() + 5) +5 \
                    and mouseY < HEIGHT // 2 - 50 + i * (text.get_height() + 5) + text.get_height() -5:
                if lastMenuButton != buttonMenu[i]:
                    scrollSound.play()
                    lastMenuButton = buttonMenu[i]
                colorButton = (255, 0, 0)
            text = menuFont.render(buttonMenu[i], 1, colorButton)
            screen.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-50+i*(text.get_height()+5)))
            if buttonMenu[i] == "Играть" and colorButton == (255, 0, 0):
                textMap = menuFont.render(">"+letMap.split(".")[0], 1, (200, 200, 10))
                screen.blit(textMap, (WIDTH // 2 + text.get_width() // 2+5, HEIGHT // 2 - 50 + i * (text.get_height() + 5)))
            if buttonMenu[i] == "Редактировать" and colorButton == (255, 0, 0):
                textMap = menuFont.render(">" + letMap.split(".")[0], 1, (200, 200, 10))
                screen.blit(textMap,
                            (WIDTH // 2 + text.get_width() // 2 + 5, HEIGHT // 2 - 50 + i * (text.get_height() + 5)))
            if buttonMenu[i] == "Сохранить" and colorButton == (255, 0, 0):
                lol = os.path.dirname(os.path.abspath(__file__))
                directory = lol + "/maps"
                files = os.listdir(directory)
                textMap = menuFont.render(">map" + str(len(files)+1), 1, (200, 200, 10))
                screen.blit(textMap,
                            (WIDTH // 2 + text.get_width() // 2 + 5, HEIGHT // 2 - 50 + i * (text.get_height() + 5)))
    elif menu == "settings":
        screen.fill(menuColor)
        timeCadrMenu += 1
        if timeCadrMenu >= FPS * SpawnSec2 // len(SpawnTexture2):
            if cadrMenu + 1 < len(SpawnTexture2):
                cadrMenu += 1
            else:
                cadrMenu = 0
            timeCadrMenu = 0
        if cadrMenu + 1 >= len(SpawnTexture2):
            cadrMenu = 0
        GGMenu = SpawnTexture2[cadrMenu]
        for j in range(len(GGMenu[0])):
            drawX = WIDTH // 2 - Size * 10 // 2 + GGMenu[0][j] * 10
            drawY = HEIGHT // 2 - Size * 10 // 2 + GGMenu[1][j] * 10
            lol = GGMenu[2][j]
            if GGMenu[2][j] == (0, 190, 0):
                lol = (50, 120, 80)
            elif GGMenu[2][j] == (0, 95, 0):
                lol = (10, 45, 20)
            elif GGMenu[2][j] == (125, 250, 135):
                lol = (50, 120, 80)
            elif GGMenu[2][j] == (220, 215, 0):
                lol = (201, 168, 58)
            pygame.draw.rect(screen, lol, (drawX, drawY, 30, 30))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    waitingForKey = False
                    selectedKeyAction = ""
                    if buttonMenu[0] == "Управление":
                        menu = "menu"
                        buttonMenu = ["Играть", "Карты", "Создать", "Настройки", "Выйти"]
                    else:
                        buttonMenu = ["Управление", "Музыка и звуки", "Сбросить настройки", "Назад"]
                    clickSound.play()
                if i.key == pygame.K_F11:
                    if fullScreen:
                        screen0 = pygame.display.set_mode(current_size)
                    else:
                        screen0 = pygame.display.set_mode((current_size), pygame.FULLSCREEN)
                    fullScreen = not fullScreen
                if waitingForKey and i.key != pygame.K_ESCAPE:
                    new_key = i.key
                    conflict = False
                    for action, key in settings["keys"].items():
                        if key == new_key and action != selectedKeyAction:
                            conflict = True
                            break
                    if not conflict:
                        settings["keys"][selectedKeyAction] = new_key
                        globals()[selectedKeyAction] = new_key
                        save_settings(settings)
                        if buttonMenu[0].startswith("UP:"):
                            buttonMenu = [
                                f"UP: {get_key_name(settings['keys']['UP'])}",
                                f"DOWN: {get_key_name(settings['keys']['DOWN'])}",
                                f"LEFT: {get_key_name(settings['keys']['LEFT'])}",
                                f"RIGHT: {get_key_name(settings['keys']['RIGHT'])}",
                                f"JUMP: {get_key_name(settings['keys']['JUMP'])}",
                                f"DASH: {get_key_name(settings['keys']['DASH'])}",
                                f"SHOOT: {get_key_name(settings['keys']['SHOOT'])}",
                                "Назад"
                            ]
                    waitingForKey = False
                    selectedKeyAction = ""
            if i.type == pygame.MOUSEMOTION:
                mouseX = i.pos[0] * k_posX
                mouseY = i.pos[1] * k_posY
                if dragging_slider:
                    slider_x = WIDTH // 2 - 100
                    slider_width = 200
                    if mouseX >= slider_x and mouseX <= slider_x + slider_width:
                        click_pos = mouseX - slider_x
                        new_volume = int((click_pos / slider_width) * 100)
                        new_volume = max(0, min(100, new_volume))
                    elif mouseX < slider_x:
                        new_volume = 0
                    elif mouseX > slider_x + slider_width:
                        new_volume = 100
                    if dragging_type == "music":
                        settings["sound"]["music_volume"] = new_volume
                    elif dragging_type == "sfx":
                        settings["sound"]["sfx_volume"] = new_volume
                    update_sound_volumes()
                    save_settings(settings)
                    buttonMenu = [
                        f"Музыка: {settings['sound']['music_volume']}%",
                        f"Звуки: {settings['sound']['sfx_volume']}%",
                        f"<< {settings['sound']['musicTheme'].split('.')[0]} >>",
                        "Назад"
                    ]
            if i.type == pygame.MOUSEBUTTONUP:
                if i.button == 1:
                    dragging_slider = False
                    dragging_type = ""
                    extra_spacing = 25 if "Музыка:" in str(buttonMenu) or "Звуки:" in str(buttonMenu) else 0
                    for j in range(len(buttonMenu)):
                        text = menuFont.render(buttonMenu[j], 1, WHITE)
                        item_height = text.get_height() + 5 + extra_spacing
                        if (i.pos[0] * k_posX > WIDTH//2-text.get_width()//2 \
                                and i.pos[0] * k_posX < WIDTH//2-text.get_width()//2+text.get_width() \
                                and i.pos[1] * k_posY > HEIGHT//2-50+j*item_height+5 \
                                and i.pos[1] * k_posY < HEIGHT // 2 - 50 + j * item_height + text.get_height()-5) \
                                and (buttonMenu[j] != f"<< {settings['sound']['musicTheme'].split('.')[0]} >>" \
                                or (i.pos[0] * k_posX < WIDTH // 2 - text.get_width() // 2 + 25 or i.pos[0] * k_posX > WIDTH // 2 - text.get_width() // 2 + text.get_width() - 25)):
                            if not((buttonMenu[j].split(":")[0] == "Музыка") or (buttonMenu[j].split(":")[0] == "Звуки")):
                                clickSound.play()
                            if buttonMenu[j] == "Назад":
                                if buttonMenu[0] == "Управление":
                                    menu = "menu"
                                    buttonMenu = ["Играть", "Карты", "Создать", "Настройки", "Выйти"]
                                else:
                                    buttonMenu = ["Управление", "Музыка и звуки", "Сбросить настройки", "Назад"]
                                waitingForKey = False
                                selectedKeyAction = ""
                                break
                            elif buttonMenu[j] == "Управление":
                                buttonMenu = [
                                    f"UP: {get_key_name(settings['keys']['UP'])}",
                                    f"DOWN: {get_key_name(settings['keys']['DOWN'])}",
                                    f"LEFT: {get_key_name(settings['keys']['LEFT'])}",
                                    f"RIGHT: {get_key_name(settings['keys']['RIGHT'])}",
                                    f"JUMP: {get_key_name(settings['keys']['JUMP'])}",
                                    f"DASH: {get_key_name(settings['keys']['DASH'])}",
                                    f"SHOOT: {get_key_name(settings['keys']['SHOOT'])}",
                                    "Назад"
                                ]
                                break
                            elif buttonMenu[j] == "Музыка и звуки":
                                buttonMenu = [
                                    f"Музыка: {settings['sound']['music_volume']}%",
                                    f"Звуки: {settings['sound']['sfx_volume']}%",
                                    f"<< {settings['sound']['musicTheme'].split('.')[0]} >>",
                                    "Назад"
                                ]
                                break
                            elif buttonMenu[j] == "Сбросить настройки":
                                settings["fullscreen"] = True
                                settings["keys"] = {
                                    "UP": pygame.K_w,
                                    "DOWN": pygame.K_s,
                                    "LEFT": pygame.K_a,
                                    "RIGHT": pygame.K_d,
                                    "JUMP": pygame.K_SPACE,
                                    "DASH": pygame.K_RSHIFT,
                                    "SHOOT": "MOUSE_1"
                                }
                                settings["sound"]["music_volume"] = 15
                                settings["sound"]["sfx_volume"] = 100
                                init_keys()
                                update_sound_volumes()
                                save_settings(settings)
                                buttonMenu = ["Управление", "Музыка и звуки", "Сбросить настройки", "Назад"]
                                break
                            elif buttonMenu[j] == f"<< {settings['sound']['musicTheme'].split('.')[0]} >>":
                                if i.pos[0] * k_posX < WIDTH // 2:
                                    musicIndex -= 1
                                    if musicIndex < 0:
                                        musicIndex = len(musicPlaylist) - 1
                                else:
                                    musicIndex += 1
                                    if musicIndex > len(musicPlaylist) - 1:
                                        musicIndex = 0
                                directory = BASE_PATH
                                settings['sound']['musicTheme'] = musicPlaylist[musicIndex]
                                pygame.mixer.music.load(directory+f"\music\{settings['sound']['musicTheme']}")
                                pygame.mixer.music.play(-1, 1)
                                save_settings(settings)
                                buttonMenu = [
                                    f"Музыка: {settings['sound']['music_volume']}%",
                                    f"Звуки: {settings['sound']['sfx_volume']}%",
                                    f"<< {settings['sound']['musicTheme'].split('.')[0]} >>",
                                    "Назад"
                                ]
                                break
                            elif buttonMenu[j].startswith("UP:"):
                                waitingForKey = True
                                selectedKeyAction = "UP"
                                break
                            elif buttonMenu[j].startswith("DOWN:"):
                                waitingForKey = True
                                selectedKeyAction = "DOWN"
                                break
                            elif buttonMenu[j].startswith("LEFT:"):
                                waitingForKey = True
                                selectedKeyAction = "LEFT"
                                break
                            elif buttonMenu[j].startswith("RIGHT:"):
                                waitingForKey = True
                                selectedKeyAction = "RIGHT"
                                break
                            elif buttonMenu[j].startswith("JUMP:"):
                                waitingForKey = True
                                selectedKeyAction = "JUMP"
                                break
                            elif buttonMenu[j].startswith("DASH:"):
                                waitingForKey = True
                                selectedKeyAction = "DASH"
                                break
                            elif buttonMenu[j].startswith("SHOOT:"):
                                waitingForKey = True
                                selectedKeyAction = "SHOOT"
                                break
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    for j in range(len(buttonMenu)):
                        if buttonMenu[j].startswith("Музыка:") or buttonMenu[j].startswith("Звуки:"):
                            extra_spacing = 25 if "Музыка:" in str(buttonMenu) or "Звуки:" in str(buttonMenu) else 0
                            item_height = menuFont.get_height() + 5 + extra_spacing
                            slider_x = WIDTH // 2 - 100
                            slider_y = HEIGHT // 2 - 50 + j * item_height + menuFont.get_height() + 8
                            slider_width = 200
                            slider_height = 20
                            if (i.pos[0] * k_posX >= slider_x and i.pos[0] * k_posX <= slider_x + slider_width and
                                i.pos[1] * k_posY >= slider_y and i.pos[1] * k_posY <= slider_y + slider_height):
                                dragging_slider = True
                                if buttonMenu[j].startswith("Музыка:"):
                                    dragging_type = "music"
                                else:
                                    dragging_type = "sfx"
                                click_pos = i.pos[0] * k_posX - slider_x
                                new_volume = int((click_pos / slider_width) * 100)
                                new_volume = max(0, min(100, new_volume))
                                if dragging_type == "music":
                                    settings["sound"]["music_volume"] = new_volume
                                elif dragging_type == "sfx":
                                    settings["sound"]["sfx_volume"] = new_volume
                                update_sound_volumes()
                                save_settings(settings)
                                buttonMenu = [
                                    f"Музыка: {settings['sound']['music_volume']}%",
                                    f"Звуки: {settings['sound']['sfx_volume']}%",
                                    f"<< {settings['sound']['musicTheme'].split('.')[0]} >>",
                                    "Назад"
                                ]
                                break
                if waitingForKey:
                    mouse_key = f"MOUSE_{i.button}"
                    conflict = False
                    for action, key in settings["keys"].items():
                        if key == mouse_key and action != selectedKeyAction:
                            conflict = True
                            break
                    if not conflict:
                        settings["keys"][selectedKeyAction] = mouse_key
                        globals()[selectedKeyAction] = mouse_key
                        save_settings(settings)
                        if buttonMenu[0].startswith("UP:"):
                            buttonMenu = [
                                f"UP: {get_key_name(settings['keys']['UP'])}",
                                f"DOWN: {get_key_name(settings['keys']['DOWN'])}",
                                f"LEFT: {get_key_name(settings['keys']['LEFT'])}",
                                f"RIGHT: {get_key_name(settings['keys']['RIGHT'])}",
                                f"JUMP: {get_key_name(settings['keys']['JUMP'])}",
                                f"DASH: {get_key_name(settings['keys']['DASH'])}",
                                f"SHOOT: {get_key_name(settings['keys']['SHOOT'])}",
                                "Назад"
                            ]
                    waitingForKey = False
                    selectedKeyAction = ""
        textMENU = fontMENU.render('НАСТРОЙКИ', 1, GREEN_d)
        screen.blit(textMENU, (WIDTH//2-textMENU.get_width()//2, HEIGHT//4))
        if waitingForKey:
            textWait = menuFont.render(f"Нажмите клавишу для {selectedKeyAction}...", 1, (0, 255, 0))
            screen.blit(textWait, (WIDTH//2-textWait.get_width()//2, HEIGHT//4 - 50))
        for i in range(len(buttonMenu)):
            colorButton = WHITE
            text = menuFont.render(buttonMenu[i], 1, colorButton)
            extra_spacing = 0
            if "Музыка:" in str(buttonMenu) or "Звуки:" in str(buttonMenu):
                extra_spacing = 25
            item_height = text.get_height() + 5 + extra_spacing
            if mouseX > WIDTH // 2 - text.get_width() // 2 \
                    and mouseX < WIDTH // 2 - text.get_width() // 2 + text.get_width() \
                    and mouseY > HEIGHT // 2 - 50 + i * item_height +5 \
                    and mouseY < HEIGHT // 2 - 50 + i * item_height + text.get_height() -5:
                if lastMenuButton != buttonMenu[i]:
                    if not ((buttonMenu[i].split(":")[0] == "Музыка") or (buttonMenu[i].split(":")[0] == "Звуки")):
                        if buttonMenu[i] == f"<< {settings['sound']['musicTheme'].split('.')[0]} >>":
                            if mouseX < WIDTH // 2 - text.get_width() // 2 + 25 \
                                    or mouseX > WIDTH // 2 - text.get_width() // 2 + text.get_width() - 25:
                                scrollSound.play()
                                lastMenuButton = buttonMenu[i]
                        else:
                            scrollSound.play()
                            lastMenuButton = buttonMenu[i]
                if not((buttonMenu[i].split(":")[0] == "Музыка") or (buttonMenu[i].split(":")[0] == "Звуки")):
                    if buttonMenu[i] == f"<< {settings['sound']['musicTheme'].split('.')[0]} >>":
                        if mouseX < WIDTH // 2 - text.get_width() // 2 + 25 \
                                or mouseX > WIDTH // 2 - text.get_width() // 2 + text.get_width() - 25:
                            colorButton = (255, 0, 0)
                    else:
                        colorButton = (255, 0, 0)
            if waitingForKey and selectedKeyAction == buttonMenu[i].split(":")[0]:
                colorButton = (0, 255, 0)
            text = menuFont.render(buttonMenu[i], 1, colorButton)
            screen.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-50+i*item_height))
            if buttonMenu[i].startswith("Музыка:") or buttonMenu[i].startswith("Звуки:"):
                slider_x = WIDTH // 2 - 100
                slider_y = HEIGHT // 2 - 50 + i * item_height + text.get_height() + 8
                slider_width = 200
                slider_height = 10
                if buttonMenu[i].startswith("Музыка:"):
                    current_value = settings["sound"]["music_volume"]
                else:
                    current_value = settings["sound"]["sfx_volume"]
                pygame.draw.rect(screen, (100, 100, 100), (slider_x, slider_y, slider_width, slider_height))
                filled_width = int((current_value / 100) * slider_width)
                pygame.draw.rect(screen, (0, 150, 255), (slider_x, slider_y, filled_width, slider_height))
                handle_x = slider_x + filled_width - 5
                handle_y = slider_y - 5
                pygame.draw.rect(screen, WHITE, (handle_x, handle_y, 10, slider_height + 10))
            if buttonMenu[i] == f"<< {settings['sound']['musicTheme'].split('.')[0]} >>":
                lvlupdraw = 1
                if plateTime < plateSec * FPS:
                    plateTime += 1
                    if plateTime >= plateSec * FPS:
                        plateTime = 0
                for cst in range(0, len(musicPlaylist)):
                    if cst == musicIndex:
                        plateTex = PLATE[min(int(plateTime // (plateSec * FPS / len(PLATE))), len(PLATE) - 1)]
                    else:
                        plateTex = CASSETTE
                    casseteX = WIDTH//2 - len(musicPlaylist) * 25 + cst * 50 + 15 * lvlupdraw
                    casseteY = HEIGHT//2-50+i*item_height + text.get_height() + 5
                    for pl in range(len(plateTex[0])):
                        drawX = casseteX + plateTex[0][pl] * lvlupdraw
                        drawY = casseteY + plateTex[1][pl] * lvlupdraw
                        pygame.draw.rect(screen, plateTex[2][pl], (drawX, drawY, 3 * lvlupdraw, 3 * lvlupdraw))
            if buttonMenu[i] == "Играть" and colorButton == (255, 0, 0):
                textMap = menuFont.render(">"+letMap, 1, (200, 200, 10))
                screen.blit(textMap, (WIDTH // 2 + text.get_width() // 2+5, HEIGHT // 2 - 50 + i * (text.get_height() + 5)))
    elif menu == "maps":
        screen.fill(menuColor)
        timeCadrMenu += 1
        if timeCadrMenu >= FPS * GGRunSec // len(GGRun):
            if cadrMenu + 1 < len(GGRun):
                cadrMenu += 1
            else:
                cadrMenu = 0
            timeCadrMenu = 0
        if cadrMenu + 1 >= len(GGRun):
            cadrMenu = 0
        GGMenu = GGRun[cadrMenu]
        for j in range(len(GGMenu[0])):
            drawX = WIDTH // 2 - Size * 10 // 2 + GGMenu[0][j] * 10
            drawY = HEIGHT // 2 - Size * 10 // 2 + GGMenu[1][j] * 10
            lol = GGMenu[2][j]
            if GGMenu[2][j] == (0, 190, 0):
                lol = (50, 120, 80)
            elif GGMenu[2][j] == (0, 95, 0):
                lol = (10, 45, 20)
            pygame.draw.rect(screen, lol, (drawX, drawY, 30, 30))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    buttonMenu = ["Играть", "Карты", "Редактировать", "Создать", "Настройки", "Выйти"]
                    menu = "menu"
                    scroll = 0
                    clickSound.play()
                if i.key == pygame.K_F11:
                    if fullScreen:
                        screen0 = pygame.display.set_mode(current_size)
                    else:
                        screen0 = pygame.display.set_mode((current_size), pygame.FULLSCREEN)
                    fullScreen = not fullScreen
            if i.type == pygame.MOUSEMOTION:
                mouseX = i.pos[0] * k_posX
                mouseY = i.pos[1] * k_posY
            if i.type == pygame.MOUSEBUTTONUP:
                if i.button == 1:
                    for j in range(len(files[scroll:])):
                        text = menuFont.render(files[j+scroll].split(".")[0], 1, WHITE)
                        if i.pos[0] * k_posX > WIDTH // 2 - text.get_width() // 2 \
                                and i.pos[0] * k_posX < WIDTH // 2 - text.get_width() // 2 + text.get_width() \
                                and i.pos[1] * k_posY > HEIGHT // 2 - 50 + j * (text.get_height() + 5) + 5 \
                                and i.pos[1] * k_posY < HEIGHT // 2 - 50 + j * (text.get_height() + 5) + text.get_height() - 5:
                            clickSound.play()
                            with open(BASE_PATH+'/maps/'+files[j+scroll], 'r') as file:
                                text1 = file.readline()
                                map = ast.literal_eval(text1)
                                text2 = file.readline()
                                x = ast.literal_eval(text2)
                                text3 = file.readline()
                                y = ast.literal_eval(text3)
                                text4 = file.readline()
                                surfX = ast.literal_eval(text4)
                                text5 = file.readline()
                                surfY = ast.literal_eval(text5)
                            spawnX = x
                            spawnY = y
                            spawnSX = surfX
                            spawnSY = surfY
                            letMap = files[j+scroll]
                            menu = "menu"
                            buttonMenu = ["Играть", "Карты", "Редактировать", "Создать", "Настройки", "Выйти"]
                            scroll = 0
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 4:
                    if scroll > 0:
                        scrollSound.play()
                        scroll -= 1
                if i.button == 5:
                    if scroll < len(files) - 7:
                        scrollSound.play()
                        scroll += 1
        fps = int(clock.get_fps())
        textEsc = font.render('Esc', 1, WHITE)
        screen.blit(textEsc, (WIDTH-textEsc.get_width()-10, +10))
        textMENU = fontMENU.render('КАРТЫ', 1, GREEN_d)
        screen.blit(textMENU, (WIDTH // 2 - textMENU.get_width() // 2, HEIGHT // 4))
        for i in range(len(files[scroll:])):
            colorButton = WHITE
            text = menuFont.render(files[i + scroll].split(".")[0], 1, colorButton)
            if mouseX > WIDTH // 2 - text.get_width() // 2 \
                    and mouseX < WIDTH // 2 - text.get_width() // 2 + text.get_width() \
                    and mouseY > HEIGHT // 2 - 50 + i * (text.get_height() + 5) + 5 \
                    and mouseY < HEIGHT // 2 - 50 + i * (text.get_height() + 5) + text.get_height() - 5:
                if lastMenuButton != files[i+scroll]:
                    scrollSound.play()
                    lastMenuButton = files[i+scroll]
                colorButton = (255, 0, 0)
            text = menuFont.render(files[i+scroll].split(".")[0], 1, colorButton)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50 + i * (text.get_height() + 5)))
            level_name = files[i+scroll].split(".")[0]
            stats_text = ""
            if level_name in settings["statistics"]["level_times"]:
                best_time = settings["statistics"]["level_times"][level_name]
                stats_text += f" Время: {format_time(best_time)}"
            if level_name in settings["statistics"]["level_deaths"]:
                deaths = settings["statistics"]["level_deaths"][level_name]
                stats_text += f" | Смерти: {deaths}"
            stats_color = (200, 200, 10) if colorButton == (255, 0, 0) else (150, 150, 150)
            stats_render = font.render(stats_text, 1, stats_color)
            screen.blit(stats_render,
                        (WIDTH // 2 + text.get_width() // 2 + 10, HEIGHT // 2 - 50 + i * (text.get_height() + 5) + 5))
    elif menu == "game":
        '''if gameMode == "surv":
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)'''
        screen.fill((5, 5, 5))
        grav = 1
        stopRun = 0
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE and victoryTime == 2 * FPS:
                    runSound.stop()
                    pygame.mixer.music.set_volume(settings["sound"]["music_volume"] / 100.0)
                    if canCreate == False:
                        pause_on()
                        buttonMenu = ["Продолжить", "Покинуть уровень"]
                    else:
                        buttonMenu = ["Продолжить", "Сохранить", "Покинуть уровень"]
                    menu = "menu"
                if i.key == pygame.K_F11:
                    if fullScreen:
                        screen0 = pygame.display.set_mode(current_size)
                    else:
                        screen0 = pygame.display.set_mode((current_size), pygame.FULLSCREEN)
                    fullScreen = not fullScreen
                if i.key == UP:
                    motionU = "motion"
                    motionD = "stop"
                if i.key == DOWN:
                    motionD = "motion"
                    motionU = "stop"
                if i.key == LEFT:
                    motionL = "motion"
                    motionR = "stop"
                    lastButton = "left"
                if i.key == RIGHT:
                    motionR = "motion"
                    motionL = "stop"
                    lastButton = "right"
                if i.key == JUMP:
                    if canJump:
                        jump = "motion"
                        canJump = False
                        speedG = 0
                        jumpSound.play()
                    if canJumpWallL:
                        jumpWallL = "motion"
                        jump = "stop"
                        canJumpWallL = False
                        speedG = 0
                        spring = 0
                        jumpSound.play()
                    elif canJumpWallR:
                        jumpWallR = "motion"
                        jump = "stop"
                        canJumpWallR = False
                        speedG = 0
                        spring = 0
                        jumpSound.play()
                if i.key == DASH:
                    if canDash:
                        dash = "motion"
                        jump = "stop"
                        jumpWallL = "stop"
                        jumpWallR = "stop"
                        speedJ = J
                        canDash = False
                        speedG = 0
                        grav = 0
                        dashSound.play()
                        if motionU == "motion" and motionR == "motion":
                            NDash = "upright"
                        elif motionU == "motion" and motionL == "motion":
                            NDash = "upleft"
                        elif motionD == "motion" and motionR == "motion":
                            NDash = "downright"
                        elif motionD == "motion" and motionL == "motion":
                            NDash = "downleft"
                        elif motionU == "motion":
                            NDash = "up"
                        elif motionD == "motion":
                            NDash = "down"
                        elif motionL == "motion":
                            NDash = "left"
                        elif motionR == "motion":
                            NDash = "right"
                        else:
                            NDash = lastButton
                if canCreate:
                    if i.key == pygame.K_g:
                        if gameMode == "surv":
                            gameMode = "creat"
                            if "enemyFly" in map:
                                for ret in range(len(map["enemyFly"][0])):
                                    map["enemyFly"][-1][ret] = 0
                                    map["enemyFly"][4][ret] = 0
                                    map["enemyFly"][5][ret] = 0
                                    map["enemyFly"][6][ret] = False
                                    map["enemyFly"][0][ret] = map["enemyFly"][7][0][ret]
                                    map["enemyFly"][1][ret] = map["enemyFly"][7][1][ret]
                                    map["enemyFly"][7][2][ret] = 0
                                    map["enemyFly"][7][3][ret] = 0
                                    map["enemyFly"][8][ret] = 0
                                    map["enemyFly"][9][ret] = hpEnemyFly
                            if "bullets" in map:
                                for ret in range(len(map["bullets"][0])):
                                    map["bullets"][0][ret] = map["bullets"][4][ret]
                                    map["bullets"][1][ret] = map["bullets"][5][ret]
                        else:
                            gameMode = "surv"
                    elif i.key == pygame.K_h:
                        hitbox = not hitbox
                if gameMode == "creat":
                    if i.key == pygame.K_DELETE:
                        for j in range(len(map["enemyFly"]) + 6):
                            if j < 4:
                                for n in range(len(correctObject["block"])):
                                    map["block"][j].pop(correctObject["block"][n])
                                for n in range(len(correctObject["spikes"])):
                                    map["spikes"][j].pop(correctObject["spikes"][n])
                                for n in range(len(correctObject["spring"])):
                                    map["spring"][j].pop(correctObject["spring"][n])
                            if j < 5:
                                for n in range(len(correctObject["background"])):
                                    map["background"][j].pop(correctObject["background"][n])
                                try:
                                    for n in range(len(correctObject["rollback"])):
                                        map["rollback"][j].pop(correctObject["rollback"][n])
                                except:
                                    pass
                                try:
                                    for n in range(len(correctObject["spawnpoint"])):
                                        map["spawnpoint"][j].pop(correctObject["spawnpoint"][n])
                                except:
                                    pass
                                try:
                                    for n in range(len(correctObject["finish"])):
                                        map["finish"][j].pop(correctObject["finish"][n])
                                except:
                                    pass
                            try:
                                for n in range(len(correctObject["bullets"])):
                                    map["bullets"][j].pop(correctObject["bullets"][n])
                            except:
                                pass
                            try:
                                for n in range(len(correctObject["enemyFly"])):
                                    if j >= 7 and j <= 10:
                                        map["enemyFly"][7][j-7].pop(correctObject["enemyFly"][n])
                                    elif j > 10:
                                        map["enemyFly"][j-3].pop(correctObject["enemyFly"][n])
                                    else:
                                        map["enemyFly"][j].pop(correctObject["enemyFly"][n])
                            except:
                                pass
                        correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [], "background": [],
                                         "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}
                        print("\nmap =", map)
                    elif i.key == pygame.K_p:
                        map["spawnpoint"][4] = -1
                        spawnX = x
                        spawnY = y
                        spawnSX = surfX
                        spawnSY = surfY
                    elif i.key == pygame.K_1:
                        createType = 'block'
                    elif i.key == pygame.K_2:
                        createType = 'spikes'
                    elif i.key == pygame.K_3:
                        createType = 'spring'
                    elif i.key == pygame.K_4:
                        createType = 'rollback'
                    elif i.key == pygame.K_5:
                        createType = 'spawnpoint'
                    elif i.key == pygame.K_6:
                        createType = 'bullets'
                    elif i.key == pygame.K_7:
                        createType = 'enemyFly'
                    elif i.key == pygame.K_8:
                        createType = 'finish'
                    if i.key == pygame.K_0 and createType == 'finish':
                        finishPacifist = not finishPacifist
                    '''if i.key == pygame.K_0:
                        createType = 'background'
                    if i.key == pygame.K_F1:
                        createColor = backColor[5]
                    if i.key == pygame.K_F2:
                        createColor = backColor[4]
                    if i.key == pygame.K_F3:
                        createColor = backColor[3]
                    if i.key == pygame.K_F4:
                        createColor = backColor[2]
                    if i.key == pygame.K_F5:
                        createColor = backColor[1]
                    if i.key == pygame.K_F6:
                        createColor = backColor[0]'''
            if i.type == pygame.KEYUP:
                if i.key == pygame.K_w:
                    motionU = "stop"
                if i.key == pygame.K_s:
                    motionD = "stop"
                if i.key == pygame.K_a:
                    motionL = "stop"
                    speed = 0
                if i.key == pygame.K_d:
                    motionR = "stop"
                    speed = 0
                if i.key == pygame.K_SPACE:
                    if jump == "motion" or jumpWallL == "motion" or jumpWallR == "motion":
                        if spring == 0:
                            jump = "stop"
                            jumpWallL = "stop"
                            jumpWallR = "stop"
                            speedG = 0
            if i.type == pygame.MOUSEBUTTONDOWN:
                if len(str(DASH).split("_")) > 1:
                    if i.button == int(DASH.split("_")[1]) and gameMode == "surv":
                        if canDash:
                            dash = "motion"
                            jump = "stop"
                            jumpWallL = "stop"
                            jumpWallR = "stop"
                            speedJ = J
                            canDash = False
                            speedG = 0
                            grav = 0
                            dashSound.play()
                            if motionU == "motion" and motionR == "motion":
                                NDash = "upright"
                            elif motionU == "motion" and motionL == "motion":
                                NDash = "upleft"
                            elif motionD == "motion" and motionR == "motion":
                                NDash = "downright"
                            elif motionD == "motion" and motionL == "motion":
                                NDash = "downleft"
                            elif motionU == "motion":
                                NDash = "up"
                            elif motionD == "motion":
                                NDash = "down"
                            elif motionL == "motion":
                                NDash = "left"
                            elif motionR == "motion":
                                NDash = "right"
                            else:
                                NDash = lastButton
                if len(str(SHOOT).split("_")) > 1:
                    if i.button == int(SHOOT.split("_")[1]) and gameMode == "surv":
                        if canShoot and bullets > 0:
                            shootSound.play()
                            shoot = "motion"
                            canShoot = False
                            bullets -= 1
                            bulletTime = 20
                            timeShoot = GunSec * FPS
                            if bullets == 0:
                                colorBullets = colorBullets2
                        elif bullets <= 0 and canShoot:
                            misfireSound.play()
                if gameMode == "creat":
                    if i.button == 1:
                        if createType != "rollback" and createType != "spawnpoint" and createType != "bullets" and createType != "enemyFly" and createType != "finish":
                            map[createType][0].append(int((i.pos[0] * k_posX+surfX) - (i.pos[0] * k_posX+surfX) % 10))
                            map[createType][1].append(int((i.pos[1] * k_posY+surfY) - (i.pos[1] * k_posY+surfY) % 10))
                        draw = 1
                    elif i.button == 3 and draw != 1:
                        firstMouseX = i.pos[0] * k_posX
                        firstMouseY = i.pos[1] * k_posY
                        draw = 2
                    elif i.button == 4:
                        indCreate = createMenu.index(createType)
                        if indCreate < len(createMenu) - 1:
                            indCreate += 1
                        else:
                            indCreate = 0
                        createType = createMenu[indCreate]
                    elif i.button == 5:
                        indCreate = createMenu.index(createType)
                        if indCreate > 0:
                            indCreate -= 1
                        else:
                            indCreate = len(createMenu) - 1
                        createType = createMenu[indCreate]
                    elif i.button == 2 and createType == 'finish':
                        finishPacifist = not finishPacifist
            if i.type == pygame.MOUSEMOTION:
                if gameMode == "creat":
                    if createType != "rollback" and createType != "spawnpoint" and createType != "bullets" and createType != "enemyFly" and createType != "finish" and draw == 1:
                        mouseX = int((i.pos[0] * k_posX + 10) - (i.pos[0] * k_posX+surfX) % 10)
                        mouseY = int((i.pos[1] * k_posY + 10) - (i.pos[1] * k_posY+surfY) % 10)
                    else:
                        mouseX = i.pos[0] * k_posX
                        mouseY = i.pos[1] * k_posY
                else:
                    mouseX = i.pos[0] * k_posX
                    mouseY = i.pos[1] * k_posY
            if i.type == pygame.MOUSEBUTTONUP:
                if i.button == 1:
                    if gameMode == "creat":
                        if createType != "rollback" and createType != "spawnpoint" and createType != "bullets" and createType != "enemyFly" and createType != "finish":
                            map[createType][2].append(int(i.pos[0] * k_posX+surfX) + 10 - int(i.pos[0] * k_posX+surfX) % 10-(map[createType][0][-1]))
                            map[createType][3].append(int(i.pos[1] * k_posY+surfY) + 10 - int(i.pos[1] * k_posY+surfY) % 10-(map[createType][1][-1]))
                            if map[createType][2][-1] < 0:
                                map[createType][0][-1] = map[createType][0][-1] + map[createType][2][-1]
                                map[createType][2][-1] *= -1
                            if map[createType][3][-1] < 0:
                                map[createType][1][-1] = map[createType][1][-1] + map[createType][3][-1]
                                map[createType][3][-1] *= -1
                        else:
                            try:
                                map[createType][0].append(int(i.pos[0] * k_posX-map[createType][2]//2 + surfX))
                                map[createType][1].append(int(i.pos[1] * k_posY-map[createType][3]//2 + surfY))
                                if createType == "enemyFly":
                                    map[createType][-1].append(0)
                                    map[createType][4].append(0)
                                    map[createType][5].append(0)
                                    map[createType][6].append(False)
                                    map[createType][7][0].append(int(i.pos[0] * k_posX-map[createType][2]//2 + surfX))
                                    map[createType][7][1].append(int(i.pos[1] * k_posY-map[createType][3]//2 + surfY))
                                    map[createType][7][2].append(0)
                                    map[createType][7][3].append(0)
                                    map[createType][8].append(0)
                                    map[createType][9].append(hpEnemyFly)
                                elif createType == "bullets":
                                    map[createType][4].append(int(i.pos[0] * k_posX - map[createType][2] // 2 + surfX))
                                    map[createType][5].append(int(i.pos[1] * k_posY - map[createType][3] // 2 + surfY))
                                elif createType == "finish":
                                    map[createType][4].append(finishPacifist)
                            except:
                                map["bullets"] = [[], [], 16, 16, [], []]
                                map["enemyFly"] = [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []]
                                map["finish"] = [[], [], 24, 24, []]
                                map[createType][0].append(int(i.pos[0] * k_posX - map[createType][2] // 2 + surfX))
                                map[createType][1].append(int(i.pos[1] * k_posY - map[createType][3] // 2 + surfY))
                                if createType == "enemyFly":
                                    map[createType][-1].append(0)
                                    map[createType][4].append(0)
                                    map[createType][5].append(0)
                                    map[createType][6].append(False)
                                    map[createType][7][0].append(int(i.pos[0] * k_posX - map[createType][2]//2 + surfX))
                                    map[createType][7][1].append(int(i.pos[1] * k_posY - map[createType][3]//2 + surfY))
                                    map[createType][7][2].append(0)
                                    map[createType][7][3].append(0)
                                    map[createType][8].append(0)
                                    map[createType][9].append(hpEnemyFly)
                                elif createType == "bullets":
                                    map[createType][4].append(int(i.pos[0] * k_posX - map[createType][2] // 2 + surfX))
                                    map[createType][5].append(int(i.pos[1] * k_posY - map[createType][3] // 2 + surfY))
                                elif createType == "finish":
                                    map[createType][4].append(finishPacifist)
                            if createType == "rollback":
                                map[createType][4].append(0)
                        if createType == "background":
                            map[createType][4].append(createColor)
                        correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [], "background": [],
                                         "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}
                        correctObject[createType] = [-1]
                        draw = -1
                        print("\nmap =", map)
                elif i.button == 3 and draw == 2:
                    if gameMode == "creat":
                        correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [], "background": [],
                                         "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}
                        if firstMouseX > mouseX:
                            mouseX = mouseX + firstMouseX
                            firstMouseX = mouseX - firstMouseX
                            mouseX = mouseX - firstMouseX
                        if firstMouseY > mouseY:
                            mouseY = mouseY + firstMouseY
                            firstMouseY = mouseY - firstMouseY
                            mouseY = mouseY - firstMouseY
                        for j in range(len(map["block"][3])):
                            if map["block"][0][j]+map["block"][2][j]-surfX > firstMouseX \
                                    and map["block"][0][j]-surfX < mouseX \
                                    and map["block"][1][j]+map["block"][3][j]-surfY > firstMouseY \
                                    and map["block"][1][j]-surfY < mouseY:
                                correctObject["block"].append(j)
                        correctObject["block"].sort(reverse=True)
                        for j in range(len(map["spikes"][3])):
                            if map["spikes"][0][j]+map["spikes"][2][j]-surfX > firstMouseX \
                                    and map["spikes"][0][j]-surfX < mouseX \
                                    and map["spikes"][1][j]+map["spikes"][3][j]-surfY > firstMouseY \
                                    and map["spikes"][1][j]-surfY < mouseY:
                                correctObject["spikes"].append(j)
                        correctObject["spikes"].sort(reverse=True)
                        for j in range(len(map["spring"][3])):
                            if map["spring"][0][j]+map["spring"][2][j]-surfX > firstMouseX \
                                    and map["spring"][0][j]-surfX < mouseX \
                                    and map["spring"][1][j]+map["spring"][3][j]-surfY > firstMouseY \
                                    and map["spring"][1][j]-surfY < mouseY:
                                correctObject["spring"].append(j)
                        correctObject["spring"].sort(reverse=True)
                        for j in range(len(map["background"][3])):
                            if map["background"][0][j]+map["background"][2][j]-surfX > firstMouseX \
                                    and map["background"][0][j]-surfX < mouseX \
                                    and map["background"][1][j]+map["background"][3][j]-surfY > firstMouseY \
                                    and map["background"][1][j]-surfY < mouseY:
                                correctObject["background"].append(j)
                        correctObject["background"].sort(reverse=True)
                        for j in range(len(map["rollback"][4])):
                            if map["rollback"][0][j]+map["rollback"][2]-surfX > firstMouseX \
                                    and map["rollback"][0][j]-surfX < mouseX \
                                    and map["rollback"][1][j]+map["rollback"][3]-surfY > firstMouseY \
                                    and map["rollback"][1][j]-surfY < mouseY:
                                correctObject["rollback"].append(j)
                        correctObject["rollback"].sort(reverse=True)
                        for j in range(len(map["spawnpoint"][1])):
                            if map["spawnpoint"][0][j]+map["spawnpoint"][2]-surfX > firstMouseX \
                                    and map["spawnpoint"][0][j]-surfX < mouseX \
                                    and map["spawnpoint"][1][j]+map["spawnpoint"][3]-surfY > firstMouseY \
                                    and map["spawnpoint"][1][j]-surfY < mouseY:
                                correctObject["spawnpoint"].append(j)
                        correctObject["spawnpoint"].sort(reverse=True)
                        try:
                            for j in range(len(map["bullets"][1])):
                                if map["bullets"][0][j]+map["bullets"][2]-surfX > firstMouseX \
                                        and map["bullets"][0][j]-surfX < mouseX \
                                        and map["bullets"][1][j]+map["bullets"][3]-surfY > firstMouseY \
                                        and map["bullets"][1][j]-surfY < mouseY:
                                    correctObject["bullets"].append(j)
                            correctObject["bullets"].sort(reverse=True)
                        except:
                            map["bullets"] = [[], [], 16, 16, [], []]
                        try:
                            for j in range(len(map["enemyFly"][1])):
                                if map["enemyFly"][0][j]+map["enemyFly"][2]-surfX > firstMouseX \
                                        and map["enemyFly"][0][j]-surfX < mouseX \
                                        and map["enemyFly"][1][j]+map["enemyFly"][3]-surfY > firstMouseY \
                                        and map["enemyFly"][1][j]-surfY < mouseY:
                                    correctObject["enemyFly"].append(j)
                            correctObject["enemyFly"].sort(reverse=True)
                        except:
                            map["enemyFly"] = [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []]
                        try:
                            for j in range(len(map["finish"][1])):
                                if map["finish"][0][j] + map["finish"][2] - surfX > firstMouseX \
                                        and map["finish"][0][j] - surfX < mouseX \
                                        and map["finish"][1][j] + map["finish"][3] - surfY > firstMouseY \
                                        and map["finish"][1][j] - surfY < mouseY:
                                    correctObject["finish"].append(j)
                            correctObject["finish"].sort(reverse=True)
                        except:
                            map["finish"] = [[], [], 24, 24, []]
                        draw = -1
        for m in range(1):
            if gameMode == "surv" and victoryTime == 2 * FPS:
                if motionL == "stop" and motionR == "stop":
                    if speed > 0:
                        speed -= maxSpeed / 4
                    if speed <= 0:
                        speed = 0
                    if xO < x:
                        x += speed
                    elif xO > x:
                        x -= speed
                if dash == "stop":
                    if jump == "motion":
                        timeCoyoteR = Coyote
                        timeCoyoteL = Coyote
                        if speedJ-speedG > 0:
                            y -= speedJ
                        else:
                            jump = "stop"
                            speedJ = J
                            spring = 0
                            speedG = 0
                    elif jumpWallL == "motion":
                        timeCoyoteL = Coyote
                        if speedJ-speedG > 0:
                            y -= speedJ
                            if speedJ-speedG > speedJ//1.5:
                                stopRun = 1
                                x -= maxSpeed
                                speed = maxSpeed
                        else:
                            jumpWallL = "stop"
                            speedG = 0
                            speedJ = J
                            spring = 0
                    elif jumpWallR == "motion":
                        timeCoyoteR = Coyote
                        if speedJ-speedG > 0:
                            y -= speedJ
                            if speedJ-speedG > speedJ//1.5:
                                stopRun = 1
                                x += maxSpeed
                                speed = maxSpeed
                        else:
                            jumpWallR = "stop"
                            speedG = 0
                            speedJ = J
                            spring = 0
                    if motionL == "motion" and stopRun == 0:
                        if speed < maxSpeed:
                            speed += maxSpeed / 4
                        else:
                            speed = maxSpeed
                        x -= speed
                    if motionR == "motion" and stopRun == 0:
                        x += speed
                        if speed < maxSpeed:
                            speed += maxSpeed / 4
                        else:
                            speed = maxSpeed
                elif dash == "motion":
                    if timeDash < maxTimeDash:
                        timeDash += 1
                        grav = 0
                        speedG = 0
                        colorGG = PURPLE
                        colorGG2 = PURPLE2
                        x, y, speedG, speed = napravl(NDash, x, y, speedG, speed)
                    else:
                        if NDash != "down" and NDash != "downright" and NDash != "downleft":
                            x, y, speedG, speed = napravl(NDash, x, y, speedG, speed)
                        dash = "stop"
                        grav = 1
                        timeDash = 0
                if shoot == "motion":
                    shoot = "stop"
                    speed //= 2
                    for i in range(-1, 2):
                        flyBullets[0].append(x + Size // 2)
                        flyBullets[1].append(y + Size // 2)
                        flyBullets[2].append(angle + 3 * i)
                        flyBullets[3].append(WHITE)
                if timeShoot > 0:
                    maxSpeed = 2
                    timeShoot -= 1
                    colorBullets = colorBullets2
                    if int((GunSec*FPS-timeShoot)//(GunSec*FPS//len(GUN))) < len(GUN):
                        Gun = GUN[int((GunSec*FPS-timeShoot)//(GunSec*FPS//len(GUN)))]
                else:
                    maxSpeed = 4
                    canShoot = True
                    Gun = GUN[0]
                    if bullets > 0:
                        colorBullets = colorBullets1
            elif gameMode == "creat":
                if motionL == "motion":
                    x -= 10
                elif motionR == "motion":
                    x += 10
                if motionU == "motion":
                    y -= 10
                elif motionD == "motion":
                    y += 10
            bulletDel = []
            for i in range(len(flyBullets[0])):
                sin = math.sin(math.radians(flyBullets[2][i]))
                cos = math.cos(math.radians(flyBullets[2][i]))
                flyBullets[0][i] += speedBullets * cos
                flyBullets[1][i] += speedBullets * sin
                if flyBullets[3][i][0] <= 50:
                    bulletDel.append(i)
                else:
                    flyBullets[3][i] = (flyBullets[3][i][0] - 12, flyBullets[3][i][1] - 12, flyBullets[3][i][2] - 12)
            bulletDel.sort(reverse=True)
            for flyBulDel in bulletDel:
                flyBullets[0].pop(flyBulDel)
                flyBullets[1].pop(flyBulDel)
                flyBullets[2].pop(flyBulDel)
                flyBullets[3].pop(flyBulDel)
        for myBackground in range(1):
            for stM in range(len(smallStarsPos[0])):
                xDrawStar = int((smallStarsPos[0][stM] * kbackground3 - surfX) // kbackground3)
                yDrawStar = int((smallStarsPos[1][stM] * kbackground3 - surfY) // kbackground3)
                if xDrawStar + SmallStarimg.get_width() < 0:
                    smallStarsPos[0][stM] += surfStarsSmall[0] + SmallStarimg.get_width()
                elif xDrawStar > surfStarsSmall[0]:
                    smallStarsPos[0][stM] -= surfStarsSmall[0] + SmallStarimg.get_width()
                if yDrawStar + SmallStarimg.get_height() < 0:
                    smallStarsPos[1][stM] += surfStarsSmall[1] + SmallStarimg.get_height()
                elif yDrawStar > surfStarsSmall[1]:
                    smallStarsPos[1][stM] -= surfStarsSmall[1] + SmallStarimg.get_height()
                if xDrawStar <= WIDTH and xDrawStar+SmallStarimg.get_width() >= 0 and yDrawStar <= HEIGHT and yDrawStar+SmallStarimg.get_height() >= 0:
                    screen.blit(SmallStarimg, (xDrawStar, yDrawStar))
            if shootingStarBigTime < timeToFallStar * FPS:
                shootingStarBigTime += 1
            else:
                shootingStarBigTime = -ShootingStarBigSec*FPS
                starSizeBig = randint(1, 2)
                timeToFallStar = randint(ShootingStarBigTSp[0], ShootingStarBigTSp[1])
                if starSizeBig == 2:
                    xShSB = surfX + (randint(-sizeShStB // 3, WIDTH - sizeShStB // 3 * 2))*kbackground2
                    yShSB = surfY + (randint(-sizeShStB // 3, HEIGHT - sizeShStB // 3 * 2))*kbackground2
                else:
                    xShSB = surfX + (randint(-sizeShStB // 3 // kShSt, WIDTH - sizeShStB // 3 * 2 // kShSt)) * kbackground2
                    yShSB = surfY + (randint(-sizeShStB // 3 // kShSt, HEIGHT - sizeShStB // 3 * 2 // kShSt)) * kbackground2
            if shootingStarBigTime < 0:
                cadrShStB = len(ShootingStarBigimg) - min(int(-shootingStarBigTime // (ShootingStarBigSec * FPS / len(ShootingStarBigimg))),
                                len(ShootingStarBigimg) - 1) - 1
                if starSizeBig == 2:
                    drawStarTex = ShootingStarBigimg[cadrShStB]
                    xDrawStar = int((xShSB - surfX) // kbackground2) + min(ShootingStarBig[cadrShStB][0])*kShSt
                    yDrawStar = int((yShSB - surfY) // kbackground2) + min(ShootingStarBig[cadrShStB][1])*kShSt
                else:
                    drawStarTex = ShootingStarSmallimg[cadrShStB]
                    xDrawStar = int((xShSB - surfX) // kbackground2) + min(ShootingStarSmall[cadrShStB][0])
                    yDrawStar = int((yShSB - surfY) // kbackground2) + min(ShootingStarSmall[cadrShStB][1])
                screen.blit(drawStarTex, (xDrawStar, yDrawStar))
            blink = False
            if timeBlinkStar < BigStarSec * FPS:
                timeBlinkStar += 1
            else:
                timeBlinkStar = 0
                blink = True
            for stB in range(len(bigStarsPos[0])):
                if blink:
                    bigStarsPos[2][stB] = not bigStarsPos[2][stB]
                xDrawStar = int((bigStarsPos[0][stB]*kbackground2 - surfX) // kbackground2)
                yDrawStar = int((bigStarsPos[1][stB]*kbackground2 - surfY) // kbackground2)
                if bigStarsPos[2][stB]:
                    bigStarText = BigStarimg[0]
                else:
                    bigStarText = BigStarimg[1]
                    xDrawStar += (BigStarimg[0].get_width() - BigStarimg[1].get_width()) // 2
                    yDrawStar += (BigStarimg[0].get_height() - BigStarimg[1].get_height()) // 2
                if xDrawStar + bigStarText.get_width() < 0:
                    bigStarsPos[0][stB] += surfStarsBig[0] + bigStarText.get_width()
                elif xDrawStar > surfStarsBig[0]:
                    bigStarsPos[0][stB] -= surfStarsBig[0] + bigStarText.get_width()
                if yDrawStar + bigStarText.get_height() < 0:
                    bigStarsPos[1][stB] += surfStarsBig[1] + bigStarText.get_height()
                elif yDrawStar > surfStarsBig[1]:
                    bigStarsPos[1][stB] -= surfStarsBig[1] + bigStarText.get_height()
                if xDrawStar <= WIDTH and xDrawStar+bigStarText.get_width() >= 0 and yDrawStar <= HEIGHT and yDrawStar+bigStarText.get_height() >= 0:
                    screen.blit(bigStarText, (xDrawStar, yDrawStar))
            xDrawBack = int((xBackground - surfX) / kbackground1)
            yDrawBack = int((yBackground - surfY) / kbackground1)
            if xDrawBack + PlanetBackgroundimg.get_width() + 50 < 0:
                xBackground += (WIDTH + 100 + PlanetBackgroundimg.get_width()) * kbackground1
            elif xDrawBack - 50 > WIDTH:
                xBackground -= (WIDTH + 100 + PlanetBackgroundimg.get_width()) * kbackground1
            if yDrawBack + PlanetBackgroundimg.get_height() + 50 < 0:
                yBackground += (HEIGHT + 100 + PlanetBackgroundimg.get_height()) * kbackground1
            elif yDrawBack - 50 > HEIGHT:
                yBackground -= (HEIGHT + 100 + PlanetBackgroundimg.get_height()) * kbackground1
            xDrawLight = xDrawBack + 11 * 6
            yDrawLight = yDrawBack + 27 * 6
            screen.blit(PlanetLight,
                        (xDrawLight - PlanetLight.get_width() // 2, yDrawLight - PlanetLight.get_height() // 2))
            screen.blit(PlanetBackgroundimg, (xDrawBack, yDrawBack))
        for G in range(1):
            if victoryTime < 2 * FPS:
                victoryTime -= 1
                if victoryTime == 0:
                    victoryTime = 2 * FPS
                    runSound.stop()
                    buttonMenu = ["Карты", "Покинуть уровень"]
                    menu = "menu"
                    pygame.mixer.music.set_volume(settings["sound"]["music_volume"] / 100.0)
                    canCreate = True
                    spawnX = TrueX
                    spawnY = TrueY
                    x = spawnX
                    y = spawnY
                    xO = x
                    yO = y
                    surfX = 0
                    surfY = 0
                    spawnSX = surfX
                    spawnSY = surfY
                    motionL = 'stop'
                    motionR = 'stop'
                    motionU = 'stop'
                    motionD = 'stop'
                    dash = 'stop'
                    jump = 'stop'
                    jumpWallL = "stop"
                    jumpWallR = "stop"
                    speed = 0
                    maxSpeed = 4
                    speedG = 0
                    timeDash = 0
                    canJump = False
                    canJumpWallR = False
                    canJumpWallL = False
                    canDash = False
                    canShoot = True
                    timeShoot = 0
                    bullets = 0
                    bulletsCadr = bullets * 2
                    bulletTime = 0
                    colorBullets = colorBullets2
                    map = {"block": [[], [], [], []], "spikes": [[], [], [], []], "spring": [[], [], [], []],
                           "rollback": [[], [], 8, 8, []], "background": [[], [], [], [], []],
                           "spawnpoint": [[], [], 21, 21, -1], "bullets": [[], [], 15, 15, [], []],
                           "enemyFly": [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []],
                           "finish": [[], [], 24, 24]}
                    correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [],
                                     "background": [], "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}
                    createType = "block"
                    letMap = "none"
            if gameMode == "surv" and victoryTime == 2 * FPS:
                if grav == 1:
                    canJump = False
                    canJumpWallL = False
                    canJumpWallR = False
                    y += speedG
                    if speedG < speedJ:
                        speedG += g
                    elif speedG > speedJ:
                        speedG = speedJ
                if y >= minY-Size:
                    y = minY-Size
                    grav = 0
                    speedG = 0
                    timeCoyoteL = Coyote
                    timeCoyoteR = Coyote
                    canJump = True
                    canDash = True
                    canJumpWallL = False
                    canJumpWallR = False
                    if y > minY - Size:
                        dash = "stop"
                        timeDash = 0
                bulFlex = []
                for bul in range(len(flyBullets[0])):
                    sin = math.sin(math.radians(flyBullets[2][bul]))
                    cos = math.cos(math.radians(flyBullets[2][bul]))
                    if flyBullets[1][bul] > minY:
                        bulFlex.append(bul)
                        hitWallSound.play()
                bulFlex.sort(reverse=True)
                for bulFlexDel in bulFlex:
                    flyBullets[0].pop(bulFlexDel)
                    flyBullets[1].pop(bulFlexDel)
                    flyBullets[2].pop(bulFlexDel)
                    flyBullets[3].pop(bulFlexDel)
                try:
                    for enem in range(len(map["enemyFly"][1])):
                        if map["enemyFly"][9][enem] <= 0:
                            continue
                        if map["enemyFly"][1][enem] >= minY - map["enemyFly"][2]:
                            map["enemyFly"][1][enem] = minY - map["enemyFly"][2]
                except:
                    pass
                FlagWall = False
                if len(map["block"][0]) == 0:
                    try:
                        for enem in range(len(map["enemyFly"][1])):
                            if map["enemyFly"][9][enem] <= 0:
                                continue
                            if (((x - map["enemyFly"][0][enem]) ** 2 + (y - map["enemyFly"][1][enem]) ** 2) ** 0.5 <= lengthSmell) \
                                    or (((x - map["enemyFly"][0][enem]) ** 2 + (y - map["enemyFly"][1][enem]) ** 2) ** 0.5 <= lengthFallSmell \
                                    and map["enemyFly"][8][enem] > 0):
                                map["enemyFly"][4][enem] = x
                                map["enemyFly"][5][enem] = y
                                if map["enemyFly"][6][enem] == False:
                                    map["enemyFly"][6][enem] = True
                                    if map["enemyFly"][8][enem] == 0:
                                        map["enemyFly"][8][enem] = timerStan
                                        startEnemyFlySound.play()
                            else:
                                if map["enemyFly"][6][enem]:
                                    map["enemyFly"][6][enem] = False
                    except:
                        pass
                else:
                    for i in range(len(map["block"][0])):
                        bulFlex = []
                        for bul in range(len(flyBullets[0])):
                            sin = math.sin(math.radians(flyBullets[2][bul]))
                            cos = math.cos(math.radians(flyBullets[2][bul]))
                            for hit in range(3):
                                hitLen = lengthBullets // 2 * hit
                                if flyBullets[1][bul] - hitLen * sin >= map["block"][1][i] and flyBullets[1][bul] - hitLen * sin < map["block"][1][i] + map["block"][3][i] \
                                        and flyBullets[0][bul] - hitLen * cos > map["block"][0][i] and flyBullets[0][bul] - hitLen * cos < map["block"][0][i] + map["block"][2][i]:
                                    bulFlex.append(bul)
                                    hitWallSound.play()
                                    break
                        bulFlex.sort(reverse=True)
                        for bulFlexDel in bulFlex:
                            flyBullets[0].pop(bulFlexDel)
                            flyBullets[1].pop(bulFlexDel)
                            flyBullets[2].pop(bulFlexDel)
                            flyBullets[3].pop(bulFlexDel)
                        try:
                            for enem in range(len(map["enemyFly"][1])):
                                if map["enemyFly"][9][enem] <= 0:
                                    continue
                                lengthEnemyTrue = ((map["enemyFly"][4][enem] - map["enemyFly"][0][enem]) ** 2 + (
                                        map["enemyFly"][5][enem] - map["enemyFly"][1][enem]) ** 2) ** 0.5
                                xEnemSpeed = (map["enemyFly"][4][enem] - map["enemyFly"][0][enem]) / lengthEnemyTrue * speedEnemy
                                yEnemSpeed = (map["enemyFly"][5][enem] - map["enemyFly"][1][enem]) / lengthEnemyTrue * speedEnemy
                                if map["enemyFly"][1][enem] + map["enemyFly"][3] > map["block"][1][i] - helpEnemy and \
                                        map["enemyFly"][1][enem] < map["block"][1][i] + map["block"][3][i] + helpEnemy \
                                        and map["enemyFly"][0][enem] + map["enemyFly"][2] > map["block"][0][i] - helpEnemy and \
                                        map["enemyFly"][0][enem] < map["block"][0][i] + map["block"][2][i] + helpEnemy:
                                    if math.fabs((map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - map["block"][1][
                                        i]) < math.fabs((map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - (
                                            map["block"][1][i] + map["block"][3][i])) \
                                            and math.fabs(
                                        (map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - map["block"][1][
                                            i]) < math.fabs((map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (
                                            map["block"][0][i] + map["block"][2][i])) \
                                            and math.fabs(
                                        (map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - map["block"][1][
                                            i]) < math.fabs(
                                        (map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (map["block"][0][i])):
                                        map["enemyFly"][1][enem] = map["block"][1][i] - map["enemyFly"][3]
                                        if map["enemyFly"][6][enem] == False:
                                            if math.fabs(xEnemSpeed) <= 0.01:
                                                if map["enemyFly"][4][enem] < map["enemyFly"][0][enem]:
                                                    map["enemyFly"][0][enem] -= 1.5
                                                else:
                                                    map["enemyFly"][0][enem] += 1.5
                                                map["enemyFly"][4][enem] = map["enemyFly"][0][enem]
                                                map["enemyFly"][5][enem] = map["enemyFly"][1][enem]
                                    elif math.fabs((map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - (
                                            map["block"][1][i] + map["block"][3][i])) < math.fabs(
                                        (map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - map["block"][1][i]) \
                                            and math.fabs((map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - (
                                            map["block"][1][i] + map["block"][3][i])) < math.fabs(
                                        (map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (
                                                map["block"][0][i] + map["block"][2][i])) \
                                            and math.fabs((map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - (
                                            map["block"][1][i] + map["block"][3][i])) < math.fabs(
                                        (map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (map["block"][0][i])):
                                        map["enemyFly"][1][enem] = map["block"][1][i] + map["block"][3][i]
                                        if map["enemyFly"][6][enem] == False:
                                            if math.fabs(xEnemSpeed) <= 0.01:
                                                if map["enemyFly"][4][enem] < map["enemyFly"][0][enem]:
                                                    map["enemyFly"][0][enem] -= 1.5
                                                else:
                                                    map["enemyFly"][0][enem] += 1.5
                                                map["enemyFly"][4][enem] = map["enemyFly"][0][enem]
                                                map["enemyFly"][5][enem] = map["enemyFly"][1][enem]
                                    elif math.fabs((map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (
                                            map["block"][0][i] + map["block"][2][i])) < math.fabs(
                                        (map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - map["block"][1][i]) \
                                            and math.fabs((map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (
                                            map["block"][0][i] + map["block"][2][i])) < math.fabs(
                                        (map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - (
                                                map["block"][1][i] + map["block"][3][i])) \
                                            and math.fabs((map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (
                                            map["block"][0][i] + map["block"][2][i])) < math.fabs(
                                        (map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (map["block"][0][i])):
                                        map["enemyFly"][0][enem] = map["block"][0][i] + map["block"][2][i]
                                        if map["enemyFly"][6][enem] == False:
                                            if math.fabs(yEnemSpeed) <= 0.01:
                                                if map["enemyFly"][5][enem] < map["enemyFly"][1][enem]:
                                                    map["enemyFly"][1][enem] -= 1.5
                                                else:
                                                    map["enemyFly"][1][enem] += 1.5
                                                map["enemyFly"][4][enem] = map["enemyFly"][0][enem]
                                                map["enemyFly"][5][enem] = map["enemyFly"][1][enem]
                                    elif math.fabs((map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (
                                            map["block"][0][i])) < math.fabs(
                                        (map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - map["block"][1][i]) \
                                            and math.fabs((map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (
                                            map["block"][0][i])) < math.fabs(
                                        (map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (
                                                map["block"][0][i] + map["block"][2][i])) \
                                            and math.fabs((map["enemyFly"][0][enem] + map["enemyFly"][2] // 2) - (
                                            map["block"][0][i])) < math.fabs(
                                        (map["enemyFly"][1][enem] + map["enemyFly"][3] // 2) - (
                                                map["block"][1][i] + map["block"][3][i])):
                                        map["enemyFly"][0][enem] = map["block"][0][i] - map["enemyFly"][2]
                                        if map["enemyFly"][6][enem] == False:
                                            if math.fabs(yEnemSpeed) <= 0.01:
                                                if map["enemyFly"][5][enem] < map["enemyFly"][1][enem]:
                                                    map["enemyFly"][1][enem] -= 1.5
                                                else:
                                                    map["enemyFly"][1][enem] += 1.5
                                                map["enemyFly"][4][enem] = map["enemyFly"][0][enem]
                                                map["enemyFly"][5][enem] = map["enemyFly"][1][enem]
                        except:
                            pass
                        if y+Size >= map["block"][1][i] and y < map["block"][1][i]+map["block"][3][i] \
                                and x+Size > map["block"][0][i] and x < map["block"][0][i]+map["block"][2][i] and yO <= y \
                                and xO+Size > map["block"][0][i] and xO < map["block"][0][i]+map["block"][2][i]:
                            speedJ = J
                            y = map["block"][1][i]-Size
                            grav = 0
                            speedG = 0
                            canJump = True
                            canDash = True
                            canJumpWallL = False
                            canJumpWallR = False
                            timeCoyoteL = Coyote
                            timeCoyoteR = Coyote
                            if y + Size > map["block"][1][i]:
                                dash = "stop"
                                timeDash = 0
                        elif y+Size > map["block"][1][i] and y < map["block"][1][i]+map["block"][3][i] \
                                and x+Size > map["block"][0][i] and x < map["block"][0][i]+map["block"][2][i] and yO > y \
                                and xO+Size > map["block"][0][i] and xO < map["block"][0][i]+map["block"][2][i]:
                            jump = "stop"
                            speedJ = J
                            jumpWallL = "stop"
                            jumpWallR = "stop"
                            y = map["block"][1][i]+map["block"][3][i]
                            speedG = 0
                            dash = "stop"
                            timeDash = 0
                            canJumpWallL = False
                            canJumpWallR = False
                        if x+Size > map["block"][0][i] and x < map["block"][0][i]+map["block"][2][i] \
                                and y+Size > map["block"][1][i] and y < map["block"][1][i]+map["block"][3][i] and xO < x \
                                and yO+Size > map["block"][1][i] and yO < map["block"][1][i]+map["block"][3][i]:
                            x = map["block"][0][i]-Size
                            speed = 0.1
                            dash = "stop"
                            speedJ = J
                            timeDash = 0
                            canJumpWallL = True
                            timeCoyoteL = 0
                            jumpWallL = "stop"
                            FlagWall = True
                            if jump == 'stop' and jumpWallR == "stop" and jumpWallL == "stop":
                                speedG = 2
                        elif x+Size > map["block"][0][i] and x < map["block"][0][i]+map["block"][2][i] \
                                and y+Size > map["block"][1][i] and y < map["block"][1][i]+map["block"][3][i] and xO > x \
                                and yO+Size > map["block"][1][i] and yO < map["block"][1][i]+map["block"][3][i]:
                            x = map["block"][0][i]+map["block"][2][i]
                            speed = 0.1
                            dash = "stop"
                            speedJ = J
                            timeDash = 0
                            canJumpWallR = True
                            timeCoyoteR = 0
                            jumpWallR = "stop"
                            FlagWall = True
                            if jump == 'stop' and jumpWallR == "stop" and jumpWallL == "stop":
                                speedG = 2
                        if x + Size + 6 > map["block"][0][i] and x < map["block"][0][i] + map["block"][2][i] \
                                and y + Size > map["block"][1][i] and y < map["block"][1][i] + map["block"][3][i] and xO <= x \
                                and yO + Size > map["block"][1][i] and yO < map["block"][1][i] + map["block"][3][i]:
                            if canJump == False:
                                canJumpWallL = True
                        elif x + Size > map["block"][0][i] and x - 6 < map["block"][0][i] + map["block"][2][i] \
                                and y + Size > map["block"][1][i] and y < map["block"][1][i] + map["block"][3][i] and xO >= x \
                                and yO + Size > map["block"][1][i] and yO < map["block"][1][i] + map["block"][3][i]:
                            if canJump == False:
                                canJumpWallR = True
                    try:
                        for enem in range(len(map["enemyFly"][1])):
                            if map["enemyFly"][9][enem] <= 0:
                                continue
                            lengthEnemyTrue = ((x - map["enemyFly"][0][enem]) ** 2 + (
                                    y - map["enemyFly"][1][enem]) ** 2) ** 0.5
                            if (lengthEnemyTrue <= lengthSmell) \
                                    or (lengthEnemyTrue <= lengthFallSmell and map["enemyFly"][8][enem] > 0):
                                FWallEnemy = True
                                hitEnemy = [0, 0, 0, 0]
                                if x - map["enemyFly"][0][enem] != 0:
                                    kFun = (y - map["enemyFly"][1][enem]) / (x - map["enemyFly"][0][enem])
                                else:
                                    kFun = 10**10
                                if kFun == 0:
                                    kFun = 10**(-10)
                                bFun = map["enemyFly"][1][enem]
                                dFun = map["enemyFly"][0][enem]
                                fourth = [0, 0]
                                if hitbox and canCreate:
                                    pygame.draw.line(screen, pygame.Color("blue"),
                                                     [x + Size // 2 - surfX, y + Size // 2 - surfY],
                                                     [map["enemyFly"][0][enem] + Size // 2 - surfX,
                                                      map["enemyFly"][1][enem] + Size // 2 - surfY], 1)
                                if x > map["enemyFly"][0][enem]:
                                    hitEnemy[0] = map["enemyFly"][0][enem]
                                    hitEnemy[2] = x + Size
                                    fourth[0] = 1
                                else:
                                    hitEnemy[0] = x
                                    hitEnemy[2] = map["enemyFly"][0][enem]+map["enemyFly"][2]
                                    fourth[0] = 2
                                if y > map["enemyFly"][1][enem]:
                                    hitEnemy[1] = map["enemyFly"][1][enem]
                                    hitEnemy[3] = y + Size
                                    fourth[1] = 1
                                else:
                                    hitEnemy[1] = y
                                    hitEnemy[3] = map["enemyFly"][1][enem] + map["enemyFly"][3]
                                    fourth[1] = 2
                                fixX = 0
                                if fourth == [1, 1]:
                                    fixX = Size
                                elif fourth == [2, 2]:
                                    fixX = Size
                                for i in range(len(map["block"][0])):
                                    if not(hitEnemy[0] < map["block"][0][i]+map["block"][2][i] and hitEnemy[2] > map["block"][0][i] \
                                        and hitEnemy[1] < map["block"][1][i]+map["block"][3][i] and hitEnemy[3] > map["block"][1][i]):
                                        continue
                                    if lengthEnemyTrue < 10:
                                        map["enemyFly"][4][enem] = x
                                        map["enemyFly"][5][enem] = y
                                        if map["enemyFly"][6][enem] == False:
                                            map["enemyFly"][6][enem] = True
                                            if map["enemyFly"][8][enem] == 0:
                                                map["enemyFly"][8][enem] = timerStan
                                                startEnemyFlySound.play()
                                            break
                                    else:
                                        for doble in range(2):
                                            if fourth[0] == 1:
                                                if map["block"][1][i] <= (map["block"][0][i]-dFun-fixX-doble*(Size-fixX*2)) * kFun+bFun+doble*Size <= map["block"][1][i] + map["block"][3][i]:
                                                    FWallEnemy = False
                                                    if hitbox and canCreate:
                                                        pygame.draw.line(screen, pygame.Color("red"), [map["enemyFly"][0][enem]+fixX+doble*(Size-fixX*2)-surfX, map["enemyFly"][1][enem]+doble*Size-surfY],
                                                                         [map["block"][0][i]-surfX, (map["block"][0][i]-dFun-fixX-doble*(Size-fixX*2)) * kFun+bFun+doble*Size-surfY], 1)
                                                    else:
                                                        break
                                            else:
                                                if map["block"][1][i] <= (map["block"][0][i]+map["block"][2][i]-dFun-fixX-doble*(Size-fixX*2)) * kFun+bFun+doble*Size <= map["block"][1][i] + map["block"][3][i]:
                                                    FWallEnemy = False
                                                    if hitbox and canCreate:
                                                        pygame.draw.line(screen, pygame.Color("red"),
                                                                         [map["enemyFly"][0][enem]+fixX+doble*(Size-fixX*2) - surfX,
                                                                          map["enemyFly"][1][enem]+doble*Size - surfY],
                                                                         [map["block"][0][i]+map["block"][2][i] - surfX, (map["block"][0][i]+map["block"][2][i]-dFun-fixX-doble*(Size-fixX*2)) * kFun+bFun+doble*Size - surfY], 1)
                                                    else:
                                                        break
                                            if fourth[1] == 1:
                                                if map["block"][0][i] <= (map["block"][1][i]-bFun-doble*Size) / kFun + dFun+fixX+doble*(Size-fixX*2) <= map["block"][0][i] + map["block"][2][i]:
                                                    FWallEnemy = False
                                                    if hitbox and canCreate:
                                                        pygame.draw.line(screen, pygame.Color("red"),
                                                                         [map["enemyFly"][0][enem]+fixX+doble*(Size-fixX*2) - surfX,
                                                                          map["enemyFly"][1][enem]+doble*Size - surfY],
                                                                         [(map["block"][1][i]-bFun-doble*Size) / kFun + dFun+fixX+doble*(Size-fixX*2) - surfX,
                                                                          map["block"][1][i] - surfY], 1)
                                                    else:
                                                        break
                                            else:
                                                if map["block"][0][i] <= (map["block"][1][i]+map["block"][3][i]-bFun-doble*Size) / kFun + dFun+fixX+doble*(Size-fixX*2) <= map["block"][0][i] + map["block"][2][i]:
                                                    FWallEnemy = False
                                                    if hitbox and canCreate:
                                                        pygame.draw.line(screen, pygame.Color("red"),
                                                                         [map["enemyFly"][0][enem]+fixX+doble*(Size-fixX*2) - surfX,
                                                                          map["enemyFly"][1][enem]+doble*Size - surfY],
                                                                         [(map["block"][1][i]+map["block"][3][i]-bFun-doble*Size) / kFun + dFun+fixX+doble*(Size-fixX*2) - surfX, map["block"][1][i]+map["block"][3][i] - surfY], 1)
                                                    else:
                                                        break
                                        if FWallEnemy == False:
                                            break
                                if FWallEnemy:
                                    map["enemyFly"][4][enem] = x
                                    map["enemyFly"][5][enem] = y
                                    if map["enemyFly"][6][enem] == False:
                                        map["enemyFly"][6][enem] = True
                                        if map["enemyFly"][8][enem] == 0:
                                            map["enemyFly"][8][enem] = timerStan
                                            startEnemyFlySound.play()
                                else:
                                    if map["enemyFly"][6][enem]:
                                        map["enemyFly"][6][enem] = False
                            else:
                                if map["enemyFly"][6][enem]:
                                    map["enemyFly"][6][enem] = False
                    except:
                        pass
                try:
                    for enem in range(len(map["enemyFly"][1])):
                        if map["enemyFly"][9][enem] <= 0:
                            continue
                        bulFlex = []
                        for bul in range(len(flyBullets[0])):
                            sin = math.sin(math.radians(flyBullets[2][bul]))
                            cos = math.cos(math.radians(flyBullets[2][bul]))
                            for hit in range(3):
                                hitLen = lengthBullets // 2 * hit
                                if flyBullets[1][bul] - hitLen * sin >= map["enemyFly"][1][enem] \
                                        and flyBullets[1][bul] - hitLen * sin < map["enemyFly"][1][enem] + map["enemyFly"][3] \
                                        and flyBullets[0][bul] - hitLen * cos > map["enemyFly"][0][enem] \
                                        and flyBullets[0][bul] - hitLen * cos < map["enemyFly"][0][enem] + map["enemyFly"][2]:
                                    bulFlex.append(bul)
                                    hitEnemSound.play()
                                    map["enemyFly"][7][2][enem] = (flyBullets[2][bul] + map["enemyFly"][7][2][enem]) / 2
                                    map["enemyFly"][7][3][enem] += speedBullets // 6
                                    map["enemyFly"][6][enem] = True
                                    map["enemyFly"][8][enem] = timerStan
                                    map["enemyFly"][4][enem] = x
                                    map["enemyFly"][5][enem] = y
                                    map["enemyFly"][9][enem] -= damage
                                    if map["enemyFly"][9][enem] <= 0:
                                        map["enemyFly"][9][enem] = 0
                                        dieEnemySound.play()
                                    break
                        bulFlex.sort(reverse=True)
                        for bulFlexDel in bulFlex:
                            flyBullets[0].pop(bulFlexDel)
                            flyBullets[1].pop(bulFlexDel)
                            flyBullets[2].pop(bulFlexDel)
                            flyBullets[3].pop(bulFlexDel)
                        if map["enemyFly"][7][3][enem] > 0:
                            sin = math.sin(math.radians(map["enemyFly"][7][2][enem]))
                            cos = math.cos(math.radians(map["enemyFly"][7][2][enem]))
                            map["enemyFly"][0][enem] += map["enemyFly"][7][3][enem] * cos
                            map["enemyFly"][1][enem] += map["enemyFly"][7][3][enem] * sin
                            map["enemyFly"][7][3][enem] -= map["enemyFly"][7][3][enem] / 10
                        else:
                            map["enemyFly"][7][2][enem] = 0
                            map["enemyFly"][7][3][enem] = 0
                except:
                    pass
                if FlagWall:
                    if playSoundSlide == 1:
                        runSound.play(-1)
                        playSoundSlide = 0
                else:
                    if playSoundSlide == 0:
                        runSound.stop()
                        playSoundSlide = 1
                for i in range(len(map["spikes"][0])):
                    bulFlex = []
                    for bul in range(len(flyBullets[0])):
                        sin = math.sin(math.radians(flyBullets[2][bul]))
                        cos = math.cos(math.radians(flyBullets[2][bul]))
                        for hit in range(3):
                            hitLen = lengthBullets // 2 * hit
                            if flyBullets[1][bul] - hitLen * sin >= map["spikes"][1][i] and flyBullets[1][
                                bul] - hitLen * sin < map["spikes"][1][i] + map["spikes"][3][i] \
                                    and flyBullets[0][bul] - hitLen * cos > map["spikes"][0][i] and flyBullets[0][
                                bul] - hitLen * cos < map["spikes"][0][i] + map["spikes"][2][i]:
                                bulFlex.append(bul)
                                hitWallSound.play()
                                break
                    bulFlex.sort(reverse=True)
                    for bulFlexDel in bulFlex:
                        flyBullets[0].pop(bulFlexDel)
                        flyBullets[1].pop(bulFlexDel)
                        flyBullets[2].pop(bulFlexDel)
                        flyBullets[3].pop(bulFlexDel)
                    if y + Size > map["spikes"][1][i]+5 and y < map["spikes"][1][i] + map["spikes"][3][i]-5 \
                    and x + Size > map["spikes"][0][i]+5 and x < map["spikes"][0][i] + map["spikes"][2][i]-5:
                        if canCreate == False:
                            add_death()
                        dieSound.play()
                        x = spawnX
                        y = spawnY
                        xO = x
                        yO = y
                        surfX = spawnSX
                        surfY = spawnSY
                        motionL = 'stop'
                        motionR = 'stop'
                        motionU = 'stop'
                        motionD = 'stop'
                        dash = 'stop'
                        jump = 'stop'
                        jumpWallL = "stop"
                        jumpWallR = "stop"
                        speed = 0
                        speedG = 0
                        speedJ = J
                        maxSpeed = 4
                        timeShoot = 0
                        canShoot = True
                        Gun = GUN[0]
                        if bullets > 0:
                            colorBullets = colorBullets1
                        timeDash = 0
                        canJump = False
                        canJumpWallR = False
                        canJumpWallL = False
                        canDash = False
                        for j in range(len(map["rollback"][4])):
                            map["rollback"][4][j] = 0
                        if "enemyFly" in map:
                            for ret in range(len(map["enemyFly"][0])):
                                if map["enemyFly"][9][ret] > 0:
                                    map["enemyFly"][-1][ret] = 0
                                    map["enemyFly"][4][ret] = 0
                                    map["enemyFly"][5][ret] = 0
                                    map["enemyFly"][6][ret] = False
                                    map["enemyFly"][0][ret] = map["enemyFly"][7][0][ret]
                                    map["enemyFly"][1][ret] = map["enemyFly"][7][1][ret]
                                    map["enemyFly"][7][2][ret] = 0
                                    map["enemyFly"][7][3][ret] = 0
                                    map["enemyFly"][8][ret] = 0
                for i in range(len(map["spring"][0])):
                    bulFlex = []
                    for bul in range(len(flyBullets[0])):
                        sin = math.sin(math.radians(flyBullets[2][bul]))
                        cos = math.cos(math.radians(flyBullets[2][bul]))
                        for hit in range(3):
                            hitLen = lengthBullets // 2 * hit
                            if flyBullets[1][bul] - hitLen * sin >= map["spring"][1][i] and flyBullets[1][
                                bul] - hitLen * sin < map["spring"][1][i] + map["spring"][3][i] \
                                    and flyBullets[0][bul] - hitLen * cos > map["spring"][0][i] and flyBullets[0][
                                bul] - hitLen * cos < map["spring"][0][i] + map["spring"][2][i]:
                                bulFlex.append(bul)
                                break
                    bulFlex.sort(reverse=True)
                    for bulFlexDel in bulFlex:
                        flyBullets[0].pop(bulFlexDel)
                        flyBullets[1].pop(bulFlexDel)
                        flyBullets[2].pop(bulFlexDel)
                        flyBullets[3].pop(bulFlexDel)
                    if y + Size > map["spring"][1][i] and y < map["spring"][1][i] + map["spring"][3][i] \
                    and x + Size > map["spring"][0][i] and x < map["spring"][0][i] + map["spring"][2][i]:
                        spring = 1
                        speedJ = SpringJ
                        jump = "motion"
                        dash = "stop"
                        timeDash = 0
                        grav = 0
                        speedG = 0
                        canDash = True
                        canJumpWallL = False
                        canJumpWallR = False
                        canJump = False
                for i in range(len(map["rollback"][0])):
                    if y + Size > map["rollback"][1][i]-3 and y < map["rollback"][1][i] + map["rollback"][3]+3 \
                            and x + Size > map["rollback"][0][i]-3 and x < map["rollback"][0][i] + map["rollback"][2]+3:
                        if canDash == False and map["rollback"][4][i] == 0:
                            canDash = True
                            rollbackSound.play()
                            map["rollback"][4][i] += 1
                    if map["rollback"][4][i] > 0:
                        map["rollback"][4][i] += 1
                    if map["rollback"][4][i] >= timeRollback:
                        map["rollback"][4][i] = 0
                for i in range(len(map["spawnpoint"][0])):
                    if y + Size > map["spawnpoint"][1][i] and y < map["spawnpoint"][1][i] + map["spawnpoint"][3] \
                            and x + Size > map["spawnpoint"][0][i] and x < map["spawnpoint"][0][i] + map["spawnpoint"][2]:
                        spawnX = map["spawnpoint"][0][i]
                        spawnY = map["spawnpoint"][1][i]
                        if spawnSX != spawnX - 440 or spawnSY != spawnY - 250:
                            saveSound.play()
                        spawnSX = spawnX - 440
                        spawnSY = spawnY - 250
                        map["spawnpoint"][4] = i
                try:
                    for i in range(len(map["finish"][0])):
                        if map["finish"][4][i] or sum(map["enemyFly"][9]) <= 0:
                            if y + Size > map["finish"][1][i] and y < map["finish"][1][i] + map["finish"][3] \
                                    and x + Size > map["finish"][0][i] and x < map["finish"][0][i] + map["finish"][2]:
                                if canCreate == False:
                                    if victoryTime == 2 * FPS:
                                        win = finish_level()
                                        finishSound.play()
                                        victoryTime -= 1
                        elif not(map["finish"][4][i]) and sum(map["enemyFly"][9]) > 0:
                            if y + Size > map["finish"][1][i] and y < map["finish"][1][i] + map["finish"][3] \
                                    and x + Size > map["finish"][0][i] and x < map["finish"][0][i] + map["finish"][2]:
                                if bullets < bulletsMax:
                                    bullets = bulletsMax
                                    chargerSound.play()
                except:
                    pass
                try:
                    if bullets < bulletsMax:
                        for i in range(len(map["bullets"][0])):
                            if y + Size > map["bullets"][1][i] and y < map["bullets"][1][i] + map["bullets"][3] \
                                    and x + Size > map["bullets"][0][i] and x < map["bullets"][0][i] + map["bullets"][2]\
                                    and bullets < bulletsMax:
                                bullets += min(3, bulletsMax-bullets)
                                chargerSound.play()
                                map["bullets"][1][i] = 3000
                except:
                    pass
                try:
                    if (True in map["enemyFly"][6]) or (sum(map["enemyFly"][8]) > 0):
                        for enem in range(len(map["enemyFly"][1])):
                            if map["enemyFly"][9][enem] <= 0:
                                continue
                            if map["enemyFly"][6][enem]:
                                try:
                                    sin = (y - map["enemyFly"][1][enem]) / ((y - map["enemyFly"][1][enem])**2 + (
                                            x - map["enemyFly"][0][enem])**2)**0.5
                                    cos = (x - map["enemyFly"][0][enem]) / ((y - map["enemyFly"][1][enem]) ** 2 + (
                                                x - map["enemyFly"][0][enem]) ** 2) ** 0.5
                                except:
                                    sin = 0
                                    cos = 0
                                map["enemyFly"][0][enem] += speedEnemy * cos
                                map["enemyFly"][1][enem] += speedEnemy * sin
                            elif (map["enemyFly"][0][enem] != map["enemyFly"][4][enem] \
                                or map["enemyFly"][1][enem] != map["enemyFly"][5][enem]):
                                oldLengthEnem = ((map["enemyFly"][1][enem] - map["enemyFly"][5][enem]) ** 2 + (map["enemyFly"][0][enem] - map["enemyFly"][4][enem]) ** 2) ** 0.5
                                if (oldLengthEnem > 0 and oldLengthEnem < speedEnemy) and map["enemyFly"][8][enem] > 0:
                                    map["enemyFly"][0][enem] = map["enemyFly"][4][enem]
                                    map["enemyFly"][1][enem] = map["enemyFly"][5][enem]
                                elif oldLengthEnem >= speedEnemy and map["enemyFly"][8][enem] > 0:
                                    try:
                                        sin = (map["enemyFly"][5][enem] - map["enemyFly"][1][enem]) / oldLengthEnem
                                        cos = (map["enemyFly"][4][enem] - map["enemyFly"][0][enem]) / oldLengthEnem
                                    except:
                                        sin = 0
                                        cos = 0
                                    map["enemyFly"][0][enem] += speedEnemy * cos
                                    map["enemyFly"][1][enem] += speedEnemy * sin
                            elif map["enemyFly"][8][enem] > 0:
                                map["enemyFly"][8][enem] -= 1
                                if map["enemyFly"][8][enem] == 0:
                                    stopEnemyFlySound.play()
                            if y + Size > map["enemyFly"][1][enem] and y < map["enemyFly"][1][enem] + map["enemyFly"][3] \
                                    and x + Size > map["enemyFly"][0][enem] and x < map["enemyFly"][0][enem] + map["enemyFly"][2]:
                                if canCreate == False:
                                    add_death()
                                dieSound.play()
                                x = spawnX
                                y = spawnY
                                xO = x
                                yO = y
                                surfX = spawnSX
                                surfY = spawnSY
                                motionL = 'stop'
                                motionR = 'stop'
                                motionU = 'stop'
                                motionD = 'stop'
                                dash = 'stop'
                                jump = 'stop'
                                jumpWallL = "stop"
                                jumpWallR = "stop"
                                speed = 0
                                speedG = 0
                                speedJ = J
                                maxSpeed = 4
                                timeShoot = 0
                                canShoot = True
                                Gun = GUN[0]
                                if bullets > 0:
                                    colorBullets = colorBullets1
                                timeDash = 0
                                canJump = False
                                canJumpWallR = False
                                canJumpWallL = False
                                canDash = False
                                for j in range(len(map["rollback"][4])):
                                    map["rollback"][4][j] = 0
                                if "enemyFly" in map:
                                    for ret in range(len(map["enemyFly"][0])):
                                        if map["enemyFly"][9][ret] > 0:
                                            map["enemyFly"][-1][ret] = 0
                                            map["enemyFly"][4][ret] = 0
                                            map["enemyFly"][5][ret] = 0
                                            map["enemyFly"][6][ret] = False
                                            map["enemyFly"][0][ret] = map["enemyFly"][7][0][ret]
                                            map["enemyFly"][1][ret] = map["enemyFly"][7][1][ret]
                                            map["enemyFly"][7][2][ret] = 0
                                            map["enemyFly"][7][3][ret] = 0
                                            map["enemyFly"][8][ret] = 0
                except:
                    pass
                if timeCoyoteL < Coyote:
                    timeCoyoteL += 1
                    canJumpWallL = True
                if timeCoyoteR < Coyote:
                    timeCoyoteR += 1
                    canJumpWallR = True
        for e in range(1):
            if x < surfX+(WIDTH-surf)//2:
                surfX -= speedSX
                if speedSX < maxSpeed:
                    speedSX += surfG
                else:
                    speedSX = maxSpeed
                if surfX+(WIDTH-surf)//2-x >= Size * 1.3:
                    speedSX = abs(xO - x)
            elif x+Size > surfX+(WIDTH+surf)//2:
                surfX += speedSX
                if speedSX < maxSpeed:
                    speedSX += surfG
                else:
                    speedSX = maxSpeed
                if x+Size-(surfX+(WIDTH+surf)//2) >= Size * 1.3:
                    speedSX = abs(xO - x)
            else:
                speedSX = 0
            if y < surfY+(HEIGHT-surf)//2:
                if speedSY < speedJ-speedG:
                    if jump == "motion" or dash == "motion":
                        speedSY += surfG
                else:
                    if jump == "motion" or dash == "motion":
                        speedSY = speedJ-speedG
                if surfY+(HEIGHT-surf)//2-y > Size * 1.3:
                    speedSY = abs(yO - y)
                surfY -= speedSY
            elif y+Size > surfY+(HEIGHT+surf)//2:
                if speedSY < speedG:
                    speedSY += g
                else:
                    if speedG != 0:
                        speedSY = speedG
                if y+Size-surfY-(HEIGHT+surf)//2 > Size * 1.3:
                    speedSY = abs(yO - y)
                surfY += speedSY
            else:
                speedSY = 0
            TrueX = x-surfX
            TrueY = y-surfY
        for d in range(1):
            for i in range(len(map["background"][3])):
                if map["background"][0][i] + map["background"][2][i] > surfX and map["background"][1][i] + map["background"][3][i] > surfY \
                        and map["background"][0][i] < surfX + WIDTH and map["background"][1][i] < surfY + HEIGHT:
                    pygame.draw.rect(screen, map["background"][4][i], (map["background"][0][i]-surfX, map["background"][1][i]-surfY, map["background"][2][i],
                                                     map["background"][3][i]))
            try:
                for i in range(len(map["enemyFly"][1])):
                    if map["enemyFly"][9][i] <= 0:
                        if map["enemyFly"][0][i] + map["enemyFly"][2] > surfX \
                                and map["enemyFly"][1][i] + map["enemyFly"][3] > surfY \
                                and map["enemyFly"][0][i] < surfX + WIDTH and map["enemyFly"][1][i] < surfY + HEIGHT:
                            enemyFly = ENEMYDIE1img
                            minListX = min(ENEMYDIE1[0])
                            minListY = min(ENEMYDIE1[1])
                            xDraw = map["enemyFly"][0][i] - surfX + minListX
                            yDraw = map["enemyFly"][1][i] - surfY + minListY
                            screen.blit(enemyFly, (xDraw, yDraw))
            except:
                pass
            timeCadrRoll += 1
            if timeCadrRoll >= FPS * RollBackSec // len(RollBackTexture):
                if cadrRoll + 1 < len(RollBackTexture):
                    cadrRoll += 1
                else:
                    cadrRoll = 0
                timeCadrRoll = 0
            RollTex = RollBackTextureimg[cadrRoll]
            RollTex2 = RollBackTexture2img[cadrRoll]
            for i in range(len(map["rollback"][4])):
                if map["rollback"][0][i] + map["rollback"][2] > surfX \
                        and map["rollback"][1][i] + map["rollback"][3] > surfY \
                        and map["rollback"][0][i] < surfX + WIDTH and map["rollback"][1][i] < surfY + HEIGHT:
                    if map["rollback"][4][i] == 0:
                        minListX = min(RollBackTexture[cadrRoll][0])
                        minListY = min(RollBackTexture[cadrRoll][1])
                        xDraw = map["rollback"][0][i] - surfX + minListX
                        yDraw = map["rollback"][1][i] - surfY + minListY
                        screen.blit(RollTex, (xDraw, yDraw))
                    else:
                        minListX = min(RollBackTexture2[cadrRoll][0])
                        minListY = min(RollBackTexture2[cadrRoll][1])
                        xDraw = map["rollback"][0][i] - surfX + minListX
                        yDraw = map["rollback"][1][i] - surfY + minListY
                        screen.blit(RollTex2, (xDraw, yDraw))
            timeCadrSpawn += 1
            timeCadrSpawn2 += 1
            if timeCadrSpawn >= FPS * SpawnSec // len(SpawnTexture):
                if cadrSpawn + 1 < len(SpawnTexture):
                    cadrSpawn += 1
                else:
                    cadrSpawn = 0
                timeCadrSpawn = 0
            if timeCadrSpawn2 >= FPS * SpawnSec2 // len(SpawnTexture2):
                if cadrSpawn2 + 1 < len(SpawnTexture2):
                    cadrSpawn2 += 1
                else:
                    cadrSpawn2 = 0
                timeCadrSpawn2 = 0
            SpawnTex = SpawnTextureimg[cadrSpawn]
            SpawnTex2 = SpawnTexture2img[cadrSpawn2]
            for i in range(len(map["spawnpoint"][1])):
                if map["spawnpoint"][0][i] + map["spawnpoint"][2] > surfX \
                        and map["spawnpoint"][1][i] + map["spawnpoint"][3] > surfY \
                        and map["spawnpoint"][0][i] < surfX + WIDTH and map["spawnpoint"][1][i] < surfY + HEIGHT:
                    if map["spawnpoint"][-1] == i:
                        minListX = min(SpawnTexture2[cadrSpawn2][0])
                        minListY = min(SpawnTexture2[cadrSpawn2][1])
                        xDraw = map["spawnpoint"][0][i] - surfX + minListX
                        yDraw = map["spawnpoint"][1][i] - surfY + minListY
                        screen.blit(SpawnTex2, (xDraw, yDraw))
                    else:
                        minListX = min(SpawnTexture[cadrSpawn][0])
                        minListY = min(SpawnTexture[cadrSpawn][1])
                        xDraw = map["spawnpoint"][0][i] - surfX + minListX
                        yDraw = map["spawnpoint"][1][i] - surfY + minListY
                        screen.blit(SpawnTex, (xDraw, yDraw))
            if finishTimeCadr < finishSec * FPS:
                finishTimeCadr += 1
                if finishTimeCadr >= finishSec * FPS:
                    finishTimeCadr = 0
            try:
                for i in range(len(map["finish"][0])):
                    if map["finish"][0][i] + map["finish"][2] > surfX \
                            and map["finish"][1][i] + map["finish"][3] > surfY \
                            and map["finish"][0][i] < surfX + WIDTH and map["finish"][1][i] < surfY + HEIGHT:
                        if map["finish"][4][i]:
                            frameFinishText = min(int(finishTimeCadr // (finishSec * FPS / len(FINISHimg))), len(FINISHimg) - 1)
                            finishTex = FINISHimg[frameFinishText]
                        else:
                            if sum(map["enemyFly"][9]) <= 0:
                                frameFinishText = min(int(finishTimeCadr // (finishSec * FPS / len(FINISH2img))),
                                                      len(FINISH2img) - 1)
                                finishTex = FINISH2img[frameFinishText]
                            else:
                                frameFinishText = 0
                                finishTex = FINISH2disimg
                        if finishTex == FINISHimg[frameFinishText]:
                            minListX = min(FINISH[frameFinishText][0])
                            minListY = min(FINISH[frameFinishText][1])
                        elif finishTex == FINISH2img[frameFinishText]:
                            minListX = min(FINISH2[frameFinishText][0])
                            minListY = min(FINISH2[frameFinishText][1])
                        else:
                            minListX = min(FINISH2dis[0])
                            minListY = min(FINISH2dis[1])
                        xDraw = map["finish"][0][i] - surfX + minListX
                        yDraw = map["finish"][1][i] - surfY + minListY
                        screen.blit(finishTex, (xDraw, yDraw))
            except:
                pass
            try:
                for i in range(len(map["bullets"][1])):
                    if map["bullets"][0][i] + map["bullets"][2] > surfX \
                            and map["bullets"][1][i] + map["bullets"][3] > surfY \
                            and map["bullets"][0][i] < surfX + WIDTH and map["bullets"][1][i] < surfY + HEIGHT:
                        minListX = min(BulletTexture[0])
                        minListY = min(BulletTexture[1])
                        xDraw = map["bullets"][0][i] - surfX + minListX
                        yDraw = map["bullets"][1][i] - surfY + minListY
                        screen.blit(BulletTextureimg, (xDraw, yDraw))
            except:
                pass
            for i in range(len(flyBullets[0])):
                if flyBullets[0][i] + lengthBullets * cos > surfX \
                        and flyBullets[1][i] + lengthBullets * sin > surfY \
                        and flyBullets[0][i] < surfX + WIDTH and flyBullets[1][i] < surfY + HEIGHT:
                    sin = math.sin(math.radians(flyBullets[2][i]))
                    cos = math.cos(math.radians(flyBullets[2][i]))
                    drawX = flyBullets[0][i] - surfX
                    drawY = flyBullets[1][i] - surfY
                    pygame.draw.line(screen, flyBullets[3][i], [drawX, drawY], [drawX - lengthBullets * cos, drawY - lengthBullets * sin], 1)
            SpringAllY -= 0.5
            for i in range(len(map["spring"][3])):
                if map["spring"][0][i] + map["spring"][2][i] > surfX and map["spring"][1][i] + \
                        map["spring"][3][i] > surfY \
                        and map["spring"][0][i] < surfX + WIDTH and map["spring"][1][i]-30 < surfY + HEIGHT:
                    pygame.draw.rect(screen, (235, 228, 30), (map["spring"][0][i] - surfX,
                                                              map["spring"][1][i] - surfY,
                                                              map["spring"][2][i], map["spring"][3][i]))
                    n = 3
                    for j in range(n):
                        ySPR = SpringAllY % 30 + 30 / n * j
                        if ySPR > 30:
                            ySPR -= 30
                        ySPR -= 30
                        pygame.draw.line(screen, (191, 149, 10),
                                         (map["spring"][0][i] - surfX, map["spring"][1][i] + ySPR - surfY),
                                         (map["spring"][0][i] + map["spring"][2][i] - surfX - 1,
                                          map["spring"][1][i] + ySPR - surfY), 2)
            if dash == "stop": 
                if xO < x and yO == y and grav == 0:
                    if anime != 0:
                        anime = 0
                        timeCadr = 0
                        cadr = 0
                    timeCadr += 1
                    if timeCadr >= FPS * GGRunSec // len(GGRun):
                        if cadr + 1 < len(GGRun):
                            cadr += 1
                        else:
                            cadr = 0
                        timeCadr = 0
                    if cadr + 1 >= len(GGRun):
                        cadr = 0
                    GG = GGRun[cadr]
                    GGRIGHT = True
                    DROP = False
                elif xO > x and yO == y and grav == 0:
                    if anime != 1:
                        anime = 1
                        timeCadr = 0
                        cadr = 0
                    timeCadr += 1
                    if timeCadr >= FPS * GGRunSec // len(GGRun):
                        if cadr + 1 < len(GGRun):
                            cadr += 1
                        else:
                            cadr = 0
                        timeCadr = 0
                    if cadr + 1 >= len(GGRun):
                        cadr = 0
                    GG = GGRun[cadr]
                    GGRIGHT = False
                    DROP = False
                elif yO > y and xO == x and FlagWall == False:
                    if anime != 2:
                        anime = 2
                        timeCadr = 0
                        cadr = 0
                    timeCadr += 1
                    if timeCadr >= FPS * GGJumpSec // len(GGJump):
                        if cadr + 1 < len(GGJump):
                            cadr += 1
                        timeCadr = 0
                    if cadr + 1 > len(GGJump):
                        cadr = 0
                    GG = GGJump[cadr]
                    DROP = False
                elif yO < y and xO == x and FlagWall == False:
                    if anime != 3:
                        anime = 3
                        timeCadr = 0
                        cadr = 0
                    timeCadr += 1
                    if timeCadr >= FPS * GGJumpSec // len(GGJump):
                        if cadr + 1 < len(GGJump):
                            cadr += 1
                        timeCadr = 0
                    if cadr + 1 > len(GGJump):
                        cadr = 0
                    GG = GGJump[cadr]
                    DROP = True
                elif yO > y and xO < x:
                    if anime != 2:
                        anime = 2
                        timeCadr = 0
                        cadr = 0
                    timeCadr += 1
                    if timeCadr >= FPS * GGJumpRunSec // len(GGJumpRun):
                        if cadr + 1 < len(GGJumpRun):
                            cadr += 1
                        timeCadr = 0
                    if cadr + 1 > len(GGJumpRun):
                        cadr = 0
                    GG = GGJumpRun[cadr]
                    DROP = False
                    GGRIGHT = True
                elif yO > y and xO > x:
                    if anime != 2:
                        anime = 2
                        timeCadr = 0
                        cadr = 0
                    timeCadr += 1
                    if timeCadr >= FPS * GGJumpRunSec // len(GGJumpRun):
                        if cadr + 1 < len(GGJumpRun):
                            cadr += 1
                        timeCadr = 0
                    if cadr + 1 > len(GGJumpRun):
                        cadr = 0
                    GG = GGJumpRun[cadr]
                    DROP = False
                    GGRIGHT = False
                elif yO < y and xO < x:
                    if anime != 3:
                        anime = 3
                        timeCadr = 0
                        cadr = 0
                    timeCadr += 1
                    if timeCadr >= FPS * GGJumpRunSec // len(GGJumpRun):
                        if cadr + 1 < len(GGJumpRun):
                            cadr += 1
                        timeCadr = 0
                    if cadr + 1 > len(GGJumpRun):
                        cadr = 0
                    GG = GGJumpRun[cadr]
                    DROP = True
                    GGRIGHT = True
                elif yO < y and xO > x:
                    if anime != 3:
                        anime = 3
                        timeCadr = 0
                        cadr = 0
                    timeCadr += 1
                    if timeCadr >= FPS * GGJumpRunSec // len(GGJumpRun):
                        if cadr + 1 < len(GGJumpRun):
                            cadr += 1
                        timeCadr = 0
                    if cadr + 1 > len(GGJumpRun):
                        cadr = 0
                    GG = GGJumpRun[cadr]
                    DROP = True
                    GGRIGHT = False
                elif yO == y and xO == x and grav == 0 or (FlagWall and int(math.sqrt((xO-x)**2 + (yO-y)**2) < 4)):
                    if anime != 4:
                        anime = 4
                        timeCadr = 0
                        cadr = 0
                    timeCadr += 1
                    if timeCadr >= FPS * GGStopSec // len(GGStop):
                        if cadr + 1 < len(GGStop):
                            cadr += 1
                        else:
                            cadr = 0
                        timeCadr = 0
                    if cadr + 1 >= len(GGStop):
                        cadr = 0
                    GG = GGStop[cadr]
                    if lastButton == "right":
                        GGRIGHT = True
                    else:
                        GGRIGHT = False
                    DROP = False
            elif dash == "motion":
                if anime != -1:
                    anime = -1
                    cadr = 0
                    timeCadr = 0
                timeCadr += 1
                if timeCadr >= FPS * GGDashSec // len(GGDash):
                    if cadr + 1 < len(GGDash):
                        cadr += 1
                    timeCadr = 0
                if NDash == "up" or NDash == "down" or NDash == "left" or NDash == "right":
                    GG = GGDash[cadr]
                    if NDash == "up":
                        DROP = False
                    elif NDash == "down":
                        DROP = True
                    if NDash == "right":
                        rotate = "right"
                    elif NDash == "left":
                        rotate = "left"
                else:
                    GG = GGDashRun[cadr]
                    if NDash[:2] == "up":
                        DROP = False
                    else:
                        DROP = True
                    if NDash[-5:] == "right":
                        GGRIGHT = True
                    else:
                        GGRIGHT = False
            for i in range(len(GG[0])):
                drawX = x + GG[0][i] - surfX
                drawY = y + GG[1][i] - surfY
                if rotate == "none":
                    if FlagWall and int(math.sqrt((xO-x)**2 + (yO-y)**2) < 4):
                        if canJumpWallL == True:
                            drawY = y - GG[0][i] - 3 - surfY + Size
                            drawX = x + GG[1][i] - surfX
                            GGRIGHT = True
                            DROP = False
                        elif canJumpWallR == True:
                            drawX = x - GG[1][i] - 3 - surfX + Size
                            drawY = y + GG[0][i] - surfY
                            GGRIGHT = True
                            DROP = True
                    if GGRIGHT == False:
                        drawX = x - (drawX - x + surfX) - surfX + Size - 3
                    if DROP:
                        drawY = y - (drawY - y + surfY) - surfY + Size - 3
                else:
                    if rotate == "left":
                        drawY = y - GG[0][i] - 3 - surfY + Size
                        drawX = x + GG[1][i] - surfX
                    else:
                        drawX = x - GG[1][i] - 3 - surfX + Size
                        drawY = y + GG[0][i] - surfY
                lol = GG[2][i]
                if canDash == False:
                    if GG[2][i] == (0, 190, 0):
                        lol = (0, 190, 190)
                    elif GG[2][i] == (0, 95, 0):
                        lol = (0, 95, 95)
                pygame.draw.rect(screen, lol, (drawX, drawY, 3, 3))
            rotate = "none"
            if hitbox and canCreate:
                pygame.draw.rect(screen, pygame.Color("red"), (x - surfX, y - surfY, Size, Size), 1) 
            timeCadrSpikes += 1
            if timeCadrSpikes >= FPS * SpikesSec // len(SpikesTexture):
                if cadrSpikes + 1 < len(SpikesTexture):
                    cadrSpikes += 1
                else:
                    cadrSpikes = 0
                timeCadrSpikes = 0
            if not hitbox:
                SpikesTex = SpikesTextureimg[cadrSpikes]
            else:
                SpikesTex = SpikesTexture[cadrSpikes]
            for i in range(len(map["spikes"][3])):
                if map["spikes"][0][i] + map["spikes"][2][i] > surfX and map["spikes"][1][i] + map["spikes"][3][i] > surfY \
                        and map["spikes"][0][i] < surfX + WIDTH and map["spikes"][1][i] < surfY + HEIGHT:
                    pygame.draw.rect(screen, (225, 225, 225), (map["spikes"][0][i]-surfX, map["spikes"][1][i]-surfY, map["spikes"][2][i], map["spikes"][3][i]))
                    for w in range(map["spikes"][2][i]//10):
                        if hitbox:
                            for j in range(len(SpikesTex[0])):
                                drawX = map["spikes"][0][i] + SpikesTex[0][j] - surfX + 10 * w
                                drawY = map["spikes"][1][i] + SpikesTex[1][j] - surfY
                                if drawX + surfX + 1 > surfX and drawY + surfY + 2 > surfY \
                                        and drawX + surfX < surfX + WIDTH and drawY + surfY < surfY + HEIGHT:
                                    pygame.draw.rect(screen, SpikesTex[2][j], (drawX, drawY, 2, 2))
                                drawY = map["spikes"][1][i] - SpikesTex[1][j] - surfY + map["spikes"][3][i] - 2
                                if drawX + surfX + 1 > surfX and drawY + surfY + 2 > surfY \
                                        and drawX + surfX < surfX + WIDTH and drawY + surfY < surfY + HEIGHT:
                                    pygame.draw.rect(screen, SpikesTex[2][j], (drawX, drawY, 2, 2))
                        else:
                            drawX = map["spikes"][0][i] - surfX + 10 * w + min(SpikesTexture[cadrSpikes][0])
                            drawY = map["spikes"][1][i] - surfY - SpikesTex.get_height()
                            if drawX + surfX + 1 > surfX and drawY + surfY + 2 > surfY \
                                    and drawX + surfX < surfX + WIDTH and drawY + surfY < surfY + HEIGHT:
                                screen.blit(SpikesTex, (drawX, drawY))
                            drawY = map["spikes"][1][i] - surfY + map["spikes"][3][i]
                            if drawX + surfX + 1 > surfX and drawY + surfY + 2 > surfY \
                                    and drawX + surfX < surfX + WIDTH and drawY + surfY < surfY + HEIGHT:
                                screen.blit(SpikesTex, (drawX, drawY))
            try:
                for i in range(len(map["enemyFly"][1])):
                    if map["enemyFly"][9][i] > 0:
                        if map["enemyFly"][0][i] + map["enemyFly"][2] > surfX \
                                and map["enemyFly"][1][i] + map["enemyFly"][3] > surfY \
                                and map["enemyFly"][0][i] < surfX + WIDTH and map["enemyFly"][1][i] < surfY + HEIGHT:
                            if map["enemyFly"][6][i] or map["enemyFly"][8][i] > 0:
                                if map["enemyFly"][-1][i] <= enemyFlySec * FPS:
                                    frameEnemyFlyImg = min(map["enemyFly"][-1][i] // (enemyFlySec * FPS // len(ENEMY1)), len(ENEMY1) - 1)
                                    map["enemyFly"][-1][i] += 1
                                else:
                                    map["enemyFly"][-1][i] = 0
                                    frameEnemyFlyImg = 0
                                enemyFly = ENEMY1img[frameEnemyFlyImg]
                                minListX = min(ENEMY1[frameEnemyFlyImg][0])
                                minListY = min(ENEMY1[frameEnemyFlyImg][1])
                            else:
                                enemyFly = ENEMYSTAN1img
                                minListX = min(ENEMYSTAN1[0])
                                minListY = min(ENEMYSTAN1[1])
                            xDraw = map["enemyFly"][0][i] - surfX + minListX
                            yDraw = map["enemyFly"][1][i] - surfY + minListY
                            screen.blit(enemyFly, (xDraw, yDraw))
                            if map["enemyFly"][9][i] < hpEnemyFly:
                                pygame.draw.line(screen, (50, 50, 50), [map["enemyFly"][0][i] - surfX,
                                                                               map["enemyFly"][1][i] - 6 - surfY],
                                                 [map["enemyFly"][0][i] + map["enemyFly"][2] - surfX,
                                                  map["enemyFly"][1][i] - 6 - surfY], 3)
                                pygame.draw.line(screen, (180, 10, 10), [map["enemyFly"][0][i] - surfX,
                                                                               map["enemyFly"][1][i] - 6 - surfY],
                                                 [map["enemyFly"][0][i] + map["enemyFly"][2] * (map["enemyFly"][9][i]/hpEnemyFly) - surfX, map["enemyFly"][1][i] - 6 - surfY], 3)
            except:
                pass
            for i in range(len(map["block"][3])):
                if map["block"][0][i] + map["block"][2][i] > surfX and map["block"][1][i] + map["block"][3][i] > surfY \
                        and map["block"][0][i] < surfX + WIDTH and map["block"][1][i] < surfY + HEIGHT:
                    pygame.draw.rect(screen, (38, 38, 38), (map["block"][0][i]-surfX, map["block"][1][i]-surfY, map["block"][2][i],
                                                     map["block"][3][i]))
                    n1 = 4
                    n2 = 4
                    if map["block"][2][i] <= 30:
                        n1 = 1
                    elif map["block"][2][i] <= 50:
                        n1 = 2
                    elif map["block"][2][i] <= 100:
                        n1 = 3
                    if map["block"][3][i] <= 30:
                        n2 = 1
                    elif map["block"][3][i] <= 50:
                        n2 = 2
                    elif map["block"][3][i] <= 100:
                        n2 = 3
                    for j in range(n1+1):
                        pygame.draw.line(screen, (101, 201, 200), (map["block"][0][i] + map["block"][2][i]/n1*j-surfX, map["block"][1][i]-surfY), (map["block"][0][i] + map["block"][2][i]/n1*j-surfX, map["block"][1][i]+map["block"][3][i]-surfY), 1)
                    for j in range(n2+1):
                        pygame.draw.line(screen, (101, 201, 200), (map["block"][0][i]-surfX, map["block"][1][i] + map["block"][3][i]/n2*j-surfY), (map["block"][0][i]+map["block"][2][i]-surfX, map["block"][1][i] + map["block"][3][i]/n2*j-surfY), 1)
            pygame.draw.rect(screen, (38, 38, 38), (0, minY - surfY, WIDTH, -minY + surfY + HEIGHT))
            pygame.draw.line(screen, (101, 201, 200), (0, minY - surfY), (WIDTH, minY - surfY))
            for gunnn in range(1):
                if mouseY < -surfY + y + Size // 2:
                    angle = -(math.acos((mouseX - (-surfX + x + Size // 2)) / ((mouseX - (-surfX + x + Size // 2)) ** 2 + (
                                mouseY - (-surfY + y + Size // 2)) ** 2) ** 0.5)) * 360 / math.pi / 2
                else:
                    angle = (math.acos((mouseX - (-surfX + x + Size//2)) / ((mouseX - (-surfX + x + Size//2)) ** 2 + (
                            mouseY - (-surfY + y + Size // 2)) ** 2) ** 0.5)) * 360 / math.pi / 2
                for gu in range(len(Gun[0])):
                    drawX = Gun[0][gu]
                    drawY = Gun[1][gu]
                    color = Gun[2][gu]
                    pygame.draw.rect(GunSurf, color, (drawX, drawY, 2, 2))
                if math.fabs(angle) > 90:
                    GunSurfR = pygame.transform.flip(GunSurf, False, True)
                    pivotGun = [int(-surfX + x + Size // 2), int(-surfY + y + Size // 2)]
                    offsetGun = pygame.math.Vector2(GunSurf.get_width()-24, 3)
                else:
                    GunSurfR = pygame.transform.flip(GunSurf, False, False)
                    pivotGun = [int(-surfX + x + Size // 2), int(-surfY + y + Size // 2)]
                    offsetGun = pygame.math.Vector2(7, -3)
                rotated_Gun, rect = rotate1(GunSurfR, angle, pivotGun, offsetGun)
                screen.blit(rotated_Gun, rect)
            if bulletTime > 0:
                bulletTime -= 1
                bulletsCadr = min(bullets * 2 + 1, 32)
            else:
                bulletsCadr = bullets * 2
            for bu in range(len(BULLETS[bulletsCadr][0])):
                drawX = BULLETS[bulletsCadr][0][bu]
                drawY = BULLETS[bulletsCadr][1][bu]
                pygame.draw.rect(screen, colorBullets, (inventory[0] + drawX, inventory[1] + drawY, 4, 4))
            for buM in range(len(BULLETSMAX[0][0])):
                drawX = BULLETSMAX[0][0][buM]
                drawY = BULLETSMAX[0][1][buM]
                pygame.draw.rect(screen, colorBullets, (inventory[0] + drawX + 62, inventory[1] + drawY, 4, 4))
            fps = int(clock.get_fps())
            textFPS = font.render('FPS: ' + str(fps), 1, WHITE)
            textX = font.render('X: ' + str(int(x)), 1, WHITE)
            textY = font.render('Y: ' + str(int(y)), 1, WHITE)
            textSpeed = font.render('Speed: ' + str(int(math.sqrt((xO - x) ** 2 + (yO - y) ** 2))), 1, WHITE)
            textGame = font.render('GameMode: ' + str(gameMode), 1, WHITE)
            textFPSShadow = font.render('FPS: ' + str(fps), 1, BLACK)
            textXShadow = font.render('X: ' + str(int(x)), 1, BLACK)
            textYShadow = font.render('Y: ' + str(int(y)), 1, BLACK)
            textSpeedShadow = font.render('Speed: ' + str(int(math.sqrt((xO - x) ** 2 + (yO - y) ** 2))), 1, BLACK)
            textGameShadow = font.render('GameMode: ' + str(gameMode), 1, BLACK)
            if createType == 'finish':
                textType = font.render('Type: ' + str(createType) + f"({finishPacifist})", 1, WHITE)
                textTypeShadow = font.render('Type: ' + str(createType) + f"({finishPacifist})", 1, BLACK)
            else:
                textType = font.render('Type: ' + str(createType), 1, WHITE)
                textTypeShadow = font.render('Type: ' + str(createType), 1, BLACK)
            if canCreate:
                screen.blit(textXShadow, (11, 31))
                screen.blit(textYShadow, (11, 51))
                screen.blit(textSpeedShadow, (11, 71))
                screen.blit(textGameShadow, (11, 91))
                screen.blit(textFPSShadow, (11, 11))
                screen.blit(textX, (10, 30))
                screen.blit(textY, (10, 50))
                screen.blit(textSpeed, (10, 70))
                screen.blit(textGame, (10, 90))
                screen.blit(textFPS, (10, 10))
            if gameMode == "creat":
                screen.blit(textTypeShadow, (11, 111))
                screen.blit(textType, (10, 110))
                if draw == 1:
                    if createType != "rollback" and createType != "spawnpoint" and createType != "bullets" and createType != "enemyFly" and createType != "finish":
                        cordBlock = [0, 0]
                        cordBlockCreate = [0, 0]
                        numFiveX = 5
                        numFiveY = 5
                        textHHH = font.render(f"w:{int(math.fabs((mouseX + surfX - map[createType][0][-1])/10))}/h:{int(math.fabs((mouseY + surfY - map[createType][1][-1])/10))}", 1, pygame.Color('red'))
                        if mouseX < map[createType][0][-1] - surfX:
                            cordBlock[0] = mouseX
                            numFiveX *= -1
                            cordBlockCreate[0] = mouseX
                        else:
                            cordBlock[0] = mouseX-textHHH.get_width()
                            cordBlockCreate[0] = map[createType][0][-1] - surfX
                        if mouseY < map[createType][1][-1] - surfY:
                            cordBlock[1] = mouseY-textHHH.get_height()-1
                            numFiveY *= -1
                            cordBlockCreate[1] = mouseY
                        else:
                            cordBlock[1] = mouseY+1
                            cordBlockCreate[1] = map[createType][1][-1] - surfY
                        textCordBlock = font.render(f"w:{int(math.fabs((mouseX + surfX+numFiveX - map[createType][0][-1])/10))}/h:{int(math.fabs((mouseY + surfY+numFiveY - map[createType][1][-1])/10))}", 1, pygame.Color('red'))
                        screen.blit(textCordBlock, (cordBlock[0], cordBlock[1]))
                        pygame.draw.rect(screen, pygame.Color('red'), (
                            cordBlockCreate[0], cordBlockCreate[1],
                            math.fabs(mouseX + surfX - map[createType][0][-1]),
                            math.fabs(mouseY + surfY - map[createType][1][-1])), 1)
                    else:
                        try:
                            pygame.draw.rect(screen, pygame.Color('red'), (
                                mouseX - map[createType][2]//2, mouseY - map[createType][3]//2,
                                mouseX + map[createType][2]//2 - (mouseX - map[createType][2]//2),
                                mouseY + map[createType][3]//2 - (mouseY - map[createType][3]//2)), 1)
                        except:
                            map["bullets"] = [[], [], 16, 16, [], []]
                            map["enemyFly"] = [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []]
                            map["finish"] = [[], [], 24, 24, []]
                            pygame.draw.rect(screen, pygame.Color('red'), (
                                mouseX - map[createType][2] // 2, mouseY - map[createType][3] // 2,
                                mouseX + map[createType][2] // 2 - (mouseX - map[createType][2] // 2),
                                mouseY + map[createType][3] // 2 - (mouseY - map[createType][3] // 2)), 1)
                elif draw == 2:
                    cordBlockTouch = [0, 0]
                    if mouseX < firstMouseX:
                        cordBlockTouch[0] = mouseX
                    else:
                        cordBlockTouch[0] = firstMouseX
                    if mouseY < firstMouseY:
                        cordBlockTouch[1] = mouseY
                    else:
                        cordBlockTouch[1] = firstMouseY
                    pygame.draw.rect(screen, pygame.Color('blue'), (cordBlockTouch[0], cordBlockTouch[1], math.fabs(mouseX-firstMouseX), math.fabs(mouseY-firstMouseY)), 1)
                elif draw == -1:
                    lineHeight = 2
                    for i in range(len(correctObject["block"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["block"][0][correctObject["block"][i]],
                                          -surfY+map["block"][1][correctObject["block"][i]],
                                          map["block"][2][correctObject["block"][i]],
                                          map["block"][3][correctObject["block"][i]]), lineHeight)
                    for i in range(len(correctObject["spikes"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX + map["spikes"][0][correctObject["spikes"][i]],
                                          -surfY + map["spikes"][1][correctObject["spikes"][i]],
                                          map["spikes"][2][correctObject["spikes"][i]],
                                          map["spikes"][3][correctObject["spikes"][i]]), lineHeight)
                    for i in range(len(correctObject["spring"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["spring"][0][correctObject["spring"][i]],
                                          -surfY+map["spring"][1][correctObject["spring"][i]],
                                          map["spring"][2][correctObject["spring"][i]],
                                          map["spring"][3][correctObject["spring"][i]]), lineHeight)
                    for i in range(len(correctObject["background"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["background"][0][correctObject["background"][i]],
                                          -surfY+map["background"][1][correctObject["background"][i]],
                                          map["background"][2][correctObject["background"][i]],
                                          map["background"][3][correctObject["background"][i]]), lineHeight)
                    for i in range(len(correctObject["rollback"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["rollback"][0][correctObject["rollback"][i]],
                                          -surfY+map["rollback"][1][correctObject["rollback"][i]],
                                          map["rollback"][2],
                                          map["rollback"][3]), lineHeight)
                    for i in range(len(correctObject["spawnpoint"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["spawnpoint"][0][correctObject["spawnpoint"][i]],
                                          -surfY+map["spawnpoint"][1][correctObject["spawnpoint"][i]],
                                          map["spawnpoint"][2],
                                          map["spawnpoint"][3]), lineHeight)
                    for i in range(len(correctObject["bullets"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["bullets"][0][correctObject["bullets"][i]],
                                          -surfY+map["bullets"][1][correctObject["bullets"][i]],
                                          map["bullets"][2],
                                          map["bullets"][3]), lineHeight)
                    for i in range(len(correctObject["enemyFly"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["enemyFly"][0][correctObject["enemyFly"][i]],
                                          -surfY+map["enemyFly"][1][correctObject["enemyFly"][i]],
                                          map["enemyFly"][2],
                                          map["enemyFly"][3]), lineHeight)
                    for i in range(len(correctObject["finish"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["finish"][0][correctObject["finish"][i]],
                                          -surfY+map["finish"][1][correctObject["finish"][i]],
                                          map["finish"][2],
                                          map["finish"][3]), lineHeight)
                if createType == "background":
                    for i in range(len(backColor)):
                        pygame.draw.rect(screen, backColor[i], (WIDTH-30-i*30, 0, 30, 30))
                        if createColor == backColor[i]:
                            pygame.draw.rect(screen, WHITE, (WIDTH - 30 - i * 30, 0, 30, 30), 2)
        if grav == 0 and yO == y and xO != x:
            if playSoundRun == 1:
                runSound.play(-1)
                playSoundRun = 0
        else:
            if playSoundRun == 0:
                runSound.stop()
                playSoundRun = 1
        if grav == 0 and yO < y:
            dropSound.play()
        xO = x
        yO = y
    virtual_display = pygame.transform.scale(screen, current_size)
    screen0.blit(virtual_display, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
sys.exit()