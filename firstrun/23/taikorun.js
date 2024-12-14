const job = new CronJob('30 6 * * *', runWrapandUnwrap, null, true, 'UTC');
console.log('Transaksi akan dijalankan setiap 06:30 UTC');
