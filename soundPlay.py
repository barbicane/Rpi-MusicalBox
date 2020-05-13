# fonction qui va lire charger une liste de son et qui va le lire au signal
import pygame, os, time
from random import choice

liste_son = os.listdir("/home/pi/Desktop/Boite-Musicale/sounds/")
#index_son = 0
bounce_time = 0
pygame.init()

def play_sound():
    global index_son, liste_son, bounce_time
    if time.time() - bounce_time < 3:
        return
    #if index_son >= len(liste_son):
    #    index_son = 0
    # charge un son
    #print("lecture")
    pygame.mixer.music.load("/home/pi/Desktop/Boite-Musicale/sounds/"+choice(liste_son))
    #pygame.mixer.music.load("/home/pi/Desktop/Boite-Musicale/sounds/"+liste_son[index_son])
    #index_son += 1
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.5)
    pygame.mixer.music.stop()
