# Installation

```text
git clone https://github.com/dfirsec/magic_check.git
cd magic_check
pip install -r requirements.txt
```

## Simple Usage

```text
python check_magic.py -p {FILE PATH}
```

**_Option_**

```text
python check_magic.py -p {FILE PATH} -f {FILE FORMAT}
```

### Check for all file formats (from list below)

```text
python check_magic.py d:\Downloads\Ultimate_Guide_Arduino_Sensors_Modules

 PDF   d:\Downloads\Ultimate_Guide_Arduino\Ultimate_Guide_Arduino_Sensors_Modules.pdf
 ZIP   d:\Downloads\Ultimate_Guide_Arduino\1 - DHT11_DHT22\Code\DHT_library.zip
 JFIF  d:\Downloads\Ultimate_Guide_Arduino\1 - DHT11_DHT22\Schematics\Schematics.jpg
 PNG   d:\Downloads\Ultimate_Guide_Arduino\10 - Tilt\Schematics\Schematics.png
 PNG   d:\Downloads\Ultimate_Guide_Arduino\11 - Microphone Sound\Schematics\Schematics.png
 PNG   d:\Downloads\Ultimate_Guide_Arduino\12 - Reed Switch\Schematics\Magnetic_Reed_Switch.png
 ZIP   d:\Downloads\Ultimate_Guide_Arduino\13 - MRFC522 RFID\Code\RFID_Library.zip
 PNG   d:\Downloads\Ultimate_Guide_Arduino\13 - MRFC522 RFID\Schematics\RFID.png
 PNG   d:\Downloads\Ultimate_Guide_Arduino\14 - Relay\Schematics\Relay_Module.png
 ...
```

### Check by specified file format (from list below)...in this example, a `zip` file.

```text
python check_magic.py d:\Downloads\Ultimate_Guide_Arduino_Sensors_Modules -f zip

d:\Downloads\Ultimate_Guide_Arduino_Sensors_Modules\1 - DHT11_DHT22\Code\DHT_library.zip
d:\Downloads\Ultimate_Guide_Arduino_Sensors_Modules\13 - MRFC522 RFID\Code\RFID_Library.zip
d:\Downloads\Ultimate_Guide_Arduino_Sensors_Modules\15 - nRF24L01\Code\RadioHead_Library.zip
d:\Downloads\Ultimate_Guide_Arduino_Sensors_Modules\16 - 433 MHZ Transmitter_Receiver\Code\RadioHead_Library.zip
d:\Downloads\Ultimate_Guide_Arduino_Sensors_Modules\18 - Dot Matrix\Code\LedControl.zip
...
```

### File Formats and Magic Signature:

```text
file_types = {
    '7z': b'37 7a bc af 27 1c',
    'aac': b'41 41 43 00 01 00',
    'asm': b'00 61 73 6d',
    'avi': b'52 49 46 46',
    'au': b'64 6e 73 2e',
    'bin': b'53 50 30 31',
    'exe': b'4d 5a',
    'bmp': b'42 4d',
    'bz2': b'42 5a 68',
    'dat': b'50 4d 4f 43 43 4d 4f 43',
    'deb': b'21 3c 61 72 63 68 3e',
    'doc': b'cf 11 e0 a1 b1 1a e1 00',
    'elf': b'7f 45 4c 46',
    'flash': b'43 57 53',
    'flv': b'46 4c 56 01',
    'gif': b'47 49 46 38 37 61',
    'jfif': b'ff d8 ff e0 00 10 4a 46 49 46 00 01',
    'jpg': b'ff d8 ff db',
    'mkv': b'1a 45 df a3',
    'mp3': b'49 44 33',
    'mp3_hd': b'49 44 33 03 00 00 00',
    'mpeg': b'00 00 01 ba',
    'mpg2': b'00 00 01 ba 44',
    'ogg': b'4f 67 67 53',
    'pcap': b'd4 c3 b2 a1',
    'pcapng': b'0a 0d 0d 0a',
    'pdf': b'25 50 44 46 2d',
    'png': b'89 50 4e 47 0d 0a 1a 0a',
    'rar': b'52 61 72 21 1a 07 01 00',
    'raw': b'52 41 57 41 44 41 54 41',
    'reg': b'72 65 67 66',
    'rtf': b'7b 5c 72 74 66 31',
    'sqlite': b'53 51 4c 69 74 65 20 66 6f 72 6d 61 74 20 33 00',
    'tarv1': b'75 73 74 61 72 00 30 30',
    'tarv2': b'75 73 74 61 72 20 20 00',
    'vmdk': b'4b 44 4d',
    'vmem': b'53 ff 00 f0',
    'wmv': b'30 26 b2 75 8e 66 cf 11 a6 d9 00 aa 00 62 ce 6c',
    'xar': b'78 61 72 21',
    'xml': b'3c 3f 78 6d 6c 20',
    'zip': b'50 4b 03 04'
}
```
