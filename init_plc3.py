import shlex
import subprocess


try:
   cmd = shlex.split(
          "/root/vsftpd-2.3.4-infected/vsftpd")
   ftp = subprocess.Popen(cmd,shell=False)
   
   cmd = shlex.split(
          "python3 /root/plc3.py")
   plc3= subprocess.Popen(cmd,shell=True)
   
   plc3.wait()
   ftp.wait()
except:
   plc3.terminate()
   ftp.terminate()
   print("something bad occurred")
