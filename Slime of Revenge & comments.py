# ===== ИМПОРТЫ БИБЛИОТЕК =====
import pygame                                        # Основная библиотека для создания игр
import math                                          # Математические функции (тригонометрия, корни)
import sys                                           # Системные функции (выход из программы)
import ast                                           # Парсинг Python-структур из текстовых файлов
import os                                            # Операции с файловой системой
from win32api import GetSystemMetrics               # Получение размеров экрана (Windows API)
from enum import Enum                               # Перечисления для структурирования констант
import json                                          # Работа с JSON файлами (настройки)
import random                                        # Генерация случайных чисел (звезды, эффекты)

# ==============================================
# Slime of Revenge — основной игровой модуль
# ----------------------------------------------
# В этом файле содержится полный игровой цикл,
# система меню, загрузка настроек и ресурсов,
# обработка ввода, физика персонажа, отрисовка,
# а также генерация параллакс-фона и логика уровней.
# 
# Структура файла (крупно):
#  - Импорты и инициализация Pygame
#  - Настройки/сохранения (JSON), биндинги клавиш
#  - Глобальные константы и переменные состояния
#  - Загрузка текстур и анимаций
#  - Инициализация звуков и параллакс-фона
#  - Главный игровой цикл с состояниями
#  - Физика, коллизии, рендеринг
#  - Инициализация окна/полноэкранного режима
#  - Аудио-ресурсы и их уровни громкости
#  - Загрузка графических данных (текстуры из *.txt)
#  - Параллакс-фон (звёзды + луна)
#  - Главный цикл с режимами: menu, settings, maps, game
#  - Обработка событий (клавиатура/мышь)
#  - Физика и взаимодействие с миром
#  - Противники, выстрелы, коллизии
#  - Рендеринг всех слоёв
# ==============================================

# ===== ИНИЦИАЛИЗАЦИЯ ШРИФТОВ =====
pygame.font.init()                                   # Инициализация системы шрифтов pygame

# ===== ПУТИ К ФАЙЛАМ =====
lol = os.path.dirname(os.path.abspath(__file__))     # Получаем путь к текущей папке игры
# directory = lol+"/maps"
# files = os.listdir(directory)

# ===== НАСТРОЙКИ И СОХРАНЕНИЯ (JSON) =====
# Система настроек позволяет сохранять:
# - Биндинги клавиш (клавиатура + мышь)
# - Громкость музыки и звуковых эффектов
# - Настройки дисплея (полноэкранный режим, FPS)
# - Статистику прохождения уровней
# -------------------------------------------------

def load_settings():
    """Загружает настройки из settings.json или создает дефолтные.
    
    Returns:
        dict: Словарь с настройками игры
    """
    default_settings = {
        "fullscreen": False,
        "keys": {
            "UP": pygame.K_w,
            "DOWN": pygame.K_s,
            "LEFT": pygame.K_a,
            "RIGHT": pygame.K_d,
            "JUMP": pygame.K_SPACE,
            "DASH": pygame.K_RSHIFT,
            "SHOOT": "MOUSE_1"
        },
        "sound": {
            "music_volume": 15,
            "sfx_volume": 100
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
            "current_level_deaths": 0,
            "current_level_name": ""
        }
    }
    try:
        with open('settings.json', 'r', encoding='utf-8') as f:
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
    """Сохраняет настройки в settings.json.
    
    Args:
        settings (dict): Словарь настроек для сохранения
    """
    try:
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка сохранения настроек: {e}")
def get_key_name(key):
    """Преобразует код клавиши pygame в читаемое название.
    
    Args:
        key: Код клавиши pygame или строка "MOUSE_n"
        
    Returns:
        str: Название клавиши для отображения в UI
    """
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
# ===== ЗАГРУЗКА НАСТРОЕК И ИНИЦИАЛИЗАЦИЯ КЛАВИШ =====
settings = load_settings()                           # Загружаем настройки из файла

# Глобальные переменные для клавиш управления (инициализируются в init_keys())
UP = None                                           # Клавиша движения вверх
DOWN = None                                         # Клавиша движения вниз
LEFT = None                                         # Клавиша движения влево
RIGHT = None                                        # Клавиша движения вправо
JUMP = None                                         # Клавиша прыжка
DASH = None                                         # Клавиша рывка
SHOOT = None                                        # Клавиша стрельбы
def is_key_pressed(key_bind, event):
    """Проверяет, нажата ли привязанная клавиша.
    
    Args:
        key_bind: Код клавиши или строка "MOUSE_n"
        event: Событие pygame
        
    Returns:
        bool: True если клавиша нажата
    """
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
    """Проверяет, отпущена ли привязанная клавиша.
    
    Args:
        key_bind: Код клавиши или строка "MOUSE_n"
        event: Событие pygame
        
    Returns:
        bool: True если клавиша отпущена
    """
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
    """Инициализирует глобальные переменные клавиш из настроек.
    Загружает биндинги из settings.json в глобальные переменные UP, DOWN, LEFT, RIGHT, JUMP, DASH, SHOOT.
    """
    global UP, DOWN, LEFT, RIGHT, JUMP, DASH, SHOOT
    UP = settings["keys"]["UP"]
    DOWN = settings["keys"]["DOWN"]
    LEFT = settings["keys"]["LEFT"]
    RIGHT = settings["keys"]["RIGHT"]
    JUMP = settings["keys"]["JUMP"]
    DASH = settings["keys"]["DASH"]
    SHOOT = settings["keys"]["SHOOT"]
# ===== ИНИЦИАЛИЗАЦИЯ КЛАВИШ И UI ПЕРЕМЕННЫХ =====
init_keys()                                         # Инициализируем клавиши из настроек

# Переменные для интерфейса настроек
gameButton = ""                                     # Текущая нажимаемая кнопка
waitingForKey = False                               # Ожидаем ли нажатия клавиши для переназначения
selectedKeyAction = ""                              # Выбранное действие для переназначения
dragging_slider = False                             # Перетаскиваем ли слайдер громкости
dragging_type = ""                                  # Тип перетаскиваемого слайдера

# Система уведомлений
notification_text = ""                              # Текст уведомления
notification_time = 0                               # Время показа уведомления
notification_duration = 3000                        # Длительность показа уведомления (в миллисекундах)

def update_sound_volumes():
    """Применяет настройки громкости к музыке и звуковым эффектам.
    Обновляет громкость всех загруженных звуков согласно settings.json.
    """
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
    shootSound.set_volume(0.3 * sfx_vol)
    misfireSound.set_volume(0.7 * sfx_vol)
    chargerSound.set_volume(2 * sfx_vol)
    stopEnemyFlySound.set_volume(0.5 * sfx_vol)
    startEnemyFlySound.set_volume(4 * sfx_vol)

def start_level_timer(level_name):
    """Начинает отсчет времени для уровня.
    
    Args:
        level_name (str): Название уровня для статистики
    """
    settings["statistics"]["current_level_name"] = level_name
    settings["statistics"]["current_level_start_time"] = pygame.time.get_ticks()
    settings["statistics"]["current_level_deaths"] = 0
    save_settings(settings)
def pause_on():
    """Включает паузу и сохраняет время паузы."""
    settings["statistics"]["current_level_pause_on"] = pygame.time.get_ticks()
    save_settings(settings)
def pause_off():
    """Выключает паузу и корректирует время уровня."""
    settings["statistics"]["current_level_start_time"] += pygame.time.get_ticks() - settings["statistics"]["current_level_pause_on"]
    save_settings(settings)
def add_death():
    """Увеличивает счетчик смертей на текущем уровне."""
    if settings["statistics"]["current_level_name"]:
        settings["statistics"]["current_level_deaths"] += 1
        save_settings(settings)
def finish_level():
    """Завершает уровень и сохраняет статистику.
    
    Сохраняет время прохождения и количество смертей в settings.json.
    """
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
    """Возвращает текущее время прохождения уровня в секундах.
    
    Returns:
        float: Время в секундах с учетом пауз
    """
    if settings["statistics"]["current_level_start_time"] > 0:
        current_time = pygame.time.get_ticks()
        return (current_time - settings["statistics"]["current_level_start_time"]) / 1000.0
    return 0
