import tkinter as tk
from tkinter import messagebox,PhotoImage
from change_password import *
from student_data_form import *
from student_details_list_view import *
from tc_data_form import *
from tc_list_view import *

#Color constants
COLOR_BACKGROUND = "#222831"
COLOR_SIDEBAR = "#393E46"
COLOR_ACCENT = "#00ccdd"
COLOR_ACCENT_HOVER = "#4c3bcf"
COLOR_TEXT = "#FFFFFF"
COLOR_BUTTON_BG = "#00CCDD"
COLOR_BUTTON_FG = "#222831"
COLOR_BUTTON_HOVER_BG = "#00ADB5"
COLOR_BUTTON_HOVER_FG = "#EEEEEE"
# Global variable to track visibility of "More" options
more_options_visible = False

def open_dashboard():
    # Main dashboard_window 
    dashboard_window = tk.Tk()
    dashboard_window.title("GASCW TC Software - Home page")
    dashboard_window.geometry("1200x800") 
    dashboard_window.state("zoomed")
    dashboard_window.configure(bg=COLOR_BACKGROUND)
    icon=PhotoImage(file=r"TC53.png")
    dashboard_window.iconphoto(True,icon)
    logo=PhotoImage(file=r"img\\image1.png")

    # Function to show the saved TCs
    def show_saved_TC():
        dashboard_window.destroy()
        status=TC_list()
        if not status:
            open_dashboard()

    # Function to create a new TC
    def create_new_TC():
        dashboard_window.destroy()
        status=TC_data_frm()
        if not status:
            open_dashboard()
    
    # Function to logout
    def logout():
        if messagebox.askokcancel("Logout", "Do you want to quit?"):
            dashboard_window.destroy()

    # Function to show student list options
    def student_data_list():
        dashboard_window.destroy()
        global more_options_visible
        more_options_visible = not more_options_visible
        status=student_list()
        if not status:
            open_dashboard()
        
    # Function to show student data form options
    def student_data_form():
        dashboard_window.destroy()
        global more_options_visible
        more_options_visible = not more_options_visible
        status=student_data()
        if not status:
            open_dashboard()
    
    # Function to call change password   
    def change_password():
        change_passwrd()
        
        
    # main content frame
    main_frame = tk.Frame(dashboard_window, bg="#ffffff")
    main_frame.grid(row=0, column=1, sticky="nsew")  # Content next to sidebar 

    # Sidebar frame (fixed width)
    sidebar_width = 250
    sidebar_frame = tk.Frame(dashboard_window, bg=COLOR_SIDEBAR, width=sidebar_width, height=800, padx=10, pady=10)
    sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=0, pady=0)

    # Sidebar content (Sidebar Menu Button that occupies full width)
    hamburger_button = tk.Button(
        sidebar_frame, text="☰", font=("Arial", 30), bg=COLOR_SIDEBAR, fg=COLOR_TEXT, 
        bd=0, command=lambda: toggle_more_options()
    )
    hamburger_button.grid(row=0, column=0, sticky="ew", pady=(0,20))  # Take up full width

    # "More" options frame (hidden by default)
    more_options_frame = tk.Frame(sidebar_frame, bg=COLOR_SIDEBAR)

    # More options (Buttons below the sidebar button)
    student_list_button = tk.Button(
        more_options_frame, text="Student List", font=("Arial", 14,"bold"), bg=COLOR_BUTTON_BG, 
        fg=COLOR_BUTTON_FG, width=20, bd=0, activebackground=COLOR_BUTTON_HOVER_BG, 
        activeforeground=COLOR_BUTTON_HOVER_FG, command=student_data_list
    )
    student_list_button.grid(row=1, column=0, pady=11, padx=20)
    
    student_data_button = tk.Button(
        more_options_frame, text="Student Data form", font=("Arial", 14,"bold"), bg=COLOR_BUTTON_BG, 
        fg=COLOR_BUTTON_FG, width=20, bd=0, activebackground=COLOR_BUTTON_HOVER_BG, 
        activeforeground=COLOR_BUTTON_HOVER_FG, command=student_data_form
    )
    student_data_button.grid(row=2, column=0, pady=11, padx=20)
    
    change_password_button = tk.Button(
        more_options_frame, text="Change Password", font=("Arial", 14,"bold"), bg=COLOR_BUTTON_BG, 
        fg=COLOR_BUTTON_FG, width=20, bd=0, activebackground=COLOR_BUTTON_HOVER_BG, 
        activeforeground=COLOR_BUTTON_HOVER_FG, command=change_password
    )
    change_password_button.grid(row=3, column=0, pady=11, padx=20)

    logout_button = tk.Button(
        more_options_frame, text="Logout", font=("Arial", 14,"bold"), bg=COLOR_BUTTON_BG, 
        fg=COLOR_BUTTON_FG, width=20, bd=0, activebackground=COLOR_BUTTON_HOVER_BG, 
        activeforeground=COLOR_BUTTON_HOVER_FG, command=logout
    )
    logout_button.grid(row=4, column=0, pady=11, padx=20)
    
    # Function to toggle visibility of the "More" options
    def toggle_more_options():
        global more_options_visible
        if more_options_visible:
            more_options_frame.grid_forget()  # Hiding the "More" options frame
        else:
            more_options_frame.grid(row=1, column=0, sticky="ew", pady=10) # Show the "More" options frame
        more_options_visible = not more_options_visible  # Toggle visibility state

    # Title for the dashboard (main content)
    dashboard_title = tk.Label(
        main_frame,image=logo,compound="left", text="Government Arts and Science College for Women, Puliakulam, Coimbatore\n\nGASCW TC Software", font=("Arial", 14, "bold"), 
        bg="#393E46", fg=COLOR_TEXT,width=1200,height=90,anchor="w",padx=10
    )
    dashboard_title.grid(row=0, column=0, columnspan=3, pady=0,sticky="w")
    
    # Button for "Saved Student TCs"
    saved_TC_button = tk.Button(
        main_frame, text="Saved TC", font=("Arial", 16,"bold"), bg=COLOR_BUTTON_BG, 
        fg=COLOR_BUTTON_FG, width=20, bd=0, activebackground=COLOR_BUTTON_HOVER_BG,height=3,
        activeforeground=COLOR_BUTTON_HOVER_FG, command=show_saved_TC
    )
    saved_TC_button.grid(row=3, column=0, pady=30,sticky="w",padx=80)

    # Button for "Create New Record"
    create_TC_button = tk.Button(
        main_frame, text="Create New TC", font=("Arial", 16,"bold"), bg=COLOR_BUTTON_BG, 
        fg=COLOR_BUTTON_FG, width=20, bd=0, activebackground=COLOR_BUTTON_HOVER_BG,height=3,
        activeforeground=COLOR_BUTTON_HOVER_FG, command=create_new_TC
    )
    create_TC_button.grid(row=1, column=0, pady=40,sticky="w",padx=80)

    # Adjusting grid configuration for resizing the dashboard_window
    dashboard_window.grid_rowconfigure(0, weight=1)
    dashboard_window.grid_columnconfigure(1, weight=1)

    # Tkinter event loop
    dashboard_window.mainloop()

if __name__ == "__main__":
    open_dashboard()