import Tkinter as tk
import ttk
import serial
import time
import threading
import Queue
import re
import math
from guiLoop import guiLoop # https://gist.github.com/niccokunzmann/8673951
import tabsConfig

root = tk.Tk()
root.title("Data Monitoring Interface")
root.resizable(width=tk.FALSE, height=tk.FALSE)
root.state('zoomed')

st_ploter = 0.00001  # Sleep time in sec for refreshing plots
st_quer = 0.00001  # Sleep time in sec for refreshing plots
NP = 100
recvActive = False

varTextConn = tk.StringVar()
comVar = tk.StringVar()
baudVar = tk.StringVar()
varTextConn.set(' Serial Unconnected ... ')

def clearPlots() :
    f1.clearPlots()
    f2.clearPlots()
    f3.clearPlots()
    f4.clearPlots()
    f5.clearPlots()
    f6.clearPlots()
    f7.clearPlots()
    f8.clearPlots()
    
def connect2Serial():
    global recvActive
    try :
        ser.baudrate = int(baudVar.get())
        ser.timeout = 0.1
        ser.port = comVar.get()
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.bytesize = serial.EIGHTBITS
        
        if not ser.isOpen() :
            ser.open()
            connectBtn.config(state='disabled')
            disconnBtn.config(state='normal')
            varTextConn.set(' Connected to ' + comVar.get() + ' at baud rate ' + baudVar.get())
            recvBtn.config(state='normal')
            time.sleep(1)
            print ser
            ser.flushInput()
            
        else :
            ser.close()
            connectBtn.config(state='normal')
            disconnBtn.config(state='disabled')
            recvBtn.config(state='normal')
            varTextConn.set(' Disconnected ...')
            recvBtn.config(state='disable')
            recvBtn.config(text = '  Receive Data   ')

            clearPlots()

        recvActive = False

    except serial.SerialException.message :
        varTextConn.set(' Can''nt connect to ' + comVar.get() + ' at baud rate ' + baudVar.get())


def receivingData():
    global recvActive
    global NP
    recvActive = not recvActive
    if recvActive :
        quer(root)
    
        recvBtn.config(text = ' Stop Receiving ')
        clearPlots()

        npStr = npBox.get()
        if npStr.isdigit() and int(npStr)>10 :
            NP = int(npStr)
        else :
            NP = 100

    else :
        recvBtn.config(text = '  Receive Data   ')

        

@guiLoop
def quer():

    while True :
        if not recvActive :
            break

        try :
            data_mm = None
            data_gyro = None
            data_mt = None
            data_ahrs = None
            data_rw = None
            data_rwc = None
            
            if ser.isOpen() and ser.inWaiting() :
                data = ser.readline()
                print "Received raw data : " + data

                recd = re.split(' |\$|@|#', data)
                data = data.replace('\n', '')
                data = data.replace('\r', '')
                
                code = int(recd[1])
                if code==1 :
                    data_mm = data
                elif code==2 :
                    data_gyro = data
                elif code==3 :
                    data_mt = data
                elif code==4 :
                    data_ahrs = data
                elif code==5 :
                    data_rw = data
                elif code==6 :
                    data_rwc = data

            if not(data_mm is None) :
                f1.plot(data_mm)
            elif not(data_gyro is None) :
                f2.plot(data_gyro)
            elif not(data_mt is None) :
                f3.plot(data_mt)
            elif not(data_ahrs is None) :
                f4.plot(data_ahrs)
                f5.plot(data_ahrs)
                f6.plot(data_ahrs)
            elif not(data_rwc is None) :
                f7.plot(data_rwc)
            elif not(data_rw is None) :
                f8.plot(data_rw)

        except :
            pass
        yield st_quer




ser = serial.Serial()

dict_mm = {'num': 4, 'offset': 2, '1': 'MM_x (uT)', '2': 'MM_y (uT)', '3': 'MM_z (uT)', '4': 'MM_Magnitude (uT)', 'outFile': 'outputMM.xls', 'mag': 1}
dict_gyro = {'num': 4, 'offset': 2, '1': 'Gyro_x (deg/s)', '2': 'Gyro_y (deg/s)', '3': 'Gyro_z (deg/s)', '4': 'Gyro_Magnitude (deg/s)', 'outFile': 'outputGyro.xls', 'mag': 1}
dict_mt = {'num': 3, 'offset': 2, '1': 'MT_x', '2': 'MT_y', '3': 'MT_z', 'outFile': 'outputMT.xls', 'mag': 0}
dict_ahrs_quat = {'num': 4, 'offset': 2, '1': 'quat_1', '2': 'quat_2', '3': 'quat_3', '4': 'quat_4', 'outFile': 'outputAHRS_Quat.xls', 'mag': 0}
dict_ahrs_euler = {'num': 3, 'offset': 6, '1': 'ang_x (deg)', '2': 'ang_y (deg)', '3': 'ang_z (deg)', 'outFile': 'outputAHRS_Euler.xls', 'mag': 0}
dict_ahrs_omega = {'num': 3, 'offset': 9, '1': 'omega_x (deg/s)', '2': 'omega_y (deg/s)', '3': 'omega_z (deg/s)', 'outFile': 'outputAHRS_Omega.xls', 'mag': 0}
dict_rw = {'num': 3, 'offset': 2, '1': 'RW_rate_x (deg/s)', '2': 'RW_rate_y (deg/s)', '3': 'RW_rate_z (deg/s)', 'outFile': 'outputRW.xls', 'mag': 0}
dict_rwc = {'num': 3, 'offset': 2, '1': 'T_RW_1 (N-m)', '2': 'T_RW_2 (N-m)', '3': 'T_RW_3 (N-m)', 'outFile': 'outputCommandRW.xls', 'mag': 0}

