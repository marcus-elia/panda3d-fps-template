# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 10:35:55 2020

@author: Marcus
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import Vec4, Vec3

from panda3d.core import LineSegs
from panda3d.core import NodePath

from math import atan2, pi, cos, sin, sqrt

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()
        self.windowWidth = 1000
        self.windowHeight = 500

        properties = WindowProperties()
        properties.setSize(self.windowWidth, self.windowHeight)
        self.win.requestProperties(properties)
        
        self.tileSize = 20
        for i in range(-3, 4):
            for j in range(-3, 4):
                grassTile = loader.loadModel("Models/Environment/ground.bam")
                grassTile.setX(self.tileSize*i)
                grassTile.setY(self.tileSize*j)
                grassTile.reparentTo(render)
        
        self.initializeKeyMap()
        self.initializePlayer()
        self.initializeMouse()

        self.camera.setPos(0, 0, 5)
        self.camera.setH(self.playerXYAngle*180/pi)
        self.camera.setP(self.playerZAngle*180/pi)
                
        self.frameNumber = 0
        self.updateTask = taskMgr.add(self.update, "update")
    
    # ============================================
    #
    #      Initialization Helper Functions
    #
    # ============================================
    def initializeKeyMap(self):
        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "jump" : False
        }
        
        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("space", self.updateKeyMap, ["jump", True])
        self.accept("space-up", self.updateKeyMap, ["jump", False])
        self.accept("escape", self.quit)
    
    def initializePlayer(self):
        self.playerHeight = 10
        self.playerLocation = Vec3(0, 0, 5)
        self.gravity = 10.0
        self.jumpStrength = 5.0
        self.playerXYSpeed = 5.0
        self.playerZSpeed = 0.0
        self.playerIsGrounded = True
        self.playerXYAngle = 0
        self.playerZAngle = 0
    
    def initializeMouse(self):
        # To set relative mode and hide the cursor:
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(props)
        self.mouseSensitivity = 0.01
        base.win.movePointer(0, 500, 250)

    # ============================================
    #
    #          Update Helper Functions
    #
    # ============================================
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
    
    def update(self, task):
        dt = globalClock.getDt()
        self.frameNumber += 1
        
        self.movePlayer(dt)
        self.reactToMouseMotion()

        return task.cont
    
    def movePlayer(self, dt):
        s = self.playerXYSpeed

        # Move the player in response to key inputs
        if self.keyMap["up"]:
            self.playerLocation.x -= sin(self.playerXYAngle)*s*dt
            self.playerLocation.y += cos(self.playerXYAngle)*s*dt
        if self.keyMap["down"]:
            self.playerLocation.x += sin(self.playerXYAngle)*s*dt
            self.playerLocation.y -= cos(self.playerXYAngle)*s*dt
        if self.keyMap["left"]:
            self.playerLocation.x -= sin(self.playerXYAngle + pi/2)*s*dt
            self.playerLocation.y += cos(self.playerXYAngle + pi/2)*s*dt
        if self.keyMap["right"]:
            self.playerLocation.x += sin(self.playerXYAngle + pi/2)*s*dt
            self.playerLocation.y -= cos(self.playerXYAngle + pi/2)*s*dt
        if self.keyMap["jump"]:
            self.tryToJump()
        
        # Apply gravity to the player
        if not self.playerIsGrounded:
            self.playerLocation.z += self.playerZSpeed*dt
            self.playerZSpeed -= self.gravity*dt
            if self.playerLocation.z < self.playerHeight/2:
                self.playerIsGrounded = True
                self.playerZSpeed = 0.0
                self.playerLocation.z = self.playerHeight/2
                
        # Move the camera to where the player is
        self.camera.setPos(self.playerLocation)
    
    def reactToMouseMotion(self):
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        # fixes stupid bug where the cursor gets moved to 600,200
        # without me moving the mouse
        if self.frameNumber < 3:
            base.win.movePointer(0, 500, 250)
            return
        if y != 250 or x != 500:
            self.playerXYAngle -= (x - 500)*self.mouseSensitivity
            self.playerZAngle -= (y - 250)*self.mouseSensitivity
            self.camera.setH(self.playerXYAngle*180/pi)
            self.camera.setP(self.playerZAngle*180/pi)
            base.win.movePointer(0, 500, 250)
    
    def tryToJump(self):
        if self.playerIsGrounded:
            self.playerZSpeed = self.jumpStrength
            self.playerIsGrounded = False
    
    def quit(self):
        #self.cleanup()
        base.userExit()


game = Game()
game.run()