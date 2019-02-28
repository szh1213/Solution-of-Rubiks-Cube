# -*- coding: utf-8 -*-
from cv2 import rectangle,destroyAllWindows,VideoCapture,imshow,waitKey
from numpy import lexsort,array,load
from math import pow
openflag=True
class camera():
    def __init__(self):
        self.video = 'http://192.168.0.105:8080/shot.jpg'
        self.cap = VideoCapture(1)
        self.color2int=['白','黄','红','橙','绿','蓝']
        self.color_name = ["face0.txt","face1.txt","face2.txt",\
                     "face3.txt","face4.txt","face5.txt"]
        self.cols = [200,280,360]
        self.rows = [120,200,280]
        self.colorid = ["color_0","color_1","color_2","color_3","color_4","color_5"]

       #RGB对比
    def closeCamera(self):
        self.openflag=False
        self.cap.release()
        destroyAllWindows()
    def prin(self,s):
        #global self.rows,self.cols,face,self.color_name
        it = 12
        savefc = ""
        fc = [1,1,1,1,11,1,1,1,1,1,1,1]
        rcolor = load("RCcl.npz")
        rcolor2= load("RCcl2.npz")
        rcolor3= load("RCcl3.npz")
        rcolor4= load("RCcl4.npz")
        rcolor5= load("RCcl5.npz")
      
        face = s
        row,col,Bo=[],[],[]
        rcol,gcol,bcol=[],[],[]
        rrr,ggg,bbb=0,0,0
        for i in range(3):
            for i1 in range(3):
                for ir in range(40):
                    for ic in range(40):
                        R=self.frame[self.rows[i1]+ir+20,self.cols[i]+ic+20][2]
                        G=self.frame[self.rows[i1]+ir+20,self.cols[i]+ic+20][1]
                        B=self.frame[self.rows[i1]+ir+20,self.cols[i]+ic+20][0]
                        rcol.append(R)
                        gcol.append(G)
                        bcol.append(B)
                for ir in range(400):
                   rcol.remove(min(rcol))
                   rcol.remove(max(rcol))
                   gcol.remove(min(gcol))
                   gcol.remove(max(gcol))
                   bcol.remove(min(bcol))
                   bcol.remove(max(bcol))
                for imm in rcol:
                   rrr+=imm
                for imm in gcol:
                   ggg+=imm
                for imm in bcol:
                   bbb+=imm
                rrr=rrr/800
                ggg=ggg/800
                bbb=bbb/800

                for icolo in range(len(self.colorid)):
                   fc[0]  =  pow(rrr-rcolor[self.colorid[icolo]][0],4)+\
                             pow(ggg-rcolor[self.colorid[icolo]][1],4)+\
                             pow(bbb-rcolor[self.colorid[icolo]][2],4)
                   fc[1]  =  pow(rrr-rcolor2[self.colorid[icolo]][0],4)+\
                             pow(ggg-rcolor[self.colorid[icolo]][1],4)+\
                             pow(bbb-rcolor[self.colorid[icolo]][2],4)
                   fc[2]  =  pow(rrr-rcolor3[self.colorid[icolo]][0],4)+\
                             pow(ggg-rcolor[self.colorid[icolo]][1],4)+\
                             pow(bbb-rcolor[self.colorid[icolo]][2],4)
                   fc[3]  =  pow(rrr-rcolor4[self.colorid[icolo]][0],4)+\
                             pow(ggg-rcolor[self.colorid[icolo]][1],4)+\
                             pow(bbb-rcolor[self.colorid[icolo]][2],4)
                   fc[4]  =  pow(rrr-rcolor5[self.colorid[icolo]][0],4)+\
                             pow(ggg-rcolor[self.colorid[icolo]][1],4)+\
                             pow(bbb-rcolor[self.colorid[icolo]][2],4)
                      
                   row.append([icolo,fc[0]])
                   row.append([icolo,fc[1]])
                   row.append([icolo,fc[2]])
                   row.append([icolo,fc[3]])
                   row.append([icolo,fc[4]])
                row = array(row)
                row = row[lexsort(row.T)]
                if i==1 and i1==1:
                   savefc+=str(face)
                else:
                   savefc+=str(int(row[0][0]))
                rcol,gcol,bcol=[],[],[]
                rrr,ggg,bbb=0,0,0
                row=[]
        with open (self.color_name[face],"w") as myfile:
            myfile.write(savefc)
            print(str(face)+'号色面：')
            print(self.color2int[int(savefc[0])],end=' ')
            print(self.color2int[int(savefc[3])],end=' ')
            print(self.color2int[int(savefc[6])])
            print(self.color2int[int(savefc[1])],end=' ')
            print(self.color2int[int(savefc[4])],end=' ')
            print(self.color2int[int(savefc[7])])
            print(self.color2int[int(savefc[2])],end=' ')
            print(self.color2int[int(savefc[5])],end=' ')
            print(self.color2int[int(savefc[8])])
    
    def loop(self):
        #cap.open(self.video)
        ret , self.frame = self.cap.read()
        for i in range(3):
            for i1 in range(3):
                rectangle(self.frame,(self.cols[i]+20,self.rows[i1]+20),(self.cols[i]+60,self.rows[i1]+60),(0,0,255),2)
        try:
            imshow('read for cube -- from Yan Jiacai (press q to close)',self.frame)
        except:
            print('检查摄像头')
            self.cap = VideoCapture(0)
        k = waitKey(1)&0xFF
        if k in [ord('0'),ord('1'),ord('2'),ord('3'),ord('4'),ord('5')]:
            self.prin(int(chr(k)))
        if k == ord('q'):
            self.closeCamera()
            return False
        return True
if __name__ == "__main__":
    c=camera()
    while c.loop():
        pass
