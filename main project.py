import sqlite3
from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog
import time
from PIL import Image,ImageTk  # to insert the image
from tkinter.ttk import Combobox # tkinter is the package and ttk is the module and combobox is the class
import random
import project_tables
import project_mail
import os,shutil

def generate_captcha(): # function to genearte the captcha
    captcha=[]

    for i in range(3):
        c=chr(random.randint(65,90))
        captcha.append(c) # list does not return anything

        n=random.randint(0,9)
        captcha.append(str(n))
    
    random.shuffle(captcha)
    captcha=' '.join(captcha)
    return captcha

def refresh():
    captcha=generate_captcha()# by clicking on refresh new captcha will be generated
    captcha_lbl.configure(text=captcha) #  called the captcha label from the bottom

def show_pass():
    pass_e.config(show='' if pass_e.cget('show') == '*' else '*')

root=Tk() # object of root window
root.state("zoomed")  # full screen window
root.configure(bg="powder blue")  # add background color
root.title("ABC BANKING SOFTWARE") # title at corner
root.resizable(width=False,height=False) # fix the window 

title_lbl=Label(root,text="Banking Automation",bg="powder blue",font=('Arial',50,"bold","underline"))
title_lbl.pack()

today_lbl=Label(root,text=time.strftime("%A %d %B %Y"),bg="powder blue",font=('Arial',18,"bold"),fg="red")
today_lbl.pack(pady=10)


img=Image.open("images/ABC_BANK.jpg").resize((300,150)) # inserting the image in root window
img_bitmap=ImageTk.PhotoImage(img,master=root)# converting it into the bitmap by imagetk lib

logo_lbl=Label(root,image=img_bitmap)
logo_lbl.place(relx=0,rely=0)

img2=Image.open("Images/ABC BANK2.jpg").resize((300,150))
img_bitmap2=ImageTk.PhotoImage(img2,master=root)

logo_lbl=Label(root,image=img_bitmap2)
logo_lbl.place(relx=.8,rely=0)

footer_lbl=Label(root,text="Developed by Akshat Saxena",bg="powder blue",font=('Arial',20,"bold"),fg="blue")
footer_lbl.pack(side="bottom",pady=3)

def main_screen(): # function to create the frame 
    def forgot():
        frm.destroy()
        forgot_screen()
    
    def login():
        uacn=acn_e.get()
        upass=pass_e.get()
        ucap=captcha_e.get()
        actual_cap=captcha_lbl.cget('text')
        actual_cap=actual_cap.replace(' ','')
        utype=user_combo.get()
        
        if utype=='Admin':
            
            if uacn=='0' and upass=='admin':
                if ucap==actual_cap:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror('Login','Invalid Captcha')
            else:
                   messagebox.showerror('Login','Invalid ACN/PASS/UTYPE') 

        elif utype=='User':
            global acno
            if ucap==actual_cap:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where accounts_acno=? and accounts_pass=?'
                curobj.execute(query,(uacn,upass))

                tup=curobj.fetchone()
                conobj.close()
                if tup==None:
                    messagebox.showerror('User Login','Invalid ACN/PASS')
                else:
                    acno=tup[0]
                    frm.destroy()
                    user_screen(uacn)
            else:
                messagebox.showerror('Login','Invalid Captcha')



        else:
            messagebox.showerror('Login','Kindly select valid user type')
    
    
    frm=Frame(root)
    frm. configure(bg="light pink")
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.77) # widhth and height of the frame

    user_lbl=Label(frm,text="User Type",bg="light pink",font=('Arial',18,),fg="red")
    user_lbl.place(relx=.32,rely=.05)

    user_combo=Combobox(frm,values=['Admin','User','---select---'],state='readonly',font=('',18))
    user_combo.current(2)
    user_combo.place(relx=.42,rely=.05)

    acn_lbl=Label(frm,text="ACN",bg="light pink",font=('Arial',18,),fg="blue")
    acn_lbl.place(relx=.32,rely=.15)

    acn_e=Entry(frm,font=('Arial',18),bd=5)
    acn_e.place(relx=.42,rely=.15)
    acn_e.focus()

    pass_lbl=Label(frm,text="Password",bg="light pink",font=('Arial',18,),fg="red")
    pass_lbl.place(relx=.32,rely=.25)

    global pass_e
    pass_e=Entry(frm,font=('Arial',18),bd=5,show='*')
    pass_e.place(relx=.42,rely=.25)

    showpass_btn=Button(frm,text="show password",bg="white",fg="blue",font=('Arial',9),bd=5,command=show_pass)
    showpass_btn.place(relx=.62,rely=.26)

    global captcha_lbl
    captcha_lbl=Label(frm,text= generate_captcha(),bg="white",font=('Arial',18,),fg="red")
    captcha_lbl.place(relx=.36,rely=.38)

    ref_btn=Button(frm,text="Refresh",bg="white",fg="blue",font=('Arial',12),bd=5,command= refresh)
    ref_btn.place(relx=.48,rely=.38)

    inputcaptcha_lbl=Label(frm,text="Captcha",bg="light pink",font=('Arial',18),fg="blue")
    inputcaptcha_lbl.place(relx=.32,rely=.55)

    captcha_e=Entry(frm,font=('Arial',18),bd=5)
    captcha_e.place(relx=.42,rely=.55)

    login_btn=Button(frm,text="Login",bg="powder blue",font=('Arial',15),bd=5,command=login)
    login_btn.place(relx=.43,rely=.65)

    def reset():
        
            user_combo.current(2)
            acn_e.delete(0,"end")
            pass_e.delete(0,"end")
            captcha_e.delete(0,"end")
            acn_e.focus()

    reset_btn=Button(frm,text="Reset",bg="powder blue",command=reset,font=('Arial',15),bd=5)
    reset_btn.place(relx=.51,rely=.65)

    forgot_btn=Button(frm,text="Forgot password",bg="powder blue",font=('Arial',15),bd=5,width=20,command=forgot)
    forgot_btn.place(relx=.42,rely=.78)

    


