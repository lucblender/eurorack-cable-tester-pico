from machine import Pin, I2C
import mcp23017
from utime import sleep
import sys

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=800_000)


led_16 = Pin(0, Pin.OUT)
led_10 = Pin(1, Pin.OUT)
led_error = Pin(2, Pin.OUT)

onboard_led = Pin(13, Pin.OUT)

onboard_led.value(1)

mcp_0 = mcp23017.MCP23017(i2c, 0x20)
mcp_1 = mcp23017.MCP23017(i2c, 0x21)

# only append in an array if the pair or the flipped pair is not in the array


def short_array_append(array, pair):
    if pair not in array and pair[::-1] not in array:
        array.append(pair)


if __name__ == "__main__":
    for i in range(0, 16):
        mcp_0[i].input()
        mcp_1[i].input(pull=1)

    # list of open connection when pluggin a 10 pins cables
    open_for_10_pin_connector = [0, 1, 2, 13, 14, 15]

    while (True):
        short_number = 0
        open_number = 0
        connected_number = 0
        open_number_array = []
        short_array = []

        try:

            for x in range(0, 16):
                for i in range(0, 16):
                    if i == x:
                        mcp_0[i].output(0)
                    else:
                        mcp_0[i].input(pull=1)

                for y in range(0, 16):
                    if x == y:
                        if mcp_1[x].value() == 0:
                            connected_number += 1
                        else:
                            open_number += 1
                            open_number_array.append(y)
                    else:
                        if mcp_1[y].value() == 0:
                            short_number += 1
                            short_array_append(short_array, [x, y])

                mcp_0[i].output(0)

            open_number_in_10_pin = 0
            for open_number_pin in open_number_array:
                if open_number_pin in open_for_10_pin_connector:
                    open_number_in_10_pin += 1

            if connected_number == 16:
                led_16.value(1)
                led_10.value(0)
                if short_number != 0:
                    led_error.value(1)
                    print("*-"*30)
                    print("short circuit pins:", short_array)
                    print("*-"*30)
                else:
                    led_error.value(0)
            elif connected_number == 10 and open_number_in_10_pin == 6:
                led_16.value(0)
                led_10.value(1)
                if short_number != 0:
                    led_error.value(1)
                    print("*-"*30)
                    print("short circuit pins:", short_array)
                    print("*-"*30)
                else:
                    led_error.value(0)
            else:
                print("*-"*30)
                print("short circuit pins number:", short_number)
                print("short circuit pins:", short_array)
                print("open circuit pins number:", open_number)
                print("open circuit pins:", open_number_array)
                print("connected pins number:", connected_number)
                print("open circuit pins number for 10 pins connector layout:",
                      open_number_in_10_pin)
                print("*-"*30)
                led_16.value(0)
                led_10.value(0)
                led_error.value(1)
        except Exception as e:
            led_error.value(1)
            print("*-"*30)
            sys.print_exception(e)
            print("*-"*30)
