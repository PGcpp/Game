class STATE:
    STOPPED = 1
    RUNNING = 2
    EXIT = 3
    SUSPEND = 4

class MENU:
    PLAY = 101
    OPTIONS = 102

class PARAMS:
    IMAGEPATH = "resources/"

class BUTTONS:
    names = {
	#generic buttom
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
        #ingame menu
        "RESUMEGAME": "resumeGameButton.png",
        "QUITGAME": "quitGameButton.png",
    #defense scene
    "VIKING":"viking.png"
	}
