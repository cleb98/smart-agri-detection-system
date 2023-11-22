# Arduino

This motion detection system includes a passive infrared sensor (PIR), a webcam, a red LED as an actuator, and an Arduino Uno microcontroller.

## Components

| Component | Description |
| ----------- | ----------- |
| `PIR Sensor` | A passive infrared sensor, the model used is an HC-SR501. It operates on a supply voltage of 5-20V, consumes 65mA current, and produces an output voltage of 0-3.3V. The sensor has a detection range of less than 120 degrees up to 7 meters. |
| `Webcam` | The system uses the webcam of the device on which the bridge script is running. |
| `LED (Actuator)` | The LED used is red in color, packaged in a 10mm casing. Its forward voltage is 1.85V, and it emits light with an intensity of 450mcd. The LED comes with 2 pins. |
| `Arduino Uno` | The Arduino Uno microcontroller is based on the ATmega328P. It features 14 digital input/output pins (6 of which can be used as PWM outputs), 6 analog inputs, a 16 MHz ceramic resonator, a USB connection, a power jack, an ICSP header, and a reset button. |

## Arduino Script

The Arduino script is divided into the following sections:

1. **Setup**: This section includes the pin assignments and the configuration of the PIR sensor and serial communication (baud rate: 9600).

2. **Control for Actuation**: The `checkSerialPackets`` function continuously checks for data reception from serial communication for actuation. When /b '0XAA 0XAB 0XAC’ is received and the LED is at LOW, it is set to HIGH. Conversely, when /b '0XAA 0XAB 0XAD’ is received and the LED is at HIGH, it is set to LOW.

3. **Loop**: In the loop, when the PIR sensor detects motion (val == HIGH), a three-byte packet (0xFF, 0xFA, 0xFE) is sent via Serial. This acts as a detection signal for the bridge.

## Functionality

In the initial setup, the Arduino board is configured to communicate with the PIR sensor and the LED. The sensor is used to detect any movement within its range, and this information is sent to the Arduino. When motion is detected, the Arduino triggers the LED to indicate the detection, and a corresponding signal is sent back to the host device through the serial port.

