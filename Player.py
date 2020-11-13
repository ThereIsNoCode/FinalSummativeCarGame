import pygame as py


class Player:
    def __init__(self, carBody, carFront, carBack, maxLaps,posX, posY):
        #Sets cars body, front and back to rotate them
        self.carBodyImg = carBody
        self.carFrontImg = carFront
        self.carBackImg = carBack

        #Relates to the movement of car
        self.position = py.Vector2(posX, posY)
        self.velocity = py.Vector2(0, 0)
        self.steerSpeed = 0.0
        self.angle = 0.0

        #Position of player rect
        self.rect = py.Rect
        self.rectPos =  py.Vector2(0,0)


        self.maxLaps = maxLaps
        self.laps = 0

        self.hitCheckpoint = False

    def Moving(self):  # Movement of Car
        keys = py.key.get_pressed()

        # Adds velocity to Y-Axis
        if keys[py.K_RSHIFT] == False:
            if keys[py.K_w]: #Forward
                if self.velocity.y < 10:
                    self.velocity.y += 0.2
                else:
                    self.velocity.y = 10

            else: #Loose forward velocity
                if self.velocity.y > 0:
                    self.velocity.y -= 0.1
                    if self.velocity.y < 0:
                        self.velocity.y = 0

            if keys[py.K_s]: #Backward
                if self.velocity.y > -5:
                    self.velocity.y -= 0.2
                else:
                    self.velocity.y = -5
            else: #loose backward velocity
                if self.velocity.y < 0:
                    self.velocity.y += 0.1
                    if self.velocity.y > 0:
                        self.velocity.y = 0

        else: #slow down car using breaks
            if self.velocity.y > 0:
                self.velocity.y -= 0.2
                if self.velocity.y < 0:
                    self.velocity.y = 0
            if self.velocity.y < 0:
                self.velocity.y += 0.2
                if self.velocity.y > 0:
                    self.velocity.y = 0

        x = round(self.velocity.y, 1)

        if x <= 0.1 and x > 0:
            self.velocity = py.Vector2(0,0)




        # Adds speed to turning
        if self.velocity.y != 0:
            #Adds steering speed to the left
            if keys[py.K_a]:
                if self.steerSpeed < 2:
                    self.steerSpeed += 0.1
                else:
                    self.steerSpeed = 2
            else: #decrease steering speed to the left
                if self.steerSpeed > 0:
                    self.steerSpeed -= 0.1
                    if self.steerSpeed < 0:
                        self.steerSpeed = 0

            #Adds steering speed to the right
            if keys[py.K_d]:
                if self.steerSpeed > -2:
                    self.steerSpeed -= 0.1
                else:
                    self.steerSpeed = -2
            else: #decrease steering speed to the right
                if self.steerSpeed < 0:
                    self.steerSpeed += 0.1
                    if self.steerSpeed > 0:
                        self.steerSpeed = 0
        else: #car speed is zero, therefore steering speed is 0
            self.steerSpeed = 0

        self.angle += self.steerSpeed


    def Draw(self,screen):  # Draws Car onto screen
        center = self.carBodyImg.get_rect().center

        #Rotates Car parts
        rotatedCar = py.transform.rotate(self.carBodyImg, self.angle)
        rotatedBack = py.transform.rotate(self.carBackImg, self.angle)
        rotatedFront = py.transform.rotate(self.carFrontImg, self.angle)

        #Rotates on center
        self.rect = rotatedCar.get_rect(center=center)
        self.rect = self.rect.move(self.position.x, self.position.y)

        self.rectPos = py.Vector2(self.rect.left, self.rect.top)

        #Updats car masks to fit with rotation
        carBackMask = py.mask.from_surface(rotatedBack)
        carFrontMask = py.mask.from_surface(rotatedFront)

        #Displays Car
        screen.blit(rotatedCar, self.rect)
        screen.blit(rotatedBack, self.rect)
        screen.blit(rotatedFront, self.rect)

        return carBackMask, carFrontMask
