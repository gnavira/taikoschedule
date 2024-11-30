import os

# Jalur folder utama
base_directory = "notrun"

# Iterasi melalui semua folder di dalam base_directory
for folder_number in range(1, 39):  # Folder bernomor 1 hingga 38
    folder_path = os.path.join(base_directory, str(folder_number))
    old_file_path = os.path.join(folder_path, "start.js")
    new_file_path = os.path.join(folder_path, "taiko.js")

    # Periksa apakah file start.js ada di folder
    if os.path.exists(old_file_path):
        try:
            # Ganti nama file
            os.rename(old_file_path, new_file_path)
            print(f"File '{old_file_path}' berhasil diganti menjadi '{new_file_path}'")
        except Exception as e:
            print(f"Terjadi kesalahan saat mengganti nama file di folder '{folder_path}': {e}")
    else:
        print(f"File 'start.js' tidak ditemukan di folder '{folder_path}'")
