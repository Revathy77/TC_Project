from tkinter import *
from tkinter import messagebox
import pymysql

def change_passwrd():
    root = Tk()
    root.title("Change Password")
    root.geometry("1200x800")
    root.config(background="#ffffff")
    root.state("zoomed")  

    global root_window
    root_window = root

    def on_closing():
        root_window.destroy()
            

    def change_pwd():
        db = pymysql.connect(host="localhost", user="root", password="admin", database="gascw_tc1")
        mycursor = db.cursor()
        mycursor.execute("SELECT password FROM user WHERE username = 'admin'")
        rows = mycursor.fetchone()
        if rows is None:
            messagebox.showerror("Failure",  " Something went wrong")
            return
        server_pwd = rows[0]
        db.commit()
        if CurrentPwd.get() == server_pwd:
            if NewPwd.get() == NewPwd2.get():
                try:
                    mycursor.execute("UPDATE user SET password = '"+str(NewPwd.get())+"' WHERE username = 'admin'")
                    db.commit()
                    messagebox.showinfo("Success",  "Password changed")
                except Exception as e:
                    messagebox.showerror("Failure",  str(e))
                    db.rollback()
                    db.close()
            else:
                messagebox.showerror("Failure",  "New Passwords didn't match")
        else:
            messagebox.showerror("Failure",  " Something went wrong")
        CurrentPwd.delete(0, END)
        NewPwd.delete(0, END)
        NewPwd2.delete(0, END)
        root_window.destroy()
        

    root_window.protocol("WM_DELETE_WINDOW", on_closing)

    # Header
    header = Frame(root, bg="#00ccdd", bd=0)
    header.pack(fill='x', pady=10)  # Making header span full width

    # Heading label
    nsec = Label(header, text="GASCW TC Software", font=("Arial", 14, "bold"), bg="#00ccdd", fg="#0f0f0f",height=2,width=60)
    nsec.pack(side="left", padx=320)

    # Profile frame (title bar and close button)
    frame2 = Frame(root, bg="#393E46",height=2)
    frame2.pack(fill='x', pady=0,padx=8)

    change_password_text = Label(frame2, text="Change Password", font=("Arial", 16,"bold"), fg="#fff", bg="#393E46")
    change_password_text.pack(side="left", padx=0)

    # Close Button at the right corner
    close = Button(frame2, text="Back", bd=3, command=on_closing, font=("Arial", 16), bg="#fff", fg="#000")
    close.pack(side="right",padx=5)

    # Panel for the content (form and button)
    panel = Frame(root, bg="#fff", bd=0)
    panel.pack(fill='both',expand=True)

    # Panel elements
    searchBy = Label(panel, text="Current Password", font=("Arial", 16), bg="#fff", fg="#222",width=14)
    searchBy.grid(row=0, column=0,sticky="w", padx=52)

    CurrentPwd = Entry(panel, font=("Arial", 18), show='*', bd=0, bg="#e0e0e0", fg="#000",width=28)
    CurrentPwd.grid(row=0, column=1, padx=10, pady=5)  

    searchBy = Label(panel, text="New Password", font=("Arial", 16), bg="#fff", fg="#222",width=12)
    searchBy.grid(row=1, column=0,sticky="w", padx=50)

    NewPwd = Entry(panel, font=("Arial", 18), show='*', bd=0, bg="#e0e0e0", fg="#000",width=28)
    NewPwd.grid(row=1, column=1, padx=10, pady=5, sticky="w")  

    searchBy = Label(panel, text="Retype New Password", font=("Arial", 16), bg="#fff", fg="#222",width=18)
    searchBy.grid(row=2, column=0, sticky="w", padx=50)

    NewPwd2 = Entry(panel, font=("Arial", 18), show='*', bd=0, bg="#e0e0e0", fg="#000",width=28)
    NewPwd2.grid(row=2, column=1, padx=10, pady=5, sticky="w")  
    
    # "Change Password" Button 
    searchBtn = Button(panel, text="Change Password", command=change_pwd, font=("Arial", 16, "bold"), bd=0, bg="#00ccdd", fg="#0f0f0f",width=20)
    searchBtn.grid(row=3, column=1, pady=50, padx=10)  

    # Configuring grid to make entries expand correctly within their cells
    panel.grid_rowconfigure(0, weight=1)
    panel.grid_rowconfigure(1, weight=1)
    panel.grid_rowconfigure(2, weight=1)

    root.mainloop()
    
if __name__ == "__main__":
    change_passwrd()