from random import randint
import pyautogui
import keyboard
import time

###Settings###
min_time:int = 2
max_time:int = 3
exit_button = 'esc'

###Script###
def main(min_time:int, max_time:int):
    global exit_button
    if not (isinstance(min_time,int) and isinstance(max_time,int)):
        print('Invalid type')
        return

    width, height = pyautogui.size()

    while True:
        if keyboard.is_pressed(exit_button):
            break  # Exit loop if 'q' is pressed

        x = randint(0, width)
        y = randint(0, height)
        durationMovement = randint(0, 1)
        pyautogui.moveTo(x, y, durationMovement)

        # Check for key press every 0.1 secondsqq
        for _ in range(randint(min_time,max_time) * 10):
            if keyboard.is_pressed(exit_button):
                break  # Exit loop if 'q' is pressed
            time.sleep(0.1)

if __name__ == '__main__':
    main(min_time, max_time)