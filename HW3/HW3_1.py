from scipy.io import wavfile
from scipy.fftpack import fft 
import matplotlib.pyplot as plt
import numpy as np
import simpleaudio as sa
import wave
import struct

def get_frequency(note_number, octave=4):
    """Convert a note number to its frequency.
    1 = Do, 2 = Re, 3 = Mi, 4 = Fa, 5 = Sol, 6 = La, 7 = Si
    octave: 4 is middle octave, 5 is one octave higher, 3 is one octave lower
    """
    # Middle C (Do) = 261.63 Hz
    base_frequencies = {
        1: 261.63,  # Do (C4)
        2: 293.66,  # Re (D4)
        3: 329.63,  # Mi (E4)
        4: 349.23,  # Fa (F4)
        5: 392.00,  # Sol (G4)
        6: 440.00,  # La (A4)
        7: 493.88   # Si (B4)
    }
    
    if note_number == 0:  # Rest
        return 0
    
    # Calculate frequency based on octave
    base_freq = base_frequencies.get(note_number, 0)
    octave_diff = octave - 4  # Difference from middle octave
    return base_freq * (2 ** octave_diff)

def generate_tone(frequency, duration, sample_rate=44100):
    """Generate a sine wave tone at the given frequency and duration."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    if frequency == 0:  # Rest
        return np.zeros(len(t))
    
    tone = np.sin(2 * np.pi * frequency * t)
    
    # Apply a simple envelope to avoid clicks
    fade = int(sample_rate * 0.01)  # 10ms fade in/out
    tone[:fade] = tone[:fade] * np.linspace(0, 1, fade)
    tone[-fade:] = tone[-fade:] * np.linspace(1, 0, fade)
    
    return tone

def getmusic(score, beat, name, octaves=None):
    """Generate a WAV file from the numbered musical notation.
    
    Args:
        score: List of integers representing notes (1=Do, 2=Re, etc., 0=rest)
        beat: List of durations for each note in seconds
        name: Name of the output file (without .wav extension)
        octaves: List of octave values for each note (default is all middle octave)
    """
    sample_rate = 44100
    
    # Validate inputs
    if len(score) != len(beat):
        raise ValueError("The score and beat lists must have the same length")
    
    if octaves is None:
        octaves = [4] * len(score)
    elif len(octaves) != len(score):
        raise ValueError("The octaves list must have the same length as score")
    
    # Generate the audio for each note
    audio = np.array([])
    for note, duration, octave in zip(score, beat, octaves):
        freq = get_frequency(note, octave)
        tone = generate_tone(freq, duration, sample_rate)
        audio = np.append(audio, tone)
    
    # Normalize the audio to avoid clipping
    if np.max(np.abs(audio)) > 0:  # Avoid division by zero
        audio = audio / np.max(np.abs(audio)) * 0.9
    
    # Convert to 16-bit PCM
    audio = (audio * 32767).astype(np.int16)
    
    # Write to WAV file
    output_file = f"{name}.wav"
    wavfile.write(output_file, sample_rate, audio)
    
    print(f"Music file created: {output_file}")
    return output_file

# Example usage (Twinkle Twinkle Little Star)
if __name__ == "__main__":
    # Original example: twinkle twinkle little star
    # score = [1, 1, 5, 5, 6, 6, 5]  # 1: Do, 2: Re, 3: Mi, ...
    # beat = [1, 1, 1, 1, 1, 1, 2]   # Duration in seconds
    # name = 'twinkle'
    
    # The score uses the following format: numbers are notes, '-' indicates a rest
    # The superscript 5 or 6 indicates a higher octave, dots below represent longer duration
    score = [
        # First line: 0 0 0 3 5 | 6. 4 4 3 2 1 2 6 | 5 6 3 3 2. 1 (6 1 | 2. 7 7 4 3 3 2 7 |
        0, 0, 0, 3, 5,
        6, 4, 4, 3, 2, 1, 2, 6,
        5, 6, 3, 3, 2, 1,
        6, 1,
        2, 7, 7, 4, 3, 3, 2, 7,
        
        # Second line: i. 7 7 5 6 5) 3 5 | 6. 4 4 3 2 7 6 5 | 5 6 7 i i 3 2 2 | 1 - - - |
        1, 7, 7, 5, 6, 5, 3, 5,
        6, 4, 4, 3, 2, 7, 6, 5,
        5, 6, 7, 1, 1, 3, 2, 2,
        1, 0, 0, 0
    ]
    
    # explain: (l) implies lower octave, (h) implies higher octave
    # explain: (2) means that the note has 2 times longer duration than others, and so on
    octaves = [
        # First line
        4, 4, 4, 4, 4,                  # Mi Sol
        4, 4, 4, 4, 4, 4, 4, 4,         # La Fa(2) Mi Re Do Re La Sol
        4, 4, 4, 4, 4, 4,               # La Sol Mi(2) Re Do
        4, 4,                           # La(l) Do(l)
        4, 3, 3, 4, 4, 4, 4, 4,         # Re Si(l, 2) Fa Mi(2) Re Si
        
        # Second line 
        5, 4, 4, 4, 4, 4, 4, 4,         # Do Si(2) Sol La Sol Mi Sol
        4, 4, 4, 4, 4, 4, 4, 4,         # La Fa(2) Mi Re Si(h) La Sol
        4, 4, 4, 5, 5, 4, 4, 4,         # Sol La Si Do Mi Re(2)
        4, 4, 4, 4                      # Do(4)
    ]
    
    # Beat durations considering legato marks and dots
    # Standard beat is 0.5 seconds
    # Notes marked with (2) get 2× duration, (4) get 4× duration, etc.
    beat = [
        # First line
        0.5, 0.5, 0.5, 0.5, 0.5,                  # 0 0 0 Mi Sol
        0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,   # La Fa(2) Mi Re Do Re La Sol
        0.5, 0.5, 1.0, 0.5, 0.5, 0.5,             # La Sol Mi(2) Re Do
        0.5, 0.5,                                 # La(l) Do(l)
        0.5, 1.0, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5,   # Re Si(l,2) Fa Mi(2) Re Si
        
        # Second line
        0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,   # Do Si(2) Sol La Sol Mi Sol
        0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,   # La Fa(2) Mi Re Si(h) La Sol
        0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5,   # Sol La Si Do Mi Re(2)
        2.0, 0.5, 0.5, 0.5                        # Do(4) - - -
    ]
    
    name = 'YOASOBI_into_the_night'
    
    # Generate the music file
    wav_file = getmusic(score, beat, name, octaves)
    
    # Play the generated audio (optional)
    try:
        wave_obj = sa.WaveObject.from_wave_file(wav_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        print(f"Could not play audio: {e}")


