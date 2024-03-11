import mixer

class Sound:
    def __init__(self):
        mixer.init()
        self.phaser_sound = mixer.Sound("sounds.wav")   # replace sound file
        self.volume = 0.1
        self.set_volume(self.volume)
    
    def set_volume(self, volume=0.3):
        pass