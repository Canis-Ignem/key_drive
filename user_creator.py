
import os
import crypt
from time import sleep
def add_user(username, password):
    
    
                        
     try:
         passwd = ""
         with open("pass",'r') as p:
             passwd = p.read()
         crypt_pass = crypt.crypt(password, 'fat')
         os.popen("sudo useradd -m {} -U -p {} ".format(username,crypt_pass) , 'w').write(passwd)
         sleep(0.2)
         os.popen("sudo chown :{} /home/{}/ ".format(username, username) , 'w').write(passwd)
         sleep(0.2)
         os.popen("sudo chmod 777 /home/{}/".format(username) , 'w').write(passwd)
         return True 
     except:           
         return False
  
add_user("test", "123")