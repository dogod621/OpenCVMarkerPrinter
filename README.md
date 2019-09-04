# OpenCVMarkerPrinter

## Description
This small app can save some commonly used opencv markers such as ArUco, Chessboard and ChArUco to vector graphics file. **Supported vector graphics file format: .svg, .pdf and .ps. Supported image file format: .png (not recommend).**

<img src="https://user-images.githubusercontent.com/6807005/64227508-64453c80-cf16-11e9-8a96-3b962e094956.jpg" height="200" />

### Dependencies
**MarkerPrinter:**  
numpy,  
opencv-python,  
opencv-contrib-python,  
cairo(for drawing vector graphic),  
cairosvg(for svg to png)  

**MarkerPrinterGUI:**  
tkinter(for GUI),  
PIL(Pillow, for image processing)  

## Tutorial
### Seletct dictionary:
<img src="https://user-images.githubusercontent.com/6807005/64227509-64453c80-cf16-11e9-9304-7cbbc87eb00f.jpg" height="200" />

### Modify size:
<img src="https://user-images.githubusercontent.com/6807005/64227510-64ddd300-cf16-11e9-8aff-c6e33bdd1ac6.jpg" height="200" />  
<img src="https://user-images.githubusercontent.com/6807005/64227512-64ddd300-cf16-11e9-8ceb-bc3f848cb7e9.jpg" height="200" />

### Modify border:
<img src="https://user-images.githubusercontent.com/6807005/64227515-64ddd300-cf16-11e9-9fc8-149aa3630284.jpg" height="200" />

## Useful Options:
### Divde output to chunks
If you are using consumer level printer, you will suffer from not able printing too large marker, so just set subSize before saving the marker to files, it will divide output marker to chunks.
<img src="https://user-images.githubusercontent.com/6807005/64241240-df6a1b00-cf35-11e9-9f13-7bda31046728.jpg" height="400" />

## Note:
### Why PNG is not recommend
PNG will suffer from artifact problem after scaling:
<img src="https://user-images.githubusercontent.com/6807005/64232240-2a7b3280-cf24-11e9-80e1-2390d97146f1.jpg" height="200" />

### Algorithm
This application use "wall follower maze solving algorithm" to draw the marker, and it is useful to avoid some problems.
<img src="https://user-images.githubusercontent.com/6807005/64232926-8a260d80-cf25-11e9-9b92-eec447395c9a.jpg" height="400" />

