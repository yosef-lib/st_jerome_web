const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const axios = require('axios');

// Konfigurasi port
const PORT = 3005;
const FLASK_URL = 'http://127.0.0.1/api/wa_webhook'; // Ganti dengan port gunicorn jika bukan 80

const app = express();
app.use(express.json());

// Inisialisasi WhatsApp Client
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    }
});

// Generate QR Code di terminal (bisa dilihat di log PM2)
client.on('qr', (qr) => {
    console.log('SCAN QR CODE INI MENGGUNAKAN WHATSAPP:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('WhatsApp Bot berhasil terhubung dan siap digunakan!');
});

// Menangkap pesan masuk (Customer Service / Bot)
client.on('message', async (msg) => {
    // Jangan tanggapi pesan dari grup (opsional) atau status
    if (msg.isGroupMsg || msg.isStatus) return;

    try {
        console.log(`Menerima pesan dari ${msg.from}: ${msg.body}`);
        // Kirim ke Flask backend untuk diproses oleh AI
        const response = await axios.post(FLASK_URL, {
            from: msg.from,
            body: msg.body,
            sender_name: msg._data.notifyName || 'Pengguna'
        });

        // Jika Flask memberikan balasan, kirim balik ke user
        if (response.data && response.data.reply) {
            msg.reply(response.data.reply);
        }
    } catch (error) {
        console.error('Gagal menghubungi Flask backend:', error.message);
    }
});

client.initialize();

// Endpoint API untuk dikirim pesan dari Flask (Notifikasi / Tagihan / Struk)
app.post('/api/send_message', async (req, res) => {
    const { number, message } = req.body;
    
    if (!number || !message) {
        return res.status(400).json({ status: 'error', message: 'Nomor dan pesan wajib diisi.' });
    }

    try {
        // Format nomor telepon Indonesia (misal: 0812... menjadi 62812...@c.us)
        let formattedNumber = number;
        if (!formattedNumber.endsWith('@g.us')) {
            formattedNumber = formattedNumber.replace(/\D/g, '');
            if (formattedNumber.startsWith('0')) {
                formattedNumber = '62' + formattedNumber.substring(1);
            }
            if (!formattedNumber.endsWith('@c.us')) {
                formattedNumber += '@c.us';
            }
        }

        // Kirim pesan
        await client.sendMessage(formattedNumber, message);
        console.log(`Berhasil mengirim pesan ke ${formattedNumber}`);
        res.json({ status: 'success', message: 'Pesan berhasil dikirim.' });
    } catch (error) {
        console.error(`Gagal mengirim pesan ke ${number}:`, error);
        res.status(500).json({ status: 'error', message: error.toString() });
    }
});


app.get('/api/groups', async (req, res) => {
    try {
        const chats = await client.getChats();
        const groups = chats.filter(chat => chat.isGroup).map(chat => ({
            id: chat.id._serialized,
            name: chat.name
        }));
        res.json({ status: 'success', groups: groups });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.toString() });
    }
});

// Jalankan Express Server
app.listen(PORT, () => {
    console.log(`API WhatsApp Gateway berjalan di http://localhost:${PORT}`);
});
