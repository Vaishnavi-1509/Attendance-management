import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
import speech_recognition as sr
import mysql.connector
from tkinter import PhotoImage
from datetime import datetime


# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="example"
)

# Create a Tkinter main window for student attendance
main_window = tk.Tk()
main_window.title("Student Attendance")
bg = PhotoImage( file= "C:\gvaishnavi\BG1.png")
# Show image using label
background_label = tk.Label(main_window, image=bg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


headingFrame1 = tk.Frame(main_window, bg="white", bd=5)
headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
print("Image width:", bg.width())
print("Image height:", bg.height())
# Create a label for the heading
headingLabel = tk.Label(headingFrame1, text="WELCOME TO THE PORTAL", bg='grey', fg='black',
                        font=('Courier bold', 15))
headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
# Function to enroll a student with voice input for name, student ID, and voiceprint
def add_sidebar(main_window):
    sidebar = tk.Frame(main_window, bg="#192529", width=10,height=967)
    sidebar.pack(fill="y", side="left")

    instructions = """
    \n
    I N S T R U C T I O N S:\n
    
    Click on the buttons\n
    to perform various tasks:\n\n
    ENROLLMENT: \n
    Enroll a student with voice input\n
    for name,student ID, \n
    and voiceprint.\n
    
    TAKE ATTENDANCE: \n
    Record voice for attendance\n 
    by subject.\n
    
    DISPLAY ENROLLED STUDENTS: \n
    View the enrolled students.\n
    
    DISPLAY ATTENDANCE: \n
    Display student attendance.\n
    
    DISPLAY ATTENDANCE CHART:\n 
    Visualize attendance in \n 
    chart form.
    """

    sidebar_label = tk.Label(sidebar, text=instructions, bg="#2b3e45",fg="white", justify="left", font=('Arial', 11, 'italic','bold'))
    sidebar_label.pack()
add_sidebar(main_window)
def enroll_student():
    def record_and_store_voice():
        with sr.Microphone() as source:
            print("Please record your voice for enrollment.")
            audio = recognizer.listen(source)
            return audio.frame_data

    def save_enrollment_data():
        global student_name, student_id
        audio_data = record_and_store_voice()

        cursor = connection.cursor()

        # Insert the student ID, name, and audio data into the 'students' table
        insert_query = "INSERT INTO students (student_id, name, voiceprint) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (student_id, student_name, audio_data))
        connection.commit()

        cursor.close()
        print(f"{student_name} with student ID {student_id} has been enrolled with audio data.")

    enrollment_window = tk.Toplevel(main_window)
    enrollment_window.title("Enroll a Student")

    def get_name():
        global student_name
        with sr.Microphone() as source:
            print("Please say the student's name:")
            name_audio = recognizer.listen(source)

        student_name = recognizer.recognize_google(name_audio)
        name_label.config(text=f"Name: {student_name}")

    def get_id():
        global student_id
        with sr.Microphone() as source:
            print("Please say the student's ID:")
            id_audio = recognizer.listen(source)

        student_id = recognizer.recognize_google(id_audio)
        id_label.config(text=f"Student ID: {student_id}")

    name_label = ttk.Label(enrollment_window, text="Name: ")
    name_label.pack(pady=5)

    id_label = ttk.Label(enrollment_window, text="Student ID: ")
    id_label.pack(pady=5)

    name_button = ttk.Button(enrollment_window, text="Get Name", command=get_name)
    name_button.pack(pady=5)

    id_button = ttk.Button(enrollment_window, text="Get Student ID", command=get_id)
    id_button.pack(pady=5)

    record_button = ttk.Button(enrollment_window, text="Record Enrollment Voice", command=save_enrollment_data)
    record_button.pack(pady=10)
    # Function to take attendance


# Function to take attendance for a specific subject
def take_attendance():
    def record_and_store_voice():
        with sr.Microphone() as source:
            print("Please record your voice for attendance.")
            audio = recognizer.listen(source)
            return audio.frame_data

    def save_attendance_data(subject):
        global student_id
        if student_id:
            audio_data = record_and_store_voice()
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor = connection.cursor()

            # Insert the student ID and audio data into the subject-specific attendance table
            insert_query = f"INSERT INTO {subject}_attendance (student_id, voicesample ,attendance_date) VALUES (%s, %s,%s)"
            print(insert_query)
            cursor.execute(insert_query, (student_id, audio_data,current_date))
            connection.commit()

            cursor.close()
            print(f"Student ID {student_id} has been given attendance for {subject} on {current_date} with audio data.")
        else:
            print("Please get the student's ID first.")

    attendance_window = tk.Toplevel(main_window)
    attendance_window.title("Take attendance")

    def get_id():
        global student_id
        with sr.Microphone() as source:
            print("Please say the student's ID:")
            id_audio = recognizer.listen(source)

        student_id = recognizer.recognize_google(id_audio)
        id_label.config(text=f"Student ID: {student_id}")

    id_label = ttk.Label(attendance_window, text="Student ID: ")
    id_label.pack(pady=5)

    id_button = ttk.Button(attendance_window, text="Get Student ID", command=get_id)
    id_button.pack(pady=5)

    subject_label = ttk.Label(attendance_window, text="Select Subject:")
    subject_label.pack(pady=5)

    subject_var = tk.StringVar()
    subject_dropdown = ttk.Combobox(attendance_window, textvariable=subject_var, values=["analog_electronics", "data_structures", "electrical_machines","electrical_network_lab","maths","power_systems","python_programming"])  # Add more subjects as needed
    subject_dropdown.pack(pady=5)

    record_button = ttk.Button(attendance_window, text="Record Attendance Voice", command=lambda: save_attendance_data(subject_var.get()))
    record_button.pack(pady=10)

# Function to display the students' table from the database
def display_students():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    students_data = cursor.fetchall()
    cursor.close()
    style = ttk.Style()
    style.configure("Treeview", borderwidth=2)  # Set the borderwidth to make it thicker
    style.configure("Treeview.Heading", font=("Helvetica bold", 12))  # Customize the column headin
    students_window = tk.Toplevel(main_window)
    students_window.title("Students Table")

    tree = ttk.Treeview(students_window, columns=("Student ID", "Name"))
    tree.heading("#1", text="Student ID")
    tree.heading("#2", text="Name")

    tree.column("#1", width=100)
    tree.column("#2", width=200)

    for student in students_data:
        tree.insert("", "end", values=(student[1], student[2]))

    tree.pack()
def display_attendance():
    subject_selection_window = tk.Toplevel(main_window,background="#2b3e44")
    subject_selection_window.geometry("500x500")
    subject_selection_window.title("Select Subject for Attendance")
    subject_label = ttk.Label(subject_selection_window, text="Select a subject:", font=('Arial', 20),background="#2b3e45")
    subject_label.pack(pady=5)

    subjects = ["Electrical Machines", "Power Systems", "Python Programming", "Maths", "Analog Electronics", "Data Structures", "Electrical Network Lab"]

    subject_var = tk.StringVar(value=subjects[0])
    subject_dropdown = ttk.Combobox(subject_selection_window, textvariable=subject_var, values=subjects,font=('Arial',10),background="#2b3e45")
    subject_dropdown.pack(pady=5)

    select_button = tk.Button(subject_selection_window, text="Select",font=('Arial 15'),background="#2b3e45",fg='white', command=lambda: display_selected_attendance(subject_var.get(), subject_selection_window))
    select_button.pack(pady=10)

def display_selected_attendance(subject, subject_selection_window):
    subject_selection_window.destroy()  # Close the subject selection window
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {subject.lower().replace(' ', '_')}_attendance")
    attendance_data = cursor.fetchall()
    cursor.close()

    attendance_window = tk.Toplevel(main_window)
    attendance_window.title(f"{subject} Attendance")

    tree = ttk.Treeview(attendance_window, columns=("Student ID", "attendance_date"))
    tree.heading("#1", text="Student ID")
    tree.heading("#2", text="attendance_date")

    for attendance in attendance_data:
        tree.insert("", "end", values=(attendance[1], attendance[3]))  # Adjust column indices as needed

    tree.pack()
def display_attendance_chart():
    update_attendance_chart()

# Define the function to update and display the attendance chart
def update_attendance_chart():
    # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="example"
    )

    # List of subjects
    subjects = ["analog_electronics", "data_structures", "electrical_machines","maths","electrical_network_lab","power_systems","python_programming","electrical_machines"]  # Add more subjects

    # Lists to hold all attendance data
    all_student_ids = []
    all_attendance_counts = []

    for subject in subjects:
        cursor = connection.cursor()
        cursor.execute(f"SELECT student_id, COUNT(*) FROM {subject}_attendance GROUP BY student_id")
        attendance_data = cursor.fetchall()
        cursor.close()

        # Extract student IDs and their attendance counts for each subject
        student_ids = [data[0] for data in attendance_data]
        attendance_counts = [data[1] for data in attendance_data]

        all_student_ids.extend(student_ids)
        all_attendance_counts.extend(attendance_counts)

    # Create a new window for the consolidated attendance chart
    chart_window = tk.Toplevel(main_window)
    chart_window.title('Consolidated Attendance Chart')

    # Create a figure and plot the consolidated bar chart for all students' attendance
    fig, ax = plt.subplots()
    ax.bar(all_student_ids, all_attendance_counts)
    ax.set_xlabel('Student IDs')
    ax.set_ylabel('Attendance Count')
    ax.set_title('Consolidated Attendance Chart')

    # Embed the plot into a Tkinter window
    chart_canvas = FigureCanvasTkAgg(fig, master=chart_window)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    connection.close()

