import os

# Direktori utama
base_directory = "."

# Template baru untuk kode dengan placeholder
job_template = """const job = new CronJob('{minute} {hour} * * *', runWrapandUnwrap, null, true, 'UTC');
console.log('Transaksi akan dijalankan setiap {hour}:{minute:02d} UTC');
"""

# Fungsi untuk mengganti jadwal dalam file
def update_schedule(file_path, hour, minute):
    try:
        # Membuat kode baru berdasarkan template
        new_content = job_template.format(hour=hour, minute=minute)
        
        # Membuka dan membaca isi file
        with open(file_path, "r") as file:
            file_content = file.read()

        # Mencari kode lama dan menggantinya dengan kode baru
        if "const job = new CronJob(" in file_content:
            start_index = file_content.find("const job = new CronJob(")
            end_index = file_content.find("console.log('Transaksi akan dijalankan setiap", start_index)
            if end_index != -1:
                # Menentukan bagian yang akan diganti
                end_index = file_content.find("');", end_index) + 3
                old_code = file_content[start_index:end_index]

                # Mengganti kode lama dengan kode baru
                file_content = file_content.replace(old_code, new_content)

                # Menulis kembali file
                with open(file_path, "w") as file:
                    file.write(file_content)

                print(f"File '{file_path}' berhasil diperbarui dengan waktu {hour}:{minute:02d} UTC!")
            else:
                print(f"Struktur kode tidak ditemukan di file '{file_path}'.")
        else:
            print(f"Kode 'const job = new CronJob' tidak ditemukan di file '{file_path}'.")
    except Exception as e:
        print(f"Terjadi kesalahan saat memproses file '{file_path}': {e}")

# Iterasi melalui folder firstrun
parent_folder = "firstrun"
hour = 1
minute = 0
for folder_number in range(1, 39):  # Folder 1 sampai 38
    folder_path = os.path.join(base_directory, parent_folder, str(folder_number))
    file_path = os.path.join(folder_path, "taikorun.js")

    # Periksa apakah file ada
    if os.path.exists(file_path):
        # Perbarui jadwal berdasarkan folder
        update_schedule(file_path, hour, minute)

        # Tambahkan 30 menit untuk folder berikutnya
        minute += 15
        if minute >= 60:
            minute -= 60
            hour += 1
    else:
        print(f"File '{file_path}' tidak ditemukan.")
