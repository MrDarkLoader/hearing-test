import pyaudio
import numpy as np

# Настройки для генерации звука
frequency_array = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392, 415.30, 440, 466.16,
                   493.88]  # Частота нот
note_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'] # Названия нот
mapped_notes = dict(zip(note_list, frequency_array))
duration = 2  # Длительность звука в секундах
volume = 0.5  # Громкость звука
discretization = 96000  # Частота дискретизации


def find_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None


def generate_wave(current_frequency, duration, volume, discretization):
    wave = (np.sin(2 * np.pi * np.arange(discretization * duration) * current_frequency / discretization)).astype(
        np.float32)
    wave *= volume
    return wave


while True:
    current_streak = 0
    current_frequency = np.random.choice(frequency_array)
    current_note = find_key_by_value(mapped_notes, current_frequency)
    # Создание аудио потока
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=discretization, output=True)

    # Воспроизведение звука
    stream.write(generate_wave(current_frequency, duration, volume, discretization).tobytes())
    input_note = input("Guess the note: ")

    # Проверка ответа
    if input_note.upper() == current_note:
        current_streak += 1
        print("Correct! " + 'Current streak: ' + str(current_streak))
    elif input_note.upper() == 'EXIT':
        break
    else:
        current_streak = 0
        print(f"Wrong, the correct answer is {current_note}, current streak: {current_streak}")
    # Закрытие потока и pyaudio
    stream.stop_stream()
    stream.close()
    p.terminate()