headingFrame = tk.Frame(main_window, bg="white", bd=5)
headingFrame.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
headingLabel = tk.Label(headingFrame, text="Student Attendance Management System", bg='#2b3e44', fg='white', font=('Courier bold', 20))
headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)

headingLabel1 = tk.Label(main_window, text="Welcome to the Portal", bg='#192529', fg='white', font=('Arial', 15))
headingLabel1.place(relx=0.4, rely=0.25, relwidth=0.20, relheight=0.06)


#adding buttons
btn1 = tk.Button(main_window, text="ENROLLMENT", bg='#2b3e44', fg='white', font="Consolas 15 bold", command=enroll_student)
btn1.place(relx=0.28, rely=0.4, relwidth=0.45, relheight=0.1)

btn2 = tk.Button(main_window, text="TAKE ATTENDANCE", bg='#2b3e44', fg='white', font="Consolas 15 bold", command=take_attendance)
btn2.place(relx=0.28, rely=0.5, relwidth=0.45, relheight=0.1)

btn3 = tk.Button(main_window, text="DISPLAY ENROLLED STUDENTS", bg='#2b3e44', fg='white', font="Consolas 15 bold", command=display_students)
btn3.place(relx=0.28, rely=0.6, relwidth=0.45, relheight=0.1)

# btn4 = tk.Button(main_window, text="DISPLAY attended students", bg='dark blue', fg='white', font="Consolas 11 bold", command=display_attendance())
# btn4.place(relx=0.28, rely=0.7, relwidth=0.45, relheight=0.1)

btn4 = tk.Button(main_window, text="DISPLAY ATTENDANCE", bg='#2b3e44', fg='white', font="Consolas 15 bold", command=display_attendance)
btn4.place(relx=0.28, rely=0.7, relwidth=0.45, relheight=0.1)
# Button to display the attendance chart
btn_display_chart = tk.Button(main_window, text="DISPLAY ATTENDANCE CHART",bg='#2b3e44', fg='white', font="Consolas 15 bold", command=display_attendance_chart)
btn_display_chart.place(relx=0.28, rely=0.8, relwidth=0.45, relheight=0.1)
# Add more buttons or features as needed


# Start the Tkinter main loop
main_window.geometry("1450x967+100+100")
main_window.mainloop()

# Close the database connection
connection.close()


