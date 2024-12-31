import cv2
from djitellopy import Tello
import matplotlib.pyplot as plt
from time import sleep 
import time
import math
import threading


class TelloClass:
    def __init__(self):

        self.x_positions = [0]
        self.y_positions = [0]
        self.z_positions = [0]
        self.t_moments = [0]

        self._initial_yaw = None
        
        self._tello = Tello()
        self._tello.connect()
        
        print(f'Battery level: {self._tello.get_battery()}%')

    def c_takeoff(self, record_video=True, orientation=None):

        self._tello.takeoff()
        pos_thread = threading.Thread(target=self.pos_calculate)
        pos_thread.start()

        if(record_video):
            record_thread = threading.Thread(target=self.record_video)
            record_thread.start()
        while (not self._tello.is_flying) or (not self._tello.stream_on):   #while tello isn't flying or stream isn't turned on, wait
            if(not record_video):   #if you don't want to record break out of this loop
                break
            sleep(0.5)
        sleep(3)

        if(orientation):
            self._initial_yaw = self._tello.get_yaw()
            print(f'Initial yaw: {self._initial_yaw}')
            self._tello.rotate_counter_clockwise(self._initial_yaw - orientation)
            
        sleep(3)
        print(f'Current yaw: {self._tello.get_yaw()}')
    
    def pos_calculate(self):
        initial_time = time.time()
        INTERVAL = 0.2
        while self._tello.is_flying:
            sleep(INTERVAL)

            new_x = self.x_positions[-1] + self._tello.get_speed_y() * INTERVAL * 10 #!!! Inverted x and y
            new_y = self.y_positions[-1] + self._tello.get_speed_x() * INTERVAL * 10 #!!! Inverted x and y
            new_z = self._tello.get_height()
            self.x_positions.append(round(new_x, 2))
            self.y_positions.append(round(new_y, 2))
            self.z_positions.append(round(new_z, 2))
            self.t_moments.append(time.time() - initial_time)
        
    
    
    
        
    def draw_graph(self):
        sleep(1)
        
        def draw_2d_graph(axis):
            positions = None
            if(axis == 'x'):
                positions = self.x_positions
            elif(axis == 'y'):
                positions = self.y_positions
            elif(axis == 'z'):
                positions = self.z_positions
            else:
                print('Invalid input!')
                return
            plt.plot(self.t_moments, positions, color='red')
            plt.title(f'Kretanje {axis} pozicije')
            plt.xlabel('Vrijeme[s]')
            plt.ylabel(f'{axis} pozicija[cm]')
            
            

        def draw_3d_graph():
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')  # Kreiraj 3D os
            ax.set_box_aspect([1, 1, 1])  
            ax.plot(self.x_positions, self.y_positions, self.z_positions, color='blue', label='Movement in 3D space')
            
            ax.scatter(self.x_positions[0], self.y_positions[0], self.z_positions[0], color='green', s=100)
            ax.scatter(self.x_positions[-1], self.y_positions[-1], self.z_positions[-1], color='red', s=100)
            
            ax.set_xlabel('X pozicija[cm]')
            ax.set_ylabel('Y pozicija[cm]')
            ax.set_zlabel('Z pozicija[cm]')
            ax.legend()
        
        plt.subplot(221)
        draw_2d_graph('x')
        plt.subplot(222)
        draw_2d_graph('y')
        plt.subplot(223)
        draw_2d_graph('z')
        plt.subplots_adjust(wspace=0.55, hspace=0.55)
        draw_3d_graph()

        plt.legend()
        plt.show()
    
    def record_video(self):
        while not self._tello.is_flying:
            sleep(0.5)
        VIDEO_NAME = 'shelf.avi'
        FRAME_DELAY = 1 / 30

        self._tello.streamon()

        # Postavljanje OpenCV VideoWriter za spremanje videa
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(VIDEO_NAME, fourcc, 30.0, (960, 720))  # FPS je postavljen na 30

        try:
            print("Pritisni 'q' za prekid.")
            prev_time = time.time()
            while self._tello.is_flying:
                # Dohvaćanje trenutnog framea iz video streama
                frame = self._tello.get_frame_read().frame
                
                # Prikaz framea u OpenCV prozoru
                cv2.imshow('Tello Video', frame)
                
                # Spremanje framea u video
                out.write(frame)
                
                # Kontrola frekvencije frameova
                elapsed_time = time.time() - prev_time
                if elapsed_time < FRAME_DELAY:
                    sleep(FRAME_DELAY - elapsed_time)
                prev_time = time.time()
                
                
                # Izlaz kada se pritisne 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            # Zaustavljanje video streama i oslobađanje resursa
            self._tello.streamoff()
            print("Video thread završio.")
            out.release()
            cv2.destroyAllWindows()  

    #osbsolite!!!  
    def __update_position__(self, x, y):

        if(x != 0):
            new_x = self.x_positions[-1] + x * math.cos(math.radians(self.c_get_yaw()))
            new_y = self.y_positions[-1] + x * math.sin(math.radians(self.c_get_yaw()))
        else:
            new_x = self.x_positions[-1] + y * math.sin(math.radians(self.c_get_yaw()))
            new_y = self.y_positions[-1] + y * math.cos(math.radians(self.c_get_yaw()))
        new_z = self._tello.get_height()

        self.x_positions.append(round(new_x, 2))
        self.y_positions.append(round(new_y, 2))
        self.z_positions.append(round(new_z, 2))  

    #obsolite!!!
    def c_move(self, distance: int, direction: str):
        if(direction == 'up'):
            self._tello.move_up(distance)
            self.__update_position__(0, 0)
        elif(direction == 'down'):
            self._tello.move_down(distance)
            self.__update_position__(0, 0)
        elif(direction == 'right'):
            self._tello.move_right(distance)
            self.__update_position__(0, -distance)
        elif(direction == 'left'):
            self._tello.move_left(distance)
            self.__update_position__(0, distance)
        elif(direction == 'forward'):
            self._tello.move_forward(distance)
            self.__update_position__(distance, 0)
        elif(direction == 'back'):
            self._tello.move_back(distance)
            self.__update_position__(-distance, 0)
        else:  #Error!!!
            self._tello.land()
            print('Invalid direction!!!')

        sleep(2)
