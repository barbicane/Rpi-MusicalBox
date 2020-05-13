# fonction qui gere et capte passage d'objet devant laser
import RPi.GPIO as GPIO
import smbus
import time
import soundPlay
import signal

address = 0x48
bus = smbus.SMBus(1)
cmd = 0x40
ledPin = 11
ledPinOut = 12
darkValue = []
lightValue = []
medianValue = 0
wrk = True
bounce_time = 0
def sigExit(s, f):
    global wrk
    wrk =False
    print("quitting")

signal.signal(signal.SIGTERM, sigExit)

def analogRead(chn):
    value = bus.read_byte_data(address, cmd + chn)
    return value


def analogWrite(value):
    bus.write_byte_data(address, cmd, value)


def setup():
    global darkValue, lightValue, medianValue
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.setup(ledPinOut, GPIO.OUT)
    GPIO.output(ledPin, GPIO.LOW)
    GPIO.output(ledPinOut, GPIO.LOW)
    for i in range(200):
        darkValue.append(analogRead(0))
#        print("dark value "+str(darkValue[-1]))
        time.sleep(0.01)
    darkValue = sum(darkValue)/200
    GPIO.output(ledPin, GPIO.HIGH)
    time.sleep(0.02)
    for i in range(200):
        lightValue.append(analogRead(0))
#        print("light value "+str(lightValue[-1]))
        time.sleep(0.01)
    lightValue = sum(lightValue)/200
    GPIO.output(ledPin, GPIO.LOW)
    medianValue = lightValue+(darkValue-lightValue)/2

def loop():
    global ledPin, ledPinOut, darkValue, lightValue, medianValue, wrk, bounce_time
    time.sleep(2)
    before = 0
    GPIO.output(ledPin, GPIO.HIGH)
    while wrk:
        #allumer ledpin 11
        #GPIO.output(ledPin, GPIO.HIGH)
        time.sleep(0.025)
        value = analogRead(0)
        #eteindre ledpin 11
        #GPIO.output(ledPin, GPIO.LOW)
        #time.sleep(0.025)
        #time.sleep(0.05)
#        print(value)
#        print("medianValue "+str(medianValue))
        if(value<medianValue and before>medianValue):
            if time.time()-bounce_time > 1:
                #print('Rien')
                #before = value
                #time.sleep(0.05)
                #print("lance son")
                GPIO.output(ledPinOut,GPIO.HIGH)
                soundPlay.play_sound()
                #time.sleep(0.05)
                GPIO.output(ledPinOut,GPIO.LOW)
                bounce_time = time.time()
        before=value
            #print('Obstacle')
        #p.ChangeDutyCycle(value * 100 / 255)
        #voltage = value / 255.0 * 3.3
        #print('ADC Value : %d, Voltage : %.2f' % (value, voltage))
        #time.sleep(0.05)


def destroy():
    bus.close()
    GPIO.cleanup()


if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        quit()
# fonction qui charge la biblioteque de son et qui la lit
