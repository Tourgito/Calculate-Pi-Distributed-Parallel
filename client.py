# -*- coding: utf-8 -*-
"""
Created on Sat May 25 20:23:05 2019

@author: user
"""

import socket
import threading
#from helpClient import create_threads, calcPi

lock = threading.Lock()
a = 0
pi = 0

#sundeei twn client me ton server dimiourgei kai trexei ta threads kai steilnei to kommati tou pi pou upologise    
def connect():
      global pi  
      
      sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      sk.connect(('localhost',8999))
       

      numbers = sk.recv(1204).decode('utf-8')  
      nb,mod,div,num = numbers.split('-')
      
      space = int(mod) + int(div)
      local_mod,local_div = divmod(space,6) #briskw mod kai div tou diasthmatos pou prepei na upologisei se sxesh me twn arithmo twn purhnwn mou

      threads = create_threads(int(num),local_mod,local_div,int(nb))#ftiaxnw lista me ta threads mou
            

      for thread in threads: #trexw ta thread
        thread.start()

      for thread in threads:           
          thread.join()
          
          
      str_pi = str(pi)
           
      sk.sendall(str_pi.encode('utf-8'))
      
      sk.close()
      
#epistrefei lista me ta threads mou      
def create_threads(num,local_mod,local_div,numberOfSteps):
    threads = []
    lower_floor = num
    for i in range(6):
     
        if i != 5:
            threads.append(threading.Thread(target=calcPi,args=(lower_floor,local_mod+lower_floor,numberOfSteps,)))
        else:
            threads.append(threading.Thread(target=calcPi,args=(lower_floor,local_mod+lower_floor+local_div,numberOfSteps,)))
        lower_floor += local_mod

    return threads      
      
      
#upologizei to kommati pi pou prepei kai to epistrefei
def calcPi(beg,end,steps):
    """ Leibniz formula for arctan(1) = pi/4 """
    global pi
    global lock
    summ = 0
    step = 1.0 / int(steps)

    for i in range(beg,end):
        x = (i + 0.5) * step
        summ += 4.0 / (1.0 + x**2)
        
    lock.acquire()    
    pi += summ * step
    lock.release()
       
        
   
    
if __name__ == "__main__":

 
    connect()    
    print(f'The part of the pi that the client calculate: {pi}')
