import sqlite3
import shlex
import subprocess

PATH = 'swat_s1_db.sqlite'
NAME = 'swat_s1'

STATE = {
    'name': NAME,
    'path': PATH
}
# SPHINX_SWAT_TUTORIAL STATE)

SCHEMA = """
CREATE TABLE swat_s1 (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT = """
    INSERT INTO swat_s1 VALUES ('MV101',    1, '0');
    INSERT INTO swat_s1 VALUES ('LIT101',   1, '0.500');
    INSERT INTO swat_s1 VALUES ('P101',     1, '1');

    INSERT INTO swat_s1 VALUES ('MV201',    2, '0');
    INSERT INTO swat_s1 VALUES ('P201',    2, '0');
    INSERT INTO swat_s1 VALUES ('LS201',    2, '1');
    INSERT INTO swat_s1 VALUES ('P203',    2, '0');
    INSERT INTO swat_s1 VALUES ('LS202',    2, '1');
    INSERT INTO swat_s1 VALUES ('P205',    2, '0');
    INSERT INTO swat_s1 VALUES ('LS203',    2, '1');

    INSERT INTO swat_s1 VALUES ('LIT301',   3, '0.500');
    INSERT INTO swat_s1 VALUES ('P301',    3, '0');
    INSERT INTO swat_s1 VALUES ('MV302',    3, '0');

    INSERT INTO swat_s1 VALUES ('P401',     4, '0');
    INSERT INTO swat_s1 VALUES ('P403',     4, '0');
    INSERT INTO swat_s1 VALUES ('LIT401',   4, '0.000');
    INSERT INTO swat_s1 VALUES ('LS401',    4, '1');

    INSERT INTO swat_s1 VALUES ('P501',   5, '0');
    INSERT INTO swat_s1 VALUES ('MV501',   5, '0');

    INSERT INTO swat_s1 VALUES ('P601',    6, '0');
    INSERT INTO swat_s1 VALUES ('LS601',    6, '0');
"""

if __name__ == "__main__":

    try:
        with sqlite3.connect(PATH) as conn:
             conn.executescript(SCHEMA)
             conn.executescript(SCHEMA_INIT)
             print( "{} successfully created.".format(PATH))
    except sqlite3.OperationalError:
             print ("{} already exists.".format(PATH))
             conn.executescript(SCHEMA_INIT)
             print( "{} successfully reinitialized.".format(PATH))


######   Start the physical Processes   ######

    try:
      cmd = shlex.split(
            "python3 /root/physical_process_rwt.py"
        )
      rwt = subprocess.Popen(cmd, shell=False)
      
      cmd = shlex.split(
            "python3 /root/physical_process_nacl.py"
        )
      naclt = subprocess.Popen(cmd, shell=False)
    
      cmd = shlex.split(
            "python3 /root/physical_process_hcl.py"
        )
      hclt = subprocess.Popen(cmd, shell=False)
    
      cmd = shlex.split(
            "python3 /root/physical_process_naocl.py"
        )
      naoclt = subprocess.Popen(cmd, shell=False)
    
      cmd = shlex.split(
            "python3 /root/physical_process_uff.py"
        )
      ufft = subprocess.Popen(cmd, shell=False)
    
      cmd = shlex.split(
            "python3 /root/physical_process_rof.py"
        )
      roft = subprocess.Popen(cmd, shell=False)
    
      cmd = shlex.split(
            "python3 /root/physical_process_nahso3.py"
        )
      nahso3t = subprocess.Popen(cmd, shell=False)
    
      cmd = shlex.split(
            "python3 /root/physical_process_rop.py"
        )
      ropt = subprocess.Popen(cmd, shell=False)

      cmd = shlex.split(
            "python3 /root/server.py"
        )
      server = subprocess.Popen(cmd, shell=False)

      cmd = shlex.split(
            "python3 /root/swat_gui.py"
        )
      sg = subprocess.Popen(cmd, shell=False)
      rwt.wait()
      naclt.wait()
      hclt.wait()
      naoclt.wait()
      ufft.wait()
      roft.wait()
      roft.wait()
      nahso3t.wait()
      ropt.wait()
      server.wait()
      sg.wait()
    except:
       rwt.terminate()
       naclt.terminate()
       hclt.terminate()
       naoclt.terminate()
       ufft.terminate()
       roft.terminate()
       roft.terminate()
       nahso3t.terminate()
       ropt.terminate()
       server.terminate()
       sg.terminate()
       print("something bad occurred")
