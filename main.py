from tkinter import font
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from tkinter import *
from tkinter import messagebox

root = Tk()
root.geometry('500x200+500+100')
root.resizable(False, False)
root.title('Visualization Data')
root.iconbitmap('Data.ico')

def all_province():

    if not provinces.get() or e.get() == 0:

        messagebox.showwarning('Warning', 'กรอกข้อมูลก่อนน')

    else:

        try:
            if int(e.get()) > 2560 and int(e.get()) < 2564:
                year = e.get()
            else:
                messagebox.showwarning('Warning', 'ปีในช่วง พ.ศ. 2560 - 2563')
        except ValueError:
            messagebox.showwarning('Warning', 'Year is not string')

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
                    name = country.split(',')
                    if len(name) < 77:
                        for x in name:
                            array.append(province.index(str(x)))
                    else:
                        messagebox.showwarning('Warning', 'เกินลิมิตจังหวัด')
                except ValueError:
                    messagebox.showwarning('Warning', 'ลองชื่อเต็มของจังหวัดดูสิ')

            sub_case = []
            for x in array:
                sub_case.append(case[x])
            
            global avg
            if len(name) > 1:
                avg = sum(sub_case) / len(name)
            else:
                avg = 0

            a = Label(root, text=f'Average : {round(avg, 3)}',font=18).place(x=240, y=60)
            ma = Label(root, text=f'Max Value : {max(sub_case)}',font=18).place(x=240, y=80)
            mi = Label(root, text=f'Min Value : {min(sub_case)}',font=18).place(x=240, y=100)
            
            plt.bar(name, sub_case)
            plt.show()

    return None

avg = 0

l = Label(root, text='Data Visualization Thailand about news',font=28)

y = Label(root, text='ปี',font=18)
s = Label(root, text='จังหวัด',font=18)

provinces = StringVar()
p = Entry(root, textvariable=provinces, justify=CENTER,font=18)

year = IntVar()
e = Entry(root, textvariable=year, justify=CENTER,font=18)
b = Button(root,text='Enter', command=all_province,font=18)

l.pack()
s.place(x=10, y=60)
p.place(x=70, y=60)
y.place(x=10, y=100)
e.place(x=50, y=100)
b.place(x=280, y=95)

root.mainloop()