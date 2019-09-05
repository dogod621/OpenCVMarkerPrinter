# OpenCVMarkerPrinter

## Description
This small app can save some commonly used opencv markers such as ArUco, ArUcoGrid, Chessboard and ChArUco to vector graphics file. **Supported vector graphics file format: .svg, .pdf and .ps. Supported image file format: .png (not recommend).**

<img src="./doc/images/0001.jpg" height="160" />

### Dependencies
#### MarkerPrinter
  * numpy
  * opencv-python
  * opencv-contrib-python
  * cairo(for drawing vector graphic)
  * cairosvg(for svg to png)

#### MarkerPrinterGUI
  * tkinter(for GUI)
  * PIL(Pillow, for image processing)

## Tutorial
### Seletct dictionary:
<img src="./doc/images/0002.jpg" height="200" />

### Modify size:
<img src="./doc/images/0003.jpg" height="200" />
<img src="./doc/images/0004.jpg" height="200" />

### Modify border:
<img src="./doc/images/0005.jpg" height="200" />

## Useful Options:
### Divde output to chunks
If you are using consumer level printer, you will suffer from not able printing too large marker, so just set subSize before saving the marker to files, it will divide output marker to chunks.
<img src="./doc/images/0006.jpg" height="400" />

## Note:
### Why PNG is not recommend
PNG will suffer from artifact problem after scaling:
<img src="./doc/images/0008.jpg" height="200" />

### Algorithm
This application use "wall follower maze solving algorithm" to draw the marker, and it is useful to avoid some problems.
<img src="./doc/images/0007.jpg" height="400" />