
import subprocess
import sys
import getpass


def add_user(username, password):
  
     try:
         subprocess.run(['useradd', '-p', password, username ])
         return True 
     except:           
         return False
  
add_user("martin", "123")