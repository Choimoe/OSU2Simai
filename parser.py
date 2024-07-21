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
        match_time = re.match(r'(\w+)(,(.*))+', line)
        if match:
            key, value = match.groups()
            if section:
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
            while cur_note < _size and self.objects[cur_note]['time'] <= round(cur_time):
                if first_note:
                    first_note = False
                else:
                    note_str = note_str + '/'
                note_str = note_str + note_to_str(self.objects[cur_note], self.timing[0]['BeatLength'] * 4, self.keys)
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
