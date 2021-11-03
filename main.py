import tkinter
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

tab = ttk.Notebook(root)

Frame1 = Frame(tab)
Frame2 = Frame(tab)
Frame3 = Frame(tab)
Frame4 = Frame(tab)

tab.add(Frame1, text="Home")
tab.add(Frame2, text="Statistics")
tab.add(Frame3, text="Data Source")
tab.add(Frame4, text="About")
tab.pack(expand=True, fill="both")

FONT = "TH Sarabun PSK", 12


def show_data():

    year = c.get()

    try:
        response = requests.get(f'https://dataapi.oncb.go.th/suppress/complain/{year}')
        print("Server online")
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
        summory = [0]
    
    elif not provinces.get() and check_province.get() == True:  #All data

        plt.bar(change_name(province), case)
        plt.show()
        summory = case
        country = province
        
    elif provinces.get() and check_province.get() == True:

        messagebox.showwarning('Warning', 'เลือกสักอย่าง')
        summory = [0]
    
    elif provinces.get() and check_province.get() == False:  #Selected data

        country = provinces.get()

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

    if len(country) > 1:
        avg = sum(summory) / len(country)
    else:
        avg = 0

    av = Label(Frame1, text=f'Average : {round(avg, 5)}',font=FONT).place(x=200, y=150)
    ma = Label(Frame1, text=f'Max Value : {max(summory)}',font=FONT).place(x=200, y=180)
    mi = Label(Frame1, text=f'Min Value : {min(summory)}',font=FONT).place(x=200, y=210)

    return None

Label(Frame3, text="เนื้อหามีข้อมูลมาจาก  ข้อมูลเปิดภาครัฐ สำนักงาน ป.ป.ส. ช่วงปี 2557-2563",font=FONT).pack()
Label(Frame3, text="ประเภทข้อมูล API",font=FONT).pack()
Label(Frame3, text="ที่มาและความสำคัญ : Data.go.ac.th",font=FONT).pack()

Label(Frame4, text="Deleloper นาย ณรงค์กร กิจรุ่งโรจน์",font=FONT).pack()
Label(Frame4, text="Sorce code : https://github.com/T0b1e/Visualization_drugs",font=FONT).pack()
Label(Frame4, text="Data source : https://data.go.th/",font=FONT).pack()

avg = 0

check_province = BooleanVar()
a = ttk.Checkbutton(Frame1, text='ทุกจังหวัด', variable=check_province, onvalue=True, offvalue=False)

l = Label(Frame1, text='Data Visualization Thailand about news', font=28)

s = Label(Frame1, text='จังหวัด', font=FONT)
y = Label(Frame1, text='ปี (พ.ศ.)', font=FONT)

years = (2557, 2558, 2559, 2560, 2561, 2562, 2563)

c = ttk.Combobox(Frame1, values=years)
c.current(6)

provinces = StringVar()
p = Entry(Frame1, textvariable=provinces, justify=CENTER, font=FONT)

year = IntVar()
e = Entry(Frame1, textvariable=year, justify=CENTER, font=FONT)
b = Button(Frame1,text='Enter', command=show_data, font=FONT)# give_data

cl = Button(Frame1,text='Clear', font=FONT)

l.pack()
s.place(x=10, y=60)
y.place(x=10, y=100)
p.place(x=70, y=60)
a.pack()
b.place(x=280, y=95)
cl.place(x=280, y=55)
c.place(x=70, y=100)

root.mainloop()
