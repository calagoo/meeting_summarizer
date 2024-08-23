// main.js

let eventSource;
let isStreaming = false;
//TODO: Fix stop streaming, hangs because eventSource is not defined?
function toggleStream() {
    if (isStreaming) {
        console.log("Stopping stream..."); // Debugging output
        finalMessage();
    } else {
        console.log("Starting stream..."); // Debugging output
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
                    const message = event.data;
                    console.log("Message received:", message); // Debugging output
                    if (message === "Streaming stopped.") {
                        // Handle the end of the stream
                        stopStream(); // Automatically stop the stream
                    } else {
                        // Update the streaming-text with the latest message
                        document.getElementById('streaming-text').textContent = message;
                        document.getElementById('info-text').textContent = "Streaming...";
                    }
                };
                document.getElementById('toggle-button').textContent = 'Stop';
                isStreaming = true;
            }
        });
}

function formatMessage(message) {
    // Remove the "FINAL_" prefix
    let cleanMessage = message.replace(/^FINAL_/, '');

    // // Split the message into sentences based on periods (.), then filter out empty strings
    // let sentences = cleanMessage.split('.').filter(sentence => sentence.trim() !== '');

    // // Trim each sentence and format it as a bullet point
    // let bulletPoints = sentences.map(sentence => `- ${sentence.trim()}.`);

    // // Join the bullet points into a single string with line breaks
    return cleanMessage;
}

function finalMessage() {
    document.getElementById('info-text').textContent = "Waiting for final message...";
    callStop();
    if (eventSource) {
        eventSource.onmessage = function(event) {
            const message = event.data;
            if (message.startsWith("FINAL_")) {
                fmsg = formatMessage(message);
                console.log("Final message received:", fmsg); // Debugging output
                document.getElementById('streaming-text').innerHTML = fmsg;
                document.getElementById('info-text').textContent = "Final message received. Stream is stopping.";
                stopStream();
            }
        };
    } else {
        console.log("EventSource is not defined."); // Debugging output
    }
}

function callStop() {
    console.log("Calling stop function..."); // Debugging output
    fetch('/stop', { method: 'POST' })
        .then(response => response.json())
}

function stopStream(info_text="Press the button to start streaming.") {
    console.log("Sending stop request..."); // Debugging output
    fetch('/stop', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (eventSource) {
                eventSource.close();
            }
            document.getElementById('toggle-button').textContent = 'Start';
            document.getElementById('info-text').textContent = info_text;
            isStreaming = false;
        });
}

window.onload = function() {
    stopStream(info_text="Press the button to start streaming.");
    document.getElementById('toggle-button').onclick = toggleStream;
};