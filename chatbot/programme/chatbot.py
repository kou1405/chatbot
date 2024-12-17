import keyword_detection
import speech_recognition_module
import elevenlabs_integration
import gemini

if __name__ == "__main__":
    while True:    
        if keyword_detection.detect_keyword():
            speech_text = speech_recognition_module.listen_and_convert()
            if speech_text:
                x=gemini.chat_with_model(speech_text)
                elevenlabs_integration.generate_and_stream_audio(x)
            else:
                print("Speech recognition failed.")



    
