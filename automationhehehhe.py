import os
import sys
import sqlite3 as sq
import re
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from email.mime.image import MIMEImage

# Printing logo
logo = '''

  ___                      _      ___,                                                     
 / (_)                 o  | |    /   |                                     o               
 \__   _  _  _    __,     | |   |    |        _|_  __   _  _  _    __, _|_     __   _  _   
 /    / |/ |/ |  /  |  |  |/    |    |  |   |  |  /  \_/ |/ |/ |  /  |  |  |  /  \_/ |/ |  
 \___/  |  |  |_/\_/|_/|_/|__/   \__/\_/ \_/|_/|_/\__/   |  |  |_/\_/|_/|_/|_/\__/   |  |_/


'''
print(logo)
# Create a database and table for storing email and name information
def database():
    if os.name == 'nt': # if the OS is Windows
        if 'emaildb.db' not in os.listdir(os.path.expanduser("~") + '\\'): # if the database file does not exist
            connect_database = sq.connect(os.path.expanduser("~") + '\\emaildb.db') # create a connection object to the database
            cur = connect_database.cursor() # create a cursor object to interact with the database
            cur.execute("CREATE TABLE IF NOT EXISTS USERS(email text, name text)") # create a table named USERS with email and name columns
            connect_database.commit() # commit the changes to the database
            connect_database.close() # close the connection
        else:
            pass

    elif os.name == 'posix': # if the OS is Unix-based
        if 'emaildb.db' not in os.listdir(os.path.expanduser("~") + '/Documents/'): # if the database file does not exist
            connect_database = sq.connect(os.path.expanduser("~") + '/Documents/emaildb.db') # create a connection object to the database
            cur = connect_database.cursor() # create a cursor object to interact with the database
            cur.execute("CREATE TABLE IF NOT EXISTS USERS(email text, name text)") # create a table named USERS with email and name columns
            connect_database.commit() # commit the changes to the database
            connect_database.close() # close the connection
        else:
            pass

# Regular expression pattern for email validation
def validate(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Function to load email and name data from a CSV file to the database
def addition():
    if os.name == 'nt': # if the OS is Windows
        connect_database = sq.connect(os.path.expanduser("~") + '\\emaildb.db') # create a connection object to the database
    elif os.name == 'posix': # if the OS is Unix-based
        connect_database = sq.connect(os.path.expanduser("~") + '/Documents/emaildb.db') # create a connection object to the database
    cur = connect_database.cursor() # create a cursor object to interact with the database
    cur.execute("CREATE TABLE IF NOT EXISTS USERS (email text, name text)") # create a table named USERS with email and name columns
    with open(os.path.expanduser("~") + '\\report1.csv') as file: # open the CSV file for reading
        csvreader = csv.reader(file) # create a CSV reader object to read the CSV file
        next(csvreader) # skip the header row
        for i in csvreader: # for each row in the CSV file
            cur.execute("INSERT INTO USERS VALUES(?, ?)", (i[1], i[2])) # insert the email and name values into the USERS table
            connect_database.commit() # commit the changes to the database

    file.close() # close the CSV file
    connect_database.close() # close the database connection
    print("CSV File loaded successfully!")

# Function to send email to all the recipients in the database

def send():
    # Set sender email and password
    sender_email = "shadwalbvp@gmail.com"
    password = "ipjptukxparkqkks" 

    # Create SMTP session and start TLS connection
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()

    # Login to the account using the app password
    session.login(sender_email, password)

    # Connect to SQLite database and retrieve all user email addresses and names
    if os.name == 'nt':
        connect_database = sq.connect(os.path.expanduser("~") + '\\emaildb.db')
    elif os.name == 'posix':
        connect_database = sq.connect(os.path.expanduser("~") + '/Documents/emaildb.db')
    cur = connect_database.cursor()
    values = []
    for i in cur.execute("SELECT * FROM USERS"):
        values.append([i[0], i[1]])

    # For each user, create email message and send it
    for i in values:
        receiver_email = i[0]
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = "Email-Automation Done!"

        message.attach(MIMEText("Hey! " + i[1], 'plain'))

        with open(r"C:\Users\sahil\Downloads\batman2.jpg", 'rb') as file:
            img = MIMEImage(file.read())
            message.attach(img)
        # Send email
        text = message.as_string()
        session.sendmail(sender_email, receiver_email, text)
        print("Email sent to", i[0])

    # Close SMTP session and print success message
    session.quit()
    print('E-Mails Sent Successfully!')


while True:
    # Display menu and get user's choice
    print("A)LOAD CSV")
    print("B)SEND EMAIL")
    print("C)EXIT")
    choice = input("> ")
    while choice.lower() not in 'abc':
        print("Invalid Choice")
        choice = input("> ")
    else:
        # Execute appropriate function based on user's choice
        if choice.lower() == 'a':
            addition()
        elif choice.lower() == 'b':
            send()
        elif choice.lower() == 'c':
            break
