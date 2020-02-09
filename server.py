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

    

#Sends the requsts of the server for each client and takes the answer of the client and sum them to calculate the Pi
def send_to_client(conn,ip,counter,numberOfSteps,num,mod,div):

    global pi
   
    if counter != 2: #The two first client    
        
        conn.sendall(f'{numberOfSteps}-{mod}-0-{num}'.encode('utf-8'))
        reply = conn.recv(1204).decode('utf-8')
        float_reply = float(reply) 
        pi += float_reply   # adds the answer of the client, which is the part of the Pi that it calculated 
  
    
    else:  #the third client
            
        conn.sendall(f'{numberOfSteps}-{mod}-{div}-{num}'.encode('utf-8'))
        reply = conn.recv(1204).decode('utf-8')
        float_reply = float(reply) 
        pi += float_reply   # adds the answer of the client, which is the part of the Pi that it calculated
     
     
    

# Run the server, connect with the clients, creates the threads that each of them is a request for a client and runs the threads
def connect_to_client(numberOfSteps):
        global counter,mod,div
        threads = []
        
        # Run the server
        conne_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conne_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        conne_socket.bind(('localhost', 8999))
        conne_socket.listen(5) 

        # Creates the threads that send parallel the requests to the clients
        while counter < 3:
          global num  
          conn, ip = conne_socket.accept()
          print('client {} connect with your server'.format(ip))
          
          threads.append(threading.Thread(target=send_to_client,args=(conn,ip,counter,numberOfSteps,num,mod,div)))
          counter += 1
          num += mod
       

        #Run the threads and calculate the time thath the clients needed to calculate the Pi
        t1 = perf_counter()
        for thread in threads: 
            thread.start()  
        
        for thread in threads: 
            thread.join()
        t2 = perf_counter()

        run_time = t2 - t1 # the time that the clients did to calculate the Pi

        conne_socket.close() # Shut down the server

        return run_time 
        
if __name__ == '__main__':
    main(argv)
        
        
