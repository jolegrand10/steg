# csteg

`csteg` uses a command line interface to feed the Stegano class.

Encode means merging a text in a picture.

Decode retrieves the text encoded in a picture.

Checked on Windows 10 and Ubuntu Focal Fossa 22.04

## Usage

`$ csteg [-h] [-a ACTION] --pic PIC [-o OUTFILE] [-i INFILE] [-v] `

Two way steganography.

'encode' merges a text in an image.

'decode' retrieves the text from an image.

options:

  `-h, --help `          show this help message and exit

  `-a ACTION, --action ACTION`    Specify encode or decode

  `--pic PIC`             Path to the picture file

  `-o OUTFILE, --output OUTFILE`  Output file. Pic or text, depending on action. Default is stdout.

  `-i INFILE, --input INFILE`      Input file. Text. Default is stdin.

  `-v, --verbose`        Show details

## Known limitations

### Redirections in Windows

`csteg` uses UTF-8 to encode/decode text files. 
In Windows, if the standard output is redirected, the local shell 
(cmd, powershell) will involve its own text encoding (possibly cp1252 or UTF-16) with the consequence that
that the output of a `csteg` step will be messed. 

Workarounds are discussed in [StackOverflow](https://stackoverflow.com/questions/56724398/windows-encoding-changed-when-redirecting-output)

### Usage as a script

Using `csteg` as a script with `$ python -m csteg` requires the python libraries to be installed, preferably in a virtual environment, with:

`$ pip install -r requirements.txt`

This is not required when using the standalone `csteg` executable resulting from 

`$ pyinstaller csteg.spec` on Unix systems, or from

`$ python setup.py ...` on Windows 10.