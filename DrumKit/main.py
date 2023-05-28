from types import TracebackType
import pygame
from pygame import mixer
from pyparsing import White
pygame.init()

scr_width = 1400
scr_height = 800

### COLORS ###
black = (0, 0, 0)
white = (252, 252, 252)
backcolor = (84, 88, 99)
backcolor2 = (66, 69, 78)
backcolor_dark = (46, 49, 58)
active_clr = (84, 155, 94)
high_clr = (149, 147, 217)
orange = (251, 80, 18)
purple = (95, 10, 135)

scr = pygame.display.set_mode([scr_width, scr_height])
pygame.display.set_caption("'Maddy's Beatboi'")

label_font = pygame.font.Font('Roboto-Bold.ttf', 30)
medium_font = pygame.font.Font('Roboto-Bold.ttf', 20)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)
beat_name = ''
typing = False

### Sounds ###
hi_hat = mixer.Sound('sounds\\hi hat.WAV')
snare = mixer.Sound('sounds\\snare.WAV')
kick = mixer.Sound('sounds\\kick.WAV')
crash = mixer.Sound('sounds\\crash.WAV')
clap = mixer.Sound('sounds\\clap.WAV')
tom = mixer.Sound('sounds\\tom.WAV')
pygame.mixer.set_num_channels(instruments * 6)

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()

