from machine import Pin
from time import sleep


class Billy():
    """ Big Mouth Billy Bass Robot """
    # Setup all the pins for each motor
    
    def __init__(self):
        self.__head1 = Pin(0, Pin.OUT)
        self.__head2 = Pin(1, Pin.OUT)
        self.__tail1 = Pin(2, Pin.OUT)
        self.__tail2 = Pin(3, Pin.OUT)
        self.__mouth1 = Pin(4, Pin.OUT)
        self.__mouth2 = Pin(5, Pin.OUT)

    def head_out(self):
        """ Move head out """
        self.__head1.value(1)
        self.__head2.value(0)
        sleep(0.25)
     
    def head_in(self):
        """ Move head in """
        self.__head1.value(0)
        self.__head2.value(0)
        sleep(0.25)

    def tail_out(self):
        """ Move tail out """
        self.__tail2.value(1)
        sleep(0.25)
        
    def tail_in(self):
        """ Move tail in """
        self.__tail2.value(0)
        sleep(0.25)
      
    def mouth_open(self):
        """ Move mouth open """
        self.__mouth1.value(0)
        self.__mouth2.value(1)
        sleep(0.25)

    def mouth_close(self):
        """ Move mouth closed """
        self.__mouth1.value(1)
        self.__mouth2.value(1)
        sleep(0.25)
        
    def flap_tail(self, times):
        for _ in range(1, times):
            self.tail_out()
            sleep(0.001)
            self.tail_in()
        
    
    def reset(self):
        self.__head1.value(0)
        self.__head2.value(0)
        self.__tail1.value(0)
        self.__tail2.value(0)
        self.__mouth1.value(0)
        self.__mouth2.value(0)
        sleep(0.25)