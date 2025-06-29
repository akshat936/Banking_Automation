import gmail

def send_mail_for_openacn(to_mail,uacno,uname,upass,udate):
    con=gmail.GMail('saxenaakshat027@gmail.com','aqci cknn kelp wzuj')
    sub="Account opened with ABC Bank"
    body=f""" Dear{uname},
    Your account has been opened succesfully with ABC Bank and deatils are
ACN={uacno}
PASS={upass}
open date={udate}

Kindly change your password when you login for the first time.
Thanks
ABC BANK
Gurugram
"""
    msg=gmail.Message(to=to_mail,subject=sub,text=body)
    con.send(msg)

def send_otp(to_mail,uname,uotp):
    con=gmail.GMail('saxenaakshat027@gmail.com','aqci cknn kelp wzuj')
    sub="Otp for password recovery"
    body=f""" Dear{uname},
Your otp ={uotp}


Kindly verify otp for password recovery.
Thanks
ABC BANK
Gurugram
"""
    msg=gmail.Message(to=to_mail,subject=sub,text=body)
    con.send(msg)