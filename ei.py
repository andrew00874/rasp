import RPi.GPIO as GPIO
import time
import Adafruit_DHT

sensor=Adafruit_DHT.DHT11
GPIO.setmode(GPIO.BCM)

# Define the pin number for DHT11 sensor and 7-segment display
dht_pin = 17
segments = (11, 4, 23, 8, 7, 10, 18, 25)
digits = (22, 27, 17, 24)

# Set up the GPIO pins for 7-segment display
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

# Define the function to convert numbers to 7-segment display format
num = {'':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}

try:
    while True:
        # Read the temperature and humidity from DHT11 sensor
        humidity, temperature = Adafruit_DHT.read_retry(sensor, dht_pin)

        # Format the temperature and humidity values
        temp_str = "{:.1f}".format(temperature)
        humidity_str = "{:.1f}".format(humidity)
        s = temp_str.rjust(4) + humidity_str.rjust(4)

        # Display the temperature and humidity on 7-segment display
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[s[digit]][loop])
                if(int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
                    GPIO.output(25, 1)
                else:
                    GPIO.output(25, 0)
            GPIO.output(digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(digits[digit], 1)

finally:
    GPIO.cleanup()
