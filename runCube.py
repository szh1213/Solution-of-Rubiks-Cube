import RPi.GPIO as GPIO  
import time  
pin = [[7,29,0.00000005,6400],[11,31,0.00000005,6400],[13,33,0.0000001,6400],
           [15,35,0.0000001,6400],[18,37,0.000000001,6400],[22,40,0.00000001,6400]]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) 

for i in range(6):
    GPIO.setup(pin[i][0],GPIO.OUT)
    GPIO.setup(pin[i][1],GPIO.OUT)

def run(face,direction):
    GPIO.output(pin[face][1],direction)
    for i in range(0, pin[face][3]):  
        GPIO.output(pin[face][0],GPIO.HIGH)
        time.sleep(pin[face][2])  
        GPIO.output(pin[face][0],GPIO.LOW)
        time.sleep(pin[face][2])
    GPIO.output(pin[face][0],GPIO.LOW)
    GPIO.output(pin[face][1],GPIO.LOW)
    time.sleep(0.03)
    
'''run(0,1)
run(1,1)
run(2,1)
run(0,0)
run(1,0)
run(2,0)

run(3,1)
run(4,1)
run(5,1)
run(3,0)
run(4,0)
run(5,0)'''
'''GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
def setStep(w1,w2,w3,w4):
    GPIO.output(11,w1)
    GPIO.output(12,w2)
    GPIO.output(13,w3)
    GPIO.output(15,w4)
def ppp(delay,steps):
    for i in range(steps):
        setStep(1,0,0,0)
        time.sleep(delay)
        setStep(0,1,0,0)
        time.sleep(delay)
        setStep(0,0,1,0)
        time.sleep(delay)
        setStep(0,0,0,1)
        time.sleep(delay)
ppp(0.003,512)'''
for j in range(4,6):
    for i in range(4):
        run(j,0)
with open ('solveCube.txt','r') as solve2run:
    how2run = solve2run.read()
    for i in how2run:
        if i=='F':
            run(0,0)
        elif i=='B':
            run(1,0)
        elif i=='L':
            run(2,0)
        elif i=='R':
            run(3,0)
        elif i=='U':
            run(4,0)
        elif i=='D':
            run(5,0)
        elif i=='f':
            run(0,1)
        elif i=='b':
            run(1,1)
        elif i=='l':
            run(2,1)
        elif i=='r':
            run(3,1)
        elif i=='u':
            run(4,1)
        elif i=='d':
            run(5,1) 
GPIO.cleanup()
