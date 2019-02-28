def doF():
    print('F',end=' ')
def doB():
    print('B',end=' ')
def doL():
    print('L',end=' ')
def doR():
    print('R',end=' ')
def doU():
    print('U',end=' ')
def doD():
    print('D',end=' ')
def unF():
    print('f',end=' ')
def unB():
    print('b',end=' ')
def unL():
    print('l',end=' ')
def unR():
    print('r',end=' ')
def unU():
    print('u',end=' ')
def unD():
    print('d',end=' ')
def main(s,m=''):
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
        elif i=='Y':
            for j in range(seed,len(t)):
                for k in dt5:
                    if t[j]==k:
                        t[j]=dt5[k]
                        break
        elif i=='y':
            for j in range(seed,len(t)):
                for k in pt5:
                    if t[j]==k:
                        t[j]=pt5[k]
                        break
        
