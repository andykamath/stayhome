import requests
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
import json

def fetch():
    df = pd.DataFrame(requests.get('https://covidtracking.com/api/states/daily').json())
    totals = df.groupby('dateChecked').agg('sum')
    return totals

def regress(x_data, y_data):
    first_nonzero = 0
    while y_data[first_nonzero] == 0:
        first_nonzero += 1
    x_data = x_data[first_nonzero:]
    y_data = y_data[first_nonzero:]
    log_x_data = np.log(x_data)
    log_y_data = np.log(y_data)

    exp, coeff = np.polyfit(x_data, log_y_data, 1)

    y = np.exp(coeff) * np.exp(exp)**x_data
    print("Base -", np.exp(coeff), "r0 -", np.exp(exp))
    return np.exp(coeff), np.exp(exp)

def what_if(arr, day, amount_home):
    base, r0 = regress(np.arange(0, len(arr)), arr)
    vals = []
    total = base
    for i, val in enumerate(arr):
        vals.append(total)
        if i == day:
            total *= r0
            total -= amount_home
        else:
            total *= r0
    return vals