const job = new CronJob('30 2 * * *', runWrapandUnwrap, null, true, 'UTC');
console.log('Transaksi akan dijalankan setiap 02:30 UTC');
