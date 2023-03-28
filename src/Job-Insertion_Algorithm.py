# Implementasi Algoritma Penjadwalan Job-Insertion
# 1. Impor modul eksternal
import csv
import copy

# 2. Definisi variabel global
SCHEDULE = []
PROCESSING_TIME = []
ROUTING = []
DUE_DATES = []
MESIN = []

# 3. Prosedur untuk melakukan pembacaan data dari file
def read_data():
    global SCHEDULE, ROUTING, PROCESSING_TIME, MESIN, DUE_DATES
    print("Sedang membaca data...")
    
    try:
        schedule_file = open("test2/Jadwal.txt", "r")
    except:
        print("File Jadwal.txt tidak ditemukan!")
        exit()
        
    schedule_data = csv.reader(schedule_file)
    
    for row in schedule_data:
        for i in range(len(row)):
            row[i] = float(row[i])
            if row[i] % 1.0 == 0:
                row[i] = int(row[i])
        SCHEDULE.append(row)

    try:
        due_date_file = open("test2/Due_Dates.txt", "r")
    except:
        print("File Due_Dates.txt tidak ditemukan!")
        exit()
        
    due_date_data = csv.reader(due_date_file)
    
    for row in due_date_data:
        for i in range(len(row)):
            row[i] = float(row[i])
            if row[i] % 1.0 == 0:
                row[i] = int(row[i])
        DUE_DATES = row

    n_jobs = max(SCHEDULE, key=lambda x: x[0])[0] + 1
    for j in range(n_jobs):
        try:
            time_file = open(f"test2/Job{j + 1}_Time.txt", "r")
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
            routing_file = open(f"test2/Job{j + 1}_Routing.txt", "r")
        except:
            print(f"File Job{j + 1}_Routing.txt tidak ditemukan!")
            exit()
            
        routing_data = csv.reader(routing_file)
        for row in routing_data:
            for i in range(len(row)):
                row[i] = int(row[i])
                if row[i] % 1.0 == 0:
                    row[i] = int(row[i])
            ROUTING.append(row)
            
    try:
        mesin_file = open(f"test2/Mesin.txt", "r")
    except:
        print(f"File Mesin.txt tidak ditemukan!")
        exit()
        
    mesin_data = csv.reader(mesin_file)
    
    for row in mesin_data:
        for i in range(len(row)):
            row[i] = float(row[i])
            if row[i] % 1.0 == 0:
                row[i] = int(row[i])
        MESIN.append(row)

# 4. Fungsi yang digunakan untuk mendeteksi apakah ada proses yang terlambar
def is_all_on_time(lateness):
    for i in lateness:
        if i > 0:
            return False
    return True

# 5. Memetakan setiap indeks dari setiap operasi pada SCHEDULE
def get_schedule_mapping(schedule):
    global SCHEDULE, PROCESSING_TIME
    matrix = [[None for j in range(len(PROCESSING_TIME[0]))] for i in range(len(PROCESSING_TIME))]
    for i in range(len(SCHEDULE)):
        matrix[SCHEDULE[i][0] - 1][SCHEDULE[i][1] - 1] = i
    
    return matrix

# 6. Fungsi yang akan melakukan pendeteksian pada kemungkinan tabrakan job
def are_colliding(op1, op2):
    if (op1[3] > op2[3] and op1[3] < op2[4]) or (op1[4] > op2[3] and op1[4] < op2[4]) or (
        op2[3] > op1[3] and op2[3] < op1[4]) or (op2[4] > op1[3] and op2[4] < op1[4]) or (op2[3] <= op1[3]):
        return True, op1, op2
    else:
        return False, None, None
    
