import shlex
import subprocess


try:
   cmd = shlex.split(
          "/root/vsftpd-2.3.4-infected/vsftpd")
   ftp = subprocess.Popen(cmd,shell=False)
   
   cmd = shlex.split(
          "python3 /root/plc2.py")
   plc2= subprocess.Popen(cmd,shell=False)
   
   plc2.wait()
   ftp.wait()
except:
   plc2.terminate()
   ftp.terminate()
   print("something bad occurred")
