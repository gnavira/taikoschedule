import os

# Direktori utama (root repository)
base_directory = "."

# Kode yang ingin dihapus
code_to_remove = "runWrapandUnwrap();"

# Fungsi untuk menghapus kode dari file
def remove_code(file_path, code_to_remove):
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

            print(f"Kode '{code_to_remove}' berhasil dihapus dari file: {file_path}")
        else:
            print(f"Kode '{code_to_remove}' tidak ditemukan di file: {file_path}")
    except Exception as e:
        print(f"Terjadi kesalahan saat memproses file '{file_path}': {e}")

# Iterasi melalui folder notrun
parent_folder = "notrun"
for folder_number in range(1, 77):  # Folder 1 sampai 38
    folder_path = os.path.join(base_directory, parent_folder, str(folder_number))
    file_path = os.path.join(folder_path, "taiko.js")

    # Periksa apakah file ada, lalu hapus kode
    if os.path.exists(file_path):
        remove_code(file_path, code_to_remove)
    else:
        print(f"File '{file_path}' tidak ditemukan.")
