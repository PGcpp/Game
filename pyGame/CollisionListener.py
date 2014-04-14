import Box2D
from Box2D import *

class CollisionListener(b2ContactListener):

    def CollisionListener(self):
        ContactListener.__init__(self)

    def BeginContact(self, contact):
        userDataA = contact.fixtureA.body.userData
        userDataB = contact.fixtureB.body.userData

        if userDataA != None and userDataB != None:
            if (userDataA[0] == "arrow" or userDataA[0] == "viking") and (userDataB[0] == "arrow" or userDataB[0] == "viking"):
                print "hit!"

    def EndContact(self, contact):
        pass

    def PreSolve(self, contact, oldManifold):
        pass

    def PostSolve(self, contact, impulse):
        pass
