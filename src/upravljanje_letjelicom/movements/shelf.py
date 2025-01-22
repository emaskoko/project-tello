import sys
sys.path.append('../')
from upravljanje_letjelicom.TelloClass import TelloClass
from time import sleep

DISTANCE = 150      #distance from shelf in [cm]
WIDTH = 300         #shelf width in [cm]
HEIGHT = 200        #shelf height in [cm]
COL_WIDTH = 50      #width of one column in [cm]
GAP = 60            #how much space will be between drone and the shelf in [cm]
MARGIN = 40         #how much space will be left where drone won't fly  
ORIENTATION = -4    #initial yaw where drone must be facing towards in °

if __name__ == '__main__':
    try:
        tello_class = TelloClass()
        tello_class.c_takeoff(orientation=ORIENTATION)
        lower_dist = tello_class._tello.get_height() - MARGIN
        if(lower_dist > 20):
            tello_class._tello.move_down(lower_dist)
            sleep(2)
        tello_class._tello.move_forward(DISTANCE - GAP)
        for i in range(WIDTH // COL_WIDTH):
            sleep(2)
            if(i % 2 == 0):
                tello_class._tello.move_up(HEIGHT - 2 * MARGIN)
            else:
                tello_class._tello.move_down(HEIGHT - 2 * MARGIN)
            sleep(2)
            tello_class._tello.move_right(COL_WIDTH)

        tello_class.detect_packages(model_path='yolov5s.pt')    
    except KeyboardInterrupt:
        print('Aborting...\nDrone is landing...')
    finally:
        tello_class._tello.land()
        tello_class.draw_graph()
