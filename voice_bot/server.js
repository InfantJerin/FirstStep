const WebSocket = require('ws');
const axios = require('axios');

// Deepgram API key
const DEEPGRAM_API_KEY = ''; // Replace with your actual API key

// WebSocket URL for Deepgram
const deepgramUrl = `wss://api.deepgram.com/v1/listen`;


// Create WebSocket server for client connections
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (clientWs) => {
    console.log('Client connected.');

    // Try to connect to Deepgram WebSocket
    let deepgramWs;

    try {
        deepgramWs = new WebSocket('wss://api.deepgram.com/v1/listen', {
            headers: {
                // Remember to replace the YOUR_DEEPGRAM_API_KEY placeholder with your Deepgram API Key
                Authorization: `${DEEPGRAM_API_KEY}`,
            },
        });
    } catch (error) {
        console.error('Error connecting to Deepgram WebSocket:', error);
        clientWs.send('Error connecting to Deepgram.');
        return;
    }

    deepgramWs.on('open', () => {
        console.log('Connected to Deepgram WebSocket successfully.');
    });

    deepgramWs.on('error', (error) => {
        console.error('Deepgram WebSocket error:', error);
        clientWs.send('Error with Deepgram connection.');
    });

    deepgramWs.on('close', (code, reason) => {
        console.log(`Deepgram WebSocket closed: ${code}, Reason: ${reason}`);
    });

    // When receiving audio from the browser, forward it to Deepgram
    clientWs.on('message', (audioData) => {
        if (deepgramWs.readyState === WebSocket.OPEN) {
            deepgramWs.send(audioData);
        } else {
            console.error('Deepgram WebSocket is not open.');
        }
    });

    // Handle transcriptions from Deepgram
    deepgramWs.on('message', (message) => {
        const data = JSON.parse(message);
        const transcript = data.channel.alternatives[0].transcript;

        if (transcript) {
            console.log('Transcript from Deepgram:', transcript);
            clientWs.send(transcript);
        }
    });

    // Handle client disconnect
    clientWs.on('close', () => {
        console.log('Client disconnected.');
        if (deepgramWs) {
            deepgramWs.close();
        }
    });
});

console.log('WebSocket server is running on ws://localhost:8080');
