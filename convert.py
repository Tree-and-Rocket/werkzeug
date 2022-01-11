import numpy as np
from scipy.io import wavfile
from PIL import Image


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def interp1d(in_array, new_len, dtype=np.double):
    array_length = len(in_array)
    x = np.linspace(0, array_length - 1, num=new_len)
    y = np.arange(array_length)
    return np.interp(x, y, in_array).astype(dtype)


def img2wav(img_filename, fps=23.98, sample_rate=48000, frame_count=128.0):
    encoded_img = Image.open(img_filename)
    img_data = np.asarray(encoded_img).flatten()
    # every 3 pixels = 1 wave byte
    wav_data = np.empty(round(img_data.size / 3), dtype=np.int16)
    idx = 0
    import warnings
    for i in range(img_data.size):
        if i % 3 == 0:
            # remap from 3 x 0..255 to -32.768 .. 32.768
            wav_data[idx] = (int(img_data[i]) + int(img_data[i + 1]) + int(img_data[i + 2])) / 768 * 65536 - 32768
            idx += 1

    wav_length = round(1/fps * sample_rate * frame_count)
    return interp1d(wav_data, wav_length, dtype=np.int16)


def wav2img(wav_filename, fps=23.98, start_frame=0.0, frame_count=128.0, out_width=2048, out_height=1024):
    sample_rate, wave_data = wavfile.read(wav_filename)
    wav_sample_start = round(1 / fps * start_frame * sample_rate)
    wav_sample_end = round(wav_sample_start + 1 / fps * frame_count * sample_rate)

    # check channel count
    if len(wave_data.shape) > 1:
        print('Error: Only wav files with 1 channel (mono) are supported')
        return False

    # check 16-Bit PCM
    if wave_data.dtype != np.int16:
        print('Error: Only wav files with 16-Bit PCM are supported')
        return False

    # check wav length
    if wav_sample_end > wave_data.size:
        print('Error: Requested end sample "' + str(wav_sample_end) + '" is after the last sample "' + str(
            wave_data.size) + '" of ' + wav_filename)
        return False

    # trim array to start / end
    wave_data = wave_data[wav_sample_start:wav_sample_end].astype(np.double)
    # remap from -32.768 .. 32.768 to 0.0 .. 768.0 --> (x+32768) / 65536 * 768
    wave_data = (wave_data + 32768) / 65536 * 768
    # resample / stretch to output image size
    out_pixel_count = out_width * out_height
    resampled_wave = interp1d(wave_data, out_pixel_count)
    # convert np array to image
    np_wave_data = np.empty([out_height, out_width, 3], dtype=np.uint8)

    for y in range(out_height):
        for x in range(out_width):
            idx = y * out_width + x
            np_wave_data[y, x, 0] = clamp(resampled_wave[idx], 0, 255)
            np_wave_data[y, x, 1] = clamp(resampled_wave[idx] - 256, 0, 255)
            np_wave_data[y, x, 2] = clamp(resampled_wave[idx] - 512, 0, 255)

    return Image.fromarray(np_wave_data)


# end to end example
# img = wav2img('STAR-TREK-TNG-S1-D1_1_mono_16bit_48000hz_5.33s.wav', out_width=1024, out_height=512)
# img.save('encoded.png')
# wav = img2wav('encoded.png')
# wavfile.write('reencoded.wav', 48000, wav)
