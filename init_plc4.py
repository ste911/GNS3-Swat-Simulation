import shlex
import subprocess


try:
   cmd = shlex.split(
          "/root/vsftpd-2.3.4-infected/vsftpd")
   ftp = subprocess.Popen(cmd,shell=False)
   
   cmd = shlex.split(
          "python3 /root/plc4.py")
   plc4= subprocess.Popen(cmd,shell=False)
   
   plc4.wait()
   ftp.wait()
except:
   plc4.terminate()
   ftp.terminate()
   print("something bad occurred")