def admin_screen():


    def open_acn():
        def open_acn_db():
            
                uname=name_e.get()
                uemail=email_e.get()
                umob=mob_e.get()
                ugen=gen_combo.get()
                ubal=0.0
                uopendate=time.strftime("%A,%d %B %Y")
                
                upass=generate_captcha().replace(' ','')

                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                query='insert into accounts values(null,?,?,?,?,?,?,?)'
                curobj.execute(query,(uname,upass,uemail,umob,ugen,uopendate,ubal))
                conobj.commit()
                conobj.close()
                
                
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()

                query="select max(accounts_acno) from accounts"
                curobj.execute(query)

                uacno=curobj.fetchone()[0]
                conobj.close()

                try:
                    project_mail.send_mail_for_openacn(uemail,uacno,uname,upass,uopendate)
                    msg=f'Account Opened with Acno{uacno} and mail sent to {uemail} check spam also'
                    messagebox.showinfo('Open Account',msg)

                except Exception as msg:
                    messagebox.showerror("Error",msg)

        def reset():
                name_e.delete(0,"end")
                email_e.delete(0,"end")
                mob_e.delete(0,"end")
                gen_combo.current(3)
                name_e.focus()

        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='powder blue')
        ifrm.place(relx=.18,rely=.2,relwidth=.7,relheight=.73)

        name_lbl=Label(ifrm,text="Name",bg="powder blue",font=('Arial',18,))
        name_lbl.place(relx=.05,rely=.02)

        name_e=Entry(ifrm,font=('Arial',18),bd=5)
        name_e.place(relx=.05,rely=.1)
        name_e.focus()

        email_lbl=Label(ifrm,text="Email",bg="powder blue",font=('Arial',18,))
        email_lbl.place(relx=.5,rely=.02)

        email_e=Entry(ifrm,font=('Arial',18),bd=5)
        email_e.place(relx=.5,rely=.1)

        mob_lbl=Label(ifrm,text="Mob",bg="powder blue",font=('Arial',18,))
        mob_lbl.place(relx=.05,rely=.3)

        mob_e=Entry(ifrm,font=('Arial',18),bd=5)
        mob_e.place(relx=.05,rely=.4)

        gen_lbl=Label(ifrm,text="Gender",bg="powder blue",font=('Arial',18,))
        gen_lbl.place(relx=.5,rely=.32)

        gen_combo=Combobox(ifrm,values=['Male','Female','others','---select---'],state='readonly',font=('',18))
        gen_combo.current(3)
        gen_combo.place(relx=.5,rely=.43)

        open_btn=Button(frm,text="Open account",bg="light green",font=('Arial',15),bd=5,command=open_acn_db)
        open_btn.place(relx=.35,rely=.66)

        reset_btn=Button(frm,text="Reset",command=reset,bg="light yellow",font=('Arial',15),bd=5)
        reset_btn.place(relx=.49,rely=.66)

        
    def del_acn():

        def send_otp():
           uacn= acn_e.get()
           

           conobj=sqlite3.connect(database='bank.sqlite')
           curobj=conobj.cursor()
           query='select * from accounts where accounts_acno=?'
           curobj.execute(query,(uacn,))

           tup=curobj.fetchone()
           conobj.close()
           if tup==None:
               messagebox.showerror('Delete Account','Record not found')
           else:
               otp=str(random.randint(1000,9999))
               project_mail.send_otp(tup[3],tup[1],otp)
               messagebox.showinfo('Delete Account','otp sent to given registered mail id')

               otp_e=Entry(ifrm,font=('Arial',18),bd=5)
               otp_e.place(relx=.42,rely=.36)

               def verify():
                   uotp=otp_e.get()
                   if otp==uotp:
                       resp=messagebox.askyesno('Delete Account','Do you want to delete the account')
                       if resp==False:
                           frm.destroy()
                           admin_screen()
                           return
                       conobj=sqlite3.connect(database='bank.sqlite')
                       curobj=conobj.cursor()
                       query='delete from accounts where accounts_acno=?'
                       curobj.execute(query,(uacn,))
                       messagebox.showinfo('Delete Account','Account deleted successfully')
                       frm.destroy()
                       admin_screen()
                       conobj.commit()
                       conobj.close()
                       
                   else:
                       messagebox.showerror('Delete Account','Incorrect Otp')

               verify_btn=Button(ifrm,text="Verify",command=verify,bg="powder blue",font=('Arial',12),bd=5)
               verify_btn.place(relx=.68,rely=.36)
           
        
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='powder blue')
        ifrm.place(relx=.18,rely=.2,relwidth=.7,relheight=.73)

        acn_lbl=Label(ifrm,text="ACN",bg="powder blue",font=('Arial',18,))
        acn_lbl.pack()

        acn_e=Entry(ifrm,font=('Arial',18),width=15,bd=5)
        acn_e.pack()

        otp_btn=Button(frm,text="send otp",command=send_otp,bg="sky blue",font=('Arial',15),bd=5)
        otp_btn.place(relx=.54,rely=.35)


    def view_acn():
        def view_details():
            uacn=acn_e.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))

            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
               messagebox.showerror('Delete Account','Record not found')
            else:
                details=f""" user name={tup[1]}
user mailid ={tup[3]}
user mob= {tup[4]}
Acn open date= {tup[6]}
user balance= {tup[7]}
user gender ={tup[5]}
"""
                messagebox.showinfo("View Account",details)
        
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='powder blue')
        ifrm.place(relx=.18,rely=.2,relwidth=.7,relheight=.73)

        Acn_lbl=Label(ifrm,text="Acn",bg="powder blue",font=('Arial',18,))
        Acn_lbl.place(relx=.08,rely=.02)

        acn_e=Entry(ifrm,font=('Arial',18),bd=5)
        acn_e.place(relx=.2,rely=.02)  

        view_btn=Button(ifrm,text="View Acn",command=view_details,bg="light pink",font=('Arial',12),bd=5)
        view_btn.place(relx=.5,rely=.02)

    def logout():
        resp=messagebox.askyesno("LOGOUT",'DO YOU WANT TO LOGOUT?')
        if resp==True:
            frm.destroy()
            main_screen() 


    frm=Frame(root)
    frm. configure(bg="light pink")
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.77) 

    wel_lbl=Label(frm,text="Welcome, Admin",bg="light pink",font=('Arial',18,),fg='green')
    wel_lbl.place(relx=.0,rely=.0)

    logout_btn=Button(frm,text="Logout",bg="Powder blue",font=('Arial',15),bd=5,command=logout)
    logout_btn.place(relx=.94,rely=.0)

    open_btn=Button(frm,text="Open Acn",bg="GREEN",font=('Arial',15),bd=5,fg='white',command=open_acn)
    open_btn.place(relx=.35,rely=.0)

    del_btn=Button(frm,text="Delete Acn",bg="red",font=('Arial',15),bd=5,command=del_acn)
    del_btn.place(relx=.45,rely=.0)
    
    view_btn=Button(frm,text="View Acn",bg="yellow",font=('Arial',15),bd=5,command=view_acn)
    view_btn.place(relx=.55,rely=.0)

