from scipy.io import wavfile
from scipy.fftpack import fft 
import matplotlib.pyplot as plt
import numpy as np
import simpleaudio as sa
import wave
import struct
import os

def get_frequency(note_number, octave=4):
    """Convert a note number to its frequency.
    Integer notes: 1 = Do, 2 = Re, 3 = Mi, 4 = Fa, 5 = Sol, 6 = La, 7 = Si
    Flat notes: 1.5 = Do♭, 2.5 = Re♭, 3.5 = Mi♭, etc.
    Sharp notes: 0.5 = Si♯, 1.5 = Do♯, 2.5 = Re♯, etc.
    octave: 4 is middle octave, 5 is one octave higher, 3 is one octave lower
    """
    import math
    
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
    
    # Add flat/sharp notes
    # A flat note is calculated as the frequency of the note times 2^(-1/12)
    # A sharp note is calculated as the frequency of the note times 2^(1/12)
    semitone_factor = 2 ** (1/12)
    
    # Add flat notes (using the next note's frequency and dividing by the semitone factor)
    flat_notes = {
        1.5: base_frequencies[2] / semitone_factor,  # Do♯/Re♭ (C♯/D♭)
        2.5: base_frequencies[3] / semitone_factor,  # Re♯/Mi♭ (D♯/E♭)
        4.5: base_frequencies[5] / semitone_factor,  # Fa♯/Sol♭ (F♯/G♭)
        5.5: base_frequencies[6] / semitone_factor,  # Sol♯/La♭ (G♯/A♭)
        6.5: base_frequencies[7] / semitone_factor,  # La♯/Si♭ (A♯/B♭)
    }
    
    # Add these to our base frequencies dictionary
    base_frequencies.update(flat_notes)
    
    # Also add the special case for note 3.5 (which would be Mi♯/Fa♭, but Mi♯ is just Fa)
    base_frequencies[3.5] = base_frequencies[4] / semitone_factor
    
    # And note 7.5 (which would be Si♯, but Si♯ is just Do of the next octave)
    base_frequencies[7.5] = base_frequencies[1] * semitone_factor
    
    # Handle the case of note 0.5 (which would be Do♭ of the current octave,
    # or equivalently Si of the previous octave)
    base_frequencies[0.5] = base_frequencies[7] / semitone_factor
    
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
        score: List of integers representing notes (1 = Do, 2 = Re, etc., 0 = rest)
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
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Write to WAV file in the same directory as the script
    output_file = os.path.join(script_dir, f"{name}.wav")
    wavfile.write(output_file, sample_rate, audio)
    
    print(f"Music file created: {output_file}")
    return output_file

def scale_beat_by_bpm(beat, bpm, default_bpm=120):
    """
    Scale the beat durations according to the desired BPM.
    """
    scale = default_bpm / bpm
    return [b * scale for b in beat]

if __name__ == "__main__":

    # Original example: twinkle twinkle little star
    # score = [1, 1, 5, 5, 6, 6, 5]  # 1: Do, 2: Re, 3: Mi, ...
    # beat = [1, 1, 1, 1, 1, 1, 2]   # Duration in seconds
    # name = 'twinkle'
    
    # The score uses the following format: numbers are notes, '-' indicates a rest
    # The superscript 5 or 6 indicates a higher octave, dots below represent longer duration
    score_ver1 = [
        # First line: 0 0 0 3 5 | 6. 4 4 3 2 1 2 6 | 5 6 3 3 2. 1 (6 1 | 2. 7 7 4 3 3 2 7 |
        0, 0, 0, 3, 5,
        6, 4, 3, 2, 1, 2, 6,
        5, 6, 3, 2, 1,
        6, 1,
        2, 7, 4, 3, 2, 7,
        
        # Second line: i. 7 7 5 6 5) 3 5 | 6. 4 4 3 2 7 6 5 | 5 6 7 i i 3 2 2 | 1 - - - |
        1, 7, 7, 5, 6, 5, 3, 5,
        6, 4, 3, 2, 7, 6, 5,
        5, 6, 7, 1, 3, 2, 
        1, 0, 0, 0
    ]
    

    score_ver2 = [
        # First line
        5, 6.5, 
        1, 6, 5, 4, 3, 4, 1,
        6.5, 1, 5, 4, 3, 1, 3,
        4, 2, 5.5, 5, 5, 4, 2,
        2.5, 2, 6.5, 1, 6.5, 5, 6.5,

        # Second line
        1, 5.5, 5, 4, 2, 1, 6.5, 
        6.5, 1, 2, 3, 5, 4, 2.5,
        1, 3, 2, 5,
    ]


    
    # explain: (l) implies lower octave, (h) implies higher octave
    # explain: (2) means that the note has 2 times longer duration than others, and so on
    octaves_ver1 = [
        # First line
        4, 4, 4, 4, 4,                  # Mi Sol
        4, 4, 4, 4, 4, 4, 4,            # La Fa(2) Mi Re Do Re La Sol
        4, 4, 4, 4, 4,                  # La Sol Mi(2) Re Do
        3, 4,                           # La(l) Do(l)
        4, 3, 4, 4, 4, 3,               # Re Si(l, 2) Fa Mi Re Si
        
        # Second line 
        4, 3, 3, 3, 4, 4, 4, 4,         # Do Si(2) Sol La Sol Mi Sol
        4, 4, 4, 4, 4, 4, 4,            # La Fa(2) Mi Re Si(h) La Sol
        4, 4, 4, 5, 4, 4,               # Sol La Si Do Mi Re
        4, 4, 4, 4                      # Do(4)
    ]
    
    ocataves_ver2 = [
        # First line
        5, 5, 
        6, 5, 5, 5, 5, 5, 6,
        5, 6, 5, 5, 5, 5, 5,
    ]


    # Beat durations considering legato marks and dots
    # Standard beat is 0.5 seconds
    beat = [
        # First line
        0.5, 0.5, 0.5, 0.5, 0.5,                  # 0 0 0 Mi Sol
        0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5,        # La Fa(2) Mi Re Do Re La
        0.4, 0.5, 0.5, 0.5, 1.0,                  # Sol La Mi Re Do
        0.5, 0.5,                                 # La(l) Do(l)
        0.5, 1.0, 1.0, 0.5, 0.5, 0.5,             # Re Si(l,2) Fa Mi(2) Re Si
        
        # Second line
        0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,   # Do Si(2) Sol La Sol Mi Sol
        0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5,        # La Fa(2) Mi Re Si(h) La Sol
        0.5, 0.5, 0.5, 1.0, 0.5, 0.5,             # Sol La Si Do Mi Re
        2.0, 0.5, 0.5, 0.5                        # Do(4) - - -
    ]
    
    name = 'YOASOBI_into_the_night'
    
    bpm = 160  

    beat_ver1 = scale_beat_by_bpm(beat, bpm)

    wav_file = getmusic(score_ver1, beat_ver1, name, octaves_ver1)
    
    # Play the generated audio (optional)
    try:
        wave_obj = sa.WaveObject.from_wave_file(wav_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        print(f"Could not play audio: {e}")


