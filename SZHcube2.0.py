from pygame import quit,init,display,font,draw,event,mouse
from tkinter import Tk,Label,StringVar,Entry,Button
from sys import exit
from traceback import print_exc
import mf
from threading import Thread
from pygame.locals import MOUSEMOTION,MOUSEBUTTONDOWN,QUIT
from random import randint,choice
from serial import Serial
import serial.tools.list_ports

try:
    ser=Serial(serial.tools.list_ports.comports()[0][0],115200)
except:
    print('重新插入串口')
init()
bg_size = width, height = 600, 600
cameraThread=None
screen = display.set_mode(bg_size)
display.set_caption("六步解三阶魔方2.0---源自1213清心")

color2int = ['白','黄','红','橙','绿','蓝']
#颜色存入块标准
store=[]
for i in range(3):
    store.append([])
    for j in range(3):
        store[i].append([])
        for k in range(3):
            store[i][j].append(set([]))
for i in range(3):
    for j in range(3):
        store[i][2][j].add(0)
        store[i][0][j].add(1)
        store[0][i][j].add(2)
        store[2][i][j].add(3)
        store[i][j][2].add(4)
        store[i][j][0].add(5)
#块存入颜色标准
face2store=[]
for k in range(6):
    face2store.append([])
    for i in range(3):
        face2store[k].append([])
        for j in range(3):
            face2store[k][i].append([-1,-1,-1])
for i in range(3):
    for j in range(3):
        face2store[0][i][j][0]=i
        face2store[0][i][j][1]=2
        face2store[0][i][j][2]=2-j
        face2store[1][i][j][0]=2-i
        face2store[1][i][j][1]=0
        face2store[1][i][j][2]=2-j
        face2store[2][i][j][0]=0
        face2store[2][i][j][1]=i
        face2store[2][i][j][2]=2-j
        face2store[3][i][j][0]=2
        face2store[3][i][j][1]=2-i
        face2store[3][i][j][2]=2-j
        face2store[4][i][j][0]=i
        face2store[4][i][j][1]=j
        face2store[4][i][j][2]=2
        face2store[5][i][j][0]=i
        face2store[5][i][j][1]=2-j
        face2store[5][i][j][2]=0
line2cube=[]
for k in range(3):
    for j in range(3):
        for i in range(3):
            line2cube.append([i,j,k])
#解法文件
SZHsolve = []
#初始化面信息和块信息
face = [[],[],[],[],[],[]]
for k in range(6):
    for i in range(3):
        face[k].append([])
        for j in range(3):
            face[k][i].append(k)
cube = []
for i in range(3):
    cube.append([])
    for j in range(3):
        cube[i].append([])
        for k in range(3):
            cube[i][j].append([i,j,k])
#颜色存入块
question=[]
for i in range(3):
    question.append([])
    for j in range(3):
        question[i].append([])
        for k in range(3):
            question[i][j].append(set([]))
for k in range(6):
    for i in range(3):
        for j in range(3):
            question[face2store[k][i][j][0]][face2store[k][i][j][1]][face2store[k][i][j][2]].add(face[k][i][j])

F2Lorder=[[],[],[],[],[],[],[],[],[],[],[],[]]
F2Lorder[0].append('RUr')
F2Lorder[0].append('fuF')
F2Lorder[0].append('FrfR')
F2Lorder[0].append('URur')

F2Lorder[1].append('u'+'RUrU'+'RUr')
F2Lorder[1].append('5'+'rUUR'+'%'+'RUr')
F2Lorder[1].append('u'+'RurU'+'RUr')
F2Lorder[1].append('Uy'+'ruRu'+'ruR')
F2Lorder[1].append('u'+'RUUr'+'5'+'ruR')
F2Lorder[1].append('5'+'rURu'+'ruR')

F2Lorder[2].append('u'+'RUUr'+'UU'+'Rur')
F2Lorder[2].append('u'+'RUr'+'UU'+'Rur')
F2Lorder[2].append('5'+'rUUR'+'UU'+'rUR')
F2Lorder[2].append('5'+'ruR'+'UU'+'rUR')

F2Lorder[3].append('yu'+'rUUR'+'u'+'rUR')
F2Lorder[3].append('URUUrr'+'FRf')
F2Lorder[3].append('Rur'+'UU'+'RUr')
F2Lorder[3].append('y'+'rUR'+'UU'+'ruR')

F2Lorder[4].append('U'+'Rur'+'u'+'fUF')
F2Lorder[4].append('u'+'fUF'+'U'+'Rur')

F2Lorder[5].append('5'+'ruR'+'%'+'RUr')
F2Lorder[5].append('u'+'RUr'+'5'+'ruR')
F2Lorder[5].append('u'+'RUUr'+'U'+'RUr')
F2Lorder[5].append('uRur'+'UU'+'Rur')

F2Lorder[6].append('RUUr'+'u'+'RUr')
F2Lorder[6].append('y'+'rUUR'+'U'+'ruR')

F2Lorder[7].append('RurU'+'5'+'ruR')
F2Lorder[7].append('y'+'rURu'+'%'+'RUr')

F2Lorder[8].append('Rur'+'5'+'rUR')
F2Lorder[8].append('RUru'+'RUru'+'RUr')

F2Lorder[9].append('RurU'+'Rur')
F2Lorder[9].append('RUru'+'FrfR')
F2Lorder[9].append('RUru'+'RUr')
F2Lorder[9].append('YluLUluL')

F2Lorder[10].append('RUr'+'5'+'rURu'+'rUR')
F2Lorder[10].append('UURRUU'+'ruRu'+'RR')

F2Lorder[11].append('RurU'+'RUUr'+'U'+'Rur')
F2Lorder[11].append('RurU'+'5'+'ruRu'+'rUR')
F2Lorder[11].append('Rur'+'u'+'RUr'+'UU'+'Rur')
F2Lorder[11].append('Ruru'+'Rur'+'U'+'fuF')
F2Lorder[11].append('RuurU'+'RuurU'+'y'+'ruR')
#通用顺时针旋转不包括四周
def rotate(qcube,qface):
    pcube = []
    pcube.extend([qcube[6],qcube[3],qcube[0]])
    pcube.extend([qcube[7],qcube[4],qcube[1]])
    pcube.extend([qcube[8],qcube[5],qcube[2]])
    pface = []
    pface.append([qface[0][2],qface[1][2],qface[2][2]])
    pface.append([qface[0][1],qface[1][1],qface[2][1]])
    pface.append([qface[0][0],qface[1][0],qface[2][0]])
    return pcube,pface
#通用顺时针旋转不包括四周
def unrotate(qcube,qface):
    pcube = []
    pcube.extend([qcube[2],qcube[5],qcube[8]])
    pcube.extend([qcube[1],qcube[4],qcube[7]])
    pcube.extend([qcube[0],qcube[3],qcube[6]])
    pface=[]
    pface.append([qface[2][0],qface[1][0],qface[0][0]])
    pface.append([qface[2][1],qface[1][1],qface[0][1]])
    pface.append([qface[2][2],qface[1][2],qface[0][2]])
    return pcube,pface
    
def doF():
    [cube[0][2][2],cube[1][2][2],cube[2][2][2],\
     cube[0][2][1],cube[1][2][1],cube[2][2][1],\
     cube[0][2][0],cube[1][2][0],cube[2][2][0]],\
     face[0]=rotate([cube[0][2][2],cube[1][2][2],cube[2][2][2],\
         cube[0][2][1],cube[1][2][1],cube[2][2][1],\
         cube[0][2][0],cube[1][2][0],cube[2][2][0]],face[0])
    t=face[3][0]
    face[3][0]=[face[4][0][2],face[4][1][2],face[4][2][2]]
    [face[4][0][2],face[4][1][2],face[4][2][2]]=\
        [face[2][2][2],face[2][2][1],face[2][2][0]]
    [face[2][2][2],face[2][2][1],face[2][2][0]]=\
        [face[5][2][0],face[5][1][0],face[5][0][0]]
    [face[5][2][0],face[5][1][0],face[5][0][0]]=t
    #print('F',end=' ')
    SZHsolve.append('F')
def unF():
    [cube[0][2][2],cube[1][2][2],cube[2][2][2],\
     cube[0][2][1],cube[1][2][1],cube[2][2][1],\
     cube[0][2][0],cube[1][2][0],cube[2][2][0]],\
     face[0]=unrotate([cube[0][2][2],cube[1][2][2],cube[2][2][2],\
         cube[0][2][1],cube[1][2][1],cube[2][2][1],\
         cube[0][2][0],cube[1][2][0],cube[2][2][0]],face[0])
    t=face[3][0]
    face[3][0]=[face[5][2][0],face[5][1][0],face[5][0][0]]
    [face[5][2][0],face[5][1][0],face[5][0][0]]=\
        [face[2][2][2],face[2][2][1],face[2][2][0]]
    [face[2][2][2],face[2][2][1],face[2][2][0]]=\
        [face[4][0][2],face[4][1][2],face[4][2][2]]
    [face[4][0][2],face[4][1][2],face[4][2][2]]=t
    #print('F\'',end=' ')
    SZHsolve.append('f')
def doL():
    [cube[0][0][2],cube[0][1][2],cube[0][2][2],\
     cube[0][0][1],cube[0][1][1],cube[0][2][1],\
     cube[0][0][0],cube[0][1][0],cube[0][2][0]],\
    face[2]=rotate([cube[0][0][2],cube[0][1][2],cube[0][2][2],\
         cube[0][0][1],cube[0][1][1],cube[0][2][1],\
         cube[0][0][0],cube[0][1][0],cube[0][2][0]],face[2])
    t=face[0][0]
    face[0][0]=face[4][0]
    face[4][0]=[face[1][2][2],face[1][2][1],face[1][2][0]]
    [face[1][2][2],face[1][2][1],face[1][2][0]]=face[5][0]
    face[5][0]=t
    #print('L',end=' ')
    SZHsolve.append('L')
