# Password2Key Adaption

## Background
In deploying a Nokia router, you may have to configure SNMPv3 on it.  For reasons that I still do not understand, Nokia routers require a weird key to be generated for SNMPv3 to be configured.  This key is a hash generated from the combination of the SNMP EngineID and SNMP user password.  To generate this key a Nokia created script (password2key.bash), only found on their NFM-P server, must be executed.  

In my environment, I prefer that my designers and technicians not need to access the NFM-P server to execute this script.  Instead, I prefer that a web interface be available where input can be provided and the needed keys generated.  

## Needed JAR Files
There are three JAR files that need to be collected for this to work correctly.  They are as follows:

    /opt/nsp/nfmp/server/nms/lib/tools/tools.jar
    /opt/nsp/nfmp/server/nms/lib/thirdparty/webnms/adventnet/AdventNetSnmp.jar
    /opt/nsp/nfmp/server/nms/lib/thirdparty/webnms/adventnet/AdventNetLogging.jar

## Script password2key.py
Place the above JAR files in the same folder as password2key.py.  In my case, in creating a web interface, place them in `/var/www/cgi-bin`.

## Web Input
I made a simple input website which will call the above Python script.  Place the `index.html` file into `/var/www/html`.     
