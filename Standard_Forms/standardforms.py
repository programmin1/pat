import os
import json
import re

#
# STILL NEEDS SOME WORK. Case sensitive file system messes with the standard winlink forms.
# Run this with all the folders in this directory. Then move these all to /res/templates so there is /res/templates/allforms.js, and temlate dirs.
#
forms = {}
for root, dirs, files in os.walk('.'):
  for f in files:
      if f.endswith('.txt'):
          with open(os.path.join(root,f)) as infile:
              jsvars = {}
              endPreamble = False
              for line in infile:
                  if endPreamble:
                      if 'Msg' in jsvars:
                          jsvars['Msg']+= line+"\n"
                      else:
                          jsvars['Msg']=''
                  else:
                    match = re.match(r'Form: (.*),', line)
                    matchother = re.match(r'([A-Za-z]*): (.*)', line)
                    if match:
                        jsvars['htm'] = match.group(1).strip()
                        forms[os.path.join(root,f).replace('.txt','')] = os.path.join(root,match.group(1)).replace('./','/res/templates/')
                        #Process the htm to post back.  
                    elif line.startswith('Msg:'):
                        endPreamble = True
                    elif matchother:
                        jsvars[matchother.group(1)] = matchother.group(2)
              #Rewrite the htm with js:
              if 'htm' in jsvars:
                  htm = ''
                  with open(os.path.join(root,jsvars['htm'])) as inhtm:
                      htm = inhtm.read()
                  with open(os.path.join(root,jsvars['htm']),'w') as outhtm:
                      outhtm.write( htm.replace('</head>', 
                        '<script>postBackValues = '+json.dumps(jsvars)+
                        ';</script><script src="/res/templates/sender.js"></script></head>'))
                  
          
out_file = open("allforms.js", "w") 
out_file.write('var winforms=')
json.dump(forms, out_file) 
out_file.close()
