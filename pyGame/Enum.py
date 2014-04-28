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
    #types
    TYPE_1 = 20
    TYPE_2 = 21
    TYPE_3 = 22
    #states
    NOT_HIT = 23
    HIT = 24
    ATTACK = 25

class BULLET:
    #types
    STONE = 100
    FIREBALL = 200
    #states
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
        #floorMenu store
        "CLOSEFLOORMENUSTORE": "closeFloorMenuButton.png",
        #defense scene
        "VIKING1":"viking1.png",
        "VIKING2":"viking2.png",
        "VIKING3":"viking3.png"
	}

class COSTS:
    DEFENDER = {
        "NONE": 0,
        "SPEARMAN": 500,
        "SLINGER": 700,
        "ARCHER": 1000,
        "CATAPULT": 1500,
        "CANNON": 1900,
        "WIZARD": 3000
        }