def unL():
    [cube[0][0][2],cube[0][1][2],cube[0][2][2],\
     cube[0][0][1],cube[0][1][1],cube[0][2][1],\
     cube[0][0][0],cube[0][1][0],cube[0][2][0]],\
    face[2]=unrotate([cube[0][0][2],cube[0][1][2],cube[0][2][2],\
         cube[0][0][1],cube[0][1][1],cube[0][2][1],\
         cube[0][0][0],cube[0][1][0],cube[0][2][0]],face[2])
    t=face[0][0]
    face[0][0]=face[5][0]
    face[5][0]=[face[1][2][2],face[1][2][1],face[1][2][0]]
    [face[1][2][2],face[1][2][1],face[1][2][0]]=face[4][0]
    face[4][0]=t
    #print('L\'',end=' ')
    SZHsolve.append('l')
def doR():
    [cube[2][2][2],cube[2][1][2],cube[2][0][2],\
     cube[2][2][1],cube[2][1][1],cube[2][0][1],\
     cube[2][2][0],cube[2][1][0],cube[2][0][0]],\
    face[3]=rotate([cube[2][2][2],cube[2][1][2],cube[2][0][2],\
         cube[2][2][1],cube[2][1][1],cube[2][0][1],\
         cube[2][2][0],cube[2][1][0],cube[2][0][0]],face[3])
    t=face[1][0]
    face[1][0]=[face[4][2][2],face[4][2][1],face[4][2][0]]
    [face[4][2][2],face[4][2][1],face[4][2][0]]=\
        [face[0][2][2],face[0][2][1],face[0][2][0]]
    [face[0][2][2],face[0][2][1],face[0][2][0]]=\
        [face[5][2][2],face[5][2][1],face[5][2][0]]
    [face[5][2][2],face[5][2][1],face[5][2][0]]=t
    #print('R',end=' ')
    SZHsolve.append('R')
def unR():
    
    [cube[2][2][2],cube[2][1][2],cube[2][0][2],\
     cube[2][2][1],cube[2][1][1],cube[2][0][1],\
     cube[2][2][0],cube[2][1][0],cube[2][0][0]],\
    face[3]=unrotate([cube[2][2][2],cube[2][1][2],cube[2][0][2],\
         cube[2][2][1],cube[2][1][1],cube[2][0][1],\
         cube[2][2][0],cube[2][1][0],cube[2][0][0]],face[3])
    t=face[1][0]
    face[1][0]=[face[5][2][2],face[5][2][1],face[5][2][0]]
    [face[5][2][2],face[5][2][1],face[5][2][0]]=\
        [face[0][2][2],face[0][2][1],face[0][2][0]]
    [face[0][2][2],face[0][2][1],face[0][2][0]]=\
        [face[4][2][2],face[4][2][1],face[4][2][0]]
    [face[4][2][2],face[4][2][1],face[4][2][0]]=t
    #print('R\'',end=' ')
    SZHsolve.append('r')
def doU():
    [cube[0][0][2],cube[1][0][2],cube[2][0][2],\
     cube[0][1][2],cube[1][1][2],cube[2][1][2],\
     cube[0][2][2],cube[1][2][2],cube[2][2][2]],\
    face[4]=rotate([cube[0][0][2],cube[1][0][2],cube[2][0][2],\
         cube[0][1][2],cube[1][1][2],cube[2][1][2],\
         cube[0][2][2],cube[1][2][2],cube[2][2][2]],face[4])
    t=[face[3][2][0],face[3][1][0],face[3][0][0]]
    face[3][2][0],face[3][1][0],face[3][0][0]=\
        face[1][2][0],face[1][1][0],face[1][0][0]
    face[1][2][0],face[1][1][0],face[1][0][0]=\
        face[2][2][0],face[2][1][0],face[2][0][0]
    face[2][2][0],face[2][1][0],face[2][0][0]=\
        face[0][2][0],face[0][1][0],face[0][0][0]
    face[0][2][0],face[0][1][0],face[0][0][0]=t[0],t[1],t[2]
    #print('U',end=' ')
    SZHsolve.append('U')
def unU():
    [cube[0][0][2],cube[1][0][2],cube[2][0][2],\
     cube[0][1][2],cube[1][1][2],cube[2][1][2],\
     cube[0][2][2],cube[1][2][2],cube[2][2][2]],\
    face[4]=unrotate([cube[0][0][2],cube[1][0][2],cube[2][0][2],\
         cube[0][1][2],cube[1][1][2],cube[2][1][2],\
         cube[0][2][2],cube[1][2][2],cube[2][2][2]],face[4])
    t=[face[3][2][0],face[3][1][0],face[3][0][0]]
    [face[3][2][0],face[3][1][0],face[3][0][0]]=\
        [face[0][2][0],face[0][1][0],face[0][0][0]]
    [face[0][2][0],face[0][1][0],face[0][0][0]]=\
        [face[2][2][0],face[2][1][0],face[2][0][0]]
    [face[2][2][0],face[2][1][0],face[2][0][0]]=\
        [face[1][2][0],face[1][1][0],face[1][0][0]]
    face[1][2][0],face[1][1][0],face[1][0][0]=t[0],t[1],t[2]
    #print('U\'',end=' ')
    SZHsolve.append('u')
def doB():
    [cube[2][0][2],cube[1][0][2],cube[0][0][2],\
     cube[2][0][1],cube[1][0][1],cube[0][0][1],\
     cube[2][0][0],cube[1][0][0],cube[0][0][0]],\
    face[1]=rotate([cube[2][0][2],cube[1][0][2],cube[0][0][2],\
         cube[2][0][1],cube[1][0][1],cube[0][0][1],\
         cube[2][0][0],cube[1][0][0],cube[0][0][0]],face[1])
    t=face[2][0]
    face[2][0]=[face[4][2][0],face[4][1][0],face[4][0][0]]
    [face[4][2][0],face[4][1][0],face[4][0][0]]=\
        [face[3][2][2],face[3][2][1],face[3][2][0]]
    [face[3][2][2],face[3][2][1],face[3][2][0]]=\
        [face[5][0][2],face[5][1][2],face[5][2][2]]
    [face[5][0][2],face[5][1][2],face[5][2][2]]=t
    #print('B',end=' ')
    SZHsolve.append('B')
def unB():
    [cube[2][0][2],cube[1][0][2],cube[0][0][2],\
     cube[2][0][1],cube[1][0][1],cube[0][0][1],\
     cube[2][0][0],cube[1][0][0],cube[0][0][0]],\
    face[1]=unrotate([cube[2][0][2],cube[1][0][2],cube[0][0][2],\
         cube[2][0][1],cube[1][0][1],cube[0][0][1],\
         cube[2][0][0],cube[1][0][0],cube[0][0][0]],face[1])
    t=face[2][0]
    face[2][0]=[face[5][0][2],face[5][1][2],face[5][2][2]]
    face[5][0][2],face[5][1][2],face[5][2][2]=\
        [face[3][2][2],face[3][2][1],face[3][2][0]]
    [face[3][2][2],face[3][2][1],face[3][2][0]]=\
        [face[4][2][0],face[4][1][0],face[4][0][0]]
    [face[4][2][0],face[4][1][0],face[4][0][0]]=t
    #print('B\'',end=' ')
    SZHsolve.append('b')
def doD():
    [cube[0][2][0],cube[1][2][0],cube[2][2][0],\
     cube[0][1][0],cube[1][1][0],cube[2][1][0],\
     cube[0][0][0],cube[1][0][0],cube[2][0][0]],\
    face[5]=rotate([cube[0][2][0],cube[1][2][0],cube[2][2][0],\
         cube[0][1][0],cube[1][1][0],cube[2][1][0],\
         cube[0][0][0],cube[1][0][0],cube[2][0][0]],face[5])
    t=[face[3][0][2],face[3][1][2],face[3][2][2]]
    face[3][0][2],face[3][1][2],face[3][2][2]=\
        face[0][0][2],face[0][1][2],face[0][2][2]
    face[0][0][2],face[0][1][2],face[0][2][2]=\
        face[2][0][2],face[2][1][2],face[2][2][2]
    face[2][0][2],face[2][1][2],face[2][2][2]=\
        face[1][0][2],face[1][1][2],face[1][2][2]
    face[1][0][2],face[1][1][2],face[1][2][2]=t[0],t[1],t[2]
    #print('D',end=' ')
    SZHsolve.append('D')
def unD():
    [cube[0][2][0],cube[1][2][0],cube[2][2][0],\
     cube[0][1][0],cube[1][1][0],cube[2][1][0],\
     cube[0][0][0],cube[1][0][0],cube[2][0][0]],\
    face[5]=unrotate([cube[0][2][0],cube[1][2][0],cube[2][2][0],\
         cube[0][1][0],cube[1][1][0],cube[2][1][0],\
         cube[0][0][0],cube[1][0][0],cube[2][0][0]],face[5])
    t=[face[3][0][2],face[3][1][2],face[3][2][2]]
    face[3][0][2],face[3][1][2],face[3][2][2]=\
        face[1][0][2],face[1][1][2],face[1][2][2]
    face[1][0][2],face[1][1][2],face[1][2][2]=\
        face[2][0][2],face[2][1][2],face[2][2][2]
    face[2][0][2],face[2][1][2],face[2][2][2]=\
        face[0][0][2],face[0][1][2],face[0][2][2]
    face[0][0][2],face[0][1][2],face[0][2][2]=t[0],t[1],t[2]
    #print('D\'',end=' ')
    SZHsolve.append('d')
def findcube(pcube):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if cube[i][j][k]==pcube:
                    return [i,j,k]
    return [-1,-1,-1]
