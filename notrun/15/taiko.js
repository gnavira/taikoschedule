const job = new CronJob('30 4 * * *', runWrapandUnwrap, null, true, 'UTC');
console.log('Transaksi akan dijalankan setiap 04:30 UTC');
