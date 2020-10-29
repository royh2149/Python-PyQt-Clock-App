from pydub import AudioSegment
import sys

base = sys.argv[1]
print(base)
filename = base
target_file = base.replace(".mp3", ".wav")

sound = AudioSegment.from_mp3(filename)

sound.export(target_file, format='wav')

# sound2 = AudioSegment.from_file(target_file, format='mp3')

# sound2.export(filename, format='wav')