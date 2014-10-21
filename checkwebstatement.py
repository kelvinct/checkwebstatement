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
    def checkimpdb(self,clientcode,uploadfiledate): 
        sql_impdb = "Driver={SQL Server};Server=192.168.0.181;Database=impdb ;UID=sa;PWD=popproduct;"        
        cnxn = pyodbc.connect(sql_impdb)        
        cursor2 =  cnxn.cursor()
        cursor2.execute ("SELECT DIStinct clientcode , UploadFileDate ,status FROM  ProcessQry WHERE UploadFile LIKE '%RPV%' and UploadFileDate ='"+uploadfiledate+"' and clientcode='"+clientcode +"'")#'broker8888'")
        status = "p"
        while 1:
           row2 = cursor2.fetchone()
           if not row2:
              break
           clientcode= row2[0]
           UploadFileDate = "20"+row2[1]
           status = row2[2]
           print "impdb:"+clientcode+">" + uploadfiledate + ",status:"+ status
           
        #filename1 = datetime.datetime.now().strftime("%Y%m%d")
          
        return clientcode,UploadFileDate,status
    
    def websData(self,clientcode):      

        print "----------------------------------------------------------------"          
        #uploadfiledate = datetime.datetime.now().strftime("%Y%m%d")
        clientcode,UploadFileDate,status = (self.checkimpdb(clientcode,"141003"))
        print clientcode 
        print UploadFileDate
        print status
        print "----------------------------------------------------------------"

        
        sql = "Driver={SQL Server};Server=192.168.0.181;Database="+ clientcode+ ";UID=sa;PWD=popproduct;"
        cnxn = pyodbc.connect(sql)         
        cursor = cnxn.cursor()
        print "start:checking in "+clientcode        
        filename1 = datetime.datetime.now().strftime("%Y%m%d")
        date = (time.strftime("%d%m%Y"))
        f = open("m_"+clientcode+date+".bat","a")                  

        #select * from statements  where DATE= convert(varchar(10),getDate(),120)
       # self.wrotelog(clientcode) 
       
        cursor.execute("SELECT statements.Accode,client.email ,statements.date  FROM statements join client on statements.Accode=  client.cid where statements.type='d' and date='2014-10-3'")
        while 1:
           row = cursor.fetchone()
           if not row:
               break
           ACCODE= row[0]
           email = row[1]          
           if email is not None :
               email =  email.replace(" ", "")
               #print email + "1"
               #print row[0],row[1],row[2]  
               flag = os.path.isfile(ACCODE+date+".txt")
               if not flag: 
                   filename = self.clientTxt(ACCODE,'broker8888',UploadFileDate)
                   #print filename
                  #SMTP -fsupport@infocenter.com.hk -tchuntung99@.com  -hmail.infocenter.com.hk -aA18.PDF -sWeb statement noification A28 For  2014-10-03  Import Success -ifile.log
                   b = ('SMTP -fsupport@infocenter.com.hk -t'+ email +" -h192.168.0.17 -sWebstatenet notification on " +  UploadFileDate + ' -i'+ filename + " >> "+"ws"+date+".log")
                   print b
                   f.write( b+"\n")
               #self.sendmail (ACCODE,clientcode,email)                       
        cnxn.close()
      #  f.close()

    def clientTxt(self,ACCode,clientcode,UploadFileDate):
        date = (time.strftime("%d%m%Y"))
        replacements = {'<%ACCODE%>':ACCode,'<%clientcode%>':clientcode, '<%date%>':UploadFileDate}
        infile = open('test.txt')
        outfile = open(ACCode+ date +'.txt', 'w')
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)
        infile.close()
        outfile.close()
        return outfile.name
            
    def sendmail(self,ACCode,clientcode,email):
        SUBJECT = "Email Data"
        msg = MIMEMultipart()
        self.clientTxt(ACCode,clientcode)
        msg.attach(MIMEText(file("testw.txt").read())) 
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
         filename1 = datetime.datetime.now().strftime("%Y%m%d")                                    
         flag = os.path.isfile('log/'+clientcode+filename1 + '.log') 
         if not flag:
             print "write"+clientcode+" log file:done"
             f = open (fil)
             sys.stdout = open('log/'+clientcode+filename1 + '.log', 'w')
             return True       
         else:
             print "error" +clientcode +" is already done"
             return False              
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
