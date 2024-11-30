import os

# Jalur folder utama
base_directory = "notrun"

# Kode yang ingin dihapus
code_to_remove = "const Timestamp() = moment().tz('Asia/Jakarta').format('HH:mm:ss [WIB] DD-MM-YYYY');"

# Iterasi melalui semua folder dan file
for folder_number in range(1, 39):  # Folder bernomor 1 hingga 38
    folder_path = os.path.join(base_directory, str(folder_number))
    file_path = os.path.join(folder_path, "taiko.js")  # Target file

    # Periksa apakah file ada
    if os.path.exists(file_path):
        try:
            # Membuka dan membaca isi file
            with open(file_path, "r") as file:
                file_content = file.read()

            # Periksa apakah kode ada di dalam file
            if code_to_remove in file_content:
                # Menghapus kode
                file_content = file_content.replace(code_to_remove, "")

                # Menulis ulang file tanpa kode tersebut
                with open(file_path, "w") as file:
                    file.write(file_content)

                print(f"Kode dihapus dari file: {file_path}")
            else:
                print(f"Kode tidak ditemukan di file: {file_path}")
        except Exception as e:
            print(f"Terjadi kesalahan saat memproses file '{file_path}': {e}")
    else:
        print(f"File 'taiko.js' tidak ditemukan di folder '{folder_path}'")
