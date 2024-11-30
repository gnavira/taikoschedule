const { ethers } = require('ethers');
const chains = require('./chains');
const provider = chains.mainnet.taiko.provider;
const changeProvider = chains.mainnet.taiko.changeRpcProvider;
const explorer = chains.mainnet.taiko.explorer;
const changeRpc = chains.mainnet.tempTaiko.changeRpcProvider;
const tempProvider = chains.mainnet.tempTaiko.provider;
const fs = require('fs');
const moment = require('moment-timezone');
const { displayHeader, delay } = require('./chains/utils/utils');
const PRIVATE_KEYS = JSON.parse(fs.readFileSync('privateKeys.json', 'utf-8'));
const { ABI, SEND_ABI } = require('./abi/abi');
const WETH_CA = '0xA51894664A773981C6C112C43ce576f315d5b1B6';
const SEND_CA = '0x2A5b0a407828b6Ca2E87e2e568CD8413fd5c24A1';
const recipientsaddress = JSON.parse(fs.readFileSync('recipients.json', 'utf8'));
const { CronJob } = require('cron');
const amountCheck = ethers.parseEther('0.5', 'ether');
const defaultgasPrice = ethers.parseUnits('0.19', 'gwei');
function Timestamp() {
  return moment().tz('Asia/Jakarta').format('HH:mm:ss [WIB] DD-MM-YYYY');
}
async function getRoundedGasPrice(provider, defaultGasPrice) {
  try {
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
    return getRoundedGasPrice;

  } catch (error) {
    console.log(`Error mendapatkan gas price: ${error.message}. Menggunakan default gas price ${ethers.formatUnits(defaultGasPrice, "gwei")} gwei`);
    return defaultGasPrice;
  }
}


function appendLog(message) {
  fs.appendFileSync('log.txt', message + '\n');
}

function isTimeoutError(error) {
  return error.message.includes('504 Gateway Timeout') || 
         error.message.includes('request timeout') || 
         error.message.includes('failed to detect network') ||
         error.message.includes('free limit') || 
         error.message.includes('constant variable');
}
async function checkWethBalance(privateKey) {
  const wallet = new ethers.Wallet(privateKey, tempProvider);
  const address = await wallet.getAddress();
  let balanceWeth = await new ethers.Contract(WETH_CA, ABI, tempProvider).balanceOf(address);

  const loadingSymbols = ['|', '/', '-', '\\'];
  let index = 0;
  const loadingInterval = setInterval(() => {
    process.stdout.write(`\rChecking WETH balance for ${address}... ${loadingSymbols[index]}`);
    index = (index + 1) % loadingSymbols.length;
  }, 200);

  const amountToUnwrap = ethers.parseUnits('0.5', 'ether');

  while (balanceWeth <= amountToUnwrap) {
    try {
      await delay(5000);
      balanceWeth = await new ethers.Contract(WETH_CA, ABI, tempProvider).balanceOf(address);
    } catch (error) {
      if (isTimeoutError(error)) {
        console.log(`Kesalahan timeout terjadi: ${error.message}`);
        await changeRpc();
        continue;
      }
      const errorMessage = `Kesalahan memeriksa saldo: ${error.message}`;
      console.log(errorMessage.red);
      appendLog(errorMessage);
      throw error;
    }
  }
  clearInterval(loadingInterval);
  process.stdout.write('\r');
  console.log(`${ethers.formatEther(balanceWeth)} WETH`.blue);
  return balanceWeth;
}

