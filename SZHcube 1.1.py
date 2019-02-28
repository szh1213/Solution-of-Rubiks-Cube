import pygame,tkinter
import sys
import traceback
from threading import *
from pygame.locals import *
from random import *
pygame.init()
bg_size = width, height = 600, 600

screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("六步解三阶魔方1.1---源自1213清心")

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
def lowCross():
    #print('\n我要开始还原底层十字啦')
    if cube[1][0][0]!=[1,0,0]:
        where = [-1,-1,-1]
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
            facecolor=str(var.get().strip())[:9]
            textseek=0
            for j in range(3):
                for i in range(3):
                    print(facecolor[textseek],end=' ')
                    if facecolor[textseek] in ['0','1','2','3','4','5']:
                        face[color][i][j]=int(facecolor[textseek])
                    else:
                        face[color][i][j]=color2int.index(facecolor[textseek])
                    textseek+=1
            print()
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
    def inputclear():
        nonlocal num
        var.set('')
        num = ''
    num = ''
    root = tkinter.Tk(className=str(color)+'号色面')  # 弹出框框名
    root.geometry('270x60')     # 设置弹出框的大小 w x h
    var = tkinter.StringVar()   # 这即是输入框中的内容
    for j in range(3):
        for i in range(3):
            num+=color2int[face[color][i][j]]
    var.set(num) # 通过var.get()/var.set() 来 获取/设置var的值
    entry1 = tkinter.Entry(root, textvariable=var)  # 设置"文本变量"为var
    entry1.pack()   # 将entry"打上去"
    btn1 = tkinter.Button(root, text='OK', command=inputint)     # 按下此按钮(Input), 触发inputint函数
    btn2 = tkinter.Button(root, text='Clear', command=inputclear)   # 按下此按钮(Clear), 触发inputclear函数
    # 按钮定位
    btn2.pack(side='right')
    btn1.pack(side='right')
    # 上述完成之后, 开始真正弹出弹出框
    root.mainloop()
def main():
    stepNum=[]
    facetxt = ['face0.txt','face1.txt','face2.txt',\
               'face3.txt','face4.txt','face5.txt']
    bigfont = pygame.font.SysFont('SimHei',30)
    smallfont = pygame.font.SysFont('SimHei',20)
    minifont = pygame.font.SysFont('SimHei',15)
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
    text_restart = minifont.render("restart",True,(255,0,0))
    text_solve = smallfont.render("solve",True,(255,0,0))
    text_run = bigfont.render("run",True,(255,0,0))
    text_print = smallfont.render("print",True,(255,0,0))
    text_rotate = minifont.render("rotate",True,(255,0,0))
    text_find = smallfont.render("find",True,(255,0,0))
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
    while True:
        screen.fill((204,204,204))
        #绘制按钮边界
        for i in [[100,100],[100,150],[100,200],\
                  [50,150],[0,150],[150,150],\
                  [0,0],[50,0],[100,0],[150,0],\
                  [200,0],[250,0],[300,0],[350,0],[400,0],\
                  [450,0],[500,0],[550,0]]:
            pygame.draw.rect(screen,(0,0,0),(i[0],i[1],50,50),2)
        screen.blit(text1,(15,10))
        screen.blit(text2,(65,10))
        screen.blit(text3,(115,10))
        screen.blit(text4,(165,10))
        screen.blit(text5,(215,10))
        screen.blit(text6,(265,10))
        screen.blit(textF,(115,160))
        screen.blit(textB,(15,160))
        screen.blit(textL,(65,160))
        screen.blit(textR,(165,160))
        screen.blit(textU,(115,110))
        screen.blit(textD,(115,210))
        screen.blit(text_restart,(300,5))
        screen.blit(text_solve,(350,11))
        screen.blit(text_print,(400,22))
        screen.blit(text_rotate,(450,15))
        screen.blit(text_find,(505,7))
        screen.blit(text_run,(555,10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                pos = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
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
                            game=1
                            del SZHsolve[:]
                            lowCross()
                            print(len(SZHsolve),end=' ')
                            ts=len(SZHsolve)
                            lowCorner()
                            middle()
                            print(len(SZHsolve)-ts,end=' ')
                            ts=len(SZHsolve)
                            highCross()
                            highFace()
                            print(len(SZHsolve)-ts,end=' ')
                            ts=len(SZHsolve)
                            simplePLL()
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
                                print(len(SZHsolve)-ts,end=' ')
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
                            #预留命令行运行机器驱动程序
                            game = 1
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
                    pygame.draw.rect(screen,color[face[k][i][j]],\
                (location[k][0]+i*50,location[k][1]+j*50,50,50),0)
        #绘制魔方色块边缘黑线
        for k in range(6):
            for i in range(4):
                pygame.draw.line(screen,(0,0,0),(location[k][0]+i*50,\
                location[k][1]),(location[k][0]+i*50,location[k][1]+150),2)
                pygame.draw.line(screen,(0,0,0),(location[k][0],\
                location[k][1]+i*50),(location[k][0]+150,location[k][1]+i*50),2)
        
        pygame.display.flip()
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
