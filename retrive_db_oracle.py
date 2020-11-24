import sqlite3,time
import requests,udplib,json
f=open("/home/faren-t/share/config",'r')
test_string = f.read()
res = json.loads(test_string)
host_ip=res['host_ip']
port_no=res['port_no']
f.close()
try:
    import httplib
except:
    import http.client as httplib

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
##        c.execute("SELECT * FROM temp_attendance ORDER BY ID ASC LIMIT 1")
        c.execute("SELECT * FROM temp_attendance ORDER BY ID DESC LIMIT 1")
        details = c.fetchone()
        if(details !=None):
                    attendance=details[1]
                    temperature=details[2]
                    mask=details[3]
                    print(details[0],attendance,temperature,mask)
                    data=attendance+"~"+str(temperature)+"~"+str(mask)
                    print(data)
                    print(udplib.Attend_send(data,host_ip=host_ip,port_no=port_no,bufferSize = 1024))
                    
                    time.sleep(0.2)
                    delete_task(conn,row[0])
    except:
            pass
    #         delete_task(conn,row[0])
    conn.close()
