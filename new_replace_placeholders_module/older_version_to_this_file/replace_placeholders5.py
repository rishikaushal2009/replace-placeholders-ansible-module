#!/usr/bin/python

import json
from ansible.module_utils.basic import AnsibleModule
import fileinput
import re
import os
from subprocess import *


def main():
    module = AnsibleModule(
       argument_spec = dict(
            envfile = dict(required=True, type='str'),
            outputdir = dict(required=True, type='str'),
       )
    )

    envfile = module.params['envfile']
    outputdir = module.params['outputdir']

    data = dict(
      output="task completed successfully"
    )

 

#envfile = '172.31.3.231:/rk-tmp/placeholders'
#outputdir = '/rk-tmp/'

    cmd = "awk '{print $9}'"
    j=envfile.split("/")[-1].strip()

    try:
     if os.path.isdir(outputdir):
            os.chdir(outputdir)
            out = open("/myssh1.exp","w")
            #line1 = "set timeout 60"
            line1 = "#!/usr/bin/expect -f"
            line2 = "set timeout 60"
            line3 = "spawn /usr/bin/scp -r -o StrictHostKeyChecking=no  root@{k} /".format(k=envfile)
            line4 = "log_user 0"
            line5 = "expect \"root@172.31.3.231\'s password: \""
            #line5 = "expect \"Password:\"" 
            line6 = "send \"35Ramrod!\\r\""
            line7 = "sleep 10"
            line8 = "interact"
            #line7 = "expect eof"
            #line8 = "end"
            out.writelines('{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(line1,line2,line3,line4,line5,line6,line7,line8))
            out.close()
            #call("chmod 777 /myssh1.exp ; /usr/bin/expect /myssh1.exp",shell=True)
            os.system("chmod 777 /myssh1.exp ; /usr/bin/expect -d -f /myssh1.exp")
            #out.close()
            call("ls -ltr {dir}|{k} | sed -n '2,$p' >list1".format(dir=outputdir,k=cmd),shell=True)
            msg1 = "/{k}".format(k=j)   
            file1 = open(msg1, "r")
            for line1 in file1:
              left = line1.split(":",1)[0]
              right  = line1.split(":",1)[-1]
              right = right.rstrip("\n")
              list1 = outputdir+'/list1'
              file2 = open(list1, "r")
              for outputfile in file2 :
                 if outputfile.strip() != j :
                   for line in  fileinput.FileInput(outputfile.strip(), inplace=True):
                     line = re.sub(left,right, line.rstrip())
                     print(line)
            call("rm -f /{k} ./list1 ./myssh1.exp".format(k=j),shell=True)
  

     module.exit_json(changed=True, success=True,msg=data)
    except Exception as e:
     module.fail_json(msg=error)

if __name__ == '__main__':
  main()



