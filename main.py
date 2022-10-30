import os
import time

import pygame
import sys


class Button:
    def __init__(self, x, y, width, height, buttonText, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onePress = onePress
        self.alreadyPressed = False
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonText = buttonText
        self.buttonSurf = pygame.font.Font(None, 36).render(buttonText, True, (20, 20, 20))
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    pass
                elif not self.alreadyPressed:
                    self.button_clicked()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

    def button_clicked(self):
        if self.buttonText in ["right", "left", "down", "up"]:
            self.append_text()
        elif self.buttonText == "enter":
            self.enter()

    def enter(self):
        ENTER[0] = True

    def append_text(self):
        if len(text) == 19:
            text.clear()
            lbl_text.fill(lbl_text_color)
        text.append(commands[self.buttonText])
        text1 = f1.render(text[-1], True,
                                      (textColor))
        lbl_text.blit(text1, (10, (len(text) - 1) * 30))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'finish':
            self.add(finish_group)
        if tile_type == 'box':
            self.add(box_group)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__(all_sprites)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if ENTER[0]:
            for i in text:
                command = commands2[i]
                if command == 'right':
                    self.rect.x += tile_width
                elif command == 'left':
                    self.rect.x -= tile_width
                elif command == 'up':
                    self.rect.y -= tile_height
                elif command == 'down':
                    self.rect.y += tile_height
                screen.blit(robot_field, (x_lbl, y_lbl))
                robot_field.fill((0, 0, 0))
                all_sprites.draw(robot_field)
                pygame.display.update()
                time.sleep(0.3)
                for i in finish_group:
                    if pygame.sprite.collide_rect(self, i):
                        WIN[0] = True

                for i in box_group:
                    if pygame.sprite.collide_rect(self, i):
                        EXPLODE[0] = True
                        break
                if EXPLODE[0]:
                    break
            ENTER[0] = False
            text.clear()
            lbl_text.fill(lbl_text_color)



def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '+':
                Tile('box', x, y)
            elif level[y][x] == '$':
                Tile('finish', x, y)
            elif level[y][x] == '@':
                new_player = Player(pygame.transform.scale(load_image("robot.png"), (tile_width, tile_height)), (tile_width * x, tile_width * y))
    return new_player, x, y


def load_level(filename):
    filename = "maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_robot_field(width_field, height_field, depth, color):
    robot_field.fill((100, 0, 0))
    for i in range(width_field):
        x = width_lbl / width_field * i
        pygame.draw.line(robot_field, color, [x, 0], [x, height_lbl], depth)
    for j in range(height_field):
        y = height_lbl / height_field * j
        pygame.draw.line(robot_field, color, [0, y], [width_lbl, y], depth)
    pygame.draw.line(
        robot_field, color,
        [width_lbl - depth, 0],
        [width_lbl - depth, height_lbl], depth)
    pygame.draw.line(robot_field, color,
                     [0, height_lbl - depth],
                     [width_lbl, height_lbl - depth], depth)


commands = {
            "right": 'Robot.MoveTo(X.Position++);',
            "left": "Robot.MoveTo(X.Position--);",
            "down": "Robot.MoveTo(Y.Position++);",
            "up": "Robot.MoveTo(Y.Position--);"
        }

commands2 = {
            'Robot.MoveTo(X.Position++);': "right",
            "Robot.MoveTo(X.Position--);": "left",
            "Robot.MoveTo(Y.Position++);": "down",
            "Robot.MoveTo(Y.Position--);": "up"
        }

filename = 'map.txt'
ENTER = [False]

size_lbl = width_lbl, height_lbl = 350, 350
x_lbl, y_lbl = (10, 240)

pygame.init()
size = width, height = (800, 600)
screen = pygame.display.set_mode(size)

player = None
file = load_level(filename)
tile_width = tile_height = width_lbl / max(len(file), len(file[0]))


tile_images = {
    'box': pygame.transform.scale(load_image('box1.png'), (tile_width, tile_height)),
    'finish': pygame.transform.scale(load_image('finish3.png'), (tile_width, tile_height)),
}

box_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

objects = []
button_right = Button(10, 20, 170, 40, "right")
button_left = Button(190, 20, 170, 40, "left")
button_up = Button(10, 80, 170, 40, "up")
button_down = Button(190, 80, 170, 40, "down")
button_enter = Button(10, 140, 350, 60, "enter")


lbl_text_color = (30,30,30)
textColor = (33,115,38)

size_lbl_text = width_lbl_text, height_lbl_text = 400, 570
x_lbl_text, y_lbl_text = (380, 20)
lbl_text = pygame.Surface(size_lbl_text)
lbl_text.fill(lbl_text_color)

clock = pygame.time.Clock()


robot_field = pygame.Surface(size_lbl)

player, level_x, level_y = generate_level(load_level(filename))
EXPLODE = [False]
text = []
screen.blit(robot_field, (x_lbl, y_lbl))
screen.blit(lbl_text, (x_lbl_text, y_lbl_text))
f1 = pygame.font.SysFont('montserrat', 32)

width_field, height_field = 14, 14
depth = 2
WIN = [False]


while 1:
    if WIN[0]:
        screen.fill((0, 100, 0))
    if EXPLODE[0]:
        screen.fill((100, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    for obj in objects:
        obj.process()
    screen.blit(lbl_text, (x_lbl_text, y_lbl_text))
    screen.blit(robot_field, (x_lbl, y_lbl))
    robot_field.fill((0, 0, 0))
    all_sprites.draw(robot_field)
    pygame.display.update()
    all_sprites.update()
    clock.tick(60)