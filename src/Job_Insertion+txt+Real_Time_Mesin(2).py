import csv
import copy
# import pyrebase
# from datetime import datetime
# import time
# import calendar


# firebaseConfig = {"apiKey": "AIzaSyD3DASICtOhpQRuSDxCdhh8DQkuw97OrsA",
#                   "authDomain": "finalta-66e60.firebaseapp.com",
#                   "databaseURL": "https://finalta-66e60-default-rtdb.firebaseio.com",
#                   "projectId": "finalta-66e60",
#                   "storageBucket": "finalta-66e60.appspot.com",
#                   "messagingSenderId": "966705935989",
#                   "appId": "1:966705935989:web:a1fc7665b3db8c51e2aa3c",
#                   "measurementId": "G-TV9WKWW9BX"}

# firebase = pyrebase.initialize_app(firebaseConfig)

# db = firebase.database()

# now = datetime.now()
# epochtime = int(time.time())+25200
# date = now.strftime("%y/%m/%d")
# date1 = now.strftime("%y-%m-%d")
# # print(date1)

# a = date.split("/")
# result = calendar.weekday(int(a[0]), int(a[1]), int(a[2]))
# day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# hari = (day[result])
# # print(hari)

# dtt = (hari+","+date1)
# # print(dtt)

READY = [3, 1, 0]
# x = 1
# mesin = int(input("Masukkan jumlah mesin: "))
# while x < mesin+1:

#     tes1 = db.child(f"Mesin {x}", dtt).order_by_key().limit_to_last(1).get()
#     for test1 in tes1.each():
#         test1 = (test1.key())
#     # print(test1)
#     # print(Users2)

#     high_w1 = db.child(f"Mesin {x}", dtt, test1).order_by_key().equal_to("Epoch_High").get()
#     for high1 in high_w1.each():
#         high1 = (high1.val())
#         # print(Users)

#     est1 = db.child(f"Mesin {x}", dtt, test1).order_by_key().equal_to("Estimasi").get()
#     for estimasi1 in est1.each():
#         estimasi1 = (estimasi1.val())*3600
#         # print(Users3)

#     hasil1 = ((high1+estimasi1-epochtime)/3600)

#     cnt1 = db.child(f"Mesin {x}", dtt, test1).order_by_key().get()
#     if len(cnt1.val()) == 5:
#         p = 0
#     elif hasil1 <= 0:
#         p = 0
#     elif hasil1 > 0:
#         p = round(hasil1, 2)

#     READY.append(p)
#     x += 1
print("Ready time mesin: ")
print(READY)

# ----------------------------------------------------------------------------------------


SCHEDULE = []
PROCESSING_TIME = []
ROUTING = []
DUE_DATES = []


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


# Function to detect lateness
def is_all_on_time(lateness):
    for i in lateness:
        if i > 0:
            return False
    return True


# Print results of insertion and its accordance to given due dates
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


# Get map of every index of every job-operation in the schedule (arrays in the schedule will not change to time)
def get_schedule_mapping(schedule):
    global SCHEDULE, PROCESSING_TIME
    matrix = [[None for j in range(len(PROCESSING_TIME[0]))]
              for i in range(len(PROCESSING_TIME))]
    for i in range(len(SCHEDULE)):
        matrix[SCHEDULE[i][0] - 1][SCHEDULE[i][1] - 1] = i
    return matrix


# Function to detect collision between two operations
def are_colliding(op1, op2):
    if (op1[3] > op2[3] and op1[3] < op2[4]) or (op1[4] > op2[3] and op1[4] < op2[4]) or (
            op2[3] > op1[3] and op2[3] < op1[4]) or (op2[4] > op1[3] and op2[4] < op1[4]) or (op2[3] <= op1[3]):
        return True, op1, op2
    else:
        return False, None, None


# Handle all collisions in the schedule and fix them
def handle_job_collisions(matrix):
    global SCHEDULE, ROUTING
    # Check every job
    for job in range(len(ROUTING)):
        # Check every operation pairing of the job
        for op1 in range(len(ROUTING[job])):
            for op2 in range(op1 + 1, len(ROUTING[job])):
                # Check if the operations are colliding
                collision = are_colliding(SCHEDULE[matrix[job][op1]],
                                          SCHEDULE[matrix[job][op2]])
                if collision[0]:
                    front = collision[1]
                    back = collision[2]
                    back_start = back[3]

                    # Shift later operation to the right until flush
                    SCHEDULE[matrix[job][back[1] - 1]][3] = front[4]
                    SCHEDULE[matrix[job][back[1] - 1]][4] = front[4] + PROCESSING_TIME[job][back[1] - 1]

                    # Shift all jobs after the later operation to the right
                    afters = sorted(filter(lambda x: x[2] == back[2] and x[3] >= back_start, SCHEDULE), key=lambda x: x[3])
                    afters.remove(SCHEDULE[matrix[job][back[1] - 1]])
                    new_start = SCHEDULE[matrix[job][back[1] - 1]][4]

                    # Shifting of afters only occurs for successive operations, as if pushing blocks to the right
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

                    # Recursion in case more collisions happen from shifting
                    handle_job_collisions(matrix)


