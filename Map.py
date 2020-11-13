import pygame as py

class Map:  # The current Map
    def __init__(self, mapImg, startLineImg, posX, posY):
        self.position = py.Vector2(posX, posY)

        self.mapImg = mapImg
        self.startLineImg = startLineImg

    def CheckCollision(self, player, carFrontMask, carBackMask, mapMask, checkpointMask, startingLineMask): # position of map depends on screen render
        offset = (int(self.position.x - player.rectPos.x), int(self.position.y - player.rectPos.y))

        #Collision results
        frontCol = carFrontMask.overlap(mapMask, offset) #collision from front of car
        backCol = carBackMask.overlap(mapMask,offset) #collision from back of car
        checkpointCol = carFrontMask.overlap(checkpointMask,offset) #collision from checkpoint
        startingLineCol = carFrontMask.overlap(startingLineMask,offset) #collision from startLine

        #Handle Collision results
        if frontCol: #stops speed from going forward
            if player.velocity.y > 0:
                player.velocity.y = 0
                player.steerSpeed = 0
        if backCol: #stops speed from going backward
            if player.velocity.y < 0:
                player.velocity.y = 0
                player.steerSpeed = 0
        if checkpointCol: #enables the lap to be completed
            player.hitCheckpoint = True
        if startingLineCol and player.hitCheckpoint == True: #Adds the lap
            player.laps += 1
            player.hitCheckpoint = False

        self.position += player.velocity.rotate(-player.angle)

    def Draw(self, screen): #Draws on screen
        screen.blit(self.startLineImg,self.position)
        screen.blit(self.mapImg, self.position)

