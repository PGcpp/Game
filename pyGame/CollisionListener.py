import Box2D
from Box2D import *

class CollisionListener(b2ContactListener):

    world = None

    def __init__(self, world):
        self.world = world
        b2ContactListener.__init__(self)

    def BeginContact(self, contact):
        userDataA = contact.fixtureA.body.userData
        userDataB = contact.fixtureB.body.userData

        if userDataA != None and userDataB != None:
            if (userDataA[0] == "bullet" or userDataA[0] == "ground") and (userDataB[0] == "bullet" or userDataB[0] == "ground"):
                print "hit!"
                """
                if userDataA[0] == "bullet":
                    self.world.DestroyBody(contact.fixtureA.body)
                else:
                    self.world.DestroyBody(contact.fixtureA.body)
"""
    def EndContact(self, contact):
        pass

    def PreSolve(self, contact, oldManifold):
        pass

    def PostSolve(self, contact, impulse):
        pass
