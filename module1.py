from sr.robot import *

import time

SEARCHING, DRIVING = range(2)

R = Robot()

MARKER_TOKENS = (MARKER_TOKEN, MARKER_TOKEN_A, MARKER_TOKEN_B, MARKER_TOKEN_C)

token_filter = lambda m: m.info.marker_type in MARKER_TOKENS

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
tokens = filter(token_filter, R.see())
m = tokens[0]
i = 1
state = SEARCHING
while True:
    tokens = filter(token_filter, R.see())
    if state == SEARCHING:
        if m.info.offset == i:
            drive(100,1.4)
            if R.grab():
                turn(25, 2.4)
                print("staaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaakkkkkkkkkk")
                drive(100, 1)
                if R.release():
                    turn(-25,1.2)
                    print("ed")
            i = i+1
            state = DRIVING
        else:
            state = SEARCHING
    elif state == DRIVING:
        turn(25,1.2)
        state = SEARCHING
