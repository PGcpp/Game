import Box2D
from Box2D import *
from Enum import *

class CollisionListener(b2ContactListener):

    def __init__(self):
        b2ContactListener.__init__(self)

    def BeginContact(self, contact):
        userDataA = contact.fixtureA.body.userData
        userDataB = contact.fixtureB.body.userData

        if userDataA != None and userDataB != None:
            if (userDataA[0] == BULLET.NOT_HIT and userDataB[0] == VIKING.NOT_HIT):
                contact.fixtureA.body.userData[0] = BULLET.HIT
                contact.fixtureB.body.userData[0] = VIKING.HIT
                contact.fixtureB.body.userData.append(userDataA[2])
                
            elif (userDataA[0] == VIKING.NOT_HIT and userDataB[0] == BULLET.NOT_HIT):
                contact.fixtureA.body.userData[0] = VIKING.HIT
                contact.fixtureB.body.userData[0] = BULLET.HIT
                contact.fixtureA.body.userData.append(userDataB[2])

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
