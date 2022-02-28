# import pygame module in this program
import random
from random import  randrange
import csv
import pygame
from sys import exit

pygame.init()
window = pygame.display.set_mode((350, 300))
icon = pygame.image.load('radar.ico')
pygame.display.set_icon(icon)
artefatcs = []
with open('artefacts.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        n_row = []
        for x,val in enumerate(row):
            if x!=0:
                n_row.append(int(row[x]))
        artefatcs.append(n_row)
signals = []

with open('signal.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        n_row = []
        for x,val in enumerate(row):
            if x!=0:
                n_row.append(int(row[x]))
        signals.append(n_row)
run = True
#for x in signal:
#    for y in range(10):
#        signal2.append(x)

#for x, val in enumerate(signal2):
#    total = 0
#    count = 0
#    if x>0:
#        total+=signal2[x-1]
#        count+=1
#    if x<len(signal2)-1:
#        total+=signal2[x+1]
#        count+=1
#    total+=val
#    count += 1
#
#    signal2[x] = int(total/count)

lines = []
clock = pygame.time.Clock()
add_rand = True
signal = 0


artefact_num = 0
artefact_pos = 0
def set_artefact():
    global artefact_pos
    global artefact_num
    artefact_pos = random.randrange(0,300)
    artefact_num = random.randrange(0,len(artefatcs))

set_artefact()
pos = window.get_rect().center
book_signal = 0
book_names = ["UCG-007: Freighter",
              "Byriat-7: Alien Ship",
              "CSS Magnan Oparii: Navy Cruiser",
              "UCG-XX2: Smuggler's Runner",
              "Byriatsko-22: Alien Fighter",
              "Byriatsko-23: Alien Elite Fighter"]
print(signals)
pygame.display.set_caption('Rugnir Sonar Demo')
font = pygame.font.Font(None, 18)

show_result = False
wintext = "Correct!"
losetext = "Wrong :c"
correct = False

font2 = pygame.font.Font(None, 16)
controlhint_text = font2.render("Controls | <: Change artefact | >: Change Signal ", True, (255,255,255))
controlhint_text_rect = controlhint_text.get_rect()
controlhint_text_rect.top=265
controlhint_text_rect.left=25

controlhint_text2 = font2.render("/\: Change Book Entry | \/: Check Answer", True, (255,255,255))
controlhint_text_rect2 = controlhint_text2.get_rect()
controlhint_text_rect2.top=280
controlhint_text_rect2.left=25

while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                add_rand = not add_rand
            if event.key == pygame.K_RIGHT:
                signal = random.randrange(0,len(signals))
                set_artefact()
                show_result = False
            if event.key == pygame.K_UP:
                book_signal += 1
                if book_signal >= len(signals):
                    book_signal = 0
            if event.key == pygame.K_DOWN:
                if book_signal == signal:
                    correct = True
                else:
                    correct = False
                show_result = True
            if event.key == pygame.K_LEFT:
                set_artefact()
        if event.type == pygame.QUIT:
            run = False

    window.fill((0,0,0))

    text = font.render(book_names[book_signal], True, (255,255,255))

    textRect = text.get_rect()

    # set the center of the rectangular object.

    rect = pygame.Rect(pos, (0, 0)).inflate((300, 100))
    pos2 = (pos[0],pos[1]+95)
    rect2 = pygame.Rect(pos2, (0, 0)).inflate((300, 10))
    textRect.top=pos2[1]-25
    textRect.left=25
    window.blit(text, textRect)
    window.blit(controlhint_text, controlhint_text_rect)
    window.blit(controlhint_text2, controlhint_text_rect2)

    if show_result:
        text2 = None
        if correct:
            text2 = font.render(wintext, True, (0,255,0))
        else:
            text2 = font.render(losetext, True, (255,0,0))

        textRect2 = text2.get_rect()
        textRect2.top = 75
        textRect2.left = 25
        window.blit(text2, textRect2)

    pixel_array = pygame.PixelArray(window)
    pixel_array2 = pygame.PixelArray(window)
    thisline = []
    truesig_line = []

    for x in range(rect.width):
        r=0
        g=0
        b=0
        sig = 0
        book_sig=0
        if x>0 and x<len(signals[signal]):
            sig = signals[signal][x]
        if x>0 and x<len(signals[book_signal]):
            book_sig = signals[book_signal][x]

        artefect_sig = 0
        artifact_x = 0
        if x>artefact_pos and x<artefact_pos+len(artefatcs[artefact_num]):
            artifact_x = (x-artefact_pos)
            artefect_sig = artefatcs[artefact_num][artifact_x]

        if add_rand:
            r = (sig+artefect_sig+randrange(-4,4))*15
            g = (sig+artefect_sig+randrange(-4,4))*15-20
            b = (sig+artefect_sig+randrange(-2,2))*15+60-g/2
        else:
            r = (sig+artefect_sig)*15
            g = (sig+artefect_sig)*15-20
            b = (sig+artefect_sig)*15+60-g/2
        if book_sig>4:
            truesig_line.append((255,255,255))
        else:
            truesig_line.append((0,0,0))
        if r>255:
            r=255
        if b>255:
            b=255
        if g>255:
            g=255
        if r<0:
            r=0
        if g<0:
            g=0
        if b<0:
            b=0
        color = (r,g,b)

        thisline.append(color)

    if len(lines)>=rect.height:
        lines.pop(len(lines)-1)
    lines.insert(0,thisline)

    for x, line in enumerate(lines):
        for y, color in enumerate(line):
            pixel_array[rect.left + y, rect.top + x] = color

    pixel_array.close()

    for y, color2 in enumerate(truesig_line):
        pixel_array2[rect2.left + y, rect2.top:rect2.bottom] = color2

    pixel_array2.close()

    pygame.display.flip()

pygame.quit()
exit()
