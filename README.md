# OpenCVMarkerPrinter

## Description
This small app can save some commonly used opencv markers such as ArucoMarker, Chessboard and ChArUco to vector graphics file.
Support vector graphics file format: .svg, .pdf, .ps
Support image file format: .png (not recommend)

Current pattern generator apps is not good enough, for example: calib.io can not modify all of the parameters.
<img src="https://user-images.githubusercontent.com/6807005/64223512-e0d01f00-cf06-11e9-8a47-962b0501eed5.jpg" width="whatever" height="200" />

Ours application can modify all of the parameters.
<img src="https://user-images.githubusercontent.com/6807005/64223560-0c530980-cf07-11e9-9d3c-878fad3c9424.jpg" width="whatever" height="200" />
<img src="https://user-images.githubusercontent.com/6807005/64223863-0e699800-cf08-11e9-84ae-37c1b0bee140.jpg" width="whatever" height="200" />
<img src="https://user-images.githubusercontent.com/6807005/64223869-11fd1f00-cf08-11e9-8cf3-5be5fa3e5391.jpg" width="whatever" height="200" />

## Tutorial
###Seletct dictionary:
![0005](https://user-images.githubusercontent.com/6807005/64223922-38bb5580-cf08-11e9-9f71-d4a71a54cd3e.jpg | width=500)

###Modify size:
![0006](https://user-images.githubusercontent.com/6807005/64224003-8d5ed080-cf08-11e9-8cc0-e49b3a5e6ffd.jpg | width=300)
![007](https://user-images.githubusercontent.com/6807005/64224074-cd25b800-cf08-11e9-97d1-c1fced38be09.jpg | width=300)

###Modify border:
![0008](https://user-images.githubusercontent.com/6807005/64224139-03633780-cf09-11e9-8a20-823f000da096.jpg | width=300)

## Useful Options:
Divde output to multi-chuncks
Since if you are using consumer level printer, you cannot print too large marker, so just set subSize before save the marker, it will divide output marker to multi-chuncks.
![0009](https://user-images.githubusercontent.com/6807005/64224727-35759900-cf0b-11e9-9e76-33c50f1f8f00.jpg | width=300)

## Note:
This application use "wall follower maze solving algorithm" to draw the marker, and it is useful to avoid some problems.
![0010](https://user-images.githubusercontent.com/6807005/64225328-84243280-cf0d-11e9-9ee6-2aabc21196d4.jpg)