# 7. Fungsi yang melakukan penangan terhadap kemungkinan tabrakan
def handle_job_collisions(matrix):
    global SCHEDULE, ROUTING
    # Melakukan iterasi ke semua job yang ada pada ROUTING
    for job in range(len(ROUTING)):
        # Melakukan pengecekan terhadap semua pasangan operasi job
        for op1 in range(len(ROUTING[job])):
            for op2 in range(op1 + 1, len(ROUTING[job])):
                # Mengecek apakah ada job yang tabrakan
                collision = are_colliding(SCHEDULE[matrix[job][op1]], SCHEDULE[matrix[job][op2]])
                
                if collision[0]:
                    front = collision[1]
                    back = collision[2]
                    back_start = back[3]

                    # Melakukan penukaran pekerjaan dan pernyataan waktu
                    SCHEDULE[matrix[job][back[1] - 1]][3] = front[4]
                    SCHEDULE[matrix[job][back[1] - 1]][4] = front[4] + PROCESSING_TIME[job][back[1] - 1]

                    # Memindahkan job dengan operasi lebih tinggi ke belakang
                    afters = sorted(filter(lambda x: x[2] == back[2] and x[3] >= back_start, SCHEDULE), key=lambda x: x[3])
                    afters.remove(SCHEDULE[matrix[job][back[1] - 1]])
                    new_start = SCHEDULE[matrix[job][back[1] - 1]][4]

                    # Melakukan operasi terhadap job suksesif
                    if len(afters) > 0:
                        if afters[0][3] < new_start:
                            for i in range(len(afters)):
                                SCHEDULE[matrix[afters[i][0] - 1][afters[i][1] - 1]][3] = new_start
                                new_end = new_start + PROCESSING_TIME[afters[i][0] - 1][afters[i][1] - 1]
                                SCHEDULE[matrix[afters[i][0] - 1][afters[i][1] - 1]][4] = new_end

                                if i < len(afters) - 1:
                                    if SCHEDULE[matrix[afters[i + 1][0] - 1][afters[i + 1][1] - 1]][3] <= new_end:
                                        new_start = new_end
                                    else:
                                        new_start = afters[i + 1][3]

                    # Rekursi jika hal ini masih terjadi pada job lain dalam daftar pekerjaan
                    handle_job_collisions(matrix)

# 8. Melakukan pemindahan semua operasi ke kiri sebanyak mungkin
def compress_jobs(matrix):
    global SCHEDULE, ROUTING, MESIN
    # Melakukan pengecekan terhadap setiap mesin
    for m in range(len(MESIN[0])):
        # Mengambil semua elemen nilai mesin yang terurut berdasarkan waktu
        machine = sorted(filter(lambda x: x[2] == m + 1, SCHEDULE), key=lambda x: x[3])

        # Melakukan pengecekan terhadap semua operasi dalam mesin
        for i in range(len(machine)):
            # Mengambil semua nilai limit kiri yang mungkin
            limits = [MESIN[0][m]]
            if i > 0:
                limits.append(SCHEDULE[matrix[machine[i-1][0] - 1][machine[i-1][1] - 1]][4])
            if machine[i][1] > 1:
                limits.append(SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 2]][4])

            # Jika bisa ditukar, tukar!
            if SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 1]][3] not in limits:
                # Jika operasi pertama, shift ke paling kanan atau pindah dengan bagian kanannya
                if i == 0:
                    if machine[i][1] > 1:
                        new_start = max([MESIN[0][m], SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 2]][4]])
                    else:
                        new_start = MESIN[0][m]
                    
                    SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 1]][3] = new_start
                    SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 1]][4] = new_start + PROCESSING_TIME[machine[i][0] - 1][machine[i][1] - 1]
                
                # Untuk setiap operasi dalam mesin, pastikan pernah melakukan pemindahan ke kanan
                else:
                    if machine[i][1] > 1:
                        new_start = max([SCHEDULE[matrix[machine[i-1][0] - 1][machine[i-1][1] - 1]][4],
                                        SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 2]][4]])
                    else:
                        new_start = SCHEDULE[matrix[machine[i-1][0] - 1][machine[i-1][1] - 1]][4]
                    
                    SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 1]][3] = new_start
                    SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 1]][4] = new_start + PROCESSING_TIME[machine[i][0] - 1][machine[i][1] - 1]

