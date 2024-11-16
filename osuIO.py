import os
import shutil
import zipfile

from config import *
from parser import *


def unzip_to_temp(zip_path, temp_dir='./tmp'):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)


def create_named_folder(zip_path, base_dir='./'):
    zip_name = os.path.splitext(os.path.basename(zip_path))[0]
    named_folder = os.path.join(base_dir, zip_name)
    if not os.path.exists(named_folder):
        os.makedirs(named_folder)
    return named_folder


def rename_and_move_file(src_dir, dst_dir, file_name, FILE_MODE=1):
    file_base, file_ext = os.path.splitext(file_name)
    if FILE_MODE == 1:
        new_name = f"track{file_ext}"
    else:
        new_name = f"BG{file_ext}"

    src_file = os.path.join(src_dir, file_name)
    dst_file = os.path.join(dst_dir, new_name)

    if os.path.exists(src_file):
        shutil.move(src_file, dst_file)
    else:
        print(f"File {file_name} not found in {src_dir}")


def list_and_select_osu_file(temp_dir):
    osu_files = [f for f in os.listdir(temp_dir) if f.endswith('.osu')]
    if not osu_files:
        raise FileNotFoundError("No .osu files found in the temporary directory.")

    print("Found the following .osu files:")
    for idx, osu_file in enumerate(osu_files, 1):
        print(f"{idx}: {osu_file}")

    choice = int(input("Select the .osu file to process (by number): ")) - 1
    return os.path.join(temp_dir, osu_files[choice])


def process_osu_file(osu_path, output_dir, name='maidata.txt'):
    parser = OsuFileParser()
    parser.parse(osu_path)
    if ONGEKI:
        result = parser.convert_ongeki_header()
        name = 'out.nyageki'
    else:
        result = parser.convert_simai_header()
    rename_and_move_file(TEMP_DIR, output_dir, parser.get_data()['General']['AudioFilename'].strip())
    if parser.get_bg().strip() != '':
        rename_and_move_file(TEMP_DIR, output_dir, parser.get_bg().strip(), 2)
    output_file = os.path.join(output_dir, name)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(result)
