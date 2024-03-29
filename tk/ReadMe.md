# tksteg #

`tksteg` uses a a Graphical User Interface based on TkInter to feed the Stegano class.

Available for Windows and Linux.

Checked on Windows 10 and Ubuntu Focal Fossa 20.4.

## Usage

Double-click the icon (Windows, Linux) or execute from the command line (Linux) to display the Graphical User Interface.

"Encode" means "merge the text in the picture".

Conversely, "Decode" is for extracting a text from a picture.

Tksteg builds a log file ("tksteg.log").

## Known limitations

Image files having non-ASCII chars in their path or name may not be loaded because CV2 fails to open them. A workaround is to move and/or rename such files to avoid non-ASCII chars.
This behaviour is observed on Windows, not in Linux.

Text files exceeding image capacity are truncated.

Alerts are issued and warnings are logged when this happens.

Encoded images cannot be saved in JPG because its compression scheme looses the information on low-weight bits.
Suitable image formats are proposed, like PNG.
