const job = new CronJob('0 6 * * *', runWrapandUnwrap, null, true, 'UTC');
console.log('Transaksi akan dijalankan setiap 06:00 UTC');
