import os

# Direktori utama
base_directory = "."

# Lokasi file test.js
test_file_path = os.path.join(base_directory, "test.js")

# Fungsi untuk membaca isi test.js
def read_test_file():
    try:
        with open(test_file_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file 'test.js': {e}")
        return None

# Fungsi untuk menyalin isi ke file target
def copy_content_to_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Isi 'test.js' berhasil disalin ke file: {file_path}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyalin isi ke file '{file_path}': {e}")

# Baca isi test.js
test_content = read_test_file()

# Periksa apakah isi berhasil dibaca
if test_content:
    # Iterasi melalui folder notrun dan firstrun
    for parent_folder in ["notrun", "firstrun"]:
        for folder_number in range(1, 39):  # Folder 1 sampai 38
            folder_path = os.path.join(base_directory, parent_folder, str(folder_number))
            
            # Cek file di folder
            file_name = "taiko.js" if parent_folder == "notrun" else "taikorun.js"
            file_path = os.path.join(folder_path, file_name)

            # Periksa apakah file ada, lalu salin isi test.js
            if os.path.exists(file_path):
                copy_content_to_file(file_path, test_content)
            else:
                print(f"File '{file_path}' tidak ditemukan.")
else:
    print("Gagal membaca isi 'test.js'.")
