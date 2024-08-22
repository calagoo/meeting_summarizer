""" VOICE RECOGNITION AND TEXT PROCESSING"""
import os
from threading import Thread
from queue import Queue
import warnings
import speech_recognition as sr
from openai import OpenAI

warnings.filterwarnings("ignore")

class Summarizer:
    """Summarizes and processes text using Google Speech Recognition and Open"""
    ai = OpenAI()
    ai.api_key = os.getenv("OPENAI_API_KEY")
    r = sr.Recognizer()
    audio_queue = Queue()
    result_queue = Queue()  # Queue to store recognized text for post-processing

    def __init__(self):
        self.text = ""
        self.context = ""
        self.ongoing = ""
        self.total_text = ""
        self.tokens = 0

    def speech_to_text(self):
        """Converts speech to text using Google Speech Recognition."""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                self.text = r.recognize_whisper(audio)
                print(f"You said: {self.text}")
            except sr.UnknownValueError:
                print("Sorry, I could not recognize what you said")

    def recognize_worker(self):
        """Continuously listens for audio from the audio queue, and recognizes it using Google Speech Recognition."""
        # this runs in a background thread
        while True:
            # retrieve the next audio processing job from the main thread
            audio = self.audio_queue.get()
            if audio is None:
                break  # stop processing if the main thread is done

            # Received audio data, now we'll recognize it using whisper speech recognition
            try:
                self.text = self.r.recognize_whisper(audio)
                self.text_processing()
            except sr.UnknownValueError:
                print("Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(
                    f"Could not request results from Speech Recognition service; {e}")

            # Mark the audio processing job as completed in the queue
            self.audio_queue.task_done()

    def thread_starting(self):
        """Starts the audio processing thread, listens for audio, and recognizes it."""
        # Start a new thread to recognize audio, while this thread focuses on listening
        recognize_thread = Thread(target=self.recognize_worker)
        recognize_thread.daemon = True
        recognize_thread.start()

        with sr.Microphone() as source:
            print("Calibrating microphone for ambient noise... Please wait.")
            self.r.adjust_for_ambient_noise(source, duration=2)
            print("Listening for audio... Press Ctrl + C to stop.")
            try:
                while True:  # Repeatedly listen for phrases and put the resulting audio on the audio processing job queue
                    self.audio_queue.put(self.r.listen(
                        source, phrase_time_limit=5))
            except KeyboardInterrupt:  # Allow Ctrl + C to shut down the program
                pass

        self.audio_queue.join()  # Block until all current audio processing jobs are done
        self.audio_queue.put(None)  # Tell the recognize_thread to stop
        recognize_thread.join()  # Wait for the recognize_thread to actually stop

    def text_processing(self):
        """Processes the recognized text, and returns a summary of the text."""
        # Use the OpenAI API to clean up and make sense
        prompt = self.ongoing + " " + self.text
        if prompt.split().__len__() < 15:
            self.ongoing = prompt
            return
        else:
            self.ongoing = ""
        # return

        # print()
        # print()
        # print(prompt)
        # print()
        # print(self.context)
        # print()

        content = (
            "Here are the current meeting notes summarized in bullet points:\n"
            + self.context
            + "\n\n"
            + "Please update these notes with the following new information:\n"
            + prompt
        )

        resp = self.ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant who looks at meeting notes and uses context to help correct them. Please only reply with a summary of the notes, in short key points.",
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],
            stream=False,
        )

        # Store the complete context
        self.total_text += resp.choices[0].message.content + "\n"

        # Update the context with the most recent 5 bullet points
        context_lines = resp.choices[0].message.content.strip().split("\n")
        self.context = "\n".join(context_lines[-5:])

        # Track tokens and update text for printing
        self.tokens += resp.usage.total_tokens
        self.text = resp.choices[0].message.content

        os.system("cls")
        print(
            f"Tokens Used: {self.tokens}. Approx {round((self.tokens/1000)*0.000600,4)} USD")
        print(self.text)

    def clean_up_notes(self):
        """Cleans up the notes and returns a summary of the notes."""
        # Use the OpenAI API to clean up and make sense
        prompt = self.total_text

        tmp = set(prompt.split("\n"))
        var = ""
        for t in tmp:
            var += t + "\n"

        prompt = var

        resp = self.ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant who looks at meeting notes and uses context to help correct them. Please clean up these notes, keep them original, but get rid of any copies.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            stream=False,
        )

        return resp.choices[0].message.content, resp.usage.total_tokens


def main():
    """main function"""

    txt = ""

    try:
        ovr = Summarizer()
        ovr.thread_starting()
    except KeyboardInterrupt:
        print("Program stopped by user")

    txt, tk = ovr.clean_up_notes()
    os.system("cls")
    print(
        f"Final Notes, using a total of {str(ovr.tokens + tk)} tokens (~${round(((ovr.tokens + tk)/1000)*0.000600,4)}).")
    print(txt)


if __name__ == "__main__":
    main()
