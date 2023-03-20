# Implementasi Algoritma Penjadwalan Genetic-Algorithm
# 1. Impor modul eksternal
import csv

# 2. Definisi variabel global
ROUTING = []
PROCESSING_TIME = []
MESIN = []
JOB_DONE = []
SCHEDULE = []

# 3. Prosedur untuk melakukan pembacaan data dari file
def read_data():
    # Menggunakan variabel global
    global ROUTING, PROCESSING_TIME, MESIN
    print("Sedang membaca data...")

    # Pembacaan data mesin dari file dan exception handling
    try:
        mesin_file = open(f"test3/Mesin.txt", "r")
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
            time_file = open(f"test3/Job{j + 1}_Time.txt", "r")
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
            routing_file = open(f"test3/Job{j + 1}_Routing.txt", "r")
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

# 4. Prosedur Eksekusi
def do_genetic_algo():
    # xx. Menggunakan variabel global
    global MESIN, JOB_DONE, SCHEDULE, CJ, TJ, RJ, ST

    # a. Mengambil nilai cj terkecil dari data masukan, job dengan cj terkecil akan diproses duluan
    # min_c = min(CJ)
    
    # b. Inisiasi senarai temporari
    temp_list = []
    
    # c. Kalau misal ada lebih dari 1 yang punya nilai minimum, digunakan skema penanganan
    # if CJ.count(min_c) > 1:
    # Inisiasi senarai yang berisi semua job dengan nilai min_c
    index_c_in_cj = [i for i in range(len(CJ))]

    # Cek nilai rj dan pilih yang mempunyai nilai rj terkecil
    # Prioritaskan yang jumlah operasinya masih banyak
    machine_list = []  # machine list

    # Isi list dengan semua data yang ada di index_c_in_cj
    for i in index_c_in_cj :
        # temp_list.append(ST[i])
        machine_list.append(ST[i][2])
        
    for i in index_c_in_cj:
        index_mac = machine_list.index(ST[i][2])
        job = ST[i][0]
        # Kalo mesinnya kosong, atau bisa selesai lebih cepat, masukin di
        # tempat yang memungkinkan, proses genetikasi
        if (ST[i][2] >= 1 and ST[i][2] <= 4):
            # print("ehsini1")
            minimum = MESIN[0][0]
            idx_mesin = 0
            for j in range (4):
                if (minimum > MESIN[0][j]):
                    idx_mesin = j
                    minimum = MESIN[0][j]
                    
            if (MESIN[0][ST[i][2] - 1] > minimum):
                ST[job-1] = [job, ST[job-1][1], idx_mesin + 1]
                MESIN[0][ST[i][2] - 1] += PROCESSING_TIME[job - 1][ST[i][1] - 1]
                temp_list.append(ST[i])
            else :
                MESIN[0][ST[i][2] - 1] += PROCESSING_TIME[job - 1][ST[i][1] - 1]
                temp_list.append(ST[i])
            print ("ST, MESIN", ST, MESIN)
        elif (ST[i][2] >= 5 and ST[i][2] <= 6):
            print("ehsini1")
            minimum = MESIN[0][4]
            idx_mesin = 4
            for j in range (4, 5):
                if (minimum > MESIN[0][j]):
                    idx_mesin = j
                    minimum = MESIN[0][j]
                    
            if (MESIN[0][ST[i][2] - 1] > minimum):
                ST[i] = [job, ST[i][1], idx_mesin + 1]
                MESIN[0][ST[i][2] - 1] += PROCESSING_TIME[job - 1][ST[i][1] - 1]
                temp_list.append(ST[i])
            else :
                MESIN[0][ST[i][2] - 1] += PROCESSING_TIME[job - 1][ST[i][1] - 1]
                temp_list.append(ST[i])
            print ("ST, MESIN", ST, MESIN)
        else :
            # Prioritas nilai rj
            if (RJ[i] < RJ[ST.index(temp_list[index_mac])]):
                temp_list[index_mac] = ST[i]
            # Prioritas jumlah operasi
            elif ST[i][1] < temp_list[index_mac][1]:
                temp_list[index_mac] = ST[i]
                
    # Sekarang temp_list isinya job yang mau dijalankan (dalam sebuah list)
    retval = temp_list

    # Kalau tidak, kembalikan saja nilai st dari cj tersebut dalam sebuah list
    """ else:
        retval = [ST[CJ.index(min_c)]] """
        
    # d. Melakukan indexing terhadap jadwal yang ada dan telah selesai
    print("retval?", retval)
    print("cek cj st 1", CJ, ST)
    job = []
    instance = []
    machine = []
    for i in range (len(retval)):
        job.append(retval[i][0])
        instance.append(retval[i][1])
        machine.append(retval[i][2])
        
    print("job, retval", job, machine)
    job_on_ST = []
    # print("ST", ST)
    for i in range (len(ST)):
        job_on_ST.append(ST[i][0])
        
    print("job_on_st", job_on_ST)
    for value in job:
        i = job_on_ST.index(value)
        # print("i", i)
        SCHEDULE.append([ST[i][0], ST[i][1], ST[i][2], CJ[i], RJ[i]])
        if ST[i][1] == len(ROUTING[ST[i][0] - 1]):
            JOB_DONE.append([ST[i][0], RJ[i]])

    # e. Lanjutan pemrosesan indexing untuk dikemas dalam senarai job dan machine
    index_job = [job_on_ST.index(value) for value in job]
    index_mac = machine
    
    print("idx_job", index_job)
    print("cek cj st 2", CJ, ST)
    
    # f. Melakukan penyalinan nilai st dan cj untuk digunakan lebih lanjut pada bagian bawah
    COPY_OF_ST = [i for i in ST]
    COPY_OF_CJ = [i for i in CJ]
    
    # g. Melakukan perubahan terhadap nilai isi mesin, tj dan st
    # bias untuk membantu skema penghapusan berdasar indeks
    bias = 0
    for i in range (len(index_job)):
        k = index_job[i]
        print(k)
        # Memperbaharui nilai MESIN
        # MESIN[0][j] = RJ[i]
        try:
            # Memperbaharui nilai tj
            print("untuk index i", k, ST[k][0] - 1, ST[k][1])
            TJ[k] = PROCESSING_TIME[ST[k][0] - 1][ST[k][1] - 1]
            print("TJ", TJ)
            # Memperbaharui nilai st
            ST[k] = [ST[k][0], ST[k][1] + 1, ROUTING[ST[k][0] - 1][ST[k][1]]]
            print("ST", ST)
            print(k, "LEWAT")
        except:
            # Exception handling jika tidak ada, maka saatnya dihapus
            TJ.pop(k - bias)
            ST.pop(k - bias)
            CJ.pop(k - bias)
            bias += 1

    print("cek cj st 3", CJ, COPY_OF_CJ, ST)
    # h. Memperbaharui nilai cj pada COPY_OF_CJ (salinan cj)
    for i in range(len(COPY_OF_ST)):
        try:
            # Jika nilai iterator berada pada index_job,
            # maka update dengan nilai data proses selanjutnya, lakukan perbandingan dengan
            # nilai proses pada mesin
            if i in index_job:
                ready_time = MESIN[0][ST[i][2] - 1]
                recent_rjx = RJ[i]
                if COPY_OF_ST[i][1] != len(ROUTING[COPY_OF_ST[i][0] - 1]):
                    if ready_time > recent_rjx:
                        COPY_OF_CJ[i] = ready_time
                    else :
                        COPY_OF_CJ[i] = recent_rjx
            # Jika tidak ada, lakukan pembaharuan dengan nilai yang ada di mesin
            # Mengingat tidak ada job yang saling overlap
            else :
                if (COPY_OF_CJ[i] <= MESIN[0][COPY_OF_ST[i][2] - 1]):
                    COPY_OF_CJ[i] = MESIN[0][COPY_OF_ST[i][2] - 1]
        except:
            # Exception handling, skip jika tidak memenuhi kondisi diatas
            continue
        
    print("cek cj st 4", CJ, COPY_OF_CJ, ST)
        
    # i. Pembahruan terhadap nilai cj berdasar pemrosesan COPY_OF_CJ dan COPY_OF_ST
    # dilakukan hanya jika panjang keduanya sudah beda (akibat proses penghapusan)
    if (len(CJ) < len(COPY_OF_CJ)):
        for i in range(len(COPY_OF_CJ) - 1, -1, -1):
            # Proses penyesuaian dengan cj yang sudah baru dengan menghapus
            if i in index_job and COPY_OF_ST[i][1] == len(ROUTING[COPY_OF_ST[i][0] - 1]):
                COPY_OF_CJ.pop(i)
            else :
                continue
            
    print("cek cj st 5", CJ, COPY_OF_CJ, ST)
    
    # Penyalinan kembali nilai cj yang telah diperbaharui
    CJ = COPY_OF_CJ
    
    print("fin cj", CJ)
    
    # j. Pembaharuan terhadap nilai rj
    RJ = [0 for i in range(len(ST))]
    for i in range (len(ST)):
        RJ[i] = CJ[i] + TJ[i]           

    # k. Pengembalian nilai ST apakah sudah kosong (semua job sudah diproses)
    return ST

# 5. Melakukan pencetakan form hasil pemrosesan ke terminal
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
    
# 6. Program utama
if __name__ == '__main__':
    # xx. Membaca data
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

    # e. Melakukan pemrosesan pembuatan jadwal
    # Proses selesai dilaksanakan jika semua job selesai terjadwal
    print("Pemrosesan sedang dilakukan...")
    print("===== initial check ======")
    print("mesin ", MESIN)
    print("processing_time ", PROCESSING_TIME)
    print("routing ", ROUTING)
    print("CJ", CJ)
    print("TJ", TJ)
    print("RJ", RJ)
    print("ST", ST)
    print("----lesgo-----")
    while do_genetic_algo() != []:
        print("===== initial check ======")
        print("mesin ", MESIN)
        print("processing_time ", PROCESSING_TIME)
        print("routing ", ROUTING)
        print("CJ", CJ)
        print("TJ", TJ)
        print("RJ", RJ)
        print("ST", ST)
        print("----lesgo-----")
        pass
    
    # f. Semua job seledai dan hasil dicetak pada terminal
    print('\n---- Semua job telah selesai ----')
    print_schedule()
    

input("\nPress Enter to Exit")