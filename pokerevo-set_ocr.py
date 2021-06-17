#!/usr/bin/env python

import pandas as pd
import os
import cv2
import difflib
import easyocr
import pyperclip
import tkinter as tk
import time as tm
from PIL import ImageEnhance
from tkinter import Button, Label, filedialog
from pynput.keyboard import Controller, Key

reader = easyocr.Reader(['en'],gpu = True)
# region Data import

# moves
df = pd.read_csv('data/moves.csv')
dictMoves = df.to_dict('list')
moves_list = dictMoves['move']

# abilities
df = pd.read_csv('data/abilities.csv')
dictAbilities = df.to_dict('list')
abilities_list = dictAbilities['ability']


# natures
df = pd.read_csv('data/natures.csv')
dictNatures = df.to_dict('list')
natures_list = dictNatures['nature']

# pokemon
df = pd.read_csv('data/pokemon.csv')
dictPokemon = df.to_dict('list')
pokemon_list = dictPokemon['species'][:802]

#  items
df = pd.read_csv('data/items.csv')
dictItems = df.to_dict('list')
items_list = ['']+dictItems['item']

# endregion

pathTuple = ()

def fileSelection():
    global pathTuple
    pathEntry.delete(0, tk.END)
    name = filedialog.askopenfilenames(
        title='Select file', initialdir='./', filetypes=[('PNG files', '*.png')])
    pathTuple = name
    pathEntry.insert(0, name)


def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def zoom(image,x):
    scale_percent = x
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return (cv2.resize(image, dim, interpolation=cv2.INTER_AREA))


def coordinates():
    f = open('coordinates.txt', 'r')
    coor = f.read()
    f.close()
    coor = coor.split(',')
    for i in range(len(coor)):
        coor[i] = int(coor[i])
    return coor

index = tk.Tk()
index.title('Pokerevo Set Showdown')

frameTop = tk.Frame(index)
frameTop.pack()
buttonPath = tk.Button(frameTop, text='Choose File', command=fileSelection)
buttonPath.pack(side=tk.RIGHT)
pathEntry = tk.Entry(frameTop, fg="black", bg="white", width=59, bd=5)
pathEntry.pack()


textBox = tk.Text(index, height=30, width=75)
textBox.pack()

liste_time=[]
def convertion(path):
    # global liste_time
    # start=tm.time()
    coor = coordinates()
    item = ''
    # region nom pokemon + cropping screenshot
    im = zoom(cv2.imread(path),220)
    image = increase_brightness(im, value=50)
    name_img = image[coor[0+1]:coor[0+3], coor[0+0]:coor[0+2]]
    pkm = reader.readtext(name_img, detail=0)[0]
    pkm = difflib.get_close_matches(pkm, pokemon_list, n=1)[0]
    pkm_ability = image[coor[4+1]:coor[4+3], coor[4+0]:coor[4+2]].copy()
    pkm_moves = image[coor[8+1]:coor[8+3], coor[8+0]:coor[8+2]].copy()
    pkm_ivs = zoom(im[coor[12+1]:coor[12+3], coor[12+0]:coor[12+2]].copy(),220)
    pkm_ivs_bords = zoom(cv2.Canny(pkm_ivs, 250, 500),70)
    if boolCropped.get()==True:
        cv2.imwrite(f'{pkm}-ivs_bord.png',pkm_ivs_bords)
        cv2.imwrite(f'{pkm}-moves.png',pkm_moves)
        cv2.imwrite(f'{pkm}-ability.png',pkm_ability)
    # endregion

    # region reading + verif + affectation
    # reading screenshots
    stats = reader.readtext(pkm_ivs_bords, detail=0, allowlist='0123456789')
    AbNa = reader.readtext(pkm_ability, detail=0)
    moves = reader.readtext(pkm_moves, detail=0)
    if boolRead.get()==True:
        print(f'Name: {pkm}\nAbility and Nature list: {AbNa}\nMoves: {moves}\nStats: {stats}')

    # evs and ivs
    IvAtt = stats[0][0:2] ;  EvAtt = stats[0][2:]
    IvDef = stats[1][0:2] ;  EvDef = stats[1][2:]
    IvSpe = stats[2][0:2] ;  EvSpe = stats[2][2:]
    IvSpA = stats[3][0:2] ;  EvSpA = stats[3][2:]
    IvSpD = stats[4][0:2] ;  EvSpD = stats[4][2:]
    IvHP = stats[5][0:2]  ;  EvHP = stats[5][2:]
    EVs=[EvAtt,EvDef,EvSpe,EvSpA,EvSpD,EvHP] ; IVs=[IvAtt,IvDef,IvSpe,IvSpA,IvSpD,IvHP]
    for k in range(6):
        EVs[k]=int(EVs[k])
        IVs[k]=int(IVs[k])
        if EVs[k]==282 or EVs[k]==262:
            EVs[k]=252
    for k in range(6):
        if sum(EVs)==490 and EVs[k]==232:
            EVs[k]=252
    # ability and nature
    Ability = difflib.get_close_matches(AbNa[1], abilities_list, n=1)[0]
    Nature = difflib.get_close_matches(AbNa[3], natures_list, n=1)[0]
    # moves
    moves[0] = difflib.get_close_matches(moves[0], moves_list, n=1)[0]
    moves[1] = difflib.get_close_matches(moves[1], moves_list, n=1)[0]
    moves[2] = difflib.get_close_matches(moves[2], moves_list, n=1)[0]
    moves[3] = difflib.get_close_matches(moves[3], moves_list, n=1)[0]
    # item
    item = difflib.get_close_matches(item, items_list, n=1)[0]
    # endregion
    
    set = f'{pkm} @ {item}\nAbility: {Ability}\n{Nature} Nature\nIVs: {IvAtt} Att / {IvDef} Def / {IvSpe} Spe / {IvSpA} SpA / {IvSpD} SpD / {IvHP} HP \nEVs: {EVs[0]} Att / {EVs[1]} Def / {EVs[2]} Spe / {EVs[3]} SpA / {EVs[4]} SpD / {EVs[5]} HP \n- {moves[0]}\n- {moves[1]}\n- {moves[2]}\n- {moves[3]}\n\n'
    
    # liste_time.append(tm.time()-start)
    # print(f'Nombre de pokemon: {len(liste_time)}\nTemps moyen par pokemon: {sum(liste_time)/len(liste_time)}\nTemps total: {sum(liste_time)}')
    # f = open('i5_4300U.txt', 'a+')
    # f.write(str(liste_time)[1:-1]+',')
    # f.close()
    
    return(set)

