import Box2D
from Box2D import *

class CollisionListener(b2ContactListener):

    bodiesToDestroy = [None, None, None, None, None, None, None, None, None, None]
    count = 0

    def __init__(self):
        b2ContactListener.__init__(self)

    def BeginContact(self, contact):
        userDataA = contact.fixtureA.body.userData
        userDataB = contact.fixtureB.body.userData

        if userDataA != None and userDataB != None:
            if (userDataA[0] == "bulletShooted" and userDataB[0] == "ground") or (userDataA[0] == "ground" and userDataB[0] == "bulletShooted"):
                if userDataA[0] == "bulletShooted":
                    self.bodiesToDestroy[self.count] = contact.fixtureA.body
                else:
                    self.bodiesToDestroy[self.count] = contact.fixtureB.body
                self.count += 1
            elif (userDataA[0] == "bulletShooted" and userDataB[0] == "viking") or (userDataA[0] == "viking" and userDataB[0] == "bulletShooted"):
                self.bodiesToDestroy[self.count] = contact.fixtureA.body
                self.bodiesToDestroy[self.count + 1] = contact.fixtureB.body
                self.count += 2

        userDataA = None
        userDataB = None

    def bulletMiss(self, userDataA, userDataB):
        pass        

    def EndContact(self, contact):
        pass

    def PreSolve(self, contact, oldManifold):
        pass

    def PostSolve(self, contact, impulse):
        pass
