import sys
sys.path.append('../')
from TelloClass import TelloClass
from time import sleep

if __name__ == '__main__':
    try:
        tello_class = TelloClass()
        print(f'Initial yaw: {tello_class._tello.get_yaw()}')
    except KeyboardInterrupt:
        print('Aborting...\nDrone is landing...')
    finally:
        pass
    
    
