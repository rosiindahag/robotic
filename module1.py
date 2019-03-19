from sr.robot import *

import time

SEARCHING, DRIVING = range(2)

R = Robot()

TOKENS = [1,2,3,4,5,6,7,8]
ARENA = [23,2,9,16,27,4,14,18]
token_filter = lambda m: m.info.marker_type in MARKER_TOKEN_A
arena_filter = lambda x: x.info.marker_type in MARKER_ARENA
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

state = SEARCHING
i = 0
while True:
    if state == SEARCHING:
        print "Searching..."
        tokens = filter(token_filter, R.see())
        arena = filter(arena_filter, R.see())
        if len(tokens) > 0:
            m = tokens[0]
            x = arena[0]
            print "Token sighted. {0} is {1}m away, bearing {2} degrees." \
                  .format(m.info.offset, m.dist, m.rot_y)
            if i == 8:
                break
            elif m.info.offset == TOKENS[i]:
                state = DRIVING
            else:
                turn(20,0.5)
                turn(-50, 0.5)
                drive(-80,0.5)
                state = SEARCHING
            print('-------')
            print(m)
            print(x)
        else:
            print "Can't see anything."
            turn(-15, 0.1)
            drive(-30,0.2)
            time.sleep(0.2)

    elif state == DRIVING:
        print "Aligning..."
        tokens = filter(token_filter, R.see())
        if len(tokens) == 0:
            state = SEARCHING
        else:
            m = tokens[0]
            if m.dist < 0.4:
                print "Found it!"
                drive(m.dist*120,0.5)
                if R.grab():
                    print "Gotcha!"
                    x = arena[0]
                    print(x.rot_y)
                    drive(-x.dist*210, 1.5)
                    turn(70,0.3)
                    R.release()
                    i = i+1                    
                    drive(-80, 0.5)
                    turn(-25,0.5)
                    state = SEARCHING
                else:
                    print "Aww, I'm not close enough."
                #exit()

            elif -15 <= m.rot_y <= 15:
                print "Ah, that'll do."
                drive(50, 0.5)

            elif m.rot_y < -15:
                print "Left a bit..."
                turn(-10, 0.5)

            elif m.rot_y > 15:
                print "Right a bit..."
                turn (10, 0.5)