def cfop(s,m=''):
    t=list(m+s)
    seed=0
    dt0={'L':'D','D':'R','R':'U','U':'L','l':'d','d':'r','r':'u','u':'l'}
    pt0={'L':'U','U':'R','R':'D','D':'L','l':'u','u':'r','r':'d','d':'l'}
    dt2={'B':'D','D':'F','F':'U','U':'B','b':'d','d':'f','f':'u','u':'b'}
    pt2={'B':'U','U':'F','F':'D','D':'B','b':'u','u':'f','f':'d','d':'b'}
    dt3={'F':'D','D':'B','B':'U','U':'F','f':'d','d':'b','b':'u','u':'f'}
    pt3={'F':'U','U':'B','B':'D','D':'F','f':'u','u':'b','b':'d','d':'f'}
    dt5={'L':'B','B':'R','R':'F','F':'L','l':'b','b':'r','r':'f','f':'l'}
    pt5={'L':'F','F':'R','R':'B','B':'L','l':'f','f':'r','r':'b','b':'l'}
    for i in t:
        seed+=1
        if i=='F':
            doF()
        elif i=='B':
            doB()
        elif i=='L':
            doL()
        elif i=='R':
            doR()
        elif i=='U':
            doU()
        elif i=='D':
            doD()
        elif i=='f':
            unF()
        elif i=='b':
            unB()
        elif i=='l':
            unL()
        elif i=='r':
            unR()
        elif i=='u':
            unU()
        elif i=='d':
            unD()
        elif i=='0':
            doB()
            for j in range(seed,len(t)):
                for k in dt0:
                    if t[j]==k:
                        t[j]=dt0[k]
                        break
        elif i==')':
            unB()
            for j in range(seed,len(t)):
                for k in pt0:
                    if t[j]==k:
                        t[j]=pt0[k]
                        break
        elif i=='2':
            doR()
            for j in range(seed,len(t)):
                for k in dt2:
                    if t[j]==k:
                        t[j]=dt2[k]
                        break
        elif i=='@':
            unR()
            for j in range(seed,len(t)):
                for k in pt2:
                    if t[j]==k:
                        t[j]=pt2[k]
                        break
        elif i=='3':
            doL()
            for j in range(seed,len(t)):
                for k in dt3:
                    if t[j]==k:
                        t[j]=dt3[k]
                        break
        elif i=='#':
            unL()
            for j in range(seed,len(t)):
                for k in pt3:
                    if t[j]==k:
                        t[j]=pt3[k]
                        break
        elif i=='5':
            doU()
            for j in range(seed,len(t)):
                for k in dt5:
                    if t[j]==k:
                        t[j]=dt5[k]
                        break
        elif i=='%':
            unU()
            for j in range(seed,len(t)):
                for k in pt5:
                    if t[j]==k:
                        t[j]=pt5[k]
                        break
        elif i=='y':
            for j in range(seed,len(t)):
                for k in dt5:
                    if t[j]==k:
                        t[j]=dt5[k]
                        break
        elif i=='Y':
            for j in range(seed,len(t)):
                for k in pt5:
                    if t[j]==k:
                        t[j]=pt5[k]
                        break
def lowCross():
    #print('\n我要开始还原底层十字啦')
    if cube[1][0][0]!=[1,0,0]:
        where = -1
        #寻找蓝黄棱块
        for i in range(3,26,2):
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==[1,0,0]:
                where = i
                break
        #对应位置,对应还原
        if where==3:
            #对应位置后对应朝向
            if face[5][0][1]==5:
                unD() 
            else:
                doL(),doB() 
        elif where==5:
            if face[5][2][1]==5:
                doD() 
            else:
                unR(),unB() 
        elif where==7:
            if face[5][1][0]==5:
                doD(),doD() 
            else:
                doF(),doL(),unD() 
        elif where==9:
            if face[1][2][1]==1:
                doB() 
            else:
                unL(),unD() 
        elif where==11:
            if face[1][0][1]==1:
                unB() 
            else:
                doR(),doD() 
        elif where==15:
            if face[0][0][1]==5:
                doL(),unD() 
            else:
                unF(),doD(),doD() 
        elif where==17:
            if face[0][2][1]==5:
                unR(),doD() 
            else:
                doF(),doD(),doD() 
        elif where==19:
            if face[1][1][0]==1:
                doB(),doB() 
            else:
                doU(),doR(),unB(),unR() 
        elif where==21:
            if face[4][0][1]==5:
                doU(),doB(),doB() 
            else:
                unL(),doB(),doL() 
        elif where==23:
            if face[4][2][1]==5:
                unU(),doB(),doB() 
            else:
                doR(),unB(),unR() 
        elif where==25:
            if face[4][1][2]==5:
                doU(),doU(),doB(),doB() 
            else:
                unU(),doR(),unB(),unR()
    elif face[5][1][2]==1:
        doB(),doR(),doD()
    #print('蓝黄棱块还原啦')
    if cube[0][1][0]!=[0,1,0]:
        where = -1
        for i in range(5,26,2):
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==[0,1,0]:
                where = i
                break
        if where==5:
            if face[5][2][1]==5:
                doR(),doF(),doF(),doL() 
            else:
                doR(),doR(),doU(),unF(),doL()
        elif where==7:
            if face[5][1][0]==5:
                doF(),doD(),unF(),unD() 
            else:
                doF(),doL()
        elif where==9:
            if face[2][0][1]==2:
                unL() 
            else:
                unD(),doB(),doD()
        elif where==11:
            if face[3][2][1]==5:
                unD(),unB(),doD() 
            else:
                doD(),doD(),doR(),doD(),doD()
        elif where==15:
            if face[2][2][1]==2:
                doL() 
            else:
                doD(),unF(),unD()
        elif where==17:
            if face[0][2][1]==2:
                doD(),doF(),unD() 
            else:
                doD(),doD(),unR(),doD(),doD()
        elif where==19:
            if face[4][1][0]==2:
                doB(),doL(),doL(),unB(),doL() 
            else:
                unU(),doL(),doL()
        elif where==21:
            if face[2][1][0]==2:
                doL(),doL() 
            else:
                unU(),unF(),doL()
        elif where==23:
            if face[4][2][1]==5:
                doU(),doU(),doL(),doL() 
            else:
                doU(),unF(),doL()
        elif where==25:
            if face[4][1][2]==2:
                unF(),doL() 
            else:
                doU(),doL(),doL()
    elif face[5][0][1]==2:
        unL(),doD(),unF(),unD()
    #print('蓝红棱块还原啦')
    if cube[2][1][0]!=[2,1,0]:
        where = -1
        for i in range(7,26,2):
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==[2,1,0]:
                where = i
                break
        if where==7:
            if face[5][1][0]==5:
                doF(),unD(),unF(),doD() 
            else:
                unF(),unR()
        elif where==9:
            if face[2][0][1]==5:
                doD(),doB(),unD() 
            else:
                doB(),doB(),doR(),doB(),doB()
        elif where==11:
            if face[3][2][1]==3:
                doR() 
            else:
                doB(),doU(),unB(),doR(),doR()
        elif where==15:
            if face[0][0][1]==5:
                doF(),doF(),unR() 
            else:
                unD(),unF(),doD()
        elif where==17:
            if face[3][0][1]==3:
                unR() 
            else:
                unD(),doF(),doD()
        elif where==19:
            if face[4][1][0]==5:
                doU(),doR(),doR() 
            else:
                unB(),doR(),doB()
        elif where==21:
            if face[4][0][1]==5:
                doU(),doU(),doR(),doR() 
            else:
                unU(),doF(),unR()
        elif where==23:
            if face[4][2][1]==5:
                doR(),doR() 
            else:
                doU(),doF(),unR()
        elif where==25:
            if face[4][1][2]==5:
                unU(),doR(),doR() 
            else:
                doF(),unR()
    elif face[3][1][2]==5:
        doR(),unF(),unU(),doR(),doR()
    #print('蓝橙棱块还原啦')
    if cube[1][2][0]!=[1,2,0]:
        where = -1
        for i in range(9,26,2):
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==[1,2,0]:
                where = i
                break
        if where==9:
            if face[2][0][1]==0:
                doL(),unU(),unL(),doF(),doF() 
            else:
                doL(),doL(),unF(),doL(),doL()
        elif where==11:
            if face[3][2][1]==0:
                unR(),doU(),doR(),doF(),doF() 
            else:
                doR(),doR(),doF(),doR(),doR()
        elif where==15:
            if face[0][0][1]==0:
                unF() 
            else:
                unL(),unU(),doL(),doF(),doF()
        elif where==17:
            if face[0][2][1]==0:
                doF() 
            else:
                doR(),doU(),unR(),doF(),doF()
        elif where==19:
            if face[4][1][0]==5:
                doU(),doU(),doF(),doF() 
            else:
                doU(),unR(),doF(),doR()
        elif where==21:
            if face[4][0][1]==5:
                unU(),doF(),doF() 
            else:
                doL(),unF(),unL()
        elif where==23:
            if face[4][2][1]==5:
                doU(),doF(),doF() 
            else:
                unR(),doF(),doR()
        elif where==25:
            if face[4][1][2]==5:
                doF(),doF() 
            else:
                unU(),unR(),doF(),doR()
    elif face[0][1][2]==5:
        unF(),doR(),doU(),unR(),doF(),doF()
    #print('蓝白棱块还原啦\n')