def format_time(seconds):
    """Форматирует время в читаемый вид MM:SS.
    
    Args:
        seconds (float): Время в секундах
        
    Returns:
        str: Время в формате "MM:SS"
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 100)
    return f"{minutes:02d}:{secs:02d}.{millisecs:02d}"
def show_notification(text):
    """Показывает уведомление на экране.
    
    Args:
        text (str): Текст уведомления
    """
    global notification_text, notification_time
    notification_text = text
    notification_time = pygame.time.get_ticks()

# ===== СТАТИСТИКА И ТАЙМЕРЫ УРОВНЕЙ =====
# Система отслеживает:
# - Время прохождения каждого уровня
# - Количество смертей на уровне
# - Общую статистику по всем картам
# - Паузы и возобновления игры
# -------------------------------------------------

### приколы /\ /\ /\
###         || || ||

# ===== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ СОСТОЯНИЯ =====
# Основные переменные, управляющие состоянием игры:
# - Позиция и движение игрока
# - Состояния анимаций и эффектов
# - Игровые объекты и их свойства
# - UI элементы и меню
# -------------------------------------------------

WIDTH = 889
HEIGHT = 500
# ===== ЦВЕТОВАЯ ПАЛИТРА =====
# Основные цвета игры
BLACK = (0, 0, 0)                    # Черный
BLUE = (71, 153, 192)                # Синий
WHITE = (225, 225, 225)              # Белый
GREEN = (0, 250, 0)                  # Зеленый (игрок)
GREEN2 = (150, 220, 150)             # Светло-зеленый
GREEN_d = (0, 255, 221)              # Голубовато-зеленый
GREEN_d2 = (151, 204, 190)           # Приглушенный зеленый
PURPLE = (171, 100, 237)             # Фиолетовый
PURPLE2 = (192, 181, 196)            # Светло-фиолетовый

# Цвета игровых объектов
colorGG = GREEN                       # Цвет игрока
colorGG2 = GREEN2                     # Альтернативный цвет игрока
menuColor = (33, 57, 94)             # Цвет меню
colorBullets1 = (116, 247, 40)       # Цвет пуль (яркий)
colorBullets2 = (60, 120, 135)       # Цвет пуль (приглушенный)
colorBullets = colorBullets2         # Текущий цвет пуль

# Цвета фонов для редактора
backRED = (163, 95, 95)              # Красноватый фон
backGREEN = (54, 64, 40)             # Зеленоватый фон
backGRAY = (158, 158, 158)           # Серый фон
backBROWN = (115, 91, 76)            # Коричневый фон
backYELLOW = (184, 183, 141)         # Желтоватый фон
backPURPLE = (196, 183, 201)         # Фиолетоватый фон
backColor = [backRED, backGREEN, backGRAY, backBROWN, backYELLOW, backPURPLE]
createColor = backColor[0]            # Текущий цвет создания
# ===== ШРИФТЫ =====
font = pygame.font.SysFont("Calibri", 23, 1)      # Основной шрифт для UI
menuFont = pygame.font.SysFont("Calibri", 33, 1)  # Шрифт для меню
fontMENU = pygame.font.SysFont("Calibri", 50, 1)  # Большой шрифт для заголовков

# ===== ГРАНИЦЫ ИГРОВОГО ПОЛЯ =====
minY = HEIGHT-50                                   # Нижняя граница игрового поля

# ===== КООРДИНАТЫ ИГРОКА =====
# Позиция игрока в игровом мире
TrueX = WIDTH//2                                    # Центр экрана по X
TrueY = HEIGHT//2                                   # Центр экрана по Y
x = TrueX                                          # Текущая позиция X
y = TrueY                                          # Текущая позиция Y
spawnX = x                                         # Точка возрождения X
spawnY = y                                         # Точка возрождения Y
xO = x                                             # Предыдущая позиция X (для анимации)
yO = y                                             # Предыдущая позиция Y (для анимации)

# Координаты камеры (смещение экрана)
surfX = 0                                          # Смещение камеры по X
surfY = 0                                          # Смещение камеры по Y
spawnSX = surfX                                    # Смещение камеры в точке спавна
spawnSY = surfY                                    # Смещение камеры в точке спавна

# Координаты мыши
mouseX = 0                                         # Позиция мыши X
mouseY = 0                                         # Позиция мыши Y
firstMouseX = 0                                    # Начальная позиция мыши X (для перетаскивания)
firstMouseY = 0                                    # Начальная позиция мыши Y (для перетаскивания)
# ===== СТРУКТУРА КАРТЫ =====
# Карта уровня содержит все игровые объекты:
# - block: блоки (платформы) [x[], y[], width[], height[]]
# - spikes: шипы [x[], y[], width[], height[]]
# - spring: пружины [x[], y[], width[], height[]]
# - rollback: точки отката [x[], y[], width, height, []]
# - background: фоновые объекты [x[], y[], width[], height[], color[]]
# - spawnpoint: точка спавна [x[], y[], width, height, -1]
# - bullets: патроны [x[], y[], width, height, [], []]
# - enemyFly: летающие враги [x[], y[], width, height, [], [], [], [animations], [], [], []]
# - finish: финиш [x[], y[], width, height]
map = {"block": [[], [], [], []], "spikes": [[], [], [], []], "spring": [[], [], [], []],
        "rollback": [[], [], 8, 8, []], "background": [[], [], [], [], []],
        "spawnpoint": [[], [], 21, 21, -1], "bullets": [[], [], 15, 15, [], []],
       "enemyFly": [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []], "finish": [[], [], 24, 24]}
# ===== ЗАГРУЗКА КАРТЫ (ЗАКОММЕНТИРОВАНО) =====
# Пример загрузки карты из файла (в данный момент не используется)
'''
with open('map.txt', 'r') as file:                   # Открываем файл карты
    text = file.read()                               # Читаем содержимое
map = ast.literal_eval(text)                         # Преобразуем текст в Python-структуру
'''
# ===== РЕДАКТОР КАРТ =====
letMap = "none"                                     # Текущая карта (загружается из файла)
createType = "block"                                # Тип создаваемого объекта в редакторе
correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [], "background": [],
                 "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}  # Корректировка объектов
draw = 0                                           # Флаг режима рисования

# ===== РАЗМЕРЫ ОБЪЕКТОВ =====
Size = 21                                          # Размер игрока
surf = 34                                          # Размер поверхности
# ===== ИНВЕНТАРЬ И ПУЛИ =====
# Система патронов
bullets = 0                                         # Текущее количество патронов
bulletsMax = 16                                     # Максимальное количество патронов
inventory = [20, HEIGHT-80]                         # Позиция отображения инвентаря
bulletsCadr = bullets * 2                           # Кадр анимации патронов
bulletTime = 0                                      # Таймер для патронов

# Летящие пули
flyBullets = [[], [], [], []]                       # [x[], y[], direction[], active[]]
# ===== ПАРАМЕТРЫ ПУЛЬ =====
speedBullets = 30                                   # Скорость полета пуль
lengthBullets = 20                                  # Длина пуль
# ===== СОСТОЯНИЯ ДВИЖЕНИЯ ИГРОКА =====
# Управление движением персонажа
motionU = "stop"                                    # Движение вверх
motionD = "stop"                                    # Движение вниз
motionL = "stop"                                    # Движение влево
motionR = "stop"                                    # Движение вправо
jump = "stop"                                       # Прыжок
jumpWallL = "stop"                                  # Прыжок от левой стены
jumpWallR = "stop"                                  # Прыжок от правой стены
dash = "stop"                                       # Рывок
shoot = "stop"                                      # Стрельба
# ===== НАПРАВЛЕНИЯ =====
lastButton = "right"                                # Последнее направление движения
NDash = lastButton                                  # Направление рывка
# ===== ФИЗИЧЕСКИЕ ПАРАМЕТРЫ =====
# Коэффициенты физики
kG = 0.81                                          # Коэффициент гравитации

# Скорости движения
maxSpeed = 4                                        # Максимальная скорость ходьбы
speed = 0                                           # Текущая скорость
J = 10 * math.sqrt(kG)                              # Сила прыжка
SpringJ = 15 * math.sqrt(kG)                        # Сила пружины
speedJ = J                                          # Скорость прыжка
maxSpeedG = 10                                      # Максимальная скорость падения
speedG = 0                                          # Текущая скорость падения
speedSX = 0                                         # Скорость по X
speedSY = 0                                         # Скорость по Y
speedDash = 10                                      # Скорость рывка
# ===== УСКОРЕНИЯ =====
g = 0.5 * kG                                        # Ускорение свободного падения
surfG = 0.4                                         # Ускорение на поверхности
# ===== ВСПОМОГАТЕЛЬНЫЕ ФЛАГИ =====
grav = 1                                            # Флаг гравитации
canJump = False                                     # Можно ли прыгать
canJumpWallL = False                                # Можно ли прыгать от левой стены
canJumpWallR = False                                # Можно ли прыгать от правой стены
canDash = False                                     # Можно ли делать рывок
canShoot = True                                     # Можно ли стрелять
gameMode = "surv"                                   # Режим игры (surv - выживание)
stopRun = 0                                         # Счетчик остановки бега
spring = 0                                          # Флаг пружины
# ===== ТАЙМЕРЫ =====
maxTimeDash = 15                                    # Максимальное время рывка
timeDash = 0                                        # Текущее время рывка
timeShoot = 0                                       # Таймер стрельбы
timeRollback = 600                                  # Таймер отката
timeCoyoteL = 5                                     # Таймер койота-прыжка (левая стена)
timeCoyoteR = 5                                     # Таймер койота-прыжка (правая стена)
# ===== СОСТОЯНИЯ МЕНЮ =====
menu = "menu"                                       # Текущее состояние меню
buttonMenu = ["Играть", "Карты", "Создать", "Настройки", "Выйти"]  # Кнопки главного меню
canCreate = False                                   # Можно ли создавать карты
# ===== НАСТРОЙКИ КЛАВИШ =====
# Старые хардкодные настройки (заменены на JSON)
'''UP = pygame.K_w
DOWN = pygame.K_s
LEFT = pygame.K_a
RIGHT = pygame.K_d
JUMP = pygame.K_SPACE
DASH = 3 # pygame.K_RSHIFT
SHOOT = 1'''
gameButton = ""                                     # Текущая нажимаемая кнопка

# ===== НАСТРОЙКИ ДИСПЛЕЯ =====
FPS = 60                                           # Частота кадров
# ===== ИНИЦИАЛИЗАЦИЯ PYGAME И ДИСПЛЕЯ =====
# Настройка аудио системы pygame
pygame.mixer.pre_init(44100, -16, 2, 512)          # Частота: 44.1kHz, битность: 16, каналы: 2, буфер: 512
pygame.init()                                       # Инициализация всех модулей pygame

# Создание игровых поверхностей
screen = pygame.Surface((WIDTH, HEIGHT))            # Внутренняя поверхность сцены (виртуальное разрешение)
fullScreen = True                                   # Текущее состояние окна: полноэкранный или оконный режим
current_size = (GetSystemMetrics(0), GetSystemMetrics(1))  # Фактический размер окна/экрана (в пикселях)

def set_display_mode(enable_fullscreen):
    """Переключает полноэкранный/оконный режим и пересчитывает коэффициенты масштабирования мыши.

    Args:
        enable_fullscreen (bool): True для полноэкранного, False для оконного по центру
    """
    global fullScreen, current_size, screen0, k_posX, k_posY
    
    if enable_fullscreen:
        # Полноэкранный режим — под размер физического экрана
        current_size = (GetSystemMetrics(0), GetSystemMetrics(1))  # Получаем размеры монитора
        screen0 = pygame.display.set_mode(current_size, pygame.FULLSCREEN)  # Создаем полноэкранное окно
        fullScreen = True
    else:
        # Оконный режим — фиксированный размер, центрируем через SDL переменную
        os.environ['SDL_VIDEO_CENTERED'] = '1'      # Центрируем окно на экране
        current_size = (WIDTH, HEIGHT)               # Используем стандартный размер игры
        screen0 = pygame.display.set_mode(current_size, pygame.RESIZABLE)  # Создаем изменяемое окно
        fullScreen = False
    
    # Коэффициенты пересчёта позиции мыши -> виртуальные координаты сцены
    # Нужны для корректной работы мыши при разных разрешениях
    k_posX = WIDTH / current_size[0]                # Коэффициент масштабирования по X
    k_posY = HEIGHT / current_size[1]               # Коэффициент масштабирования по Y

# Устанавливаем полноэкранный режим по умолчанию
set_display_mode(True)

# ===== ПАРАЛЛАКС-ФОН: ЗВЁЗДНОЕ НЕБО С ЛУНОЙ =====
# Создание многослойного фона для эффекта глубины
star_layers = []                                    # Слои звезд для параллакс-эффекта
bg_width = WIDTH * 4                                # Ширина фона (в 4 раза больше экрана)
bg_height = HEIGHT * 3                              # Высота фона (в 3 раза больше экрана)
moon_surface = None                                 # Поверхность с луной
moon_base_pos = (int(WIDTH * 1.6), int(HEIGHT * 0.55))  # Базовая позиция луны на фоне

def init_parallax_background():
    """Генерирует слои звёзд и поверхность луны для параллакс-фона.

    - Несколько слоёв звёзд с разной скоростью смещения (factor)
    - Полупрозрачная луна с простыми кратерами
    Результаты кэшируются в глобальных переменных для повторного использования.
    """
    global star_layers, moon_surface
    random.seed(42)
    star_layers.clear()
    layer_specs = [
        # (num_stars, parallax_factor, color, size)
        (220, 0.15, (220, 220, 255), 1),
        (140, 0.35, (200, 205, 255), 1),
        (80,  0.6,  (255, 255, 255), 2),
    ]
    for num_stars, factor, color, size in layer_specs:
        positions = [(random.randrange(0, bg_width), random.randrange(0, bg_height)) for _ in range(num_stars)]
        star_layers.append({
            "positions": positions,
            "factor": factor,
            "color": color,
            "size": size,
        })

    # Луна
    radius = max(40, HEIGHT // 8)
    moon_diameter = radius * 2
    surf = pygame.Surface((moon_diameter + 20, moon_diameter + 20), pygame.SRCALPHA)
    center = (surf.get_width() // 2, surf.get_height() // 2)
    # свечение
    for r, alpha in ((radius + 18, 20), (radius + 12, 35), (radius + 6, 60)):
        pygame.draw.circle(surf, (250, 250, 220, alpha), center, r)
    # диск луны
    pygame.draw.circle(surf, (235, 235, 210), center, radius)
    # кратеры
    crater_specs = [
        (-radius // 3, -radius // 4, radius // 6),
        (radius // 5, -radius // 6, radius // 7),
        (-radius // 6, radius // 6, radius // 8),
        (radius // 4, radius // 5, radius // 9),
    ]
    for dx, dy, cr in crater_specs:
        pygame.draw.circle(surf, (210, 210, 195), (center[0] + dx, center[1] + dy), cr)
        pygame.draw.circle(surf, (200, 200, 185), (center[0] + dx + cr // 4, center[1] + dy + cr // 4), cr // 2)

    global moon_surface
    moon_surface = surf

def draw_parallax_background(target_surf: pygame.Surface, camera_x: int, camera_y: int):
    """Рисует параллакс-фон на `target_surf` с учётом смещения камеры.

    camera_x, camera_y — виртуальные координаты смещения сцены, чтобы добиться
    эффекта параллакса (дальние объекты двигаются медленнее).
    """
    # базовый цвет неба
    target_surf.fill((6, 9, 22))

    # звёзды слоями
    for layer in star_layers:
        positions = layer["positions"]
        factor = layer["factor"]
        color = layer["color"]
        size = layer["size"]
        off_x = int((camera_x * factor) % bg_width)
        off_y = int((camera_y * factor) % bg_height)
        for sx, sy in positions:
            x = sx - off_x
            y = sy - off_y
            # дублируем по краям, чтобы покрыть экран
            for dx in (-bg_width, 0, bg_width):
                px = x + dx
                if px < -size or px > WIDTH:
                    continue
                for dy in (-bg_height, 0, bg_height):
                    py = y + dy
                    if py < -size or py > HEIGHT:
                        continue
                    target_surf.fill(color, (px, py, size, size))

    # луна (самый дальний слой)
    if moon_surface is not None:
        moon_factor = 0.08
        mx = int(moon_base_pos[0] - camera_x * moon_factor)
        my = int(moon_base_pos[1] - camera_y * moon_factor)
        target_surf.blit(moon_surface, (mx - moon_surface.get_width() // 2, my - moon_surface.get_height() // 2))

# ===== ИНИЦИАЛИЗАЦИЯ ПАРАЛЛАКС-ФОНА =====
init_parallax_background()                          # Создаем звездное небо и луну

# ===== ЗАГРУЗКА АУДИО РЕСУРСОВ =====
# Главная тема меню (фоновая музыка)
pygame.mixer.music.load(lol+r"\sounds\menu.mp3")    # Загружаем музыку меню
pygame.mixer.music.set_volume(0.15)                 # Устанавливаем громкость музыки
pygame.mixer.music.play(-1, 1)                      # Запускаем музыку в цикле с задержкой 1 секунда

# ===== ЗВУКОВЫЕ ЭФФЕКТЫ =====
# Звук клика (основной звук интерфейса)
clickSound = pygame.mixer.Sound(lol+'\sounds\click.ogg')  # Загружаем звук клика
clickSound.set_volume(1)                            # Устанавливаем громкость звука
# Звуки интерфейса
scrollSound = pygame.mixer.Sound(lol+'\sounds\scroll.ogg')        # Звук прокрутки
scrollSound.set_volume(3)                                         # Громкость прокрутки

# Звуки движения игрока
runSound = pygame.mixer.Sound(lol+'\sounds\Run.ogg')              # Звук бега
runSound.set_volume(0.2)                                          # Громкость бега
runSo = -1                                                        # Флаг воспроизведения бега
playSoundRun = 1                                                  # Флаг возможности воспроизведения бега
playSoundSlide = 1                                                # Флаг возможности воспроизведения скольжения

jumpSound = pygame.mixer.Sound(lol+'\sounds\jump.ogg')            # Звук прыжка
jumpSound.set_volume(1)                                           # Громкость прыжка

dropSound = pygame.mixer.Sound(lol+'\sounds\drop.ogg')            # Звук падения
dropSound.set_volume(0.8)                                         # Громкость падения

dashSound = pygame.mixer.Sound(lol+'\sounds\dash.ogg')            # Звук рывка
dashSound.set_volume(0.5)                                         # Громкость рывка

# Звуки игровых событий
saveSound = pygame.mixer.Sound(lol+'\sounds\save.ogg')            # Звук сохранения
saveSound.set_volume(0.2)                                         # Громкость сохранения

rollbackSound = pygame.mixer.Sound(lol+'\sounds\Rollback.ogg')    # Звук отката
rollbackSound.set_volume(3)                                       # Громкость отката

dieSound = pygame.mixer.Sound(lol+'\sounds\die.ogg')              # Звук смерти игрока
dieSound.set_volume(1)                                            # Громкость смерти

# Звуки оружия
shootSound = pygame.mixer.Sound(lol+'\sounds\Shoot.ogg')          # Звук выстрела
shootSound.set_volume(0.3)                                        # Громкость выстрела

misfireSound = pygame.mixer.Sound(lol+'\sounds\misfire.ogg')      # Звук осечки
misfireSound.set_volume(0.7)                                      # Громкость осечки

chargerSound = pygame.mixer.Sound(lol+'\sounds\charger.ogg')      # Звук перезарядки
chargerSound.set_volume(2)                                        # Громкость перезарядки

# Звуки врагов
stopEnemyFlySound = pygame.mixer.Sound(lol+'\sounds\StartEnemy.ogg')  # Звук остановки врага
stopEnemyFlySound.set_volume(0.5)                                 # Громкость остановки врага

startEnemyFlySound = pygame.mixer.Sound(lol+'\sounds\StoptEnemy.ogg') # Звук запуска врага
startEnemyFlySound.set_volume(4)                                  # Громкость запуска врага

# Звуки столкновений
hitWallSound = pygame.mixer.Sound(lol+'\sounds\hitWall.ogg')      # Звук удара о стену
hitWallSound.set_volume(0.6)                                      # Громкость удара о стену

hitEnemSound = pygame.mixer.Sound(lol+'\sounds\hitEnem.ogg')      # Звук попадания во врага
hitEnemSound.set_volume(0.4)                                      # Громкость попадания во врага

dieEnemySound = pygame.mixer.Sound(lol+'\sounds\dieEnemy.ogg')    # Звук смерти врага
dieEnemySound.set_volume(0.7)                                     # Громкость смерти врага

# Звук завершения уровня
finishSound = pygame.mixer.Sound(lol+'\sounds\Finish.ogg')        # Звук финиша
finishSound.set_volume(1)                                         # Громкость финиша

# ===== ИНИЦИАЛИЗАЦИЯ ЗВУКОВ =====
lastMenuButton = ""                                               # Последняя нажатая кнопка меню
update_sound_volumes()                                            # Применяем настройки громкости
# ===== ЗАГРУЗКА ТЕКСТУР И АНИМАЦИЙ (ДИЗАЙН) =====
# Текстуры хранятся в текстовых файлах формата:
# [ [x_offsets], [y_offsets], [colors] ] для каждого кадра анимации.
# Ниже последовательно подгружаются наборы спрайтов для игрока, оружия, врагов и объектов.
# Параллельно считываем длительности (Sec) для вычисления кадров по FPS.
# -------------------------------------------------
# ===== ЗАГРУЗКА АНИМАЦИЙ ИГРОКА =====
# Анимация остановки (стояние на месте)
with open('textures/GGStop.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    GGStop = ast.literal_eval(text1)                # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    GGStopSec = ast.literal_eval(text2)             # Преобразуем в список длительностей

# Анимация бега
with open('textures/GGRun.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    GGRun = ast.literal_eval(text1)                 # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    GGRunSec = ast.literal_eval(text2)              # Преобразуем в список длительностей

# Анимация прыжка
with open('textures/GGJump.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    GGJump = ast.literal_eval(text1)                # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    GGJumpSec = ast.literal_eval(text2)             # Преобразуем в список длительностей

# Анимация прыжка в беге
with open('textures/GGJumpRun.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    GGJumpRun = ast.literal_eval(text1)             # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    GGJumpRunSec = ast.literal_eval(text2)          # Преобразуем в список длительностей

# Анимация рывка
with open('textures/GGDash.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    GGDash = ast.literal_eval(text1)                # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    GGDashSec = ast.literal_eval(text2)             # Преобразуем в список длительностей

# Анимация рывка в беге
with open('textures/GGDashRun.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    GGDashRun = ast.literal_eval(text1)             # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    GGDashRunSec = ast.literal_eval(text2)          # Преобразуем в список длительностей
# ===== АНИМАЦИЯ СПАВНА И ЭФФЕКТОВ =====
# Анимация спавна (появления игрока)
timeCadrRoll = 0                                    # Счетчик кадров анимации спавна
cadrRoll = 0                                        # Текущий кадр анимации спавна

# Анимация отката (первая версия)
with open('textures/RollBack.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    RollBackTexture = ast.literal_eval(text1)       # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    RollBackSec = ast.literal_eval(text2)           # Преобразуем в список длительностей

# Анимация отката (вторая версия)
with open('textures/RollBack2.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    RollBackTexture2 = ast.literal_eval(text1)      # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    RollBackSec2 = ast.literal_eval(text2)          # Преобразуем в список длительностей
# ===== ЗАГРУЗКА ОРУЖИЯ =====
# Текстура пистолета
with open('textures/Gun.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    GUN = ast.literal_eval(text1)                   # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    GunSec = ast.literal_eval(text2)                # Преобразуем в список длительностей

# Создание поверхности для пистолета
Gun = GUN[0]                                        # Берем первый кадр анимации пистолета
GunSurf = pygame.Surface((max(Gun[0])+2, max(Gun[1])+2), pygame.SRCALPHA)  # Создаем поверхность с прозрачностью
GunSurfR = GunSurf                                  # Копия поверхности для поворота
pivotGun = [int(-surfX + x + Size//2), int(-surfY + y + Size//2)]  # Точка вращения пистолета
offsetGun = pygame.math.Vector2(7, -3)             # Смещение пистолета относительно игрока
# ===== ЗАГРУЗКА ПУЛЬ =====
# Текстура пуль (обычные)
with open('textures/Bullets.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    BULLETS = ast.literal_eval(text1)               # Преобразуем в список координат

# Текстура пуль (максимальные)
with open('textures/BulletsMAX.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    BULLETSMAX = ast.literal_eval(text1)            # Преобразуем в список координат

# Текстура пуль (общая)
with open('textures/BulletTexture.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    BulletTexture = ast.literal_eval(text1)         # Преобразуем в список координат
# ===== ЗАГРУЗКА ВРАГОВ =====
# Текстура врага в состоянии покоя
with open('textures/enemyFlyStan.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    ENEMYSTAN1 = ast.literal_eval(text1)            # Преобразуем в список координат

# Текстура смерти врага
with open('textures/dieEnemyFly.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    ENEMYDIE1 = ast.literal_eval(text1)             # Преобразуем в список координат

# Текстура врага в движении
with open('textures/enemyFly.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    ENEMY1 = ast.literal_eval(text1)                # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    enemyFlySec = ast.literal_eval(text2)           # Преобразуем в список длительностей

# ===== ПАРАМЕТРЫ ВРАГОВ =====
enemyFly = ENEMY1[0]                                # Первый кадр анимации врага
lengthSmell = HEIGHT//2 + 50                        # Дальность обоняния врага (по вертикали)
lengthFallSmell = WIDTH//2 + 50                     # Дальность обоняния врага (по горизонтали)
speedEnemy = 3.5                                    # Скорость движения врага
hpEnemyFly = 100                                    # Здоровье врага
# ===== ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ ВРАГОВ =====
timerStan = 3 * FPS                                 # Время в состоянии покоя врага
helpEnemy = 0                                       # Счетчик помощи врагу
damage = 15                                         # Урон от врага

# ===== ЗАГРУЗКА ФИНИША =====
# Текстура финишной точки
with open('textures/Finish.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    FINISH = ast.literal_eval(text1)                # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    finishSec = ast.literal_eval(text2)             # Преобразуем в список длительностей

# ===== ИНИЦИАЛИЗАЦИЯ ТЕКСТУР =====
finishTex = FINISH[0]                               # Первый кадр анимации финиша
finishTimeCadr = 0                                  # Счетчик кадров анимации финиша

# Текущие текстуры отката
RollTex = RollBackTexture[cadrRoll]                # Текущая текстура отката (версия 1)
RollTex2 = RollBackTexture2[cadrRoll]              # Текущая текстура отката (версия 2)

# Утилита поворота произвольной поверхности вокруг опорной точки
def rotate1(surface, angle, pivot, offset):
    """Возвращает повернутую поверхность и прямоугольник с учетом смещённого pivot.

    surface: pygame.Surface — исходная поверхность
    angle: float — угол в градусах (по часовой стрелке)
    pivot: (x, y) — точка вращения в экранных координатах
    offset: pygame.Vector2 — вектор смещения от pivot до центра поверхности
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

