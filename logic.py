#from collections import Counter
import pandas as pd

#path_to_data = 'F:\\Датасеты с ЛЦТ\\Book_exp.csv'
def number_listt(path_to_data):
    Exp = pd.read_csv(path_to_data)
    Exp = Exp.drop('userid', axis = 1)
    Exp_T = Exp.T
    number_list = []
    for number in range(0, len(Exp_T)):
        number_list.append(number)
    return number_list
def stock_list(path_to_data):
    Exp = pd.read_csv(path_to_data)
    Exp = Exp.drop('userid', axis = 1)
    Exp_T = Exp.T
    return Exp_T
def many_stocks(Exp_T, number):
    Exp_T = list(Exp_T[number])
    res_EXP = []
    for i in range(0, len(Exp_T)):
        if str(Exp_T[i]) != 'nan':
            res_EXP.append(Exp_T[i])
    return res_EXP
def main_sort(UC):
    l = []
    for i in range(0, len(UC)):
        for j in range(0, len(UC)):
            q = UC[int(i)]
            w = UC[int(j)]
            if q > w:
                a = (w, q)
                l.append(a)
            elif q < w:
                a = (q, w)
                l.append(a)
    a = dict(Counter(l))
    b = a.keys()
    b = pd.DataFrame(b)
    b.columns = ['Object_1', 'Object_2']
    vala = a.values()
    val = pd.DataFrame(vala)
    val.columns = ['val']
    qwer = val.val.tolist()
    b['val'] = qwer
    b['val'] = b['val']/2
    return b
def merge_stocks():
    dc = pd.DataFrame(columns = ['Object_1', 'Object_2', 'val'])
    Object_1p = []
    Object_2p = []
    valp = []
    number_list = number_listt(path_to_data)
    for i in number_list:
        Exp_T = stock_list(path_to_data)
        UC = many_stocks(Exp_T, i)
        number = i
        Object_1_i = []
        Object_2_i = []
        val_i = []
        df = main_sort(UC)
        Object_1 = list(df.Object_1)
        Object_2 = list(df.Object_2)
        val = list(df.val)
        Object_1p = Object_1p + Object_1
        Object_2p = Object_2p + Object_2
        valp = valp + val
        Object_1_i.append(Object_1p)
        Object_2_i.append(Object_2p)
        val_i.append(valp)
    end_df = pd.DataFrame({'Object_1' : Object_1_i[0], 'Object_2' :Object_2_i[0], 'val' : val_i[0]})
    return end_df
#merge_stocks()
def book_expir(path_to_data):
    Exp = pd.read_csv(path_to_data)
    Exp_T = list(Exp.iloc[1])
    res_EXP = []
    for i in range(0, len(Exp_T)):
        if str(Exp_T[i]) != 'nan':
            res_EXP.append(Exp_T[i])