import pyaudio
import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write

fs = 44100

def isfloat(num):
    try: 
        float(num)
        return True
    except ValueError:
        return False


def noise_generator(amplitude, duration, fs): 
    t = np.linspace(0, duration, int(duration * fs), endpoint=False)
    noise = np.random.normal(0.5,0.1,(fs * duration))
    wave = amplitude * noise

    # Ramp the signal at the beginning and end
    window = int(fs * 0.25) # elements in first 1/4s
    ramp_vector = np.linspace(0, amplitude, num=window)
    wave[0:window] = ramp_vector

    end_window = len(wave) - window
    end_ramp = ramp_vector[::-1]
    wave[end_window:len(wave)] = end_ramp

    wave = wave * noise
    
    return wave.astype(np.float32)


def calibrate(amplitude):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True,
                    frames_per_buffer=1024)

    # Set paramters for the wave
    # amplitude = 0.2
    duration = 5

    wave = noise_generator(amplitude, duration, fs)

    while True:
        stream.write(wave)

        # Get user input and update the amplitude
        print(f"Previous Amplitude = {amplitude}")
        user_input = input("Enter a new amplitude value (0-1): ")
        if not isfloat(user_input): 
            return amplitude
        amplitude = float(user_input)
        wave = noise_generator(amplitude, duration, fs)


def wave_generator(base, peak): 
    duration = 10
   
    # Create the period for rising wave
    rise = np.linspace(base, peak, int(fs * 0.4))
    fall = np.linspace(peak, base,int(fs * 0.01) )
    base_vec = np.array(base)
    base_vec = np.repeat(base_vec, int(fs * 0.59))

    period = np.concatenate([rise, fall, base_vec])
    xT = np.linspace(0, 10, fs)
    x = np.linspace(0, 10, fs*10)

    # Repeat period for duration
    wave = np.tile(period, duration)

    noise = np.random.normal(0.5,0.1, (fs * duration))
    wave = wave * noise

    # Create background sound that plays noise at base amplitude
    # Test will last around 10-15 mins, 20min file made just to be sure
    background = np.array(base)
    background = np.repeat(background, fs * 1200) # 20 mins = 1200 seconds

    noise = np.random.normal(0.5, 0.1, fs * 1200)

    background = background * noise
    
    return wave.astype(np.float32), background.astype(np.float32)


if __name__ == "__main__":
    base = calibrate(0.2)
    peak = calibrate(0.7)

    wave, background = wave_generator(base, peak) 

    # pa = pyaudio.PyAudio()
    # stream = pa.open(format=pyaudio.paFloat32,
    #                 channels=1,
    #                 rate=fs,
    #                 output=True)
    
    # stream.write(wave)

    # stream.stop_stream()
    # stream.close()
    # pa.terminate
    write("auditory_looming_stimulus.wav", fs, wave)
    write("background_noise.wav", fs, background)
