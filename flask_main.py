"""Flask app to stream data to the client using Server-Sent Events (SSE)."""
import time
from flask import Flask, render_template, jsonify, Response
import threading
from main import Summarizer

class StreamingApp:
    """Class to handle the Flask app for streaming data."""
    def __init__(self):
        self.app = Flask(__name__)
        self.summarizer = Summarizer()

        self.streaming = False
        self.setup_routes()

    def setup_routes(self):
        """Setup the routes for the Flask app."""
        @self.app.route('/')
        def home():
            return render_template('index.html')

        @self.app.route('/start', methods=['POST'])
        def start_stream():
            if not self.streaming:
                self.streaming = True
                return jsonify({'status': 'started'})
            return jsonify({'status': 'already started'})

        @self.app.route('/stream')
        def stream():
            if self.streaming:
                return Response(self.mrmin(), mimetype='text/event-stream')
            return jsonify({'status': 'not streaming'})

        @self.app.route('/stop', methods=['POST'])
        def stop_stream():
            if self.streaming:
                self.streaming = False
                self.stop_streaming()
                return jsonify({'status': 'stopped'})
            return jsonify({'status': 'already stopped'})

    def mrmin(self):
        """Generator function to stream data to the client."""
        
        # Start the summarizer thread in a separate thread to avoid blocking
        summarizer_thread = threading.Thread(target=self.summarizer.thread_starting, args=(False,))
        summarizer_thread.daemon = True
        summarizer_thread.start()

        self.streaming = True

        print("Streaming data...")

        try:
            while self.streaming:
                if not self.summarizer.result_queue.empty():
                    data = self.summarizer.result_queue.get()
                    yield f"data: {data}\n\n"  # Proper SSE format
                else:
                    time.sleep(0.1)
        finally:
            self.summarizer.stop_listening()  # Signal the summarizer to stop listening
            summarizer_thread.join()  # Ensure the thread is properly closed
            yield "data: Streaming stopped.\n\n"

    def stop_streaming(self):
        """Stop the streaming process."""
        self.summarizer.stop_listening()
        self.streaming = False
        print("Closing...")

    def run(self):
        """Run the Flask app."""
        self.app.run(debug=True)

if __name__ == '__main__':
    streaming_app = StreamingApp()
    streaming_app.run()
