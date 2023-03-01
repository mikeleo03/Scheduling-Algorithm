import pyrebase
from datetime import datetime
import time
import calendar


firebaseConfig = {  "apiKey": "AIzaSyD3DASICtOhpQRuSDxCdhh8DQkuw97OrsA",
  "authDomain": "finalta-66e60.firebaseapp.com",
  "databaseURL": "https://finalta-66e60-default-rtdb.firebaseio.com",
  "projectId": "finalta-66e60",
  "storageBucket": "finalta-66e60.appspot.com",
  "messagingSenderId": "966705935989",
  "appId": "1:966705935989:web:a1fc7665b3db8c51e2aa3c",
  "measurementId": "G-TV9WKWW9BX"}

firebase=pyrebase.initialize_app(firebaseConfig)

db=firebase.database()

now = datetime.now()
epochtime = int(time.time())+25200
date = now.strftime("%y/%m/%d")
date1 = now.strftime("%y-%m-%d")
#print(date1)

a = date.split("/")
result = calendar.weekday(int(a[0]), int(a[1]), int(a[2]))
day = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
hari = (day[result])
#print(hari)

dtt = (hari+","+date1)
#print(dtt)

MESIN = []
x = 1
mesin = int(input("Masukkan jumlah mesin: "))
while x<mesin+1:
    
    tes1 = db.child(f"Mesin {x}",dtt).order_by_key().limit_to_last(1).get()
    for test1 in tes1.each():
        test1 = (test1.key())
    #print(test1)
    #print(Users2)

    high_w1 = db.child(f"Mesin {x}",dtt,test1).order_by_key().equal_to("Epoch_High").get()
    for high1 in high_w1.each():
        high1 = (high1.val())
        #print(Users)

    est1 = db.child(f"Mesin {x}",dtt,test1).order_by_key().equal_to("Estimasi").get()
    for estimasi1 in est1.each():
        estimasi1 = (estimasi1.val())*3600
        #print(Users3)

    hasil1 = ((high1+estimasi1-epochtime)/3600)

    cnt1 = db.child(f"Mesin {x}",dtt,test1).order_by_key().get()
    if len(cnt1.val()) == 5:
        p = 0
    elif hasil1 <= 0:
        p = 0
    elif hasil1 > 0:
        p = round(hasil1,2)
    
    MESIN.append(p)
    x+=1
print("Ready time mesin: ")
print(MESIN)
#----------------------------------------------------------------------------------

import copy
import csv

# PROCESSING_TIME contains lists of time needed for each operation

# PROCESSING_TIME = [
#     [1, 3, 2],  # Job 1
#     [3, 4, 2],  # Job 2
#     [2, 3, 3],  # Job 3
#     [2, 3, 4],  # Job 4
# ]

# Example from the given excel sheet
# PROCESSING_TIME = [
#     [4, 3, 2],  # Job 1
#     [1, 4, 4],  # Job 2
#     [3, 2, 3],  # Job 3
#     [3, 3, 1],  # Job 4
# ]

PROCESSING_TIME = []

# ROUTING contains lists of which machine is used for each operation

# ROUTING = [
#     [3, 1, 2],  # Job 1
#     [2, 1, 3],  # Job 2
#     [1, 2, 3],  # Job 3
#     [2, 3, 1],  # Job 4
# ]

# Example from the given excel sheet
# ROUTING = [
#     [1, 2, 3],  # Job 1
#     [2, 1, 3],  # Job 2
#     [3, 2, 1],  # Job 3
#     [2, 3, 1],  # Job 4
# ]

ROUTING = []

JOB_DONE = []

# Schedule in the form of lists of integers
SCHEDULE = []
# SCHEDULE = [[3, 1, 3, 0, 3], [2, 1, 2, 1, 2], [4, 1, 2, 2, 5], [1, 1, 1, 3, 7], [3, 2, 2, 5, 7], [4, 2, 3, 5, 8], [
#     1, 2, 2, 7, 10], [3, 3, 1, 7, 10], [1, 3, 3, 10, 12], [4, 3, 1, 10, 11], [2, 2, 1, 11, 15], [2, 3, 3, 15, 19]]

# MESIN contains ready time for each machine

# MESIN = [4, 2, 1]
# READY = [4, 2, 1]

# Example from the given excel sheet
# MESIN = [3, 1, 0]
# READY = [3, 1, 0]

st = [[i + 1, 1, ROUTING[i][0]] for i in range(len(ROUTING))]
tj = [PROCESSING_TIME[i][0] for i in range(len(ROUTING))]
cj = [MESIN[st[i][2] - 1] for i in range(len(ROUTING))]

# Show info about current stage


def show_info(rj):
    print(f'MESIN: {MESIN}')
    for i in range(len(st)):
        print(st[i], cj[i], tj[i], rj[i])


# Function automate_schedule() appends time for every finished job to JOB_DONE
# Values returned will be in a 3 dimensional array [[Job, Operation, Machine]]


