import speech_recognition as sr

def listen_and_convert(language="fr-FR"):
  """Listens to audio input, converts speech to text, and detects French."""
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    audio = r.listen(source)

  try:
    text = r.recognize_google(audio, language=language)  # Specify language code
    print("You said: " + text)
    return text
  except sr.UnknownValueError:
    print("Could not understand audio")
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
  return None

if __name__ == "__main__":
  speech_text = listen_and_convert(language="fr-FR")  # Set language to French
  if speech_text:
    print("Speech to text conversion:", speech_text)
  else:
    print("Speech recognition failed.")
