from djitellopy import Tello

tello = Tello()
tello.connect()
print(f'Battery level: {tello.get_battery()}%')
tello.end()
