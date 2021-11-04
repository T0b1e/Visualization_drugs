import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

def get_data(year):

    response = requests.get(f'https://dataapi.oncb.go.th/suppress/case_per/{year}')
    print("Server online")
    if response.status_code == 200:
        data_base = response.json()
        return data_base['data']
    else:
        print("Server Down")

def set_data(data):

    final = []
    prov = []
    case = []
    for a in data:
        prov.append(a['PROV_NAME'])
        case.append(a['arrestAll_case'])
    final.append(prov)
    final.append(case)

    return final

def show(year):

    response = requests.get(f'https://dataapi.oncb.go.th/suppress/case_per/{year}')
    print("Server online")
    if response.status_code == 200:
        data_base = response.json()
        data = data_base['data']
    else:
        print("Server Down")

    final = []
    prov = []
    case = []
    for a in data:
        prov.append(a['PROV_NAME'])
        case.append(a['arrestAll_case'])
    final.append(prov)
    final.append(case)

    plt.bar(final[0], final[1])

    return plt.show()

d = get_data(2563)
print(set_data(d))