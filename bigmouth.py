from machine import Pin
from time import sleep

# Setup all the pins for each motor
head1 = Pin(0, Pin.OUT)
head2 = Pin(1, Pin.OUT)
tail1 = Pin(2, Pin.OUT)
tail2 = Pin(3, Pin.OUT)
mouth1 = Pin(4, Pin.OUT)
mouth2 = Pin(5, Pin.OUT)

fishy_parts = [mouth1, mouth2, tail1, tail2, head1, head2]

def head_out(m1, m2):
    m1.value(1)

def head_in(m1, m2):
    m1.value(0)

def head(m1, m2):
    m1.value(1)
    sleep(0.25)
    m1.value(0)
    sleep(0.25)

# def tail_open(t1,t2,value):
#     print(f'tail flip: {value}')
#     t2.value(value)
#     sleep(0.25)
    
#     print(f'tail flip: {value}')
#     value = 0
#     t2.value(value)
#     sleep(0.25)

def tail_out(t1,t2):
    print(f'tail flip out')
    t2.value(1)
    
def tail_in(t1,t2):
    print(f'tail flip in')
    t2.value(0)

def mouth_open(motor_1,motor_2):
    print(f'mouth open')
    motor_1.value(0)
    motor_2.value(1)

def mouth_close(motor_1,motor_2):
    print(f'mouth closed')
    motor_1.value(1)
    motor_2.value(1)
 
while True or KeyboardInterrupt:
#     head(head1, head2)
    head_out(head1, head2)
    sleep(0.5)
    tail_out(tail1, tail2)
    for _ in range (1.10):
        mouth_open(mouth1, mouth2)
        sleep(0.25)
        mouth_close(mouth1, mouth2)
        sleep(0.25)
    head_in(head1, head2)
    tail_in(tail1, tail2)
    mouth_close(mouth1, mouth2)
    sleep(1)