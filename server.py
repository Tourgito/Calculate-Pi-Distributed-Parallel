# -*- coding: utf-8 -*-
"""
Created on Sat May 25 19:58:47 2019

@author: user
"""

import threading
import socket
from time import perf_counter
from math import pi as mathPi
from sys import argv, exit

counter = 0
mod = None
div = None
pi = 0
num = 0

def main(argv):
    global mod, div, pi
    
    if len(argv) != 2:
        print('Usage: {} <number of steps>' .format(argv[0]))
        exit(1)

    numberOfSteps = argv[1]

    try:
       numberOfSteps = int(numberOfSteps)

    except ValueError as e:
        print('Integer convertion error: {}' .format(e))
        exit(2)

    if numberOfSteps <= 0:
        print('Steps cannot be non-positive.')
        exit(3)
        
    mod,div = divmod(numberOfSteps,3) #briskw to div kai to mod sto diasthma tou numberOfSteps me bash twn arithmw twn client    
  

    run_time = connect_to_client(numberOfSteps)


    print('Sequential program results with {} steps' .format(numberOfSteps))
    print('Computed pi = {}' .format(pi))
    print('Difference between estimated pi and math.pi = {}' .format(abs(pi - mathPi)))
    print('Time to compute = {} seconds' .format(run_time))

    

#ta threads epikoinwnoun me tous client kai upologizei to teliko pi      
def send_to_client(conn,ip,counter,numberOfSteps,num,mod,div):
    global pi
   
    if counter != 2:  # se ayth thn if mpainoun oloi ektos tvn teleutaio client  
        
        conn.sendall(f'{numberOfSteps}-{mod}-0-{num}'.encode('utf-8'))
        reply = conn.recv(1204).decode('utf-8')
        float_reply = float(reply) 
        pi += float_reply
  
    
    else:  #mpainei o teleutaios client
            
        conn.sendall(f'{numberOfSteps}-{mod}-{div}-{num}'.encode('utf-8'))
        reply = conn.recv(1204).decode('utf-8')
        float_reply = float(reply) 
        pi += float_reply
     
     
    

        
#sundeei tous client me ton serverkai dimiourgei kai trexei ta threads kai epistrefei twn xrono ulopoihshs        
def connect_to_client(numberOfSteps):
        global counter,mod,div
        threads = []  #lista opou apothikeuwnte ta threads
        conne_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conne_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        conne_socket.bind(('localhost', 8999))
        conne_socket.listen(5)

        while counter < 3:
          global num  
          conn, ip = conne_socket.accept()
          print('client {} connect with your server'.format(ip))
          
          threads.append(threading.Thread(target=send_to_client,args=(conn,ip,counter,numberOfSteps,num,mod,div)))
          counter += 1
          num += mod
       


        t1 = perf_counter()

        for thread in threads: #trexw ta thread
            thread.start()  
        
        for thread in threads: 
            thread.join()

        t2 = perf_counter()
        run_time = t2 - t1

        conne_socket.close()

        return run_time
        
if __name__ == '__main__':
    main(argv)
        
        
