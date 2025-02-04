import sys
from TelloClass import TelloClass
from time import sleep


DISTANCE = 100      #distance from shelf in [cm]

COL_WIDTH = 40      #width of one column in [cm]
GAP = 0            #how much space will be between drone and the shelf in [cm]
MARGIN = 0         #how much space will be left where drone won't fly  
ORIENTATION = 171    #initial yaw where drone must be facing towards in °

tello_class = TelloClass()

def shelf_scan(width=0, height=0):
    #shelf width in [cm]
    #shelf height in [cm]
    print(f'width = {width} height = {height}')
    try:
        #tello_class = TelloClass()
        tello_class.c_takeoff(video_name='proba_video.avi', path='./')
        sleep(2)
        tello_class._tello.land()
        # return
        # lower_dist = tello_class._tello.get_height() - MARGIN
        #if(lower_dist > 20):
            #tello_class._tello.move_down(lower_dist)
            #sleep(2)
        tello_class._tello.move_forward(DISTANCE - GAP)
        for i in range(width // COL_WIDTH):
            sleep(2)
            if(i % 2 == 0):
                tello_class._tello.move_up(height - 2 * MARGIN)
            else:
                tello_class._tello.move_down(height - 2 * MARGIN)
            sleep(5)
            tello_class._tello.move_right(COL_WIDTH)
    except KeyboardInterrupt:
        print('Aborting...\nDrone is landing...')
    finally:
        tello_class._tello.land()
        tello_class.draw_graph()

if __name__ == '__main__':
    shelf_scan()