def convert():
    global pathTuple, liste_time
    for path in pathTuple:
        textBox.insert("1.0", convertion(path))
    liste_time=[]


def copy():
    pyperclip.copy(textBox.get("1.0", tk.END))


def fileWrite():
    text = textBox.get("1.0", tk.END)
    fileSet = open("sets.txt", "w+")
    fileSet.write(text)
    fileSet.close()


def textClean():
    textBox.delete('1.0', tk.END)

compteurShow = 0
def calibrageShow():
    global compteurShow
    compteurShow+=1
    if compteurShow%2==1:
        labelCalibre.pack()
        pathEntryCalibrageWindow.pack()
        buttonCalibrageSelect.pack()
        buttonCalibrageWindow.pack()
    if compteurShow%2==0:
        labelCalibre.pack_forget()
        pathEntryCalibrageWindow.pack_forget()
        buttonCalibrageSelect.pack_forget()
        buttonCalibrageWindow.pack_forget()

boolCropped = tk.IntVar()
boolRead = tk.IntVar()
frameButtons = tk.Frame(index)
frameButtons.pack()


croppedBoxes = tk.Checkbutton(frameButtons, text='Create cropped screenshots', variable=boolCropped)
croppedBoxes.pack(side=tk.TOP)
readBoxes = tk.Checkbutton(frameButtons, text='Print text read from screenshots', variable=boolRead)
readBoxes.pack(side=tk.TOP)
buttonConvert = tk.Button(frameButtons, text='Convert', command=convert)
buttonConvert.pack(side=tk.TOP)


buttonCopy = tk.Button(frameButtons, text='Copy', command=copy)
buttonCopy.pack(side=tk.RIGHT)
buttonWrite = tk.Button(frameButtons, text='set.txt', command=fileWrite)
buttonWrite.pack(side=tk.RIGHT)
buttonClean = tk.Button(frameButtons, text='Clean', command=textClean)
buttonClean.pack(side=tk.RIGHT)
buttonCalibrage = tk.Button(frameButtons, text='Calibrate', command=calibrageShow)
buttonCalibrage.pack(side=tk.TOP)




def fileSelectionCalibrage():
    pathEntryCalibrageWindow.delete(0, tk.END)
    name = filedialog.askopenfilename(
        title='Select file', initialdir='./', filetypes=[('PNG files', '*.png')])
    pathEntryCalibrageWindow.insert(0, name)


img =[]; l=[]; c=0; point=[]
def click_event(event, x, y, flags, params):
    global c, point, l, img
    if event == cv2.EVENT_LBUTTONDOWN:
        l.append(x)
        l.append(y)
        point = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        l.append(x)
        l.append(y)
        point.append((x, y))
        c = c+2
        cv2.rectangle(img, point[0], point[1], (0, 255, 0), 2)
        cv2.imshow("image", img)
    if c == 8:
        f = open('coordinates.txt', 'w+')
        f.write(str(l)[1:-1])
        f.close()
        keyboard = Controller()
        keyboard.press('a')
        keyboard.release('a')

def calibrer():
    global img,c,l
    c=0;l=[]
    img = zoom(cv2.imread(pathEntryCalibrageWindow.get(), 1),220)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyWindow('image')



labelCalibre = tk.Label(
    index, text="You need to frame: Name, ability + nature, moves(without 'Moves') and last 2 rows of stats")
buttonCalibrageSelect = tk.Button(
    index, text='Choose file', command=fileSelectionCalibrage)
pathEntryCalibrageWindow = tk.Entry(
    index, fg="black", bg="white", width=50, bd=5)
buttonCalibrageWindow = tk.Button(index, text='Calibrate', command=calibrer)


index.mainloop()
