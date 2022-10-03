import pygame
import time

def play_music():
    #files = ['./vp1.mp3','./vp.mp3']
    files = ['music.mp3']
    pygame.init()
    pygame.mixer.init()
    
    stepper = 0
    #file loading
    while stepper < len(files):
        pygame.mixer.music.load(files[stepper])
        print("Playing:",files[stepper])
        stepper += 1
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
    #play and pause
        while pygame.mixer.music.get_busy():
            timer = pygame.mixer.music.get_pos()
            time.sleep(1)
            control = input()
            pygame.time.Clock().tick(10)
            if control == "pause":
                pygame.mixer.music.pause()
            elif control == "play" :
                pygame.mixer.music.unpause()
            elif control == "stop":
                pygame.mixer.music.stop()
            elif control == "time":
                timer = pygame.mixer.music.get_pos()
                timer = timer/1000
                print (str(timer))
            elif int(timer) > 10:
                print ("True")
                pygame.mixer.music.stop()
                break
            else:
                continue
if __name__ == "__main__":
    play_music()