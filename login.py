import tkinter as tk #For GUI
from tkinter import messagebox,PhotoImage
import pymysql
from pymysql import MySQLError
from dashboard import *
from student_data_form import *
from student_details_list_view import *
from tc_data_form import *
from tc_list_view import *
from preview import *
            
def login_page():
    # Function to validate login using MySQL
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()

        try:
            # Establish a connection to MySQL
            connection = pymysql.connect(
                host='localhost',  # MySQL host
                database='gascw_tc1',  # database name
                user='root',  # MySQL username
                password='admin'  # MySQL password
            )

            if connection.open:
                cursor = connection.cursor()

                # Query to check if the user exists with the provided username and password
                query = "SELECT * FROM user WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))

                # Fetch one record
                user = cursor.fetchone()

                if user:
                    login_window.destroy()
                    open_dashboard()
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password")
        
        except MySQLError as e:
            messagebox.showerror("Error", f"Error : {e}")
        except Exception as e:
            messagebox.showerror("Exception", f"Exception : {e}")
        
        finally:
            if connection.open:
                cursor.close()
                connection.close()
        
    # Creating main login_window
    login_window = tk.Tk()
    login_window.title("GASCW TC Software - Login")
    icon=PhotoImage(file=r"img\\TC53.png")
    login_window.iconphoto(True,icon)
    #login_window size and background color
    login_window.geometry("1200x800")
    login_window.state("zoomed")
    login_window.configure(bg="#ffffff")  

    # Creating a frame for the login content
    frame = tk.Frame(login_window, bg="#ffffff", padx=50, pady=50, bd=0,height=140,width=620, relief="groove")
    frame.place(relx=0.48, rely=0.54, anchor="center")
    logo=PhotoImage(file=r"img\\image1.png")

    # HEADER Label
    Header_label = tk.Label(
        login_window,image=logo,compound="left", text="  Government Arts and Science College for Women, Puliakulam, Coimbatore", font=("Arial", 18,"bold"), 
        bg="#4c3bcf", fg="#ffffff",height=67
    )
    Header_label.pack(side="top", pady=17,padx=8,fill="x")

    # Title Label
    title_label = tk.Label(
        frame, text="Login", font=("Arial", 25, "bold"), bg="#ffffff", fg="#4c3bcf"
    )
    title_label.grid(row=0, column=0, columnspan=3, pady=(18, 27),sticky="w", padx=(9, 20))

    # Username field
    username_label = tk.Label(
        frame, text="Username", font=("Arial", 14,"bold"), bg="#ffffff", fg="#4c3bcf"
    )
    username_label.grid(row=1, column=0, pady=(22, 25), sticky="w",padx=(10,20))
    username_entry = tk.Entry(
        frame, width=27, font=("Arial", 12,"bold"), bd=2, bg="#eeeeee", fg="#222831", relief="ridge",highlightbackground="#eeeeee",highlightcolor="#ffffff"
    )
    username_entry.grid(row=1, column=1, pady=(25, 25), padx=(20, 10))

    # Password field
    password_label = tk.Label(
        frame, text="Password", font=("Arial", 14,"bold"), bg="#ffffff", fg="#4c3bcf"
    )
    password_label.grid(row=2, column=0, pady=(27, 25), sticky="w",padx=(10,20))
    password_entry = tk.Entry(
        frame, width=27, font=("Arial", 12,"bold"), bd=2, bg="#eeeeee", fg="#222831",  show="*",relief="ridge",highlightbackground="#eeeeee",highlightcolor="#ffffff"
    )
    password_entry.grid(row=2, column=1, pady=(30, 25), padx=(20, 10))

    # Login button
    login_button = tk.Button(
        frame, text="Login", font=("Arial", 14, "bold"), bg="#4c3bcf", fg="#f5f5f5", 
        bd=0, width=8, activebackground="#eeeeee", activeforeground="#4c3bcf", relief="sunken",
        command=validate_login
    )
    login_button.grid(row=4, column=1, columnspan=3, pady=(39, 10))


    #Tkinter event loop
    login_window.mainloop()
    
    
if __name__ == "__main__":
    login_page()