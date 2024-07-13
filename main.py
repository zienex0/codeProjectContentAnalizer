import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from termcolor import colored
from pprint import pprint


def project_directory_path():
    root = tk.Tk()
    root.withdraw()

    directory_path = filedialog.askdirectory(initialdir=Path.home(), title="Select Project Directory")

    if directory_path:
        return Path(directory_path)
    else:
        return None


class FileInfo:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.content_lines = None
        self.line_count = 0
        self.white_spaces = 0
        self.word_count = {}

        self.get_info_from_file(file_path=file_path)
        self.count_words()

    def get_info_from_file(self, file_path: Path):
        if file_path.is_dir():
            raise ValueError(f"Chosen path '{file_path}' is a directory, not a file.")
        
        with file_path.open() as f:
            self.content_lines = [line.strip() for line in f.readlines()]
            self.line_count = len(self.content_lines)
            self.white_spaces = self.content_lines.count('')

    def count_words(self):
        for word in self.content_lines:
            if word in self.word_count:
                self.word_count[word] += 1
            else:
                self.word_count[word] = 1
        
        self.word_count = sorted(self.word_count.items(), key=lambda x: x[1], reverse=True)


def read_all_files(directory_path: Path, valid_extensions: list[str]):
    files = []

    print("All file paths found in project", 'green')
    if directory_path.is_dir():
        for path in directory_path.iterdir():
            if path.is_dir() and not is_secret(path):
                print(colored(str(path), 'green'))
                files.extend(read_all_files(path, valid_extensions))

            elif path.is_file() and not is_secret(path):
                if has_valid_extension(path, valid_extensions):
                    print(colored(str(path), 'green'))
                    file = FileInfo(path)
                    files.append(file)
                else:
                    print(colored(f"Skipping {path} due to invalid extension", 'yellow'))

    return files


def has_valid_extension(file_path: Path, valid_extensions: list[str]):
    return file_path.suffix.lower() in valid_extensions


def is_secret(path: Path):
    splited = str(path).split('/')
    for splited_part in splited:
        if splited_part.startswith('.'):
            return True
    return False


def analyze_all_files(files_info: list[FileInfo]):
    all_lines = 0
    longest_file = None
    shortest_file = None
    white_spaces = 0

    for file in files_info:
        all_lines += file.line_count
        white_spaces += file.white_spaces

        if longest_file is None or file.line_count > longest_file.line_count:
            longest_file = file

        if shortest_file is None or file.line_count < shortest_file.line_count:
            shortest_file = file

    return {
        'all_lines_in_project': all_lines,
        'white_spaces_total': white_spaces,
        'longest_file': str(longest_file.file_path) + '|' + str(longest_file.line_count) + 'lines' if longest_file else None,
        'shortest_file': str(shortest_file.file_path) + '|' + str(shortest_file.line_count) + 'lines' if shortest_file else None,
    }


if __name__ == "__main__":
    print(colored('Please select your project directory in a new window', 'green'))

    selected_directory = project_directory_path()
    if selected_directory:
        print(f"Selected directory path: {selected_directory}")
        valid_extensions = ['.txt', '.py'] 
        result = read_all_files(selected_directory, valid_extensions)
        analyzed = analyze_all_files(result)
        pprint(analyzed)
    else:
        print(colored("No directory selected or operation canceled.", 'red'))
