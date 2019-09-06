# OpenCVMarkerPrinter

## Description
This small app can save some commonly used opencv markers such as ArUco, ArUcoGrid, Chessboard and ChArUco to vector graphics file. **Supported vector graphics file format: .svg, .pdf and .ps.**

<img src="./doc/images/0001.jpg" height="160" />

### Dependencies
#### MarkerPrinter
  * numpy
  * PIL(Pillow, for image processing)
  * cairo(for drawing vector graphic)
  * cairosvg(for svg to png)

#### MarkerPrinterGUI
  * tkinter(for GUI)
  
#### Install

## Tutorial
### Seletct dictionary:
<img src="./doc/images/0002.jpg" height="200" />

### Modify size:
<img src="./doc/images/0003.jpg" height="200" />

### Modify border:
<img src="./doc/images/0004.jpg" height="200" />

## Useful Options:
### Divde output to chunks
If you are using consumer level printer, you will suffer from not able printing too large marker, so just set subSize before saving the marker to files, it will divide output marker to chunks.
<img src="./doc/images/0005.jpg" height="400" />