def lowCorner():
    #print('我要开始还原底层四角啦')
    if cube[0][0][0]!=[0,0,0]:
        where = -1
        for i in [2,6,8,18,20,24,26]:
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==[0,0,0]:
                where=i
                break
        if where==2:
            if face[5][2][2]==5:
                unR(),unU(),doR(),unU(),unB(),doU(),doB() 
            elif face[1][0][2]==5:
                unR(),unU(),doR(),doL(),doU(),doU(),unL(),unU(),doL(),doU(),unL()
            else:
                unR(),unU(),doR(),unB(),unU(),doB()
        elif where==6:
            if face[5][0][0]==5:
                doF(),doU(),unF(),unB(),unU(),doB() 
            elif face[2][2][2]==5:
                doF(),doU(),unF(),doL(),doU(),doU(),unL(),unU(),doL(),doU(),unL()
            else:
                doF(),doU(),unF(),doL(),doU(),unL()
        elif where==8:
            if face[5][2][0]==5:
                doR(),unU(),unR(),unB(),doU(),doU(),doB() 
            elif face[0][2][2]==5:
                doR(),unU(),unR(),doL(),doU(),doU(),unL()
            else:
                doR(),doU(),unR(),unB(),doU(),doB()
        elif where==18:
            if face[1][2][0]==5:
                doU(),doL(),unU(),unL() 
            elif face[2][0][0]==5:
                unU(),unB(),doU(),doB()
            else:
                doL(),doU(),doU(),unL(),doU(),doU(),unB(),doU(),doB()
        elif where==20:
            if face[1][0][0]==5:
                doU(),doU(),unB(),doU(),doB() 
            elif face[3][2][0]==5:
                doL(),unU(),unL()
            else:
                unU(),doL(),doU(),doU(),unL(),doU(),doU(),unB(),doU(),doB()
        elif where==24:
            if face[0][0][0]==5:
                unB(),doU(),doB() 
            elif face[2][2][0]==5:
                doU(),doU(),doL(),unU(),unL()
            else:
                doU(),doL(),doU(),doU(),unL(),doU(),doU(),unB(),doU(),doB()
        elif where==26:
            if face[0][2][0]==5:
                unU(),doL(),unU(),unL() 
            elif face[3][0][0]==5:
                doU(),unB(),doU(),doB()
            else:
                doU(),doU(),doL(),doU(),doU(),unL(),doU(),doU(),unB(),doU(),doB()
    elif face[1][2][2]==5:
        unB(),unU(),doB(),doU(),doU(),doL(),unU(),unL()
    elif face[2][0][2]==5:
        doL(),doU(),unL(),doU(),doU(),unB(),doU(),doB()
    #print('蓝黄红角块还原啦')
    if cube[2][0][0]!=[2,0,0]:
        where = -1
        for i in [6,8,18,20,24,26]:
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==[2,0,0]:
                where=i
                break
        if where==6:
            if face[5][0][0]==5:
                unL(),unU(),doL(),doU(),doU(),unR(),doU(),doR() 
            elif face[0][0][2]==5:
                doF(),doU(),unF(),unR(),doU(),doR()
            else:
                unL(),unU(),doL(),doB(),unU(),unB()
        elif where==8:
            if face[5][2][0]==5:
                doR(),doU(),unR(),doB(),doU(),doU(),unB() 
            elif face[0][2][2]==5:
                doR(),unU(),unR(),doB(),unU(),unB()
            else:
                doR(),doU(),unR(),unR(),doU(),doU(),doR()
        elif where==18:
            if face[4][0][0]==5:
                doU(),doB(),doU(),doU(),unB(),doU(),doU(),unR(),doU(),doR() 
            elif face[1][2][0]==5:
                doU(),doU(),doB(),unU(),unB()
            else:
                unR(),doU(),doR()
        elif where==20:
            if face[4][2][0]==5:
                doB(),doU(),doU(),unB(),doU(),doU(),unR(),doU(),doR() 
            elif face[1][0][0]==5:
                unU(),unR(),doU(),doR()
            else:
                doU(),doB(),unU(),unB()
        elif where==24:
            if face[4][0][2]==5:
                doU(),doU(),doB(),doU(),doU(),unB(),doU(),doU(),unR(),doU(),doR() 
            elif face[2][2][0]==5:
                unU(),doB(),unU(),unB()
            else:
                doU(),unR(),doU(),doR()
        elif where==26:
            if face[4][2][2]==5:
                unU(),doB(),doU(),doU(),unB(),doU(),doU(),unR(),doU(),doR() 
            elif face[0][2][0]==5:
                doB(),unU(),unB()
            else:
                doU(),doU(),unR(),doU(),doR()
    elif face[1][0][2]==5:
        doB(),doU(),unB(),doU(),doU(),unR(),doU(),doR()
    elif face[3][2][2]==5:
        unR(),unU(),doR(),doU(),doU(),doB(),unU(),unB()
    #print('蓝黄橙角块还原啦')
    if cube[0][2][0]!=[0,2,0]:
        where = -1
        for i in [8,18,20,24,26]:
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==[0,2,0]:
                where=i
                break
        if where==8:
            if face[5][2][0]==5:
                doR(),doU(),doU(),unR(),doF(),unU(),unF() 
            elif face[0][2][2]==5:
                unF(),unU(),doF(),doF(),doU(),doU(),unF()
            else:
                doR(),doU(),unR(),unU(),unL(),doU(),doL()
        elif where==18:
            if face[4][0][0]==5:
                unU(),unL(),doU(),doU(),doL(),doU(),doU(),doF(),unU(),unF() 
            elif face[1][2][0]==5:
                doF(),unU(),unF()
            else:
                doU(),doU(),unL(),doU(),doL()
        elif where==20:
            if face[4][2][0]==5:
                doU(),doU(),unL(),doU(),doU(),doL(),doU(),doU(),doF(),unU(),unF() 
            elif face[1][0][0]==5:
                doU(),unL(),doU(),doL()
            else:
                unU(),doF(),unU(),unF()
        elif where==24:
            if face[4][0][2]==5:
                unL(),doU(),doU(),doL(),doU(),doU(),doF(),unU(),unF() 
            elif face[2][2][0]==5:
                doU(),doF(),unU(),unF()
            else:
                unU(),unL(),doU(),doL()
        elif where==26:
            if face[4][2][2]==5:
                doU(),unL(),doU(),doU(),doL(),doU(),doU(),doF(),unU(),unF() 
            elif face[0][2][0]==5:
                doU(),doU(),doF(),unU(),unF()
            else:
                unL(),doU(),doL()
    elif face[0][0][2]==5:
        doF(),doU(),unF(),doU(),doU(),unL(),doU(),doL()
    elif face[2][2][2]==5:
        unL(),unU(),doL(),doU(),doU(),doF(),unU(),unF()
    #print('蓝白红角块还原啦')
    if cube[2][2][0]!=[2,2,0]:
        where = -1
        for i in [18,20,24,26]:
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==[2,2,0]:
                where=i
                break
        if where==18:
            if face[4][0][0]==5:
                doU(),doU(),doR(),doU(),doU(),unR(),doU(),doU(),unF(),doU(),doF() 
            elif face[1][2][0]==5:
                doR(),doU(),doU(),unR()
            else:
                unF(),doU(),doU(),doF()
        elif where==20:
            if face[4][2][0]==5:
                doU(),doR(),doU(),doU(),unR(),doU(),doU(),unF(),doU(),doF() 
            elif face[3][2][0]==5:
                unU(),doR(),doU(),doU(),unR()
            else:
                unU(),unF(),doU(),doU(),doF()
        elif where==24:
            if face[4][0][2]==5:
                unU(),doR(),doU(),doU(),unR(),doU(),doU(),unF(),doU(),doF() 
            elif face[2][2][0]==5:
                doU(),doR(),doU(),doU(),unR()
            else:
                doU(),unF(),doU(),doU(),doF()
        elif where==26:
            if face[4][2][2]==5:
                doR(),doU(),doU(),unR(),doU(),doU(),unF(),doU(),doF() 
            elif face[0][2][0]==5:
                doU(),doU(),doR(),doU(),doU(),unR()
            else:
                doU(),doU(),unF(),doU(),doU(),doF()
    elif face[0][2][2]==5:
        unF(),unU(),doF(),doU(),doU(),doR(),unU(),unR()
    elif face[3][0][2]==5:
        doR(),doU(),unR(),doU(),doU(),unF(),doU(),doF()
    #print('蓝白橙角块还原啦\n')
    #print('底层还原啦\n')
