import pygame
import math
import sys
import ast
import os
import json
from win32api import GetSystemMetrics
# Функции настроек
def load_settings():
    default_settings = {
        "sound": {
            "music_volume": 50,
            "sfx_volume": 100
        },
        "display": {
            "fullscreen": False
        },
        "keys": {
            "undo": pygame.K_z,
            "redo": pygame.K_y,
            "save": pygame.K_s,
            "play_pause": pygame.K_SPACE,
            "grid": pygame.K_g,
            "palette": pygame.K_p,
            "frame_left": pygame.K_LEFT,
            "frame_right": pygame.K_RIGHT
        }
    }
    try:
        with open('settings_draw.json', 'r', encoding='utf-8') as f:
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
        with open('settings_draw.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка сохранения настроек: {e}")
def update_sound_volumes():
    pygame.mixer.music.set_volume(settings["sound"]["music_volume"] / 100.0)
def get_key_name(key):
    key_names = {
        pygame.K_z: "Z", pygame.K_y: "Y", pygame.K_s: "S", pygame.K_SPACE: "SPACE",
        pygame.K_g: "G", pygame.K_p: "P", pygame.K_LEFT: "←", pygame.K_RIGHT: "→",
        pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D",
        pygame.K_e: "E", pygame.K_f: "F", pygame.K_h: "H", pygame.K_i: "I",
        pygame.K_j: "J", pygame.K_k: "K", pygame.K_l: "L", pygame.K_m: "M",
        pygame.K_n: "N", pygame.K_o: "O", pygame.K_q: "Q", pygame.K_r: "R",
        pygame.K_t: "T", pygame.K_u: "U", pygame.K_v: "V", pygame.K_w: "W",
        pygame.K_x: "X", pygame.K_UP: "↑", pygame.K_DOWN: "↓",
        pygame.K_RETURN: "ENTER", pygame.K_ESCAPE: "ESC", pygame.K_TAB: "TAB",
        pygame.K_BACKSPACE: "BACKSPACE", pygame.K_DELETE: "DELETE",
        pygame.K_LSHIFT: "LSHIFT", pygame.K_RSHIFT: "RSHIFT",
        pygame.K_LCTRL: "LCTRL", pygame.K_RCTRL: "RCTRL"
    }
    return key_names.get(key, f"KEY_{key}")
pygame.font.init()
lol = os.path.dirname(os.path.abspath(__file__))
texture_directory = lol + "/textures"
try:
    texture_files = [f for f in os.listdir(texture_directory) if f.endswith('.txt')]
    texture_files.sort()
except:
    texture_files = []
# Загружаем настройки
settings = load_settings()
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
Size = 65*4
pixel = 5
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
buttonMenu = ["Ластик", "Копировать", "Вставить", "Сохранить", "Проверить", "Анимации", "Палитра", "Настройки", "Выйти"]
canCreate = False
animation_menu = False
settings_menu = False
keys_menu = False
waiting_for_key = False
selected_key_action = ""
dragging_slider = False
dragging_type = ""
selected_animation_index = 0
current_texture_name = "Finish.txt"
animation_scroll_offset = 0
max_visible_animations = 100
############################################################################################
# История Undo/Redo                                                                        #
history = []                                                                               #
history_index = -1                                                                         #
max_history = 50  # Максимум шагов истории                                                 #
############################################################################################
# Мини-плеер                                                                               #
mini_player_size = 60                                                                      #
mini_player_x = WIDTH - mini_player_size - 10                                              #
mini_player_y = HEIGHT - mini_player_size - 60                                             #
mini_player_frame = 0                                                                      #
mini_player_timer = 0                                                                      #
############################################################################################
# Сетка                                                                                    #
show_grid = False                                                                          #
grid_size = pixel * 4  # Размер клетки сетки                                               #
############################################################################################
# Палитра цветов и кисти                                                                   #
show_palette = False                                                                       #
palette_colors = [
    (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128), (64, 64, 64),
    (255, 128, 0), (128, 255, 0), (0, 128, 255), (255, 0, 128), (128, 0, 255),
    (255, 192, 192), (192, 255, 192), (192, 192, 255), (255, 255, 192), (192, 255, 255)
]
brush_sizes = [1, 2, 3, 4, 5]  # Размеры кисти в пикселях                                   #
current_brush_size = 1                                                                      #
palette_x = WIDTH // 2 - 150                                                                #
palette_y = HEIGHT // 2 - 100                                                               #
#############################################################################################
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
pygame.display.set_caption("Texture Editor")
# Загрузка и запуск музыки
try:
    pygame.mixer.music.load(r'sounds/menu.mp3')
    pygame.mixer.music.play(-1)
    update_sound_volumes()
    print("Музыка загружена и запущена")
except Exception as e:
    print(f"Ошибка загрузки музыки: {e}")
try:
    current_size = (GetSystemMetrics(0), GetSystemMetrics(1))
    print(current_size)
    if settings["display"]["fullscreen"]:
        screen0 = pygame.display.set_mode(current_size, pygame.FULLSCREEN)
    else:
        screen0 = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    screen = pygame.Surface((WIDTH, HEIGHT))
    k_posX = WIDTH/current_size[0]
    k_posY = HEIGHT/current_size[1]
except:
    current_size = (1920, 1080)
    if settings["display"]["fullscreen"]:
        screen0 = pygame.display.set_mode(current_size, pygame.FULLSCREEN)
    else:
        screen0 = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    screen = pygame.Surface((WIDTH, HEIGHT))
    k_posX = WIDTH/current_size[0]
    k_posY = HEIGHT/current_size[1]
fullScreen = settings["display"]["fullscreen"]
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
try:
    default_texture = "GGStop.txt"
    if default_texture != "":
        with open('textures/' + default_texture, 'r') as file:
            text1 = file.readline()
            anime = ast.literal_eval(text1)
            text2 = file.readline()
            second = ast.literal_eval(text2)
except:
    pass
def list_deepcopy(l):
    return [
        elem if not isinstance(elem, list) else list_deepcopy(elem)
        for elem in l
    ]
def load_animation(filename):
    global anime, second, current_texture_name, cadr, history, history_index
    try:
        with open('textures/' + filename, 'r') as file:
            text1 = file.readline()
            anime = ast.literal_eval(text1)
            text2 = file.readline()
            second = ast.literal_eval(text2)
            current_texture_name = filename
            cadr = 0
            history = []
            history_index = -1
            save_to_history()
            print(f"Загружена анимация: {filename}")
    except Exception as e:
        print(f"Ошибка загрузки анимации {filename}: {e}")
        anime = [[[], [], []]]
        second = 1
def save_to_history():
    global history, history_index, anime, second, cadr
    current_state = {
        'anime': list_deepcopy(anime),
        'second': second,
        'cadr': cadr
    }
    history = history[:history_index + 1]
    history.append(current_state)
    if len(history) > max_history:
        history.pop(0)
    else:
        history_index += 1
def undo():
# Отменяет последнее действие
    global history, history_index, anime, second, cadr
    if history_index > 0:
        history_index -= 1
        state = history[history_index]
        anime = list_deepcopy(state['anime'])
        second = state['second']
        cadr = state['cadr']
        print("Отмена действия")
def redo():
# Повторяет отмененное действие
    global history, history_index, anime, second, cadr
    if history_index < len(history) - 1:
        history_index += 1
        state = history[history_index]
        anime = list_deepcopy(state['anime'])
        second = state['second']
        cadr = state['cadr']
        print("Повтор действия")
def save_animation():
# Сохранение анимации
    global anime, second, current_texture_name
    try:
        with open('textures/' + current_texture_name, 'w') as file:
            file.write(str(anime) + '\n')
            file.write(str(second) + '\n')
        print(f"Анимация сохранена: {current_texture_name}")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
def draw_pixel_with_brush(mouse_x, mouse_y, color, brush_size):
# Рисует пиксель с учетом размера кисти
    global anime, cadr
    center_x = int((mouse_x - x) // 4 - (mouse_x - x) // 4 % pixel)
    center_y = int((mouse_y - y) // 4 - (mouse_y - y) // 4 % pixel)
    half_size = brush_size // 2
    for dx in range(-half_size, half_size + 1):
        for dy in range(-half_size, half_size + 1):
            pixel_x = center_x + dx * pixel
            pixel_y = center_y + dy * pixel
            # Проверяем, есть ли уже пиксель в этой позиции
            found = False
            for j in range(len(anime[cadr][0])):
                if anime[cadr][0][j] == pixel_x and anime[cadr][1][j] == pixel_y:
                    anime[cadr][2][j] = color
                    found = True
                    break
            # Если пикселя нет, добавляем новый
            if not found:
                anime[cadr][0].append(pixel_x)
                anime[cadr][1].append(pixel_y)
                anime[cadr][2].append(color)
def erase_pixel_with_brush(mouse_x, mouse_y, brush_size):
# Стирает пиксель с учетом размера кисти
    global anime, cadr
    center_x = int((mouse_x - x) // 4 - (mouse_x - x) // 4 % pixel)
    center_y = int((mouse_y - y) // 4 - (mouse_y - y) // 4 % pixel)
    half_size = brush_size // 2
    for dx in range(-half_size, half_size + 1):
        for dy in range(-half_size, half_size + 1):
            pixel_x = center_x + dx * pixel
            pixel_y = center_y + dy * pixel
            j = 0
            while j < len(anime[cadr][0]):
                if anime[cadr][0][j] == pixel_x and anime[cadr][1][j] == pixel_y:
                    anime[cadr][0].pop(j)
                    anime[cadr][1].pop(j)
                    anime[cadr][2].pop(j)
                else:
                    j += 1
lastMenuButton = ""
clock = pygame.time.Clock()
save_to_history()
while True:
    screen.fill(menuColor)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                pygame.quit()
            # Обработка назначения новой клавиши
            if waiting_for_key:
                # Проверяем на конфликты
                conflict = False
                for action, key in settings["keys"].items():
                    if key == i.key and action != selected_key_action:
                        print(f"Конфликт! Клавиша {get_key_name(i.key)} уже назначена для {action}")
                        conflict = True
                        break
                if not conflict:
                    settings["keys"][selected_key_action] = i.key
                    save_settings(settings)
                    print(f"Клавиша {get_key_name(i.key)} назначена для {selected_key_action}")
                waiting_for_key = False
                selected_key_action = ""
            # Горячие клавиши
            elif i.key == settings["keys"]["undo"] and (pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]):
                undo()
            elif i.key == settings["keys"]["redo"] and (pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]):
                redo()
            elif i.key == settings["keys"]["save"] and (pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]):
                save_animation()
            elif i.key == settings["keys"]["play_pause"]:
                play = not play
                print("Воспроизведение:", "включено" if play else "выключено")
            elif i.key == settings["keys"]["grid"]:
                show_grid = not show_grid
                print("Сетка:", "включена" if show_grid else "выключена")
            elif i.key == settings["keys"]["palette"] and not (pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]):
                show_palette = not show_palette
                print("Палитра:", "открыта" if show_palette else "закрыта")
            elif i.key == settings["keys"]["frame_left"]:
                if cadr > 0:
                    cadr -= 1
                else:
                    cadr = len(anime) - 1
                print(f"Кадр: {cadr + 1}/{len(anime)}")
            elif i.key == settings["keys"]["frame_right"]:
                if cadr + 1 < len(anime):
                    cadr += 1
                else:
                    cadr = 0
                print(f"Кадр: {cadr + 1}/{len(anime)}")
            if i.key == pygame.K_DELETE:
                if len(anime) > 1:
                    save_to_history()
                    anime.pop(cadr)
                    if cadr != 0:
                        cadr -= 1
            if i.key == 61:
                if cadr+1 == len(anime):
                    cadr = 0
                else:
                    cadr += 1
            if i.key == pygame.K_p:
                save_to_history()
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
                    screen0 = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                else:
                    screen0 = pygame.display.set_mode(current_size, pygame.FULLSCREEN)
                fullScreen = not fullScreen
                settings["display"]["fullscreen"] = fullScreen
                save_settings(settings)
                print("Полноэкранный режим:", "включен" if fullScreen else "выключен")
            if animation_menu and texture_files:
                if i.key == pygame.K_UP:
                    selected_animation_index = (selected_animation_index - 1) % len(texture_files)
                    if selected_animation_index < animation_scroll_offset:
                        animation_scroll_offset = selected_animation_index
                elif i.key == pygame.K_DOWN:
                    selected_animation_index = (selected_animation_index + 1) % len(texture_files)
                    if selected_animation_index >= animation_scroll_offset + max_visible_animations:
                        animation_scroll_offset = selected_animation_index - max_visible_animations + 1
                elif i.key == pygame.K_RETURN:
                    load_animation(texture_files[selected_animation_index])
                    animation_menu = False
                elif i.key == pygame.K_ESCAPE:
                    animation_menu = False
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                if settings_menu:
                    # Слайдер музыки
                    music_slider_x = WIDTH//2 - 100
                    music_slider_y = HEIGHT//2 - 20
                    music_slider_w = 200
                    if (i.pos[0] * k_posX > music_slider_x and i.pos[0] * k_posX < music_slider_x + music_slider_w and
                        i.pos[1] * k_posY > music_slider_y and i.pos[1] * k_posY < music_slider_y + 20):
                        dragging_slider = True
                        dragging_type = "music"
                        relative_x = i.pos[0] * k_posX - music_slider_x
                        settings["sound"]["music_volume"] = int((relative_x / music_slider_w) * 100)
                        settings["sound"]["music_volume"] = max(0, min(100, settings["sound"]["music_volume"]))
                        update_sound_volumes()
                        save_settings(settings)
                        print(f"Громкость музыки: {settings['sound']['music_volume']}%")
                    # Кнопка полноэкранного режима
                    fullscreen_text = menuFont.render("Полноэкранный режим", 1, WHITE)
                    fullscreen_x = WIDTH//2 - fullscreen_text.get_width()//2
                    fullscreen_y = HEIGHT//2 + 40
                    if (i.pos[0] * k_posX > fullscreen_x and i.pos[0] * k_posX < fullscreen_x + fullscreen_text.get_width() and
                        i.pos[1] * k_posY > fullscreen_y and i.pos[1] * k_posY < fullscreen_y + fullscreen_text.get_height()):
                        if fullScreen:
                            screen0 = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                        else:
                            screen0 = pygame.display.set_mode(current_size, pygame.FULLSCREEN)
                        fullScreen = not fullScreen
                        settings["display"]["fullscreen"] = fullScreen
                        save_settings(settings)
                        print("Полноэкранный режим:", "включен" if fullScreen else "выключен")
                    keys_text = menuFont.render("Клавиши", 1, WHITE)
                    keys_x = WIDTH//2 - 40
                    keys_y = HEIGHT//2 + 80
                    if (i.pos[0] * k_posX > keys_x and i.pos[0] * k_posX < keys_x + 80 and
                        i.pos[1] * k_posY > keys_y and i.pos[1] * k_posY < keys_y + keys_text.get_height()):
                        keys_menu = True
                        settings_menu = False
                        print("Открыто меню клавиш")
                    back_text = menuFont.render("Выйти", 1, WHITE)
                    back_x = WIDTH//2 - 30
                    back_y = HEIGHT - 80
                    if (i.pos[0] * k_posX > back_x and i.pos[0] * k_posX < back_x + 60 and
                        i.pos[1] * k_posY > back_y and i.pos[1] * k_posY < back_y + back_text.get_height()):
                        settings_menu = False
                        print("Настройки закрыты")
                if keys_menu and not waiting_for_key:
                    key_actions = ["undo", "redo", "save", "play_pause", "grid", "palette", "frame_left", "frame_right"]
                    action_names = {
                        "undo": "Отмена (Ctrl+)",
                        "redo": "Повтор (Ctrl+)",
                        "save": "Сохранить (Ctrl+)",
                        "play_pause": "Пауза/Воспроизведение",
                        "grid": "Сетка",
                        "palette": "Палитра",
                        "frame_left": "Предыдущий кадр",
                        "frame_right": "Следующий кадр"
                    }
                    start_y = 120
                    for j, action in enumerate(key_actions):
                        action_text = menuFont.render(action_names[action], 1, WHITE)
                        key_text = menuFont.render(get_key_name(settings["keys"][action]), 1, (100, 200, 100))
                        click_x = WIDTH//2 + 100
                        click_y = start_y + j * 30
                        if (i.pos[0] * k_posX > click_x and i.pos[0] * k_posX < click_x + 100 and
                            i.pos[1] * k_posY > click_y and i.pos[1] * k_posY < click_y + key_text.get_height()):
                            waiting_for_key = True
                            selected_key_action = action
                            print(f"Нажмите новую клавишу для {action_names[action]}")
                    back_text = menuFont.render("Назад", 1, WHITE)
                    back_x = WIDTH//2 - 30
                    back_y = HEIGHT - 80
                    if (i.pos[0] * k_posX > back_x and i.pos[0] * k_posX < back_x + 60 and
                        i.pos[1] * k_posY > back_y and i.pos[1] * k_posY < back_y + back_text.get_height()):
                        keys_menu = False
                        settings_menu = True
                        print("Возврат в настройки")
                # Палитра
                palette_clicked = False
                if show_palette:
                    # Цвета
                    for j, color in enumerate(palette_colors):
                        color_x = palette_x + (j % 5) * 35
                        color_y = palette_y + 20 + (j // 5) * 35
                        if (i.pos[0] * k_posX > color_x and i.pos[0] * k_posX < color_x + 30 and
                            i.pos[1] * k_posY > color_y and i.pos[1] * k_posY < color_y + 30):
                            drawColor = color
                            RGB[0][1] = color[0]
                            RGB[1][1] = color[1]
                            RGB[2][1] = color[2]
                            print(f"Выбран цвет: {color}")
                            palette_clicked = True
                            break
                    if not palette_clicked:
                        # Размеры кисти
                        for j, size in enumerate(brush_sizes):
                            brush_x = palette_x + j * 40
                            brush_y = palette_y + 155
                            if (i.pos[0] * k_posX > brush_x and i.pos[0] * k_posX < brush_x + 35 and
                                i.pos[1] * k_posY > brush_y and i.pos[1] * k_posY < brush_y + 35):
                                current_brush_size = size
                                print(f"Выбран размер кисти: {size}")
                                palette_clicked = True
                                break
                    if not palette_clicked:
                        # Закрытие палитры
                        close_x = palette_x + 270
                        close_y = palette_y
                        if (i.pos[0] * k_posX > close_x and i.pos[0] * k_posX < close_x + 25 and
                            i.pos[1] * k_posY > close_y and i.pos[1] * k_posY < close_y + 25):
                            show_palette = False
                            palette_clicked = True
                if not show_palette and not palette_clicked and not settings_menu and not keys_menu:
                    if pen:
                        if i.pos[0] * k_posX > 150 and i.pos[0] * k_posX < WIDTH-100:
                            save_to_history()
                            draw_pixel_with_brush(i.pos[0] * k_posX, i.pos[1] * k_posY, drawColor, current_brush_size)
                    else:
                        if i.pos[0] * k_posX > 150 and i.pos[0] * k_posX < WIDTH-100:
                            save_to_history()
                            erase_pixel_with_brush(i.pos[0] * k_posX, i.pos[1] * k_posY, current_brush_size)
            if i.button == 3:
                for j in range(len(anime[cadr][0])):
                    if int(i.pos[0] * k_posX - x) // 4 - int(i.pos[0] * k_posX - x) // 4 % pixel == anime[cadr][0][j] \
                            and int(i.pos[1] * k_posY - y) // 4 - int(i.pos[1] * k_posY - y) // 4 % pixel == anime[cadr][1][j]:
                        drawColor = anime[cadr][2][j]
                        pass
            if i.button == 4:
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
            if dragging_slider and dragging_type == "music":
                music_slider_x = WIDTH//2 - 100
                music_slider_w = 200
                relative_x = max(0, min(music_slider_w, i.pos[0] * k_posX - music_slider_x))
                settings["sound"]["music_volume"] = int((relative_x / music_slider_w) * 100)
                update_sound_volumes()
        if i.type == pygame.MOUSEBUTTONUP:
            if i.button == 1:
                if dragging_slider:
                    dragging_slider = False
                    dragging_type = ""
                    save_settings(settings)
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
                            buttonMenu = ["Ластик", "Копировать", "Вставить", "Сохранить", "Стоп", "Анимации", "Палитра", "Настройки", "Выйти"]
                            play = True
                            pen = True
                        elif buttonMenu[j] == "Стоп":
                            buttonMenu = ["Ластик", "Копировать", "Вставить", "Сохранить", "Проверить", "Анимации", "Палитра", "Настройки", "Выйти"]
                            play = False
                            pen = True
                            timeCadr = 0
                        elif buttonMenu[j] == "Ластик":
                            pen = False
                            buttonMenu = ["Ручка", "Копировать", "Вставить", "Сохранить", "Проверить", "Анимации", "Палитра", "Настройки", "Выйти"]
                        elif buttonMenu[j] == "Ручка":
                            pen = True
                            buttonMenu = ["Ластик", "Копировать", "Вставить", "Сохранить", "Проверить", "Анимации", "Палитра", "Настройки", "Выйти"]
                        elif buttonMenu[j] == "Копировать":
                            copyAnime = list_deepcopy(anime[cadr])
                            print(list_deepcopy(anime[cadr]))
                        elif buttonMenu[j] == "Вставить":
                            if copyAnime != "none":
                                anime[cadr] = list_deepcopy(copyAnime)
                                print(anime[cadr])
                        elif buttonMenu[j] == "Анимации":
                            animation_menu = True
                        elif buttonMenu[j] == "Палитра":
                            show_palette = not show_palette
                        elif buttonMenu[j] == "Настройки":
                            settings_menu = True
                if animation_menu and texture_files:
                    visible_files = texture_files[animation_scroll_offset:animation_scroll_offset + max_visible_animations]
                    for j, filename in enumerate(visible_files):
                        text = menuFont.render(filename, 1, WHITE)
                        y_pos = 50 + j * (text.get_height() + 5)
                        if (i.pos[0] * k_posX > WIDTH//2 - 200 and 
                            i.pos[0] * k_posX < WIDTH//2 + 200 and
                            i.pos[1] * k_posY > y_pos and 
                            i.pos[1] * k_posY < y_pos + text.get_height()):
                            load_animation(filename)
                            animation_menu = False
                            break
                    back_text = menuFont.render("Назад", 1, WHITE)
                    back_y = HEIGHT - 50
                    if (i.pos[0] * k_posX > WIDTH//2 - 50 and 
                        i.pos[0] * k_posX < WIDTH//2 + 50 and
                        i.pos[1] * k_posY > back_y and 
                        i.pos[1] * k_posY < back_y + back_text.get_height()):
                        animation_menu = False
    if play:
        timeCadr += 1
        if timeCadr == FPS*second // len(anime):
            if cadr + 1 < len(anime):
                cadr += 1
            else:
                cadr = 0
            timeCadr = 0
    # Мини-плеер
    mini_player_timer += 1
    if mini_player_timer >= FPS * second // len(anime):
        mini_player_frame = (mini_player_frame + 1) % len(anime)
        mini_player_timer = 0
    for i in range(len(buttonMenu)):
        colorButton = WHITE
        if pygame.get_init():
            text = menuFont.render(buttonMenu[i], 1, colorButton)
        else:
            continue
        if mouseX > 5 \
                and mouseX < 5 + text.get_width() \
                and mouseY > 5 + i * (text.get_height() + 5) +5 \
                and mouseY < 5 + i * (text.get_height() + 5) + text.get_height() -5:
            if lastMenuButton != buttonMenu[i]:
                lastMenuButton = buttonMenu[i]
            colorButton = (255, 0, 0)
        if pygame.get_init():
            text = menuFont.render(buttonMenu[i], 1, colorButton)
            screen.blit(text, (5, 5+i*(text.get_height()+5)))
    if pygame.get_init():
        textCadr = menuFont.render("cadr: " + str(cadr+1) + "/" + str(len(anime)), 1, WHITE)
        screen.blit(textCadr, (WIDTH-5-textCadr.get_width(), 5))
    else:
        textCadr = pygame.Surface((100, 20))
    pygame.draw.rect(screen, drawColor, (WIDTH-5-textCadr.get_width(), textCadr.get_height()+5, textCadr.get_width(), textCadr.get_width()))
    if pen == False:
        pygame.draw.line(screen, pygame.Color("red"), (WIDTH - 5 - textCadr.get_width(), textCadr.get_height() + 5), (WIDTH - 5, textCadr.get_width()+textCadr.get_height() + 5), 5)
        pygame.draw.line(screen, pygame.Color("red"), (WIDTH - 5, textCadr.get_height() + 5),(WIDTH - 5 - textCadr.get_width(), textCadr.get_width() + textCadr.get_height() + 5), 5)
    if pygame.get_init():
        for i in range(len(RGB)):
            textRGB = menuFont.render(RGB[i][0]+": "+str(RGB[i][1]), 1, WHITE)
            screen.blit(textRGB, (WIDTH - 5 - textCadr.get_width(), 10+textCadr.get_width()+textCadr.get_height()+textRGB.get_height()*i))
        textSecond = menuFont.render("sec: "+str(second), 1, WHITE)
        screen.blit(textSecond, (WIDTH - 5 - textCadr.get_width(), 10 + textCadr.get_width() + textCadr.get_height() + textSecond.get_height() * i + textCadr.get_height()))
    for i in range(len(anime[cadr][0])):
        pygame.draw.rect(screen, anime[cadr][2][i], (anime[cadr][0][i]*4 + x, anime[cadr][1][i]*4 + y, pixel*4, pixel*4))
    # Отрисовка сетки
    if show_grid:
        grid_color = (100, 100, 100)
        # Вертикальные линии
        for i in range(x, x + Size + 1, grid_size):
            pygame.draw.line(screen, grid_color, (i, y), (i, y + Size), 1)
        # Горизонтальные линии
        for i in range(y, y + Size + 1, grid_size):
            pygame.draw.line(screen, grid_color, (x, i), (x + Size, i), 1)
    if hitbox:
        pygame.draw.rect(screen, GREEN, (x, y, Size, Size), 1)
    if animation_menu:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        if pygame.get_init():
            title_text = fontMENU.render("Выберите анимацию", 1, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 10))
        if texture_files:
            visible_files = texture_files[animation_scroll_offset:animation_scroll_offset + max_visible_animations]
            if pygame.get_init():
                for j, filename in enumerate(visible_files):
                    actual_index = animation_scroll_offset + j
                    color = (255, 255, 0) if actual_index == selected_animation_index else WHITE
                    if filename == current_texture_name:
                        color = (0, 255, 0)
                    text = menuFont.render(filename, 1, color)
                    y_pos = 50 + j * (text.get_height() + 5)
                    screen.blit(text, (WIDTH//2 - text.get_width()//2, y_pos))
            if len(texture_files) > max_visible_animations and pygame.get_init():
                scroll_text = menuFont.render(f"{animation_scroll_offset + 1}-{min(animation_scroll_offset + max_visible_animations, len(texture_files))} из {len(texture_files)}", 1, (150, 150, 150))
                screen.blit(scroll_text, (WIDTH//2 - scroll_text.get_width()//2, 50 + max_visible_animations * 25))
        else:
            if pygame.get_init():
                no_files_text = menuFont.render("Файлы анимаций не найдены", 1, WHITE)
                screen.blit(no_files_text, (WIDTH//2 - no_files_text.get_width()//2, HEIGHT//2))
        if pygame.get_init():
            instructions = [
                "↑/↓ - навигация",
                "Enter - выбрать",
                "Escape - назад",
                "Клик мышью - выбрать"
            ]
            for i, instruction in enumerate(instructions):
                inst_text = menuFont.render(instruction, 1, (200, 200, 200))
                screen.blit(inst_text, (10, HEIGHT - 100 + i * 20))
            back_text = menuFont.render("Назад", 1, WHITE)
            back_y = HEIGHT - 50
            pygame.draw.rect(screen, (50, 50, 50), (WIDTH//2 - 50, back_y - 5, 100, back_text.get_height() + 10))
            screen.blit(back_text, (WIDTH//2 - back_text.get_width()//2, back_y))
    # Отрисовка меню настроек
    if settings_menu:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        if pygame.get_init():
            title_text = fontMENU.render("Настройки", 1, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
            # Слайдер громкости музыки
            music_text = menuFont.render("Громкость музыки:", 1, WHITE)
            screen.blit(music_text, (WIDTH//2 - music_text.get_width()//2, HEIGHT//2 - 50))
        music_slider_x = WIDTH//2 - 100
        music_slider_y = HEIGHT//2 - 20
        music_slider_w = 200
        music_slider_h = 20
        pygame.draw.rect(screen, (60, 60, 60), (music_slider_x, music_slider_y, music_slider_w, music_slider_h))
        pygame.draw.rect(screen, WHITE, (music_slider_x, music_slider_y, music_slider_w, music_slider_h), 2)
        fill_width = int((settings["sound"]["music_volume"] / 100.0) * music_slider_w)
        if fill_width > 0:
            pygame.draw.rect(screen, (100, 200, 100), (music_slider_x, music_slider_y, fill_width, music_slider_h))
        slider_pos = music_slider_x + fill_width
        pygame.draw.circle(screen, WHITE, (slider_pos, music_slider_y + music_slider_h//2), 12)
        pygame.draw.circle(screen, (100, 200, 100), (slider_pos, music_slider_y + music_slider_h//2), 8)
        if pygame.get_init():
            volume_text = menuFont.render(f"{settings['sound']['music_volume']}%", 1, WHITE)
            screen.blit(volume_text, (WIDTH//2 - volume_text.get_width()//2, HEIGHT//2 + 10))
            fullscreen_status = "ВКЛ" if fullScreen else "ВЫКЛ"
            fullscreen_text = menuFont.render("Полноэкранный режим", 1, WHITE)
            fullscreen_status_text = menuFont.render(f"[{fullscreen_status}]", 1, (100, 200, 100) if fullScreen else (200, 100, 100))
            fullscreen_x = WIDTH//2 - fullscreen_text.get_width()//2
            fullscreen_y = HEIGHT//2 + 40
            pygame.draw.rect(screen, (50, 50, 50), (fullscreen_x - 10, fullscreen_y - 5, fullscreen_text.get_width() + 20, fullscreen_text.get_height() + 10))
            pygame.draw.rect(screen, (100, 100, 100), (fullscreen_x - 10, fullscreen_y - 5, fullscreen_text.get_width() + 20, fullscreen_text.get_height() + 10), 2)
            screen.blit(fullscreen_text, (fullscreen_x, fullscreen_y))
            screen.blit(fullscreen_status_text, (fullscreen_x + fullscreen_text.get_width() + 10, fullscreen_y))
            keys_text = menuFont.render("Клавиши", 1, WHITE)
            keys_x = WIDTH//2 - 40
            keys_y = HEIGHT//2 + 80
            pygame.draw.rect(screen, (50, 50, 50), (keys_x, keys_y - 5, 80, keys_text.get_height() + 10))
            pygame.draw.rect(screen, (100, 100, 100), (keys_x, keys_y - 5, 80, keys_text.get_height() + 10), 2)
            screen.blit(keys_text, (keys_x + 40 - keys_text.get_width()//2, keys_y))
            back_text = menuFont.render("Выйти", 1, WHITE)
            back_y = HEIGHT - 80
            back_x = WIDTH//2 - 30
            pygame.draw.rect(screen, (50, 50, 50), (back_x, back_y - 5, 60, back_text.get_height() + 10))
            pygame.draw.rect(screen, (100, 100, 100), (back_x, back_y - 5, 60, back_text.get_height() + 10), 2)
            screen.blit(back_text, (back_x + 30 - back_text.get_width()//2, back_y))
    # Отрисовка меню клавиш
    if keys_menu:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        if pygame.get_init():
            title_text = fontMENU.render("Настройка клавиш", 1, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
            if waiting_for_key:
                wait_text = menuFont.render(f"Нажмите новую клавишу для: {selected_key_action}", 1, (255, 255, 0))
                screen.blit(wait_text, (WIDTH//2 - wait_text.get_width()//2, 90))
            else:
                help_text = menuFont.render("Кликните на клавишу для переназначения", 1, (200, 200, 200))
                screen.blit(help_text, (WIDTH//2 - help_text.get_width()//2, 90))
        key_actions = ["undo", "redo", "save", "play_pause", "grid", "palette", "frame_left", "frame_right"]
        action_names = {
            "undo": "Отмена (Ctrl+)",
            "redo": "Повтор (Ctrl+)",
            "save": "Сохранить (Ctrl+)",
            "play_pause": "Пауза/Воспроизведение",
            "grid": "Сетка",
            "palette": "Палитра",
            "frame_left": "Предыдущий кадр",
            "frame_right": "Следующий кадр"
        }
        start_y = 120
        if pygame.get_init():
            for j, action in enumerate(key_actions):
                action_text = menuFont.render(action_names[action], 1, WHITE)
                key_text = menuFont.render(get_key_name(settings["keys"][action]), 1, (100, 200, 100))
                screen.blit(action_text, (WIDTH//2 - 200, start_y + j * 30))
                click_x = WIDTH//2 + 100
                click_y = start_y + j * 30
                pygame.draw.rect(screen, (60, 60, 60), (click_x, click_y - 2, 100, key_text.get_height() + 4))
                pygame.draw.rect(screen, (120, 120, 120), (click_x, click_y - 2, 100, key_text.get_height() + 4), 2)
                screen.blit(key_text, (click_x + 50 - key_text.get_width()//2, click_y))
            # Кнопка "Назад"
            back_text = menuFont.render("Назад", 1, WHITE)
            back_x = WIDTH//2 - 30
            back_y = HEIGHT - 80
            pygame.draw.rect(screen, (50, 50, 50), (back_x, back_y - 5, 60, back_text.get_height() + 10))
            pygame.draw.rect(screen, (100, 100, 100), (back_x, back_y - 5, 60, back_text.get_height() + 10), 2)
            screen.blit(back_text, (back_x + 30 - back_text.get_width()//2, back_y))
    # Отрисовка палитры
    if show_palette:
        palette_width = 300
        palette_height = 210
        pygame.draw.rect(screen, (40, 40, 40), (palette_x - 10, palette_y - 10, palette_width, palette_height))
        pygame.draw.rect(screen, (120, 120, 120), (palette_x - 10, palette_y - 10, palette_width, palette_height), 3)
        if pygame.get_init():
            title_text = menuFont.render("Палитра цветов", 1, WHITE)
            screen.blit(title_text, (palette_x, palette_y - 5))
        for j, color in enumerate(palette_colors):
            color_x = palette_x + (j % 5) * 35
            color_y = palette_y + 20 + (j // 5) * 35
            if color == drawColor:
                pygame.draw.rect(screen, WHITE, (color_x - 2, color_y - 2, 34, 34), 2)
            pygame.draw.rect(screen, color, (color_x, color_y, 30, 30))
            pygame.draw.rect(screen, (100, 100, 100), (color_x, color_y, 30, 30), 1)
        for j, size in enumerate(brush_sizes):
            brush_x = palette_x + j * 40
            brush_y = palette_y + 155
            if size == current_brush_size:
                pygame.draw.rect(screen, WHITE, (brush_x - 2, brush_y - 2, 39, 39), 2)
            pygame.draw.rect(screen, (80, 80, 80), (brush_x, brush_y, 35, 35))
            pygame.draw.rect(screen, (120, 120, 120), (brush_x, brush_y, 35, 35), 1)
            center_x = brush_x + 17
            center_y = brush_y + 17
            brush_size_visual = min(size * 3, 15)
            pygame.draw.rect(screen, WHITE, (center_x - brush_size_visual//2, center_y - brush_size_visual//2, brush_size_visual, brush_size_visual))
            if pygame.get_init():
                size_text = menuFont.render(str(size), 1, WHITE)
                screen.blit(size_text, (brush_x + 17 - size_text.get_width()//2, brush_y + 25))
        close_x = palette_x + 270
        close_y = palette_y
        pygame.draw.rect(screen, (200, 50, 50), (close_x, close_y, 25, 25))
        pygame.draw.rect(screen, WHITE, (close_x, close_y, 25, 25), 1)
        if pygame.get_init():
            close_text = menuFont.render("×", 1, WHITE)
            screen.blit(close_text, (close_x + 7, close_y + 2))
    # Отрисовка мини-плеера
    if not animation_menu:
        pygame.draw.rect(screen, (40, 40, 40), (mini_player_x - 5, mini_player_y - 5, mini_player_size + 10, mini_player_size + 30))
        pygame.draw.rect(screen, (80, 80, 80), (mini_player_x - 5, mini_player_y - 5, mini_player_size + 10, mini_player_size + 30), 2)
        if len(anime) > 0 and mini_player_frame < len(anime):
            current_frame = anime[mini_player_frame]
            if len(current_frame[0]) > 0:
                scale = mini_player_size / Size
                for i in range(len(current_frame[0])):
                    mini_x = mini_player_x + int(current_frame[0][i] * 4 * scale)
                    mini_y = mini_player_y + int(current_frame[1][i] * 4 * scale)
                    mini_size = max(1, int(pixel * 4 * scale))
                    pygame.draw.rect(screen, current_frame[2][i], (mini_x, mini_y, mini_size, mini_size))
        # Подпись файла
        if pygame.get_init():
            file_text = menuFont.render(current_texture_name.replace('.txt', ''), 1, WHITE)
            screen.blit(file_text, (mini_player_x + mini_player_size//2 - file_text.get_width()//2, mini_player_y + mini_player_size + 5))
    # Отображение информации о горячих клавишах
    if not animation_menu and not settings_menu and not keys_menu:
        hotkeys_text = [
            f"Ctrl+{get_key_name(settings['keys']['undo'])} - отмена",
            f"Ctrl+{get_key_name(settings['keys']['redo'])} - повтор", 
            f"Ctrl+{get_key_name(settings['keys']['save'])} - сохранить",
            f"{get_key_name(settings['keys']['play_pause'])} - пауза/воспроизведение",
            f"{get_key_name(settings['keys']['grid'])} - сетка",
            f"{get_key_name(settings['keys']['palette'])} - палитра",
            f"{get_key_name(settings['keys']['frame_left'])} {get_key_name(settings['keys']['frame_right'])} - смена кадра"
        ]
        if pygame.get_init():
            for i, hotkey in enumerate(hotkeys_text):
                text = menuFont.render(hotkey, 1, (150, 150, 150))
                screen.blit(text, (5, HEIGHT - 120 + i * 20))
    virtual_display = pygame.transform.scale(screen, current_size)
    screen0.blit(virtual_display, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()