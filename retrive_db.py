import sqlite3,time
import requests
try:
    import httplib
except:
    import http.client as httplib
import cx_Oracle
def insert(detail, temp, mask):
    conn = cx_Oracle.connect("system", "Novi1234", "192.168.43.33/orcl:5500",encoding = 'UTF-8')
    cursor = conn.cursor()
    sql = ("insert into attendance_table (detail, temp, mask) values (%s,%s,%s)"%(detail, temp, mask))
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
def checkInternetHttplib(url="www.google.com", timeout=3):
    conn = httplib.HTTPConnection(url, timeout=timeout)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except Exception as e:
#         print(e)
        return False
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM temp_attendance WHERE ID=?", (priority,))

    rows = cur.fetchall()
    
    print(rows[0])
    return rows[0]
def delete_task(conn, id):
    """
        Delete a task by task id
        :param conn:  Connection to the SQLite database
        :param id: id of the task
        :return:        """
    sql = 'DELETE FROM temp_attendance WHERE ID=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
while 1:
        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        try:
            for row in c.execute('SELECT ID FROM temp_attendance'):
                    print(row[0])
                    details=select_task_by_priority(conn,row[0])
                    attendance=details[1]
                    DeviceName=details[2]
                    DateTime=details[3]
                    temperature=details[4]
                    mask=details[5]
                    print(attendance,temperature,mask)
                    print(requests.get('http://attendance.coitor.com/client_send.php?att_details='+str(attendance)+'&mask='+str(mask)+'&temperature='+str(temperature)))
                    
                    time.sleep(0.2)
                    delete_task(conn,row[0])
        except:
            pass
    #         delete_task(conn,row[0])
    conn.close()
