# OpenCVMarkerPrinter

## Description
This small app can save some commonly used opencv markers such as ArucoMarker, Chessboard and ChArUco to vector graphics file. **Supported vector graphics file format: .svg, .pdf and .ps. Supported image file format: .png (not recommend).**

### Current pattern generator apps:
Not good enough, for example: calib.io can not modify all of the parameters.  
<img src="https://user-images.githubusercontent.com/6807005/64223512-e0d01f00-cf06-11e9-8a47-962b0501eed5.jpg" height="200" />

### Ours application:
Can modify all of the parameters.  
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
Since if you are using consumer level printer, you will suffer from not able printing too large marker, so just set subSize before saving the marker to files, it will divide output marker to chunks.
<img src="https://user-images.githubusercontent.com/6807005/64227516-65766980-cf16-11e9-86c5-a5e6c91006f3.jpg" height="400" />

## Note:
### Why PNG is not recommend
PNG will suffer from artifact problem after scaling:
<img src="https://user-images.githubusercontent.com/6807005/64232240-2a7b3280-cf24-11e9-80e1-2390d97146f1.jpg" height="200" />

### Algorithm
This application use "wall follower maze solving algorithm" to draw the marker, and it is useful to avoid some problems.
<img src="https://user-images.githubusercontent.com/6807005/64227518-65766980-cf16-11e9-9378-33e3995e72c7.jpg" height="400" />