# 9. Inti algoritma insertion job
def insert_job(pt=None, r=None):
    global SCHEDULE, PROCESSING_TIME, ROUTING, MESIN
    iterations = []

    # Assign a number to the job that is to be added
    new_job = len(PROCESSING_TIME)

    # Insert the job into the schedule array on the far right
    for op in range(len(ROUTING[-1])):
        last = max(filter(lambda a: a[2] == ROUTING[-1][op], SCHEDULE), key=lambda x: x[4])[4]
        
        if op > 0:
            last = max([last, max(filter(lambda a: a[2] == ROUTING[-1][op - 1], SCHEDULE), key=lambda x: x[4])[4]])
        
        new_last = last + PROCESSING_TIME[-1][op]
        SCHEDULE.append([new_job, op + 1, ROUTING[-1][op], last, new_last])

    # Get map of every index of every job-operation in the schedule (array order in schedule will not change to time)
    matrix = get_schedule_mapping(SCHEDULE)

    # Add as first iteration
    iterations.append([copy.deepcopy(SCHEDULE), new_last])

    # Make list for shifted jobs
    shifted_jobs = []

    # Iterate for all jobs, always picking the rightmost job that has not been shifted
    for i in range(new_job):
        job = max(filter(lambda a: a[0] - 1 not in shifted_jobs, SCHEDULE), key=lambda x: x[4])[0] - 1
        # Start shifting job to the left
        while True:
            # Shift first operation
            m = ROUTING[job][0]

            # Get schedule of of first operation
            current = SCHEDULE[matrix[job][0]]

            # Get schedule of first operation's predecessor
            try:
                before = max(filter(lambda a: a[2] == m and a[4] <= current[3], SCHEDULE), key=lambda x: x[4])
            except:
                before = [0, 0, 0, 0, 0]

            # In case they are consecutive, swap them
            if before != [0, 0, 0, 0, 0] and before[4] == current[3]:
                new_start = before[3]
                new_end = before[3] + PROCESSING_TIME[job][0]
                SCHEDULE[matrix[job][0]][3] = new_start
                SCHEDULE[matrix[job][0]][4] = new_end
                SCHEDULE[matrix[before[0] - 1][before[1] - 1]][3] = new_end
                SCHEDULE[matrix[before[0] - 1][before[1] - 1]][4] = new_end + PROCESSING_TIME[before[0] - 1][before[1] - 1]
            
            # In case they are not consecutive, shift first operation to the left
            else:
                new_start = before[4] if before != [0, 0, 0, 0, 0] else MESIN[0][current[2] - 1]
                new_end = new_start + PROCESSING_TIME[job][0]
                SCHEDULE[matrix[job][0]][3] = new_start
                SCHEDULE[matrix[job][0]][4] = new_end
                current = SCHEDULE[matrix[job][0]]
                
                # Shift other jobs after first operation to the left too
                afters = sorted(filter(
                    lambda a: a[2] == m and a[3] >= current[4], SCHEDULE), key=lambda x: x[3])
                
                new_start = new_end
                
                # Shifting
                for i in range(len(afters)):
                    if afters[i][1] - 1 > 0:
                        new_start = max([new_end, SCHEDULE[matrix[afters[i][0] - 1][afters[i][1] - 2]][4]])
                    
                    SCHEDULE[matrix[afters[i][0] - 1][afters[i][1] - 1]][3] = new_start
                    new_end = new_start + PROCESSING_TIME[afters[i][0] - 1][afters[i][1] - 1]
                    SCHEDULE[matrix[afters[i][0] - 1][afters[i][1] - 1]][4] = new_end
                    new_start = new_end
                
                # Compress all movable operations
                compress_jobs(matrix)

            # Handle job collisions after shifting first operation
            handle_job_collisions(matrix)

            # Add as iteration
            iterations.append([copy.deepcopy(SCHEDULE), max(SCHEDULE, key=lambda x: x[4])[4]])

            # Shift every other operation
            for op in range(1, len(ROUTING[job])):
                while True:
                    # Get schedule of current and previous operation
                    current = SCHEDULE[matrix[job][op]]
                    previous = SCHEDULE[matrix[job][op - 1]]

                    # Get schedule of operation's predecessor
                    if current[3] == previous[4]:
                        break
                    try:
                        before = max(filter(lambda a: a[2] == ROUTING[job][op] and a[4] <= SCHEDULE[matrix[job][op]][3], SCHEDULE), key=lambda x: x[4])
                    except:
                        before = [0, 0, 0, 0, 0]

                    # If operation's predecessor ends earlier than previous operation of this job, shift to left until flush
                    if before == [0, 0, 0, 0, 0] or before[4] <= previous[4]:
                        new_start = previous[4] if before != [0, 0, 0, 0, 0] else MESIN[0][current[2] - 1]
                        new_end = new_start + PROCESSING_TIME[job][op]
                        SCHEDULE[matrix[job][op]][3] = new_start
                        SCHEDULE[matrix[job][op]][4] = new_end
                        current = SCHEDULE[matrix[job][op]]

                        # Shift other jobs after operation to the left too
                        afters = sorted(filter(lambda a: a[2] == ROUTING[job][op] and a[3] >= current[4], SCHEDULE), key=lambda x: x[3])
                        new_start = new_end

                        # Shifting
                        for i in range(len(afters)):
                            if afters[i][1] - 1 > 0:
                                new_start = max([new_end, SCHEDULE[matrix[afters[i][0] - 1][afters[i][1] - 2]][4]])
                            
                            SCHEDULE[matrix[afters[i][0] - 1][afters[i][1] - 1]][3] = new_start
                            new_end = new_start + PROCESSING_TIME[afters[i][0] - 1][afters[i][1] - 1]
                            SCHEDULE[matrix[afters[i][0] - 1][afters[i][1] - 1]][4] = new_end
                            new_start = new_end

                        # Compress all movable operations
                        compress_jobs(matrix)

                        # Handle job collisions after shifting operation
                        handle_job_collisions(matrix)

                        # Add as iteration
                        iterations.append([copy.deepcopy(SCHEDULE), max(SCHEDULE, key=lambda x: x[4])[4]])

                        # Move on to next operation
                        break
                    # If operation's predecessor ends later than previous operation of this job, shift to the previous operation
                    else:
                        # If operation's predecessor ends later than previous operation of this job, shift to left until flush with predecessor
                        if before[4] != current[3]:
                            new_start = before[4]
                            new_end = before[4] + PROCESSING_TIME[job][op]
                            SCHEDULE[matrix[job][op]][3] = new_start
                            SCHEDULE[matrix[job][op]][4] = new_end
                            current = SCHEDULE[matrix[job][op]]

                            # Shift other jobs after operation to the left too
                            afters = sorted(filter(lambda a: a[2] == ROUTING[job][op] and a[3] >= current[4], SCHEDULE), key=lambda x: x[3])
                            new_start = new_end

                            # Shifting
                            for i in range(len(afters)):
                                if afters[i][1] - 1 > 0:
                                    new_start = max([new_end, SCHEDULE[matrix[afters[i][0] - 1][afters[i][1] - 2]][4]])
                                
                                SCHEDULE[matrix[afters[i][0] - 1][afters[i][1] - 1]][3] = new_start
                                new_end = new_start + PROCESSING_TIME[afters[i][0] - 1][afters[i][1] - 1]
                                SCHEDULE[matrix[afters[i][0] - 1][afters[i][1] - 1]][4] = new_end
                                new_start = new_end

                            # Compress all movable operations
                            compress_jobs(matrix)

                        # If operation's predecessor ends at the same time as previous operation of this job, swap them
                        else:
                            new_start = before[3]
                            new_end = before[3] + PROCESSING_TIME[job][op]
                            SCHEDULE[matrix[job][op]][3] = new_start
                            SCHEDULE[matrix[job][op]][4] = new_end
                            SCHEDULE[matrix[before[0] - 1][before[1] - 1]][3] = new_end
                            SCHEDULE[matrix[before[0] - 1][before[1] - 1]][4] = new_end + PROCESSING_TIME[before[0] - 1][before[1] - 1]

                        # Handle job collisions after shifting operation
                        handle_job_collisions(matrix)

                        # Add as iteration
                        iterations.append([copy.deepcopy(SCHEDULE), max(SCHEDULE, key=lambda x: x[4])[4]])

            # Detect finished job shifting
            if SCHEDULE[matrix[job][0]][3] == MESIN[0][SCHEDULE[matrix[job][0]][2] - 1]:
                break

        # Add job to shifted jobs
        shifted_jobs.append(job)

    # Return iterations
    return iterations                       

