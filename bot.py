from pyautogui import *
import pyautogui
import time
import pytesseract
from PIL import Image
import keyboard
import win32api, win32con
import random
import numpy as np


#path to tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"   

#Time used to train troops
trainingTime = 27*60+10  


#Hvor i et område gitt på formen til pyautogui sin locate on screen, her find_image() man vil trykke
#Ikke bruk denne senere, kun for bruk i clickPic()
def clickPos(pic):
    x,y = int(pic.left + pic.width/2), int(pic.top + pic.height/2)
    return x,y


#Trykke på noe gitt funn på skjerm. Enten fra find_image() eller wait_for_image()
def clickPic(pic):
    x,y = clickPos(pic)
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


#Trykke på en spesifikk koordinat
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


#Trykk på space
def hitSpace():
    pyautogui.press('space')


#Trykk på kryss ut knappen i clash
def hitX():
    xBtn = find_image('Xbtn.png')
    if xBtn != None:
        x,y = clickPos(xBtn)
        click(x,y)


#vent i x sekunder
def wait(x):
    time.sleep(x)


#Finn området et gitt bilde er vist på skjærmen
def find_image(path, region=None, confidence = 0.8):
    path = '.\\images\\' + path
    if region is None:
        region = (0,0,pyautogui.size().width, pyautogui.size().height)
    return pyautogui.locateOnScreen(path, region=region, confidence=confidence)


#Vent til man finner dette området
def  wait_for_image(path, region=None, confidence = 0.8):
    i = 0
    while True:
        location = find_image(path, region, confidence)
        if i%10 == 0:
            print(location)
        if location != None:
            return location
        else:
            wait(0.1)
            i += 1


#Tren tropper via quicktrain
def train():
    trainIcon = wait_for_image('trainIcon.png')
    x,y = clickPos(trainIcon)
    wait(0.5) 
    click(x,y)
    wait(1)

    quickTrain = wait_for_image('quickTrain.png')
    x,y = clickPos(quickTrain)
    click(x,y)
    wait(1)

    trainBtn = wait_for_image('trainBtn.png')
    x,y=clickPos(trainBtn)
    click(x,y)
    wait(1)

    xBtn = wait_for_image('Xbtn.png')
    x,y = clickPos(xBtn)
    click(x,y)
    wait(1)


#Samle ressurser
def resources():
    gold = find_image('gold.png')
    elixir = find_image('elixir.png')
    dark = find_image('dark.png')

    if gold!=None:
        clickPic(gold)
    if elixir!=None:
        clickPic(elixir)
    if dark!=None:
        clickPic(dark)

    wait(1)


#Tell antall byggere ledig
def countBuilders():
    buildersPic = wait_for_image('builderIcon.png')     #finner builder ikonet

    #tar skjermbildet av tallet som sier hvor mange ledige byggere, finn + fra feks paint
    pyautogui.screenshot('screen.png',region=(buildersPic.left + 108, buildersPic.top+34, 22, 32))
    img = Image.open('screen.png')      #åpne skjermbildet

    builders = pytesseract.image_to_string(img, config='--psm 10')   #Leser teksten på bildet, --psm 10 sier at det er en karakter i bildet.
    print(builders) #mest for feiltesting

    try:
        builders = int(builders)
    except ValueError:
        if 'o' in builders or 'O' in builders:
            builders = 0
        else:
            builders = 5
    print(builders)     #For feiltesting
    
    return builders


#Start å oppgradere bygninger hvis du har ledige byggere
def startUpgrade():
    builders = countBuilders()
    while builders > 0:
        build = wait_for_image('builderIcon.png')
        clickPic(build)
        
        suggest = wait_for_image('suggest.png')

        #330,65  avstand fra suggest til der man skal trykke, finn denne selv, feks i paint
        click(suggest.left + 330, suggest.top + 65)     

        upgrade = wait_for_image('upgrade.png')
        clickPic(upgrade)
        wait(1)

        #930, 890
        
        click(930,890)  #Klikk posisjon på oppgraderknappen, finn denne selv via pyautogui.locateOnScreen() i terminalen
        wait(1)
        builders = countBuilders()
        hitX()
        hitX()

#plasser en tropp, gitt ved hvilken tropp, hvor skal den plasseres, og hvor mange skal plasseres
def place(troop, where,  n):
    clickPic(troop)
    for i in range(n):
        clickPic(where)
        wait(0.1)


#et GoWiPe angrep for rådhus 8
def gowipe():
    hitX()
    hitSpace()
    wait(1)

    findMatch = wait_for_image('findMatch.png')
    clickPic(findMatch)
    wait(1)

    next = wait_for_image('next.png')

    #troops
    golem = wait_for_image('golem.png')
    golems = 2
    pekka = wait_for_image('pekka.png')
    pekkas = 3
    wizard = wait_for_image('wizard.png')
    wizards = 13
    wallbreaker = wait_for_image('wallbreaker.png')
    wallbreakers = 6
    archer = wait_for_image('archer.png')
    archers = 1
    king = wait_for_image('king.png')
    kings = 1

    #spells
    rage = wait_for_image('rage.png')
    rages = 2
    heal = wait_for_image('heal.png')
    heals = 1
    poison = wait_for_image('poison.png')
    poisons = 1

    openSpace = wait_for_image('openSpace.png', confidence=0.6)  #Hvor troppene skal plasseres
    place(golem, openSpace, golems) 
    wait(2)
    place(king, openSpace, kings)
    place(wallbreaker, openSpace, wallbreakers)
    wait(1)
    place(wizard, openSpace, wizards)
    wait(1)
    place(pekka, openSpace, pekkas)
    place(archer, openSpace, archers)

    wait(5)
    place(rage, openSpace, rages)
    place(heal, openSpace, heals)
    place(poison, openSpace, poisons)

    
    #Når kampen er over skal man returnere tilbake til hjem
    returnHome = wait_for_image('returnHome.png')  
    clickPic(returnHome)


    wait(5) #Venter så man er sikker på at den er klar
    hitX()  #Krysser ut om det er en eventuell popup, som stjernebonus

    wait(5)
    train() #tren tropper med quick train
    


wait(5) # Ventetid, så man rekker å bytte til programmet før det starter

while keyboard.is_pressed('q') == False:



    gowipe() #angrip

    t = time.time() + trainingTime      #hvor lenge den skal vente mellom hvert angrep

    while (time.time() < t) and (keyboard.is_pressed('q') == False):  #samle ressurser og oppgrader mellom hvert angrep
        resources()
        startUpgrade()
    