# ===== ЗАГРУЗКА АНИМАЦИЙ СПАВНА =====
# Счетчики анимации спавна
timeCadrSpawn = 0                                   # Счетчик времени анимации спавна (версия 1)
timeCadrSpawn2 = 0                                  # Счетчик времени анимации спавна (версия 2)
cadrSpawn = 0                                       # Текущий кадр анимации спавна (версия 1)
cadrSpawn2 = 0                                      # Текущий кадр анимации спавна (версия 2)

# Анимация спавна (первая версия)
with open('textures/SpawnAnime.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    SpawnTexture = ast.literal_eval(text1)          # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    SpawnSec = ast.literal_eval(text2)              # Преобразуем в список длительностей

# Анимация спавна (вторая версия)
with open('textures/SpawnAnime2.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    SpawnTexture2 = ast.literal_eval(text1)         # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    SpawnSec2 = ast.literal_eval(text2)             # Преобразуем в список длительностей

# Текущие текстуры спавна
SpawnTex = SpawnTexture[cadrSpawn]                  # Текущая текстура спавна (версия 1)
SpawnTex2 = SpawnTexture2[cadrSpawn]                # Текущая текстура спавна (версия 2)

# ===== ЗАГРУЗКА АНИМАЦИИ ШИПОВ =====
# Счетчики анимации шипов
timeCadrSpikes = 0                                  # Счетчик времени анимации шипов
cadrSpikes = 0                                      # Текущий кадр анимации шипов

# Текстура шипов
with open('textures/Spikes.txt', 'r') as file:
    text1 = file.readline()                         # Читаем координаты пикселей
    SpikesTexture = ast.literal_eval(text1)         # Преобразуем в список координат
    text2 = file.readline()                         # Читаем длительности кадров
    SpikesSec = ast.literal_eval(text2)             # Преобразуем в список длительностей

# Текущая текстура шипов (временно использует текстуру отката)
SpikesTex = RollBackTexture[cadrRoll]

# ===== ИНИЦИАЛИЗАЦИЯ АНИМАЦИИ ИГРОКА =====
timeCadr = 0                                        # Счетчик времени анимации игрока
cadr = 0                                            # Текущий кадр анимации игрока

# Текущее состояние анимации игрока (GG) — выбирается из соответствующих наборов GG*
GG = GGStop[cadr]                                   # Текущая анимация игрока (по умолчанию - остановка)

# ===== НАПРАВЛЕНИЯ И СОСТОЯНИЯ ИГРОКА =====
GGRIGHT = True                                      # Игрок смотрит вправо
DROP = False                                        # Игрок не падает
drawX = 0                                           # Координата X для отрисовки
drawY = 0                                           # Координата Y для отрисовки
anime = 0                                           # Флаг анимации
rotate = "none"                                     # Направление поворота
FlagWall = False                                    # Флаг стены
SpringAllY = 0                                      # Общая сила пружины по Y

# ===== АНИМАЦИЯ В МЕНЮ =====
timeCadrMenu = 0                                    # Счетчик времени анимации в меню
cadrMenu = 0                                        # Текущий кадр анимации в меню
GGMenu = GGStop[cadr]                               # Анимация игрока в меню


def list_deepcopy(l):
    """Небольшой deep-copy для вложенных списков без импортов copy.deepcopy.

    Используется для копирования структур уровня, содержащих вложенные массивы.
    """
    return [
        elem if not isinstance(elem, list) else list_deepcopy(elem)
        for elem in l
    ]
def napravl(NDash, x, y, speedG, speed):
    """Применяет смещение от рывка (dash) по направлению `NDash`.

    Возвращает обновлённые x, y, а также побочные эффекты на speedG/speed.
    """
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

# ===== ПЕРЕМЕННЫЕ ИГРОВОГО ЦИКЛА =====
scroll = 0                                           # Счетчик прокрутки
victoryTime = 2 * FPS                                # Время показа экрана победы (2 секунды)
win = False                                          # Флаг победы
clock = pygame.time.Clock()                          # Таймер для ограничения FPS
# ===== ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ =====
# Структура кадра:
# 1) В зависимости от состояния (menu/settings/maps/game) обрабатываем события
# 2) Обновляем логику (физика, таймеры, ИИ, столкновения)
# 3) Рендерим: фон → объекты → UI
while True:
    # ===== СОСТОЯНИЕ: ГЛАВНОЕ МЕНЮ =====
    if menu == "menu":
        # Обновляем кнопки меню если карта загружена
        if buttonMenu[0] == "Играть" and letMap != "none":
            buttonMenu = ["Играть", "Карты", "Редактировать", "Создать", "Настройки", "Выйти"]
        
        # Отрисовка параллакс-фона в меню
        draw_parallax_background(screen, 0, 0)
        
        # ===== АНИМАЦИЯ ИГРОКА В МЕНЮ =====
        timeCadrMenu += 1                            # Увеличиваем счетчик времени
        if timeCadrMenu >= FPS * GGStopSec // len(GGStop):  # Проверяем, нужно ли сменить кадр
            if cadrMenu + 1 < len(GGStop):           # Если есть следующий кадр
                cadrMenu += 1                        # Переходим к следующему кадру
            else:
                cadrMenu = 0                         # Возвращаемся к первому кадру
            timeCadrMenu = 0                         # Сбрасываем счетчик времени
        
        # Дополнительная проверка границ анимации
        if cadrMenu + 1 >= len(GGStop):
            cadrMenu = 0
        
        # Получаем текущий кадр анимации для меню
        GGMenu = GGStop[cadrMenu]
        
        # ===== ОТРИСОВКА ИГРОКА В МЕНЮ =====
        for j in range(len(GGMenu[0])):              # Проходим по всем пикселям анимации
            # Вычисляем позицию для отрисовки (центрируем на экране)
            drawX = WIDTH // 2 - Size * 10 // 2 + GGMenu[0][j] * 10
            drawY = HEIGHT // 2 - Size * 10 // 2 + GGMenu[1][j] * 10
            
            # Получаем цвет пикселя
            lol = GGMenu[2][j]
            
            # Корректируем цвета для лучшего отображения в меню
            if GGMenu[2][j] == (0, 190, 0):          # Светло-зеленый
                lol = (50, 120, 80)                  # Делаем более темным
            elif GGMenu[2][j] == (0, 95, 0):         # Темно-зеленый
                lol = (10, 45, 20)                   # Делаем еще темнее
            
            # Отрисовываем пиксель как прямоугольник
            pygame.draw.rect(screen, lol, (drawX, drawY, 30, 30))
        # ===== ОБРАБОТКА СОБЫТИЙ В МЕНЮ =====
        for i in pygame.event.get():
            # Обработка закрытия окна
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Обработка нажатий клавиш
            if i.type == pygame.KEYDOWN:
                # Горячие клавиши меню
                if i.key == pygame.K_ESCAPE:         # Клавиша ESC
                    if buttonMenu[0] == "Продолжить": # Если есть сохраненная игра
                        menu = "game"                # Переходим в игру
                        pygame.mixer.music.set_volume(0.06)  # Уменьшаем громкость музыки
                        clickSound.play()            # Воспроизводим звук клика
                    else:
                        pygame.quit()                # Выходим из игры
                        sys.exit()
                
                # Переключение полноэкранного режима
                if i.key == pygame.K_F11:
                    set_display_mode(not fullScreen) # Переключаем режим экрана
            
            # Обработка движения мыши
            if i.type == pygame.MOUSEMOTION:
                mouseX = i.pos[0] * k_posX           # Обновляем позицию мыши X с учетом масштабирования
                mouseY = i.pos[1] * k_posY           # Обновляем позицию мыши Y с учетом масштабирования
            
            # Обработка кликов мыши
            if i.type == pygame.MOUSEBUTTONUP:
                if i.button == 1:                    # Левая кнопка мыши
                    # Проверяем клик по каждой кнопке меню
                    for j in range(len(buttonMenu)):
                        text = menuFont.render(buttonMenu[j], 1, WHITE)  # Рендерим текст кнопки
                        
                        # Проверяем, находится ли курсор в пределах кнопки
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
                                pygame.mixer.music.set_volume(0.06)
                                start_level_timer(letMap.split(".")[0])
                                break
                            elif buttonMenu[j] == "Продолжить":
                                menu = "game"
                                pygame.mixer.music.set_volume(0.06)
                                pause_off()
                                break
                            elif buttonMenu[j] == "Карты" or buttonMenu[j] == "Список карт":
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
                                        map["enemyFly"][1][ret] = map["enemyFly"][7][1][ret]  # Возвращаем Y позицию врага на исходную
                                        map["enemyFly"][7][2][ret] = 0                        # Сбрасываем угол движения врага
                                        map["enemyFly"][7][3][ret] = 0                        # Сбрасываем скорость движения врага
                                        map["enemyFly"][8][ret] = 0                           # Сбрасываем таймер оглушения врага
                                        map["enemyFly"][9][ret] = hpEnemyFly                  # Восстанавливаем здоровье врага
                                # ===== СБРОС ПУЛЬ НА ИСХОДНЫЕ ПОЗИЦИИ =====
                                if "bullets" in map:                                   # Если на карте есть пули
                                    for ret in range(len(map["bullets"][0])):          # Перебираем все пули
                                        map["bullets"][0][ret] = map["bullets"][4][ret]  # Возвращаем X позицию пули на исходную
                                        map["bullets"][1][ret] = map["bullets"][5][ret]  # Возвращаем Y позицию пули на исходную
                                # ===== СОХРАНЕНИЕ КАРТЫ В ФАЙЛ =====
                                lol = os.path.dirname(os.path.abspath(__file__))        # Получаем путь к папке игры
                                directory = lol + "/maps"                               # Путь к папке с картами
                                files = os.listdir(directory)                          # Получаем список всех файлов карт
                                my_file = open(directory+"/map"+str(len(files)+1)+".txt", "w+")  # Создаем новый файл карты
                                my_file.write(str(map)+"\n"+str(spawnX)+"\n"+str(spawnY)+"\n"+str(spawnSX)+"\n"+str(spawnSY))  # Записываем данные карты
                                break
                            elif buttonMenu[j] == "Настройки":                       # Кнопка "Настройки"
                                menu = "settings"                                    # Переходим в меню настроек
                                buttonMenu = ["Управление", "Звук", "Сбросить настройки", "Назад"]  # Обновляем список кнопок
                                break
                            elif buttonMenu[j] == "Редактировать":                    # Кнопка "Редактировать"
                                victoryTime = 2 * FPS                                # Устанавливаем время победы
                                pygame.mixer.music.set_volume(0.06)                  # Устанавливаем громкость музыки
                                menu = "game"                                        # Переходим в игровой режим
                                canCreate = True                                     # Разрешаем создание объектов
                                gameMode = "surv"                                    # Устанавливаем режим выживания
                                createType = "block"                                 # Устанавливаем тип создаваемого объекта
                                correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [],
                                                 "background": [], "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}  # Инициализируем словарь для корректировки объектов
                                break
                            elif buttonMenu[j] == "Создать":                          # Кнопка "Создать"
                                victoryTime = 2 * FPS                                # Устанавливаем время победы
                                pygame.mixer.music.set_volume(0.06)                  # Устанавливаем громкость музыки
                                menu = "game"                                        # Переходим в игровой режим
                                gameMode = "surv"                                    # Устанавливаем режим выживания
                                canCreate = True                                     # Разрешаем создание объектов
                                # ===== СБРОС ПОЗИЦИИ ИГРОКА =====
                                x = spawnX                                           # Устанавливаем X позицию игрока
                                y = spawnY                                           # Устанавливаем Y позицию игрока
                                xO = x                                               # Обновляем предыдущую X позицию
                                yO = y                                               # Обновляем предыдущую Y позицию
                                surfX = spawnSX                                      # Устанавливаем позицию камеры по X
                                surfY = spawnSY                                      # Устанавливаем позицию камеры по Y
                                # ===== СБРОС ДВИЖЕНИЯ ИГРОКА =====
                                motionL = 'stop'                                     # Останавливаем движение влево
                                motionR = 'stop'                                     # Останавливаем движение вправо
                                motionU = 'stop'                                     # Останавливаем движение вверх
                                motionD = 'stop'                                     # Останавливаем движение вниз
                                dash = 'stop'                                        # Останавливаем рывок
                                jump = 'stop'                                        # Останавливаем прыжок
                                jumpWallL = "stop"                                   # Останавливаем прыжок от стены влево
                                jumpWallR = "stop"                                   # Останавливаем прыжок от стены вправо
                                speed = 0                                            # Сбрасываем скорость
                                speedG = 0                                           # Сбрасываем скорость по Y
                                timeDash = 0                                         # Сбрасываем таймер рывка
                                canJump = False                                      # Запрещаем прыжок
                                canJumpWallR = False                                 # Запрещаем прыжок от стены вправо
                                canJumpWallL = False                                 # Запрещаем прыжок от стены влево
                                canDash = False                                      # Запрещаем рывок
                                # ===== СОЗДАНИЕ ПУСТОЙ КАРТЫ =====
                                map = {"block": [[], [], [], []], "spikes": [[], [], [], []], "spring": [[], [], [], []],
                                      "rollback": [[], [], 8, 8, []], "background": [[], [], [], [], []],
                                      "spawnpoint": [[], [], 21, 21, -1], "bullets": [[], [], 15, 15, [], []],
                                       "enemyFly": [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []], "finish": [[], [], 24, 24]}  # Создаем пустую карту со всеми типами объектов
                                correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [],
                                                 "background": [], "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}  # Инициализируем словарь для корректировки объектов
                                letMap = "none"                                       # Устанавливаем название карты как "none"
                                createType = "block"                                  # Устанавливаем тип создаваемого объекта как блок
                                break
                            elif buttonMenu[j] == "Покинуть уровень" or  buttonMenu[j] == "Поплакать" or buttonMenu[j] == "Выход в главное меню":  # Кнопки выхода из уровня
                                victoryTime = 2 * FPS                                # Устанавливаем время победы
                                menu = "menu"                                        # Возвращаемся в главное меню
                                buttonMenu = ["Играть", "Карты", "Создать", "Настройки", "Выйти"]  # Обновляем список кнопок
                                canCreate = True                                     # Разрешаем создание объектов
                                # ===== ВОЗВРАТ К ИСХОДНЫМ ПОЗИЦИЯМ =====
                                spawnX = TrueX                                       # Возвращаем исходную X позицию спавна
                                spawnY = TrueY                                       # Возвращаем исходную Y позицию спавна
                                x = spawnX                                           # Устанавливаем X позицию игрока
                                y = spawnY                                           # Устанавливаем Y позицию игрока
                                xO = x                                               # Обновляем предыдущую X позицию
                                yO = y                                               # Обновляем предыдущую Y позицию
                                surfX = 0                                            # Сбрасываем позицию камеры по X
                                surfY = 0                                            # Сбрасываем позицию камеры по Y
                                spawnSX = surfX                                      # Обновляем позицию спавна камеры по X
                                spawnSY = surfY                                      # Обновляем позицию спавна камеры по Y
                                # ===== СБРОС ДВИЖЕНИЯ ИГРОКА =====
                                motionL = 'stop'                                      # Останавливаем движение влево
                                motionR = 'stop'                                      # Останавливаем движение вправо
                                motionU = 'stop'                                      # Останавливаем движение вверх
                                motionD = 'stop'                                      # Останавливаем движение вниз
                                dash = 'stop'                                         # Останавливаем рывок
                                jump = 'stop'                                         # Останавливаем прыжок
                                jumpWallL = "stop"                                    # Останавливаем прыжок от стены влево
                                jumpWallR = "stop"                                    # Останавливаем прыжок от стены вправо
                                # ===== СБРОС ФИЗИЧЕСКИХ ПАРАМЕТРОВ =====
                                speed = 0                                             # Сбрасываем скорость
                                maxSpeed = 4                                          # Устанавливаем максимальную скорость
                                speedG = 0                                            # Сбрасываем скорость по Y
                                timeDash = 0                                          # Сбрасываем таймер рывка
                                # ===== СБРОС СПОСОБНОСТЕЙ =====
                                canJump = False                                       # Запрещаем прыжок
                                canJumpWallR = False                                  # Запрещаем прыжок от стены вправо
                                canJumpWallL = False                                  # Запрещаем прыжок от стены влево
                                canDash = False                                       # Запрещаем рывок
                                canShoot = True                                       # Разрешаем стрельбу
                                timeShoot = 0                                         # Сбрасываем таймер стрельбы
                                bullets = 0                                           # Сбрасываем количество пуль
                                bulletsCadr = bullets * 2                             # Обновляем кадр пуль
                                # ===== СБРОС ИГРОВЫХ ПАРАМЕТРОВ =====
                                bulletTime = 0                                       # Сбрасываем таймер пуль
                                colorBullets = colorBullets2                         # Устанавливаем цвет пуль по умолчанию
                                
                                # ===== СОЗДАНИЕ ПУСТОЙ КАРТЫ =====
                                # Инициализируем пустую карту со всеми типами объектов
                                map = {"block": [[], [], [], []], "spikes": [[], [], [], []], "spring": [[], [], [], []],
                                      "rollback": [[], [], 8, 8, []], "background": [[], [], [], [], []],
                                      "spawnpoint": [[], [], 21, 21, -1], "bullets": [[], [], 15, 15, [], []],
                                       "enemyFly": [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []], "finish": [[], [], 24, 24]}  # Создаем пустую карту со всеми типами объектов
                                
                                # ===== СБРОС КОРРЕКТИРОВКИ ОБЪЕКТОВ =====
                                correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [],
                                                 "background": [], "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}  # Инициализируем словарь для корректировки объектов
                                
                                # ===== СБРОС НАСТРОЕК РЕДАКТОРА =====
                                letMap = "none"                                      # Сбрасываем текущую карту
                                createType = "block"                                 # Устанавливаем тип создания по умолчанию
                                letMap = "none"                                      # Дублируем сброс карты
                                break
                            elif buttonMenu[j] == "Выйти":                           # Кнопка "Выйти"
                                pygame.quit()                                        # Завершаем работу pygame
                                sys.exit()
        # ===== ОТРИСОВКА ЗАГОЛОВКА МЕНЮ =====
        textMENU = fontMENU.render('МЕНЮ', 1, GREEN_d)                              # Рендерим заголовок "МЕНЮ"
        screen.blit(textMENU, (WIDTH//2-textMENU.get_width()//2, HEIGHT//4))        # Отображаем заголовок по центру экрана
        # ===== ОТРИСОВКА РЕЗУЛЬТАТОВ УРОВНЯ =====
        if buttonMenu[0] == "Поплакать" or buttonMenu[0] == "Покинуть уровень" or buttonMenu[0] == "Выход в главное меню":  # Если это экран завершения уровня
            if win[0]:                                                                 # Если установлен новый рекорд
                colorWin = (0, 255, 0)                                                # Зеленый цвет для рекорда
                textWinGame = "НОВЫЙ РЕКОРД:"                                         # Текст нового рекорда
                best_time = settings["statistics"]["level_times"][letMap.split(".")[0]]  # Получаем лучшее время
                textWinGame += f" | Время: {format_time(best_time)}"                   # Добавляем время к тексту
            else:                                                                      # Если рекорд не установлен
                colorWin = (255, 0, 0)                                                # Красный цвет для обычного результата
                textWinGame = ""                                                       # Пустой текст
                textWinGame += f"Время: {format_time(win[1])}"                         # Добавляем время прохождения
            textWin = menuFont.render(textWinGame, 1, colorWin)                       # Рендерим текст результата
            screen.blit(textWin, (WIDTH // 2 - textWin.get_width() // 2, HEIGHT // 4 - 50))  # Отображаем результат
        # ===== ОТРИСОВКА КНОПОК МЕНЮ =====
        for i in range(len(buttonMenu)):                                             # Перебираем все кнопки меню
            colorButton = WHITE                                                       # Устанавливаем белый цвет по умолчанию
            text = menuFont.render(buttonMenu[i], 1, colorButton)                    # Рендерим текст кнопки
            # ===== ПРОВЕРКА НАВЕДЕНИЯ МЫШИ НА КНОПКУ =====
            if mouseX > WIDTH // 2 - text.get_width() // 2 \
                    and mouseX < WIDTH // 2 - text.get_width() // 2 + text.get_width() \
                    and mouseY > HEIGHT // 2 - 50 + i * (text.get_height() + 5) +5 \
                    and mouseY < HEIGHT // 2 - 50 + i * (text.get_height() + 5) + text.get_height() -5:
                if lastMenuButton != buttonMenu[i]:                                   # Если наведена на новую кнопку
                    scrollSound.play()                                               # Воспроизводим звук прокрутки
                    lastMenuButton = buttonMenu[i]                                   # Запоминаем текущую кнопку
                colorButton = (255, 0, 0)                                            # Устанавливаем красный цвет для подсветки
            text = menuFont.render(buttonMenu[i], 1, colorButton)                    # Рендерим текст кнопки с новым цветом
            screen.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-50+i*(text.get_height()+5)))  # Отображаем кнопку
            # ===== ОТРИСОВКА ДОПОЛНИТЕЛЬНОЙ ИНФОРМАЦИИ ДЛЯ КНОПОК =====
            if buttonMenu[i] == "Играть" and colorButton == (255, 0, 0):              # Если наведена на кнопку "Играть"
                textMap = menuFont.render(">"+letMap.split(".")[0], 1, (200, 200, 10))  # Показываем название карты
                screen.blit(textMap, (WIDTH // 2 + text.get_width() // 2+5, HEIGHT // 2 - 50 + i * (text.get_height() + 5)))  # Отображаем справа от кнопки
            if buttonMenu[i] == "Редактировать" and colorButton == (255, 0, 0):        # Если наведена на кнопку "Редактировать"
                textMap = menuFont.render(">" + letMap.split(".")[0], 1, (200, 200, 10))  # Показываем название карты
                screen.blit(textMap,
                            (WIDTH // 2 + text.get_width() // 2 + 5, HEIGHT // 2 - 50 + i * (text.get_height() + 5)))  # Отображаем справа от кнопки
            if buttonMenu[i] == "Сохранить" and colorButton == (255, 0, 0):            # Если наведена на кнопку "Сохранить"
                lol = os.path.dirname(os.path.abspath(__file__))                        # Получаем путь к папке игры
                directory = lol + "/maps"                                               # Путь к папке с картами
                files = os.listdir(directory)                                          # Получаем список файлов карт
                textMap = menuFont.render(">map" + str(len(files)+1), 1, (200, 200, 10))  # Показываем номер новой карты
                screen.blit(textMap,
                            (WIDTH // 2 + text.get_width() // 2 + 5, HEIGHT // 2 - 50 + i * (text.get_height() + 5)))  # Отображаем справа от кнопки
    # ===== СОСТОЯНИЕ: НАСТРОЙКИ =====
    elif menu == "settings":                                                         # Если активен режим настроек
        draw_parallax_background(screen, 0, 0)                                       # Отрисовываем параллакс-фон
        # ===== АНИМАЦИЯ ИГРОКА В НАСТРОЙКАХ =====
        timeCadrMenu += 1                                                            # Увеличиваем счетчик времени
        if timeCadrMenu >= FPS * SpawnSec2 // len(SpawnTexture2):                    # Проверяем, нужно ли сменить кадр
            if cadrMenu + 1 < len(SpawnTexture2):                                    # Если есть следующий кадр
                cadrMenu += 1                                                        # Переходим к следующему кадру
            else:
                cadrMenu = 0                                                         # Возвращаемся к первому кадру
            timeCadrMenu = 0                                                         # Сбрасываем счетчик времени
        if cadrMenu + 1 >= len(SpawnTexture2):                                       # Дополнительная проверка границ
            cadrMenu = 0                                                             # Сбрасываем кадр если вышли за границы
        GGMenu = SpawnTexture2[cadrMenu]                                            # Получаем текущий кадр анимации
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
                        buttonMenu = ["Управление", "Звук", "Сбросить настройки", "Назад"]
                    clickSound.play()
                if i.key == pygame.K_F11:
                    set_display_mode(not fullScreen)
                ## Славина настройка
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
                        # мгновенно обновляем список управления, если он открыт
                        if buttonMenu and (buttonMenu[0].startswith("UP:") or buttonMenu[0].startswith("Вверх:")):
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
                ## Славина настройка музыки
                if dragging_slider:
                    slider_x = WIDTH // 2 - 100
                    slider_width = 200
                    if mouseX >= slider_x and mouseX <= slider_x + slider_width:
                        click_pos = mouseX - slider_x
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
                        if i.pos[0] * k_posX > WIDTH//2-text.get_width()//2 \
                                and i.pos[0] * k_posX < WIDTH//2-text.get_width()//2+text.get_width() \
                                and i.pos[1] * k_posY > HEIGHT//2-50+j*item_height+5 \
                                and i.pos[1] * k_posY < HEIGHT // 2 - 50 + j * item_height + text.get_height()-5:
                            if not((buttonMenu[j].split(":")[0] == "Музыка") or (buttonMenu[j].split(":")[0] == "Звуки")):
                                clickSound.play()
                            if buttonMenu[j] == "Назад":
                                if buttonMenu[0] == "Управление":
                                    menu = "menu"
                                    buttonMenu = ["Играть", "Карты", "Создать", "Настройки", "Выйти"]
                                else:
                                    buttonMenu = ["Управление", "Звук", "Сбросить настройки", "Назад"]
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
                            elif buttonMenu[j] == "Звук":
                                buttonMenu = [
                                    f"Музыка: {settings['sound']['music_volume']}%",
                                    f"Звуки: {settings['sound']['sfx_volume']}%",
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
                                settings["sound"] = {
                                    "music_volume": 15,
                                    "sfx_volume": 100
                                }
                                init_keys()
                                update_sound_volumes()
                                save_settings(settings)
                                buttonMenu = ["Управление", "Звук", "Сбросить настройки", "Назад"]
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
                        if buttonMenu and buttonMenu[0].startswith("UP:"):
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
                        scrollSound.play()
                        lastMenuButton = buttonMenu[i]
                if not((buttonMenu[i].split(":")[0] == "Музыка") or (buttonMenu[i].split(":")[0] == "Звуки")):
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
            if buttonMenu[i] == "Играть" and colorButton == (255, 0, 0):
                textMap = menuFont.render(">"+letMap, 1, (200, 200, 10))
                screen.blit(textMap, (WIDTH // 2 + text.get_width() // 2+5, HEIGHT // 2 - 50 + i * (text.get_height() + 5)))
    # ===== СОСТОЯНИЕ: СПИСОК КАРТ =====
    elif menu == "maps":
        draw_parallax_background(screen, 0, 0)
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
                    menu = "menu"
                    scroll = 0
                    clickSound.play()
                if i.key == pygame.K_F11:
                    set_display_mode(not fullScreen)
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
                            with open('maps/'+files[j+scroll], 'r') as file:
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
            #
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
    # ===== СОСТОЯНИЕ: ИГРА =====
    elif menu == "game":
        '''if gameMode == "surv":
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)'''
        # Параллакс фон завязан на смещение камеры: используем surfX/surfY
        draw_parallax_background(screen, surfX, surfY)
        grav = 1
        stopRun = 0
        # Обработка событий ввода (клавиатура/мышь)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
            # нажатие
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE and victoryTime == 2 * FPS:
                    #pygame.mouse.set_visible(True)
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(0.15)
                    if canCreate == False:
                        pause_on()
                        buttonMenu = ["Продолжить", "Покинуть уровень"]
                    else:
                        buttonMenu = ["Продолжить", "Сохранить", "Покинуть уровень"]
                    menu = "menu"
                if i.key == pygame.K_F11:
                    set_display_mode(not fullScreen)
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
                #специфические
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
                            pygame.mixer.music.pause()
                        else:
                            gameMode = "surv"
                            pygame.mixer.music.unpause()
                if gameMode == "creat":
                    if i.key == pygame.K_DELETE:
                        for j in range(len(map["enemyFly"]) + 3):
                            if j < 4:
                                lol = 0
                                for n in range(len(correctObject["block"])):
                                    map["block"][j].pop(correctObject["block"][n+lol])
                                    lol -= 1
                                lol = 0
                                for n in range(len(correctObject["spikes"])):
                                    map["spikes"][j].pop(correctObject["spikes"][n+lol])
                                    lol -= 1
                                lol = 0
                                for n in range(len(correctObject["spring"])):
                                    map["spring"][j].pop(correctObject["spring"][n+lol])
                                    lol -= 1
                            if j < 5:
                                lol = 0
                                for n in range(len(correctObject["background"])):
                                    map["background"][j].pop(correctObject["background"][n+lol])
                                    lol -= 1
                                try:
                                    lol = 0
                                    for n in range(len(correctObject["rollback"])):
                                        map["rollback"][j].pop(correctObject["rollback"][n+lol])
                                        lol -= 1
                                except:
                                    pass
                                try:
                                    lol = 0
                                    for n in range(len(correctObject["spawnpoint"])):
                                        map["spawnpoint"][j].pop(correctObject["spawnpoint"][n+lol])
                                        lol -= 1
                                except:
                                    pass
                                try:
                                    lol = 0
                                    for n in range(len(correctObject["finish"])):
                                        map["finish"][j].pop(correctObject["finish"][n+lol])
                                        lol -= 1
                                except:
                                    pass
                            try:
                                lol = 0
                                for n in range(len(correctObject["bullets"])):
                                    map["bullets"][j].pop(correctObject["bullets"][n+lol])
                                    lol -= 1
                            except:
                                pass
                            try:
                                lol = 0
                                for n in range(len(correctObject["enemyFly"])):
                                    if j >= 7 and j <= 10:
                                        map["enemyFly"][7][j-7].pop(correctObject["enemyFly"][n + lol])
                                    else:
                                        map["enemyFly"][j].pop(correctObject["enemyFly"][n+lol])
                                    lol -= 1
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
            # отпускание
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
            # мышь
            if i.type == pygame.MOUSEBUTTONDOWN:
                if isinstance(DASH, str) and len(DASH.split("_")) > 1:
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
                if isinstance(SHOOT, str) and len(SHOOT.split("_")) > 1:
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
                if i.button == 1:
                    if gameMode == "creat":
                        if createType != "rollback" and createType != "spawnpoint" and createType != "bullets" and createType != "enemyFly" and createType != "finish":
                            map[createType][0].append(int(i.pos[0] * k_posX+surfX) - int(i.pos[0] * k_posX+surfX) % 10)
                            map[createType][1].append(int(i.pos[1] * k_posY+surfY) - int(i.pos[1] * k_posY+surfY) % 10)
                        draw = 1
                elif i.button == 3:
                    if gameMode == "creat":
                        firstMouseX = i.pos[0] * k_posX
                        firstMouseY = i.pos[1] * k_posY
                        draw = 2
            if i.type == pygame.MOUSEMOTION:
                if gameMode == "creat":
                    if createType != "rollback" and createType != "spawnpoint" and createType != "bullets" and createType != "enemyFly" and createType != "finish":
                        mouseX = i.pos[0] * k_posX + 10 - int(i.pos[0] * k_posX+surfX) % 10
                        mouseY = i.pos[1] * k_posY + 10 - int(i.pos[1] * k_posY+surfY) % 10
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
                            except:
                                map["bullets"] = [[], [], 15, 15, [], []]
                                map["enemyFly"] = [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []]
                                map["finish"] = [[], [], 24, 24]
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
                            if createType == "rollback":
                                map[createType][4].append(0)
                        if createType == "background":
                            map[createType][4].append(createColor)
                        correctObject = {"block": [], "spikes": [], "spring": [], "rollback": [], "background": [],
                                         "spawnpoint": [], "bullets": [], "enemyFly": [], "finish": []}
                        
                        # ===== НАСТРОЙКА КОРРЕКТИРОВКИ ОБЪЕКТОВ =====
                        correctObject[createType] = [-1]                            # Устанавливаем корректировку для текущего типа объекта
                        draw = -1                                                   # Сбрасываем режим рисования
                        print("\nmap =", map)                                       # Выводим карту в консоль для отладки
                elif i.button == 3:
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
                        for j in range(len(map["spikes"][3])):
                            if map["spikes"][0][j]+map["spikes"][2][j]-surfX > firstMouseX \
                                    and map["spikes"][0][j]-surfX < mouseX \
                                    and map["spikes"][1][j]+map["spikes"][3][j]-surfY > firstMouseY \
                                    and map["spikes"][1][j]-surfY < mouseY:
                                correctObject["spikes"].append(j)
                        for j in range(len(map["spring"][3])):
                            if map["spring"][0][j]+map["spring"][2][j]-surfX > firstMouseX \
                                    and map["spring"][0][j]-surfX < mouseX \
                                    and map["spring"][1][j]+map["spring"][3][j]-surfY > firstMouseY \
                                    and map["spring"][1][j]-surfY < mouseY:
                                correctObject["spring"].append(j)
                        for j in range(len(map["background"][3])):
                            if map["background"][0][j]+map["background"][2][j]-surfX > firstMouseX \
                                    and map["background"][0][j]-surfX < mouseX \
                                    and map["background"][1][j]+map["background"][3][j]-surfY > firstMouseY \
                                    and map["background"][1][j]-surfY < mouseY:
                                correctObject["background"].append(j)
                        for j in range(len(map["rollback"][4])):
                            if map["rollback"][0][j]+map["rollback"][2]-surfX > firstMouseX \
                                    and map["rollback"][0][j]-surfX < mouseX \
                                    and map["rollback"][1][j]+map["rollback"][3]-surfY > firstMouseY \
                                    and map["rollback"][1][j]-surfY < mouseY:
                                correctObject["rollback"].append(j)
                        for j in range(len(map["spawnpoint"][1])):
                            if map["spawnpoint"][0][j]+map["spawnpoint"][2]-surfX > firstMouseX \
                                    and map["spawnpoint"][0][j]-surfX < mouseX \
                                    and map["spawnpoint"][1][j]+map["spawnpoint"][3]-surfY > firstMouseY \
                                    and map["spawnpoint"][1][j]-surfY < mouseY:
                                correctObject["spawnpoint"].append(j)
                        try:
                            for j in range(len(map["bullets"][1])):
                                if map["bullets"][0][j]+map["bullets"][2]-surfX > firstMouseX \
                                        and map["bullets"][0][j]-surfX < mouseX \
                                        and map["bullets"][1][j]+map["bullets"][3]-surfY > firstMouseY \
                                        and map["bullets"][1][j]-surfY < mouseY:
                                    correctObject["bullets"].append(j)
                        except:
                            map["bullets"] = [[], [], 15, 15, [], []]
                        try:
                            for j in range(len(map["enemyFly"][1])):
                                if map["enemyFly"][0][j]+map["enemyFly"][2]-surfX > firstMouseX \
                                        and map["enemyFly"][0][j]-surfX < mouseX \
                                        and map["enemyFly"][1][j]+map["enemyFly"][3]-surfY > firstMouseY \
                                        and map["enemyFly"][1][j]-surfY < mouseY:
                                    correctObject["enemyFly"].append(j)
                        except:
                            map["enemyFly"] = [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []]
                        try:
                            for j in range(len(map["finish"][1])):
                                if map["finish"][0][j] + map["finish"][2] - surfX > firstMouseX \
                                        and map["finish"][0][j] - surfX < mouseX \
                                        and map["finish"][1][j] + map["finish"][3] - surfY > firstMouseY \
                                        and map["finish"][1][j] - surfY < mouseY:
                                    correctObject["finish"].append(j)
                        except:
                            map["finish"] = [[], [], 24, 24]
                        draw = -1
        # действия
        for m in range(1):
            if gameMode == "surv" and victoryTime == 2 * FPS:
                #тормоз
                if motionL == "stop" and motionR == "stop":
                    if speed > 0:
                        speed -= maxSpeed / 4
                    if speed <= 0:
                        speed = 0
                    if xO < x:
                        x += speed
                    elif xO > x:
                        x -= speed
                #остальное
                if dash == "stop":
                    if jump == "motion":
                        if speedJ-speedG > 0:
                            y -= speedJ
                        else:
                            jump = "stop"
                            speedJ = J
                            spring = 0
                            speedG = 0
                    elif jumpWallL == "motion":
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
                            grav = 0
                            speedG = 0
                            x, y, speedG, speed = napravl(NDash, x, y, speedG, speed)
                        dash = "stop"
                        grav = 1
                        timeDash = 0

                # стрельба
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
            # пули летят
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
        # ===== ОБНОВЛЕНИЕ ЛОГИКИ: взаимодействие и гравитация =====
        for G in range(1):
            # победа
            if victoryTime < 2 * FPS:
                victoryTime -= 1
                if victoryTime == 0:
                    # После финиша показываем 2 кнопки: выход в главное меню и список карт
                    buttonMenu = ["Выход в главное меню", "Список карт"]
                    menu = "menu"
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(0.15)

            if gameMode == "surv" and victoryTime == 2 * FPS:
                # гравитация
                if grav == 1:
                    canJump = False
                    canJumpWallL = False
                    canJumpWallR = False
                    y += speedG
                    if speedG < speedJ:
                        speedG += g
                # взаимодействие с полом
                if y >= minY-Size:
                    y = minY-Size
                    grav = 0
                    speedG = 0
                    timeCoyoteL = 5
                    timeCoyoteR = 5
                    canJump = True
                    canDash = True
                    canJumpWallL = False
                    canJumpWallR = False
                    if y > minY - Size:
                        dash = "stop"
                        timeDash = 0
                # пуль с полом
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
                # врагов с полом
                try:
                    for enem in range(len(map["enemyFly"][1])):
                        if map["enemyFly"][9][enem] <= 0:
                            continue
                        if map["enemyFly"][1][enem] >= minY - map["enemyFly"][2]:
                            map["enemyFly"][1][enem] = minY - map["enemyFly"][2]
                except:
                    pass
                # блоки
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
                        # пули
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
                        # враги не могут пройти
                        try:
                            for enem in range(len(map["enemyFly"][1])):
                                if map["enemyFly"][9][enem] <= 0:
                                    continue
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
                                            map["enemyFly"][4][enem] = map["enemyFly"][0][enem]
                                            map["enemyFly"][5][enem] = map["enemyFly"][1][enem]
                        except:
                            pass
                        # игрок:::###
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
                            timeCoyoteL = 5
                            timeCoyoteR = 5
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
                        # прыжок от стены
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
                    # Враги ищут путь
                    try:
                        for enem in range(len(map["enemyFly"][1])):
                            if map["enemyFly"][9][enem] <= 0:
                                continue
                            lengthEnemyTrue = ((x - map["enemyFly"][0][enem]) ** 2 + (
                                    y - map["enemyFly"][1][enem]) ** 2) ** 0.5
                            try:
                                sin = (y - map["enemyFly"][1][enem]) / lengthEnemyTrue
                                cos = (x - map["enemyFly"][0][enem]) / lengthEnemyTrue
                            except:
                                sin = 0
                                cos = 0
                            if (lengthEnemyTrue <= lengthSmell) \
                                    or (lengthEnemyTrue <= lengthFallSmell and map["enemyFly"][8][enem] > 0):
                                FWallEnemy = True
                                for i in range(len(map["block"][0])):
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
                                            if (map["enemyFly"][0][enem] - x) * (map["enemyFly"][1][enem] - y) > 0:
                                                xFoundWall = map["enemyFly"][0][enem] + map["enemyFly"][2] * doble
                                                yFoundWall = map["enemyFly"][1][enem] + map["enemyFly"][3] * (1 - doble)
                                            else:
                                                xFoundWall = map["enemyFly"][0][enem] + map["enemyFly"][2] * doble
                                                yFoundWall = map["enemyFly"][1][enem] + map["enemyFly"][3] * doble
                                            for ii in range(0, int(lengthEnemyTrue // 5)):
                                                xFoundWall += 5 * cos
                                                yFoundWall += 5 * sin
                                                if yFoundWall > map["block"][1][i] \
                                                        and yFoundWall < map["block"][1][i] + map["block"][3][i] \
                                                        and xFoundWall > map["block"][0][i] \
                                                        and xFoundWall < map["block"][0][i] + map["block"][2][i]:
                                                    FWallEnemy = False
                                                    break
                                            if FWallEnemy == False:
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
                                    # ===== СБРОС СОСТОЯНИЯ ВРАГА =====
                                    if map["enemyFly"][6][enem]:                      # Если враг в состоянии оглушения
                                        map["enemyFly"][6][enem] = False              # Сбрасываем состояние оглушения
                            else:
                                # ===== СБРОС СОСТОЯНИЯ ВРАГА (АЛЬТЕРНАТИВНЫЙ ПУТЬ) =====
                                if map["enemyFly"][6][enem]:                          # Если враг в состоянии оглушения
                                    map["enemyFly"][6][enem] = False                  # Сбрасываем состояние оглушения
                    except:
                        pass                                                        # Игнорируем ошибки при обработке врагов
                # ===== ПРОВЕРКА ПОПАДАНИЯ ПУЛЬ ПО ВРАГАМ =====
                try:
                    for enem in range(len(map["enemyFly"][1])):                       # Перебираем всех летающих врагов
                        if map["enemyFly"][9][enem] <= 0:                            # Если враг мертв (здоровье <= 0)
                            continue                                                 # Пропускаем мертвого врага
                        # ===== ПРОВЕРКА КОЛЛИЗИИ ПУЛЬ С ВРАГОМ =====
                        bulFlex = []                                                  # Список пуль для удаления
                        for bul in range(len(flyBullets[0])):                        # Перебираем все летящие пули
                            sin = math.sin(math.radians(flyBullets[2][bul]))         # Синус угла полета пули
                            cos = math.cos(math.radians(flyBullets[2][bul]))         # Косинус угла полета пули
                            for hit in range(3):                                     # Проверяем 3 точки вдоль пули
                                hitLen = lengthBullets // 2 * hit                    # Длина от начала пули до точки проверки
                                # ===== ПРОВЕРКА ПЕРЕСЕЧЕНИЯ ПУЛИ С ВРАГОМ =====
                                if flyBullets[1][bul] - hitLen * sin >= map["enemyFly"][1][enem] \
                                        and flyBullets[1][bul] - hitLen * sin < map["enemyFly"][1][enem] + map["enemyFly"][3] \
                                        and flyBullets[0][bul] - hitLen * cos > map["enemyFly"][0][enem] \
                                        and flyBullets[0][bul] - hitLen * cos < map["enemyFly"][0][enem] + map["enemyFly"][2]:
                                    # ===== ОБРАБОТКА ПОПАДАНИЯ ПУЛИ ВО ВРАГА =====
                                    bulFlex.append(bul)                               # Добавляем пулю в список для удаления
                                    hitEnemSound.play()                              # Воспроизводим звук попадания
                                    # ===== РАСЧЕТ НОВОГО НАПРАВЛЕНИЯ ВРАГА =====
                                    map["enemyFly"][7][2][enem] = (flyBullets[2][bul] + map["enemyFly"][7][2][enem]) / 2  # Средний угол
                                    map["enemyFly"][7][3][enem] += speedBullets // 6  # Добавляем скорость от удара
                                    map["enemyFly"][6][enem] = True                   # Устанавливаем состояние оглушения
                                    map["enemyFly"][8][enem] = timerStan             # Устанавливаем таймер оглушения
                                    map["enemyFly"][4][enem] = x                     # Запоминаем позицию игрока
                                    map["enemyFly"][5][enem] = y                     # Запоминаем позицию игрока
                                    map["enemyFly"][9][enem] -= damage               # Уменьшаем здоровье врага
                                    if map["enemyFly"][9][enem] <= 0:                # Если враг умер
                                        dieEnemySound.play()                         # Воспроизводим звук смерти врага
                                    break                                            # Прерываем проверку точек пули
                        # ===== УДАЛЕНИЕ ПУЛЬ, ПОПАВШИХ ВО ВРАГА =====
                        bulFlex.sort(reverse=True)                                    # Сортируем индексы в обратном порядке для безопасного удаления
                        for bulFlexDel in bulFlex:                                   # Удаляем все пули, попавшие во врага
                            flyBullets[0].pop(bulFlexDel)                           # Удаляем X координату пули
                            flyBullets[1].pop(bulFlexDel)                           # Удаляем Y координату пули
                            flyBullets[2].pop(bulFlexDel)                           # Удаляем угол пули
                            flyBullets[3].pop(bulFlexDel)                           # Удаляем скорость пули
                        # ===== ПРИМЕНЕНИЕ ФИЗИКИ К ВРАГУ ПОСЛЕ ПОПАДАНИЯ =====
                        if map["enemyFly"][7][3][enem] > 0:                         # Если у врага есть скорость от удара
                            sin = math.sin(math.radians(map["enemyFly"][7][2][enem]))  # Синус угла движения врага
                            cos = math.cos(math.radians(map["enemyFly"][7][2][enem]))  # Косинус угла движения врага
                            map["enemyFly"][0][enem] += map["enemyFly"][7][3][enem] * cos  # Обновляем X позицию врага
                            map["enemyFly"][1][enem] += map["enemyFly"][7][3][enem] * sin  # Обновляем Y позицию врага
                            map["enemyFly"][7][3][enem] -= map["enemyFly"][7][3][enem] / 10  # Уменьшаем скорость (сопротивление воздуха)
                        else:
                            # ===== СБРОС ФИЗИКИ ВРАГА =====
                            map["enemyFly"][7][2][enem] = 0                         # Сбрасываем угол движения
                            map["enemyFly"][7][3][enem] = 0                         # Сбрасываем скорость движения
                except:
                    pass                                                        # Игнорируем ошибки при обработке врагов
                # ===== УПРАВЛЕНИЕ ЗВУКОМ БЕГА =====
                if FlagWall:                                                   # Если игрок касается стены
                    if playSoundSlide == 1:                                    # Если звук бега не воспроизводится
                        runSound.play(-1)                                      # Запускаем звук бега в цикле
                        playSoundSlide = 0                                     # Отмечаем, что звук запущен
                else:                                                          # Если игрок не касается стены
                    if playSoundSlide == 0:                                    # Если звук бега воспроизводится
                        runSound.stop()                                        # Останавливаем звук бега
                        playSoundSlide = 1                                     # Отмечаем, что звук остановлен
                # ===== ОБРАБОТКА ШИПОВ =====
                for i in range(len(map["spikes"][0])):                           # Перебираем все шипы на карте
                    # ===== ПРОВЕРКА КОЛЛИЗИИ ПУЛЬ С ШИПАМИ =====
                    bulFlex = []                                                  # Список пуль для удаления
                    for bul in range(len(flyBullets[0])):                        # Перебираем все летящие пули
                        sin = math.sin(math.radians(flyBullets[2][bul]))         # Синус угла полета пули
                        cos = math.cos(math.radians(flyBullets[2][bul]))         # Косинус угла полета пули
                        for hit in range(3):                                     # Проверяем 3 точки вдоль пули
                            hitLen = lengthBullets // 2 * hit                    # Длина от начала пули до точки проверки
                            # ===== ПРОВЕРКА ПЕРЕСЕЧЕНИЯ ПУЛИ С ШИПАМИ =====
                            if flyBullets[1][bul] - hitLen * sin >= map["spikes"][1][i] and flyBullets[1][
                                bul] - hitLen * sin < map["spikes"][1][i] + map["spikes"][3][i] \
                                    and flyBullets[0][bul] - hitLen * cos > map["spikes"][0][i] and flyBullets[0][
                                bul] - hitLen * cos < map["spikes"][0][i] + map["spikes"][2][i]:
                                bulFlex.append(bul)                              # Добавляем пулю в список для удаления
                                hitWallSound.play()                             # Воспроизводим звук попадания в стену
                                break                                            # Прерываем проверку точек пули
                    # ===== УДАЛЕНИЕ ПУЛЬ, ПОПАВШИХ В ШИПЫ =====
                    bulFlex.sort(reverse=True)                                    # Сортируем индексы в обратном порядке для безопасного удаления
                    for bulFlexDel in bulFlex:                                   # Удаляем все пули, попавшие в шипы
                        flyBullets[0].pop(bulFlexDel)                           # Удаляем X координату пули
                        flyBullets[1].pop(bulFlexDel)                           # Удаляем Y координату пули
                        flyBullets[2].pop(bulFlexDel)                           # Удаляем угол пули
                        flyBullets[3].pop(bulFlexDel)                           # Удаляем скорость пули
                    # ===== ПРОВЕРКА КОЛЛИЗИИ ИГРОКА С ШИПАМИ =====
                    if y + Size > map["spikes"][1][i]+5 and y < map["spikes"][1][i] + map["spikes"][3][i]-5 \
                    and x + Size > map["spikes"][0][i]+5 and x < map["spikes"][0][i] + map["spikes"][2][i]-5:
                        # ===== ОБРАБОТКА СМЕРТИ ИГРОКА ОТ ШИПОВ =====
                        if canCreate == False:                                    # Если не в режиме создания карты
                            add_death()                                           # Добавляем смерть в статистику
                        dieSound.play()                                          # Воспроизводим звук смерти
                        # ===== ВОЗВРАТ ИГРОКА НА ТОЧКУ СПАВНА =====
                        x = spawnX                                               # Возвращаем X позицию на спавн
                        y = spawnY                                               # Возвращаем Y позицию на спавн
                        xO = x                                                   # Обновляем предыдущую X позицию
                        yO = y                                                   # Обновляем предыдущую Y позицию
                        surfX = spawnSX                                          # Возвращаем камеру на спавн по X
                        surfY = spawnSY                                          # Возвращаем камеру на спавн по Y
                        # ===== СБРОС ВСЕХ ДВИЖЕНИЙ ИГРОКА =====
                        motionL = 'stop'                                         # Останавливаем движение влево
                        motionR = 'stop'                                         # Останавливаем движение вправо
                        motionU = 'stop'                                         # Останавливаем движение вверх
                        motionD = 'stop'                                         # Останавливаем движение вниз
                        dash = 'stop'                                            # Останавливаем рывок
                        jump = 'stop'                                            # Останавливаем прыжок
                        jumpWallL = "stop"                                       # Останавливаем прыжок от стены влево
                        jumpWallR = "stop"                                       # Останавливаем прыжок от стены вправо
                        speed = 0                                                # Сбрасываем скорость
                        speedG = 0                                               # Сбрасываем скорость по Y
                        timeDash = 0                                             # Сбрасываем таймер рывка
                        canJump = False                                          # Запрещаем прыжок
                        canJumpWallR = False                                     # Запрещаем прыжок от стены вправо
                        canJumpWallL = False                                     # Запрещаем прыжок от стены влево
                        canDash = False                                          # Запрещаем рывок
                        # ===== СБРОС ВСЕХ ОТКАТОВ РЫВКА =====
                        for j in range(len(map["rollback"][4])):                   # Перебираем все точки отката рывка
                            map["rollback"][4][j] = 0                             # Сбрасываем счетчик использования
                        # ===== СБРОС ВСЕХ ВРАГОВ НА ИСХОДНЫЕ ПОЗИЦИИ =====
                        if "enemyFly" in map:                                     # Если на карте есть летающие враги
                            for ret in range(len(map["enemyFly"][0])):            # Перебираем всех врагов
                                if map["enemyFly"][9][ret] > 0:                   # Если враг жив
                                    map["enemyFly"][-1][ret] = 0                  # Сбрасываем состояние врага
                                    map["enemyFly"][4][ret] = 0                  # Сбрасываем X позицию игрока для врага
                                    map["enemyFly"][5][ret] = 0                  # Сбрасываем Y позицию игрока для врага
                                    map["enemyFly"][6][ret] = False              # Сбрасываем состояние оглушения
                                    map["enemyFly"][0][ret] = map["enemyFly"][7][0][ret]  # Возвращаем на исходную X позицию
                                    map["enemyFly"][1][ret] = map["enemyFly"][7][1][ret]  # Возвращаем на исходную Y позицию
                                    map["enemyFly"][7][2][ret] = 0               # Сбрасываем угол движения
                                    map["enemyFly"][7][3][ret] = 0               # Сбрасываем скорость движения
                                    map["enemyFly"][8][ret] = 0                  # Сбрасываем таймер оглушения
                # ===== ОБРАБОТКА ПРУЖИН =====
                for i in range(len(map["spring"][0])):                             # Перебираем все пружины на карте
                    # ===== ПРОВЕРКА КОЛЛИЗИИ ПУЛЬ С ПРУЖИНАМИ =====
                    bulFlex = []                                                    # Список пуль для удаления
                    for bul in range(len(flyBullets[0])):                          # Перебираем все летящие пули
                        sin = math.sin(math.radians(flyBullets[2][bul]))           # Синус угла полета пули
                        cos = math.cos(math.radians(flyBullets[2][bul]))           # Косинус угла полета пули
                        for hit in range(3):                                       # Проверяем 3 точки вдоль пули
                            hitLen = lengthBullets // 2 * hit                      # Длина от начала пули до точки проверки
                            # ===== ПРОВЕРКА ПЕРЕСЕЧЕНИЯ ПУЛИ С ПРУЖИНОЙ =====
                            if flyBullets[1][bul] - hitLen * sin >= map["spring"][1][i] and flyBullets[1][
                                bul] - hitLen * sin < map["spring"][1][i] + map["spring"][3][i] \
                                    and flyBullets[0][bul] - hitLen * cos > map["spring"][0][i] and flyBullets[0][
                                bul] - hitLen * cos < map["spring"][0][i] + map["spring"][2][i]:
                                bulFlex.append(bul)                                # Добавляем пулю в список для удаления
                                break                                              # Прерываем проверку точек пули
                    # ===== УДАЛЕНИЕ ПУЛЬ, ПОПАВШИХ В ПРУЖИНЫ =====
                    bulFlex.sort(reverse=True)                                      # Сортируем индексы в обратном порядке для безопасного удаления
                    for bulFlexDel in bulFlex:                                     # Удаляем все пули, попавшие в пружины
                        flyBullets[0].pop(bulFlexDel)                             # Удаляем X координату пули
                        flyBullets[1].pop(bulFlexDel)                             # Удаляем Y координату пули
                        flyBullets[2].pop(bulFlexDel)                             # Удаляем угол пули
                        flyBullets[3].pop(bulFlexDel)                             # Удаляем скорость пули
                    # ===== ПРОВЕРКА КОЛЛИЗИИ ИГРОКА С ПРУЖИНОЙ =====
                    if y + Size > map["spring"][1][i] and y < map["spring"][1][i] + map["spring"][3][i] \
                    and x + Size > map["spring"][0][i] and x < map["spring"][0][i] + map["spring"][2][i]:
                        # ===== АКТИВАЦИЯ ПРУЖИНЫ =====
                        spring = 1                                                 # Устанавливаем флаг пружины
                        speedJ = SpringJ                                          # Устанавливаем скорость прыжка от пружины
                        jump = "motion"                                           # Запускаем прыжок
                        dash = "stop"                                             # Останавливаем рывок
                        timeDash = 0                                              # Сбрасываем таймер рывка
                        grav = 0                                                  # Отключаем гравитацию
                        speedG = 0                                                # Сбрасываем скорость по Y
                        canDash = True                                            # Разрешаем рывок
                        canJumpWallL = False                                      # Запрещаем прыжок от стены влево
                        canJumpWallR = False                                      # Запрещаем прыжок от стены вправо
                        canJump = False                                           # Запрещаем обычный прыжок
                # ===== ОБРАБОТКА ТОЧЕК ОТКАТА РЫВКА =====
                for i in range(len(map["rollback"][0])):                           # Перебираем все точки отката рывка
                    # ===== ПРОВЕРКА КОЛЛИЗИИ ИГРОКА С ТОЧКОЙ ОТКАТА =====
                    if y + Size > map["rollback"][1][i]-2 and y < map["rollback"][1][i] + map["rollback"][3]+2 \
                            and x + Size > map["rollback"][0][i]-2 and x < map["rollback"][0][i] + map["rollback"][2]+2:
                        if canDash == False and map["rollback"][4][i] == 0:        # Если рывок недоступен и точка не использована
                            canDash = True                                         # Разрешаем рывок
                            rollbackSound.play()                                   # Воспроизводим звук восстановления рывка
                            map["rollback"][4][i] += 1                            # Отмечаем точку как использованную
                    # ===== ОБНОВЛЕНИЕ ТАЙМЕРА ТОЧКИ ОТКАТА =====
                    if map["rollback"][4][i] > 0:                                 # Если точка используется
                        map["rollback"][4][i] += 1                                # Увеличиваем таймер
                    if map["rollback"][4][i] >= timeRollback:                     # Если время восстановления истекло
                        map["rollback"][4][i] = 0                                 # Сбрасываем таймер (точка готова к использованию)
                # ===== ОБРАБОТКА ТОЧЕК СПАВНА =====
                for i in range(len(map["spawnpoint"][0])):                         # Перебираем все точки спавна
                    # ===== ПРОВЕРКА КОЛЛИЗИИ ИГРОКА С ТОЧКОЙ СПАВНА =====
                    if y + Size > map["spawnpoint"][1][i] and y < map["spawnpoint"][1][i] + map["spawnpoint"][3] \
                            and x + Size > map["spawnpoint"][0][i] and x < map["spawnpoint"][0][i] + map["spawnpoint"][2]:
                        spawnX = map["spawnpoint"][0][i]                          # Обновляем X координату точки спавна
                        spawnY = map["spawnpoint"][1][i]
                        if spawnSX != spawnX - 440 or spawnSY != spawnY - 250:
                            saveSound.play()
                        spawnSX = spawnX - 440
                        spawnSY = spawnY - 250
                        map["spawnpoint"][4] = i
                # финиш №№№№№
                try:
                    for i in range(len(map["finish"][0])):
                        if y + Size > map["finish"][1][i] and y < map["finish"][1][i] + map["finish"][3] \
                                and x + Size > map["finish"][0][i] and x < map["finish"][0][i] + map["finish"][2]:
                            if canCreate == False:
                                if victoryTime == 2 * FPS:
                                    win = finish_level()
                                    finishSound.play()
                                    victoryTime -= 1
                except:
                    pass
                # патроны на карте
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
                # враги нападают
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
                            # смэрт
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
                # coyoteTime
                if timeCoyoteL < 5:
                    timeCoyoteL += 1
                    canJumpWallL = True
                if timeCoyoteR < 5:
                    timeCoyoteR += 1
                    canJumpWallR = True

        # экран
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
        # ===== РЕНДЕРИНГ КАДРА =====
        for d in range(1):
            # задник
            for i in range(len(map["background"][3])):
                if map["background"][0][i] + map["background"][2][i] > surfX and map["background"][1][i] + map["background"][3][i] > surfY \
                        and map["background"][0][i] < surfX + WIDTH and map["background"][1][i] < surfY + HEIGHT:
                    pygame.draw.rect(screen, map["background"][4][i], (map["background"][0][i]-surfX, map["background"][1][i]-surfY, map["background"][2][i],
                                                     map["background"][3][i]))
            ## Мёртвые противники
            try:
                for i in range(len(map["enemyFly"][1])):
                    if map["enemyFly"][9][i] <= 0:
                        if map["enemyFly"][0][i] + map["enemyFly"][2] > surfX \
                                and map["enemyFly"][1][i] + map["enemyFly"][3] > surfY \
                                and map["enemyFly"][0][i] < surfX + WIDTH and map["enemyFly"][1][i] < surfY + HEIGHT:
                            enemyFly = ENEMYDIE1
                            for j in range(len(enemyFly[0])):
                                drawX = map["enemyFly"][0][i] + enemyFly[0][j] - surfX
                                drawY = map["enemyFly"][1][i] + enemyFly[1][j] - surfY
                                pygame.draw.rect(screen, enemyFly[2][j], (drawX, drawY, 3, 3))
            except:
                pass
            # откат рывка
            timeCadrRoll += 1
            if timeCadrRoll >= FPS * RollBackSec // len(RollBackTexture):
                if cadrRoll + 1 < len(RollBackTexture):
                    cadrRoll += 1
                else:
                    cadrRoll = 0
                timeCadrRoll = 0
            RollTex = RollBackTexture[cadrRoll]
            RollTex2 = RollBackTexture2[cadrRoll]
            for i in range(len(map["rollback"][4])):
                if map["rollback"][0][i] + map["rollback"][2] > surfX \
                        and map["rollback"][1][i] + map["rollback"][3] > surfY \
                        and map["rollback"][0][i] < surfX + WIDTH and map["rollback"][1][i] < surfY + HEIGHT:
                    if map["rollback"][4][i] == 0:
                        for j in range(len(RollTex[0])):
                            drawX = map["rollback"][0][i] + RollTex[0][j] - surfX
                            drawY = map["rollback"][1][i] + RollTex[1][j] - surfY
                            pygame.draw.rect(screen, RollTex[2][j], (drawX, drawY, 2, 2))
                    else:
                        for j in range(len(RollTex2[0])):
                            drawX = map["rollback"][0][i] + RollTex2[0][j] - surfX
                            drawY = map["rollback"][1][i] + RollTex2[1][j] - surfY
                            pygame.draw.rect(screen, RollTex2[2][j], (drawX, drawY, 2, 2))
            # спавнер
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
            SpawnTex = SpawnTexture[cadrSpawn]
            SpawnTex2 = SpawnTexture2[cadrSpawn2]
            for i in range(len(map["spawnpoint"][1])):
                if map["spawnpoint"][0][i] + map["spawnpoint"][2] > surfX \
                        and map["spawnpoint"][1][i] + map["spawnpoint"][3] > surfY \
                        and map["spawnpoint"][0][i] < surfX + WIDTH and map["spawnpoint"][1][i] < surfY + HEIGHT:
                    if map["spawnpoint"][-1] == i:
                        for j in range(len(SpawnTex2[0])):
                            drawX = map["spawnpoint"][0][i] + SpawnTex2[0][j] - surfX
                            drawY = map["spawnpoint"][1][i] + SpawnTex2[1][j] - surfY
                            pygame.draw.rect(screen, SpawnTex2[2][j], (drawX, drawY, 3, 3))
                    else:
                        for j in range(len(SpawnTex[0])):
                            drawX = map["spawnpoint"][0][i] + SpawnTex[0][j] - surfX
                            drawY = map["spawnpoint"][1][i] + SpawnTex[1][j] - surfY
                            pygame.draw.rect(screen, SpawnTex[2][j], (drawX, drawY, 3, 3))
            ### ФИНИШ !!!!
            if finishTimeCadr < finishSec * FPS:
                finishTimeCadr += 1
                if finishTimeCadr >= finishSec * FPS:
                    finishTimeCadr = 0
            finishTex = FINISH[min(int(finishTimeCadr // (finishSec*FPS/len(FINISH))), len(FINISH) - 1)]
            try:
                for i in range(len(map["finish"][0])):
                    if map["finish"][0][i] + map["finish"][2] > surfX \
                            and map["finish"][1][i] + map["finish"][3] > surfY \
                            and map["finish"][0][i] < surfX + WIDTH and map["finish"][1][i] < surfY + HEIGHT:
                        for j in range(len(finishTex[0])):
                            drawX = map["finish"][0][i] + finishTex[0][j] - surfX
                            drawY = map["finish"][1][i] + finishTex[1][j] - surfY
                            pygame.draw.rect(screen, finishTex[2][j], (drawX, drawY, 3, 3))
            except:
                pass
            ### патроны на карте ###
            try:
                for i in range(len(map["bullets"][1])):
                    if map["bullets"][0][i] + map["bullets"][2] > surfX \
                            and map["bullets"][1][i] + map["bullets"][3] > surfY \
                            and map["bullets"][0][i] < surfX + WIDTH and map["bullets"][1][i] < surfY + HEIGHT:
                        for j in range(len(BulletTexture[0])):
                            drawX = map["bullets"][0][i] + BulletTexture[0][j] - surfX
                            drawY = map["bullets"][1][i] + BulletTexture[1][j] - surfY
                            pygame.draw.rect(screen, BulletTexture[2][j], (drawX, drawY, 3, 3))
            except:
                pass
            # пули летящие №№
            for i in range(len(flyBullets[0])):
                if flyBullets[0][i] + lengthBullets * cos > surfX \
                        and flyBullets[1][i] + lengthBullets * sin > surfY \
                        and flyBullets[0][i] < surfX + WIDTH and flyBullets[1][i] < surfY + HEIGHT:
                    sin = math.sin(math.radians(flyBullets[2][i]))
                    cos = math.cos(math.radians(flyBullets[2][i]))
                    drawX = flyBullets[0][i] - surfX
                    drawY = flyBullets[1][i] - surfY
                    pygame.draw.line(screen, flyBullets[3][i], [drawX, drawY], [drawX - lengthBullets * cos, drawY - lengthBullets * sin], 1)
            # пружинки
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
            # Главный Герой
            if dash == "stop": # and canDash == True and canJumpWallL == False and canJumpWallR == False:
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
            #pygame.draw.rect(screen, pygame.Color("red"), (x - surfX, y - surfY, Size, Size), 1) # хитбокс
            # шипы
            timeCadrSpikes += 1
            if timeCadrSpikes >= FPS * SpikesSec // len(SpikesTexture):
                if cadrSpikes + 1 < len(SpikesTexture):
                    cadrSpikes += 1
                else:
                    cadrSpikes = 0
                timeCadrSpikes = 0
            SpikesTex = SpikesTexture[cadrSpikes]
            for i in range(len(map["spikes"][3])):
                if map["spikes"][0][i] + map["spikes"][2][i] > surfX and map["spikes"][1][i] + map["spikes"][3][i] > surfY \
                        and map["spikes"][0][i] < surfX + WIDTH and map["spikes"][1][i] < surfY + HEIGHT:
                    pygame.draw.rect(screen, (225, 225, 225), (map["spikes"][0][i]-surfX, map["spikes"][1][i]-surfY, map["spikes"][2][i], map["spikes"][3][i]))
                    for w in range(map["spikes"][2][i]//10):
                        for j in range(len(SpikesTex[0])):
                            drawX = map["spikes"][0][i] + SpikesTex[0][j] - surfX + 10 * w
                            drawY = map["spikes"][1][i] + SpikesTex[1][j] - surfY
                            if drawX + surfX + 1 > surfX and drawY + surfY + 2 > surfY \
                                    and drawX + surfX < surfX + WIDTH and drawY + surfY < surfY + HEIGHT:
                                pygame.draw.rect(screen, SpikesTex[2][j], (drawX, drawY, 2, 2))
                    for h in range(map["spikes"][2][i] // 10):
                        for j in range(len(SpikesTex[0])):
                            drawX = map["spikes"][0][i] + SpikesTex[0][j] - surfX + 10 * h
                            drawY = map["spikes"][1][i] - SpikesTex[1][j] - surfY + map["spikes"][3][i]-2
                            if drawX + surfX + 1 > surfX and drawY + surfY + 2 > surfY \
                                    and drawX + surfX < surfX + WIDTH and drawY + surfY < surfY + HEIGHT:
                                pygame.draw.rect(screen, SpikesTex[2][j], (drawX, drawY, 2, 2))
            ### противники:::
            try:
                for i in range(len(map["enemyFly"][1])):
                    if map["enemyFly"][9][i] > 0:
                        if map["enemyFly"][0][i] + map["enemyFly"][2] > surfX \
                                and map["enemyFly"][1][i] + map["enemyFly"][3] > surfY \
                                and map["enemyFly"][0][i] < surfX + WIDTH and map["enemyFly"][1][i] < surfY + HEIGHT:
                            if map["enemyFly"][6][i] or map["enemyFly"][8][i] > 0:
                                if map["enemyFly"][-1][i] <= enemyFlySec * FPS:
                                    enemyFly = ENEMY1[
                                        min(map["enemyFly"][-1][i] // (enemyFlySec * FPS // len(ENEMY1)), len(ENEMY1) - 1)]
                                    map["enemyFly"][-1][i] += 1
                                else:
                                    map["enemyFly"][-1][i] = 0
                                    enemyFly = ENEMY1[0]
                            else:
                                enemyFly = ENEMYSTAN1
                            for j in range(len(enemyFly[0])):
                                drawX = map["enemyFly"][0][i] + enemyFly[0][j] - surfX
                                drawY = map["enemyFly"][1][i] + enemyFly[1][j] - surfY
                                pygame.draw.rect(screen, enemyFly[2][j], (drawX, drawY, 3, 3))
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
            # блоки
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
            #pygame.draw.rect(screen, pygame.Color('yellow'), (WIDTH//2-surf//2, 0, surf, HEIGHT), 1)
            #pygame.draw.rect(screen, pygame.Color('yellow'), (0, HEIGHT//2-surf//2, WIDTH, surf), 1)
            fps = int(clock.get_fps())
            textFPS = font.render('FPS: ' + str(fps), 1, WHITE)
            textX = font.render('X: ' + str(int(x)), 1, WHITE)
            textY = font.render('Y: ' + str(int(y)), 1, WHITE)
            textSpeed = font.render('Speed: ' + str(int(math.sqrt((xO-x)**2 + (yO-y)**2))), 1, WHITE)
            textGame = font.render('GameMode: ' + str(gameMode), 1, WHITE)
            textType = font.render('Type: ' + str(createType), 1, WHITE)
            # оружие
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
                #screen.blit(GunSurf, (400, 400))
            # патроны
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

            # прочее
            if canCreate:
                screen.blit(textX, (10, 30))
                screen.blit(textY, (10, 50))
                screen.blit(textSpeed, (10, 70))
                screen.blit(textGame, (10, 90))
                screen.blit(textFPS, (10, 10))
            if gameMode == "creat":
                screen.blit(textType, (10, 110))
                if draw == 1:
                    if createType != "rollback" and createType != "spawnpoint" and createType != "bullets" and createType != "enemyFly" and createType != "finish":
                        pygame.draw.rect(screen, pygame.Color('red'), (
                            map[createType][0][-1] - surfX, map[createType][1][-1] - surfY,
                            mouseX + surfX - map[createType][0][-1],
                            mouseY + surfY - map[createType][1][-1]), 1)
                    else:
                        try:
                            pygame.draw.rect(screen, pygame.Color('red'), (
                                mouseX - map[createType][2]//2, mouseY - map[createType][3]//2,
                                mouseX + map[createType][2]//2 - (mouseX - map[createType][2]//2),
                                mouseY + map[createType][3]//2 - (mouseY - map[createType][3]//2)), 1)
                        except:
                            map["bullets"] = [[], [], 15, 15, [], []]
                            map["enemyFly"] = [[], [], 21, 21, [], [], [], [[], [], [], []], [], [], []]
                            map["finish"] = [[], [], 24, 24]
                            pygame.draw.rect(screen, pygame.Color('red'), (
                                mouseX - map[createType][2] // 2, mouseY - map[createType][3] // 2,
                                mouseX + map[createType][2] // 2 - (mouseX - map[createType][2] // 2),
                                mouseY + map[createType][3] // 2 - (mouseY - map[createType][3] // 2)), 1)
                elif draw == 2:
                    pygame.draw.rect(screen, pygame.Color('blue'), (firstMouseX, firstMouseY, mouseX-firstMouseX, mouseY-firstMouseY), 1)
                elif draw == -1:
                    for i in range(len(correctObject["block"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["block"][0][correctObject["block"][i]],
                                          -surfY+map["block"][1][correctObject["block"][i]],
                                          map["block"][2][correctObject["block"][i]],
                                          map["block"][3][correctObject["block"][i]]), 2)
                    for i in range(len(correctObject["spikes"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX + map["spikes"][0][correctObject["spikes"][i]],
                                          -surfY + map["spikes"][1][correctObject["spikes"][i]],
                                          map["spikes"][2][correctObject["spikes"][i]],
                                          map["spikes"][3][correctObject["spikes"][i]]), 2)
                    for i in range(len(correctObject["spring"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["spring"][0][correctObject["spring"][i]],
                                          -surfY+map["spring"][1][correctObject["spring"][i]],
                                          map["spring"][2][correctObject["spring"][i]],
                                          map["spring"][3][correctObject["spring"][i]]), 2)
                    for i in range(len(correctObject["background"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["background"][0][correctObject["background"][i]],
                                          -surfY+map["background"][1][correctObject["background"][i]],
                                          map["background"][2][correctObject["background"][i]],
                                          map["background"][3][correctObject["background"][i]]), 2)
                    for i in range(len(correctObject["rollback"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["rollback"][0][correctObject["rollback"][i]],
                                          -surfY+map["rollback"][1][correctObject["rollback"][i]],
                                          map["rollback"][2],
                                          map["rollback"][3]), 2)
                    for i in range(len(correctObject["spawnpoint"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["spawnpoint"][0][correctObject["spawnpoint"][i]],
                                          -surfY+map["spawnpoint"][1][correctObject["spawnpoint"][i]],
                                          map["spawnpoint"][2],
                                          map["spawnpoint"][3]), 2)
                    for i in range(len(correctObject["bullets"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["bullets"][0][correctObject["bullets"][i]],
                                          -surfY+map["bullets"][1][correctObject["bullets"][i]],
                                          map["bullets"][2],
                                          map["bullets"][3]), 2)
                    for i in range(len(correctObject["enemyFly"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["enemyFly"][0][correctObject["enemyFly"][i]],
                                          -surfY+map["enemyFly"][1][correctObject["enemyFly"][i]],
                                          map["enemyFly"][2],
                                          map["enemyFly"][3]), 2)
                    for i in range(len(correctObject["finish"])):
                        pygame.draw.rect(screen, pygame.Color('blue'),
                                         (-surfX+map["finish"][0][correctObject["finish"][i]],
                                          -surfY+map["finish"][1][correctObject["finish"][i]],
                                          map["finish"][2],
                                          map["finish"][3]), 2)

                if createType == "background":
                    for i in range(len(backColor)):
                        pygame.draw.rect(screen, backColor[i], (WIDTH-30-i*30, 0, 30, 30))
                        if createColor == backColor[i]:
                            pygame.draw.rect(screen, WHITE, (WIDTH - 30 - i * 30, 0, 30, 30), 2)
        # ===== ОБРАБОТКА ЗВУКОВ ДВИЖЕНИЯ =====
        # Воспроизведение звука бега при движении по земле
        if grav == 0 and yO == y and xO != x:        # Игрок на земле и движется горизонтально
            if playSoundRun == 1:                    # Если звук бега не играет
                runSound.play(-1)                    # Запускаем звук бега в цикле
                playSoundRun = 0                     # Отмечаем, что звук играет
        else:                                        # Игрок не на земле или не движется
            if playSoundRun == 0:                    # Если звук бега играет
                runSound.stop()                      # Останавливаем звук бега
                playSoundRun = 1                     # Отмечаем, что звук остановлен
        
        # Воспроизведение звука падения
        if grav == 0 and yO < y:                     # Игрок падает (был выше, стал ниже)
            dropSound.play()                         # Воспроизводим звук падения
        
        # ===== ОБНОВЛЕНИЕ ПРЕДЫДУЩИХ ПОЗИЦИЙ =====
        # Сохраняем текущие позиции для следующего кадра
        xO = x                                       # Предыдущая позиция X
        yO = y                                       # Предыдущая позиция Y
    # ===== ЭКРАН ЗАВЕРШЕНИЯ УРОВНЯ (ЗАКОММЕНТИРОВАНО) =====
    # Старая версия экрана завершения уровня (заменена на новую)
    '''if finish_menu_open:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        title_text = "УРОВЕНЬ ЗАВЕРШЕН!"
        title_font = pygame.font.Font(None, 48)
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_surface, title_rect)
        if completion_time > 0:
            time_seconds = completion_time // 1000
            time_minutes = time_seconds // 60
            time_seconds = time_seconds % 60
            time_text = f"Время: {time_minutes:02d}:{time_seconds:02d}"
        else:
            time_text = "Время: --:--"
        time_font = pygame.font.Font(None, 32)
        time_surface = time_font.render(time_text, True, (255, 255, 0))
        time_rect = time_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        screen.blit(time_surface, time_rect)
        deaths_text = f"Смертей: {settings['statistics']['current_level_deaths']}"
        deaths_surface = time_font.render(deaths_text, True, (255, 100, 100))
        deaths_rect = deaths_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(deaths_surface, deaths_rect)
        button_font = pygame.font.Font(None, 28)
        main_menu_text = "Главное меню (ESC)"
        main_menu_surface = button_font.render(main_menu_text, True, (200, 200, 200))
        main_menu_rect = main_menu_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(main_menu_surface, main_menu_rect)
        maps_text = "Выбор карт (Enter)"
        maps_surface = button_font.render(maps_text, True, (200, 200, 200))
        maps_rect = maps_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90))
        screen.blit(maps_surface, maps_rect)'''
    
    # ===== ФИНАЛИЗАЦИЯ КАДРА =====
    # Масштабирование и отображение на экране
    virtual_display = pygame.transform.scale(screen, current_size)  # Масштабируем виртуальный экран под реальный
    screen0.blit(virtual_display, (0, 0))                          # Копируем на физический экран
    pygame.display.update()                                        # Обновляем дисплей
    clock.tick(FPS)                                                # Ограничиваем FPS

# ===== ЗАВЕРШЕНИЕ ПРОГРАММЫ =====
pygame.quit()                                                      # Корректно завершаем pygame
sys.exit()