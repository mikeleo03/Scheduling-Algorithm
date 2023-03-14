# Implementasi Algoritma Penjadwalan Non-delay
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
        mesin_file = open(f"test2/Mesin.txt", "r")
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
            time_file = open(f"test2/Job{j + 1}_Time.txt", "r")
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
            routing_file = open(f"test2/Job{j + 1}_Routing.txt", "r")
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
def state_check():
    # xx. Menggunakan variabel global
    global MESIN, JOB_DONE, SCHEDULE, CJ, TJ, RJ, ST

    # a. Mengambil nilai cj terkecil dari data masukan, job dengan cj terkecil akan diproses duluan
    min_c = min(CJ)
    
    # b. Inisiasi senarai temporari
    temp_list = []
    
    # c. Kalau misal ada lebih dari 1 yang punya nilai minimum, digunakan skema penanganan
    if CJ.count(min_c) > 1:
        # Inisiasi senarai yang berisi semua job dengan nilai min_c
        index_c_in_cj = [i for i in range(len(CJ)) if CJ[i] == min_c]

        # Cek nilai rj dan pilih yang mempunyai nilai rj terkecil
        # Prioritaskan yang jumlah operasinya masih banyak
        machine_list = []  # machine list

        # Isi list dengan semua data yang ada di index_c_in_cj
        for i in index_c_in_cj:
            # Kalau belum ada di machine list, tambahkan
            if len(temp_list) == 0 or ST[i][2] not in machine_list:
                temp_list.append(ST[i])
                machine_list.append(ST[i][2])
            # Kalau sudah ada, lakukan filtering sesuai kriteria diatas
            elif ST[i][2] in machine_list:
                index_mac = machine_list.index(ST[i][2])
                # Prioritas nilai rj
                if (RJ[i] < RJ[ST.index(temp_list[index_mac])]):
                    temp_list[index_mac] = ST[i]
                # Prioritas jumlah operasi
                elif ST[i][1] < temp_list[index_mac][1]:
                    temp_list[index_mac] = ST[i]
                    
        # Sekarang temp_list isinya job yang mau dijalankan (dalam sebuah list)
        retval = temp_list

    # Kalau tidak, kembalikan saja nilai st dari cj tersebut dalam sebuah list
    else:
        retval = [ST[CJ.index(min_c)]]
        
    # d. Melakukan indexing terhadap jadwal yang ada dan telah selesai
    for value in retval:
        i = ST.index(value)
        SCHEDULE.append([value[0], value[1], value[2], CJ[i], RJ[i]])
        if value[1] == 3:
            JOB_DONE.append([value[0], RJ[i]])

    # e. Lanjutan pemrosesan indexing untuk dikemas dalam senarai job dan machine
    index_job = [ST.index(i) for i in retval]
    index_mac = [i[2] - 1 for i in retval]
    
    # f. Melakukan penyalinan nilai st dan cj untuk digunakan lebih lanjut pada bagian bawah
    COPY_OF_ST = [i for i in ST]
    COPY_OF_CJ = [i for i in CJ]
    
    # g. Melakukan perubahan terhadap nilai isi mesin, tj dan st
    # bias untuk membantu skema penghapusan berdasar indeks
    bias = 0
    for i, j in zip(index_job, index_mac):
        # Memperbaharui nilai MESIN
        MESIN[0][j] = RJ[i]
        try:
            # Memperbaharui nilai tj
            TJ[i] = PROCESSING_TIME[ST[i][0] - 1][ST[i][1]]
            # Memperbaharui nilai st
            ST[i] = [ST[i][0], ST[i][1] + 1, ROUTING[ST[i][0] - 1][ST[i][1]]]
        except:
            # Exception handling jika tidak ada, maka saatnya dihapus
            TJ.pop(i - bias)
            ST.pop(i - bias)
            CJ.pop(i - bias)
            bias += 1

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
        
    # i. Pembahruan terhadap nilai cj berdasar pemrosesan COPY_OF_CJ dan COPY_OF_ST
    # dilakukan hanya jika panjang keduanya sudah beda (akibat proses penghapusan)
    if (len(CJ) < len(COPY_OF_CJ)):
        for i in range(len(COPY_OF_CJ) - 1, -1, -1):
            # Proses penyesuaian dengan cj yang sudah baru dengan menghapus
            if i in index_job and COPY_OF_ST[i][1] == len(ROUTING[COPY_OF_ST[i][0] - 1]):
                COPY_OF_CJ.pop(i)
            else :
                continue
    
    # Penyalinan kembali nilai cj yang telah diperbaharui
    CJ = COPY_OF_CJ
    
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
    while state_check() != []:
        pass
    
    # f. Semua job seledai dan hasil dicetak pada terminal
    print('\n---- Semua job telah selesai ----')
    print_schedule()

input("\nPress Enter to Exit")