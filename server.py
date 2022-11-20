import socket
import sys
import string
import sqlite3




class Server ():

    def __init__(self):

        HOST='192.168.1.1'
        PORT=3001 
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print('Socket created')

        try: 
            s.bind((HOST,PORT))
        except socket.error as  err:
            print('Bind failed. Error: ' +str(err[0]) + 'Message: ' + str(err[1]))


        print ('Socket bind completed')
        s.listen()
        print('Socket ready to listen')
  

        while 1:
            conn,addr = s.accept()
            #print ( 'Request received by ' + addr[0]+ ':' + str(addr[1]))
            req= conn.recv(512)
            #print(req)
            strreq=req.decode().split(':')
            if strreq[0] == 'GET':
                what = (strreq[1],int(strreq[2]))
                #print(strreq)
                res=self.get(what)
                #print(res)
                conn.send(str(res).encode())
            elif strreq[0]=='SET':
                what = (strreq[1],int(strreq[2]))
                #print(what)
                if strreq[1].startswith('P') or strreq[1].startswith('M'):
                     value = int(strreq[3])
                else:    
                     value = float(strreq[3])
                self.set(what,value)
            else:
                print('Errore, ',strreq[0])
                exit()

    def get(self,what):
        get_query = 'SELECT value FROM swat_s1 WHERE name = ? AND pid = ?'
        with sqlite3.connect("swat_s1_db.sqlite") as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(get_query, what )
                record = cursor.fetchone()
                return record[0] 
            except sqlite3.Error as e:
                print('_get ERROR: %s: ' % e.args[0])

    def set(self, what, value):
        set_query = 'UPDATE  swat_s1 SET value = ? WHERE name = ? AND pid = ?'
        what = tuple([value,what[0],what[1]])
        with sqlite3.connect("swat_s1_db.sqlite") as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(set_query, what )
                conn.commit()
                return value
            except sqlite3.Error as e:
                print('_get ERROR: %s: ' % e.args[0])

if __name__ == "__main__":

    server= Server()