import Box2D
from Box2D import *

class CollisionListener(b2ContactListener):

    bodyToDestroy = None

    def __init__(self):
        b2ContactListener.__init__(self)

    def BeginContact(self, contact):
        userDataA = contact.fixtureA.body.userData
        userDataB = contact.fixtureB.body.userData

        if userDataA != None and userDataB != None:
            if (userDataA[0] == "bulletShooted" or userDataA[0] == "ground") and (userDataB[0] == "bulletShooted" or userDataB[0] == "ground"):
                print "hit!"

                if userDataA[0] == "bulletShooted":
                    self.bodyToDestroy = contact.fixtureA.body
                else:
                    self.bodyToDestroy = contact.fixtureB.body
        userDataA = None
        userDataB = None

    def EndContact(self, contact):
        pass

    def PreSolve(self, contact, oldManifold):
        pass

    def PostSolve(self, contact, impulse):
        pass
