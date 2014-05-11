class STATE:
    STOPPED = 1
    RUNNING = 2
    EXIT = 3
    SUSPEND = 4

class MENU:
    PLAY = 10
    OPTIONS = 11

class PARAMS:
    IMAGEPATH = "resources/"

class VIKING:
    TYPE_1 = 20
    TYPE_2 = 21
    TYPE_3 = 22
    #viking state
    NOT_HIT = 23
    HIT = 24
    ATTACK = 25

    TYPE_1 = {
        "ATTACKINTERVAL": 60,
        "DAMAGE": 10,
        "HEALTH": 50,
        "MONEY": 100,
        "SPEED": 3,
        "IMAGE": "viking1.png",
        }
    TYPE_2 = {
        "ATTACKINTERVAL": 60,
        "DAMAGE": 15,
        "HEALTH": 150,
        "MONEY": 200,
        "SPEED": 5,
        "IMAGE": "viking2.png",
        }
    TYPE_3 = {
        "ATTACKINTERVAL": 60,
        "DAMAGE": 20,
        "HEALTH": 300,
        "MONEY": 300,
        "SPEED": 1,
        "IMAGE": "viking3.png",
        }

class BULLET:
    STONE = 100
    FIREBALL = 200
    #bullet state
    NOT_HIT = 30
    HIT = 31

class BUTTONS:
    names = {
	#generic button
	"DEFAULT": "playButton.png",
	#main menu
	"NEW_GAME": "playButton.png",
	"OPTIONS": "settingsButton.png",
	"EXIT": "exitButton.png",
        #submenu
        "MUSICMINUS": "settingsMinusButton.png",
        "MUSICPLUS": "settingsPlusButton.png",
        "FXMINUS": "settingsMinusButton.png",
        "FXPLUS": "settingsPlusButton.png",
        "DIFFICULTYEASY": "difficultyEasyButton.png",
        "DIFFICULTYMEDIUM": "difficultyMediumButton.png",
        "DIFFICULTYHARD": "difficultyHardButton.png",
        "EXITSETTINGS": "exitSettingsButton.png",
        "SAVESETTINGS": "saveSettingsButton.png",
        #game
        "SHOWMENU": "showMenuButton.png",
        #ingame menu
        "RESUMEGAME": "resumeGameButton.png",
        "QUITGAME": "quitGameButton.png",
        #floors of tower
        "FLOOR1": "floorButton.png",
        "FLOOR2": "floorButton.png",
        "FLOOR3": "floorButton.png",
        "FLOOR4": "floorButton.png",
        "CLOSEFLOORMENU": "closeFloorMenuButton.png",
        #towerFloor menu
        "UPGRADEFLOORLEVEL": "upgradeButton.png",
        "FIXTOWERFLOOR": "fixTowerFloorButton.png",
        "BUYDEFENDER": "buyButton.png",
        "SELLDEFENDER": "sellButton.png",
        "UPGRADEDEFENDERDAMAGE": "upgradeButton.png",
        "UPGRADEDEFENDERINTERVAL": "upgradeButton.png",
        "UPGRADEDEFENDERSPEED": "upgradeButton.png",
        #floorMenu store
        "CLOSEFLOORMENUSTORE": "closeFloorMenuButton.png",
        "BUYSPEARMAN" : "buyButton.png",
        "BUYSLINGER" : "buyButton.png",
        "BUYARCHER" : "buyButton.png",
        "BUYCATAPULT" : "buyButton.png",
        "BUYCANNON" : "buyButton.png",
        "BUYWIZARD" : "buyButton.png",
        #defense scene
        "VIKING1":"viking1.png",
        "VIKING2":"viking2.png",
        "VIKING3":"viking3.png",
        #gameOver
        "BACKTOMENU": "backToMenuButton.png"
	}

class COSTS:
    DEFENDER = {
        "NONE": 0,
        "SPEARMAN": 1000,
        "SLINGER": 1500,
        "ARCHER": 2000,
        "CATAPULT": 4000,
        "CANNON": 5000,
        "WIZARD": 10000
        }

    class DEFENDERUPGRADE:
        DAMAGE = 500
        RELOAD = 500
        SPEED = 500

        STEP = 500

    class FLOOR:
        UPGRADE = 10000

class CATEGORY:
    GROUND = 0x0001
    VIKING = 0x0002
    BULLET = 0x0003
    TOWER = 0x0004

class SKILLS:
    DAMAGE = {
        "NONE": 0.0,
        "SPEARMAN": 100.0,
        "SLINGER": 50.0,
        "ARCHER": 50.0,
        "CATAPULT": 100.0,
        "CANNON": 125.0,
        "WIZARD": 100.0
        }
    SPEED = {
        "NONE": 0.0,
        "SPEARMAN": 75.0,
        "SLINGER": 30.0,
        "ARCHER": 40.0,
        "CATAPULT": 45.0,
        "CANNON": 75.0,
        "WIZARD": 100.0
        }
    INTERVAL = {
        "NONE": -1.0,
        "SPEARMAN": 60.0,
        "SLINGER": 140.0,
        "ARCHER": 100.0,
        "CATAPULT": 180.0,
        "CANNON": 240.0,
        "WIZARD": 80.0
        }
    MAXDISTANCE = {
        "NONE": -1.0,
        "SPEARMAN": 10.0,
        "SLINGER": 30.0,
        "ARCHER": 40.0,
        "CATAPULT": 50.0,
        "CANNON": 60.0,
        "WIZARD": 70.0
        }
    
    STEP = 5
    #interwal 35 frame'ow -> 2 strzaly na sekunde
    MINVALUE = 35

    class FLOOR:
        MAXLEVEL = 1

class BULLETSPRITE:
    name = {
        "NONE":  "resources/bullet_spearman.png",
        "SPEARMAN": "resources/bullet_spearman.png",
        "SLINGER":  "resources/bullet_slinger.png",
        "ARCHER":  "resources/bullet_archer.png",
        "CATAPULT":  "resources/bullet_catapult.png",
        "CANNON":  "resources/bullet_cannon.png",
        "WIZARD":  "resources/bullet_wizard.png"
        }

class BULLETMUSIC:
    name = {
        "NONE":  "resources/none.ogg",
        "SPEARMAN": "resources/slinger.ogg",
        "SLINGER":  "resources/slinger.ogg",
        "ARCHER":  "resources/archer.ogg",
        "CATAPULT":  "resources/catapult.ogg",
        "CANNON":  "resources/cannon.ogg",
        "WIZARD":  "resources/wizard.ogg"
        }

    
