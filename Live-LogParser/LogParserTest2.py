import smtplib
import string
import os 
import HTML
import datetime
from datetime import date, timedelta
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import formatdate
from collections import OrderedDict

def parse(file_name):
 try:
    line_list = [line for line in open(file_name, "r")]
    response_times = []
    response_dict=dict()
    for line in line_list:
        log_parts = line.split('|')
        # if(len(log_parts) > 0) : Defensive Programming
        #print log_parts[1]
        log_rawurl = log_parts[0].split('-')
        log_url = log_rawurl[1].split('?')
        url = log_url[0]+" "+"("+log_parts[1]+")"
        #converting the data type of response_time to float
        response_time = float(log_parts[3])
        if response_dict.has_key(url):
            response_dict[url].append(response_time)
        else:
            response_dict[url]=[response_time]
    return response_dict
 except IOError: 
        print "Error: Can't find the file "            
        ErrorFilePath = 'C:\Documents and Settings\murali\pyth\HTML\Error-Report.html'
        sendEmail("lee2kris@gmail.com","hayagriventerprises@gmail.com",ErrorFilePath)
        
            
# returns a dict with key as url and value as average
def compute_average(response_dict):
    avg_response = dict()
    for k, v in response_dict.items():
       sum_response_times = 0.0
       for item in v:
            sum_response_times = sum_response_times+ item
       avg_res = sum_response_times/len(v)     
       avg_reponse_time = round(avg_res,2)
       avg_response[k] = avg_reponse_time 
    return avg_response   

          
#sorting the avg_response time
def sort(x):
    x_sorted_by_value = dict()
    x_sorted_by_value = OrderedDict(sorted(x.items(), key=lambda s: s[1],reverse=True))    
    return x_sorted_by_value
    
#Displaying the avg_response time in HtmlFormat      
def HtmlFormat(response_dict):       
    # open an HTML file to show output in a browser
   print response_dict 
   HTMLFILE = 'ResponseTime-Report.html'
   f = open(HTMLFILE, 'w')
   t = HTML.Table(header_row=['URL(Request Type)','Max Time','Min Time', 'Average ResponseTime(ms)','Number of Hits'],
     col_width=['70%','10%','10%','10%','10%'],
     col_align=['left','center','center','center','Center'],
     col_styles=['font-size: 105%','','','background-color:lightgrey','font-size:105%'])
   for k, v in response_dict.items():
       sum_response_times = 0.0
       maximum = max(v)
       minimum = min(v)
       print maximum
       print minimum
       for item in v:
            sum_response_times = sum_response_times+ item
       avg_res = sum_response_times/len(v)     
       avg_reponse_time = round(avg_res,2)
       avg_response[k] = avg_reponse_time
       t.rows.append(["%s"% k,"%s"% maximum,"%s"% minimum,"%s"% avg_reponse_time,"%s"% len(v)])
   htmlcode = str(t)
   #print htmlcode
   f.write(htmlcode)
   f.write('<p>\n')
    
#Send Email function      
def sendEmail(TO,FROM,FilePath):
    HOST = "smtp.gmail.com"
 
    msg = MIMEMultipart()
    msg["From"] = FROM
    msg["To"] = TO
    if FilePath == ResponseFilePath:
       msg["Subject"] = "Response Time Report (%s) - Local"%date
    else:
       msg["Subject"] = "Error Report (%s) - Local"%date
    msg['Date']    = formatdate(localtime=True)
    
 
    # attach a file
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open("%s"% FilePath ,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename("%s"% FilePath))
    body = '''Team,\n
Please check the Auto-generate ResponseTimeLog-Report.\n\n
Regards,
QA Team
    '''          
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(part)
 
    server = smtplib.SMTP(HOST)
    server.starttls()
    server.login(FROM,'')
     
    try:
        failed = server.sendmail(FROM, TO, msg.as_string())
        print "Mail Sent Successfully"
        server.close()
    except Exception, e:
        errorMsg = "Unable to send email. Error: %s" % str(e)



if __name__ == "__main__":
 yesterday = date.today() - timedelta(1)
 date = yesterday.strftime('%Y_%m_%d')
 ResponseFilePath = 'C:\Documents and Settings\murali\pyth\HTML\ResponseTime-Report.html'
 response_dict = parse("C:\Documents and Settings\murali\Desktop\RequestLog_%s.txt"%date)
 avg_response = compute_average(response_dict)
 x_sorted_by_value=sort(response_dict)
 HtmlFormat(x_sorted_by_value)
# ResponseFilePath = 'C:\Documents and Settings\murali\pyth\HTML\ResponseTime-Report.html'
 sendEmail("lee2kris@gmail.com","hayagriventerprises@gmail.com",ResponseFilePath)
   
#output(avg_response)
