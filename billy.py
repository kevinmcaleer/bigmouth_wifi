from machine import Pin, RTC
from time import sleep, gmtime
from phew import logging
import usocket
import struct

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
        
        print(' ______     __     ______        __    __     ______     __  __     ______   __  __               ')
        print('/\  == \   /\ \   /\  ___\      /\ "-./  \   /\  __ \   /\ \/\ \   /\__  _\ /\ \_\ \              ')
        print('\ \  __<   \ \ \  \ \ \__ \     \ \ \-./\ \  \ \ \/\ \  \ \ \_\ \  \/_/\ \/ \ \  __ \             ')
        print(' \ \_____\  \ \_\  \ \_____\     \ \_\ \ \_\  \ \_____\  \ \_____\    \ \_\  \ \_\ \_\            ')
        print('  \/_____/   \/_/   \/_____/      \/_/  \/_/   \/_____/   \/_____/     \/_/   \/_/\/_/            ')
        print('')
        print(' ______     __     __         __         __  __        ______     ______     ______     ______    ')
        print('/\  == \   /\ \   /\ \       /\ \       /\ \_\ \      /\  == \   /\  __ \   /\  ___\   /\  ___\   ')
        print('\ \  __<   \ \ \  \ \ \____  \ \ \____  \ \____ \     \ \  __<   \ \  __ \  \ \___  \  \ \___  \   ')
        print(' \ \_____\  \ \_\  \ \_____\  \ \_____\  \/\_____\     \ \_____\  \ \_\ \_\  \/\_____\  \/\_____\ ')
        print('  \/_____/   \/_/   \/_____/   \/_____/   \/_____/      \/_____/   \/_/\/_/   \/_____/   \/_____/ ')
        print('')

        # truncate log to keep it to at most three blocks on disk)
        logging.info("truncating log file")
        logging.truncate(8192)
    
    # returns True if we've used up 90% of the internal filesystem
    @staticmethod
    def low_disk_space():
      try:
        return (os.statvfs(".")[3] / os.statvfs(".")[2]) < 0.1
      except:
        # os.statvfs doesn't exist on remote mounts but in that case we can
        # assume plenty of space
        pass
      return False
    
    @staticmethod
    def what_time_is_it_mr_wolf()->list:
        time_list = gmtime()
        current_time = {'year': str(time_list[0]),
                        'month': str(time_list[1]),
                        'day': str(time_list[2]),
                        'hour': str(time_list[3]),
                        'minute': str(time_list[4]),
                        'second': str(time_list[5])}
        return str(current_time['hour'] + ":" + current_time['minute'] + ":" +  current_time['second'] + " " + current_time['day'] + "/" + current_time['month'] + "/" + current_time['year'] )

    @staticmethod
    def clock_set():
      return RTC().datetime()[0] > 2020 # year greater than 2020? we're golden!

    @staticmethod
    def update_rtc_from_ntp(max_attempts = 5):
      logging.info("> fetching date and time from ntp server")
      ntp_host = "pool.ntp.org"
      attempt = 1
      while attempt < max_attempts:
        try:
          logging.info("  - synching rtc attempt", attempt)
          query = bytearray(48)
          query[0] = 0x1b
          address = usocket.getaddrinfo(ntp_host, 123)[0][-1]
          socket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
          socket.settimeout(30)
          socket.sendto(query, address)
          data = socket.recv(48)
          socket.close()
          local_epoch = 2208988800  # selected by Chris, by experiment. blame him. :-D
          timestamp = struct.unpack("!I", data[40:44])[0] - local_epoch
          t = gmtime(timestamp)
          return t      
        except Exception as e:
          logging.error(e)

        attempt += 1
      return False

    # connect to wifi and then attempt to fetch the current time from an ntp server
    # once fetch set the onboard rtc and the pico's own rtc
    @staticmethod
    def sync_clock_from_ntp(self):
      t = update_rtc_from_ntp()
      if not t:
        logging.error("  - failed to fetch time from ntp server")
        return False
      
      # set the pico rtc time
      RTC().datetime((t[0], t[1], t[2], t[6], t[3], t[4], t[5], 0))      
      logging.info("  - rtc synched")      
      return True          
    
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