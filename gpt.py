import openai
import pyttsx3
import speech_recognition as sr
import os

# Set your OpenAI API key
openai.api_key = "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"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def audToText(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def generateResponse(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speakText(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Say 'sia' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if transcription.lower() == "sia":
                filename = "input.wav"
                print("What do you want to know?")
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())
                text = audToText(filename)
                if text:
                    print(f"You said: {text}")

                    response = generateResponse(text)
                    print(f"GPT-3 says: {response}")

                    # Speak the response aloud
                    speakText(response)
        except sr.UnknownValueError:
            speakText("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            speakText(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            speakText(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
