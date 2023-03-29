from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from sys import exit
from colors import *
from random import randrange, choice, randint
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import shelve
from numba import prange


open_file = shelve.open("save_game")
if "MONEY" in open_file:
    Money = open_file["MONEY"]
else:
    Money = 0
pygame.init()
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Змейка")
state = "MENU"
clock = pygame.time.Clock()
menu_fon = pygame.image.load('menu.jpg')
menu_fon = pygame.transform.scale(menu_fon, display.get_size())
font = pygame.font.SysFont(None, 58)
level = 1

game_fon1 = pygame.image.load("map.png")
game_fon1 = pygame.transform.scale(game_fon1, display.get_size())
walls_rects = []

x1 = display.get_size()[0] / 2
y1 = display.get_size()[1] / 2


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, black, [x[0], x[1], snake_block, snake_block])


class MENU_BUTTONS(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.image = pygame.Surface([300, 80])
        self.image.fill((255, 224, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text


    def draw_text(self):
        display.blit(font.render(self.text, True, (0, 23, 255)), (self.rect.x + self.image.get_size()[0] / 4, self.rect.y + self.image.get_size()[1] / 3))


menu_group = pygame.sprite.Group()
button1 = MENU_BUTTONS(int(display.get_size()[0] / 2 - 150), int(display.get_size()[1] / 3 - 200), "Играть")
button2 = MENU_BUTTONS(int(display.get_size()[0] / 2 - 150), int(display.get_size()[1] / 2 - 200), "Уровни")
button3 = MENU_BUTTONS(int(display.get_size()[0] / 2 - 150), int(display.get_size()[1] / 2), "Выйти")
menu_group.add(button2)
menu_group.add(button1)
menu_group.add(button3)

foodx = round(randrange(0, display.get_size()[0] - snake_block) / 10.0) * 10.0
foody = round(randrange(0, display.get_size()[1] - snake_block) / 10.0) * 10.0

x1_change = snake_block

levels_fon = pygame.image.load("levels.jpg")
levels_fon = pygame.transform.scale(levels_fon, display.get_size())


sclad_menu = pygame.sprite.Group()
button1_sclad = MENU_BUTTONS(int(display.get_size()[0] / 3 - 100), int(display.get_size()[1] / 2 - 200), "Своя карта")
button2_sclad = MENU_BUTTONS(int(display.get_size()[0] / 2), int(display.get_size()[1] / 2 - 200), "Наша карта")
button3_sclad = MENU_BUTTONS(int(display.get_size()[0] / 2 - 150), int(display.get_size()[1] / 2), "Простая карта")
sclad_menu.add(button1_sclad)
sclad_menu.add(button2_sclad)
sclad_menu.add(button3_sclad)

coordinats = []

filetypes = (
    ('text files', '*.txt'),
    ('All files', '*.*')
)


def randomx_food():

    choose = []
    all_sizes = []
    for i in coordinats:
        all_sizes.append(int(i.split(",")[0]))

    for j in prange(1, len(all_sizes)):
        if all_sizes[j - 1] > all_sizes[j]:
            choose.append(randint(all_sizes[j], all_sizes[j - 1]))
        else:
            choose.append(randint(all_sizes[j - 1], all_sizes[j]))


    return choice(choose)



def randomy_food():
    choose = []
    all_sizes = []
    for i in coordinats:
        all_sizes.append(int(i.split(",")[1]))

    for j in prange(1, len(all_sizes)):
        if all_sizes[j - 1] > all_sizes[j]:
            choose.append(randint(all_sizes[j], all_sizes[j - 1]))
        else:
            choose.append(randint(all_sizes[j - 1], all_sizes[j]))

    return choice(choose)

def eating_himself():
    ate = False
    for i in snake_List:
        if i != snake_List[0]:
            if pygame.Rect(snake_List[0], (snake_block, snake_block)).colliderect(pygame.Rect(i, (snake_block, snake_block))):
                ate = True

    return ate


def blit_money():
    display.blit(font.render("Денег: " + str(Money), True, red), (180, 50))


while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                open_file["MONEY"] = Money
                open_file.close()
                pygame.quit()
                exit()
        elif event.type == pygame.QUIT:
            open_file["MONEY"] = Money
            open_file.close()
            pygame.quit()
            exit()
        if state == "MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button3.rect.collidepoint(pos):
                    open_file["MONEY"] = Money
                    open_file.close()
                    pygame.quit()
                    exit()
                elif button1.rect.collidepoint(pos):
                    x1 = display.get_size()[0] / 2
                    y1 = display.get_size()[1] / 2
                    walls_rects = []
                    Length_of_snake = 1
                    snake_List = []
                    if level == 1:
                        foodx = round(randrange(0, display.get_size()[0] - snake_block) / 10.0) * 10.0
                        foody = round(randrange(0, display.get_size()[1] - snake_block) / 10.0) * 10.0
                    else:
                        foodx = randomx_food()
                        foody = randomy_food()
                    state = "GAME"
                elif button2.rect.collidepoint(pos):
                    state = "LEVELS"

        elif state == "GAME":

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not ON_PAUSE:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and not ON_PAUSE:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and not ON_PAUSE:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and not ON_PAUSE:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_SPACE:
                    if not ON_PAUSE:
                        tmp1 = x1_change
                        tmp2 = y1_change

                        x1_change = 0
                        y1_change = 0
                        ON_PAUSE = True
                    else:
                        x1_change = tmp1
                        y1_change = tmp2
                        ON_PAUSE = False
                elif event.key == pygame.K_TAB:
                    state = "MENU"
                    walls_rects = []
                    Length_of_snake = 1

        elif state == "LEVELS":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    state = "MENU"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if button1_sclad.rect.collidepoint(mouse):
                    root = Tk()
                    root.withdraw()
                    d = askopenfilename(parent=root, filetypes=filetypes)
                    root.destroy()
                    if d:
                        level = 3
                        with open(d, "r") as file:
                            coordinats = file.read().split(" ")
                elif button3_sclad.rect.collidepoint(mouse):
                    level = 1
                    coordinats = []
                elif button2_sclad.rect.collidepoint(mouse):
                    level = 2
                    coordinats = ["500, 300", "400, 100", "300, 300", "800,200", "500,500"]

    if state == "MENU":
        display.blit(menu_fon, (0, 0))
        menu_group.draw(display)
        button1.draw_text()
        button2.draw_text()
        button3.draw_text()
        blit_money()
        clock.tick(30)

    elif state == "GAME":

        display.blit(game_fon1, (0, 0))

        if level != 1:
            for i in coordinats:
                walls_rects.append(pygame.draw.rect(display, red, (int(i.split(",")[0]), int(i.split(",")[1]), wall_size, wall_size)))
        if ON_PAUSE:
            pygame.draw.rect(display, (56, 73, 239, 255), (0,0, display.get_size()[0], display.get_size()[1]))
            blit_money()
            display.blit(font.render("Вы на паузе нажмате на пробел чтобы играть", True, red), (400, 400))
        else:
            if x1 >= display.get_size()[0] or x1 < 0 or y1 >= display.get_size()[1] or y1 < 0:
                state = "MENU"

            if eating_himself():
                state = "MENU"

            clock.tick(snake_speed)

            x1 += x1_change
            y1 += y1_change

            pygame.draw.rect(display, green, [foodx, foody, snake_block, snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)

            for x in snake_List[:-1]:
                if x == snake_Head:
                    Length_of_snake = 1
                    walls_rects = []
                    state = "MENU"

            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            our_snake(snake_block, snake_List)
            if pygame.Rect(snake_Head, (snake_block, snake_block)).colliderect(pygame.Rect((foodx, foody), (snake_block, snake_block))):
                if level == 1:
                    foodx = round(randrange(0, display.get_size()[0] - snake_block) / 10.0) * 10.0
                    foody = round(randrange(0, display.get_size()[1] - snake_block) / 10.0) * 10.0
                else:
                    foodx = randomx_food()
                    foody = randomy_food()

                Length_of_snake += 1
                Money += 1

            for i in walls_rects:
                if pygame.Rect(snake_Head, (snake_block, snake_block)).colliderect(i):
                    walls_rects = []
                    Length_of_snake = 1
                    state = "MENU"

            blit_money()

    elif state == "LEVELS":
        display.blit(levels_fon, (0, 0))
        sclad_menu.draw(display)
        button1_sclad.draw_text()
        button2_sclad.draw_text()
        button3_sclad.draw_text()

    pygame.display.flip()