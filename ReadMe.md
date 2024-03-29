# Steg

A simple steganography application, written in Python delivered in various forms in several environments to demonstrate Python's versatility.

- `stegano.py` is the script that contains the core functions and can be executed from a development environment where Python and the required libraries are available.

- `tksteg` has a Graphical User Interface based on TkInter. It is delivered in the form of executables targeted at different OS environments (Windows, Linux, Darwin).

- `csteg` has a Command Line Interface. It is delivered as executables.

- `wsteg` is a web application, using `PyScript` as the script language embedded in a web page.


# Steganography

Steganography is the process to hide discretely information in a media, as defined in [Wikipedia](https://en.wikipedia.org/wiki/Steganography). 
A great many of GitHub projects involve steganography.

# The Steg project

The Steg project started as a student's project aiming at exploring the concept of steganography and beyond this, the
different ways to deliver a Python development to end-users.

# stegano.py

The present project limits itself to concealing a text in an image. This process is called "*encoding*", while the retrieval
of the text included in an image is called "*decoding*".

The Stegano class provides essentially 2 methods : `encode` and `decode`.


It uses the least significant bit of every channel and every pixel in an image to encode 1 bit of the information to be concealed.

It requires 

`$ pip install opencv-python` 

(preferably in a virtual environment) for reading/writing image files 
and can be executed with 

`$ python stegano.py`

where the `$` represents the command line prompt.

## Executables @ Windows

To build executables (`tksteg` and `csteg`) for Windows `cx_Freeze` is required:

`$ pip install cx-Freeze` 

And then

`$ python setup.py build `

To build installation file (msi file) for Windows 

`$ python setup.py bdist_msi`


## Executables @ Linux

To build an exe for Linux, first:

`$ pip install pyinstaller`

and then, either use the spec file:

`$ pyinstaller tksteg.spec`\
`$ pyinstaller csteg.spec`

or execute the following 1-line command (shown here for `tksteg` only):

`$ pyinstaller main.py --hiddenimport PIL --hiddenimport PIL._imagingtk --hiddenimport PIL._tkinter_finder --name tksteg --onefile`
