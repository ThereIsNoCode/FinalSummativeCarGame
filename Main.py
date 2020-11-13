import pygame as py
from Player import Player
from Map import Map

py.init()
WIDTH, HEIGHT = 1200, 900
screen = py.display.set_mode((WIDTH, HEIGHT))  # Initiallizes screen
py.display.set_caption("Car game, by Shaya Jabbarzadeh")

# Keeps the Game running smooth
clock = py.time.Clock()
ticks = 60
curElapsedTime = py.time.get_ticks()

# Gets required Car Images and mask
carBody = py.image.load('Car.png').convert_alpha()
carBack = py.image.load('CarBack.png').convert_alpha()
carFront = py.image.load('CarFront.png').convert_alpha()
carBackMask = py.mask.from_surface(carBack)
carFrontMask = py.mask.from_surface(carFront)

#Gets required Map Images and mask
mapImg = py.image.load('Map.png').convert_alpha()
mapStartLineImg = py.image.load('MapStartingLine.png').convert_alpha()
mapCheckpointImg = py.image.load('MapCheckPoint1.png').convert_alpha()

mapMask = py.mask.from_surface(mapImg)
checkpointMask = py.mask.from_surface(mapCheckpointImg)
startingLineMask = py.mask.from_surface(mapStartLineImg)

#game UI
#Note: this repeats for the rest of text
gameFont = py.font.Font('freesansbold.ttf', 32) #Gets the font and font size for text

timerTxt = gameFont.render('Time: ', True, (0,0,0))#Sets Text
timerRect = timerTxt.get_rect()
timerRect.center = ((WIDTH / 2), (HEIGHT / 2) - 380) #sets position of text

lapCountTxt = gameFont.render('Lap: x/y ', True, (0,0,0))
lapCountTxtRect = lapCountTxt.get_rect()
lapCountTxtRect.center = ((WIDTH / 2)+ 250, (HEIGHT / 2) - 380)

#Main Menu UI
menuFont = py.font.Font('freesansbold.ttf', 50)
titleTxt = menuFont.render('Car Game ', True, (0,0,0))
titleTxtRect = titleTxt.get_rect()
titleTxtRect.center = (WIDTH/2, HEIGHT/2 + - 150)

playTxt = menuFont.render('Play', True, (0,0,0))
playTxtRect = playTxt.get_rect()
playTxtRect.center = (WIDTH/2, HEIGHT/2)

scoreTxt = menuFont.render('Fastest Time: ', True, (0,0,0))
scoreRect = scoreTxt.get_rect()
scoreRect.center = (WIDTH/2 -100, (HEIGHT/2) + 100)

#UI Buttons
playButton = py.Rect(0,0, 500,100) #
playButton.center = (WIDTH/2,HEIGHT/2) #centers the playButton


currentHighScore = "0"

#Gets current highscore from text file
f = open("score.txt", "r")
currentHighScore = f.read() #Loads in score
f.close()

def CheckScore(endTime): #Checks if current time is faster than the highscore
    global currentHighScore

    if  not currentHighScore  or endTime < float(currentHighScore):
        currentHighScore = str(endTime)
        f = open("score.txt", "w")
        f.write(str(currentHighScore))
        f.close()

def DrawMenu():#Draws the main menu
    py.draw.rect(screen, (87,168,126), playButton) #Draws button rect

    screen.blit(titleTxt, titleTxtRect) #draws text
    screen.blit(playTxt,playTxtRect)
    scoreTxt = menuFont.render(f'Highscore: {currentHighScore} Seconds', True, (0,0,0))
    screen.blit(scoreTxt, scoreRect)


# Creates objects
player = Player(carBody,carFront,carBack, 3, WIDTH/2, HEIGHT/2)
_map = Map(mapImg,mapStartLineImg, 0, -600)

isRun = True
isMenu = True #If we are in the main menu


while isRun:  # Main loop
    for event in py.event.get():
        if event.type == py.QUIT:
            isRun = False
        if event.type == py.MOUSEBUTTONDOWN:
            if isMenu == True: #When mouse is down, check if player clicked on "Play" button
                mousePos = py.mouse.get_pos()
                result = playButton.collidepoint(mousePos[0], mousePos[1])
                if result: #Finds if user clicked on play
                    curElapsedTime = py.time.get_ticks()
                    isMenu = False


    screen.fill((221, 221, 222))  # Screen white
    if isMenu == True: #Displays Main menu
        DrawMenu()
    else: #Displays Game

        player.Moving() #Gets user input to move

        _map.CheckCollision(player,carFrontMask, carBackMask, mapMask, checkpointMask, startingLineMask) #Checks for collision using the following Mask

        _map.Draw(screen)  #draws map onto screen
        carBackMask, carFrontMask = player.Draw(screen)  #Draws and updates the mask colliders with rotated version of image

        #Sets and displays UI in-game
        timerTxt = gameFont.render(f'Time: {(py.time.get_ticks() - curElapsedTime)/1000}', True, (0,0,0))
        lapCountTxt = gameFont.render(f'Lap: {player.laps + 1}/{player.maxLaps}', True, (0,0,0))

        screen.blit(timerTxt, timerRect)
        screen.blit(lapCountTxt, lapCountTxtRect)

        if player.laps == player.maxLaps: #when laps reach max laps, reset player and map values and return to menu
            endTime = (py.time.get_ticks() - curElapsedTime )/1000
            scoreBeaten = CheckScore(endTime)

            _map.position = py.Vector2(0,-600)
            player.velocity = py.Vector2(0,0)
            player.angle = 0
            player.laps = 0
            isMenu = True

    py.display.update() #Refreshes screen

    clock.tick(ticks)#Holds game at 60 frames or less
