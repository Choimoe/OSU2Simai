from config import *
import numpy as np


def convert_value(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            if ',' in value:
                return [int(i) for i in value.split(',')]
            return value


def closest_fraction(x, y):
    target = x / y
    max_denominator = 96
    from fractions import Fraction
    fraction = Fraction(target).limit_denominator(max_denominator)
    return fraction.numerator, fraction.denominator


def compress_dashes(input_str):
    from math import gcd
    import re
    parts = re.split('(,+)', input_str)
    data_parts = parts[::2]
    dash_parts = parts[1::2]

    _gcd = 96
    for i in dash_parts:
        _gcd = gcd(_gcd, len(i))

    new_dash_counts = [len(i) // _gcd for i in dash_parts]

    new_str = re.sub(r'\{.*?}', '{' + str(96 // _gcd) + '}', data_parts[0])
    for i in range(len(dash_parts)):
        new_str += ',' * new_dash_counts[i] + data_parts[i + 1]

    return new_str


def parse_timing_point(timing_string):
    parts = timing_string.split(',')

    offset = float(parts[0])
    bpm = round(60000 / float(parts[1])) if float(parts[1]) > 0 else -1
    time_signature = int(parts[2])
    meter_time = int(parts[3])
    inherit = bool(int(parts[4]))
    volume = int(parts[5])
    effects = bool(int(parts[6]))
    sample_set = int(parts[7])

    return {
        'Offset': offset,
        'BPM': str(bpm),
        'BeatLength': float(parts[1]) if float(parts[1]) > 0 else -1,
        'Time Signature': f"{time_signature}/{meter_time}",
        'Inherited': inherit,
        'Volume': volume,
        'Effects': effects,
        'Sample Set': sample_set
    }


def parse_common_parts(para):
    x = int(para[0])
    y = int(para[1])
    time = int(para[2])
    note_type = int(para[3])
    para = int(para[5].split(':')[0])
    return x, y, time, note_type, para


def note_to_str(param, beatLength, key_num, prev):
    note_pos = KEYS[key_num][param['x']]
    if RANDOM:
        if RANDOM == 2:
            if note_pos == 4:
                note_pos = np.random.randint(low=1, high=5)
            else:
                note_pos = np.random.randint(low=5, high=9)
        else:
            note_pos = np.random.randint(low=1, high=9)
            while note_pos in prev:
                note_pos = np.random.randint(low=1, high=9)

    if param['object_type'] != 128:
        return str(note_pos)
    else:
        note_length = param['end'] - param['time']
        beat_len, beat_fac = closest_fraction(note_length, beatLength)
        return str(note_pos) + 'h[{}:{}]'.format(beat_fac, beat_len)
