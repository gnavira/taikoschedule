import os

# Direktori utama
base_directory = "."

# Fungsi untuk menulis isi file dengan cron berbeda
def write_cron_to_file(file_path, hour, minute):
    try:
        # Format cron berdasarkan jam dan menit
        cron_code = f"""const job = new CronJob('{minute} {hour} * * *', runWrapandUnwrap, null, true, 'UTC');
console.log('Transaksi akan dijalankan setiap {hour:02d}:{minute:02d} UTC');
"""
        with open(file_path, "w") as file:
            file.write(cron_code)
        print(f"Cron berhasil ditulis ke file: {file_path}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menulis cron ke file '{file_path}': {e}")

# Iterasi melalui folder notrun dan firstrun
for parent_folder in ["notrun", "firstrun"]:
    hour, minute = 1, 0  # Mulai dari jam 01:00
    for folder_number in range(1, 39):  # Folder 1 sampai 38
        folder_path = os.path.join(base_directory, parent_folder, str(folder_number))
        
        # Tentukan file yang akan diubah
        file_name = "taiko.js" if parent_folder == "notrun" else "taikorun.js"
        file_path = os.path.join(folder_path, file_name)

        # Periksa apakah file ada
        if os.path.exists(file_path):
            write_cron_to_file(file_path, hour, minute)

            # Tambahkan 15 menit untuk file berikutnya
            minute += 15
            if minute >= 60:  # Jika menit melebihi 60, tambahkan 1 jam
                minute -= 60
                hour += 1
        else:
            print(f"File '{file_path}' tidak ditemukan.")