### Items on Screen ###
def set_grid(clicks, beat, actives):
    left_menu = pygame.draw.rect(scr, backcolor2, [5, 5, 200, scr_height-205], 5)
    bottom_menu = pygame.draw.rect(scr, backcolor2, [5, scr_height-205, scr_width-10, 200], 5)
    boxes = []
    colors = [backcolor2, white, backcolor2]
    hi_hat_text = label_font.render('Hi Hat', True, colors[actives[0]])
    scr.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render('Snare', True, colors[actives[1]])
    scr.blit(snare_text, (30, 130))
    kick_text = label_font.render('Kick', True, colors[actives[2]])
    scr.blit(kick_text, (30, 230))
    crash_text = label_font.render('Crash', True, colors[actives[3]])
    scr.blit(crash_text, (30, 330))
    clap_text = label_font.render('Clap', True, colors[actives[4]])
    scr.blit(clap_text, (30, 430))
    tom_text = label_font.render('Floor Tom', True, colors[actives[5]])
    scr.blit(tom_text, (30, 530))
    for i in range(instruments-1):
        pygame.draw.line(scr, backcolor2, (5, (i*100) + 100), (200, (i*100) + 100), 3)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = backcolor2
            else:
                if actives[j] == 1:
                    color = active_clr
                else:
                    color = backcolor_dark
            rect = pygame.draw.rect(scr, color,[i * ((scr_width - 205) // beats) + 205, (j * 100) + 5, ((scr_width - 200) // beats) - 10,90], 0, 3)
            pygame.draw.rect(scr, high_clr, [i * ((scr_width - 205) // beats) + 200, j * 100, ((scr_width - 200) // beats), 100], 5, 5)
            pygame.draw.rect(scr, purple,[i * ((scr_width - 205) // beats) + 200, j * 100, ((scr_width - 200) // beats), 100], 2, 5)
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(scr, orange, [beat * ((scr_width-205) // beats) + 200, 0, ((scr_width -200) // beats), instruments * 100], 5, 3)
    return boxes

def draw_save_menu(beat_name, typing):
    pygame.draw.rect(scr, backcolor, [0, 0, scr_width, scr_height])
    menu_text = label_font.render('SAVE MENU', True, white)
    saving_btn = pygame.draw.rect(scr, backcolor2, [scr_width // 2 - 200, scr_height * 0.75, 400, 100], 0, 5)
    saving_txt = label_font.render('Save Beat', True, white)
    scr.blit(saving_txt, (scr_width // 2 - 60, scr_height * 0.75 + 30))
    scr.blit(menu_text, (600, 40))
    menu_text2 = label_font.render('Enter a name for Current Beat', True, white)
    scr.blit(menu_text2, (500, 70))
    exit_button = pygame.draw.rect(scr, backcolor2, [scr_width - 200, scr_height - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    scr.blit(exit_text, (scr_width - 150, scr_height - 70))
    if typing:
        pygame.draw.rect(scr, backcolor_dark, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(scr, backcolor2, [400, 200, 600, 200], 5, 5)
    entry_txt = label_font.render(f'{beat_name}', True, white)
    scr.blit(entry_txt, (430, 250))
    return exit_button, saving_btn, entry_rect

def draw_load_menu():
    pygame.draw.rect(scr, backcolor, [0, 0, scr_width, scr_height])
    menu_text = label_font.render('LOAD MENU', True, white)
    loading_btn = pygame.draw.rect(scr, backcolor2, [scr_width // 2 - 200, scr_height * 0.80, 400, 100], 0, 5)
    loading_txt = label_font.render('Load Beat', True, white)
    scr.blit(loading_txt, (scr_width // 2 - 60, scr_height * 0.80 + 30))
    delete_btn  = pygame.draw.rect(scr, backcolor2, [(scr_width//2) - 500, scr_height * 0.80, 200, 100], 0, 5)
    delete_txt =label_font.render('Delete Beat', True, white)
    scr.blit(delete_txt, ((scr_width//2) - 480, scr_height * 0.80 + 30))
    scr.blit(menu_text, (600, 40))
    menu_text2 = label_font.render('Select a Beat', True, white)
    scr.blit(menu_text2, (595, 70))
    exit_button = pygame.draw.rect(scr, backcolor2, [scr_width - 200, scr_height - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    scr.blit(exit_text, (scr_width - 150, scr_height - 70))
    loaded_rect = pygame.draw.rect(scr, backcolor2, [190, 130, 1000, 500], 5, 5)

    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, white)
            scr.blit(row_text, (200, 150 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ') + 6
            name_index_end = saved_beats[beat].index(', beats:')
            name_text = medium_font.render(saved_beats[beat][name_index_start:name_index_end], True, white)
            scr.blit(name_text, (240, 150 + beat * 50))

    return exit_button, loading_btn, delete_btn, loaded_rect

run = True
### Main Gameloop ###
while run:
    timer.tick(fps)
    scr.fill(backcolor)
    
    boxes = set_grid(clicked, active_beat, active_list)

    ### Lower Menu ###
    play_pause = pygame.draw.rect(scr, backcolor2, [50, scr_height - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    scr.blit(play_text, (70, scr_height - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, high_clr)
    else:
        play_text2 = medium_font.render('Paused', True, high_clr)
    scr.blit(play_text2, (70, scr_height - 100))

    ### Bpm ###
    bpm_rect = pygame.draw.rect(scr, backcolor2, [300, scr_height - 150, 200, 100], 0, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    scr.blit(bpm_text, (323, scr_height - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, high_clr)
    scr.blit(bpm_text2, (370, scr_height - 100))
    bpm_add_rect = pygame.draw.rect(scr, backcolor2, [510, scr_height - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(scr, backcolor2, [510, scr_height - 100, 48, 48], 0, 5)
    add_text = medium_font.render('+5', True, white)
    sub_text = medium_font.render('-5', True, white)
    scr.blit(add_text, (523, scr_height - 137))
    scr.blit(sub_text, (523, scr_height - 87))

    ### Beats ###
    beats_rect = pygame.draw.rect(scr, backcolor2, [600, scr_height - 150, 200, 100], 0, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    scr.blit(beats_text, (638, scr_height - 130))
    beats_text2 = label_font.render(f'{beats}', True, high_clr)
    scr.blit(beats_text2, (685, scr_height - 100))
    beats_add_rect = pygame.draw.rect(scr, backcolor2, [810, scr_height - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(scr, backcolor2, [810, scr_height - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render('+1', True, white)
    sub_text2 = medium_font.render('-1', True, white)
    scr.blit(add_text2, (823, scr_height - 137))
    scr.blit(sub_text2, (823, scr_height - 87))

    ### Instruments rects ###
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)

    ### Save and Load ###
    save_button = pygame.draw.rect(scr, backcolor2, [900, scr_height - 150, 200, 48], 0, 5)
    save_text = label_font.render('Save Beat', True, white)
    scr.blit(save_text, (930, scr_height - 145))
    load_button = pygame.draw.rect(scr, backcolor2, [900, scr_height - 100, 200, 48], 0, 5)
    load_text = label_font.render('Load Beat', True, white)
    scr.blit(load_text, (930, scr_height - 95))

    ### Clear Board ###
    clear_button = pygame.draw.rect(scr, backcolor2, [1150, scr_height - 150, 200, 100], 0, 5)
    clear_text = label_font.render('Clear Board', True, white)
    scr.blit(clear_text, (1170, scr_height - 120))

    if save_menu:
        playing = False
        exit_button, saving_btn, entry_rect = draw_save_menu(beat_name, typing)
    if load_menu:
        playing = False
        exit_button, loading_btn, delete_btn, loaded_rect = draw_load_menu()

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True 
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                   clicked[i].append(-1) 
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu - False
                playing = True
                beat_name = ''
                typing = False
            elif entry_rect.collidepoint(event.pos):
                if typing:
                    typing = False
                elif not typing:
                    typing = True
            elif saving_btn.collidepoint(event.pos):
                file = open('saved_beats.txt', 'w')
                saved_beats.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')
                for i in range(len(saved_beats)):
                    file.write(str(saved_beats[i]))
                file.close()
                save_menu = False
                typing = False
                beat_name = ''
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]

    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
pygame.quit()