def automate_schedule(st, cj, tj):

    global MESIN, JOB_DONE, SCHEDULE

    retval = []

    if len(st) == 0:
        return None

    # Define rj where rj = cj + tj

    rj = [(i + j) for i, j in zip(cj, tj)]

    # show_info(rj)

    # Decide which machine(s) should work first from cj
    # Job(s) which has the smallest cj will operate first

    c = min(cj)

    if cj.count(c) > 1:
        index_c_in_cj = [i for i in range(len(cj)) if cj[i] == c]

        # Check machine and its rj, choose which one has the smallest rj (rj*)
        # Different machine can work at the same time, but remaining operations more prioritized

        tmp = []  # temporary list
        mac = []  # machine list

        for i in index_c_in_cj:

            if len(tmp) == 0 or st[i][2] not in mac:
                tmp.append(st[i])
                mac.append(st[i][2])

            elif st[i][2] in mac:
                index_mac = mac.index(st[i][2]) #i

                if (rj[i] < rj[st.index(tmp[index_mac])]):
                    tmp[index_mac] = st[i]

                elif st[i][1] < tmp[index_mac][1]:
                    tmp[index_mac] = st[i]

        # Now tmp contains the schedule(s) for the job(s)
        # Assign its value to return value (retval)

        retval = tmp

    else:
        retval = [st[cj.index(c)]]

    # print(f'ROUTING SCHEDULE: {retval}')

    for value in retval:
        i = st.index(value)
        SCHEDULE.append([value[0], value[1], value[2], cj[i], rj[i]])
        if value[1] == 3:
            JOB_DONE.append([value[0], rj[i]])

    index_job = [st.index(i) for i in retval]
    index_mac = [i[2] - 1 for i in retval]

    COPY_OF_ST = [i for i in st]

    bias = 0

    for i, j in zip(index_job, index_mac):

        # Updating MESIN
        MESIN[j] = rj[i]

        try:

            # Updating tj

            tj[i] = PROCESSING_TIME[st[i][0] - 1][st[i][1]]

            # Updating st

            st[i] = [st[i][0], st[i][1] + 1, ROUTING[st[i][0] - 1][st[i][1]]]

        except:
            tj.pop(i - bias)
            st.pop(i - bias)
            cj.pop(i - bias)
            bias += 1

    # Updating cj

    for i in index_job:
        try:
            ready_time = MESIN[st[i][2] - 1]
            recent_rjx = rj[i]
            if COPY_OF_ST[i][1] != 3:
                cj[i] = max([ready_time, recent_rjx])
        except:
            continue

    for i in range(len(cj)):
        if st[i] in COPY_OF_ST:
            ready_time = MESIN[st[i][2] - 1]
            current_cj = cj[i]
            if i == COPY_OF_ST.index(st[i]) or st[i] not in retval:
                cj[i] = max([ready_time, current_cj])
            else:
                cj[i] = ready_time

    return retval


# Print makeform and schedule to string form in the console
def print_schedule(schedule=SCHEDULE, lateness=None):
    global PROCESSING_TIME
    makespan = max(schedule, key=lambda x: x[4])[4]
    for i in range(len(PROCESSING_TIME)):
        j = max(filter(lambda a: a[0] == i + 1, schedule), key=lambda x: x[4])[4]
        print(f'Job {i + 1} telah selesai dengan waktu selesai {round(j,2)}')
        for s in sorted(schedule, key=lambda x: x[0]):
            if s[0] == i + 1:
                print(f'{s[0]}{s[1]}{s[2]}: Start {round(s[3],2)} End {round(s[4],2)}')
        if lateness is not None:
            print(f"Earliness: {round(lateness[i],2) * -1}" if lateness[i] <= 0 else f"Tardiness: {round(lateness[i],2)}")
    print(f'---\nmakespan: {round(makespan,2)}')


def read_data():
    global ROUTING, PROCESSING_TIME, MESIN
    print("Sedang membaca data...")

    n_jobs = int(input("Masukkan jumlah job: "))
    for j in range(n_jobs):
        try:
            time_file = open(f"Job{j + 1}_Time.txt", "r")
        except:
            print(f"File Job{j + 1}_Time.txt tidak ditemukan!")
            exit()
        time_data = csv.reader(time_file)
        for row in time_data:
            for i in range(len(row)):
                row[i] = float(row[i])
                if row[i] % 1.0 == 0:
                    row[i] = int(row[i])
            PROCESSING_TIME.append(row)

        try:
            routing_file = open(f"Job{j + 1}_Routing.txt", "r")
        except:
            print(f"File Job{j + 1}_Routing.txt tidak ditemukan!")
            exit()
        routing_data = csv.reader(routing_file)
        for row in routing_data:
            for i in range(len(row)):
                row[i] = float(row[i])
                if row[i] % 1.0 == 0:
                    row[i] = int(row[i])
            ROUTING.append(row)

    st = [[i + 1, 1, ROUTING[i][0]] for i in range(len(ROUTING))]
    tj = [PROCESSING_TIME[i][0] for i in range(len(ROUTING))]
    cj = [MESIN[st[i][2] - 1] for i in range(len(ROUTING))]

    return st, tj, cj


if __name__ == '__main__':
    st, tj, cj = read_data()

    while automate_schedule(st, cj, tj) != None:
        pass
    print('---- Semua job telah selesai ----')
    print_schedule()

input("Press Enter to Exit")
