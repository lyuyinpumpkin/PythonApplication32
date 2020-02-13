from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox
from datetime import datetime, timedelta
import os
import time
import datetime
from threading import Thread,Timer
import pickle 
import psutil

def judgeprocess(processname):
    pl = psutil.pids()
    try:
        for pid in pl:
            if psutil.Process(pid).name() == processname:
                break
        else:
            os.system("start /B "+ restart_address)
    except:
        pass

def selectPath():
    if change_state.get()=="normal":
        path_ = askdirectory()
        path.set(path_)
    else:
        return

def lockParameter():
    global e1
    global e2
    if change_state.get()=="normal":
        change_state.set("disabled") 
        e1['state']=change_state.get()
        e2['state']=change_state.get()
        windows.update()     
    elif change_state.get()=="disabled":
        change_state.set("normal") 
        e1['state']=change_state.get()
        e2['state']=change_state.get()
        windows.update()
    with open(program_address,'r+b') as f1:
        read_list=pickle.load(f1)
        read_list.update(pathsave=path.get())
        read_list.update(date_numbersave=date_number.get())
    with open(program_address,'w+b') as f2:
        pickle.dump(read_list,f2)

def change_schedule(now_schedule,all_schedule):
    canvas.coords(fill_rec, (5, 5,5+(now_schedule/all_schedule)*200, 25))
    windows.update()
    x.set(str(round(now_schedule/all_schedule*100,2)) + '%')
    if round(now_schedule/all_schedule*100,2) == 100.00:
        x.set("完成")

def startProgram(): 
    
    global thread_signal
    if  thread_signal == True:
        tkinter.messagebox.showerror('错误','程序已打开')
        return
    else:
        pass
    thread_signal=True
    global goal_path
    goal_path= path.get()
    if os.path.exists(path.get()):
        try:
            delta_time=int(date_number.get())
        except:
            tkinter.messagebox.showerror('错误','输入保留天数错误，请重新输入！')
            return
    else:
        tkinter.messagebox.showerror('错误','输入地址错误，请重新输入！')
        return
    global e1
    global e2
    change_state.set("disabled") 
    e1['state']=change_state.get()
    e2['state']=change_state.get()
    windows.update()
    with open(program_address,'rb') as f1:
        read_list=pickle.load(f1)
        read_list.update(pathsave=path.get())
        read_list.update(date_numbersave=date_number.get())
    with open(program_address,'wb') as f2:
        pickle.dump(read_list,f2)
    starttime = datetime.datetime.now()
    d1 = starttime - timedelta(days=delta_time)
    #d2 = starttime - timedelta(days=n) #获取n天前的时间
    date1=str(d1)
    index = date1.find('.')  # 第一次出现的位置
    global datatime_usr
    datatime_usr = date1[:index]
    global thread_del
    thread_del = Thread(target=del_all,args=(goal_path,datatime_usr))
    thread_del.start()
   
def file_count(filedir1):
    btn_text.set("删除中")
    global filecount
    for root, dirs, filenames in os.walk(filedir1):
        filecount+=len(filenames)
        filecount+=len(dirs)
        for filename in (filenames):
            filepath_list.append(os.path.join(root,filename))
        for dir in dirs:
            folderpath_list.insert(0,os.path.join(root,dir))

def del_all(allpath,set_time):  
    global thread_signal
    global filecount
    filecount = 0
    file_count(allpath)
    global realcount
    realcount = 0
    delfile(set_time)
    delfolder()
    filepath_list.clear()
    folderpath_list.clear()
    btn_text.set("开始删除")
    thread_signal=False
    return

def delfile(datatime):
    global thread_signal
    i=0
    for each in filepath_list:
        filetime_stamp=os.stat(each).st_mtime
        filetime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(filetime_stamp))
        global realcount
        realcount+=1
        change_schedule(realcount,filecount)
        if (datatime > filetime):
            os.remove(each)
            i+=1

