import os
from tqdm import tqdm
import shutil

###Settings###
target_dir = r'<add/your/target_dir/here>' #dir you want to analyse
sorted_out_dir = r'<add/your/sorted_out_dir/here>' #dir you want to move all the double pictures

###Script###
def is_valid_path(path) -> bool:
    return os.path.exists(path)

def create_file_size_dict(directory) -> dict:
    file_size_dict = {}
    
    for filename in tqdm(os.listdir(directory)):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            if file_size in file_size_dict:
                file_size_dict[file_size].append(file_path)
            else:
                file_size_dict[file_size] = [file_path]
    
    return file_size_dict

def find_duplicate_file_paths(file_size_dict) -> list:
    duplicate_file_paths = [file_paths for file_paths in file_size_dict.values() if len(file_paths) > 1]
    return duplicate_file_paths

def get_files_to_move(duplicate_file_paths) -> list:
    to_move_files = []
    for file_paths in duplicate_file_paths:
        # Keep the first file and move the rest
        to_move_files.extend(file_paths[1:])
    
    return to_move_files

def move_files_from_list(file_list, target_directory) -> None:
    for file_path in tqdm(file_list):
        filename = os.path.basename(file_path)
        new_file_path = os.path.join(target_directory, filename)

        if not os.path.exists(new_file_path):
            shutil.move(file_path, new_file_path)

def main() -> None:
    global target_dir
    global sorted_out_dir
    input('press to continue...')
    if not (is_valid_path(target_dir) and is_valid_path(sorted_out_dir)):
        print('invalid path...')
        return

    file_size_dict = create_file_size_dict(target_dir)
    duplicate_file_paths = find_duplicate_file_paths(file_size_dict)
    files_to_move = get_files_to_move(duplicate_file_paths)
    move_files_from_list(files_to_move,sorted_out_dir)
    print(f'moved files: {len(files_to_move)}/{len(file_size_dict)+len(files_to_move)}')

if __name__ == '__main__':
    main()