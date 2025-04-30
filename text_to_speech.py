from gtts import gTTS
import os
import platform

def text_to_speech(text, filename="flashcard.mp3"):
    """ Convert extracted text to speech with better cross-platform support """
    if not text.strip():
        print("Error: No text provided for speech synthesis.")
        return
    
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    print(f"Flashcard audio saved as {filename}")

    # Cross-platform audio playback
    if platform.system() == "Windows":
        os.system(f"start {filename}")
    elif platform.system() == "Darwin":  # macOS
        os.system(f"afplay {filename}")
    else:  # Linux
        os.system(f"mpg321 {filename}")

if __name__ == "__main__":
    sample_text = "Machine learning enhances data analysis."
    text_to_speech(sample_text)
