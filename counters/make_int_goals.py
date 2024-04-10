import os
import sys
import re

folder = 'fn-counters-rnd/'

for f in os.listdir(folder):
    if 'instance_' in f:
        #print(f)
        #f_d_w = open('fn-counters/'+f+'_temp', 'rb+')
        new_content = ''
        with open(folder+f) as f_d: 
            s = f_d.readlines()
            for line in s:
                m = re.search('\(< \(value c([\d]+)\) \(value c([\d]+)\)\)', line)
                if m:
                    new_content += '(<= (+ (value c'+m.group(1)+') 1) (value c'+m.group(2)+'))\n'
                else:
                    new_content += line
        with open(folder+f,'w') as f_d:
            f_d.write(new_content)
            
            

