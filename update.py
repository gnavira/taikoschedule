import os

# Direktori utama
base_dirs = ["notrun", "firstrun"]

# Kode lama yang ingin diganti

# Kode baru yang akan menggantikan kode lama
new_code = """async function getRoundedGasPrice(provider, defaultGasPrice) {
  try {
    // Mendapatkan data gas fee
    const feeData = await provider.getFeeData();
    let gasPrice = feeData.gasPrice;
    if (!gasPrice) throw new Error("Gas price tidak tersedia");
    let gasPriceInGwei = parseFloat(ethers.formatUnits(gasPrice, "gwei"));
    if (gasPriceInGwei < 0.15) {
      gasPriceInGwei = 0.15;
    } else {
      gasPriceInGwei = Math.ceil(gasPriceInGwei * 100) / 100;
    }
    const getRoundedGasPrice = ethers.parseUnits(gasPriceInGwei.toString(), "gwei");
    console.log(`Gas price: ${gasPriceInGwei} gwei`);
    return getRoundedGasPrice;

  } catch (error) {
    console.log(`Error mendapatkan gas price: ${error.message}. Menggunakan default gas price ${ethers.formatUnits(defaultGasPrice, "gwei")} gwei`);
    return defaultGasPrice;
  }
}
"""

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
