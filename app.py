import streamlit as st
import requests
import pandas as pd
import threading
from streamlit_extras.let_it_rain import rain
from datetime import datetime
import json
import time

# print('🔵 🟢 🟡 🔴 🟠 '*2,'Welcome',' 🔵 🟢 🟡 🔴 🟠'*2)

results = pd.DataFrame(
    columns=["ID's", "Code", "Gift/Msg", "log", "Time Taken", "Start Time", "End Time"])
sss = """"""


def redeem_code(cid, code):
    global sss,results
    start_time = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    URL = 'https://lordsmobile.igg.com/project/gifts/ajax.php?game_id=1051029902'
    payload = {
        'ac': 'get_gifts',
        'type': '0',
        'iggid': str(cid),
        'charname': '',
        'cdkey': str(code),
        'lang': 'en',
    }
    response = requests.post(URL, data=payload, headers=headers)
    result = response.json()
    # print(result)
    end_time = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
    delta = end_time - start_time
    d = dict()
    d['ID'] = cid
    d['gift_code'] = code
    d['server_reply'] = result['msg']
    d['succ'] = result['succ']
    d['start_time'] = str(start_time)
    d['end_time'] = str(end_time)
    d['task_time'] = str(delta.total_seconds())
    sss = sss+str(json.dumps(d, indent=4))
    if(result['succ'] == 0):
        # results.loc[len(results)] = [cid,code,result['msg'],'Fail',str(delta.total_seconds())+' sec',start_time,end_time]
        res = pd.DataFrame(
            {
                "ID's": [cid],
                "Code": [code],
                "Gift/Msg": [result['msg']],
                "log": ['Fail'],
                "Time Taken": [str(delta.total_seconds())+' sec'],
                "Start Time": [start_time],
                "End Time": [end_time]
            }
        )
        results=pd.concat([results,res],ignore_index=True)
    else:
        # results.loc[len(results)] = [cid,code,result['msg'],'Success',str(delta.total_seconds())+' sec',start_time,end_time]
        res = pd.DataFrame(
            {
                "ID's": [cid],
                "Code": [code],
                "Gift/Msg": [result['msg']],
                "log": ['Success'],
                "Time Taken": [str(delta.total_seconds())+' sec'],
                "Start Time": [start_time],
                "End Time": [end_time]
            }
        )
        results=pd.concat([results,res],ignore_index=True)


def start_threads(code):
    threads = []
    f = open("ids.txt", "r")
    ids = f.read()
    for id in ids.split(','):
        mythread = threading.Thread(
            target=redeem_code, name="redeem_code", args=(id, code))
        # time.sleep(0.1)
        mythread.start()
        threads.append(mythread)

    for x in threads:
        global logtxt
        x.join()
        logtxt += sss + ' \n'
        logtxtbox.text_area("Logging: ", logtxt)


st.title("Lords Mobile Code Redeem")
code = st.text_input("Enter your code:")
submit_button = st.button("Submit")
logtxtbox = st.empty()
logtxt = ''
logtxtbox.text_area("Logging: ", logtxt)
if submit_button:
    st.write(f"submitting code: {code}")
    start_threads(code)
    rain(
        emoji="😍",
        font_size=40,
        falling_speed=5,
        animation_length="1",
    )
    st.balloons()
    st.write("Results:")
    st.write(results)
