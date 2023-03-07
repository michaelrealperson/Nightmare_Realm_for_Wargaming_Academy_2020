import asyncio
import pygame
import random

# создание окна
pygame.init()
widht_window = 400
height_window = 480
screen = pygame.display.set_mode((widht_window, height_window))
pygame.display.set_caption('Nightmare Realm')

# загрузка изображений
background = pygame.image.load('images/bg.png')
chips_images = { 'wall' : pygame.image.load('images/wall.png'),
                 'hall' : pygame.image.load('images/hall.png'),
                 'card' : pygame.image.load('images/card.png'),
                 'clock' : pygame.image.load('images/clock.png'),
                 'cup' : pygame.image.load('images/cup.png'),
                 'selected' : pygame.image.load('images/selected.png'),
                 'update' : pygame.image.load('images/update.png') }
animation_images = { 'card' : [],
                     'clock' : [],
                     'cup' : []  }

winning_animation = []

# анимация фишек
for item in animation_images.items():
    for i in range(1, 9):
        animation_images[item[0]].append(pygame.image.load('images/animation/'+item[0]+'/'+item[0]+'_0000'+str(i)+'.png'))
    for i in range(10, 24):
        animation_images[item[0]].append(pygame.image.load('images/animation/'+item[0]+'/'+item[0]+'_000'+str(i)+'.png'))
# победная анимация
for i in range(0, 9):
    winning_animation.append(pygame.image.load('images/animation/alice/alice0'+str(i)+'.png'))
for i in range(10, 23):
    winning_animation.append(pygame.image.load('images/animation/alice/alice'+str(i)+'.png'))

# загрузка музыки
music = 'music/American McGees Alice - Flying On the Wings of Steam.wav'

# другие переменные
field = []
size_chip = 80
check_select_chip = False
x_chip = 0
y_chip = 0
counting_chips = [0, 0, 0]
victory = False
check_position = [x_chip, y_chip]
chip_animation_index = 0
winner_animation_index = 0
clock = pygame.time.Clock()
FPS = 20

# создание поля
async def creat_field():
    global field
    await asyncio.sleep(0)
    field = [[],[],[],[],[], []]
    for i in range(5):
        if i % 2 == 0:
            for j in range(5):
                if j % 2 == 0:
                    field[i].append('hall')
                else:
                    field[i].append('wall')
        else:
            for j in range(5):
                field[i].append('hall')
        field[5].append('wall')

# расстановка фишек
async def random_chips():
    global field
    await asyncio.sleep(0)
    for i in range(3):
        chips_count = 5
        while chips_count > 0:
            x = random.randint(0,4)
            y = random.randint(0,4)
            if field[x][y] == 'hall':
                if i == 0:
                    field[x][y] = 'clock'
                    chips_count -= 1
                elif i == 1:
                    field[x][y] = 'card'
                    chips_count -= 1
                elif i == 2:
                    field[x][y] = 'cup'
                    chips_count -= 1       
        

# прорисовка объектов      
async def draw_window():
    global field
    global check_select_chip
    global check_position
    global counting_chips
    global size_chip
    global victory
    global winning_animation
    global winner_animation_index
    await asyncio.sleep(0)
    screen.blit(background, (0,0))
    counting_chips = [0, 0, 0]
    for i in field:
        if i[0] == 'card':
            counting_chips[0] += 1
        if i[2] == 'clock':
            counting_chips[1] += 1
        if i[4] == 'cup':
            counting_chips[2] += 1
    if check_select_chip:
        screen.blit(chips_images['selected'], check_position)
    for i in range(3):
        if counting_chips[i] == 5:
            for j in range(5):
                screen.blit(chips_images['selected'], (2*i*size_chip, j*size_chip))    
    for i in range(5):
        for j in range(5):
            index = field[i][j]
            if index == 'card' or index == 'clock' or index == 'cup':
                screen.blit(animation_images[index][chip_animation_index], [j*size_chip, i*size_chip])
            else:
                screen.blit(chips_images[index], [j*size_chip, i*size_chip])
    screen.blit(chips_images['card'], [0*size_chip, 5*size_chip])
    screen.blit(chips_images['update'], (1*size_chip, 5*size_chip))
    screen.blit(chips_images['clock'], [2*size_chip, 5*size_chip])
    screen.blit(chips_images['update'], (3*size_chip, 5*size_chip))
    screen.blit(chips_images['cup'], [4*size_chip, 5*size_chip])
    if victory:
        screen.blit(winning_animation[winner_animation_index], (0,0))
        winner_animation_index += 1
        if winner_animation_index == 22:
            winner_animation_index = 0
    pygame.display.update()

# новое поле
asyncio.run(creat_field())
asyncio.run(random_chips())
asyncio.run(draw_window())
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)

# старт игры
while True:
    clock.tick(FPS)
    position_mouse = pygame.mouse.get_pos()
    x_mouse = position_mouse[1]//size_chip
    y_mouse = position_mouse[0]//size_chip
    check_push_update = (x_mouse == 5) and (y_mouse == 1 or y_mouse == 3)
    check_free_field = check_select_chip and abs(x_mouse - x_chip) + abs(y_mouse - y_chip) == 1 and field[x_mouse][y_mouse] == 'hall' and not victory
    check_presence_chip = field[x_mouse][y_mouse] != 'wall' and field[x_mouse][y_mouse] != 'hall' and not victory
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if check_push_update:
                    asyncio.run(creat_field())
                    asyncio.run(random_chips())
                    victory = False
                elif check_free_field:
                    check_select_chip = False
                    field[x_mouse][y_mouse], field[x_chip][y_chip] = field[x_chip][y_chip], field[x_mouse][y_mouse]
                elif check_presence_chip:
                    x_chip = x_mouse
                    y_chip = y_mouse
                    check_select_chip = True
                    check_position = [y_mouse*size_chip, x_mouse*size_chip]
    chip_animation_index += 1
    if chip_animation_index == 22:
        chip_animation_index = 0
    if counting_chips == [5, 5, 5]:
        victory = True
    asyncio.run(draw_window())