def delfolder():
    j=0
    for each in folderpath_list:
        global realcount
        realcount+=1
        change_schedule(realcount,filecount)
        if not os.listdir(each):
            os.rmdir(each)
            j+=1

def cycle_start():
    global countdown
    for i in range (3600):
        countdown.set(3600 - i)
        windows.update()
        time.sleep(1)
    if thread_signal == False:
        startProgram()
        t_cycle = Timer(1, cycle_start)
        t_cycle.start()
    elif thread_signal == True:
        t_cycle = Timer(1, cycle_start)
        t_cycle.start()

def main():
    global path
    global date_number
    global x
    global countdown
    countdown = StringVar()
    x =StringVar()
    path = StringVar(windows,value=pathinitial)
    date_number=StringVar(windows,value=dateinitial)
    Label(windows,text = "目标路径:",font=('Calibri', 12)).grid(row=0, column=0, padx=10,pady=5)
    global e1
    e1=Entry(windows, textvariable = path,font=('Calibri', 12),state=change_state.get())
    e1.grid(row=0, column=1,padx=0,pady=5)
    Button(windows, text = "路径选择", font=('Calibri', 12),command = selectPath,bg="coral",activebackground="orange").grid(row=0,column=2,padx=10,pady=5)
    Label(windows,text = "保留天数:",font=('Calibri', 12)).grid(row=1, column=0,padx=10,pady=5)
    global e2
    e2=Entry(windows, textvariable = date_number,font=('Calibri', 12),state=change_state.get())
    e2.grid(row=1, column=1,padx=0,pady=5)
    Button(windows, text = "锁定", font=('Calibri', 12),command = lockParameter,bg="coral",activebackground="orange").grid(row=1,column=2,padx=10,pady=5)
    Button(windows, textvariable=btn_text, font=('Calibri', 20),command =startProgram,bg="aqua",activebackground="orange").grid(row=2, column=1,padx=10,pady=10)
    Label(windows,text = "删除进度:",font=('Calibri', 12)).grid(row=3, column = 0,padx=10,pady=5)
    global canvas
    frame = Frame(windows).grid(row = 3,column = 0,padx=10,pady=5)
    canvas = Canvas(windows,width=205,height=25,bg = "white")
    canvas.grid(row=3,column=1,padx=10,pady=5)
    out_rec = canvas.create_rectangle(5,5,205,25,outline = "lime",width = 1)
    global fill_rec
    fill_rec = canvas.create_rectangle(5,5,5,25,outline = "",width = 0,fill = "lime")
    Label(frame,textvariable = x).grid(row = 3,column = 2,padx=10,pady=5)
    Label(windows,textvariable = countdown,font=('Calibri', 12)).grid(row = 2,column = 2,pady=5)

if __name__ == '__main__':
    windows = Tk()
    windows.title('删除文件v1.4')
    windows.geometry('425x200')
    restart_address = os.path.join(os.getcwd(),'restartProgram.exe')
    judgeprocess('restartProgram.exe')
    global filepath_list
    filepath_list=[]
    global folderpath_list 
    folderpath_list=[]
    global btn_text
    btn_text = StringVar()
    btn_text.set("开始删除")
    change_state = StringVar(windows,value="disabled")
    program_address_folder = os.getcwd()
    program_address = os.path.join(program_address_folder,"my_list.pkl")
    if os.path.exists(program_address):
        with open(program_address, "rb") as fp:
            read_file=pickle.load(fp)
            pathinitial=read_file.get("pathsave")
            dateinitial=read_file.get("date_numbersave")   
    else:
        my_list= dict(zip(["pathsave","date_numbersave"],[None,None]))
        pathinitial= ""
        dateinitial= ""
        pickle_file=open(program_address,"wb")
        pickle.dump(my_list,pickle_file)
        pickle_file.close()
    thread_signal= False
    main()
    thread_cyc = Thread(target=cycle_start)
    thread_cyc.start()
    windows.mainloop()
   