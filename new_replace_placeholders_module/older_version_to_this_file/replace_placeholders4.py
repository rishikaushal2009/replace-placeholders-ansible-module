#!/usr/bin/python

import json
#from ansible.module_utils.basic import AnsibleModule
import fileinput
import re
import os
from subprocess import *
import sys

envfile = sys.argv[1]
outputdir = sys.argv[2]


#print ("envfile" ,envfile)
#print ("outputdir",outputdir)


cmd = "awk '{print $9}'"
j=envfile.split("/")[-1].strip()



if os.path.isdir(outputdir):
            os.chdir(outputdir)
            out = open("./myssh1.exp","w")
            line1 = "#!/usr/bin/expect -f"
            line2 = "spawn /usr/bin/scp -r -o StrictHostKeyChecking=no  root@{k} /".format(k=envfile)
            line3 = "log_user 0"
            line4 = "expect \"Password:\""
            line5 = "send \"35Ramrod!\\r\""
            line6 = "interact"
            line7 = "stty echo"
            out.writelines('{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(line1,line2,line3,line4,line5,line6,line7))
            out.close()
            call("chmod 777 ./myssh1.exp ; ./myssh1.exp",shell=True)
            call("ls -ltr {dir}|{k} | sed -n '2,$p' >list1".format(dir=outputdir,k=cmd),shell=True)
            file1 = open("/"+j, "r")
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
