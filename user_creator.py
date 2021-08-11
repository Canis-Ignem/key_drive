
import os
import crypt

def add_user(username, password):
    
    
                        
     try:
         passwd = ""
         with open("pass",'r') as p:
             passwd = p.read()
         crypt_pass = crypt.crypt(password, 'fat')
         os.popen("sudo useradd -m {} -U -p {} ".format(username.strip(),crypt_pass) , 'w').write(passwd)
         os.popen("sudo chown :{} /home/{} ".format(username.strip(), username) , 'w').write(passwd)
         os.popen("sudo chmod 777 /home/{}".format(username.strip()) , 'w').write(passwd)
         return True 
     except:           
         return False
  
add_user("martin", "123")