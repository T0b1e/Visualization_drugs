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

def all_province():

    if not provinces.get():

        messagebox.showwarning('Warning', 'กรอกข้อมูลก่อนน')

    else:

        year = c.get()

        response = requests.get(f'https://dataapi.oncb.go.th/suppress/complain/{year}')
        data = response.json()
        real_data = data['data']

        province = []
        for a in real_data:
            province.append(a['PROV_NAME'])

        case = []
        for b in real_data:
            case.append(b['complainAll'])

        if not provinces.get():

            plt.bar(province, case)
            plt.show()
        
        else:

            array = []
            country = provinces.get()
            try:
                int(country)
                messagebox.showwarning('Warning', 'ใส่เป็นชื่อจังหวัด')
            except ValueError:
                try:
                    '''if ',' not in [i for i in country]:
                        messagebox.showwarning('Warning', 'ใส่ , ขั้นกลางด้วย')'''

                    name = country.split(',')
                    if len(name) < 77:
                        for x in name:
                            array.append(province.index(str(x)))
                    else:
                        messagebox.showwarning('Warning', 'เกินลิมิตจังหวัด')
                except ValueError:
                    messagebox.showwarning('Warning', 'ลองชื่อเต็มของจังหวัดดูสิ')

            new_name = change_name(name)

            sub_case = []
            for x in array:
                sub_case.append(case[x])
            
            global avg
            if len(name) > 1:
                avg = sum(sub_case) / len(name)
            else:
                avg = 0

            a = Label(root, text=f'Average : {round(avg, 3)}',font=FONT).place(x=200, y=150)
            ma = Label(root, text=f'Max Value : {max(sub_case)}',font=FONT).place(x=200, y=180)
            mi = Label(root, text=f'Min Value : {min(sub_case)}',font=FONT).place(x=200, y=210)
            
            plt.bar(new_name, sub_case)
            plt.show()

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

years = (2557, 2558, 2559, 2560, 2561, 2562, 2563)


l = Label(root, text='Data Visualization Thailand about news',font=28)

c = ttk.Combobox(root, values=years)
c.current(6)

s = Label(root, text='จังหวัด',font=FONT)
y = Label(root, text='ปี (พ.ศ.)',font=FONT)

provinces = StringVar()
p = Entry(root, textvariable=provinces, justify=CENTER,font=FONT)

year = IntVar()
e = Entry(root, textvariable=year, justify=CENTER,font=FONT)
b = Button(root,text='Enter', command=all_province,font=FONT)

l.pack()
s.place(x=10, y=60)
y.place(x=10, y=100)
p.place(x=70, y=60)
#e.place(x=70, y=100)
b.place(x=280, y=95)
c.place(x=70, y=100)

root.mainloop()