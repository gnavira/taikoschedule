import os

# Direktori utama
base_dirs = ["notrun", "firstrun"]

# Kode lama yang ingin diganti
old_code = """async function doWrap(privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const amount = ethers.parseUnits('1.5', 'ether');
  const maxRetries = 3;
  let attempt = 0;
  const address = await wallet.getAddress();
  while (attempt < maxRetries) {
    try {
	  const nonce = await provider.getTransactionCount(address, "latest");
	  console.log(`Nonce: ${nonce}`);
      const gasPrice = await getRoundedGasPrice(provider, defaultgasPrice);
      const wrapContract = new ethers.Contract(WETH_CA, ABI, wallet);
      const txWrap = await wrapContract.deposit({ value: amount, gasPrice: gasPrice });
      const receipt = await txWrap.wait(1);
      return receipt.hash;
    } catch (error) {
      attempt++;
      const errorMessage = `[$timezone] Error executing Wrap transaction (Attempt ${attempt}/${maxRetries}): ${error.message}`;
      console.log(errorMessage.red);
      appendLog(errorMessage);
      if (attempt < maxRetries && (error.message.includes('insufficient funds') || 
          error.message.includes('nonce has already') ||
          error.message.includes('Gateway Timeout') ||
          error.message.includes('failed to detect network') ||
		  error.message.includes('request timeout') ||
		  error.message.includes('free limit') ||
          error.message.includes('missing revert data'))) {
        console.log(`Retrying transaction after delay...`);
        await delay(20000);
        await changeProvider();
      } else {
        throw error;
      }
    }
  }

  throw new Error(`Exceeded maximum retries for Wrap transaction.`);
}

async function doUnwrap(privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const amount = ethers.parseUnits('1.5', 'ether');
  const maxRetries = 3;
  let attempt = 0;
  const address = await wallet.getAddress();
  while (attempt < maxRetries) {
    try {
	  const nonce = await provider.getTransactionCount(address, "latest");
	  console.log(`Nonce: ${nonce}`);
      const gasPrice = await getRoundedGasPrice(provider, defaultgasPrice);
      const unwrapContract = new ethers.Contract(WETH_CA, ABI, wallet);
      const txUnwrap = await unwrapContract.withdraw(amount, { gasPrice: gasPrice });
      const receipt = await txUnwrap.wait(1);
      return receipt.hash;
    } catch (error) {
      attempt++;
      const errorMessage = `[$timezone] Error executing Unwrap transaction (Attempt ${attempt}/${maxRetries}): ${error.message}`;
      console.log(errorMessage.red);
      appendLog(errorMessage);
      if (attempt < maxRetries && (error.message.includes('insufficient funds') || 
          error.message.includes('nonce has already') ||
          error.message.includes('Gateway Timeout') ||
          error.message.includes('failed to detect network') ||
		  error.message.includes('request timeout') ||
		  error.message.includes('free limit') ||
          error.message.includes('missing revert data'))) {
        console.log(`Retrying transaction after delay...`);
        await delay(20000);
        await changeProvider();
      } else {
        throw error;
      }
    }
  }

  throw new Error(`Exceeded maximum retries for Unwrap transaction.`);
}

async function doSendEther(privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const recipients = recipientsaddress;
  const values = recipients.map(() => ethers.parseUnits('1.5', 'ether'));
  const sendContract = new ethers.Contract(SEND_CA, SEND_ABI, wallet);
  const maxRetries = 3;
  let attempt = 0;
  const address = await wallet.getAddress();
  while (attempt < maxRetries) {
    try {
	  const nonce = await provider.getTransactionCount(address, "latest");
	  console.log(`Nonce: ${nonce}`);
      const gasPrice = await getRoundedGasPrice(provider, defaultgasPrice);
      const txSendContract = await sendContract.multicall(recipients, values, { value: ethers.parseUnits('1.5', 'ether'), gasPrice: gasPrice });
      const receipt = await txSendContract.wait(1);
      return receipt.hash;
    } catch (error) {
      attempt++;
      const errorMessage = `[$timezone] Error executing Send ETH transaction (Attempt ${attempt}/${maxRetries}): ${error.message}`;
      console.log(errorMessage.red);
      appendLog(errorMessage);
      if (attempt < maxRetries && (error.message.includes('insufficient funds') || 
          error.message.includes('nonce has already') ||
          error.message.includes('Gateway Timeout') ||
          error.message.includes('failed to detect network') ||
		  error.message.includes('request timeout') ||
		  error.message.includes('free limit') ||
          error.message.includes('missing revert data'))) {
        console.log(`Retrying transaction after delay...`);
        await delay(20000);
        await changeProvider();
      } else {
        throw error;
      }
    }
  }

  throw new Error(`Exceeded maximum retries for Send ETH transaction.`);
}"""
# Kode baru yang akan menggantikan kode lama
new_code = """async function doWrap(privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const amount = ethers.parseUnits('1.5', 'ether');
  const maxRetries = 3;
  let attempt = 0;
  const address = await wallet.getAddress();
  while (attempt < maxRetries) {
    try {
	  const nonce = await provider.getTransactionCount(address, "latest");
	  console.log(`Nonce: ${nonce}`);
      const gasPrice = await getRoundedGasPrice(provider, defaultgasPrice);
      const wrapContract = new ethers.Contract(WETH_CA, ABI, wallet);
      const txWrap = await wrapContract.deposit({ value: amount, gasPrice: gasPrice, nonce: nonce});
      const receipt = await txWrap.wait(1);
      return receipt.hash;
    } catch (error) {
      attempt++;
      const errorMessage = `[$timezone] Error executing Wrap transaction (Attempt ${attempt}/${maxRetries}): ${error.message}`;
      console.log(errorMessage.red);
      appendLog(errorMessage);
      if (attempt < maxRetries && (error.message.includes('insufficient funds') || 
          error.message.includes('nonce has already') ||
          error.message.includes('Gateway Timeout') ||
          error.message.includes('failed to detect network') ||
		  error.message.includes('request timeout') ||
		  error.message.includes('free limit') ||
          error.message.includes('missing revert data'))) {
        console.log(`Retrying transaction after delay...`);
        await delay(20000);
        await changeProvider();
      } else {
        throw error;
      }
    }
  }

  throw new Error(`Exceeded maximum retries for Wrap transaction.`);
}

async function doUnwrap(privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const amount = ethers.parseUnits('1.5', 'ether');
  const maxRetries = 3;
  let attempt = 0;
  const address = await wallet.getAddress();
  while (attempt < maxRetries) {
    try {
	  const nonce = await provider.getTransactionCount(address, "latest");
	  console.log(`Nonce: ${nonce}`);
      const gasPrice = await getRoundedGasPrice(provider, defaultgasPrice);
      const unwrapContract = new ethers.Contract(WETH_CA, ABI, wallet);
      const txUnwrap = await unwrapContract.withdraw(amount, { gasPrice: gasPrice, nonce: nonce});
      const receipt = await txUnwrap.wait(1);
      return receipt.hash;
    } catch (error) {
      attempt++;
      const errorMessage = `[$timezone] Error executing Unwrap transaction (Attempt ${attempt}/${maxRetries}): ${error.message}`;
      console.log(errorMessage.red);
      appendLog(errorMessage);
      if (attempt < maxRetries && (error.message.includes('insufficient funds') || 
          error.message.includes('nonce has already') ||
          error.message.includes('Gateway Timeout') ||
          error.message.includes('failed to detect network') ||
		  error.message.includes('request timeout') ||
		  error.message.includes('free limit') ||
          error.message.includes('missing revert data'))) {
        console.log(`Retrying transaction after delay...`);
        await delay(20000);
        await changeProvider();
      } else {
        throw error;
      }
    }
  }

  throw new Error(`Exceeded maximum retries for Unwrap transaction.`);
}

async function doSendEther(privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const recipients = recipientsaddress;
  const values = recipients.map(() => ethers.parseUnits('1.5', 'ether'));
  const sendContract = new ethers.Contract(SEND_CA, SEND_ABI, wallet);
  const maxRetries = 3;
  let attempt = 0;
  const address = await wallet.getAddress();
  while (attempt < maxRetries) {
    try {
	  const nonce = await provider.getTransactionCount(address, "latest");
	  console.log(`Nonce: ${nonce}`);
      const gasPrice = await getRoundedGasPrice(provider, defaultgasPrice);
      const txSendContract = await sendContract.multicall(recipients, values, { value: ethers.parseUnits('1.5', 'ether'), gasPrice: gasPrice, nonce: nonce });
      const receipt = await txSendContract.wait(1);
      return receipt.hash;
    } catch (error) {
      attempt++;
      const errorMessage = `[$timezone] Error executing Send ETH transaction (Attempt ${attempt}/${maxRetries}): ${error.message}`;
      console.log(errorMessage.red);
      appendLog(errorMessage);
      if (attempt < maxRetries && (error.message.includes('insufficient funds') || 
          error.message.includes('nonce has already') ||
          error.message.includes('Gateway Timeout') ||
          error.message.includes('failed to detect network') ||
		  error.message.includes('request timeout') ||
		  error.message.includes('free limit') ||
          error.message.includes('missing revert data'))) {
        console.log(`Retrying transaction after delay...`);
        await delay(20000);
        await changeProvider();
      } else {
        throw error;
      }
    }
  }

  throw new Error(`Exceeded maximum retries for Send ETH transaction.`);
}"""

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
