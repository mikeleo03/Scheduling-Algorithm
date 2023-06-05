# Implementasi Algoritma Penjadwalan Genetic-Algorithm
# 1. Impor modul eksternal
import csv

# 2. Definisi variabel global
ROUTING = []
PROCESSING_TIME = []
MESIN = []
JOB_DONE = []
SCHEDULE = []
CJ = []
TJ = []
RJ = []
ST = []

# 3. Prosedur untuk melakukan pembacaan data dari file
def read_data():
    # Menggunakan variabel global
    global ROUTING, PROCESSING_TIME, MESIN, CJ, TJ, RJ, ST
    print("============   PEMILIHAN FOLDER   ============")
    folder = input("Masukkan nama folder yang akan dianalisis\n[Gunakan test2 dan test3 sebagai contoh]\n>> ")
    print("\n=============   PEMBACAAN DATA   =============")
    print("Sedang membaca data...")

    # Pembacaan data mesin dari file dan exception handling
    try:
        file = folder + "/Mesin.txt"
        mesin_file = open(file, "r")
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
            file = folder + f"/Job{j + 1}_Time.txt"
            time_file = open(file, "r")
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
            file = folder + f"/Job{j + 1}_Routing.txt"
            routing_file = open(file, "r")
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
    
    # Pendefinisian kondisi awal
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
    
    print("Kondisi awal pemrosesan telah siap diproses")

