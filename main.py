import random
import types

import RPi.GPIO as GPIO
import time

pwmPins = [11, 12, 13] # GPIO17, GPIO18, GPIO27

buttonMinus = 29 # GPIO5, убавить цвет
buttonPlus = 31 # GPIO6, добавить цвет
buttonColorSelector = 40 # GPIO21, выбор цвета для настройки
buttonMode = 37 # GPIO26, ручной режим: настройка каждого цвета по отдельности, автоматический: цвет меняется рандомно
buttonsTimeStep = 0.1

pwmFrequency = 2000

currentMode = 0
modes = types.SimpleNamespace()
modes.Manual = 0
modes.Auto = 1

colorValueManual = 0
currentColorNumber = 0
colors = types.SimpleNamespace()
colors.Red = 0
colors.Green = 1
colors.Blue = 2

r = 0
g = 0
b = 0

def setup():
    global pwmRed, pwmGreen, pwmBlue

    GPIO.setmode(GPIO.BOARD)
    buttonPins = [buttonMinus, buttonPlus, buttonMode, buttonColorSelector]
    GPIO.setup(buttonPins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(pwmPins, GPIO.OUT)
    GPIO.output(pwmPins, GPIO.LOW)

    pwmRed = GPIO.PWM(pwmPins[0], pwmFrequency)
    pwmRed.start(0)

    pwmGreen = GPIO.PWM(pwmPins[1], pwmFrequency)
    pwmGreen.start(0)

    pwmBlue = GPIO.PWM(pwmPins[2], pwmFrequency)
    pwmBlue.start(0)



def setColor(r_val, g_val, b_val):
    pwmRed.ChangeDutyCycle(r_val)
    pwmGreen.ChangeDutyCycle(g_val)
    pwmBlue.ChangeDutyCycle(b_val)

def setMode(channel):
    global currentMode, r, g, b, colorValueManual, currentColorNumber
    currentMode = not currentMode

    if currentMode == modes.Auto:
        print('mode was changed to Auto')
    elif currentMode == modes.Manual:
        print('mode was changed to Manual')

    r = 0
    g = 0
    b = 0
    colorValueManual = 0
    currentColorNumber = 0

    # pwmRed.start(0)
    # pwmGreen.start(0)
    # pwmBlue.start(0)


def changeColorValue(channel):
    global currentColorNumber, colorValueManual

    if currentColorNumber < 2:
        currentColorNumber += 1
    else:
        currentColorNumber = 0


    if currentColorNumber == colors.Red:
        colorValueManual = r
        print('setting up red color')
    elif currentColorNumber == colors.Green:
        colorValueManual = g
        print('setting up green color')
    elif currentColorNumber == colors.Blue:
        colorValueManual = b
        print('setting up blue color')


def loop():
    global r,g,b, colorValueManual

    while True:
        if currentMode == modes.Auto:
            r = random.randint(0, 100)
            g = random.randint(0, 100)
            b = random.randint(0, 100)
            #print("color: %s, %s, %s"%(r,g,b))
            setColor(100 - r, 100 -g, 100 - b)

            time.sleep(0.1)
        elif currentMode == modes.Manual:
            if GPIO.input(buttonPlus) == GPIO.HIGH and colorValueManual < 100:
                colorValueManual += 1
                print("color: %s, %s, %s" % (r, g, b))
                print(colorValueManual)
                time.sleep(buttonsTimeStep)

            if GPIO.input(buttonMinus) == GPIO.HIGH and colorValueManual > 0:
                colorValueManual -= 1
                print("color: %s, %s, %s" % (r, g, b))
                print(colorValueManual)
                time.sleep(buttonsTimeStep)

            if currentColorNumber == colors.Red:
                r = colorValueManual
            elif currentColorNumber == colors.Green:
                g = colorValueManual
            elif currentColorNumber == colors.Blue:
                b = colorValueManual

            setColor(r, g, b)

def destroy():
    GPIO.cleanup()
    pwmRed.stop()
    pwmGreen.stop()
    pwmBlue.stop()
    GPIO.cleanup()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setup()
    GPIO.add_event_detect(buttonMode, GPIO.RISING, callback=setMode, bouncetime=200)
    GPIO.add_event_detect(buttonColorSelector, GPIO.RISING, callback=changeColorValue, bouncetime=200)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
