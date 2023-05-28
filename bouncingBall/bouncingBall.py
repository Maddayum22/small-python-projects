from random import randint
from turtle import speed
import pygame as py 

py.init()

# Colors #
background = (93, 112, 127)
ballColor = (102, 206, 214)

# Display #

gameScreen = py.display.set_mode((0,0), py.FULLSCREEN)
py.display.set_caption('Bouncing Ball')

# Ball Info #
ballSize = 20
ballX = randint(ballSize, (gameScreen.get_width() - ballSize))
ballY = randint(ballSize, (gameScreen.get_height() - ballSize))
speedY = randint(1, 4)
speedX = randint(1, 3)
bounciness = 0.9

# Game Loop #
clock = py.time.Clock()
running = True

while running:
    gameScreen.fill(background)

    speedY += 0.5

    ballX += speedX

    # Ball Movement #
    if ballY <= gameScreen.get_height() - ballSize:
        ballY += speedY
    
    else:
        ballY = gameScreen.get_height() - ballSize
        speedY = -speedY * bounciness

    if  ballX > gameScreen.get_width() - ballSize:
        speedX = -speedX * bounciness

    elif ballX < 0 - ballSize:
        speedX = speedX * bounciness

    ball = py.draw.circle(gameScreen, ballColor, (ballX, ballY), ballSize, 0)

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                running = False
    py.display.update()
    clock.tick(60)

py.quit()
quit()