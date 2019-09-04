# OpenCVMarkerPrinter

This small app can save some commonly used opencv markers such as ArucoMarker, Chessboard and ChArUco to vector graphics file.
Support vector graphics file format: .svg, .pdf, .ps
Support image file format: .png (not recommend)

Current pattern generator apps is not good enough, for example: calib.io can not modify all of the parameters.
![0001](https://user-images.githubusercontent.com/6807005/64223512-e0d01f00-cf06-11e9-8a47-962b0501eed5.jpg)

Ours application can modify all of the parameters.
![0002](https://user-images.githubusercontent.com/6807005/64223560-0c530980-cf07-11e9-9d3c-878fad3c9424.jpg)
![0003](https://user-images.githubusercontent.com/6807005/64223863-0e699800-cf08-11e9-84ae-37c1b0bee140.jpg)
![0004](https://user-images.githubusercontent.com/6807005/64223869-11fd1f00-cf08-11e9-8cf3-5be5fa3e5391.jpg)

For example:
Seletct dictionary:
![0005](https://user-images.githubusercontent.com/6807005/64223922-38bb5580-cf08-11e9-9f71-d4a71a54cd3e.jpg)

Modify size:
![0006](https://user-images.githubusercontent.com/6807005/64224003-8d5ed080-cf08-11e9-8cc0-e49b3a5e6ffd.jpg)
![007](https://user-images.githubusercontent.com/6807005/64224074-cd25b800-cf08-11e9-97d1-c1fced38be09.jpg)

Modify border:
![0008](https://user-images.githubusercontent.com/6807005/64224139-03633780-cf09-11e9-8a20-823f000da096.jpg)

Useful Options:
Divde output to multi-chuncks
Since if you are using consumer level printer, you cannot print too large marker, so just set subSize before save the marker, it will divide output marker to multi-chuncks.
![0009](https://user-images.githubusercontent.com/6807005/64224727-35759900-cf0b-11e9-9e76-33c50f1f8f00.jpg)

Note:
This application use "wall follower maze solving algorithm" to draw the marker, and it is useful to avoid some problems.
![0010](https://user-images.githubusercontent.com/6807005/64225007-2e02bf80-cf0c-11e9-8503-8b024cdaaecf.jpg)
