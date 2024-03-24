
import wave # module that provides support for reading and writing WAV files
import sys #provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
import pyaudio

CHUNK = 1024 #size of each buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == "darwin" else 2
RATE = 44100


def record_audio(seconds: int):
    output_path = "output.wav"
    with wave.open(output_path, "wb") as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        print("Recording...")
        for index in range(0, RATE // CHUNK * seconds):
            if index % (RATE // CHUNK) == 0:
                print(f"{index // (RATE // CHUNK)} / {seconds}s")
            wf.writeframes(stream.read(CHUNK))
        print("Done")

        stream.close()
        p.terminate()
    print(f"File saved at {output_path}")
    return output_path

if __name__ == "__main__":
    record_audio(20)