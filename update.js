const fs = require('fs');
const path = require('path');

// Folder utama tempat `firstrun` dan `notrun` berada
const mainFolders = ['firstrun', 'notrun'];

// Fungsi untuk mencari dan menghapus teks tertentu di dalam file `start.js`
function removeTextInFile(filePath) {
    // Baca konten file
    let fileContent = fs.readFileSync(filePath, 'utf-8');
    
    // Hapus baris `await runWrapandUnwrap();` dan `});`
    const updatedContent = fileContent.replace(/await runWrapandUnwrap\(\);\s*\n\s*\}\);/g, '');

    // Tulis kembali konten yang telah diperbarui ke dalam file
    fs.writeFileSync(filePath, updatedContent, 'utf-8');
    console.log(`Updated: ${filePath}`);
}

// Fungsi untuk memproses folder 1 hingga 38 di dalam `firstrun` dan `notrun`
function processFolders() {
    mainFolders.forEach(folder => {
        for (let i = 1; i <= 38; i++) {
            const subfolderPath = path.join(folder, String(i));
            const filePath = path.join(subfolderPath, 'start.js');
            
            // Periksa apakah file `start.js` ada, lalu lakukan penggantian
            if (fs.existsSync(filePath)) {
                removeTextInFile(filePath);
            } else {
                console.log(`File not found: ${filePath}`);
            }
        }
    });
}

// Jalankan proses penggantian
processFolders();