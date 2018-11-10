import socket 
import string
import json
from threading import Thread 
from SocketServer import ThreadingMixIn 
 
# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print "[+] New server socket thread started for " + ip + ":" + str(port) 
    def create_socket(self, ip, port):
      s = socket.socket()
      s.connect((ip,int(port)))
      return s
   
    def check_in_root(self, domain):
      print "root: check_in_root"
      root_cache_file = open("root_cache.txt", "r")
      for line in root_cache_file:
        cache_entry = line.split(" : ")[0]  
        print cache_entry + "-"
        print domain + "-"
        if cache_entry == domain:
          print "found domain"
          return True, line.split(" : ")[1], line.split(" : ")[2]
      print "not_found"
      return False, "Nabooodesh khare", "nist agha jan"
    def get_ip_iter(self, domain, tld):
      print "root: get_ip_iter"

    def get_ip_rec(self, domain, auth, req_type):
      print "root : get_ip_rec"
      print"check_in_root"+  domain + "-"
      org_config_file = open("org_config.txt", "r")
      for line in org_config_file:
          temp_auth = line.split(" : ")[0]
          if temp_auth == auth:
            ip = line.split(" : ")[1]
            port = 12345 
            print "port" , port , "ip" , ip
            if req_type == "rec":
              json_msg = {
              'type' : "rec",
              'domain' : domain,
              'action' : "alaki"
              }
              auth_socket  = self.create_socket(ip, port)
              auth_socket.send(json.dumps(json_msg)) 
              auth_data =  auth_socket.recv(2048)
              print auth_data
              conn.send(auth_data)
            else :
              print "iter"
              print "-"+ip+ "-"
              clean_ip = ip[:-2]
              print "-"+clean_ip+"-"
              json_msg={
                  'ip': ip,  
                  'port' : port,
                  'ans' : False
              }
              conn.send(json.dumps(json_msg))
              print "send done!" , json_msg
          else :
            continue

    def run(self): 
          data = conn.recv(2048) 
          print "Server received data:", data
          load_data = json.loads(data)
          req_type = load_data["type"]
          domain = load_data["domain"]
          if len(load_data["domain"].split("."))>2 :
            print "len bozorgtar az 2"
            auth =  load_data["domain"].split(".")[1]
            print "auth :-"+auth+"-"
          else:
            auth=load_data["domain"].split(".")[0]
            print "auth :-"+auth+"-"
          if req_type == "rec":
            print "run : domain:" + domain + "-"
            self.get_ip_rec(domain,auth,"rec")
          elif req_type == "iter":
            print "run : iter:"
            self.get_ip_rec(domain,auth,"iter")
          else :
            print "root run type else"
          conn.close()
#            self.send_root_rec(data)
 
# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '10.0.0.3' 
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
