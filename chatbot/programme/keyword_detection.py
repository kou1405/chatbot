import pyaudio
import pvporcupine
import numpy as np  # for data type conversion

# Configuration constants
CHUNK = 512  # Size of audio chunk
FORMAT = pyaudio.paInt16  # 16-bit signed integers format
CHANNELS = 1 # Mono audio
RATE = 16000  # Sample rate in Hz

def init_audio_stream():

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    return p, stream

def get_next_audio_frame(stream):

    try:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_frame = np.frombuffer(data, dtype=np.int16)
        return audio_frame
    except IOError as e:
        print(f"Error reading audio stream: {e}")
        return None

def detect_keyword():


    p, stream = init_audio_stream()


    keyword_paths = ['flora_fr_windows_v3_0_0.ppn']

    porcupine = pvporcupine.create(
        access_key='vvEUGMMYC4SwNKtz34CU5SEJWBxAfCeGUekC3v6cUFjH+MTPuPIpeQ==',  # Replace with your Picovoice access key
        keyword_paths=keyword_paths,
        model_path="porcupine_params_fr.pv",
        sensitivities=[0.5]
    )

    try:
        keyword_detected = False
        print("Listening for wake word...")

        while not keyword_detected:
            audio_frame = get_next_audio_frame(stream)
            if audio_frame is not None:
                keyword_index = porcupine.process(audio_frame)
                if keyword_index >= 0:
                    return True
                    keyword_detected = True
                else:
                    print("No keyword detected in the current frame.")

    except KeyboardInterrupt:
        print("Exiting...")

    finally:

        stream.stop_stream()
        stream.close()
        p.terminate()
        porcupine.delete()
        print("Cleanup completed.")

if __name__ == "__main__":
    detect_keyword()
