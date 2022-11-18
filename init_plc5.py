import shlex
import subprocess


try:
   cmd = shlex.split(
          "/root/vsftpd-2.3.4-infected/vsftpd")
   ftp = subprocess.Popen(cmd,shell=False)
   
   cmd = shlex.split(
          "python3 /root/plc5.py")
   plc5= subprocess.Popen(cmd,shell=True)
   
   plc5.wait()
   ftp.wait()
except:
   plc5.terminate()
   ftp.terminate()
   print("something bad occurred")
