import shlex
import subprocess


try:
   cmd = shlex.split(
          "/root/vsftpd-2.3.4-infected/vsftpd")
   ftp = subprocess.Popen(cmd,shell=False)
   
   cmd = shlex.split(
          "python3 /root/plc6.py")
   plc6= subprocess.Popen(cmd,shell=False)
   
   plc6.wait()
   ftp.wait()
except:
   plc6.terminate()
   ftp.terminate()
   print("something bad occurred")
