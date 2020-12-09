#!/usr/bin/python

import json
from ansible.module_utils.basic import AnsibleModule
import fileinput
import re
import os
def main():
    module = AnsibleModule(
       argument_spec = dict(
            envfile = dict(required=True, type='str'),
            outputfile = dict(required=True, type='str'),
       #     dir = dict(required=True, type='str'), 
       )
    )

    envfile = module.params['envfile']
    outputfile = module.params['outputfile']
    #dir = module.params['dir']

    data = dict(
      output="task completed successfully"
    )
   
    try:
       #os.chdir(dir)
       file1 = open(envfile, "r") 
       for line1 in file1: 
#          left , right = line1.split(":")
          left = line1.split(":",1)[0]
          right  = line1.split(":",1)[-1]
          right = right.rstrip("\n")
          for line in  fileinput.FileInput(outputfile, inplace=True, backup='.bak'):
           line = re.sub(left,right, line.rstrip())
           print(line)
       
       module.exit_json(changed=True, success=True,msg=data)
    except Exception as e:
     module.fail_json(msg='error')

if __name__ == '__main__':
  main()
