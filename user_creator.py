
import subprocess
import sys
import getpass
import crypt

def add_user(username, password):
  
     try:
         crypt_pass = crypt.crypt(password, 'fat')
         subprocess.run(['useradd', '-m', '-p', crypt_pass, username ])
         return True 
     except:           
         return False
  
add_user("martin", "123")