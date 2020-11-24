import pymsgbox,time

def MsgApp(data='Unknown'):
    #MsgBox = tk.messagebox.askquestion (,"Are You sure, You Are "+str(data),icon = 'warning')
        MsgBox = pymsgbox.confirm(timeout=5000,text='Are You sure, You Are '+str(data), title='Exit Application', buttons=['Yes', 'No'])
        
        if MsgBox == 'No':
            pymsgbox.alert(timeout=1000, title='Return',text='Please Keep straight ur face')
            return 1
        else:
            #Attendance.Attendance(data)
            pymsgbox.alert(timeout=1000, title='Success ',text='Your Attendance is marked Sucessfully')
            return 0
        return MsgBox
def Display(time=10000,data='',title='Exit Application'):
    pymsgbox.alert(timeout=time,text=data, title=title)
def prompt(time=10000,text='',title='defalt' ):
    data=pymsgbox.prompt(text=text, title=title)
    return data
if __name__=="__main__":
    print(MsgApp("Naveen"))
    time.sleep(2)
    print(MsgApp("Anachalam"))
    time.sleep(2)
    print(MsgApp("ananth"))
    time.sleep(2)
    print(MsgApp("thamarai"))
    Display(time=10000,data='Face Recognition startted show ur face',title='Exit Application')
    
