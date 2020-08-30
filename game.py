# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 10:35:55 2020

@author: Marcus
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import Vec4, Vec3

import sys

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        properties = WindowProperties()
        properties.setSize(1000, 500)
        self.win.requestProperties(properties)
        
        self.environment = loader.loadModel("Models/Environment/ground.bam")
        self.environment.reparentTo(render)
        
        self.initializeKeyMap()
        self.initializePlayer()

        self.camera.setPos(0, 0, 5)
        self.camera.setP(-30)
                
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
        self.gravity = 10.0
        self.jumpStrength = 5.0
        self.playerXYSpeed = 5.0
        self.playerZSpeed = 0.0
        self.playerIsGrounded = True

    # ============================================
    #
    #          Update Helper Functions
    #
    # ============================================
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
    
    def update(self, task):
        dt = globalClock.getDt()
        s = self.playerXYSpeed

        if self.keyMap["up"]:
            self.camera.setPos(self.camera.getPos() + Vec3(0, s*dt, 0))
        if self.keyMap["down"]:
            self.camera.setPos(self.camera.getPos() + Vec3(0, -s*dt, 0))
        if self.keyMap["left"]:
            self.camera.setPos(self.camera.getPos() + Vec3(-s*dt, 0, 0))
        if self.keyMap["right"]:
            self.camera.setPos(self.camera.getPos() + Vec3(s*dt, 0, 0))
        if self.keyMap["jump"]:
            self.tryToJump()
        
        if not self.playerIsGrounded:
            self.camera.setPos(self.camera.getPos() + Vec3(0, 0, self.playerZSpeed*dt))
            self.playerZSpeed -= self.gravity*dt
            if self.camera.getPos().z < self.playerHeight/2:
                self.playerIsGrounded = True
                self.playerZSpeed = 0.0
                self.camera.setPos(self.camera.getPos().x, self.camera.getPos().y, self.playerHeight/2)

        return task.cont
    
    def tryToJump(self):
        if self.playerIsGrounded:
            self.playerZSpeed = self.jumpStrength
            self.playerIsGrounded = False
    
    def quit(self):
        #self.cleanup()
        base.userExit()


game = Game()
game.run()