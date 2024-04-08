# Abstract
- LIS3MDL sensor reads data of magnetic field using stm32f103zet6,
- Python serial reads the data transmitted by stm32 uart.
- STM32 transmits data when python sends a data flag through serial port.
# STM32 Setup for LIS3MDL

- The VCC pin in LIS3MDL is connected to 3.3V in STM32.
- The SDO pin in LIS3MDL is connected to PA6 in STM32.
- The SDA PIN in LIS3MDL is connected to PA7 in STM32.
- The CS  PIN in LIS3MDL is connected to PB7 in STM32.
- The INT  and DRDY pin are floating pin.
