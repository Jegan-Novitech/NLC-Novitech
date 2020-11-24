import sqlite3,time
import socket
conn = sqlite3.connect('attendance.db')
c = conn.cursor()
now=time.localtime()
print(now)
reader_name= str(socket.gethostname())
print("'"+reader_name+"'")
reader_name="'"+reader_name+"'"
time_stamp=str(now[3])+str(now[4])+str(now[5])
date_stamp=str(now[2])+str(now[1])+str(now[0])
# Create table
try:
    c.execute('''CREATE TABLE temp_attendance
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,reader_id text, time text, date text, emp_id text)''')
except:
    pass
# Insert a row of data
c.execute("INSERT INTO temp_attendance (reader_id , time , date , emp_id) VALUES (%s,%s,%s,'B0474160')"% (reader_name,time_stamp,date_stamp))

# Save (commit) the changes
conn.commit()
for row in c.execute('SELECT * FROM temp_attendance ORDER BY ID'):
        print(row)
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()