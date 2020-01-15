from serial import *
from tkinter import *
import tkinter.ttk as ttk
import serial
import serial.tools.list_ports
import threading        # for parallel computing

class myThread(threading.Thread):
    def __init__(self, name,ser):
        threading.Thread.__init__(self)
        self.name = name
        self.ser = ser
        self.stopevent = threading.Event()
        self.paused = False

    def run(self):
        while self.ser.isOpen():
            if not self.paused:
                received_text.insert(END,self.ser.readline())
                received_text.see(END)
                if self.stopevent.isSet():
                    break

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def disconnect(self):
        self.stopevent.set()

def serial_ports():
    return serial.tools.list_ports.comports()

def on_select(event=None):

    # get selection from event
    print("event.widget:", event.widget.get())

    # or get selection directly from combobox
    print("comboboxes: ", cb.get())

def serial_open_cmd():
    try:
        global ser
        ser = serial.Serial(serial_port,ser_baudrate, timeout=1)
        global thread1
        thread1 = myThread("Updating", ser)
        thread1.start()
        print(serial_port, "is connected")
        # open port if not already open
        if ser.isOpen() == False:
            ser.open()
        elif ser.isOpen() == True:
            b1.configure(text = "Connected")
    except serial.SerialException:
            print ("error open serial port: " + ser.port )

def serial_close_cmd():
    if ser.isOpen() == True:
        thread1.disconnect()
        ser.close()
        print("Disconnected")
        b1.configure(text = "Connect")

def mSend(command):
    # try:
    thread1.pause()
    ser.write(command.encode('ascii'))
    thread1.resume()
    # except:
        # print ("Could not send command. Port closed?")
    return

def config_cmd():
    mSend("C")
def fwd_cmd(event):
    try:
        mSend('F')
    except:
        pass
def rvs_cmd(event):
    try:
        mSend('R')
    except:
        pass
def set_cmd():
    mSend('S')
def rst_cmd():
    mSend('N')
def count_cmd():
    mSend('A')

def change_vel(event):
    try:
        vel = w1.get()
        print(vel)
        if (vel==20):
            mSend('Q')
        if (vel==25):
            mSend('W')
        if (vel==30):
            mSend('E')
        if (vel==35):
            mSend('T')
        if (vel==40):
            mSend('Y')
        if (vel==45):
            mSend('D')
        if (vel==50):
            mSend('G')
        if (vel==60):
            mSend('J')
        if (vel==70):
            mSend('L')
        if (vel==80):
            mSend('V')
        if (vel==90):
            mSend('B')
        if (vel==100):
            mSend('O')
    except:
        pass



def releasing(event):
    try:
        mSend('M')
    except:
        pass

if len(serial.tools.list_ports.comports()) != 0:
    COM = serial.tools.list_ports.comports()
    serial_port = COM[0][0]
    ser_baudrate = 9600

root = Tk()
root.resizable(False,False)

root.wm_title("MERİÇ Serial Communication For DC Motor Driver")

cb = ttk.Combobox(root, values=serial_ports())
cb.grid(row = 1, column = 0,padx=10,pady=10)
# assign function to combobox
cb.bind('<<ComboboxSelected>>', on_select)

l1=Label(root,text="Serial Port Selection",height=2,width=20)
l1.grid(row=0,column=0,columnspan=2)

l2=Label(root,text="Sent",height=2,width=20)
l2.grid(row=0,column=2,columnspan=4,padx=10,pady=1)

l3=Label(root,text="Received",height=2,width=20)
l3.grid(row=2,column=2,columnspan=4,padx=10,pady=1)

received_text = Text (root, takefocus=0)
received_text.grid(row = 3,rowspan = 6,column = 2,columnspan = 4,padx=10,pady=10)
# received_text.bind("<Return>", readSerial)

b1=Button(root, text="Connect", width=12,command=serial_open_cmd)
b1.grid(row=2,column=0,padx=10,pady=10)

b_disconnect=Button(root, text="Disconnect", width=12,command=serial_close_cmd)
b_disconnect.grid(row=3,column=0,padx=10,pady=10)

b2=Button(root, text="Config", width=12,command=config_cmd)
b2.grid(row=1,column=2,padx=10,pady=10)

b3=Button(root, text="Forward", width=12)
b3.grid(row=1,column=3,padx=10,pady=10)
b3.bind("<ButtonPress-1>",fwd_cmd)
b3.bind("<ButtonRelease-1>",releasing)

b4=Button(root, text="Reverse", width=12)
b4.grid(row=1,column=4,padx=10,pady=10)
b4.bind("<ButtonPress-1>",rvs_cmd)
b4.bind("<ButtonRelease-1>",releasing)

b5=Button(root, text="SET", width=12,command=set_cmd)
b5.grid(row=1,column=5,padx=10,pady=10)

b6=Button(root, text="RESET", width=12,command=rst_cmd)
b6.grid(row=1,column=6,padx=10,pady=10)

b7=Button(root, text="ENCODER", width=12,command=count_cmd)
b7.grid(row=2,column=6,padx=10,pady=10)

global vel
w1 = Scale(root, from_=20, to=100, resolution = 5,command=change_vel)
vel=20
w1.set(vel)
w1.grid(row = 3, column= 6,padx=10,pady=10)

time.sleep(1)

root.mainloop()
