const job = new CronJob('30 7 * * *', runWrapandUnwrap, null, true, 'UTC');
console.log('Transaksi akan dijalankan setiap 07:30 UTC');
