import pygame
from pygame import *
from random import randint
import button
from character import Character

init()
mixer.pre_init(44100, -16, 1, 512)
mixer.init()
clock = time.Clock()
# define color and size
WIDTH, HEIGHT, FPS = 1200, 730, 60
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
GREEN, BLUE, YELLOW = (0, 255, 0), (0, 0, 255), (239, 228, 176)
# create game window
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Catch or Lose")
display.set_icon(image.load("images/logo.png"))
# insert sounds
c_catch = mixer.Sound('songs/catch.wav')
d_catch = mixer.Sound('songs/screaming_demogorgon.wav')
v_catch = mixer.Sound('songs/screaming_vecna.wav')
song_for_the_game = 'songs/Kids - Kyle Dixon.mp3'
# define variables
game, menu, game_start = True, True, False
menu_state = "main"
speed_min, speed_max, speed_portal, frequency = 1, 2, 8, 1000
game_score, life, level = 0, 3, 1
history_of_scores = []
# define image elements
game_background = image.load('images/hawkins.jpeg').convert()
game_background = transform.scale(game_background, (WIDTH, HEIGHT))
menu_background = image.load('images/background_menu.png').convert_alpha()
menu_background = transform.scale(menu_background, (WIDTH, HEIGHT))
score_image = image.load('images/score.png').convert_alpha()
score_image = transform.scale(score_image, (score_image.get_width() // 3, score_image.get_height() // 3))
area_for_score = image.load('button_image/area_for_score.png').convert_alpha()
area_for_score = transform.scale(area_for_score,
                                 (area_for_score.get_width() // 3, area_for_score.get_height() // 3))
life_image = image.load('images/fire.png').convert_alpha()
life_image = transform.scale(life_image, (life_image.get_width() // 21, life_image.get_height() // 21))
portal = image.load('images/portal.png').convert_alpha()
portal = transform.scale(portal, (portal.get_width() // 3.5, portal.get_height() // 3.5))
portal_rect = portal.get_rect(centerx=WIDTH // 2, bottom=HEIGHT - 5)
area_for_rules = image.load('button_image/area_for_rules.png').convert_alpha()
# define character image
eleven = image.load('images/eleven.bmp')
eleven = transform.scale(eleven, (eleven.get_width() // 1.7, eleven.get_height() // 1.7))
dustin = image.load('images/dustin.bmp')
dustin = transform.scale(dustin, (dustin.get_width() // 1.7, dustin.get_height() // 1.7))
steve = image.load('images/steve2.bmp')
steve = transform.scale(steve, (steve.get_width() // 1.7, steve.get_height() // 1.7))
hopper = image.load('images/hopper.bmp')
hopper = transform.scale(hopper, (hopper.get_width() // 1.7, hopper.get_height() // 1.7))
demogorgan = image.load('images/demogorgan.bmp')
demogorgan = transform.scale(demogorgan, (demogorgan.get_width() // 1.7, demogorgan.get_height() // 1.7))
demogorgan2 = image.load('images/demogorgan2.bmp')
demogorgan2 = transform.scale(demogorgan2, (demogorgan2.get_width() // 1.7, demogorgan2.get_height() // 1.7))
vecna = image.load('images/vecna.bmp')
vecna = transform.scale(vecna, (vecna.get_width() // 1.7, vecna.get_height() // 1.7))
# define fonts
ARIAL_BLACK_18 = font.SysFont('arialblack', 18)
ARIAL_BLACK_25 = font.SysFont('arialblack', 25)
ARIAL_30 = font.SysFont('arial', 30)
LEELAWADEE_40 = font.SysFont('leelawadeeuisemilight', 40)
# load button images
resume_img = image.load("button_image/button_resume.png").convert_alpha()
start_img = image.load("button_image/button_start.png").convert_alpha()
audio_img = image.load("button_image/button_audio.png").convert_alpha()
quit_img = image.load("button_image/button_quit.png").convert_alpha()
soundtrack1_img = image.load("button_image/button_soundtrack_1.png").convert_alpha()
soundtrack2_img = image.load("button_image/button_soundtrack_2.png").convert_alpha()
soundtrack3_img = image.load("button_image/button_soundtrack_3.png").convert_alpha()
back_img = image.load("button_image/button_back.png").convert_alpha()
rules_img = image.load("button_image/button_rules.png")
main_menu_img = image.load("button_image/button_main_menu.png")
sound_on_img = image.load("button_image/button_sound_on.bmp")
sound_off_img = image.load("button_image/button_sound_off.bmp")
# create button instances
start_button = button.Button(55, 375, start_img, 1)
resume_button = button.Button(55, 575, resume_img, 1)
audio_button = button.Button(55, 475, audio_img, 1)
quit_button = button.Button(55, 675, quit_img, 1)
soundtrack1_button = button.Button(55, 375, soundtrack1_img, 1)
soundtrack2_button = button.Button(55, 475, soundtrack2_img, 1)
soundtrack3_button = button.Button(55, 575, soundtrack3_img, 1)
back_button = button.Button(200, 675, back_img, 1)
rules_button = button.Button(55, 575, rules_img, 1)
main_menu_button = button.Button(200, 675, main_menu_img, 1)
sound_on_button = button.Button(1140, 2, sound_on_img, 1)
sound_off_button = button.Button(1140, 2, sound_off_img, 1)
# create and delete characters
character_data = ({'path': 'eleven.bmp', 'score': 30, 'action': 'nothing'},
                  {'path': 'steve2.bmp', 'score': 15, 'action': 'nothing'},
                  {'path': 'dustin.bmp', 'score': 20, 'action': 'nothing'},
                  {'path': 'hopper.bmp', 'score': 10, 'action': 'nothing'},
                  {'path': 'demogorgan.bmp', 'score': 40, 'action': 'damage'},
                  {'path': 'demogorgan2.bmp', 'score': 40, 'action': 'damage'},
                  {'path': 'vecna.bmp', 'score': 0, 'action': 'game_over'})
characters_surf = [image.load('images/' + data['path']).convert_alpha() for data in character_data]


def create_character(group):
    index = randint(0, len(characters_surf) - 1)
    width_of_use = randint(50, WIDTH - 50)
    speed = randint(speed_min, speed_max)
    return Character(width_of_use, speed, characters_surf[index], character_data[index]['score'],
                     character_data[index]['action'], group)


characters = sprite.Group()
create_character(characters)


def delete_character():
    for character in characters:
        character.kill()


# define collision


def collide_characters():
    global game_score, game_start, menu_state, running, life
    for character in characters:
        if portal_rect.collidepoint(character.rect.center):
            if character.action == "game_over":
                v_catch.play()
                v_catch.set_volume(0.4)
                draw.rect(screen, WHITE, (200, 450, 800, 100), width=2, border_radius=10)
                draw_text("Ehh, unfortunately you lost. Your score:", LEELAWADEE_40, WHITE, 345, 455)
                draw_text(f"{game_score} points", ARIAL_BLACK_25, WHITE, 540, 500)
                display.flip()
                time.wait(3000)
                game_start, running = False, False
                menu_state = "main"
                character.kill()
            elif character.action == "damage":
                d_catch.play()
                d_catch.set_volume(0.2)
                screen.fill(RED)
                game_score -= character.score
                character.kill()
                life -= 1
                if life == 0:
                    screen.blit(game_background, (0, 0))
                    draw.rect(screen, WHITE, (200, 450, 800, 100), width=2, border_radius=10)
                    draw_text("Ehh, unfortunately you lost. Your score:", LEELAWADEE_40, WHITE, 345, 455)
                    draw_text(f"{game_score} points", ARIAL_BLACK_25, WHITE, 540, 500)
                    display.flip()
                    time.wait(3000)
                    game_start, running = False, False
            else:
                c_catch.play()
                c_catch.set_volume(0.1)
                game_score += character.score
                character.kill()


def draw_text(text, font_name, text_color, x, y):
    img = font_name.render(text, True, text_color)
    screen.blit(img, (x, y))


def frequency_change():
    global frequency
    if game_score <= 100: frequency = 1000
    if 100 < game_score <= 300: frequency = 800
    elif 300 < game_score <= 700: frequency = 600
    elif 700 < game_score <= 1500: frequency = 400
    elif 1500 < game_score <= 2500: frequency = 300
    elif 2500 < game_score <= 5000: frequency = 300
    elif game_score > 5000: frequency = 300
    return time.set_timer(USEREVENT, frequency)


while game:
    if menu_state != "resume":
        mixer.music.load('songs/song_for_menu.mp3')
        mixer.music.play(-1)

    menu, game_start = True, False
    while menu:
        screen.blit(menu_background, (0, 0))
        draw_text(f"Soundtrack: {song_for_the_game[6:-4]}",
                  ARIAL_BLACK_18, WHITE, WIDTH - (len(song_for_the_game[6:-4]) - 12) - 320, HEIGHT - 25)
        screen.blit(area_for_score, (930, -350))

        try:
            adjustable_height = 40
            draw_text(f"Last score", ARIAL_BLACK_18, WHITE, 1008, adjustable_height)
            for line in range(len(history_of_scores)):
                if line < 5:
                    adjustable_height = adjustable_height + 30
                    draw_text(f"{line + 1}:  {history_of_scores[line]} points",
                              ARIAL_BLACK_18, WHITE, 960, adjustable_height)
                    draw.line(screen, WHITE, (960, adjustable_height), (1155, adjustable_height), 2)
        except IndexError:
            pass

        for event in pygame.event.get():
            if event.type == QUIT:
                menu, game = False, False
        if menu_state == "main":
            if start_button.draw(screen):
                game_start, menu = True, False
            if audio_button.draw(screen):
                menu_state = "audio"
            if rules_button.draw(screen):
                menu_state = "rules"
            if back_button.draw(screen):
                pass
            if quit_button.draw(screen):
                menu, game = False, False
        if menu_state == "audio":
            if soundtrack1_button.draw(screen):
                song_for_the_game = 'songs/Running Up That Hill.mp3'
            if soundtrack2_button.draw(screen):
                song_for_the_game = "songs/Kids - Kyle Dixon.mp3"
            if soundtrack3_button.draw(screen):
                song_for_the_game = "songs/California Dreamin'.mp3"
            if back_button.draw(screen):
                menu_state = "main"
            if quit_button.draw(screen):
                menu, game = False, False
        if menu_state == "resume":
            if resume_button.draw(screen):
                game_start, menu = True, False
            if main_menu_button.draw(screen):
                game_start, menu = False, False
                menu_state = "main"
            if quit_button.draw(screen):
                menu, game = False, False
        if menu_state == "rules":
            screen.blit(area_for_rules, (-5, 255))
            screen.blit(eleven, (150, 490)) and screen.blit(dustin, (485, 565))
            screen.blit(steve, (150, 560)) and screen.blit(hopper, (470, 500))
            screen.blit(demogorgan, (770, 500)) and screen.blit(demogorgan2, (810, 493))
            screen.blit(vecna, (810, 560))
            if back_button.draw(screen):
                menu_state = "main"
            if quit_button.draw(screen):
                menu, game = False, False
        display.update()

    if game_start == True and menu_state == "resume":
        mixer.music.unpause()
    elif game_start == True and menu_state == "main":
        mixer.music.load(song_for_the_game)
        mixer.music.play(-1)

    sound_on_off = 0
    while game_start:
        frequency_change()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_start, running, game = False, False, False
                elif event.type == USEREVENT:
                    create_character(characters)

            while sound_on_off == 0:
                if sound_on_button.draw(game_background):
                    mixer.music.pause()
                    sound_on_off = 1
                else:
                    break
            while sound_on_off == 1:
                if sound_off_button.draw(game_background):
                    mixer.music.unpause()
                    sound_on_off = 0
                else:
                    break

            keys = key.get_pressed()
            if keys[K_LEFT]:
                portal_rect.x -= speed_portal
                if portal_rect.x < 0:
                    portal_rect.x = 0
            elif keys[K_RIGHT]:
                portal_rect.x += speed_portal
                if portal_rect.x > WIDTH - portal_rect.width:
                    portal_rect.x = WIDTH - portal_rect.width
            elif keys[K_ESCAPE]:
                mixer.music.pause()
                running, game_start = False, False
                menu_state = "resume"

            screen.blit(game_background, (0, 0))
            screen.blit(score_image, (0, 0))

            adjustable_width = -5
            for i in range(life):
                screen.blit(life_image, (adjustable_width, 65))
                adjustable_width += 40

            screen_text = ARIAL_BLACK_25.render(str(game_score), True, WHITE)
            screen.blit(screen_text, (10, 20))
            characters.update(HEIGHT)
            collide_characters()
            characters.draw(screen)
            screen.blit(portal, portal_rect)
            display.update()
            clock.tick(FPS)
            characters.update(HEIGHT)

            if 100 < game_score <= 300:
                while level == 1:
                    speed_min, speed_max, speed_portal = 1, 3, 10
                    running, level = False, 2
            elif 300 < game_score <= 700:
                while level == 2:
                    speed_min, speed_max, speed_portal = 1, 4, 11
                    running, level = False, 3
            elif 700 < game_score <= 1500:
                while level == 3:
                    speed_min, speed_max, speed_portal = 1, 5, 15
                    running, level = False, 4
            elif 1500 < game_score < 2500:
                while level == 4:
                    speed_min, speed_max, speed_portal = 2, 5, 15
                    running, level = False, 5
            elif 2500 < game_score < 5000:
                while level == 5:
                    speed_min, speed_max, speed_portal = 2, 6, 20
                    running, level = False, 6
            elif game_score > 5000:
                while level == 6:
                    speed_min, speed_max, speed_portal = 3, 6, 20
                    running, level = False, 7
    if menu_state == "main":
        history_of_scores.insert(0, game_score)
        delete_character()
        game_score, life, level = 0, 3, 0
        speed_min, speed_max, speed_portal = 1, 2, 8
quit()
