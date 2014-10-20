# -*- coding: utf-8 -*-
import pyodbc
import code
import smtplib
import time 
from email.MIMEMultipart  import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from email import encoders
import datetime
import sys
import os
import os.path
import argparse


class MyApplication:       
    
        
    def websData(self,clientcode):       
        #clientcode ="broker8888"
        sql = "Driver={SQL Server};Server=192.168.0.181;Database="+ clientcode+ ";UID=sa;PWD=popproduct;"
        #print sql
        cnxn = pyodbc.connect(sql)
        filename1 = datetime.datetime.now().strftime("%Y%m%d")
    #cnxn = pyodbc.connect(r'Driver={SQL Server};Server=.\sqlexpress;Database=webstatement;UID=sa;PWD=POPproduct01;')
    
        cursor = cnxn.cursor()
        print "start:checking in "+clientcode
        
        #current day
        #select * from statements  where DATE= convert(varchar(10),getDate(),120)
        cursor.execute("SELECT statements.Accode,client.email ,statements.date  FROM statements join client on statements.Accode=  client.cid where statements.type='d' and date='2014-10-3'")
        while 1:
           row = cursor.fetchone()
           if not row:
               break
           ACCODE= row[0]
           email = row[1]
           if email is not None :
               #print row[0],row[1],row[2]  
               self.sendmail (ACCODE,clientcode,email)      
                       
        cnxn.close()
        self.wrotelog(clientcode)

    def clientTxt(self,ACCode,clientcode):
        date = (time.strftime("%d/%m/%Y"))
        replacements = {'<%ACCODE%>':ACCode,'<%clientcode%>':clientcode, '<%date%>':date}
        infile = open('test.txt')
        outfile = open('testw.txt', 'w')
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)
        infile.close()
        outfile.close()

            
    def sendmail(self,ACCode,clientcode,email):
        SUBJECT = "Email Data"
        msg = MIMEMultipart()
        self.clientTxt(ACCode,clientcode)
        msg.attach(MIMEText(file("testw.txt").read()))
    #msg.attach(MIMEImage(file("pic.jpg").read()))
        sender = 'kelvinl@infocenter.com.hk'
        receivers = ['chuntung99@gmail.com']
        date = (time.strftime("%d/%m/%Y"))
        message = """webstatement notifcation "
  
        """
        msg['Subject'] = 'Webstatement notififcation on ' + date
        try:
           smtpObj = smtplib.SMTP('192.168.0.17')
           date = (time.strftime("%d/%m/%Y"))
    
           message = message.format (date,email)
           smtpObj.sendmail(sender, email, msg.as_string())         
           print "Successfully sent email of",ACCode ,email
         
        except smtplib.SMTPException:
           print "Error: unable to send email"
       
        
    def wrotelog(self,clientcode):
         filename1 = datetime.datetime.now().strftime("%Y%m%d")        #
                                   
         flag = os.path.isfile('log/'+clientcode+filename1 + '.log') 
         if not flag:
             print "write"+clientcode+" log file:done"
             sys.stdout = open('log/'+clientcode+filename1 + '.log', 'w')
         else:
             print "error" +clientcode +" is already done"              
    #    cnxn.close()
def main():
    s = MyApplication()
    total = len(sys.argv)
    
   # s.websData("broker8888")
    #s.websData("broker9999")
    
    #s.sendmail("chuntung99@gmail.com")
    # Get the total number of args passed to the demo.py
    total = len(sys.argv)
 
# Get the arguments list 
    cmdargs = str(sys.argv)
 
# Print it
   # print ("The total numbers of args passed to the script: %d " % total)
    #print ("Args list: %s " % cmdargs)
# Pharsing args one by one 
    #print ("Script name: %s" % str(sys.argv[0]))
    #print ("First argument: %s" % str(sys.argv[1]))
    s.websData(str(sys.argv[1]))
#    print ("Second argument: %s" % str(sys.argv[2]))

if __name__ == "__main__":
    main()
    

#filename1 = datetime.datetime.now().strftime("%Y%m%d")
#sys.stdout = open(filename1 + '.log', 'w')
