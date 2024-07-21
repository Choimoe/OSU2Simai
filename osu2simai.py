import sys

from osuIO import *

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python osu2simai.py input.osz")
        sys.exit(1)

    zip_path = sys.argv[1]
    # zip_path = '889405 Sakuzyo - Fracture Ray.osz'
    unzip_to_temp(zip_path, TEMP_DIR)
    named_folder = create_named_folder(zip_path)
    osu_file_path = list_and_select_osu_file(TEMP_DIR)
    process_osu_file(osu_file_path, named_folder)
    shutil.rmtree(TEMP_DIR)
