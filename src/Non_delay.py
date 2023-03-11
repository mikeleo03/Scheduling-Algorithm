# Implementasi algoritma Non-delay
# 0.1. Impor modul eksternal
from datetime import datetime
import time
import calendar
import csv

# 0.2. Definisi variabel global
ROUTING = []
PROCESSING_TIME = []
MESIN = []
JOB_DONE = []
SCHEDULE = []

# 1. Prosedur untuk melakukan pembacaan data dari file
def read_data():
    # Menggunakan variabel global
    global ROUTING, PROCESSING_TIME, MESIN
    print("Sedang membaca data...")

    # Pembacaan data mesin dari file
    # Exception handling
    try:
        mesin_file = open(f"test/Mesin.txt", "r")
    except:
        print(f"File Mesin.txt tidak ditemukan!")
        exit()
        
    # Konversi ke tabel
    mesin_data = csv.reader(mesin_file)
    
    # Pengolahan isi tabel
    for row in mesin_data:
        for i in range(len(row)):
            row[i] = float(row[i])
            if row[i] % 1.0 == 0:
                row[i] = int(row[i])
        MESIN.append(row)
        
    print("Data mesin berhasil dibaca!")
    
    # Pembacaan data job dari file      
    n_jobs = int(input("Masukkan jumlah job: "))
    for j in range(n_jobs):
        # Exception handling  
        try:
            time_file = open(f"test/Job{j + 1}_Time.txt", "r")
        except:
            print(f"File Job{j + 1}_Time.txt tidak ditemukan!")
            exit()
            
        # Konversi ke tabel
        time_data = csv.reader(time_file)
        
        # Pengolahan isi tabel
        for row in time_data:
            for i in range(len(row)):
                row[i] = float(row[i])
                if row[i] % 1.0 == 0:
                    row[i] = int(row[i])
            PROCESSING_TIME.append(row)

        # Exception handling 
        try:
            routing_file = open(f"test/Job{j + 1}_Routing.txt", "r")
        except:
            print(f"File Job{j + 1}_Routing.txt tidak ditemukan!")
            exit()
            
        # Konversi ke tabel
        routing_data = csv.reader(routing_file)
        
        # Pengolahan isi tabel
        for row in routing_data:
            for i in range(len(row)):
                row[i] = float(row[i])
                if row[i] % 1.0 == 0:
                    row[i] = int(row[i])
            ROUTING.append(row)
            
    print("Data time dan routing berhasil dibaca!")

# 2. Defining ID of process
def define_id(i, j, k):
    ID = str(i) + str(j) + str(k)
    return ID
    
