import tkinter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from province import change_name


root = Tk()
root.geometry('500x300+500+100')
root.resizable(False, False)
root.title('Visualization Data')
root.iconbitmap('Data.ico')

FONT = "TH Sarabun PSK", 12


def show_data():

    year = c.get()

    try:
        response = requests.get(f'https://dataapi.oncb.go.th/suppress/complain/{year}')
        print(year)
        print(response.status_code)
        if response.status_code == 200:
            data_base = response.json()
            data_set = data_base['data']
        else:
            messagebox.showwarning('Warning', 'Server Down')


    except ValueError:
        messagebox.showwarning('Warning', "Can't connect to server anymore")

    province = []
    for a in data_set:
        province.append(a['PROV_NAME'])

    case = []
    for b in data_set:
        case.append(b['complainAll'])

    if not provinces.get() and check_province.get() == False:

        messagebox.showwarning('Warning', 'กรอกข้อมูลก่อนน')
        summory = 0
    
    elif not provinces.get() and check_province.get() == True:  #All data

        plt.bar(change_name(province), case)
        summory = case
        plt.show()
    
    elif provinces.get() and check_province.get() == True:

        messagebox.showwarning('Warning', 'เลือกสักอย่าง')
        summory = 0
    
    elif provinces.get() and check_province.get() == False:  #Selected data

        try:
            array = []
            for a in (provinces.get()).split(','):
                array.append(province.index(a))
            
            sub_case = []
            for x in array:
                sub_case.append(case[x])

            summory = sub_case

            plt.bar(change_name((provinces.get()).split(',')), sub_case)
            plt.show()

        except ValueError:
            print(ValueError)
            messagebox.showwarning('Warning', 'สะกดชื่อเต็มของจังหวัดดูสิ')
    
    else:

        messagebox.showwarning('Warning', 'กรอกข้อมูลก่อนน')
    
    global avg
    if len((provinces.get()).split(',')) > 1:
        avg = sum(summory) / len((provinces.get()).split(','))
    else:
        avg = 0

    a = Label(root, text=f'Average : {round(avg, 3)}',font=FONT).place(x=200, y=150)
    ma = Label(root, text=f'Max Value : {max(summory)}',font=FONT).place(x=200, y=180)
    mi = Label(root, text=f'Min Value : {min(summory)}',font=FONT).place(x=200, y=210)

    return None

def source():
    widget2 = Tk()
    widget2.geometry('500x300+500+100')
    widget2.resizable(False, False)
    widget2.title('Source Data')
    widget2.iconbitmap('Data.ico')
    Label(widget2, text="เนื้อหามีข้อมูลมาจาก  ข้อมูลเปิดภาครัฐ สำนักงาน ป.ป.ส. ช่วงปี 2557-2563",font=FONT).pack()
    Label(widget2, text="ประเภทข้อมูล API",font=FONT).pack()
    Label(widget2, text="ที่มาและความสำคัญ : Data.go.ac.th",font=FONT).pack()

def bout():
    widget3 = Tk()
    widget3.geometry('500x300+500+100')
    widget3.resizable(False, False)
    widget3.title('About')
    widget3.iconbitmap('Data.ico')
    Label(widget3, text="Deleloper นาย ณรงค์กร กิจรุ่งโรจน์",font=FONT).pack()
    Label(widget3, text="Sorce code : https://github.com/T0b1e/Visualization_drugs",font=FONT).pack()
    Label(widget3, text="Data source : https://data.go.th/",font=FONT).pack()

sub_menu = Menu()
sub_menu.add_command(label='Source', command=source)
sub_menu.add_command(label='About',command=bout)

main_menu = Menu()
root.config(menu=main_menu)
main_menu.add_cascade(label='Documentation', menu=sub_menu)

avg = 0

check_province = BooleanVar()
a = ttk.Checkbutton(root, text='ทุกจังหวัด', variable=check_province, onvalue=True, offvalue=False)

l = Label(root, text='Data Visualization Thailand about news', font=28)

s = Label(root, text='จังหวัด', font=FONT)
y = Label(root, text='ปี (พ.ศ.)', font=FONT)

years = (2557, 2558, 2559, 2560, 2561, 2562, 2563)

c = ttk.Combobox(root, values=years)
c.current(6)

provinces = StringVar()
p = Entry(root, textvariable=provinces, justify=CENTER, font=FONT)

year = IntVar()
e = Entry(root, textvariable=year, justify=CENTER, font=FONT)
b = Button(root,text='Enter', command=show_data, font=FONT)# give_data

l.pack()
s.place(x=10, y=60)
y.place(x=10, y=100)
p.place(x=70, y=60)
a.pack()
b.place(x=280, y=95)
c.place(x=70, y=100)

root.mainloop()
