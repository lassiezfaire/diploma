let mediaRecorder;
let audioChunks = [];

const recognize_url = "/voice/process/";
const command_url = "/command/";
const recordButton = document.getElementById('recordButton');
const audioPlayback = document.getElementById('audioPlayback');
const recognizedText = document.getElementById('recognized');
const sendButton = document.getElementById('sendButton')
const sendImmediately = document.getElementById('sendImmediately')

const audioContext = new (window.AudioContext || window.webkitAudioContext)();
let analyser = audioContext.createAnalyser();
let source;

sendButton.onclick = sendCommand

recordButton.onmousedown = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const options = { mimeType: 'audio/ogg' }
    mediaRecorder = new MediaRecorder(stream, options);
    mediaRecorder.start();
    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
    // Отправляем на сервер данные для распознавания
        document.body.style.cursor = 'wait';
        const audioBlob = new Blob(audioChunks, { type: 'audio/ogg' });
        audioPlayback.src = URL.createObjectURL(audioBlob);

        const formData = new FormData();
        formData.append('audiofile', audioBlob);
        const response = await fetch(recognize_url, {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        console.log(result);
        recognizedText.value = result.text
        recognizedText.dispatchEvent(new Event('input'))
        audioChunks = [];
        if (document.getElementById('sendImmediately').checked) {
           sendCommand()
        }
        document.body.style.cursor = ''
    };
};


sendImmediately.onclick = () => {
    sendButton.style.visibility = sendImmediately.checked?'hidden':'visible';
};

recordButton.onmouseup = () => {
    mediaRecorder.stop();
};


function sendCommand() {
    document.body.style.cursor = 'wait';
    data = {'prompt' : recognizedText.value}
    const response = fetch(command_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    document.body.style.cursor = '';
}