def forgot_screen():
        def back():
            frm.destroy()
            main_screen()

        def send_otp():
           uacn= acn_e.get()
           uemail=email_e.get()
           ucap=captcha_e.get()
           if ucap!=forgot_captcha.replace(' ',''):
               messagebox.showerror('Forgot Password','Incorrect Captcha')
               return

           conobj=sqlite3.connect(database='bank.sqlite')
           curobj=conobj.cursor()
           query='select * from accounts where accounts_acno=? and accounts_email=?'
           curobj.execute(query,(uacn,uemail))

           tup=curobj.fetchone()
           conobj.close()
           if tup==None:
               messagebox.showerror('Forgot Password','Record not found')
           else:
               otp=str(random.randint(1000,9999))
               project_mail.send_otp(uemail,tup[1],otp)
               messagebox.showinfo(f'otp sent to given registered mail id{uemail}')

               otp_e=Entry(frm,font=('Arial',18),bd=5)
               otp_e.place(relx=.42,rely=.78)

               def verify():
                   uotp=otp_e.get()
                   if otp==uotp:
                       messagebox.showinfo('Forgot password',f'Your pass = {tup[2]}')
                   else:
                       messagebox.showerror('Forgot Password','Incorrect Otp')

               verify_btn=Button(frm,text="Verify",command=verify,bg="powder blue",font=('Arial',15),bd=5)
               verify_btn.place(relx=.6,rely=.78)
           
               

        frm=Frame(root)
        frm. configure(bg="light pink")
        frm.place(relx=0,rely=.18,relwidth=1,relheight=.77)

        back_btn=Button(frm,text="Back",bg="sky blue",font=('Arial',15),bd=5,command=back)
        back_btn.place(relx=0,rely=0)


        acn_lbl=Label(frm,text="ACN",bg="light pink",font=('Arial',18,),fg="blue")
        acn_lbl.place(relx=.32,rely=.15)

        acn_e=Entry(frm,font=('Arial',18),bd=5)
        acn_e.place(relx=.42,rely=.15)
        acn_e.focus()

        email_lbl=Label(frm,text="Email",bg="light pink",font=('Arial',18,),fg="blue")
        email_lbl.place(relx=.32,rely=.25)

        email_e=Entry(frm,font=('Arial',18),bd=5)
        email_e.place(relx=.42,rely=.25)

        global captcha_lbl
        forgot_captcha=generate_captcha()
        captcha_lbl=Label(frm,text= forgot_captcha,bg="white",font=('Arial',18,),fg="red")
        captcha_lbl.place(relx=.36,rely=.38)

        ref_btn=Button(frm,text="Refresh",bg="white",fg="blue",font=('Arial',12),bd=5,command= refresh)
        ref_btn.place(relx=.48,rely=.38)

        captcha_e=Entry(frm,font=('Arial',18),bd=5)
        captcha_e.place(relx=.42,rely=.55)

        otp_btn=Button(frm,text="send otp",command=send_otp,bg="powder blue",font=('Arial',15),bd=5)
        otp_btn.place(relx=.43,rely=.65)

        reset_btn=Button(frm,text="Reset",bg="powder blue",font=('Arial',15),bd=5)
        reset_btn.place(relx=.53,rely=.65)

