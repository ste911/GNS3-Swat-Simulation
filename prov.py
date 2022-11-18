
import subprocess
import shlex
import time

  

#cmd = shlex.split( getfile)
result = subprocess.run("""python3 -c "print('hello')";python3 -c "print('hello2'); print('hello3')" """ , shell=True)
# time.sleep(10)
#result.terminate()
print(result)
 