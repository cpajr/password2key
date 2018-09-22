#!/usr/bin/env python3

'''
################################################################################
Using a combination of the Nokia password2key.bash script (JAR Files), 
and a combination of custom elements, this script will take the input
from the user to create an appropriate EngineID and generate needed hashes for 
the router configuration
################################################################################
'''

import os
import sys

#Gather user input

print("Gathering IP Address information....")
ip_addr1 = "172"
ip_addr2 = "028"
ip_addr3 = input("3rd Octet: ")
ip_addr4 = input("4th Octet: ")

#verfiy IP address input
try:
    if int(ip_addr3) <= 0 or int(ip_addr3) >=255:
        print()
        print("ERROR: Not valid 3rd octet IP address.")
        print("Must be greater than 0 and less than 255")
        sys.exit()

    if int(ip_addr4) <= 0 or int(ip_addr4) >=255:
        print()
        print("ERROR: Not valid 4th octet IP address")
        print("Must be greater than 0 and less than 255")
        sys.exit()

except ValueError:
    print()
    print("ERROR: An improper number was provided.  Please try again.")
    print("Exiting...")
    sys.exit()

#Print out the System IP Address

system_ip_addr = "172.28." + ip_addr3 + "." + ip_addr4

print("-"*80)
#print("System IP Address: 172.28.{}.{}".format(ip_addr3, ip_addr4))
print ("{:>20} {:<30}".format("System IP Address:", system_ip_addr))

#Create EngineID
lead_zeros = "000000000000"

if int(ip_addr3) < 10:
	ip_addr3 = "00" + ip_addr3
elif int(ip_addr3) < 100:
	ip_addr3 = "0" + ip_addr3

if int(ip_addr4) < 10:
	ip_addr4 = "00" + ip_addr4
elif int(ip_addr4) < 100:
	ip_addr4 = "0" + ip_addr4

engineid = lead_zeros + ip_addr1 + ip_addr2 + ip_addr3 + ip_addr4

#print("EngineID: ", format(engineid))
print ("{:>20} {:<30}".format("EngineID:", engineid))
print("-"*80)
print()

#Needed elements for the password2key execution
classpath = "tools.jar:AdventNetSnmp.jar:AdventNetLogging.jar"
jar = "com.timetra.nms.server.mediator.snmp.tools.PasswordToKey"

write_passwd = ""
read_passwd = ""

#Create the Write SNMP hash
try:
    output = os.popen("java -client -classpath {} {} SHA {} {}".format(classpath, jar, write_passwd, engineid)).read()
except OSError:
    print("Error: Java script did not execute correctly")
    print("Exiting....")
    sys.exit()


print("-"*80)
print("SNMP Write Hash")
print("-"*80)

for line in output.splitlines():
    hashline = line.split()
    if hashline[0] == "SHA":
        #print("SHA: {}".format(hashline[2]))
        print("{:>20} {:<30}".format("SHA:", hashline[2]))

    if hashline[0] == "AES":
        #print("AES: {}".format(hashline[2]))
        print("{:>20} {:<30}".format("AES:", hashline[2]))

print("-"*80)
print()

#Create the Read SNMP hash
try:
    output = os.popen("java -client -classpath {} {} SHA {} {}".format(classpath, jar, read_passwd, engineid)).read()
except OSError:
    print("Error: Java script did not execute correctly")
    print("Exiting....")
    sys.exit()

print("-"*80)
print("SNMP Read Hash")
print("-"*80)

for line in output.splitlines():
    hashline = line.split()
    if hashline[0] == "SHA":
        #print("SHA: {}".format(hashline[2]))
        print("{:>20} {:<30}".format("SHA:", hashline[2]))

    if hashline[0] == "AES":
        #print("AES: {}".format(hashline[2]))
        print("{:>20} {:<30}".format("AES:", hashline[2]))

print("-"*80)
print()
