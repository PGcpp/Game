import Box2D
from Box2D import *

class CollisionListener(b2ContactListener):

    def CollisionListener(self):
        ContactListener.__init__(self)

    def BeginContact(self, contact):
        userData = contact.fixtureA.body.userData
        if userData != None:
        	print "viking hitting!"

        userData = contact.fixtureB.body.userData
        if userData != None:
        	print "viking hitting!"

    def EndContact(self, contact):
        pass

    def PreSolve(self, contact, oldManifold):
        pass

    def PostSolve(self, contact, impulse):
        pass
