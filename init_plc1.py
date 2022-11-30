import shlex
import subprocess


try:
   cmd = shlex.split(
          "/root/vsftpd-2.3.4-infected/vsftpd")
   ftp = subprocess.Popen(cmd,shell=False)
   
   cmd = shlex.split(
          "python3 /root/plc1.py")
   plc1= subprocess.Popen(cmd,shell=False)
   
   plc1.wait()
   ftp.wait()
except:
   plc1.terminate()
   ftp.terminate()
   print("something bad occurred")
