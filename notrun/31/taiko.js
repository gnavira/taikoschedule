const job = new CronJob('30 8 * * *', runWrapandUnwrap, null, true, 'UTC');
console.log('Transaksi akan dijalankan setiap 08:30 UTC');
