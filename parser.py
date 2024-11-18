from utils import *


class OsuFileParser:
    def __init__(self):
        self.data = {}
        self.timing = []
        self.objects = []
        self.keys = 4
        self.bg = ''

    def parse(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            section = None
            for line in file:
                line = line.strip()
                if not line or line.startswith('//'):
                    continue
                elif line.startswith('[') and line.endswith(']'):
                    section = line[1:-1]
                    self.data[section] = {}
                else:
                    self.parse_line(line, section)

    def parse_line(self, line, section):
        import re
        match = re.match(r'(\w+):(.*)', line)
        match_time = re.match(r'([\w.]+)(,(.*))+', line)
        if match:
            key, value = match.groups()
            if section:
                if not key.startswith("AI"):
                    self.data[section][key] = convert_value(value)
            if section == 'Difficulty' and key == 'CircleSize':
                self.keys = convert_value(value)
        elif match_time:
            parts = line.split(',')
            if len(parts) == 6:
                common = parse_common_parts(parts)

                from math import floor
                hit_object = {
                    'x': floor(self.keys * common[0] / 512),
                    'y': common[1],
                    'time': common[2],
                    'object_type': common[3],
                    'end': common[4],
                }
                self.objects.append(hit_object)
            elif len(parts) == 8:
                self.timing.append(parse_timing_point(line))
            elif len(parts) == 5 and self.bg == '':
                # print(parts)
                if parts[2].endswith('.jpg"') or parts[2].endswith('.png"'):
                    self.bg = parts[2][1:-1]

    def get_data(self):
        return self.data

    def get_timing(self):
        return self.timing

    def get_objects(self):
        return self.objects

    def get_bg(self):
        return self.bg

    def convert_simai_header(self):
        header = "&title=" + self.data['Metadata']['TitleUnicode'] + '\n'
        header = header + "&artist=" + self.data['Metadata']['ArtistUnicode'] + '\n'
        header = header + "&first=" + str(self.timing[0]['Offset'] / 1000) + '\n'
        header = header + "&des=" + AUTHOR + '\n'
        header = header + "&wholebpm=" + self.timing[0]['BPM'] + '\n'
        header = header + "&lv_5={}\n&inote_5=".format(LEVEL)

        simai = ''

        _STEPS = 96
        cur_bpm_pointer = 0
        cur_time = self.timing[0]['Offset']
        time_step = self.timing[0]['BeatLength'] * 4 / _STEPS
        cur_note = 0
        sub_count = 0

        _size = len(self.objects)
        _timing_size = len(self.timing)
        while cur_note < _size:
            note_str = ''
            first_note = True
            while cur_bpm_pointer < _timing_size and self.timing[cur_bpm_pointer]['Offset'] <= round(cur_time):
                if self.timing[cur_bpm_pointer]['BPM'] != '-1':
                    # print(self.timing[cur_bpm_pointer]['BPM'])
                    last_bpm = self.timing[cur_bpm_pointer]['BeatLength']
                    note_str = note_str + '\n(' + self.timing[cur_bpm_pointer]['BPM'] + ')'
                    time_step = last_bpm * 4 / _STEPS
                    sub_count = 0
                cur_bpm_pointer += 1
            if sub_count == 0:
                note_str = note_str + '\n{96}'
                sub_count = _STEPS
            lst_notes = []
            same_notes = False
            while cur_note < _size and self.objects[cur_note]['time'] <= round(cur_time):
                if (not SAME) and same_notes:
                    cur_note += 1
                    continue
                if first_note:
                    first_note = False
                else:
                    note_str = note_str + '/'
                    same_notes = True
                new_note = note_to_str(self.objects[cur_note], self.timing[0]['BeatLength'] * 4, self.keys, lst_notes)
                lst_notes.append(new_note)
                note_str = note_str + new_note
                cur_note += 1
            if note_str is not None:
                simai = simai + note_str + ','
                sub_count -= 1
            cur_time += time_step

        simai = simai + '\nE\n'

        reduce_result = ''
        for line in simai.splitlines():
            reduce_result = reduce_result + compress_dashes(line) + '\n'

        return header + reduce_result

    def convert_ongeki_header(self):
        header = "Header.Version\t:\t1.0.0\n"
        header += "Header.Creator\t:\t{}\n".format(AUTHOR)
        header += "Header.FirstBpm\t:\t{}\n".format(self.timing[0]['BPM'])
        header += "Header.CommonBpm\t:\t{}\n".format(self.timing[0]['BPM'])
        header += "Header.MaximumBpm\t:\t{}\n".format(self.timing[0]['BPM'])
        header += "Header.MinimumBpm\t:\t{}\n".format(self.timing[0]['BPM'])
        header += "Header.Meter\t:\t4 / 4\n"
        header += "Header.TRESOLUTION\t:\t1920\n"
        header += "Header.XRESOLUTION\t:\t4096\n"
        header += "Header.ClickDefinition\t:\t1920\n"
        header += "Header.Tutorial\t:\tFalse\n"
        header += "Header.BeamDamage\t:\t2\n"
        header += "Header.HardBulletDamage\t:\t2\n"
        header += "Header.DangerBulletDamage\t:\t4\n"
        header += "Header.BulletDamage\t:\t1\n"
        header += "Header.ProgJudgeBpm\t:\t{}\n".format(240)

        header += "\n\n\n\n\n"

        output_tap = []
        output_hold = []

        beat_len = self.timing[0]['BeatLength'] * 4
        start = self.timing[0]['Offset']
        tot_len = 0

        for note_id, obj in enumerate(self.objects):
            x_value = ONGEKI_KEYS[obj['x']-1]
            measure, position = time_to_measure(obj['time'] - start, beat_len)
            tot_len = max(tot_len, measure)

            if obj['object_type'] <= 5:
                line = f"Tap\t:\t{obj['x']}\t:\tX[{x_value},0], T[{measure},{position}], C[False]"
                output_tap.append(line)

            elif obj['object_type'] == 128:
                end_measure, end_position = time_to_measure(obj['end'] - start, beat_len)
                line = (f"Hold\t:\t{obj['x']}, False, False\t:\t"
                        f"(X[{x_value},0], T[{measure},{position}])\t->\t"
                        f"(X[{x_value},0], T[{end_measure},{end_position}])")
                output_hold.append(line)
                tot_len = max(tot_len, end_measure)

        header += "Lane: 2:    (Type[LRS], X[{}, 0], T[0, 0])    ->    (Type[LRE], X[{}, 0], T[{}, 0])\n".format(
            ONGEKI_KEYS[2], ONGEKI_KEYS[2], tot_len)
        header += "Lane: 5:    (Type[LRS], X[{}, 0], T[0, 0])    ->    (Type[LRE], X[{}, 0], T[{}, 0])\n\n".format(
            ONGEKI_KEYS[5], ONGEKI_KEYS[5], tot_len)
        header += "Lane: 0:    (Type[LLS], X[{}, 0], T[0, 0])    ->    (Type[LLE], X[{}, 0], T[{}, 0])\n".format(
            ONGEKI_KEYS[0], ONGEKI_KEYS[0], tot_len)
        header += "Lane: 3:    (Type[LLS], X[{}, 0], T[0, 0])    ->    (Type[LLE], X[{}, 0], T[{}, 0])\n\n".format(
            ONGEKI_KEYS[3], ONGEKI_KEYS[3], tot_len)
        header += "Lane: 1:    (Type[LCS], X[{}, 0], T[0, 0])    ->    (Type[LCE], X[{}, 0], T[{}, 0])\n".format(
            ONGEKI_KEYS[1], ONGEKI_KEYS[1], tot_len)
        header += "Lane: 4:    (Type[LCS], X[{}, 0], T[0, 0])    ->    (Type[LCE], X[{}, 0], T[{}, 0])\n\n".format(
            ONGEKI_KEYS[4], ONGEKI_KEYS[4], tot_len)

        return header + "\n\n\n\n\n" + '\n'.join(output_tap) + "\n\n\n\n\n" + '\n'.join(output_hold)