# Shift all movable operations to the left as much as possible
def compress_jobs(matrix):
    global SCHEDULE, ROUTING, READY
    # Check every machine
    for m in range(len(READY)):
        # Get all operations in machine ordered by time
        machine = sorted(filter(lambda x: x[2] == m + 1, SCHEDULE), key=lambda x: x[3])

        # Check every operation in the machine
        for i in range(len(machine)):
            # Get the possible left-side limits of moving the operation
            limits = [READY[m]]
            if i > 0:
                limits.append(SCHEDULE[matrix[machine[i-1][0] - 1][machine[i-1][1] - 1]][4])
            if machine[i][1] > 1:
                limits.append(SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 2]][4])

            # If operation can be shifted further, shift it
            if SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 1]][3] not in limits:
                # If operation is the first in the machine, shift it to the leftmost position or flush to the previous operation of the job
                if i == 0:
                    if machine[i][1] > 1:
                        new_start = max([READY[m], SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 2]][4]])
                    else:
                        new_start = READY[m]
                    SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 1]][3] = new_start
                    SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 1]][4] = new_start + \
                        PROCESSING_TIME[machine[i][0] - 1][machine[i][1] - 1]
                # For every other operation in the machine, shift it flush to the previous operation of the job or to the operation on the left
                else:
                    if machine[i][1] > 1:
                        new_start = max([SCHEDULE[matrix[machine[i-1][0] - 1][machine[i-1][1] - 1]][4],
                                        SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 2]][4]])
                    else:
                        new_start = SCHEDULE[matrix[machine[i-1][0] - 1][machine[i-1][1] - 1]][4]
                    SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 1]][3] = new_start
                    SCHEDULE[matrix[machine[i][0] - 1][machine[i][1] - 1]][4] = new_start + \
                        PROCESSING_TIME[machine[i][0] - 1][machine[i][1] - 1]


# Job insertion algorithm, inserts a job with processing time (pt) and routing (r) into the schedule array
def insert_job(pt=None, r=None):
    global SCHEDULE, PROCESSING_TIME, ROUTING, READY
    iterations = []

    # Assign a number to the job that is to be added
    new_job = len(PROCESSING_TIME)

    # Insert the job into the schedule array on the far right
    for op in range(len(ROUTING[-1])):
        last = max(filter(lambda a: a[2] == ROUTING[-1][op], SCHEDULE),
                   key=lambda x: x[4])[4]
        if op > 0:
            last = max([
                last,
                max(filter(lambda a: a[2] == ROUTING[-1][op - 1], SCHEDULE),
                    key=lambda x: x[4])[4]
            ])
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
                new_start = before[4] if before != [0, 0, 0, 0, 0] else READY[current[2] - 1]
                new_end = new_start + PROCESSING_TIME[job][0]
                SCHEDULE[matrix[job][0]][3] = new_start
                SCHEDULE[matrix[job][0]][4] = new_end
                current = SCHEDULE[matrix[job][0]]
                # Shift other jobs after first operation to the left too
                afters = sorted(filter(
                    lambda a: a[2] == m and a[3] >= current[4], SCHEDULE),
                    key=lambda x: x[3])
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
                        before = max(filter(lambda a: a[2] == ROUTING[job][op] and a[4] <=
                                            SCHEDULE[matrix[job][op]][3], SCHEDULE), key=lambda x: x[4])
                    except:
                        before = [0, 0, 0, 0, 0]

                    # If operation's predecessor ends earlier than previous operation of this job, shift to left until flush
                    if before == [0, 0, 0, 0, 0] or before[4] <= previous[4]:
                        new_start = previous[4] if before != [0, 0, 0, 0, 0] else READY[current[2] - 1]
                        new_end = new_start + PROCESSING_TIME[job][op]
                        SCHEDULE[matrix[job][op]][3] = new_start
                        SCHEDULE[matrix[job][op]][4] = new_end
                        current = SCHEDULE[matrix[job][op]]

                        # Shift other jobs after operation to the left too
                        afters = sorted(filter(
                            lambda a: a[2] == ROUTING[job][op] and a[3] >= current[4], SCHEDULE),
                            key=lambda x: x[3])
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
                            afters = sorted(filter(
                                lambda a: a[2] == ROUTING[job][op] and a[3] >= current[4], SCHEDULE),
                                key=lambda x: x[3])
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
                            SCHEDULE[matrix[before[0] - 1][before[1] - 1]][4] = new_end + \
                                PROCESSING_TIME[before[0] - 1][before[1] - 1]

                        # Handle job collisions after shifting operation
                        handle_job_collisions(matrix)

                        # Add as iteration
                        iterations.append([copy.deepcopy(SCHEDULE), max(SCHEDULE, key=lambda x: x[4])[4]])

            # Detect finished job shifting
            if SCHEDULE[matrix[job][0]][3] == READY[SCHEDULE[matrix[job][0]][2] - 1]:
                break

        # Add job to shifted jobs
        shifted_jobs.append(job)

    # Return iterations
    return iterations


def read_data():
    global SCHEDULE, ROUTING, PROCESSING_TIME, READY, DUE_DATES
    print("Sedang membaca data...")
    try:
        schedule_file = open("test/Jadwal.txt", "r")
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
        due_date_file = open("Due_Dates.txt", "r")
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
                row[i] = int(row[i])
                if row[i] % 1.0 == 0:
                    row[i] = int(row[i])
            ROUTING.append(row)


if __name__ == '__main__':
    read_data()
    print("Data telah dibaca!")
    iterations = insert_job()
    print_results(iterations, DUE_DATES)

input("Press Enter to Exit")