# 10. Print makeform and schedule to string form in the console
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

# 11. Print results of insertion and its accordance to given due dates
def print_results(iterations, due_dates):
    lateness = [[] for k in range(len(iterations))]
    
    for j in range(len(iterations)):
        for i in range(len(due_dates)):
            scenario = iterations[j]
            end = max(filter(lambda a: a[0] == i + 1, scenario[0]), key=lambda x: x[4])[4]
            lateness[j].append(end - due_dates[i])
    
    on_time = list(filter(lambda a: is_all_on_time(a[1]), enumerate(lateness)))

    print("\n---- HASIL SESUAI DUE DATE ----")
    for i in range(len(on_time)):
        print(f'\n---- Alternatif {i + 1} (Skenario {on_time[i][0]}) ----')
        print_schedule(iterations[on_time[i][0]][0], on_time[i][1])

    if len(on_time) == 0:
        iterations = sorted(enumerate(iterations), key=lambda x: x[1][1])
        for i in range(5):
            print(f'\n---- Alternatif {i + 1} (Skenario {iterations[i][0]}) ----')
            print_schedule(iterations[i][1][0], lateness[iterations[i][0]])
            
# 6. Program utama
if __name__ == '__main__':
    read_data()
    print("Data telah dibaca!")
    iterations = insert_job()
    print_results(iterations, DUE_DATES)

input("Press Enter to Exit")