def middle():
    if cube[0][0][1]!=[0,0,1]:
        where=-1
        for i in [11,15,17,19,21,23,25]:
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==[0,0,1]:
                where=i
                break
        if where==11:
            if face[1][0][1]==1:
                doB(),unU(),unB(),unU(),unR(),doU(),doR(),\
                    doU(),doU(),doL(),unU(),unL(),unU(),unB(),doU(),doB() 
            else:
                doB(),unU(),unB(),unU(),unR(),doU(),doR(),\
                unU(),unB(),doU(),doB(),doU(),doL(),unU(),unL()
        elif where==15:
            if face[2][2][1]==2:
                doF(),unU(),unF(),unU(),unL(),doU(),doL(),\
                doL(),unU(),unL(),unU(),unB(),doU(),doB() 
            else:
                doF(),unU(),unF(),unU(),unL(),doU(),doL(),\
                doU(),unB(),doU(),doB(),doU(),doL(),unU(),unL()
        elif where==17:
            if face[0][2][1]==1:
                doR(),unU(),unR(),unU(),unF(),doU(),doF(),\
                doU(),doU(),unB(),doU(),doB(),doU(),doL(),unU(),unL() 
            else:
                doR(),unU(),unR(),unU(),unF(),doU(),doF(),\
                doU(),doL(),unU(),unL(),unU(),unB(),doU(),doB()
        elif where==19:
            if face[1][1][0]==1:
                doU(),doL(),unU(),unL(),unU(),unB(),doU(),doB() 
            else:
                doU(),doU(),unB(),doU(),doB(),doU(),doL(),unU(),unL()
        elif where==21:
            if face[2][1][0]==1:
                doU(),doU(),doL(),unU(),unL(),unU(),unB(),doU(),doB() 
            else:
                unU(),unB(),doU(),doB(),doU(),doL(),unU(),unL()
        elif where==23:
            if face[3][1][0]==1:
                doL(),unU(),unL(),unU(),unB(),doU(),doB() 
            else:
                doU(),unB(),doU(),doB(),doU(),doL(),unU(),unL()
        elif where==25:
            if face[0][1][0]==1:
                unU(),doL(),unU(),unL(),unU(),unB(),doU(),doB() 
            else:
                unB(),doU(),doB(),doU(),doL(),unU(),unL()
    elif face[1][2][1]==2:
        unB(),doU(),doB(),doU(),doL(),unU(),unL(),doU(),\
                unB(),doU(),doB(),doU(),doL(),unU(),unL()
    #print('黄红棱块还原啦')
    if cube[2][0][1]!=line2cube[11]:
        where=-1
        for i in [15,17,19,21,23,25]:
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==line2cube[11]:
                where=i
                break
        if where==15:
            if face[0][0][1]==3:
                doF(),unU(),unF(),unU(),unL(),doU(),doL()
                doU(),doB(),unU(),unB(),unU(),unR(),doU(),doR()
            else:
                doF(),unU(),unF(),unU(),unL(),doU(),doL()
                doU(),doU(),unR(),doU(),doR(),doU(),doB(),unU(),unB()
        elif where==17:
            if face[0][2][1]==1:
                unF(),doU(),doF(),doU(),doR(),unU(),unR()
                unR(),doU(),doR(),doU(),doB(),unU(),unB()
            else:
                unF(),doU(),doF(),doU(),doR(),unU(),unR()
                unU(),doB(),unU(),unB(),unU(),unR(),doU(),doR()
        elif where==19:
            if face[1][1][0]==1:
                unU(),unR(),doU(),doR(),doU(),doB(),unU(),unB()
            else:
                doU(),doU(),doB(),unU(),unB(),unU(),unR(),doU(),doR()
        elif where==21:
            if face[2][1][0]==1:
                unR(),doU(),doR(),doU(),doB(),unU(),unB()
            else:
                unU(),doB(),unU(),unB(),unU(),unR(),doU(),doR()
        elif where==23:
            if face[3][1][0]==1:
                doU(),doU(),unR(),doU(),doR(),doU(),doB(),unU(),unB()
            else:
                doU(),doB(),unU(),unB(),unU(),unR(),doU(),doR()
        elif where==25:
            if face[0][1][0]==1:
                doU(),unR(),doU(),doR(),doU(),doB(),unU(),unB()
            else:
                doB(),unU(),unB(),unU(),unR(),doU(),doR()
    elif face[3][2][1]==1:
        doB(),unU(),unB(),unU(),unR(),doU(),doR(),unU(),\
            doB(),unU(),unB(),unU(),unR(),doU(),doR()
    #print('黄橙棱块还原啦')
    if cube[0][2][1]!=line2cube[15]:
        where=-1
        for i in [17,19,21,23,25]:
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==line2cube[15]:
                where=i
                break
        if where==17:
            if face[0][2][1]==0:
                doR(),unU(),unR(),unU(),unF(),doU(),doF()
                doF(),unU(),unF(),unU(),unL(),doU(),doL()
            else:
                doR(),unU(),unR(),unU(),unF(),doU(),doF()
                doU(),unL(),doU(),doL(),doU(),doF(),unU(),unF()
        elif where==19:
            if face[1][1][0]==2:
                doF(),unU(),unF(),unU(),unL(),doU(),doL()
            else:
                doU(),unL(),doU(),doL(),doU(),doF(),unU(),unF()
        elif where==21:
            if face[2][1][0]==2:
                doU(),doF(),unU(),unF(),unU(),unL(),doU(),doL()
            else:
                doU(),doU(),unL(),doU(),doL(),doU(),doF(),unU(),unF()
        elif where==23:
            if face[3][1][0]==2:
                unU(),doF(),unU(),unF(),unU(),unL(),doU(),doL()
            else:
                unL(),doU(),doL(),doU(),doF(),unU(),unF()
        elif where==25:
            if face[0][1][0]==2:
                doU(),doU(),doF(),unU(),unF(),unU(),unL(),doU(),doL()
            else:
                unU(),unL(),doU(),doL(),doU(),doF(),unU(),unF()
    elif face[0][0][1]==2:
        unL(),doU(),doL(),doU(),doF(),unU(),unF(),doU(),\
                unL(),doU(),doL(),doU(),doF(),unU(),unF()
    #print('白红棱块还原啦')
    if cube[2][2][1]!=line2cube[17]:
        where=-1
        for i in [19,21,23,25]:
            if cube[line2cube[i][0]][line2cube[i][1]][line2cube[i][2]]==line2cube[17]:
                where=i
                break
        if where==19:
            if face[1][1][0]==3:
                unF(),doU(),doF(),doU(),doR(),unU(),unR()
            else:
                unU(),doR(),unU(),unR(),unU(),unF(),doU(),doF()
        elif where==21:
            if face[2][1][0]==3:
                doU(),unF(),doU(),doF(),doU(),doR(),unU(),unR()
            else:
                doR(),unU(),unR(),unU(),unF(),doU(),doF()
        elif where==23:
            if face[3][1][0]==3:
                unU(),unF(),doU(),doF(),doU(),doR(),unU(),unR()
            else:
                doU(),doU(),doR(),unU(),unR(),unU(),unF(),doU(),doF()
        elif where==25:
            if face[0][1][0]==3:
                doU(),doU(),unF(),doU(),doF(),doU(),doR(),unU(),unR()
            else:
                doU(),doR(),unU(),unR(),unU(),unF(),doU(),doF()
    elif face[0][2][1]==3:
        doR(),unU(),unR(),unU(),unF(),doU(),doF(),unU(),\
            doR(),unU(),unR(),unU(),unF(),doU(),doF()
    #print('白橙棱块还原啦\n')
    #print('中层还原啦\n')

def F2LB(k,i,j,f):
    tk=[[1,0,3,2,4,5],[3,2,0,1,4,5],[2,3,1,0,4,5],[0,1,2,3,4,5]]
    n8=[[[0,0],[0,1],[0,2]],[[1,0],[1,1],[1,2]],[[2,0],[2,1],[2,2]]]
    tmp,n6=rotate([1,2,3,4,5,6,7,8,9],n8)
    tmp,n0=rotate([1,2,3,4,5,6,7,8,9],n6)
    tmp,n2=rotate([1,2,3,4,5,6,7,8,9],n0)
    if f==0:
        if k==4 or k==5:
            return [tk[0][k],n0[i][j][0],n0[i][j][1]]
        return [tk[0][k],i,j]
    elif f==2:
        if k==4 or k==5:
            return [tk[1][k],n2[i][j][0],n2[i][j][1]]
        return [tk[1][k],i,j]
    elif f==6:
        if k==4 or k==5:
            return [tk[2][k],n6[i][j][0],n6[i][j][1]]
        return [tk[2][k],i,j]
    elif f==8:
        if k==4 or k==5:
            return [tk[3][k],n8[i][j][0],n8[i][j][1]]
        return [tk[3][k],i,j]
def F2LA(a,b,leftc,rightc,icube=-1):
    ma,mb=False,False
    if a==1:
        if face[0][2][0]==5 and face[4][2][2]==leftc:
            ma=True
    elif a==2:
        if face[3][0][0]==5 and face[4][2][2]==rightc:
            ma=True
    elif a==3:
        if face[4][2][2]==5 and face[3][0][0]==leftc:
            ma=True
    elif a==-1:
        if face[0][2][2]==5 and face[5][2][0]==rightc:
            ma=True
    elif a==-2:
        if face[3][2][2]==5 and face[0][2][2]==rightc:
            ma=True
    elif a==-3:
        if face[5][2][0]==5 and face[3][0][2]==rightc:
            ma=True
    if b==1:
        if (face[4][1][0],face[1][1][0])==(leftc,rightc):
            mb=True
    elif b==2:
        if (face[4][0][1],face[2][1][0])==(leftc,rightc):
            mb=True
    elif b==3:
        if (face[4][1][2],face[0][1][0])==(leftc,rightc):
            mb=True
    elif b==4:
        if (face[4][2][1],face[3][1][0])==(leftc,rightc):
            mb=True
    elif b==5:
        if (face[F2LB(0,2,1,icube)[0]][F2LB(0,2,1,icube)[1]][F2LB(0,2,1,icube)[2]],\
            face[F2LB(3,0,1,icube)[0]][F2LB(3,0,1,icube)[1]][F2LB(3,0,1,icube)[2]])==(leftc,rightc):
            mb=True
    elif b==-1:
        if (face[4][1][0],face[1][1][0])==(rightc,leftc):
            mb=True
    elif b==-2:
        if (face[4][0][1],face[2][1][0])==(rightc,leftc):
            mb=True
    elif b==-3:
        if (face[4][1][2],face[0][1][0])==(rightc,leftc):
            mb=True
    elif b==-4:
        if (face[4][2][1],face[3][1][0])==(rightc,leftc):
            mb=True
    elif b==-5:
        if (face[F2LB(0,2,1,icube)[0]][F2LB(0,2,1,icube)[1]][F2LB(0,2,1,icube)[2]],\
            face[F2LB(3,0,1,icube)[0]][F2LB(3,0,1,icube)[1]][F2LB(3,0,1,icube)[2]])==(rightc,leftc):
            mb=True
    if ma and mb:
        return True
    return False
