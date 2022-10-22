import sys, pygame


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonText = buttonText
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

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
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction(self.buttonText)
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


def button_pushed(buttonText):
    if len(text) == 19:
        text.clear()
        lbl_text.fill((255, 255, 255))
    if buttonText == 'right':
        text.append('right')
    if buttonText == 'left':
        text.append('left')
    if buttonText == 'down':
        text.append('down')
    if buttonText == 'up':
        text.append('up')
    text1 = f1.render(text[-1], True,
                      (180, 0, 0))
    lbl_text.blit(text1, (10, (len(text) - 1) * 30))

pygame.init()

font = pygame.font.Font(None, 36)
objects = []
button_right = Button(10, 10, 100, 20, "right", button_pushed)
button_left = Button(130, 10, 100, 20, "left", button_pushed)
button_up = Button(10, 40, 100, 20, "up", button_pushed)
button_down = Button(130, 40, 100, 20, "down", button_pushed)

size_lbl = width_lbl, height_lbl = 350, 350
x_lbl, y_lbl = (10, 240)

size_lbl_text = width_lbl_text, height_lbl_text = 400, 570
x_lbl_text, y_lbl_text = (380, 20)
lbl_text = pygame.Surface(size_lbl_text)
lbl_text.fill((255, 255, 255))

black = 0, 0, 0
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

speed_x = 0
speed_y = 0
x = 0
y = 0
SPEED = 3
K_w, K_s, K_a, K_d = 0, 0, 0, 0

clock = pygame.time.Clock()


hero = pygame.Surface((10, 10))
hero.fill((255, 255, 255))
bg = pygame.Surface(size_lbl)
bg.fill((100, 0, 0))

text = []
screen.blit(bg, (x_lbl, y_lbl))
screen.blit(lbl_text, (x_lbl_text, y_lbl_text))
f1 = pygame.font.Font(None, 36)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                K_w = -1
            elif event.key == pygame.K_s:
                K_s = 1
            elif event.key == pygame.K_d:
                K_d = 1
            elif event.key == pygame.K_a:
                K_a = -1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                K_w = 0
            elif event.key == pygame.K_s:
                K_s = 0
            elif event.key == pygame.K_d:
                K_d = 0
            elif event.key == pygame.K_a:
                K_a = 0
    for object in objects:
        object.process()

    speed_x = SPEED * (K_a + K_d)
    speed_y = SPEED * (K_w + K_s)
    x += speed_x
    y += speed_y
    if x < 0 or x > width_lbl - 10 or y < 0 or y > height_lbl - 10:
        x, y = width_lbl // 2, height_lbl // 2
    bg.fill((100, 0, 0))
    bg.blit(hero, (x, y))
    screen.blit(bg, (x_lbl, y_lbl))

    screen.blit(lbl_text, (x_lbl_text, y_lbl_text))
    pygame.display.update()
    clock.tick(60)