def user_screen(uacn=None):
    global ifrm
    ifrm=None

    def ifrm_destroy():
        if ifrm is not None:
            ifrm.destroy()
            ifrm=None

    def get_details():
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=?'
        curobj.execute(query,(uacn,))

        tup=curobj.fetchone()
        conobj.close()
        return tup
           

    def logout():
        resp=messagebox.askyesno("LOGOUT",'DO YOU WANT TO LOGOUT?')
        if resp==True:
            frm.destroy()
            main_screen() 

    def check_details_screen():
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
            ifrm=None
        
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='powder blue')
        ifrm.place(relx=.18,rely=.2,relwidth=.6,relheight=.73)

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
        tup=curobj.fetchone()
        conobj.close()

        details=f"""     Account No.= {tup[0]}

        Name={tup[1]}

        Mail id ={tup[3]}

        Mob no.= {tup[4]}

        Available balance= {tup[7]}

        Acn open date= {tup[6]}
"""
        det_lbl=Label(ifrm, text= details,bg='powder blue',font=('arial',15,'bold'))
        det_lbl.place(relx=.2,rely=.2)

    def update_details_screen():
        

        def update_db():
           global acno
           uname= name_e.get()
           uemail=email_e.get()
           upass=pass_e.get()
           umob=mob_e.get()

           conobj=sqlite3.connect(database='bank.sqlite')
           curobj=conobj.cursor()
           query=('update accounts set accounts_name=?,accounts_pass=?,accounts_mob=?,accounts_email=? where accounts_acno=?')
           curobj.execute(query,(uname,upass,umob,uemail,acno))
           conobj.commit()
           conobj.close()
           messagebox.showinfo('Update Details','Profile Updated')
           frm.destroy()
           user_screen(uacn)


        global ifrm
        if ifrm is not None:
            ifrm.destroy()
            ifrm=None

        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.18,rely=.2,relwidth=.6,relheight=.73)

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
        tup=curobj.fetchone()
        conobj.close()

        name_lbl=Label(ifrm,text="Name",bg='white',font=('Arial',18,))
        name_lbl.place(relx=.05,rely=.02)

        
        name_e=Entry(ifrm,font=('Arial',18),bd=5)
        name_e.place(relx=.05,rely=.1)
        name_e.insert(0,tup[1])
        name_e.focus()

        pass_lbl=Label(ifrm,text="Password",bg="white",font=('Arial',18,))
        pass_lbl.place(relx=.5,rely=.02)

        pass_e=Entry(ifrm,font=('Arial',18),bd=5)
        pass_e.insert(0,tup[2])
        pass_e.place(relx=.5,rely=.1)
        

        mob_lbl=Label(ifrm,text="Mob",bg="white",font=('Arial',18,))
        mob_lbl.place(relx=.05,rely=.3)

        mob_e=Entry(ifrm,font=('Arial',18),bd=5)
        mob_e.insert(0,tup[4])
        mob_e.place(relx=.05,rely=.4)

        email_lbl=Label(ifrm,text="Email",bg="white",font=('Arial',18,))
        email_lbl.place(relx=.5,rely=.32)

        email_e=Entry(ifrm,font=('Arial',18),bd=5)
        email_e.insert(0,tup[3])
        email_e.place(relx=.5,rely=.4)

        update_details_btn=Button(frm,text="update",bg="light green",font=('Arial',16),bd=5,command=update_db)
        update_details_btn.place(relx=.4,rely=.66)

    def deposit_details_screen():

        def deposit():
            uamt=float(amt_e.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="update accounts set accounts_bal=accounts_bal+? where accounts_acno=?"
            curobj.execute(query,(uamt,acno))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select accounts_bal from accounts where accounts_acno=?"
            curobj.execute(query,(acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            t=str((time.time()))
            utxn=('txn'+t[:t.index('.')])
            query="select accounts_bal from accounts where accounts_acno=?"
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="insert into stmts values(?,?,?,?,?,?)"
            curobj.execute(query,(acno,uamt,'CR.',time.strftime('%d-%m-%Y %r'),ubal,utxn))
            conobj.commit()
            conobj.close()

            messagebox.showinfo('Deposit',f'{uamt} Amount deposited')
            frm.destroy()
            user_screen(uacn)

        global ifrm
        if ifrm is not None:
            ifrm.destroy()
            ifrm=None

        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.18,rely=.2,relwidth=.6,relheight=.73)

        Amt_lbl=Label(ifrm,text="Amount",bg='white',font=('Arial',18,))
        Amt_lbl.place(relx=.08,rely=.02)

        amt_e=Entry(ifrm,font=('Arial',18),bd=5)
        amt_e.place(relx=.2,rely=.02)  

        deposit_detail_btn=Button(ifrm,text="Deposit",command=deposit,font=('Arial',15),bd=5)
        deposit_detail_btn.place(relx=.55,rely=.02)

    def withdraw_details_screen():
        def withdraw():
            uamt=float(amt_e.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select accounts_bal from accounts where accounts_acno=?"
            curobj.execute(query,(acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query="update accounts set accounts_bal=accounts_bal-? where accounts_acno=?"
                curobj.execute(query,(uamt,acno))
                conobj.commit()
                conobj.close()

                t=str((time.time()))
                utxn=('txn'+t[:t.index('.')])
                query="select accounts_bal from accounts where accounts_acno=?"
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query="insert into stmts values(?,?,?,?,?,?)"
                curobj.execute(query,(acno,uamt,'DEB.',time.strftime('%d-%m-%Y %r'),ubal-uamt,utxn))
                messagebox.showinfo('Withdraw',f'{uamt} withdrawn successfully')
                conobj.commit()
                conobj.close()
                frm.destroy()
                user_screen(uacn)
            else:

                messagebox.showinfo('Withdraw',f'Insufficient amount{ubal}')
                
            
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
            ifrm=None

        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='powder blue')
        ifrm.place(relx=.18,rely=.2,relwidth=.6,relheight=.73)

        Amt_lbl=Label(ifrm,text="Amount",bg="powder blue",font=('Arial',18,))
        Amt_lbl.place(relx=.08,rely=.02)

        amt_e=Entry(ifrm,font=('Arial',18),bd=5)
        amt_e.place(relx=.2,rely=.02)  

        withdraw_detail_btn=Button(ifrm,text="Withdraw",command=withdraw,bg="light pink",font=('Arial',15),bd=5)
        withdraw_detail_btn.place(relx=.55,rely=.02)

    def trnsfer_details_screen():
        def Transfer():
            toacn=to_e.get()
            uamt=float(amt_e.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select * from accounts where accounts_acno=?"
            curobj.execute(query,(acno,))
            to_tup=curobj.fetchone()
            conobj.close()

            if to_tup == None:
                messagebox.showerror('Transfer','Account not exist')
                return
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select accounts_bal from accounts where accounts_acno=?"
            curobj.execute(query,(acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            
            if ubal>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query_deduct="update accounts set accounts_bal=accounts_bal-? where accounts_acno=?"
                query_credit="update accounts set accounts_bal=accounts_bal+? where accounts_acno=?"
                
                curobj.execute(query_deduct,(uamt,acno))
                curobj.execute(query_credit,(uamt,toacn))
                conobj.commit()
                conobj.close()

                t=str((time.time()))
                utxn1=('txnDEB'+t[:t.index('.')])
                utxn2=('txnCR'+t[:t.index('.')])
                query="select accounts_bal from accounts where accounts_acno=?"
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query1="insert into stmts values(?,?,?,?,?,?)"
                query2="insert into stmts values(?,?,?,?,?,?)"

                curobj.execute(query1,(acno,uamt,'DEB.',time.strftime('%d-%m-%Y %r'),ubal-uamt,utxn1))
                
                curobj.execute(query2,(toacn,uamt,'CR.',time.strftime('%d-%m-%Y %r'),ubal+uamt,utxn2))
                messagebox.showinfo('Transfer',f'{uamt} Transfer successfully')
                conobj.commit()
                conobj.close()
                frm.destroy()
                user_screen(uacn)
            else:

                messagebox.showerror('Transfer',f'Insufficient amount{ubal}')

         
        global ifrm
        if ifrm is not None:
            ifrm.destroy()
            ifrm=None

        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='powder blue')
        ifrm.place(relx=.18,rely=.2,relwidth=.6,relheight=.73)

        to_acn_lbl=Label(ifrm,text="To Acno",bg="powder blue",font=('Arial',18,))
        to_acn_lbl.place(relx=.05,rely=.02)

        to_e=Entry(ifrm,font=('Arial',18),bd=5)
        to_e.place(relx=.2,rely=.02)  

        Amt_lbl=Label(ifrm,text="Amount",bg="powder blue",font=('Arial',18,))
        Amt_lbl.place(relx=.05,rely=.15)

        amt_e=Entry(ifrm,font=('Arial',18),bd=5)
        amt_e.place(relx=.2,rely=.15)  

        deposit_detail_btn=Button(ifrm,text="Transfer",command=Transfer,bg="light pink",font=('Arial',12),bd=5)
        deposit_detail_btn.place(relx=.4,rely=.3)

    def history_details_screen(): # inner frame of the history section

            global ifrm
            if ifrm is not None:
                ifrm.destroy()
                ifrm=None

            ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
            ifrm.configure(bg='white')
            ifrm.place(relx=.18,rely=.2,relwidth=.6,relheight=.73)

            from tktable import Table
            table_headers= ('Txn Id','Txn type','Amount','Updated bal ','date')
            mytable=Table(ifrm,table_headers,col_width=150,headings_bold=True)
            mytable.pack(pady=20)

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select stmts_txnid,stmts_type,stmts_amt,stmts_update_bal,stmts_date from stmts where stmts_acno=?"
            curobj.execute(query,(acno,))
            for tup in curobj:
                mytable.insert_row(tup)

            import sys
            del sys.modules['tktable']

            conobj.close()
            
            
            
    def update_pic():
        path=filedialog.askopenfilename()
        shutil.copy(path,f'Images/{uacn}.png')
        

        img=Image.open(f"Images/{uacn}.png").resize((130,110))# profile pic in the user section image 
        profile_bitmap=ImageTk.PhotoImage(img,master=root)# convert it into the bitmap
    
        profile_pic_lbl.image=profile_bitmap
        profile_pic_lbl.configure(image=profile_bitmap)

    
    frm=Frame(root) # maiin frame of the user screen 
    frm. configure(bg="light pink")
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.77) 

    wel_lbl=Label(frm,text=f"Welcome {get_details()[1]}",bg="light pink",font=('Arial',18,),fg='green')# user welcome label
    wel_lbl.place(relx=.0,rely=.0)

    if os.path.exists(f'Images/{uacn}.png'):
            path=f'Images/{uacn}.png'
    else:
            path="Images/profile pic.jpg"
    
    img=Image.open(path).resize((130,110))# profile pic in the user section image 
    profile_bitmap=ImageTk.PhotoImage(img,master=root)# convert it into the bitmap
    
    profile_pic_lbl=Label(frm,image=profile_bitmap)
    profile_pic_lbl.image=profile_bitmap # in under function we have to pass the image 
    profile_pic_lbl.place(relx=.005,rely=.06)

    update_pic_btn=Button(frm,text="update pic",command=update_pic,bg="light green",width=12,font=('Arial',15),bd=5)
    update_pic_btn.place(relx=.005,rely=.26)
    
    logout_btn=Button(frm,text="Logout",bg="cyan",font=('Arial',15),bd=5,command=logout)
    logout_btn.place(relx=.94,rely=.0)

    check_btn=Button(frm,text="Check details",bg="Powder blue",width=12,font=('Arial',15),bd=5,command=check_details_screen)
    check_btn.place(relx=.005,rely=.36)

    deposit_btn=Button(frm,text="Deposit",bg="light green",width=12,font=('Arial',15),bd=5,command=deposit_details_screen)
    deposit_btn.place(relx=.005,rely=.46)

    withdraw_btn=Button(frm,text="Withdraw",bg="red",width=12,font=('Arial',15),bd=5,command=withdraw_details_screen)
    withdraw_btn.place(relx=.005,rely=.56)

    update_btn=Button(frm,text="Update",bg="light green",width=12,font=('Arial',15),bd=5,command=update_details_screen)
    update_btn.place(relx=.005,rely=.66)

    trnsfer_btn=Button(frm,text="Transfer",bg="light yellow",width=12,font=('Arial',15),bd=5,command=trnsfer_details_screen)
    trnsfer_btn.place(relx=.005,rely=.76)

    history_btn=Button(frm,text="History",bg="cyan",width=12,font=('Arial',15),bd=5,command=history_details_screen)
    history_btn.place(relx=.005,rely=.86)

main_screen()
root.mainloop()



