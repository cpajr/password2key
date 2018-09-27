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
import cgi,cgitb

#HTML Output
print("Content-Type: text/html")    
print()

#Gather user input
form = cgi.FieldStorage()

#print("Gathering IP Address information....")
ip_addr1 = "***"
ip_addr2 = "***"
ip_addr3 = form.getvalue('ip_addr3')
ip_addr4 = form.getvalue('ip_addr4')

#verfiy IP address input
try:
    if int(ip_addr3) <= 0 or int(ip_addr3) >=255:
        print()
        print("ERROR: Not valid 3rd octet IP address.<br><br>")
        print("Must be greater than 0 and less than 255<br>")
        print("Return to <a href=\"../index.html\">start page</a>")
        sys.exit()

    if int(ip_addr4) <= 0 or int(ip_addr4) >=255:
        print()
        print("ERROR: Not valid 4th octet IP address<br><br>")
        print("Must be greater than 0 and less than 255i<br>")
        print("Return to <a href=\"../index.html\">start page</a>")
        sys.exit()

except ValueError:
    print("ERROR: An improper number was provided.  Please try again.<br><br>")
    print("Return to <a href=\"../index.html\">start page</a>")
    sys.exit()

#Print out the System IP Address

system_ip_addr = "*******" + ip_addr3 + "." + ip_addr4

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

write_sha = ""
write_aes = ""

for line in output.splitlines():
    hashline = line.split()
    if hashline[0] == "SHA":
        write_sha = hashline[2]

    if hashline[0] == "AES":
        write_aes = hashline[2]

#Create the Read SNMP hash
try:
    output = os.popen("java -client -classpath {} {} SHA {} {}".format(classpath, jar, read_passwd, engineid)).read()
except OSError:
    print("Error: Java script did not execute correctly")
    print("Exiting....")
    sys.exit()

for line in output.splitlines():
    hashline = line.split()
    if hashline[0] == "SHA":
        read_sha = hashline[2]

    if hashline[0] == "AES":
        read_aes = hashline[2]


'''
We're going to print out all of the information
'''
print("-" * 80)
print("<br>")
print ("{:>20} {:<30} <br>".format("<b>System IP Address</b>:", system_ip_addr))
print ("{:>20} {:<30}".format("<b>EngineID</b>:", engineid))
print("<br>")
print("-"*80)
print("<br><br>")
print("-"*80)
print("<br>")
print("<b>SNMP Write Hash</b>")
print("<br>")
print("-"*80)
print("<br>")
print("{} {}".format("<b>SHA</b>:", write_sha))
print("<br>")
print("{} {}".format("<b>AES</b>:", write_aes))
print("<br>")
print("-"*80)
print("<br>")
print("-"*80)
print("<br>")
print("<b>SNMP Read Hash</b>")
print("<br>")
print("-"*80)
print("<br>")
print("{} {}".format("<b>SHA</b>:", read_sha))
print("<br>")
print("{} {}".format("<b>AES</b>:", read_aes))
print("<br>")
print("-"*80)
print("<br>")




