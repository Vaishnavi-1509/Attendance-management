import mysql.connector

# Initialize the MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="example"
)

# Create tables for the subjects
cursor = connection.cursor()

# Electrical Machines
cursor.execute("""
    CREATE TABLE IF NOT EXISTS electrical_machines_attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(255),
        voicesample LONGBLOB
    )
""")
# Power Systems
cursor.execute("""
    CREATE TABLE IF NOT EXISTS power_systems_attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(255),
        voicesample LONGBLOB
    )
""")
cursor.execute(f"ALTER TABLE power_systems_attendance ADD COLUMN attendance_date DATE")

# Python Programming
cursor.execute("""
    CREATE TABLE IF NOT EXISTS python_programming_attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(255),
        voicesample LONGBLOB
    )
""")
cursor.execute(f"ALTER TABLE python_programming_attendance ADD COLUMN attendance_date DATE")

# Maths
cursor.execute("""
    CREATE TABLE IF NOT EXISTS maths_attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(255),
        voicesample LONGBLOB
    )
""")
cursor.execute(f"ALTER TABLE maths_attendance ADD COLUMN attendance_date DATE")
# Analog Electronics
cursor.execute("""
    CREATE TABLE IF NOT EXISTS analog_electronics_attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(255),
        voicesample LONGBLOB
    )
""")

cursor.execute(f"ALTER TABLE analog_electronics_attendance ADD COLUMN attendance_date DATE")
# Data Structures
cursor.execute("""
    CREATE TABLE IF NOT EXISTS data_structures_attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(255),
        voicesample LONGBLOB
    )
""")
cursor.execute(f"ALTER TABLE data_structures_attendance ADD COLUMN attendance_date DATE")

# Electrical Network Lab
cursor.execute("""
    CREATE TABLE IF NOT EXISTS electrical_network_lab_attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(255),
        voicesample LONGBLOB
    )
""")
cursor.execute(f"ALTER TABLE electrical_network_lab_attendance ADD COLUMN attendance_date DATE")

connection.commit()

# Close the database connection
connection.close()
