import sys
sys.path.append('../')
from TelloClass import TelloClass

#orientate drone 
tello_class = TelloClass()
print(f'Initial yaw: {tello_class._tello.get_yaw()}')
    
    
    
