# Power Consumption Record system

This system use ADC of Arduino to get the drop of resistor(10ohm), then use UART transmit to PC,

In PC, I programing in Python to receive data from Arduino, then record and calculate power consumption.

System architecture shows below

<img src="https://github.com/TripleC-Light/Current-Record-System/blob/master/image/Hardware%20architecture.jpg?raw=true" width=600>

Arduino transmit 2 bytes every 343us that is a constant time interval,

So I can know the transmit time on Python, according transmit time I can calculate the accurate power on system

## About Me
 - My Blog : [愛德華空想科學誌]
 - E-mail : TripleC.Light@gmail.com
 - LinkedIn : [Edward Chou](https://www.linkedin.com/in/edward-chou-42058912a)
 - Buy Me A Coffee : [Buy Me A Coffee](https://www.buymeacoffee.com/YrFKPo2)
 - Paypal : [Link](https://www.paypal.me/TripleCLight?locale.x=zh_TW)
