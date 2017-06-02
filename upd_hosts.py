import time
import os

num = 0
if os.system('ls | grep upd_hosts.log') != 0:
    os.system('touch upd_hosts.log')
else:
    pass

while True: 
    log_time = time.strftime('%Y-%m-%d %H:%M:%S')
    num += 1
    if os.system('git clone https://github.com/racaljk/hosts &&sudo mv hosts/hosts /etc/ -f && rm hosts/ -rf') != 0:
        os.system('echo "%s   [Warning]Fail to update hosts." >> upd_hosts.log'%log_time) 
        print '%s   [Warning]Fail to update hosts.'%log_time
    else:
        os.system('echo "%s   Successfully update hosts %d times." >> upd_hosts.log'%(log_time,num)) 
        print '%s   Successfully updated hosts %d times.'%(log_time,num)
    time.sleep(28800)