trueset=set()
def F2L(deep=0):
    if deep>1:
        middle()
        print('error',end='    ')
        return 0
    num=[0,0,0,0,0,0,0,0,0]
    error=[[],[],[],[],[],[],[],[],[]]
    for count4 in range(8):
        for icube in [0,2,6,8]:
            tmp,leftc,rightc='',-1,-1
            F2Lod=[-1,-1]
            if icube==0:
                tmp,leftc,rightc='55',1,2
            elif icube==2:
                tmp,leftc,rightc='%',3,1
            elif icube==6:
                tmp,leftc,rightc='5',2,0
            elif icube==8:
                tmp,leftc,rightc='',0,3
            if findcube(line2cube[icube])[2]==2:
                if findcube(line2cube[icube])==[0,0,2]:
                    doU(),doU()
                elif findcube(line2cube[icube])==[2,0,2]:
                    doU()
                elif findcube(line2cube[icube])==[0,2,2]:
                    unU()
                if F2LA(2,1,leftc,rightc):
                    F2Lod=[0,0]
                elif F2LA(1,-2,leftc,rightc):
                    F2Lod=[0,1]
                elif F2LA(2,-3,leftc,rightc):
                    F2Lod=[0,2]
                elif F2LA(1,4,leftc,rightc):
                    F2Lod=[0,3]
                        
                elif F2LA(2,2,leftc,rightc):
                    F2Lod=[1,0]
                elif F2LA(2,3,leftc,rightc):
                    F2Lod=[1,1]
                elif F2LA(2,4,leftc,rightc):
                    F2Lod=[1,2]
                elif F2LA(1,-1,leftc,rightc):
                    F2Lod=[1,3]
                elif F2LA(1,-4,leftc,rightc):
                    F2Lod=[1,4]
                elif F2LA(1,-3,leftc,rightc):
                    F2Lod=[1,5]

                elif F2LA(1,2,leftc,rightc):
                    F2Lod=[2,0]
                elif F2LA(1,1,leftc,rightc):
                    F2Lod=[2,1]
                elif F2LA(2,-1,leftc,rightc):
                    F2Lod=[2,2]
                elif F2LA(2,-2,leftc,rightc):
                    F2Lod=[2,3]

                elif F2LA(3,-2,leftc,rightc):
                    F2Lod=[3,0]
                elif F2LA(3,1,leftc,rightc):
                    F2Lod=[3,1]
                elif F2LA(3,2,leftc,rightc):
                    F2Lod=[3,2]
                elif F2LA(3,-1,leftc,rightc):
                    F2Lod=[3,3]

                elif F2LA(3,4,leftc,rightc):
                    F2Lod=[6,0]
                elif F2LA(3,-3,leftc,rightc):
                    F2Lod=[6,1]

                elif F2LA(2,-4,leftc,rightc):
                    F2Lod=[7,0]
                elif F2LA(1,3,leftc,rightc):
                    F2Lod=[7,1]

                elif F2LA(3,-4,leftc,rightc):
                    F2Lod=[10,0]
                elif F2LA(3,3,leftc,rightc):
                    F2Lod=[10,1]
                    
                elif F2LA(2,-5,leftc,rightc,icube):
                    F2Lod=[5,0]
                elif F2LA(1,-5,leftc,rightc,icube):
                    F2Lod=[5,1]
                elif F2LA(2,5,leftc,rightc,icube):
                    F2Lod=[5,2]
                elif F2LA(1,5,leftc,rightc,icube):
                    F2Lod=[5,3]

                elif F2LA(3,-5,leftc,rightc,icube):
                    F2Lod=[8,0]
                elif F2LA(3,5,leftc,rightc,icube):
                    F2Lod=[8,1]

            elif face[F2LB(5,2,0,icube)[0]][F2LB(5,2,0,icube)[1]][F2LB(5,2,0,icube)[2]]==5\
                and face[F2LB(3,0,2,icube)[0]][F2LB(3,0,2,icube)[1]][F2LB(3,0,2,icube)[2]]==rightc\
                and findcube(line2cube[icube+9])[2]==2:
                for i in range(3):
                    if face[0][1][0]==leftc and face[4][1][2]==rightc:
                        F2Lod=[4,0]
                        break
                    elif face[3][1][0]==rightc and face[4][2][1]==leftc:
                        F2Lod=[4,1]
                    else:
                        doU()
            elif face[F2LB(5,2,0,icube)[0]][F2LB(5,2,0,icube)[1]][F2LB(5,2,0,icube)[2]]==rightc\
                and face[F2LB(0,2,2,icube)[0]][F2LB(0,2,2,icube)[1]][F2LB(0,2,2,icube)[2]]==5\
                and findcube(line2cube[icube+9])[2]==2:
                for i in range(3):
                    if face[0][1][0]==leftc and face[4][1][2]==rightc:
                        F2Lod=[9,3]
                        break
                    elif face[3][1][0]==rightc and face[4][2][1]==leftc:
                        F2Lod=[9,0]
                    else:
                        doU()
            elif face[F2LB(5,2,0,icube)[0]][F2LB(5,2,0,icube)[1]][F2LB(5,2,0,icube)[2]]==leftc\
                and face[F2LB(3,0,2,icube)[0]][F2LB(3,0,2,icube)[1]][F2LB(3,0,2,icube)[2]]==5\
                and findcube(line2cube[icube+9])[2]==2:
                for i in range(3):
                    if face[0][1][0]==leftc and face[4][1][2]==rightc:
                        F2Lod=[9,1]
                        break
                    elif face[3][1][0]==rightc and face[4][2][1]==leftc:
                        F2Lod=[9,2]
                    else:
                        doU()
            elif face[F2LB(5,2,0,icube)[0]][F2LB(5,2,0,icube)[1]][F2LB(5,2,0,icube)[2]]==leftc\
                and face[F2LB(3,0,2,icube)[0]][F2LB(3,0,2,icube)[1]][F2LB(3,0,2,icube)[2]]==5:
                if face[F2LB(0,2,1,icube)[0]][F2LB(0,2,1,icube)[1]][F2LB(0,2,1,icube)[2]]==leftc\
                    and face[F2LB(3,0,1,icube)[0]][F2LB(3,0,1,icube)[1]][F2LB(3,0,1,icube)[2]]==rightc:
                    F2Lod=[11,0]
                elif face[F2LB(0,2,1,icube)[0]][F2LB(0,2,1,icube)[1]][F2LB(0,2,1,icube)[2]]==rightc\
                    and face[F2LB(3,0,1,icube)[0]][F2LB(3,0,1,icube)[1]][F2LB(3,0,1,icube)[2]]==leftc:
                    F2Lod=[11,1]
            elif face[F2LB(5,2,0,icube)[0]][F2LB(5,2,0,icube)[1]][F2LB(5,2,0,icube)[2]]==rightc\
                and face[F2LB(0,2,2,icube)[0]][F2LB(0,2,2,icube)[1]][F2LB(0,2,2,icube)[2]]==5:
                if face[F2LB(0,2,1,icube)[0]][F2LB(0,2,1,icube)[1]][F2LB(0,2,1,icube)[2]]==leftc\
                    and face[F2LB(3,0,1,icube)[0]][F2LB(3,0,1,icube)[1]][F2LB(3,0,1,icube)[2]]==rightc:
                    F2Lod=[11,2]
                elif face[F2LB(0,2,1,icube)[0]][F2LB(0,2,1,icube)[1]][F2LB(0,2,1,icube)[2]]==rightc\
                    and face[F2LB(3,0,1,icube)[0]][F2LB(3,0,1,icube)[1]][F2LB(3,0,1,icube)[2]]==leftc:
                    F2Lod=[11,3]
            elif face[F2LB(5,2,0,icube)[0]][F2LB(5,2,0,icube)[1]][F2LB(5,2,0,icube)[2]]==5\
                and face[F2LB(0,2,2,icube)[0]][F2LB(0,2,2,icube)[1]][F2LB(0,2,2,icube)[2]]==leftc:
                if face[F2LB(0,2,1,icube)[0]][F2LB(0,2,1,icube)[1]][F2LB(0,2,1,icube)[2]]==rightc\
                    and face[F2LB(3,0,1,icube)[0]][F2LB(3,0,1,icube)[1]][F2LB(3,0,1,icube)[2]]==leftc:
                    F2Lod=[11,4]
            if F2Lod!=[-1,-1]:
                cfop(F2Lorder[F2Lod[0]][F2Lod[1]],tmp)
                num[icube]+=1
                error[icube].append(F2Lod)
                trueset.add(str(F2Lod))
                #print(icube,F2Lod,end=' ')
    for i in range(9):
        if num[i]>1:
            print('error',error[i])
            return 1
    for k in [0,1,2,3]:
        for i in [0,1,2]:
            for j in [1,2]:
                if face[k][i][j]!=k:
                    lowCorner()
                    deep+=1
                    F2L(deep)
                    return 0
def highCross():
    if face[4][1][0]+face[4][0][1]+face[4][2][1]+face[4][1][2]==6:
        unR(),unU(),unF(),doU(),doF(),doR(),\
        doF(),doR(),doU(),unR(),unU(),unF()
    elif face[4][0][1]==face[4][2][1]==4 and face[4][1][0]!=4:
        doF(),doR(),doU(),unR(),unU(),unF()
    elif face[4][1][0]==face[4][1][2]==4 and face[4][2][1]!=4:
        doU(),doF(),doR(),doU(),unR(),unU(),unF()
    elif face[4][1][0]==face[4][0][1]==4 and face[4][2][1]!=4:
        unR(),unU(),unF(),doU(),doF(),doR()
    elif face[4][0][1]==face[4][1][2]==4 and face[4][1][0]!=4:
        doU(),unR(),unU(),unF(),doU(),doF(),doR()
    elif face[4][1][2]==face[4][2][1]==4 and face[4][1][0]!=4:
        doU(),doU(),unR(),unU(),unF(),doU(),doF(),doR()
    elif face[4][2][1]==face[4][1][0]==4 and face[4][0][1]!=4:
        unU(),unR(),unU(),unF(),doU(),doF(),doR()
    #print('顶层出现十字啦\n')
