import pygame
import sys
import random

from pygame.locals import *

#Executable functions
#Ball moving animations
def ballAnimation():
    global ballSpeed_x, ballSpeed_y, playerScore, opponentScore, scoreTime

    ball.x += ballSpeed_x
    ball.y += ballSpeed_y

    #Bouncy walls
    if ball.top <= 0 or ball.bottom >= screenHeight:
        ballSpeed_y *= -1

    #Player score
    if ball.left <= 0:
        scoreTime = pygame.time.get_ticks()
        playerScore += 1

    # Opponent score
    if ball.left <= 0:
        scoreTime = pygame.time.get_ticks()
        opponentScore += 1

    #When ball collides witht the top or bottom of the player bars
    if ball.colliderect(player) and ballSpeed_x > 0:
        if abs(ball.right - player.left) < 10:
            ballSpeed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ballSpeed_y > 0:
            ballSpeed_y *= -1
        elif abs(ball.top- player.bottom) < 10 and ballSpeed_y < 0:
            ballSpeed_y *= -1

    #When ball collides witht the top or bottom of the opponent bars
    if ball.colliderect(opponent) and ballSpeed_x > 0:
        if abs(ball.right - opponent.left) < 10:
            ballSpeed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ballSpeed_y > 0:
            ballSpeed_y *= -1
        elif abs(ball.top- opponent.bottom) < 10 and ballSpeed_y < 0:
            ballSpeed_y *= -1

#Player movement restrictions so that the bars dont go beyond the window
def playerAnimation():
    player.y += playerSpeed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screenHeight:
        player.bottom = screenHeight

#Opponent or computer movements, restrictions to not let bars go beyond window
#and to move to block the ball
def opponentAnimations():
    #computer movements
    if opponent.top < ball.y:
        opponent.y += opponentSpeed
    if opponent.bottom > ball.y:
        opponent.y -= opponentSpeed

    #bar restrictions
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screenHeight:
        opponent.bottom = screenHeight

#Ball position when game starts
def ballStart():
    global ballSpeed_x, ballSpeed_y, ballMoving, scoreTime

    #place ball in the center and to get current time to calculate timer
    ball.center = (screenWidth/2, screenHeight/2)
    currentTime = pygame.time.get_ticks()

    #countdown timer before the ball starts moving
    if currentTime - scoreTime < 700:
        numberThree = font.render("3", False, lightGrey)
        screen.blit(numberThree, (screenWidth/2 - 10, screenHeight/2 +20))
    
    if 700 < currentTime - scoreTime < 1400:
        numberTwo = font.render("3", False, lightGrey)
        screen.blit(numberTwo, (screenWidth/2 - 10, screenHeight/2 +20))

    if 1400 < currentTime - scoreTime < 2100:
        numberOne = font.render("3", False, lightGrey)
        screen.blit(numberOne, (screenWidth/2 - 10, screenHeight/2 +20))

    #Ball moves in random when timer runs down
    if currentTime - scoreTime < 2100:
        ballSpeed_y, ballSpeed_x = 0,0
    else:
        ballSpeed_x = 7*random.choice((-1,1))
        ballSpeed_y = 7*random.choice((-1,1))
        scoreTime = None

#Setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

#Main Window
screenWidth = 1280
screenHeight = 960
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("PingPong")

#Colors
lightGrey = (200,200,200)
backgroundColor = pygame.Color("grey12")

#Game elements
player = pygame.Rect(screenWidth - 20, screenHeight/2 - 70, 10, 140)
opponent = pygame.Rect(10, screenHeight/2 - 70, 10, 140)
ball = pygame.Rect(screenWidth/2 - 10, screenHeight/2 -10, 20, 20)

#Variables
ballSpeed_x = 7 * random.choice((1,-1))
ballSpeed_y = 7 * random.choice((1,-1))
playerSpeed = 0
opponentSpeed = 7 
ballMoving = False
scoreTime = True

#Score text
playerScore = 0
opponentScore = 0
font =pygame.font.SysFont("FreeSans.ttf", 30)

#Sound


#Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerSpeed -= 6
            if event.key == pygame.K_DOWN:
                playerSpeed += 6 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                playerSpeed += 6
            if event.key == pygame.K_DOWN:
                playerSpeed -= 6
        
    #Game executables
    ballAnimation()
    playerAnimation()
    opponentAnimations()

    #Visuals
    screen.fill(backgroundColor)
    pygame.draw.rect(screen, lightGrey, player)
    pygame.draw.rect(screen, lightGrey, opponent)
    pygame.draw.ellipse(screen, lightGrey, ball)
    pygame.draw.aaline(screen, lightGrey, (screenWidth/2, 0), (screenWidth/2, screenHeight))

    if scoreTime:
        ballStart()

    playerText = font.render(f'{playerScore}', False, lightGrey)
    screen.blit(playerText,(600,470))

    opponentText = font.render(f'{opponentScore}', False, lightGrey)
    screen.blit(opponentText,(600,470))

    pygame.display.flip()
    clock.tick(60)
