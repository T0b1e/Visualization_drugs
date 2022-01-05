import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from province import change_name

# --Main Frame--

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

tree = ttk.Treeview(Frame2)  #TODO
tree['columns'] = ('Static', 'Value')
tree.column('#0', width=0, stretch=NO)
tree.column('Static', anchor=CENTER, width=100)
tree.column('Value',anchor=CENTER, width=100)

tree.heading('#0', text="", anchor=CENTER)
tree.heading('Static', text="Static", anchor=CENTER)
tree.heading('Value', text="Value", anchor=CENTER)

# --get data from https://dataapi.oncb.go.th/suppress/complain/{year} and decalir what is presenting year

def show_data():

    average = IntVar()
    average.set(0)
    graph.get()

    year = c.get()

    try:
        response = requests.get(f'https://dataapi.oncb.go.th/suppress/complain/{2563}') # Get data
        print("Server online")
        if response.status_code == 200: # Check is server still ok if server is ok response will be <200>
            data_base = response.json()
            data_set = data_base['data']
        else:
            messagebox.showwarning('Warning', 'Server Down')


    except ValueError:
        messagebox.showwarning('Warning', "Can't connect to server anymore")

    province = []
    for a in data_set:
        province.append(a['PROV_NAME']) # Get all of provinces name 73 prov

    case = []
    for b in data_set:
        case.append(b['complainAll']) # Get case of all provinces

    All = []
    for d in range(1,77):
        All.append(province)
        All.append(case) # Put provices and case in to one array

    # --Check--
    
    if not provinces.get() and check_province.get() == False: # If Provinces entry is empty and checkbox is uncheck

        messagebox.showwarning('Warning', 'กรอกข้อมูลก่อนน')
        summory = [0]
    
    if not provinces.get() and check_province.get() == True:  # If provinces entry is empty but the checkbox in check == True

        summory = case
        country = province

        plt.title(f'Visualization Data during {year} in Thailand') # Set title of image in range year

        if graph.get() == '1':  # Chart graph

            plt.bar(change_name(province), case)
            plt.show()
        
        if graph.get() == '0': # Pie chart

            plt.pie(case, labels=change_name(province))
            plt.show()
        
        else:
            
            messagebox.showwarning('Warning', 'เลือกประเภทกราฟก่อน')
        
    if provinces.get() and check_province.get() == True:

        messagebox.showwarning('Warning', 'เลือกสักอย่าง')
        summory = [0]
    
    if provinces.get() and check_province.get() == False:  #Selected data

        country = provinces.get()
        title_name = change_name((provinces.get()).split(','))
        
        name = (provinces.get()).split(',')
        plt.title(f'Visualization Data during {year} in {title_name}')

        try:
            array = []
            for a in (provinces.get()).split(','):
                array.append(province.index(a))
            
            sub_case = []
            for x in array:
                sub_case.append(case[x])

            summory = sub_case

            if graph.get() == '1':  # bar chart

                plt.bar(change_name(name), sub_case)
                plt.show()
            
            elif graph.get() == '0': # pie chart

                plt.pie(sub_case, labels=change_name(name))
                plt.show()
            
            else:
                
                messagebox.showwarning('Warning', 'เลือกประเภทกราฟก่อน')

        except ValueError:

            messagebox.showwarning('Warning', 'สะกดชื่อเต็มของจังหวัดดูสิ')
    
    else:

        messagebox.showwarning('Warning', 'กรอกข้อมูลก่อนน') # If everything is empty

    global mean

    if len(country) > 1:
        mean = round((sum(summory) / len(country)), 3)
    else:
        mean = 0

    average.set(round(mean, 5)) # ค่าเฉลี่ย

    med = (len(country) + 1) / 2  # ค่ากึ่งกลาง

    sd = round(((sum((x - mean)**2 for x in summory) / len(summory)) ** 0.5), 3)  

    max_count = (0, 0) 
    for x in summory:
        occurences = summory.count(x)
        if occurences > max_count[0]:
            max_count = (occurences, x)

    mode = max_count[1]

    mid_range = (max(summory) + min(summory)) / 2

    # Show result in table

    tree.insert(parent='', index=0, iid=0, text='', values=('ส่วนเบี่ยงเบนมาตรฐาน', str(sd)))  
    tree.insert(parent='', index=1, iid=1, text='', values=('ค่าเฉลี่ยเลขคณิต', str(mean)))
    tree.insert(parent='', index=2, iid=2, text='', values=('ค่ามัธยฐาน', str(med)))
    tree.insert(parent='', index=3, iid=3, text='', values=('ฐานนิยม', str(mode)))
    tree.insert(parent='', index=4, iid=4, text='', values=('ค่ากึ่งกลางพิสัย', str(mid_range)))
    tree.insert(parent='', index=5, iid=5, text='', values=('ค่าสูงสุด', str(max(summory))))
    tree.insert(parent='', index=6, iid=6, text='', values=('ค่าต่ำสุด', str(min(summory))))

    tree.pack()


    return None

def clear():

    if not p.get():
        messagebox.showwarning('Warning', 'ไม่มีข้อมูล')
    else:
        p.delete(0,"end")

# Documentation Frame

Label(Frame3, text="เนื้อหามีข้อมูลมาจาก  ข้อมูลเปิดภาครัฐ สำนักงาน ป.ป.ส. ช่วงปี 2557-2563",font=FONT).pack()
Label(Frame3, text="ประเภทข้อมูล API",font=FONT).pack()
Label(Frame3, text="ที่มาและความสำคัญ : Data.go.ac.th",font=FONT).pack()

Label(Frame4, text="Developer นาย ณรงค์กร กิจรุ่งโรจน์",font=FONT).pack()
Label(Frame4, text="Sorce code : https://github.com/T0b1e/Visualization_drugs",font=FONT).pack()
Label(Frame4, text="Data source : https://data.go.th/",font=FONT).pack()
Label(Frame4, text="Contact me: Email : 3068@psuwit.ac.th\n Facebook : Narongkorn kitrungrot",font=FONT).pack()

mean = 0

# Checkbox of all province

check_province = BooleanVar()
a = ttk.Checkbutton(Frame1, text='ทุกจังหวัด', variable=check_province, onvalue=True, offvalue=False)

l = Label(Frame1, text='Data Visualization Thailand about news', font=28)

s = Label(Frame1, text='จังหวัด', font=FONT)
y = Label(Frame1, text='ปี (พ.ศ.)', font=FONT)

years = (2557, 2558, 2559, 2560, 2561, 2562, 2563)

c = ttk.Combobox(Frame1, values=years)
c.current(6)

# get province name so you can put 1 or more than 1 Thailand province name for for example Songkhla

provinces = StringVar()
p = Entry(Frame1, textvariable=provinces, justify=CENTER, font=FONT)

# Select year

year = IntVar()
b = Button(Frame1,text='Enter', command=show_data, font=FONT)# give_data

cl = Button(Frame1,text='Clear',command=clear, font=FONT)

graph = StringVar()
g1 = ttk.Radiobutton(Frame1, text='Bar Graph', value=True, variable=graph)  # 1
g2 =ttk.Radiobutton(Frame1, text='Pie Chart', value=False, variable=graph)  # 0

# Show 

l.pack()
s.place(x=10, y=60)
y.place(x=10, y=100)
p.place(x=70, y=60)
a.pack()
b.place(x=280, y=95)
cl.place(x=280, y=55)
c.place(x=70, y=100)
g1.place(x=70, y=140)
g2.place(x=160, y=140)

root.mainloop()
