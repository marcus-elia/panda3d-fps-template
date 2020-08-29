# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 10:35:55 2020

@author: Marcus
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Plane
from panda3d.core import WindowProperties

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

game = Game()
game.run()