nb = ttk.Notebook(root)
nb.grid(row=1, column=0, sticky='NW', padx=5, pady=5, ipadx=5, ipady=5)
f1 = tabsConfig.tabFrame(root, **dict_mm)
f2 = tabsConfig.tabFrame(root, **dict_gyro)
f3 = tabsConfig.tabFrame(root, **dict_mt)
f4 = tabsConfig.tabFrame(root, **dict_ahrs_quat)
f5 = tabsConfig.tabFrame(root, **dict_ahrs_euler)
f6 = tabsConfig.tabFrame(root, **dict_ahrs_omega)
f7 = tabsConfig.tabFrame(root, **dict_rw)
f8 = tabsConfig.tabFrame(root, **dict_rwc)
nb.add(f1, text='  Magnetometer ')
nb.add(f2, text='  Gyro ')
nb.add(f3, text='  MagnetoTorquer Commands ')
nb.add(f4, text='  AHRS Quaternion ')
nb.add(f5, text='  AHRS Euler Angles ')
nb.add(f6, text='  AHRS Omega ')
nb.add(f7, text='  RW Outputs ')
nb.add(f8, text='  RW Commands ')

btnLf = tk.LabelFrame(root)
btnLf.grid(row=0, column=0, sticky='NW', padx=5, pady=5)


## ------ Serial communication setting : ------
comChoices = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9']
baudChoices = [9600, 19200, 38400, 57600, 115200]
comVar.set('COM3')
baudVar.set(115200)

serFr = tk.Frame(btnLf)
serFr.grid(row=0, column=0, sticky='NW', padx=5, pady=5) #, ipadx=10, ipady=10)

comLbl = tk.Label(serFr, text="Port", fg='blue') #,anchor='w')
comLbl.grid(row=0, column=0) #, sticky='W', padx=5, pady=5)
comCombo = ttk.Combobox(serFr, state="readonly", values=comChoices, textvariable=comVar)
comCombo.set(comChoices[2])
comCombo.grid(row=0, column=1) #, sticky='W', padx=10, pady=5)
baudLbl = tk.Label(serFr, text="Baud rate", fg='blue') #, anchor='w')
baudLbl.grid(row=0, column=2, padx=5, pady=5) #, sticky='E')
baudCombo = ttk.Combobox(serFr, state="readonly", values=baudChoices, textvariable=baudVar)
baudCombo.set(baudChoices[4])
baudCombo.grid(row=0, column=3, padx=5, pady=5) #, sticky='E')

connectBtn = tk.Button(serFr, text=' Connect ', command= lambda : connect2Serial())
connectBtn.grid(row=0, column=4, padx=15, pady=10, sticky='E')
disconnBtn = tk.Button(serFr, text=' Disconnect ', command= lambda : connect2Serial(), state='disable')
disconnBtn.grid(row=0, column=5, pady=10, sticky='W')

connStatus_Lbl = tk.Label(serFr, textvariable=varTextConn, fg='purple')
connStatus_Lbl.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='W')

recFrame = tk.Frame(btnLf)
recFrame.grid(row=0, column=1, sticky='E', padx=10, pady=15, ipadx=10)
npLbl = tk.Label(recFrame, text="Max. number of points : ", anchor='e')
npLbl.grid(row=1, column=0, columnspan=2, sticky='W', padx=50, pady=5)
npBox = tk.Entry(recFrame, bd=3, width=7)
npBox.grid(row=1, column=1, sticky='E', padx=45, pady=5)
npBox.insert(0, "100")


recvBtn = tk.Button(recFrame, text='  Receive Data  ', anchor='w', command= lambda : receivingData())
recvBtn.grid(row=0, column=0, sticky='W', columnspan=4, padx=390, pady=7)

clearPlots()
recvBtn.config(state='disable')

root.mainloop()

if ser.isOpen() :
    ser.close()
