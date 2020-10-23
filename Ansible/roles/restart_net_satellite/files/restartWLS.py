import sys
import os
from java.lang import System
from java.io import FileInputStream

propInputStream = FileInputStream(sys.argv[1]+".properties")

configProps = Properties()
configProps.load(propInputStream)

connect(configProps.get("user"),configProps.get("pass"),'t3://'+configProps.get("host")+':'+configProps.get("port"))

shutdown(sys.argv[2],'Server',force='true')
start(sys.argv[2],'Server')
disconnect()
exit()
