import os

# Direktori utama
base_dirs = ["notrun", "firstrun"]

# Kode lama yang ingin diganti
old_code = """"""
# Kode baru yang akan menggantikan kode lama
new_code = """"""

# Fungsi untuk mencari dan mengganti kode di file
def replace_code_in_file(file_path, old_code, new_code):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Replaced code in {file_path}")
    else:
        print(f"No matching code found in {file_path}")

# Menjalankan penggantian pada setiap file start.js di subfolder 1-38
for base_dir in base_dirs:
    for i in range(1, 39):  # Folder dari 1 hingga 38
        folder_path = os.path.join(base_dir, str(i))
        file_path = os.path.join(folder_path, "start.js")
        
        if os.path.isfile(file_path):
            replace_code_in_file(file_path, old_code, new_code)
        else:
            print(f"File {file_path} does not exist.")