def highFace():
    number = 0
    for i in [face[4][0][0],face[4][2][0],face[4][0][2],face[4][2][2]]:
        if i==4:
            number+=1
    if number==0:
        for i in range(4):
            if face[2][0][0]+face[2][2][0]<8:
                doU()
        if face[3][0][0]==face[3][2][0]==4:
            unR(),unU(),doR(),unU(),\
                    unR(),doU(),doR(),unU(),\
            unR(),doU(),doU(),doR()
        elif face[1][0][0]==face[0][2][0]==4:
            doR(),doU(),doU(),doR(),doR(),unU(),doR(),doR(),unU(),doR(),\
                    doR(),doU(),doU(),doR()
    elif number==1:
        for i in range(4):
            if face[4][0][0]!=4:
                doU()
        if face[2][2][0]==4:
            doF(),doU(),unF(),doU(),doF(),doU(),doU(),unF()
        elif face[0][0][0]==4:
            unR(),unU(),doR(),unU(),\
                unR(),doU(),doU(),doR()
    elif number==2:
        if face[4][0][0]==face[4][2][2] or face[4][2][0]==face[4][0][2]:
            for i in range(4):
                if  face[2][0][0]!=4:
                    doU()
            unR(),unU(),doR(),unU(),\
                    unR(),doU(),doR(),unU(),\
                    unR(),doU(),doR(),unU(),\
            unR(),doU(),doU(),doR()
        else:
            for i in range(4):
                if face[4][2][0]==4 or face[4][2][2]==4 :
                    doU()
            if face[3][0][0]==face[3][2][0]==4:
                unR(),doU(),doU(),doR(),\
                    doU(),unR(),doU(),doR(),\
                    doU(),unR(),unU(),doR(),unU(),\
                unR(),doU(),doU(),doR()
            elif face[1][0][0]==face[0][2][0]==4:
                unR(),unF(),doL(),doF(),doR(),unF(),unL(),doF()
    #print('顶面还原啦')
def simplePLL():
    flag = False
    for i in [0,1,2,3]:
        if face[i][0][0]==face[i][2][0]:
            flag=True
    if flag:
        for i in range(4):
            if not face[2][0][0]==face[2][2][0]:
                doU()
        if face[3][0][0]!=face[3][2][0]:
            doR(),doU(),unR(),unU(),\
            unR(),doF(),doR(),doR(),\
            unU(),unR(),unU(),\
            doR(),doU(),unR(),unF()
    else:
        for i in range(4):
            if face[0][0][0]!=0:
                doU()
        doF(),doR(),unU(),unR(),unU(),\
        doR(),doU(),unR(),unF(),\
        doR(),doU(),unR(),unU(),\
        unR(),doF(),doR(),unF()
    #print('就想转个行')
    flag = False
    for i in [0,1,2,3]:
        if face[i][0][0]==face[i][1][0]==face[i][2][0]:
            flag = True
    if flag:
        for i in range(4):
            if face[1][0][0]!=face[1][1][0]:
                doU()
        if face[2][1][0]==face[3][0][0]:
            doR(),doR(),doU(),doR(),doU(),unR(),unU(),\
                unR(),unU(),unR(),doU(),unR()
        elif face[2][1][0]==face[0][0][0]:
            doR(),unU(),doR(),doU(),\
                doR(),doU(),doR(),unU(),unR(),unU(),doR(),doR()
        for i in range(4):
            if face[0][0][0]!=0:
                doU()
    elif face[1][1][0]==face[3][2][0]:
        doL(),unR(),doF(),\
            doL(),doL(),unR(),unR(),doB(),\
            doL(),doL(),unR(),unR(),doF(),\
            doL(),unR(),doD(),doD(),\
            doL(),doL(),unR(),unR(),unU()
    elif face[1][1][0]==face[2][0][0]:
        doU(),doL(),unR(),doF(),\
            doL(),doL(),unR(),unR(),doB(),\
            doL(),doL(),unR(),unR(),doF(),\
            doL(),unR(),doD(),doD(),\
            doL(),doL(),unR(),unR(),unU()
    else:
        doL(),doL(),unR(),unR(),doD(),\
        doL(),doL(),unR(),unR(),doU(),doU(),\
        doL(),doL(),unR(),unR(),doD(),\
        doL(),doL(),unR(),unR()
    for i in range(4):
        if face[0][0][0]!=0:
            doU()
    #print('\n顶层还原啦\n')
    #print('大功告成')
def randomFind():
    with open('randomFind.txt','w') as rf:
        for i in range(randint(4,80)):
            rf.write(choice(['F','B','L','R','U','D','f','b','l','r','u','d']))
def randomRotate():
    with open('randomFind.txt','r') as randRotate:
        randFile = randRotate.read()
        for i in range(len(randFile)):
            if randFile[i]=='F':
                doF()
            elif randFile[i]=='B':
                doB()
            elif randFile[i]=='L':
                doL()
            elif randFile[i]=='R':
                doR()
            elif randFile[i]=='U':
                doU()
            elif randFile[i]=='D':
                doD()
            elif randFile[i]=='f':
                unF()
            elif randFile[i]=='b':
                unB()
            elif randFile[i]=='l':
                unL()
            elif randFile[i]=='r':
                unR()
            elif randFile[i]=='u':
                unU()
            elif randFile[i]=='d':
                unD()
def pop_up_box(color):
    def inputint():
        try:
            facecolor=[str(var1.get().strip())[:3],str(var2.get().strip())[:3],str(var3.get().strip())[:3]]
            with open('face'+str(color)+'.txt','w')as f:
                for j in range(3):
                    print(facecolor[j])
                    for i in range(3):
                        if facecolor[j][i] in ['0','1','2','3','4','5']:
                            face[color][i][j]=int(facecolor[j][i])
                        else:
                            face[color][i][j]=color2int.index(facecolor[j][i])
                for i in range(3):
                    for j in range(3):
                        f.write(str(face[color][i][j]))
                    
            #颜色存入块
            question=[]
            for i in range(3):
                question.append([])
                for j in range(3):
                    question[i].append([])
                    for k in range(3):
                        question[i][j].append(set([]))
            for k in range(6):
                for i in range(3):
                    for j in range(3):
                        question[face2store[k][i][j][0]][face2store[k][i][j][1]][face2store[k][i][j][2]].add(face[k][i][j])
            #面信息化为块位置信息
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        for a in range(3):
                            for b in range(3):
                                for c in range(3):
                                    if question[i][j][k]==store[a][b][c]:
                                        cube[i][j][k]=[a,b,c]
            root.destroy()
        except:
            print('请输入合法颜色')
            with open('face'+str(color)+'.txt','w')as f:
                for i in range(3):
                    for j in range(3):
                        f.write(str(face[color][i][j]))
    def inputclear():
        nonlocal num
        var1.set('')
        var2.set('')
        var3.set('')
        num = ['','','']
    num = ['','','']
    root = Tk(className=str(color)+'号色面')
    #root.title(className=str(color)+'号色面')# 弹出框框名
    root.geometry('220x120')    # 设置弹出框的大小 w x h
    Label(root,text='第一行:').place(x=10,y=0)
    Label(root,text='第二行:').place(x=10,y=30)
    Label(root,text='第三行:').place(x=10,y=60)
    var1 = StringVar()   # 这即是输入框中的内容
    var2 = StringVar()   # 这即是输入框中的内容
    var3 = StringVar()   # 这即是输入框中的内容
    for j in range(3):
        for i in range(3):
            num[j]+=color2int[face[color][i][j]]
    var1.set(num[0]) # 通过var.get()/var.set() 来 获取/设置var的值
    var2.set(num[1]) # 通过var.get()/var.set() 来 获取/设置var的值
    var3.set(num[2]) # 通过var.get()/var.set() 来 获取/设置var的值
    entry1 = Entry(root, textvariable=var1)  # 设置"文本变量"为var
    entry1.pack()   # 将entry"打上去"
    entry2 = Entry(root, textvariable=var2)  # 设置"文本变量"为var
    entry2.pack()   # 将entry"打上去"
    entry3 = Entry(root, textvariable=var3)  # 设置"文本变量"为var
    entry3.pack()   # 将entry"打上去"
    entry1.place(x=60,y=0)
    entry2.place(x=60,y=30)
    entry3.place(x=60,y=60)
    btn1 = Button(root, text='OK', command=inputint)     # 按下此按钮(Input), 触发inputint函数
    btn2 = Button(root, text='Clear', command=inputclear)   # 按下此按钮(Clear), 触发inputclear函数
    # 按钮定位
    btn1.place(x=20,y=90)
    btn2.place(x=160,y=90)
    # 上述完成之后, 开始真正弹出弹出框
    root.mainloop()
def simplify():
    flag=False
    for i in range(len(SZHsolve)-2):
        if SZHsolve[i]==SZHsolve[i+1]==SZHsolve[i+2]:
            del SZHsolve[i]
            del SZHsolve[i]
            SZHsolve[i] = chr(ord(SZHsolve[i])+32) if ord(SZHsolve[i])<90 else chr(ord(SZHsolve[i])-32)
            flag=True
            break
        elif abs(ord(SZHsolve[i])-ord(SZHsolve[i+1]))==32:
            del SZHsolve[i]
            del SZHsolve[i]
            flag=True
            break
    if flag:
        simplify()
