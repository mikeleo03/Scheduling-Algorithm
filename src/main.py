# Implemenetasi program utama yang menyatukan algoritma penjadwalan
# 0. Mengimpor fungsionalitas dari masing-masing algoritma
import Genetic_Algorithm as ga
import Job_Insertion_Algorithm as ji
import Non_delay_Algorithm as nd

# 1. Program utama
if __name__ == '__main__':
    print("Selamat datang pada sistem algoritma penjadwalan")
    print("\n==========   PEMILIHAN ALGORITMA   ===========")
    print("Pilih algoritma yang ingin dijalankan :")
    print(" 1. Algoritma Penjadwalan Non-delay")
    print(" 2. Algoritma Job-Insertion")
    print(" 3. Algoritma Genetik (Genetic Algorithm)")
    print("Masukkan pilihan")
    nums = int(input(">> "))
    while (nums < 0 or nums > 3):
        print("Masukan Anda salah, ulangi!\n")
        print("Pilih algoritma yang ingin dijalankan :")
        print(" 1. Algoritma Penjadwalan Non-delay")
        print(" 2. Algoritma Job-Insertion")
        print(" 3. Algoritma Genetik (Genetic Algorithm)")
        print("Masukkan pilihan")
        nums = int(input(">> "))
    
    # Masukan pengguna sudah valid
    print(" ")
    if (nums == 1) :
        print(">>>>>   Algoritma Penjadwalan Non-delay   <<<<<")
        nd.main()
    elif (nums == 2):
        print(">>>>>>>     Algoritma Job-Insertion     <<<<<<<")
        ji.main()
    else :
        print(">>   Algoritma Genetik (Genetic Algorithm)   <<")
        ga.main()