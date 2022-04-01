# for short audio files
import speech_recognition as sr

filename = "test.wav"

r = sr.Recognizer()

with sr.AudioFile(filename) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print(text)

# for large audio files
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()

# a funtion that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_text(path):
    """
    Splitting the large audio file into chunks and
    apply speech recognition on each chunk
    :param path: the file path to the audio file
    :return: the text of all chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)

    # split audio sound where silence is grtr than 700 milliseconds and get chunks
    chunks = split_on_silence(sound,
                              min_silence_len=500,          # adjust for each audio file
                              silence_thresh=sound.dBFS-14, # adjustable
                              keep_silence=500)             # adjustable

    folder_name = "audio-chunks"

    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    whole_text = ""

    # process each chunk
    for index, audio_chunk in enumerate(chunks, start=1):

        # export audio chunk and save it in the 'folder_name' directory
        chunk_filename = os.path.join(folder_name, f"chunk{index}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)

            # try to convert it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text

    # return the text for all chunks detected
    return whole_text



