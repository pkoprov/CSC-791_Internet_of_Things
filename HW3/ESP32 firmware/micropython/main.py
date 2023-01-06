from machine import I2C, Pin

from mpu6500 import MPU6500

# IMU addresses
sda = Pin(21)
scl = Pin(22)

repl_button = Pin(0, Pin.IN, Pin.PULL_UP)

# create the I2C
i2c = I2C(1, scl=scl, sda=sda)

# Scan the bus
m = MPU6500(i2c)

led = Pin(2, Pin.OUT, value=1)
time.sleep(1)
led.off()

start = time.time()
calibration_data = []
while time.time() - start <= 1:
    calibration_data.append(m.gyro[1])
mean = sum(calibration_data) / len(calibration_data)
sd = (sum([(i - mean) ** 2 for i in calibration_data]) / len(calibration_data)) ** 0.5

print("Start the loop")

while True:
    # break the loop of running the main.py
    if repl_button.value() == 0:
        print("Dropping to REPL")
        led.on()
        time.sleep(0.5)
        led.off()
        sys.exit()

        # check if thw door is moving
    if m.gyro[1] > mean + 5 * sd or m.gyro[1] < mean - 5 * sd:
        try:
            client.publish("fwh2200/c10/DDATA/esp32", str([m.acceleration[0], m.acceleration[2], m.gyro[1]])[1:-1])
        except:
            print("Not working!")
            time.sleep(1)
