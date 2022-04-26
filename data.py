#
# import board
# import adafruit_ccs811
#
# i2c = board.I2C()  # uses board.SCL and board.SDA
# ccs811 = adafruit_ccs811.CCS811(i2c)
#
# def get_registered_user():
#     return {
#         "CO2": ccs811.eco2,
#         "TVOC": ccs811.tvoc,
#
#     }
#
# if __name__ == "__main__":
#     print("CO2: {} PPM, TVOC: {} PPB".format(ccs811.eco2, ccs811.tvoc))
#
#
#
from random import *




def get_registered_user():
    # create random values
    co2 = randint(350, 650)
    tvoc = randint(5, 15)
    temp = randint(15, 33)
    return {
        "CO2": co2,
        "TVOC": tvoc,
        "Temp": temp,
    }


if __name__ == "__main__":
    print("CO2: {} PPM, TVOC: {} PPB,Temp: {}".format(get_registered_user()["CO2"], get_registered_user()["TVOC"], get_registered_user()["Temp"]))