# 3. Ekekusi time
def state_check(count):
    global MESIN, JOB_DONE, SCHEDULE, CJ, TJ, RJ, ST
    print("seconds : ",count)
    print("cj",CJ)
    print("tj",TJ)
    print("rj",RJ)
    print("st",ST)
    print("MESIN",MESIN)
    
    print("============================")
    
    # e. Menentukan nilai cj terkecil, job dengan cj terkecil akan diproses duluan
    min_c = min(CJ)
    
    temp_list = []  # temporary list
    
    # f. Kalo misal ada lebih dari 1 yang punya nilai minimum itu, kita handle
    if CJ.count(min_c) > 1:
        print("adaberapa?",CJ.count(min_c))
        # Bikin list yang isinya semua job yang punya nilai min_c
        index_c_in_cj = [i for i in range(len(CJ)) if CJ[i] == min_c]
        print("indeiks",index_c_in_cj)

        # Cek nilai rj dan pilih yang mempunyai nilai rj terkecil
        # Prioritasin yang jumlah operasinya masih banyak
        machine_list = []  # machine list

        # Isi list dengan semua data yang ada di index_c_in_cj
        for i in index_c_in_cj:
            if len(temp_list) == 0 or ST[i][2] not in machine_list:
                temp_list.append(ST[i])
                machine_list.append(ST[i][2])
            elif ST[i][2] in machine_list:
                index_mac = machine_list.index(ST[i][2]) #i
                if (RJ[i] < RJ[ST.index(temp_list[index_mac])]):
                    temp_list[index_mac] = ST[i]
                elif ST[i][1] < temp_list[index_mac][1]:
                    temp_list[index_mac] = ST[i]
                    
        print("cekie",temp_list, machine_list)
        # sehkarang temp_list isinya job yang mau dijalankan
        retval = temp_list

    else:
        retval = [ST[CJ.index(min_c)]]
    
    print("retval",retval)
    # Index job value (?) 
    for value in retval:
        i = ST.index(value)
        SCHEDULE.append([value[0], value[1], value[2], CJ[i], RJ[i]])
        if value[1] == 3:
            JOB_DONE.append([value[0], RJ[i]])

    index_job = [ST.index(i) for i in retval]
    index_mac = [i[2] - 1 for i in retval]
    
    print("idx_job, idx_mach",index_job, index_mac)

    COPY_OF_ST = [i for i in ST]
    COPY_OF_CJ = [i for i in CJ]
    
    bias = 0
    
    print("older cj, st",CJ, ST)
    print("len borth", len(CJ), len(COPY_OF_CJ))

    for i, j in zip(index_job, index_mac):
        # Updating MESIN
        MESIN[0][j] = RJ[i]
        try:
            # Updating cj
            # CJ[i] = RJ[i]
            # Updating tj
            TJ[i] = PROCESSING_TIME[ST[i][0] - 1][ST[i][1]]
            # Updating st
            ST[i] = [ST[i][0], ST[i][1] + 1, ROUTING[ST[i][0] - 1][ST[i][1]]]
        except:
            TJ.pop(i - bias)
            ST.pop(i - bias)
            CJ.pop(i - bias)
            bias += 1
            
    # index_job1 = [ST.index(i) for i in COPY_OF_ST]
    """ index_job1 = []
    for i in COPY_OF_ST:
        try :
            index_job1.append(ST.index(i))
        except :
            continue """
    
    print("old cj, st",CJ, ST)
    # Updating the cj
    for i in range(len(COPY_OF_ST)):
        try:
            if i in index_job:
                ready_time = MESIN[0][ST[i][2] - 1]
                recent_rjx = RJ[i]
                # print("rd, rcnt",ready_time, recent_rjx)
                if COPY_OF_ST[i][1] != len(COPY_OF_ST[0]):
                    if ready_time > recent_rjx:
                        COPY_OF_CJ[i] = ready_time
                    else :
                        COPY_OF_CJ[i] = recent_rjx
            else :
                print(i)
                print("mesin", MESIN[0][COPY_OF_ST[i][2] - 1])
                if (COPY_OF_CJ[i] <= MESIN[0][COPY_OF_ST[i][2] - 1]):
                    COPY_OF_CJ[i] = MESIN[0][COPY_OF_ST[i][2] - 1]
        except:
            continue
        
    print("latestcopy",COPY_OF_CJ)
    
    if (len(CJ) < len(COPY_OF_CJ)):
        for i in range(len(COPY_OF_CJ) - 1, -1, -1):
            if i in index_job and COPY_OF_ST[i][1] == len(COPY_OF_ST[0]):
                print(i)
                COPY_OF_CJ.pop(i)
            else :
                continue
            
    CJ = COPY_OF_CJ
                    
    print("cj, st", CJ, ST)
        
    # Updating cj kalo overdua
    # retval = [3, 1, 3] mewakili job3, yang1, mesin3
    """ print("strv2",retval,TEMP_ST)
    for i in range (len(retval)):
        if retval[i] != TEMP_ST and count + 1 == CJ[ST.index(value)]:
            CJ[i] += 1 """
     
    # Updating rj
    RJ = [0 for i in range(len(ST))]
    for i in range (len(ST)):
        RJ[i] = CJ[i] + TJ[i]           
        
    print("----------------------------")

    return ST

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
    
read_data()
# a. Mendefinisikan posisi melalui routing
CJ = [MESIN[0][ROUTING[i][0] - 1] for i in range(len(ROUTING))]
# b. Mendefinisikan waktu pemrosesan
TJ = [PROCESSING_TIME[i][0] for i in range(len(ROUTING))]
# c. Mendefinisikan waktu berakhir
RJ = [0 for i in range(len(ROUTING))]
for i in range (len(ROUTING)):
    RJ[i] = CJ[i] + TJ[i]
# d. Mendefinisikan id st (job, operasi, mesin)
ST = [[i + 1, 1, ROUTING[i][0]] for i in range(len(ROUTING))]
print("pt",PROCESSING_TIME)
print("r",ROUTING)
print("m",MESIN)
# state_check()
count = 0
while state_check(count) != []:
    count += 1
    pass
print('---- Semua job telah selesai ----')
print_schedule()
# cj, tj, rj, st = state_check()
""" print("Hasil state check")
print("cj", cj)
print("tj", tj)
print("rj", rj)
print("st", st) """
print(SCHEDULE)
print(JOB_DONE)