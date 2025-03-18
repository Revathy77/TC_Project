import tkinter as tk
from tkinter import ttk, messagebox, filedialog,PhotoImage
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import pymysql
from datetime import datetime
import io

status = False

# MySQL Database Connection
def connect_to_database():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="admin",
            database="gascw_tc1"
        )
        return connection
    except pymysql.MySQLError as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None
    except Exception as e:
            messagebox.showerror("Exception", f"Error connecting to MySQL : {e}")

# Main Application Window
class student_data_form:
    def __init__(self, root,admission_num=None):
        self.root = root
        self.root.title(" Student Data Form ")
        icon=PhotoImage(file=r"img\\TC53.png")
        self.root.iconphoto(True,icon)
        self.root.geometry("1200x700")
        self.root.configure(bg="#00ccdd")
        self.root.state("zoomed")

        # Title Label
        title_label = tk.Label(root, text="Student Data Form", font=("Arial", 18, "bold"), bg="#393E46", fg="#ffffff")
        title_label.pack(fill=tk.X, pady=6)

        # Main Frame with Vertical Scrollbar
        main_frame = tk.Frame(root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg="white")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.content_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Student Personal Information Frame
        personal_info_frame = tk.LabelFrame(self.content_frame, text="Student Personal Information", font=("Arial", 14, "bold"), bg="white", fg="#00adb5")
        personal_info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Fields for Personal Information
        fields = [
            ("Admission No.", "admission_num"),
            ("Name", "name"),
            ("மாணவியர் பெயர்","name_in_tamil"),
            ("Father or Mother Name", "father_or_mother_name"),
            ("Nationality, Religion, Caste", "nationality_religion_caste"),
            ("Community", "community"),
            ("Sex", "gender"),
            ("Date of Birth", "dob"),
            ("Date of Birth in words", "dob_in_words"),
            ("First Language","first_language"),
            
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields):
            tk.Label(personal_info_frame, text=label, font=("Arial", 12,"bold"), bg="white", fg="#4c3bcf").grid(row=i, column=0, padx=30, pady=5, sticky="w")
            if field == "dob":
                entry = DateEntry(personal_info_frame,width=12,background="darkblue",foreground="white",borderwidth=2 ,font=("Arial", 12), date_pattern="dd-mm-yyyy",showweeknumbers=False)
            elif field == "nationality_religion_caste" or field == "community" or field == "gender":
                entry = ttk.Combobox(personal_info_frame, font=("Arial", 12), width=27)
                if field == "community":
                    entry["values"] = ["REFER COMMUNITY CERTIFICATE"]
                elif field == "nationality_religion_caste":
                    entry["values"] = ["INDIAN"]
                else :
                    entry["values"] = ["FEMALE"]
            else:
                entry = tk.Entry(personal_info_frame, font=("Nirmala UI", 12), width=58, border=True)
            entry.grid(row=i, column=1, padx=20, pady=18, sticky="ew")
            self.entries[field] = entry

        #Adding search icon button next to admission_num field
            if field == "admission_num":
                search_icon = Image.open(r"img\\search.png")
                search_icon = search_icon.resize((20, 20), Image.Resampling.LANCZOS)
                search_icon = ImageTk.PhotoImage(search_icon)
                search_button = tk.Button(personal_info_frame, image=search_icon, command=self.search_student)
                search_button.image = search_icon  # Keeping reference
                search_button.grid(row=i, column=2, padx=10, pady=10, sticky="w")   
                
        # Photo Field
        self.photo_label = tk.Label(personal_info_frame, bg="white", width=12, height=5, relief=tk.SUNKEN)
        self.photo_label.grid(row=0, column=3, rowspan=2, padx=10, pady=10, sticky="nsew")

        upload_button = tk.Button(personal_info_frame, text="Upload Photo", font=("Arial", 11,"bold"), bg="#222831", fg="#ffffff", command=self.upload_photo)
        upload_button.grid(row=2, column=3, padx=10, pady=10, sticky="ew")

        # Adding scanner icon button next to Upload Photo button
        scanner_icon = Image.open(r"img\\scan.png")
        scanner_icon = scanner_icon.resize((20, 20), Image.Resampling.LANCZOS)
        scanner_icon = ImageTk.PhotoImage(scanner_icon)
        scanner_button = tk.Button(personal_info_frame, image=scanner_icon, command=self.scan_photo)
        scanner_button.image = scanner_icon  # Keeping reference
        scanner_button.grid(row=2, column=4, padx=10, pady=10, sticky="ew")

        # Academic information Frame
        academic_info_frame = tk.LabelFrame(self.content_frame, text="Academic Information", font=("Arial", 14, "bold"), bg="white", fg="#00adb5")
        academic_info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        academic_info_fields = [
            ("Roll No.", "roll_no"),
            ("Date of Admission", "doa"),
            ("Date of Admission in Words", "doa_in_words"),
            ("Academic Year", "academic_year"),
            ("Class Admitted", "class_admitted"),
            ("Course offered Main and Ancillary", "course_offered_main_and_ancillary"),
            ("Language under part 1", "language_under_part_1"),
            ("Medium of Instruction", "medium_of_instruction")
        ]

        self.academic_entries = {}
        for i, (label, field) in enumerate(academic_info_fields):
            tk.Label(academic_info_frame, text=label, font=("Arial", 12,"bold"), bg="white", fg="#4c3bcf").grid(row=i, column=0, padx=29, pady=10, sticky="w")
            if field == "doa":
                entry = DateEntry(academic_info_frame,width=12,background="darkblue",foreground="white",borderwidth=2 ,font=("Arial", 12), date_pattern="dd-mm-yyyy",showweeknumbers=False)
            elif field == "class_admitted" or field == "medium_of_instruction":
                entry = ttk.Combobox(academic_info_frame, font=("Arial", 12), width=27)
                if field == "class_admitted":
                    entry["values"] = ["B.A. TAMIL", "B.A. ENGLISH ", "B.Sc MATHEMATICS", "B.Sc COMPUTER SCIENCE", "B.Com. COMMERCE"]
                else:
                    entry["values"] = ["TAMIL", "ENGLISH"]
            else:
                entry = tk.Entry(academic_info_frame, font=("Arial", 12), width=75)
            entry.grid(row=i, column=1, padx=10, pady=25, sticky="ew")
            self.academic_entries[field] = entry

        # Bottom Frame with Buttons
        button_frame = tk.Frame(root, bg="#00ccdd")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        buttons = [
            ("Add New", self.add_new_record),
            ("Save", self.save_record),
            ("Delete", self.delete_record),
            ("Next", self.next_record),
            ("Previous", self.previous_record),
            ("First", self.first_record),
            ("Last", self.last_record),
            ("Clear", self.clear_form),
            ("Back", self.back_to_dashboard)
        ]

        for i, (btn_text, cmd) in enumerate(buttons):
            row = 0 if i < 9 else 1
            col = i % 9
            button = tk.Button(button_frame, text=btn_text, font=("Arial", 11,"bold"), bg="white", fg="#222831", width=9, command=cmd)
            button.grid(row=row, column=col, padx=14, pady=5)
        
        # Initializing variables
        self.current_admission_num = admission_num
        self.photo_data = None
        if self.current_admission_num:
            self.load_record(self.current_admission_num)
        
        def on_close():
            self.root.destroy()
            global status
            status= True
            return status
        root.protocol("WM_DELETE_WINDOW",on_close)
        
    def search_student(self):
        admission_num = self.entries["admission_num"].get()
        if not admission_num:
            messagebox.showwarning("Input Error", "Please enter a Admission No. to search.",parent=self.root)
            return

        try:
            connection = connect_to_database()
            if connection:
                cursor = connection.cursor()

                # Fetch student details
                cursor.execute("SELECT * FROM student_personal_info WHERE admission_num = %s", (admission_num,))
                student = cursor.fetchone()

                if student:
                    # Populate personal information fields
                    self.entries["name"].delete(0, tk.END)
                    self.entries["name"].insert(0, student[1])
                    self.entries["father_or_mother_name"].delete(0, tk.END)
                    self.entries["father_or_mother_name"].insert(0, student[3])
                    self.entries["nationality_religion_caste"].delete(0, tk.END)
                    self.entries["nationality_religion_caste"].set(student[4])
                    self.entries["community"].delete(0, tk.END)
                    self.entries["community"].set(student[5])
                    self.entries["gender"].delete(0, tk.END)
                    self.entries["gender"].set(student[6])
                    self.entries["dob"].set_date(student[7].strftime("%d-%m-%Y"))
                    self.entries["dob_in_words"].delete(0, tk.END)
                    self.entries["dob_in_words"].insert(0, student[8])
                    self.entries["first_language"].delete(0, tk.END)
                    self.entries["first_language"].insert(0, student[9])
                    self.entries["name_in_tamil"].delete(0, tk.END)
                    self.entries["name_in_tamil"].insert(0, student[10])
                    # Display photo
                    self.photo_data = student[2]
                    if self.photo_data:
                        image = Image.open(io.BytesIO(self.photo_data))
                        image = image.resize((82, 90), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        self.photo_label.config(image=photo)
                        self.photo_label.image = photo

                    # Fetch academic details
                    cursor.execute("SELECT * FROM academic_info WHERE admission_num = %s", (admission_num,))
                    academic_info = cursor.fetchone()
                    if academic_info:
                        self.academic_entries["roll_no"].delete(0,tk.END)
                        self.academic_entries["roll_no"].insert(0, str(academic_info[1]))
                        self.academic_entries["doa"].set_date(academic_info[2].strftime("%d-%m-%Y"))
                        self.academic_entries["doa_in_words"].delete(0, tk.END)
                        self.academic_entries["doa_in_words"].insert(0, str(academic_info[3]))
                        self.academic_entries["academic_year"].delete(0, tk.END)
                        self.academic_entries["academic_year"].insert(0, str(academic_info[4]))
                        self.academic_entries["class_admitted"].set(academic_info[5])
                        self.academic_entries["course_offered_main_and_ancillary"].delete(0, tk.END)
                        self.academic_entries["course_offered_main_and_ancillary"].insert(0, str(academic_info[6]))
                        self.academic_entries["language_under_part_1"].delete(0, tk.END)
                        self.academic_entries["language_under_part_1"].insert(0, str(academic_info[7]))
                        self.academic_entries["medium_of_instruction"].set(academic_info[8])
                    self.current_admission_num = admission_num
                else:
                    messagebox.showinfo("Not Found", "No student found with the Admission No.",parent=self.root)

                cursor.close()
                connection.close()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch student details: {e}",parent=self.root)
        
    
    # Function to Upload and Display Photo
    def upload_photo(self):
        file_path = filedialog.askopenfilename(
            title="Select a Photo",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")],parent=self.root
        )
        if file_path:
            try:
                # Open and resize the image
                image = Image.open(file_path)
                image = image.resize((82, 90), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                # Convert image to binary data
                with open(file_path, "rb") as file:
                    self.photo_data = file.read()

                # Display the image in the label
                self.photo_label.config(image=photo)
                self.photo_label.image = photo  # Keeping reference to avoid garbage collection
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}",parent=self.root)
                
    # Function for Scanner Input
    def scan_photo(self):
        pass

    # Function to Add New Record (Clear Form for New Entry)
    def add_new_record(self):
        self.clear_form()

    # Function to Load Record
    def load_record(self, admission_num):
        try:
            self.current_admission_num=admission_num
            connection = connect_to_database()
            if connection:
                cursor = connection.cursor()

                # Fetch student data
                self.clear_form()
                cursor.execute("SELECT * FROM student_personal_info WHERE admission_num = %s", (admission_num,))
                student_data = cursor.fetchone()

                # Fetch academic_info data
                cursor.execute("SELECT * FROM academic_info WHERE admission_num = %s", (admission_num,))
                academic_info_data = cursor.fetchone()

                if student_data and academic_info_data:
                    # Populate student fields
                    self.entries["admission_num"].insert(0, student_data[0])
                    self.entries["name"].insert(0, student_data[1])
                    self.entries["father_or_mother_name"].insert(0, student_data[3])
                    self.entries["nationality_religion_caste"].set(student_data[4])
                    self.entries["community"].set(student_data[5])
                    self.entries["gender"].set(student_data[6])
                    self.entries["dob"].set_date(student_data[7].strftime("%d-%m-%Y"))
                    self.entries["dob_in_words"].insert(0, student_data[8])
                    self.entries["first_language"].insert(0, student_data[9])
                    self.entries["name_in_tamil"].insert(0, student_data[10])
                    self.photo_data = student_data[2]  # Store photo data
                    if self.photo_data:
                        image = Image.open(io.BytesIO(self.photo_data))
                        image = image.resize((82, 90), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        self.photo_label.config(image=photo)
                        self.photo_label.image = photo  # Keeping reference

                    # Populate academic_info fields
                    self.academic_entries["roll_no"].insert(0, academic_info_data[1])
                    self.academic_entries["doa"].set_date(academic_info_data[2].strftime("%d-%m-%Y"))
                    self.academic_entries["doa_in_words"].insert(0, academic_info_data[3])
                    self.academic_entries["academic_year"].insert(0, academic_info_data[4])
                    self.academic_entries["class_admitted"].set(academic_info_data[5])
                    self.academic_entries["course_offered_main_and_ancillary"].insert(0, academic_info_data[6])
                    self.academic_entries["language_under_part_1"].insert(0, academic_info_data[7])
                    self.academic_entries["medium_of_instruction"].set(academic_info_data[8])
                    
                cursor.close()
                connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load record: {e}",parent=self.root)

    # Function to Save Record (Add or Update)
    def save_record(self):
        try:
            connection = connect_to_database()
            if connection:
                cursor = connection.cursor()

                # Get student data
                admission_num = self.entries["admission_num"].get()
                name = self.entries["name"].get()
                father_or_mother_name = self.entries["father_or_mother_name"].get()
                nationality_religion_caste = self.entries["nationality_religion_caste"].get()
                community = self.entries["community"].get()
                gender = self.entries["gender"].get()
                dob = datetime.strptime(self.entries["dob"].get(), "%d-%m-%Y").strftime("%Y-%m-%d")
                dob_in_words = self.entries["dob_in_words"].get()
                first_language = self.entries["first_language"].get()
                name_in_tamil = self.entries["name_in_tamil"].get()
                
                # Check if admission_num already exists
                cursor.execute("SELECT * FROM student_personal_info WHERE admission_num = %s", (admission_num,))
                existing_student = cursor.fetchone()

                if existing_student:
                    # Updating existing student record
                    student_query = """
                    UPDATE student_personal_info
                    SET name = %s, photo = %s, father_or_mother_name = %s, nationality_religion_caste = %s, community = %s, gender = %s,dob = %s,dob_in_words = %s,first_language = %s,name_in_tamil = %s
                    WHERE admission_num = %s
                    """
                    student_data = (name,self.photo_data,father_or_mother_name, nationality_religion_caste, community, gender,dob,dob_in_words,first_language,name_in_tamil,admission_num)
                    cursor.execute(student_query, student_data)

                    # Updating academic_info record
                    academic_info_query = """
                    UPDATE academic_info
                    SET roll_no = %s, doa = %s, doa_in_words = %s, academic_year = %s,class_admitted = %s, course_offered_main_and_ancillary = %s, language_under_part_1 =%s, medium_of_instruction = %s
                    WHERE admission_num = %s
                    """
                    academic_info_data = (
                        self.academic_entries["roll_no"].get(),
                        datetime.strptime(self.academic_entries["doa"].get(), "%d-%m-%Y").strftime("%Y-%m-%d"),
                        self.academic_entries["doa_in_words"].get(),
                        self.academic_entries["academic_year"].get(),
                        self.academic_entries["class_admitted"].get(),
                        self.academic_entries["course_offered_main_and_ancillary"].get(),
                        self.academic_entries["language_under_part_1"].get(),
                        self.academic_entries["medium_of_instruction"].get(),
                        admission_num                                           
                                        )
                    cursor.execute(academic_info_query, academic_info_data)
                else:
                    # Insert new student record
                    student_query = """
                    INSERT INTO student_personal_info (admission_num, name, photo,father_or_mother_name,nationality_religion_caste,community,gender,dob,dob_in_words,first_language,name_in_tamil)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)
                    """
                    student_data = (admission_num, name, self.photo_data,father_or_mother_name, nationality_religion_caste, community, gender, dob,dob_in_words,first_language,name_in_tamil)
                    cursor.execute(student_query, student_data)

                    # Insert new academic_info record
                    academic_info_query = """
                    INSERT INTO academic_info (admission_num, roll_no, doa, doa_in_words, academic_year, class_admitted, course_offered_main_and_ancillary , language_under_part_1,medium_of_instruction)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    academic_info_data = (
                        admission_num,
                        self.academic_entries["roll_no"].get(),
                        datetime.strptime(self.academic_entries["doa"].get(), "%d-%m-%Y").strftime("%Y-%m-%d"),
                        self.academic_entries["doa_in_words"].get(),
                        self.academic_entries["academic_year"].get(),
                        self.academic_entries["class_admitted"].get(),
                        self.academic_entries["course_offered_main_and_ancillary"].get(),
                        self.academic_entries["language_under_part_1"].get(),
                        self.academic_entries["medium_of_instruction"].get(),
                                        )
                    cursor.execute(academic_info_query, academic_info_data)

                connection.commit()
                messagebox.showinfo("Success", "Record saved successfully!",parent=self.root)
                cursor.close()
                connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save record: {e}",parent=self.root)

    # Function to Delete Record
    def delete_record(self):
        try:
            admission_num = self.entries["admission_num"].get()
            if admission_num:
                connection = connect_to_database()
                if connection:
                    cursor = connection.cursor()

                    # Delete from academic_info table first (due to foreign key constraint)
                    cursor.execute("DELETE FROM academic_info WHERE admission_num = %s", (admission_num,))

                    # Delete from student_personal_info table
                    cursor.execute("DELETE FROM student_personal_info WHERE admission_num = %s", (admission_num,))

                    connection.commit()
                    messagebox.showinfo("Success", "Record deleted successfully!",parent=self.root)
                    self.clear_form()
                    cursor.close()
                    connection.close()
            else:
                messagebox.showwarning("Warning", "No record selected to delete!",parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record: {e}",parent=self.root)

    # Function to Clear Form
    def clear_form(self):
        for entry in self.entries.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, DateEntry):
                entry.set_date("")
            elif isinstance(entry, ttk.Combobox):
                entry.set("")
        for entry in self.academic_entries.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, DateEntry):
                entry.set_date("")
            elif isinstance(entry, ttk.Combobox):
                entry.set("")
        self.photo_label.config(image=None)
        self.photo_label.image = None
        self.photo_data = None
        self.current_admission_num = None
        
    def next_record(self):
        try:
            self.current_admission_num = self.entries["admission_num"].get()
            if self.current_admission_num is None:
                messagebox.showinfo("Info", "No record is currently loaded.",parent=self.root)
                return

            connection = connect_to_database()
            if connection:
                cursor = connection.cursor()

                # Fetch the next admission_num
                cursor.execute("SELECT admission_num FROM student_personal_info WHERE admission_num > %s ORDER BY admission_num LIMIT 1", (self.current_admission_num,))
                next_student = cursor.fetchone()

                if next_student:
                    self.current_admission_num = next_student[0]  # Updating current_admission_num
                    self.load_record(self.current_admission_num)  # Loading next record
                else:
                    messagebox.showinfo("Info", "No more records!",parent=self.root)

                cursor.close()
                connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load next record: {e}",parent=self.root)
            
    def previous_record(self):
        try:
            self.current_admission_num = self.entries["admission_num"].get()
            if self.current_admission_num is None:
                messagebox.showinfo("Info", "No record is currently loaded.",parent=self.root)
                return

            connection = connect_to_database()
            if connection:
                cursor = connection.cursor()

                # Fetch the previous admission_num
                cursor.execute("SELECT admission_num FROM student_personal_info WHERE admission_num < %s ORDER BY admission_num DESC LIMIT 1", (self.current_admission_num,))
                previous_student = cursor.fetchone()

                if previous_student:
                    self.current_admission_num = previous_student[0]  # Updating current_admission_num
                    self.load_record(self.current_admission_num)  # Loading previous record
                else:
                    messagebox.showinfo("Info", "No previous records!",parent=self.root)

                cursor.close()
                connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load previous record: {e}",parent=self.root)
            
    def first_record(self):
        try:
            connection = connect_to_database()
            if connection:
                cursor = connection.cursor()

                # Fetch the first admission_num
                cursor.execute("SELECT admission_num FROM student_personal_info ORDER BY admission_num LIMIT 1")
                first_student = cursor.fetchone()

                if first_student:
                    self.current_admission_num = first_student[0]  # Updating current_admission_num
                    self.load_record(self.current_admission_num)  # Loading first record
                else:
                    messagebox.showinfo("Info", "No records found!")

                cursor.close()
                connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load first record: {e}",parent=self.root)
            
    def last_record(self):
        try:
            connection = connect_to_database()
            if connection:
                cursor = connection.cursor()

                # Fetch the last admission_num
                cursor.execute("SELECT admission_num FROM student_personal_info ORDER BY admission_num DESC LIMIT 1")
                last_student = cursor.fetchone()

                if last_student:
                    self.current_admission_num = last_student[0]  # Updating current_admission_num
                    self.load_record(self.current_admission_num)  # Loading last record
                else:
                    messagebox.showinfo("Info", "No records found!",parent=self.root)

                cursor.close()
                connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load last record: {e}",parent=self.root)
            
    def back_to_dashboard(self):
        self.root.destroy() # Close the current window
    
def student_data():
    root = tk.Tk()
    app = student_data_form(root)
    root.mainloop()
    return status

# Running the Application
if __name__ == "__main__":  
    student_data()