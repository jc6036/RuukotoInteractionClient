import socket
import threading

'''
 This file contains the code to listen for client connections and send out
 commands to said clients.

 Example of usage:

 server = InteractionServer('0.0.0.0', 8081)
 # run the main loop in a thread
 servthread = threading.Thread(target=server.runserver,daemon=True)
 servthread.start()
 server.addcommand(userid, 'OOT LOWGRAV') # Low grav in ocarina of time
'''

class InteractionServ:
  def __init__(self, HOST,  PORT):
    self.PORT = PORT
    self.HOST = HOST
    self.threadpool = []
    self.commandqueue = []
    self.running = True

  # Main method. Keeps open and waits for connections.
  # Each connection is assigned to a new thread.
  def runserver(self):
    # Mainloop
    while self.running:
      # Open listen socket
      self.cleanupthreadpool() # Cleanup before attempting new connections.
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.bind((self.HOST, self.PORT))
      sock.listen()

      # Handle incoming Connection
      connection, addr = sock.accept()
      connection.settimeout(30)
      print(addr[0] + ' has connected.')

      # Get initial payload
      try:
        data = connection.recv(128)
        threaduserid = self.processinitialdata(data)
        if threaduserid == '':
          print(addr[0] + ': initial payload was invalid.')
          connection.close()
        else:
          # Thread the connection if it's a success
          connthread = threading.Thread(target=self.processconnection,name=threaduserid, args=((connection, addr)), daemon = True)
          connthread.start()
          connthread.run()
          self.threadpool.append(connthread)
      except TimeoutError:
        print(addr[0] + ' has timed out.')
        connection.close()

  # Method meant to be threaded.
  # Maintain open connection and wait for data to be sent out.
  def processconnection(self, connection, address):
    connopen = True
    # Main connection loop
    while connopen:
      # Check command queue
      for x in self.commandqueue:
        if x.first == threading.current_thread().name:
          try:
            connection.send(x.second)
            reply = connection.recv(128)
            self.processreply(reply)
          except TimeoutError:
            print ('Timeout error on ' + address[0])
            connection.close()
            connopen = False
            break
          try:
            self.commandqueue.remove(x)
          except ValueError:
            pass

      # Heartbeat
      try:
        connection.send(bytes('KEEPALIVE', 'utf-8'))
        reply = connection.recv(128)
        self.processreply(reply)
      except TimeoutError:
        print ('Timeout error on ' + address[0])
        connection.close()
        connopen = False

  # Process initial payload.
  # Expects a discord user id.
  # If there is a problem with the payload, return a blank string.
  # If successful, returns results of payload.
  def processinitialdata(self, data):
    # Reflects param as string for now. Update with validation in the future.
    return data.decode()

  # Stub for now, but will check the reply from the remote client and react accordingly.
  # This will help us process wrong command messages and the like.
  def processreply(self, reply):
    pass

  # targetid = discord user id which identifies the connection. Usually the
  # userid of the person running the remote client on their computer.
  # command = actual contents of text command meant to be interpreted by
  # the remote client. Command is regular string - gets converted by method
  # to bytes.
  def addcommand(self, targetid, command):
    self.commandqueue.append((targetid, bytes(command, 'utf-8')))

  # Cleans up inactive threads from our thread pool object
  def cleanupthreadpool(self):
    for x in self.threadpool:
      if not x.is_alive():
        try:
          self.threadpool.remove(x)
        except ValueError:
          pass

  # For debugging. Easy way to terminate all threads and connections without stopping ruu.
  def shutdown(self):
    self.running = False
