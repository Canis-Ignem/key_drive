
import os
import crypt

def add_user(username, password):
    
    
                        
     try:
         passwd = ""
         with open("pass",'r') as p:
             passwd = p.read()
         crypt_pass = crypt.crypt(password, 'fat')
         os.popen("sudo useradd -m {} -U -p {} ".format(username),crypt_pass) , 'w').write(passwd)
         os.popen("sudo chown :{} /home/{} ".format(username, username) , 'w').write(passwd)
         os.popen("sudo chmod 777 /home/{}".format(username) , 'w').write(passwd)
         return True 
     except:           
         return False
  
add_user("martin", "123")