const express = require('express');
const multer  = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Configure multer to handle file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, path.join(__dirname, 'uploads'));
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname);
    }
});
const upload = multer({ storage: storage });

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Serve index.html on the root URL
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Handle file upload POST request
app.post('/upload', upload.array('file'), (req, res) => {
    // Multer stores the uploaded files in 'req.files'
    if (!req.files || req.files.length === 0) {
        return res.status(400).send('No files were uploaded.');
    }

    // Process each uploaded file
    req.files.forEach(file => {
        const filePath = path.join(__dirname, 'uploads', file.originalname);
        fs.writeFile(filePath, file.buffer, err => {
            if (err) {
                console.error(`Failed to write file ${file.originalname}: ${err}`);
                return res.status(500).send('Failed to upload files.');
            }
            console.log(`Uploaded file: ${file.originalname}`);
        });
    });

    res.status(200).send('Files uploaded successfully!');
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
