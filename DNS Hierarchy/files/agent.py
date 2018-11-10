import socket 
import json
import time
from threading import Thread 
from SocketServer import ThreadingMixIn 


cache = []

def limit_not_exceeded(item):
  diff = time.time()-item["last_req_time"]
  print "diff =",diff
  return diff<int(item["time_limit"])

def search_cache(data):
  print "cache : "
  print cache
  for item in cache:
    print "item_domain :-"+item["domain"]+"-"
    print "data :-"+data+"-"
    if item["domain"]==data:
      if limit_not_exceeded(item):
        return True,item
  return False,"false"

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print "[+] New server socket thread started for " + ip + ":" + str(port) 
    def create_socket(self, ip, port):
      print "agent : create_socket"
      s = socket.socket()
      s.connect((ip,int(port)))
      return s
    def send_root(self, data, req_type):
        json_msg = {
            'type' : req_type,
            'domain' : data
            }
        agent_config_file  = open ("agent_config.txt", "r")
        for line in agent_config_file:
            ip = line.split(" : ")[1]
            port = 12345 
            print "port" , port , "ip" , ip
            root_socket  = self.create_socket(ip, port)
            root_socket.send(json.dumps(json_msg)) 
            print "send done!" , json_msg 
            return root_socket 
    def get_ip_rec(self, data):
      root_socket = self.send_root(data,"rec")
      root_response = root_socket.recv(2048)
      print "root_response = " + root_response
      load_root_response = json.loads(root_response) 
      ip = load_root_response["ip"]
      port = load_root_response["port"]
      time_limit = load_root_response["time_limit"]
      cache_item = {
        "domain" : data,
        "ip" : ip,
        "port" : port,
        "time_limit" : time_limit,
        "last_req_time" : time.time()
      }
      cache.append(cache_item)
    def send_req(self, ip, port, data, req_type,action):
      req_socket = self.create_socket(ip, port)
      json_msg = {
           'type' : req_type,
           'domain' : data,
           'action' : action
           }
      req_socket.send(json.dumps(json_msg))
      return req_socket
    def get_ip_iter(self, data, mode):
        if mode == "add" or mode == "update":
          domain = data.split(" : ")[0]
          print "-"+domain+"-"
        else:
          domain = data

        root_socket = self.send_root(domain, "iter")
        root_response = root_socket.recv(2048)
        print "root_response =" , root_response
        load_root_response = json.loads(root_response) 
        ip = load_root_response["ip"]
        port = load_root_response["port"]
        
        if load_root_response["ans"]:
          time_limit = load_root_response["time_limit"]
          print "ans was in root"
          print "ip : " , ip, "port: " , port
          cache_item = {
            "domain" : domain,
            "ip" : ip,
            "port" : port,
            "time_limit" : time_limit,
            "last_req_time" : time.time()
          }
          cache.append(cache_item)
        else:
          tld_socket= self.send_req(ip, port, domain, "iter",mode)
          tld_response = tld_socket.recv(2048)
          print "tld_response =" , tld_response
          load_tld_response = json.loads(tld_response)
          ip = load_tld_response["ip"]
          port  =  load_tld_response["port"]
          auth_socket= self.send_req(ip, port, data, "iter",mode)
          auth_response = auth_socket.recv(2048)
          print "auth_response =" , auth_response
          load_auth_response = json.loads(auth_response)
          ip = load_auth_response["ip"]
          port  =  load_auth_response["port"]

          time_limit = load_auth_response["time_limit"]
          print "port:" , port, "ip:", ip, "time:", time_limit
          cache_item = {
            "domain" : domain,
            "ip" : ip,
            "port" : port,
            "time_limit" : time_limit,
            "last_req_time" : time.time()
          }
          cache.append(cache_item)
    
    def run(self): 
        while True : 
            data = conn.recv(2048) 
            print "Server received data:", data, "-"
            clean_data = data[:-2]
            print "-"+ clean_data+ "-"
            domain = clean_data.split(" --")[0]
            mode = clean_data.split(" --")[1]
            print "domain :-"+domain+"-"
            print "mode :-"+mode+"-"
            if mode == "rec" or mode =="iter":
              in_cache,ans = search_cache(domain)
            if in_cache:
              print "found in cache"
              print "domain : "+ans["domain"]+" - ip : "+ans["ip"]+" - port : ",ans["port"]
            else:
              print "not in cache"
              if mode=="rec":
                print "--- rec mode ---"
                self.get_ip_rec(domain)
              elif mode=="iter":
                print "--- iter mode ---"
                self.get_ip_iter(domain,"iterative") 
              elif mode=="add":
                print "--- add mode ---"
                self.get_ip_iter(domain,"add")
              elif mode=="update":
                print "--- update mode ---"
                self.get_ip_iter(domain,"update")
 
# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '10.0.0.1' 
TCP_PORT = 1234
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 
 
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    print "Multithreaded Python server : Waiting for connections from TCP clients..." 
    (conn, (ip,port)) = tcpServer.accept() 
    print ip, port
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join() 