async function doWrap(privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const amount = ethers.parseUnits('1', 'ether');
  const maxRetries = 3;
  let attempt = 0;
  const address = await wallet.getAddress();
  while (attempt < maxRetries) {
    try {
      const gasPrice = await getRoundedGasPrice(provider, defaultgasPrice);
	  const nonce = await provider.getTransactionCount(address, "latest");
	  console.log(`Nonce: ${nonce} , Gas Price: ${ethers.formatUnits(gasPrice, "gwei")}`);
      const wrapContract = new ethers.Contract(WETH_CA, ABI, wallet);
      const txWrap = await wrapContract.deposit({ value: amount, gasPrice: gasPrice, nonce: nonce});
      const receipt = await txWrap.wait(1);
      return receipt.hash;
    } catch (error) {
      attempt++;
      const errorMessage = `[$Timestamp()] Error executing Wrap transaction (Attempt ${attempt}/${maxRetries}): ${error.message}`;
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
  const amount = ethers.parseUnits('1', 'ether');
  const maxRetries = 3;
  let attempt = 0;
  const address = await wallet.getAddress();
  while (attempt < maxRetries) {
    try {
      const gasPrice = await getRoundedGasPrice(provider, defaultgasPrice);
	  const nonce = await provider.getTransactionCount(address, "latest");
	  console.log(`Nonce: ${nonce} , Gas Price: ${ethers.formatUnits(gasPrice, "gwei")}`);
      const unwrapContract = new ethers.Contract(WETH_CA, ABI, wallet);
      const txUnwrap = await unwrapContract.withdraw(amount, { gasPrice: gasPrice, nonce: nonce});
      const receipt = await txUnwrap.wait(1);
      return receipt.hash;
    } catch (error) {
      attempt++;
      const errorMessage = `[$Timestamp()] Error executing Unwrap transaction (Attempt ${attempt}/${maxRetries}): ${error.message}`;
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
  const values = recipients.map(() => ethers.parseUnits('1', 'ether'));
  const sendContract = new ethers.Contract(SEND_CA, SEND_ABI, wallet);
  const maxRetries = 3;
  let attempt = 0;
  const address = await wallet.getAddress();
  while (attempt < maxRetries) {
    try {
      const gasPrice = await getRoundedGasPrice(provider, defaultgasPrice);
	  const nonce = await provider.getTransactionCount(address, "latest");
	  console.log(`Nonce: ${nonce} , Gas Price: ${ethers.formatUnits(gasPrice, "gwei")}`);
      const txSendContract = await sendContract.multicall(recipients, values, { value: ethers.parseUnits('1', 'ether'), gasPrice: gasPrice, nonce: nonce });
      const receipt = await txSendContract.wait(1);
      return receipt.hash;
    } catch (error) {
      attempt++;
      const errorMessage = `[$Timestamp()] Error executing Send ETH transaction (Attempt ${attempt}/${maxRetries}): ${error.message}`;
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
}
async function checkBalance(privateKey) {
  const wallet = new ethers.Wallet(privateKey, tempProvider);
  const address = await wallet.getAddress();
  let balance = await tempProvider.getBalance(address);

  const loadingSymbols = ['|', '/', '-', '\\'];
  let index = 0;
  const loadingInterval = setInterval(() => {
    process.stdout.write(`\rMemeriksa saldo untuk ${address}... ${loadingSymbols[index]}`);
    index = (index + 1) % loadingSymbols.length;
  }, 200);

  while (balance <= amountCheck) {
    try {
      await delay(120000);
      balance = await tempProvider.getBalance(address);
    } catch (error) {
      if (isTimeoutError(error)) {
        console.log(`Kesalahan timeout terjadi: ${error.message}`);
        await changeRpc();
        continue;
      }
      const errorMessage = `Kesalahan memeriksa saldo: ${error.message}`;
      console.log(errorMessage.red);
      appendLog(errorMessage);
      throw error;
    }
  }

  clearInterval(loadingInterval);
  process.stdout.write('\r');
  console.log(`Pemeriksaan saldo selesai. Saldo: ${ethers.formatEther(balance)} ETH`);
  return balance;
}
async function checkBalanceDeposit(privateKey) {
  const wallet = new ethers.Wallet(privateKey, tempProvider);
  const address = await wallet.getAddress();
  let balanceDeposit = await tempProvider.getBalance(address);

  const loadingSymbols = ['|', '/', '-', '\\'];
  let index = 0;
  const loadingInterval = setInterval(() => {
    process.stdout.write(`\rChecking balance for ${address}... ${loadingSymbols[index]}`);
    index = (index + 1) % loadingSymbols.length;
  }, 200);

  while (balanceDeposit <= amountCheck) {
    try {
      await delay(5000);
      balanceDeposit = await tempProvider.getBalance(address);
    } catch (error) {
      if (isTimeoutError(error)) {
        console.log(`Kesalahan timeout terjadi: ${error.message}`);
        await changeRpc();
        continue;
      }
      const errorMessage = `Kesalahan memeriksa saldo: ${error.message}`;
      console.log(errorMessage.red);
      appendLog(errorMessage);
      throw error;
    }
  }
  clearInterval(loadingInterval);
  process.stdout.write('\r');
  console.log(`${ethers.formatEther(balanceDeposit)} ETH`.blue);
  return balanceDeposit;
}

async function runWrapandUnwrap() {
  displayHeader();
  for (const PRIVATE_KEY of PRIVATE_KEYS) {
    try {
      let balance = await checkBalance(PRIVATE_KEY);
      await delay(5000);
      for (let i = 0; i < 10; i++) {
        try {
		  const Timestamp() = moment().tz('Asia/Jakarta').format('HH:mm:ss [WIB] DD-MM-YYYY');
          const txMessage = `Transaction Wrap and Unwrap(${i + 1}/10)`;
          console.log(txMessage);
          appendLog(txMessage);
          let balanceDeposit = await checkBalanceDeposit(PRIVATE_KEY);
          await delay(5000);
          const receiptTx = await doWrap(PRIVATE_KEY);
          if (receiptTx) {
            const successMessage = `[${Timestamp()}] Transaction Wrap: ${explorer.tx(receiptTx)}`;
            console.log(successMessage.cyan);
            appendLog(successMessage);
			await delay(5000);
          }
          let balanceWeth = await checkWethBalance(PRIVATE_KEY);
          await delay(5000);
          const receiptTx2 = await doUnwrap(PRIVATE_KEY);
          if (receiptTx2) {
            const successMessage = `[${Timestamp()}] Transaction Unwrap: ${explorer.tx(receiptTx2)}`;
            console.log(successMessage.cyan);
            appendLog(successMessage);
			await delay(5000);
          }
		  console.log('');
        } catch (error) {
          const errorMessage = `[${Timestamp()}] Error in Wrap and Unwrap iteration ${i + 1}: ${error.message}`;
          console.log(errorMessage.red);
          appendLog(errorMessage);
          if (isTimeoutError(error)) {
            console.log(`Timeout error detected. Changing RPC and retrying iteration ${i + 1}...`);
            await changeRpc();
            await delay(10000);
            i--;
          } else {
            throw error;
          }
        }
      }
      await delay(5000);
      const sendMessage = `Transaction Send ETH`;
      console.log(sendMessage);
      appendLog(sendMessage);

      let balanceSend = await checkBalanceDeposit(PRIVATE_KEY);
      await delay(5000);
      const receiptTxSend = await doSendEther(PRIVATE_KEY);
      if (receiptTxSend) {
        const successMessage = `[${Timestamp()}] Transaction Send ETH: ${explorer.tx(receiptTxSend)}`;
        console.log(successMessage.cyan);
        appendLog(successMessage);
		await delay(5000);
      }
    } catch (error) {
      const errorMessage = `[${Timestamp()}] Error processing transactions for private key. Details: ${error.message}`;
      console.log(errorMessage.red);
      console.log(error);
      appendLog(errorMessage);
      await delay(5000);
    }
	displayHeader();
    console.log('Menunggu Giliran Selanjutnya...');
  }
}
const job = new CronJob('0 19 * * *', runWrapandUnwrap, null, true, 'UTC'); console.log('Transaksi akan dijalankan setiap 19:00 UTC');
  
job.start();
runWrapandUnwrap();
