# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 10:35:55 2020

@author: Marcus
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import Vec4, Vec3

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        properties = WindowProperties()
        properties.setSize(1000, 500)
        self.win.requestProperties(properties)
        
        self.environment = loader.loadModel("Models/Environment/ground.bam")
        self.environment.reparentTo(render)

        self.camera.setPos(0, 0, 5)
        self.camera.setP(-30)
        
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
        self.accept("mouse1", self.updateKeyMap, ["jump", True])
        self.accept("mouse1-up", self.updateKeyMap, ["jump", False])
        
        self.updateTask = taskMgr.add(self.update, "update")
    
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
    
    def update(self, task):
        dt = globalClock.getDt()

        if self.keyMap["up"]:
            self.camera.setPos(self.camera.getPos() + Vec3(0, 5.0*dt, 0))
        if self.keyMap["down"]:
            self.camera.setPos(self.camera.getPos() + Vec3(0, -5.0*dt, 0))
        if self.keyMap["left"]:
            self.camera.setPos(self.camera.getPos() + Vec3(-5.0*dt, 0, 0))
        if self.keyMap["right"]:
            self.camera.setPos(self.camera.getPos() + Vec3(5.0*dt, 0, 0))
        if self.keyMap["jump"]:
            print ("jump!")

        return task.cont

game = Game()
game.run()