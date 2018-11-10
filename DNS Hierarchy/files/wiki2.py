import socket 
import string
import fileinput
import sys

import json
from threading import Thread 
from SocketServer import ThreadingMixIn 
 
def add_domain(domain):
  print "in_add"
  wiki2_file = open("wiki2_config.txt", "a")
  wiki2_file.write("\n")
  wiki2_file.write(domain)
  wiki2_file.close()
  

def replaceAll(file,searchExp,replaceExp):
  for line in fileinput.input(file, inplace=1):
    domain = line.split(" : ")[0]
    if searchExp == domain:
      line = line.replace(line,replaceExp)
    sys.stdout.write(line)

def update_domain(domain):
  print "in update"
  real_domain = domain.split (" : ")[0]
  print "-"+real_domain+"-"
  replaceAll("wiki2_config.txt", real_domain, domain)
# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
  
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print "[+] New server socket thread started for " + ip + ":" + str(port) 
    def create_socket(self, ip, port):
      s = socket.socket()
      s.connect((ip,port))
      return s
    def get_ip_rec(self, domain, action):
      print "wiki2 : get_ip_rec"
      if action=="add":
        add_domain(domain)
        domain = domain.split(" : ")[0]
      elif action =="update":
        update_domain(domain)
        domain = domain.split(" : ")[0]

      wiki2_file = open("wiki2_config.txt", "r")
      for line in wiki2_file:
        wiki2_entry = line.split(" : ")[0]  
        print wiki2_entry + "-"
        print domain + "-"
        if wiki2_entry == domain:
          print "found domain"
          print line.split(" : ")[1]
 	  time_limit = line.split(" : ")[2]
	  clean_time = time_limit[:-1]
          json_response = {
           'ip' :  line.split(" : ")[1],
           'port' : 12345,
           'time_limit' : clean_time
          }
      conn.send(json.dumps(json_response))
      print "send done!",json_response
     

    def run(self): 
          data = conn.recv(2048) 
          print "Server received data:", data
          load_data = json.loads(data)
          req_type = load_data["type"]
          domain = load_data["domain"]
          action = load_data["action"]
          self.get_ip_rec(domain,action)
          conn.close()
#            self.send_root_rec(data)
 
# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '10.0.0.9' 
TCP_PORT = 12345
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 
 
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    print "Multithreaded Python server : Waiting for connections from TCP clients..." 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join() 
