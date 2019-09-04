# OpenCVMarkerPrinter

## Description
This small app can save some commonly used opencv markers such as ArucoMarker, Chessboard and ChArUco to vector graphics file. **Supported vector graphics file format: .svg, .pdf and .ps. Supported image file format: .png (not recommend).**

### Current pattern generator apps:
Not good enough, for example: calib.io can not modify all of the parameters.  
<img src="https://user-images.githubusercontent.com/6807005/64223512-e0d01f00-cf06-11e9-8a47-962b0501eed5.jpg" width="whatever" height="200" />

### Ours application:
Can modify all of the parameters.  
<img src="https://user-images.githubusercontent.com/6807005/64225418-eda44100-cf0d-11e9-95a1-424f18205a26.jpg" width="whatever" height="200" />

## Tutorial
### Seletct dictionary:
<img src="https://user-images.githubusercontent.com/6807005/64223922-38bb5580-cf08-11e9-9f71-d4a71a54cd3e.jpg" width="whatever" height="200" />

### Modify size:
<img src="https://user-images.githubusercontent.com/6807005/64224003-8d5ed080-cf08-11e9-8cc0-e49b3a5e6ffd.jpg" width="whatever" height="200" />  
<img src="https://user-images.githubusercontent.com/6807005/64224074-cd25b800-cf08-11e9-97d1-c1fced38be09.jpg" width="whatever" height="200" />

### Modify border:
<img src="https://user-images.githubusercontent.com/6807005/64224139-03633780-cf09-11e9-8a20-823f000da096.jpg" width="whatever" height="200" />

## Useful Options:
### Divde output to multi-chuncks
Since if you are using consumer level printer, you will suffer from not able printing too large marker, so just set subSize before saving the marker to files, it will divide output marker to multi-chuncks files.
<img src="https://user-images.githubusercontent.com/6807005/64224727-35759900-cf0b-11e9-9e76-33c50f1f8f00.jpg" width="whatever" height="400" />

## Note:
This application use "wall follower maze solving algorithm" to draw the marker, and it is useful to avoid some problems.
<img src="https://user-images.githubusercontent.com/6807005/64225708-20026e00-cf0f-11e9-9141-a2b014a6fbfc.jpg" width="whatever" height="400" />

