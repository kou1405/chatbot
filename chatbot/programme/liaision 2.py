import pyaudio
import pvporcupine
import numpy as np  # for data type conversion
import google.generativeai as genai
from gtts import gTTS
from playsound import playsound
from io import BytesIO
from tempfile import TemporaryDirectory
import speech_recognition as sr

# PyAudio configuration
CHUNK = 512  # Adjust CHUNK size based on your findings (might need to experiment)
FORMAT = pyaudio.paInt16  # Ensure format is set to 16-bit signed integers
CHANNELS = 1
RATE = 16000

# Initialize PyAudio stream outside the loop
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def get_next_audio_frame():
    """Reads audio data from the open PyAudio stream (converts to int16)"""
    data = stream.read(CHUNK)
    # Convert captured data to NumPy array of int16
    audio_frame = np.frombuffer(data, dtype=np.int16)
    return audio_frame

# Replace with path to your custom "hey blink" model file
keyword_paths = ['a.ppn']

porcupine = pvporcupine.create(
    access_key='',  # Replace with your Picovoice access key
    keyword_paths=keyword_paths
)

def listen_and_convert():
    """Listens for user input and converts it to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your question...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None

def text_to_speech(text):
    # Text to convert to speech
    language = 'en'
    # Create gTTS object
    tts = gTTS(text=text, lang=language)
    # Create a BytesIO object to store audio data
    output_buffer = BytesIO()
    # Write the audio data to the buffer
    tts.write_to_fp(output_buffer)
    # Get the audio data from the buffer
    audio_data = output_buffer.getvalue()
    # Use TemporaryDirectory to create a temporary directory with a shorter path
    with TemporaryDirectory() as temp_dir:
        temp_file = open(f"{temp_dir}/speech.mp3", 'wb')
        temp_file.write(audio_data)
        temp_file.close()
        # Play the audio from the temporary file
        playsound(temp_file.name, block=True)

def generate_and_speak_answer(question):
    """Uses Google AI to answer a question and speaks the answer"""
    # Replace with your actual Google AI API key
    API_KEY = "AIzaSyBivUaHrj09khl2R4HoKesX6CQAdi-8f7o"
    genai.configure(api_key=API_KEY)
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    convo = model.start_chat(history=[])
    convo.send_message(question)
    answer = convo.last.text
    print(answer)
    # Text to speech conversion
    text_to_speech(answer)

try:
    keyword_detected = False
    while not keyword_detected:
        audio_frame = get_next_audio_frame()
        if audio_frame is not None:
            keyword_index = porcupine.process(audio_frame)
            if keyword_index >= 0:
                print("Wake word 'hey blink' detected!")
                keyword_detected = True

    question = listen_and_convert()
    if question:
        generate_and_speak_answer(question)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
