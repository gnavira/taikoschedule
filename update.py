import os

# Direktori utama
base_directory = "."

# Kode lama yang ingin dihapus
old_function = """function appendLog(message) {
  fs.appendFileSync('log.txt', message + '
');
}"""

# Kode baru untuk menggantikan
new_function = """function appendLog(message) {
  fs.appendFileSync('log.txt', message + '\\n');
}"""

# Fungsi untuk mengganti fungsi lama dengan yang baru
def replace_append_log(file_path):
    try:
        # Membuka dan membaca isi file
        with open(file_path, "r") as file:
            file_content = file.read()

        # Periksa apakah fungsi lama ada di dalam file
        if old_function in file_content:
            # Ganti fungsi lama dengan fungsi baru
            file_content = file_content.replace(old_function, new_function)

            # Menulis kembali file dengan konten yang diperbarui
            with open(file_path, "w") as file:
                file.write(file_content)

            print(f"File '{file_path}' berhasil diperbarui!")
        else:
            print(f"Fungsi lama tidak ditemukan di file '{file_path}'.")
    except Exception as e:
        print(f"Terjadi kesalahan saat memproses file '{file_path}': {e}")

# Iterasi melalui folder notrun dan firstrun
for parent_folder in ["notrun", "firstrun"]:
    for folder_number in range(1, 39):  # Folder 1 sampai 38
        folder_path = os.path.join(base_directory, parent_folder, str(folder_number))
        
        # Cek file di folder
        file_names = ["taiko.js", "taikorun.js"] if parent_folder == "firstrun" else ["taiko.js"]
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)

            # Periksa apakah file ada, lalu ganti kode
            if os.path.exists(file_path):
                replace_append_log(file_path)
            else:
                print(f"File '{file_path}' tidak ditemukan.")
