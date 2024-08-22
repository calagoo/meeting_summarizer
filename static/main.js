// main.js

let eventSource;
let isStreaming = false;

function toggleStream() {
    if (isStreaming) {
        stopStream();
    } else {
        startStream();
    }
}

function startStream() {
    fetch('/start', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'started') {
                eventSource = new EventSource('/stream');
                eventSource.onmessage = function(event) {
                    document.getElementById('streaming-text').textContent = event.data;
                };
                document.getElementById('toggle-button').textContent = 'Stop';
                isStreaming = true;
            }
        });
}

function stopStream() {
    fetch('/stop', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (eventSource) {
                eventSource.close();
            }
            document.getElementById('toggle-button').textContent = 'Start';
            document.getElementById('streaming-text').textContent = 'Streaming stopped.';
            isStreaming = false;
        });
}

window.onload = function() {
    stopStream();
    document.getElementById('toggle-button').onclick = toggleStream;
};