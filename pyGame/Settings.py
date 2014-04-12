import ConfigParser

def getMusicLevel():
    settings = ConfigParser.ConfigParser()
    settings.readfp(open('settings.cfg'))
    temp =  float(settings.get("MUSIC", "LEVEL")) * 0.2
    print temp
    return temp

def getEffectsLevel():
    settings = ConfigParser.ConfigParser()
    settings.readfp(open('settings.cfg'))
    temp =  float(settings.get("EFFECTS", "LEVEL")) * 0.2
    print temp
    return temp

def getDifficultyLevel():
    pass
        

        

