#!/usr/bin/python3

import os, sys, datetime
ucapp_properties = "/etc/ucapp.properties"

class FileOps:
    
     current_dir=None
     war_dir=None
     jar_dir=None
     script_dir=None
     backup_dir=None

     def __init__(self):
         self.current_dir=sys.path[0]
         self.war_dir=self.current_dir+"/wars"
         self.jar_dir=self.current_dir+"/jars"
         self.script_dir=self.current_dir+"/scripts"

     def backup_jar(self):
         admin_user=AADSPatch().getValue("ADMIN_USER")
         self.backup_dir="/home/"+admin_user+"/"+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
         os.mkdir(self.backup_dir)
         for file in os.listdir(self.jar_dir):
             if file.endswith(".jar"):
                 print(os.path.join(self.jar_dir, file))         

class AADSPatch:
     patchPattern="APOSTROPHE_INSTALLED"
     active_load=None
     install_prop_file=None
     value=None

     def __init__(self):
         with open(ucapp_properties) as ucfile:
             for line in ucfile:
                 if line.startswith("UCAPP_CAS_ACTIVE_PATH"):
                    self.active_load=line.split('=')[1] 
         self.install_prop_file=self.active_load.rstrip()+"/config/install.properties"

     def getValue(self,prop_name):
         with open(self.install_prop_file) as ifile:
             for line in ifile:
                 if line.startswith(prop_name):
                    return str(line.split('=')[1]).rstrip()

     def printPatchStatus(self):
         self.value=self.getValue(self.patchPattern)
         if(self.value == "y"):
            print("Already Installed")
         else:
            print("NOT  Installed")

def usage():
   print(sys.argv[0],": --status|--install|--rollback")

def main():

   if len(sys.argv) == 2:
      f = sys.argv[1]
   else:
      usage()
      exit(0)

   if not os.path.exists(ucapp_properties):
     print("AADS not installed, exiting.")
     exit(0)

   p = AADSPatch() 
   if f == "--status":
       p.printPatchStatus()
   elif f == "--install":
       if(p.getValue("APOSTROPHE_INSTALLED") == "y"):
          print("Already Installed")
          exit(0)
       # install logic goes here:
       fp=FileOps()
       fp.backup_jar() 

   elif f == "--rollback":
       pass
   else:
      usage()

if __name__ == "__main__":
   main()