# 4. Prosedur Eksekusi
def do_genetic_algo(count):
    # xx. Menggunakan variabel global
    global MESIN, JOB_DONE, SCHEDULE, CJ, TJ, RJ, ST
    
    # a. Inisiasi senarai temporari
    temp_list = []
    
    # b. Melakukan pendataan index dari CJ untuk diproses lebih lanjut
    index_c_in_cj = [i for i in range(len(CJ))]

    # c. Deklarasi senarai mesin sebagai penampung daftar mesin yang akan digunakan
    machine_list = []  # machine list

    # d. Lakukan penyalinan nilai CJ pada COPY_OF_CJ 
    # sehingga nilainya tidak berubah setelah pemrosesan
    COPY_OF_CJ = [i for i in CJ]
    
    # Mengisi index mesin dengan nilai ST[i][2]
    for i in index_c_in_cj :
        machine_list.append(ST[i][2])
    
    # e. Lakukan pemrosesan terhadap nilai semua index pada COPY_OF_CJ, ST, dan MESIN
    for i in index_c_in_cj:
        job = ST[i][0]
        # Kalo mesinnya kosong, atau bisa selesai lebih cepat, masukin di
        # tempat yang memungkinkan, proses genetikasi
        # Mesin 1-4 bisa kerja paralel, jadi bisa switch
        if (ST[i][2] >= 1 and ST[i][2] <= 4):
            # Menerima nilai minimum dari setiap mesin pada rentang 1-4
            minimum = MESIN[0][0]
            idx_mesin = 0
            for j in range (4):
                if (minimum > MESIN[0][j]):
                    idx_mesin = j
                    minimum = MESIN[0][j]
            
            # Jika ternyata lebih efektif di mesin lain, switch ke mesin tersebut
            if (MESIN[0][ST[i][2] - 1] > minimum):
                ST[i] = [job, ST[i][1], idx_mesin + 1]      # Ubah nilai ST
                hinggap = idx_mesin + 1                             # Inisiasi nilai pembanding
                temp_list.append(ST[i])                             # Masukkan dalam senarai solusi
            # Jika ternyata tidak, maka 
            else :
                hinggap = ST[i][2]          # Inisialisasi nilai pembanding
                temp_list.append(ST[i])     # Langsung saja masukkan pada senarai solusi
            
            # Selanjutnya pemrosesan terhadap nilai mesin
            # Jika ini bukan pemrosesan pertama, lakukan perbandingan antara panjang job sebelumnya
            # dengan nilai kesediaan mesin yang akan dihinggapi/diswitch
            if (count > 1):
                nums1 = CJ[i]                   # Nilai job sebelumnya
                nums2 = MESIN[0][hinggap - 1]   # Nilai kesediaan mesin
                # Untuk setiap nilai yang lebih besar
                if nums1 > nums2:
                    # Lakukan pengubahan nilai mesin menjadi yang terbesar
                    MESIN[0][ST[i][2] - 1] = nums1 
                    # Menambahkan nilai mesin dengan waktu permosesan                                  
                    MESIN[0][ST[i][2] - 1] += PROCESSING_TIME[job - 1][ST[i][1] - 1]
                    # Mengubah nilai COPY_OF_CJ dengan nilai terbesar yang didefinisikan
                    COPY_OF_CJ[i] = nums1
                # Hal yang sama juga dilakukan jika komponen yang lebih besar adalah nilai yang lain
                else :
                    MESIN[0][ST[i][2] - 1] = nums2
                    MESIN[0][ST[i][2] - 1] += PROCESSING_TIME[job - 1][ST[i][1] - 1]
                    COPY_OF_CJ[i] = nums2
            # Akan tetapi jika ini adalah putaran pertama
            # Maka cukup tambahkan nilai mesin saja
            else :
                nums1 = CJ[i]
                nums2 = MESIN[0][hinggap - 1]
                MESIN[0][ST[i][2] - 1] += PROCESSING_TIME[job - 1][ST[i][1] - 1]
                COPY_OF_CJ[i] = nums2
        
        # Mesin 5-6 adalah mesin yang sama
        # Maka dapat menerapkan skema yang sama seperti mesin 1-4 diatas    
        elif (ST[i][2] >= 5 and ST[i][2] <= 6):
            # Section penentuan mesin yang lebih efektif
            minimum = MESIN[0][4]
            idx_mesin = 4
            for j in range (4, 5):
                if (minimum > MESIN[0][j]):
                    idx_mesin = j
                    minimum = MESIN[0][j]
            
            # Jika ternyata lebih efektif di mesin lain, switch ke mesin tersebut      
            if (MESIN[0][ST[i][2] - 1] > minimum):
                ST[i] = [job, ST[i][1], idx_mesin + 1]
                hinggap = idx_mesin + 1
                temp_list.append(ST[i])
            else :
                hinggap = ST[i][2]
                temp_list.append(ST[i])
            
            # Pemrosesan terhadap nilai mesin
            if (count > 1):
                nums1 = CJ[i]
                nums2 = MESIN[0][hinggap - 1]
                if nums1 > nums2:
                    MESIN[0][ST[i][2] - 1] = nums1
                    MESIN[0][ST[i][2] - 1] += PROCESSING_TIME[job - 1][ST[i][1] - 1]
                    COPY_OF_CJ[i] = nums1
                else :
                    MESIN[0][ST[i][2] - 1] = nums2
                    MESIN[0][ST[i][2] - 1] += PROCESSING_TIME[job - 1][ST[i][1] - 1]
                    COPY_OF_CJ[i] = nums2
            else :
                nums1 = CJ[i]
                nums2 = MESIN[0][hinggap - 1]
                MESIN[0][ST[i][2] - 1] += PROCESSING_TIME[job - 1][ST[i][1] - 1]
                COPY_OF_CJ[i] = nums2
        
        # Karena mesin 7 berbeda sendiri, lakukan pemrosesan secara normal
        else :                
            temp_list.append(ST[i])
                
    # Sekarang temp_list isinya job yang mau dijalankan (dalam sebuah senarai)
    retval = temp_list
        
    # f. Melakukan indexing terhadap jadwal yang ada pada retval
    # Khususnya terhadap senarai job, instance, dan mesin
    job = []
    instance = []
    machine = []
    for i in range (len(retval)):
        job.append(retval[i][0])
        instance.append(retval[i][1])
        machine.append(retval[i][2])
        
    # Melakukan pengisian senarai job_on_ST berdasar semua nilai job pada ST
    job_on_ST = []
    for i in range (len(ST)):
        job_on_ST.append(ST[i][0])
    
    # g. Pendefinisian index_job berdasar nilai setiap elemen pada job_on_ST pada job
    index_job = [job_on_ST.index(value) for value in job]
    
    # h. Mengubah nilai CJ sebelum dimasukkan pada daftar SCHEDULE
    for i in range(len(ST)):
        try:
            # Jika nilai iterator berada pada index_job,
            # maka update dengan nilai CJ dengan nilai COPY_OF_CJ yang telah dimodifikasi
            # dengan nilai TJ yang telah dideklarasikan di awal oleh setiap proses pada mesin
            if i in index_job:
                CJ[i] = COPY_OF_CJ[i] + TJ[i]
            # Jika tidak ada, lakukan pembaharuan dengan nilai yang ada di mesin
            # Mengingat tidak ada job yang saling overlap
            else :
                if (CJ[i] <= MESIN[0][ST[i][2] - 1]):
                    CJ[i] = MESIN[0][ST[i][2] - 1]
        except:
            # Exception handling, skip jika tidak memenuhi kondisi diatas
            continue
        
    # i. Memasukkan semua proses diatas ke SCHEDULE
    for value in job:
        i = job_on_ST.index(value)
        SCHEDULE.append([ST[i][0], ST[i][1], ST[i][2], COPY_OF_CJ[i], CJ[i]])
        # Jika sudah tidak ada lagi instance pada job tersebut
        # Maka masukkan pada senarai JOB_DONE
        if ST[i][1] == len(ROUTING[ST[i][0] - 1]):
            JOB_DONE.append([ST[i][0], RJ[i]])
    
    # j. Melakukan perubahan terhadap nilai isi MESIN, TJ, dan ST
    list_tidak_lewat = []      
    for i in index_job:
        # Memperbaharui nilai TJ di setiap index_job
        # Jika nilai TJ masih bisa diupdate, update
        if (ST[i][1] < len(PROCESSING_TIME[ST[i][0] - 1])) :
            TJ[i] = PROCESSING_TIME[ST[i][0] - 1][ST[i][1]]
        # Jika tidak, maka masukkan indeks pada senarai tidak lewat
        else :
            list_tidak_lewat.append(i)

        # Memperbaharui nilai ST di setiap index_job
        if (ST[i][1] < len(ROUTING[ST[i][0] - 1])) :
            ST[i] = [ST[i][0], ST[i][1] + 1, ROUTING[ST[i][0] - 1][ST[i][1]]]
    
    # k. Menghapus elemen yang sudah tidak ada di dalam TJ, ST, dan TJ
    # bias untuk membantu skema penghapusan berdasar indeks
    bias = 0   
    for i in list_tidak_lewat:
        TJ.pop(i - bias)
        ST.pop(i - bias)
        CJ.pop(i - bias)
        bias += 1
    
    # l. Pembaharuan terhadap nilai RJ
    RJ = [0 for i in range(len(ST))]
    for i in range (len(ST)):
        RJ[i] = CJ[i] + TJ[i]           

    # m. Pengembalian nilai ST apakah sudah kosong (semua job sudah diproses)
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
def main():
    # xx. Membaca data
    read_data()

    # a. Melakukan pemrosesan pembuatan jadwal
    # Proses selesai dilaksanakan jika semua job selesai terjadwal
    print("\nPemrosesan sedang dilakukan...")
    count = 1  # Instansiasi untuk menunjukkan jumlah iterasi yang telah dilakukan
    while do_genetic_algo(count) != []:
        count += 1
        pass
    
    # b. Semua job seledai dan hasil dicetak pada terminal
    print("\n============   HASIL PEMROSESAN   ============")
    print("Berikut adalah hasil pemrosesan penyusunan jadwal :\n")
    print_schedule()
    
    input("\nTekan Enter untuk keluar dari program")