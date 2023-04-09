import RPi.GPIO as GPIO
import time
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
DHT11_pin = 2

GPIO.setmode(GPIO.BCM)

segments = (11, 4, 23, 8, 7, 10, 18, 25)

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

digits = (22, 27, 5, 24)

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

num = {'':(0, 0, 0, 0, 0, 0, 0),
       '0':(1, 1, 1, 1, 1, 1, 0),
       '1':(0, 1, 1, 0, 0, 0, 0),
       '2':(1, 1, 0, 1, 1, 0, 1),
       '3':(1, 1, 1, 1, 0, 0, 1),
       '4':(0, 1, 1, 0, 0, 1, 1),
       '5':(1, 0, 1, 1, 0, 1, 1),
       '6':(1, 0, 1, 1, 1, 1, 1),
       '7':(1, 1, 1, 0, 0, 0, 0),
       '8':(1, 1, 1, 1, 1, 1, 1),
       '9':(1, 1, 1, 1, 0, 1, 1)}

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT11_pin)

        if humidity is not None and temperature is not None:
            temp = str(int(temperature)).rjust(2)
            hum = str(int(humidity)).rjust(2)
            s = temp + hum
            for digit in range(4):
                for loop in range(0, 7):
                    GPIO.output(segments[loop], num[s[digit]][loop])
                GPIO.output(digits[digit], 0)
                time.sleep(0.001)
                GPIO.output(digits[digit], 1)
        else:
            print('Failed to get reading. Try again!')
except KeyboardInterrupt:
    print('Program stopped by user')
finally:
    GPIO.cleanup()