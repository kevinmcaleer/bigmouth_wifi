from machine import Pin
from time import sleep


class Billy():
    """ Big Mouth Billy Bass Robot """
    # Setup all the pins for each motor
    
    head = False
    tail = False
    mouth = False

    def __init__(self):
        self.__head1 = Pin(0, Pin.OUT)
        self.__head2 = Pin(1, Pin.OUT)
        self.__tail1 = Pin(2, Pin.OUT)
        self.__tail2 = Pin(3, Pin.OUT)
        self.__mouth1 = Pin(4, Pin.OUT)
        self.__mouth2 = Pin(5, Pin.OUT)

    def head_out(self):
        """ Move head out """
        self.head = True
        self.__head1.value(1)
        self.__head2.value(0)
        sleep(0.25)
     
    def head_in(self):
        """ Move head in """
        self.head = False
        self.__head1.value(0)
        self.__head2.value(0)
        sleep(0.25)

    def tail_out(self):
        """ Move tail out """
        self.tail = True
        self.__tail2.value(1)
        sleep(0.25)
        
    def tail_in(self):
        """ Move tail in """
        self.tail = False
        self.__tail2.value(0)
        sleep(0.25)
      
    def mouth_open(self):
        """ Move mouth open """
        self.mouth = True
        self.__mouth1.value(0)
        self.__mouth2.value(1)
        sleep(0.25)

    def mouth_close(self):
        """ Move mouth closed """
        self.mouth = False
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
        
    @property
    def status(self)->str:
        message = "Billy's "
        if self.head:
            message = message + "Head is out, " 
        else:
            message = message + "Head is in, "
            
        if self.mouth:
            message = message + "mouth open, "
        else:
            message = message + "mouth closed, "
            
        if self.tail:
            message = message + "and the tail is out."
        else:
            message = message + "and the tail is in."
            
        return message
    
    def __str__(self):
        state = [0,0,0]
        if self.mouth:
            state[0] = 1
        else:
            state[0] = 0
        if self.head:
            state[1] = 1
        else:
            state[1] = 0
        if self.tail:
            state[2] = 1
        else:
            state[2] = 0
        
        return ''.join(str(e) for e in state)