def readColor():
    facetxt = ['face0.txt','face1.txt','face2.txt',\
               'face3.txt','face4.txt','face5.txt']
    #从文件中读取颜色信息
    for k in range(6):
        with open(facetxt[k],'r') as readtxt:
            for i in range(3):
                for j in range(3):
                    face[k][i][j]=int(readtxt.read(1))
    #颜色存入块
    question=[]
    for i in range(3):
        question.append([])
        for j in range(3):
            question[i].append([])
            for k in range(3):
                question[i][j].append(set([]))
    for k in range(6):
        for i in range(3):
            for j in range(3):
                question[face2store[k][i][j][0]][face2store[k][i][j][1]][face2store[k][i][j][2]].add(face[k][i][j])
    #面信息化为块位置信息
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for a in range(3):
                    for b in range(3):
                        for c in range(3):
                            if question[i][j][k]==store[a][b][c]:
                                cube[i][j][k]=[a,b,c]
def main():
    global cameraThread
    #stepNum=[]
    bigfont = font.SysFont('SimHei',30)
    smallfont = font.SysFont('SimHei',20)
    #minifont = font.SysFont('SimHei',15)
    text1 = bigfont.render("一",True,(255,0,0))
    text2 = bigfont.render("二",True,(255,0,0))
    text3 = bigfont.render("三",True,(255,0,0))
    text4 = bigfont.render("四",True,(255,0,0))
    text5 = bigfont.render("五",True,(255,0,0))
    text6 = bigfont.render("六",True,(255,0,0))
    textF = bigfont.render("0",True,(255,0,0))
    textB = bigfont.render("1",True,(255,0,0))
    textL = bigfont.render("2",True,(255,0,0))
    textR = bigfont.render("3",True,(255,0,0))
    textU = bigfont.render("4",True,(255,0,0))
    textD = bigfont.render("5",True,(255,0,0))
    textF2L = bigfont.render("F2L",True,(255,0,0))
    text_restart = smallfont.render("清零",True,(255,0,0))
    text_solve = smallfont.render("求解",True,(255,0,0))
    text_camera = smallfont.render("相机",True,(255,0,0))
    text_run = bigfont.render("run",True,(255,0,0))
    text_print = smallfont.render("print",True,(255,0,0))
    text_read = smallfont.render("read",True,(255,0,0))
    text_rotate = smallfont.render("打乱",True,(255,0,0))
    text_find = smallfont.render("随机",True,(255,0,0))
    #图形颜色组
    white,yellow = (255,255,255),(255,255,0)
    red,orange = (204,0,0),(255,128,0)
    blue,green = (0,0,255),(0,128,0)
    nocolor = (204,204,204)
    color = [white,yellow,red,orange,green,blue,nocolor]
    #图形位置组
    front,back = [300,300],[0,300]
    left,right = [150,300],[450,300]
    up,down = [300,150],[300,450]
    location = [front,back,left,right,up,down]
    readColor()
    while True:
        screen.fill((204,204,204))
        if cameraThread:
            cameraThread.loop()
        #绘制按钮边界
        for i in [[100,100],[100,150],[100,200],\
                  [50,150],[0,150],[150,150],\
                  [0,0],[50,0],[100,0],[150,0],\
                  [200,0],[250,0],[300,0],[350,0],[350,50],[400,0],[400,50],\
                  [450,0],[500,0],[550,0]]:
            draw.rect(screen,(0,0,0),(i[0],i[1],50,50),2)
        draw.rect(screen,(0,0,0),(50,50,100,50),2)
        screen.blit(text1,(15,10))
        screen.blit(text2,(65,10))
        screen.blit(text3,(115,10))
        screen.blit(text4,(165,10))
        screen.blit(text5,(215,10))
        screen.blit(text6,(265,10))
        screen.blit(textF2L,(80,65))
        screen.blit(textF,(115,160))
        screen.blit(textB,(15,160))
        screen.blit(textL,(65,160))
        screen.blit(textR,(165,160))
        screen.blit(textU,(115,110))
        screen.blit(textD,(115,210))
        screen.blit(text_restart,(305,15))
        screen.blit(text_solve,(355,15))
        screen.blit(text_camera,(355,66))
        screen.blit(text_print,(400,22))
        screen.blit(text_read,(400,72))
        screen.blit(text_rotate,(455,15))
        screen.blit(text_find,(510,15))
        screen.blit(text_run,(555,10))
        for eventi in event.get():
            if eventi.type == QUIT:
                quit()
                exit()
            if eventi.type == MOUSEMOTION:
                pos = mouse.get_pos()
            elif eventi.type == MOUSEBUTTONDOWN:
                pressed_array = mouse.get_pressed()
                if pressed_array[0]:
                    for k in range(6):
                        if location[k][0]<pos[0]<location[k][0]+150\
                           and location[k][1]<pos[1]<location[k][1]+150:
                            Thread(target=pop_up_box,args=(k,)).start()
                    #鼠标左键点击面对应按钮,使其正转
                    if 100<pos[0]<150:
                        if 100<pos[1]<150:
                            doU()
                        elif 150<pos[1]<200:
                            doF()
                        elif 200<pos[1]<250:
                            doD()
                    elif 150<pos[1]<200:
                        if 0<pos[0]<50:
                            doB()
                        elif 50<pos[0]<100:
                            doL()
                        elif 150<pos[0]<200:
                            doR()
                    if 50<pos[1]<100:
                        if 50<pos[0]<150:
                            F2L()
                        elif 350<pos[0]<400:
                            if not cameraThread:
                                cameraThread=mf.camera()
                            else:
                                cameraThread.closeCamera()
                                cameraThread=None
                        elif 400<pos[0]<450:
                            readColor()
                    #鼠标左键点击，运行方法
                    if 0<pos[1]<50:
                        if 0<pos[0]<50:
                            lowCross()
                        elif 50<pos[0]<100:
                            lowCorner()
                        elif 100<pos[0]<150:
                            middle()
                        elif 150<pos[0]<200:
                            highCross()
                        elif 200<pos[0]<250:
                            highFace()
                        elif 250<pos[0]<300:
                            simplePLL()
                        elif 300<pos[0]<350:
                            for k in range(6):
                                for i in range(3):
                                    for j in range(3):
                                        face[k][i][j]=k
                            for i in range(3):
                                for j in range(3):
                                    for k in range(3):
                                        cube[i][j][k]=[i,j,k]
                            print('已重置数据')
                        elif 350<pos[0]<400:
                            #game=1
                            del SZHsolve[:]
                            lowCross()
                            simplify()
                            print(len(SZHsolve),end=' ')
                            ts=len(SZHsolve)
                            F2L()
                            simplify()
                            print(len(SZHsolve)-ts,end=' ')
                            ts=len(SZHsolve)
                            highCross()
                            highFace()
                            simplify()
                            print(len(SZHsolve)-ts,end=' ')
                            ts=len(SZHsolve)
                            simplePLL()
                            simplify()
                            print(len(SZHsolve)-ts,end=' ')
                            readerror=0
                            for k in range(6):
                                for i in range(3):
                                    for j in range(3):
                                        if face[k][i][j]!=k:
                                            readerror=1
                            if readerror:
                                print('数据输入错误')
                                
                            #输出解法TXT文件
                            elif SZHsolve != []:
                                simplify()
                                print(len(SZHsolve))
                                with open('solveCube.txt','w') as write:
                                    for index in SZHsolve:
                                        write.write(index)
                        elif 400<pos[0]<450:
                            tmp=''
                            for i in SZHsolve:
                                tmp+=i
                            if tmp!='':
                                print(tmp)
                        elif 450<pos[0]<500:
                            randomRotate()
                        elif 500<pos[0]<550:
                            randomFind()
                            print('已经生成随机打乱文件')
                        elif 550<pos[0]<600:
                            try:
                                for index in SZHsolve:
                                    ser.write(bytes(index,'utf-8'))
                                    print(str(ser.read()))
                            except:
                                print('端口错误')
                            '''flagg=False
                            for timerror in range(1000):
                                if flagg:
                                    break
                                randomFind(),randomRotate(),lowCross()
                                if F2L()==1:
                                    break
                                for k in [0,1,2,3]:
                                    for i in [0,1,2]:
                                        for j in [1,2]:
                                            if face[k][i][j]!=k:
                                                flagg=True
                                print(timerror)'''
                            '''for timerror in range(10000):
                                randomFind()
                                randomRotate()
                                del SZHsolve[:]
                                lowCross()
                                F2L()
                                highCross()
                                highFace()
                                simplePLL()
                                if SZHsolve != []:
                                    simplify()
                                    stepNum.append(len(SZHsolve))
                                    print(sum(stepNum)/len(stepNum))
                                    with open('solveCube.txt','w') as write:
                                        for index in SZHsolve:
                                            write.write(index)'''
                                
                #鼠标右键点击面对应按钮,使其反转
                if pressed_array[2]:
                    if 100<pos[0]<150:
                        if 100<pos[1]<150:
                            unU()
                        if 150<pos[1]<200:
                            unF()
                        if 200<pos[1]<250:
                            unD()
                    elif 150<pos[1]<200:
                        if 0<pos[0]<50:
                            unB()
                        if 50<pos[0]<100:
                            unL()
                        if 150<pos[0]<200:
                            unR()
                #鼠标滚轮点击,输出当前魔方三维数据矩阵
                if pressed_array[1]:
                    print('face=[',end='')
                    for i in range(6):
                        print(face[i],',\\')
        #绘制所有魔方色块
        for k in range(6):
            for i in range(3):
                for j in range(3):
                    draw.rect(screen,color[face[k][i][j]],\
                (location[k][0]+i*50,location[k][1]+j*50,50,50),0)
        #绘制魔方色块边缘黑线
        for k in range(6):
            for i in range(4):
                draw.line(screen,(0,0,0),(location[k][0]+i*50,\
                location[k][1]),(location[k][0]+i*50,location[k][1]+150),2)
                draw.line(screen,(0,0,0),(location[k][0],\
                location[k][1]+i*50),(location[k][0]+150,location[k][1]+i*50),2)
        
        display.flip()
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    '''except:
        print_exc()
        quit()
        input()'''
