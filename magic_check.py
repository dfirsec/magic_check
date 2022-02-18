"""Confirm file type by matching the magic number/signature."""

import argparse
import binascii
import sys
from os import scandir
from pathlib import Path

from colorama import Fore, Style, init

AUTHOR = "DFIRSec (@pulsecode)"
VERSION = "v0.0.5"

# Credit:
# https://www.garykessler.net/library/file_sigs.html
# https://asecuritysite.com/forensics/magic

filesigs = {
    "7z": b"37 7a bc af 27 1c",
    "aac": b"41 41 43 00 01 00",
    "asm": b"00 61 73 6d",
    "avi": b"52 49 46 46",
    "au": b"64 6e 73 2e",
    "bin": b"53 50 30 31",
    "exe": b"4d 5a 90 00",
    "bmp": b"42 4d",
    "bz2": b"42 5a 68",
    "cab": b"4d 53 43 46",
    "class": b"ca fe ba be",
    "dat": b"50 4d 4f 43 43 4d 4f 43",
    "deb": b"21 3c 61 72 63 68 3e",
    "doc": b"cf 11 e0 a1 b1 1a e1 00",
    "docx": b"50 4b 03 04",
    "elf": b"7f 45 4c 46",
    "flac": b"66 4c 61 43",
    "flash": b"43 57 53",
    "flv": b"46 4c 56 01",
    "ico": b"00 00 01 00",
    "gif87a": b"47 49 46 38 37 61",
    "gif89a": b"47 49 46 38 39 61",
    "gz": b"1f 8b 08",
    "gzip": b"1f 8b 08",
    "jar": b"50 4b 03 04 14 00 08 00 08 00",
    "jfif": b"ff d8 ff e0 00 10 4a 46 49 46 00 01",
    "jpg": b"ff d8 ff db",
    "luac": b"1b 4c 75 61",
    "lz4": b"04 22 4d 18",
    "mdb": b"53 74 61 6e 64 61 72 64 20 4a 65 74",
    "mkv": b"1a 45 df a3",
    "mlv": b"4d 4c 56 49",
    "mp3": b"49 44 33",
    "mp3_hd": b"49 44 33 03 00 00 00",
    "mpeg": b"00 00 01 ba",
    "mpg2": b"00 00 01 ba 44",
    "msg": b"d0 cf 11 e0 a1 b1 1a e1",
    "ogg": b"4f 67 67 53",
    "ovpn": b"63 6c 69 65 6e 74 0a 64 65 76",
    "pcap": b"d4 c3 b2 a1",
    "pcapng": b"0a 0d 0d 0a",
    "pdf": b"25 50 44 46 2d",
    "png": b"89 50 4e 47 0d 0a 1a 0a",
    "pptx": b"50 4b 03 04",
    "psd": b"38 42 50 53",
    "rar": b"52 61 72 21 1a 07 01 00",
    "raw": b"52 41 57 41 44 41 54 41",
    "reg": b"72 65 67 66",
    "rpm": b"ed ab ee db",
    "rtf": b"7b 5c 72 74 66 31",
    "sqlite": b"53 51 4c 69 74 65 20 66 6f 72 6d 61 74 20 33 00",
    "tar": b"75 73 74 61 72",
    "tif": b"49 49 2a 00",
    "tor": b"64 38 3a 61 6e 6e 6f 75 6e 63 65",
    "vmdk": b"4b 44 4d",
    "vmem": b"53 ff 00 f0",
    "webp": b"52 49 46 46 94 45 0a 00 57 45 42 50 56 50 38",
    "wmf": b"d7 cd c6 9a",
    "wmv": b"30 26 b2 75 8e 66 cf 11 a6 d9 00 aa 00 62 ce 6c",
    "xar": b"78 61 72 21",
    "xlsx": b"50 4b 03 04",
    "xml": b"3c 3f 78 6d 6c",
    "zip": b"50 4b 03 04",
    "zlib": b"78 9c",
}

# terminal colors
init()  # initialize colorama
BOLD = Fore.LIGHTWHITE_EX
CYAN = Fore.CYAN
GRAY = Fore.LIGHTBLACK_EX
GREEN = Fore.LIGHTGREEN_EX
RED = Fore.RED
YELLOW = Fore.LIGHTYELLOW_EX
RESET = Style.RESET_ALL


def get_file_header(path) -> bytes:
    """Grab the first 20 bytes of the file header.

    Args:
        path: Full path to file

    Returns:
        bytes: String of hex bytes representing the file signature
    """
    num_bytes = 20
    with open(path, "rb") as infile:
        header = infile.read(num_bytes)
    return header


def dirscanner(path: Path):
    """Scans directory and grab file headers.

    Args:
        path (Path): Full path to file

    Yields:
        generator: Generator of hex representation of the binary data
    """
    with scandir(path) as enum_dir:
        try:
            for files in enum_dir:
                if not files.name.startswith(".") and files.is_file():
                    file_obj = get_file_header(files)
                    yield binascii.hexlify(file_obj, " "), files.path
        except PermissionError as perm_err:
            print(perm_err)
        except FileNotFoundError as file_err:
            sys.exit(file_err)


def get_results(path: Path, filetype=None):
    """Yield the results of file matches.

    Args:
        path (Path): Full path to file
        filetype (str, optional): File extension. Defaults to None.

    Yields:
        generator: Generator of file matches
    """
    for (header, filepath) in dirscanner(path):
        if filetype:
            if filetype == filepath.split(".")[1] and filesigs[filetype] in header:
                yield f" {BOLD}{filetype.upper():7}{RESET}{filepath}"
        # if no filetype, yield all file results
        else:
            for ext, byte_str in filesigs.items():
                if byte_str in header:
                    yield f" {BOLD}{ext.upper():7}{RESET}{filepath}"


def main(path: Path, filetype):
    """Main program execution.

    Args:
        path (Path): Full path to file
        filetype (str): File extension
    """
    found = "\n".join(list(get_results(path, filetype)))

    if found:
        print(found)
    else:
        print(f"{YELLOW}[-] No matching file types found for '{filetype}'.{RESET}")


if __name__ == "__main__":
    banner = fr"""
        __  ___            _         ________              __
       /  |/  /___ _____ _(_)____   / ____/ /_  ___  _____/ /__
      / /|_/ / __ `/ __ `/ / ___/  / /   / __ \/ _ \/ ___/ //_/
     / /  / / /_/ / /_/ / / /__   / /___/ / / /  __/ /__/ ,<
    /_/  /_/\__,_/\__, /_/\___/   \____/_/ /_/\___/\___/_/|_|
                 /____/
                                                {VERSION}
                                                {AUTHOR}
    """

    print(f"{CYAN}{banner}{RESET}")

    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to search")
    parser.add_argument("-f", "--filetype", help="file type selector")
    parser.add_argument("-l", "--listtype", action="store_true", help="list file types")

    args = parser.parse_args()

    if args.listtype:
        print(f"{GREEN}Choose from the following:{RESET}")
        print("\n".join(list(filesigs.keys())))
    elif args.filetype:
        try:
            main(args.path, args.filetype.lower())
        except KeyError:
            sys.exit(f"[x] File format '{YELLOW}{args.filetype}{RESET}' is not an available selection.")
        except NotADirectoryError as dir_err:
            print(dir_err)
    else:
        try:
            main(args.path, filetype=None)
        except NotADirectoryError as dir_err:
            print(dir_err)
