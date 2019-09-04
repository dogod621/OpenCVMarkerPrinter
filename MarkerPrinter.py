import numpy as np
import cv2
import warnings
import os
from cv2 import aruco
import cairo
import math
from cairosvg import svg2png
import tempfile

class MarkerPrinter:

    debugMode = None # "LINE" "BLOCK"

    # Static Vars
    # SVG https://oreillymedia.github.io/Using_SVG/guide/units.html
    # for PDF and SVG, 1 pixel = 1/72 inch, 1 cm = 1/2.54 inch, 1pixl = 2.54/72 cm, 1cm = 72/2.54 pixels
    ptPerMeter = 72 / 2.54 * 100

    surface = {
            ".PNG": cairo.SVGSurface,
            ".SVG": cairo.SVGSurface,
            ".PDF": cairo.PDFSurface,
            ".PS": cairo.PSSurface }

    surfaceEXT = {
            ".PNG": ".svg",
            ".SVG": ".svg",
            ".PDF": ".pdf",
            ".PS": ".ps" }

    #
    def __DrawBlock(context, 
                  dictionary = None, markerLength = None, borderBits = 1, 
                  chessboardSize = (1, 1), squareLength = None, firstMarkerID = 0, 
                  blockX = 0, blockY = 0, originX = 0, originY = 0, 
                  mode = "CHESS" ):
        
        if(squareLength is None):
            squareLength = markerLength

        if(markerLength is None):
            markerLength = squareLength

        if((squareLength is None) or (markerLength is None)):
            warnings.warn("lenght is None") 
            return False 

        if((( blockX % 2 == 0 ) == ( blockY % 2 == 0 )) or mode == "ARUCOGRID"):
            if (mode != "CHESS"):
                if(dictionary is None):
                    warnings.warn("dictionary is None") 
                    return False 

                unitLength = markerLength / (float)(dictionary.markerSize + borderBits * 2)

                if  (mode == "CHARUCO"):
                    originX = (blockX - originX) * squareLength + (squareLength - markerLength)*0.5
                    originY = (blockY - originY) * squareLength + (squareLength - markerLength)*0.5
                else:
                    originX = (blockX - originX) * squareLength 
                    originY = (blockY - originY) * squareLength 
                
                #
                context.set_source_rgba(0.0, 0.0, 0.0, 1.0)
                context.rectangle(originX, originY, markerLength, markerLength)
                context.fill()

                #
                if  (mode == "CHARUCO"):
                    markerID = firstMarkerID + (blockY * chessboardSize[0] + blockX) // 2
                elif (mode == "ARUCO"):
                    markerID = firstMarkerID
                elif (mode == "ARUCOGRID"):
                    markerID = firstMarkerID + (blockY * chessboardSize[0] + blockX) 

                markerBitMap = np.swapaxes(dictionary.drawMarker(markerID, dictionary.markerSize + borderBits * 2, borderBits = borderBits), 0, 1)

                hEdges = np.zeros(shape = (dictionary.markerSize+1,dictionary.markerSize+1), dtype = np.uint8)
                vEdges = np.zeros(shape = (dictionary.markerSize+1,dictionary.markerSize+1), dtype = np.uint8)

                #
                for mx in range(dictionary.markerSize):
                    for my in range(dictionary.markerSize+1):
                        if( markerBitMap[mx + borderBits, my + borderBits - 1] != markerBitMap[mx + borderBits, my + borderBits]):
                            hEdges[mx, my] = 255

                for mx in range(dictionary.markerSize+1):
                    for my in range(dictionary.markerSize):
                        if( markerBitMap[mx + borderBits - 1, my + borderBits] != markerBitMap[mx + borderBits, my + borderBits]):
                            vEdges[mx, my] = 255

                # Use for debug, check edge or position is correct or not
                if(MarkerPrinter.debugMode is not None):
                    if(MarkerPrinter.debugMode.upper() == "LINE"):
                        context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                        context.set_line_width(unitLength * 0.1)
                        for mx in range(dictionary.markerSize+1):
                            for my in range(dictionary.markerSize+1):
                                if(hEdges[mx, my] > 0):
                                    context.move_to(originX + unitLength * (mx + borderBits    ), originY + unitLength * (my + borderBits    ))
                                    context.line_to(originX + unitLength * (mx + borderBits + 1), originY + unitLength * (my + borderBits    ))
                                    context.stroke()
                                if(vEdges[mx, my] > 0):
                                    context.move_to(originX + unitLength * (mx + borderBits    ), originY + unitLength * (my + borderBits    ))
                                    context.line_to(originX + unitLength * (mx + borderBits    ), originY + unitLength * (my + borderBits + 1))
                                    context.stroke()
            
                    elif(MarkerPrinter.debugMode.upper() == "BLOCK"):
                        context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                        for mx in range(dictionary.markerSize):
                            for my in range(dictionary.markerSize):
                                if( markerBitMap[mx + borderBits, my + borderBits] > 0):
                                    context.rectangle(
                                        originX + unitLength * (mx + borderBits), 
                                        originY + unitLength * (my + borderBits), 
                                        unitLength, unitLength)
                                    context.fill()

                else:
                    while(True):
                        found = False

                        # Find start position
                        sx = 0
                        sy = 0
                        for my in range(dictionary.markerSize):
                            for mx in range(dictionary.markerSize):
                                if(hEdges[mx, my] > 0):
                                    found = True
                                    sx = mx
                                    sy = my
                                    if(markerBitMap[sx + borderBits, sy + borderBits - 1] > 0):
                                        context.set_source_rgba(0.0, 0.0, 0.0, 1.0)
                                    else:
                                        context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                                    break
                            if(found):
                                break

                        context.move_to (originX + unitLength * (sx + borderBits), originY + unitLength * (sy + borderBits))

                        # Use wall follower maze solving algorithm to draw white part
                        cx = sx
                        cy = sy
                        cd = 3 # 0 right, 1 down, 2 left, 3 up
                        while(True):
                            nd = (cd + 1)%4  
                            moved = False
                            if(nd == 0):
                                if(hEdges[cx, cy] > 0):
                                    hEdges[cx, cy] = 0
                                    cx = cx + 1
                                    moved = True
                            elif(nd == 1):
                                if(vEdges[cx, cy] > 0):
                                    vEdges[cx, cy] = 0
                                    cy = cy + 1
                                    moved = True
                            elif(nd == 2):
                                if(hEdges[cx - 1, cy] > 0):
                                    hEdges[cx - 1, cy] = 0
                                    cx = cx - 1
                                    moved = True
                            elif(nd == 3):
                                if(vEdges[cx, cy - 1] > 0):
                                    vEdges[cx, cy - 1] = 0
                                    cy = cy - 1
                                    moved = True

                            if((cx == sx) and (cy == sy)):
                                context.close_path ()
                                break
                            else:
                                if(moved):
                                    context.line_to(originX + unitLength * (cx + borderBits), originY + unitLength * (cy + borderBits))
                                cd = nd

                        if (found):
                            context.fill()
                        else:
                            break

        else:
            originX = (blockX - originX) * squareLength
            originY = (blockY - originY) * squareLength

            #
            context.set_source_rgba(0.0, 0.0, 0.0, 1.0)
            context.rectangle(originX, originY, squareLength, squareLength)
            context.fill()

        return True 

    def PreviewChessMarkerImage(chessboardSize, squareLength, dpi=96):
        squareLength = squareLength * MarkerPrinter.ptPerMeter

        if(len(chessboardSize) != 2):
            warnings.warn("chessboardSize is not valid") 
            return None

            if not ((chessboardSize[0] > 0) and (chessboardSize[1] > 0)):
                warnings.warn("chessboardSize is not valid") 
                return None 
        
        prevImage = None
        with tempfile.TemporaryDirectory() as tmpdirname:
            with MarkerPrinter.surface[".SVG"] (os.path.join(tmpdirname, "tempSVG.svg"), chessboardSize[0] * squareLength, chessboardSize[1] * squareLength) as surface:
                context = cairo.Context(surface)

                context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                context.rectangle(0, 0, chessboardSize[0] * squareLength, chessboardSize[1] * squareLength)
                context.fill()

                for bx in range(chessboardSize[0]):
                    for by in range(chessboardSize[1]):
                        if not MarkerPrinter.__DrawBlock(context = context,
                                    chessboardSize = chessboardSize, squareLength = squareLength, 
                                    blockX = bx, blockY = by, mode = "CHESS" ):
                            warnings.warn("Failed draw marker") 
                            return None 

            with open(os.path.join(tmpdirname, "tempSVG.svg")) as file:
                prevImage = svg2png(bytestring=file.read(), dpi=dpi)

        if(prevImage is not None):
            prevImage = np.frombuffer(prevImage, dtype=np.uint8) 
            prevImage = cv2.imdecode(prevImage, cv2.IMREAD_GRAYSCALE)
        return prevImage

    def GenChessMarkerImage(filePath, chessboardSize, squareLength, subSize=None):
        squareLength = squareLength * MarkerPrinter.ptPerMeter

        # check
        path, nameExt = os.path.split(filePath)
        name, ext = os.path.splitext(nameExt)

        if not(os.path.isdir(path)):
            os.makedirs(path)

        if((ext.upper() != ".PNG") and (ext.upper() != ".SVG") and (ext.upper() != ".PS") and (ext.upper() != ".PDF")):
            warnings.warn("file extention is not support, must be: png, svg, ps, pdf") 
            return False 

        if(len(chessboardSize) != 2):
            warnings.warn("chessboardSize is not valid") 
            return False

            if not ((chessboardSize[0] > 0) and (chessboardSize[1] > 0)):
                warnings.warn("chessboardSize is not valid") 
                return False 
        
        if(subSize is not None):
            if(len(subSize) != 2):
                warnings.warn("subSize is not valid") 
                return False 
            if not ((subSize[0] > 0) and (subSize[1] > 0)):
                warnings.warn("subSize is not valid") 
                return False 

        #
        with tempfile.TemporaryDirectory() as tmpdirname:
            path2 = path
            if(ext.upper() == ".PNG"):
                path2 = tmpdirname

            with MarkerPrinter.surface[ext.upper()] (os.path.join(path2, name + MarkerPrinter.surfaceEXT[ext.upper()]), chessboardSize[0] * squareLength, chessboardSize[1] * squareLength) as surface:
                context = cairo.Context(surface)

                context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                context.rectangle(0, 0, chessboardSize[0] * squareLength, chessboardSize[1] * squareLength)
                context.fill()

                for bx in range(chessboardSize[0]):
                    for by in range(chessboardSize[1]):
                        if not MarkerPrinter.__DrawBlock(context = context,
                                    chessboardSize = chessboardSize, squareLength = squareLength, 
                                    blockX = bx, blockY = by, mode = "CHESS" ):
                            warnings.warn("Failed draw marker") 
                            return False 

                ''' Too slow
                if(ext.upper() == ".PNG"):
                    with surface.map_to_image(None) as imageSurface:
                        imageSurface.write_to_png (filePath)
                '''

            if(ext.upper() == ".PNG"):
                with open(os.path.join(path2, name + MarkerPrinter.surfaceEXT[ext.upper()])) as file:
                    svg2png(bytestring=file.read(),write_to=filePath)
                    

            if(subSize is not None):
                subDivide = (\
                    chessboardSize[0] // subSize[0] + int(chessboardSize[0] % subSize[0] > 0),
                    chessboardSize[1] // subSize[1] + int(chessboardSize[1] % subSize[1] > 0))

                subChessboardBlockX = np.clip ( np.arange(0, subSize[0] * subDivide[0] + 1, subSize[0]), 0, chessboardSize[0])
                subChessboardBlockY = np.clip ( np.arange(0, subSize[1] * subDivide[1] + 1, subSize[1]), 0, chessboardSize[1])
            
                subChessboardSliceX = subChessboardBlockX.astype(np.float) * squareLength
                subChessboardSliceY = subChessboardBlockY.astype(np.float) * squareLength

                for subXID in range(subDivide[0]):
                    for subYID in range(subDivide[1]):
                        subName = name + \
                            "_X" + str(subChessboardBlockX[subXID]) + "_" + str(subChessboardBlockX[subXID+1]) + \
                            "_Y" + str(subChessboardBlockY[subYID]) + "_" + str(subChessboardBlockY[subYID+1])

                        with MarkerPrinter.surface[ext.upper()](os.path.join(path2, subName + MarkerPrinter.surfaceEXT[ext.upper()]), subChessboardSliceX[subXID+1] - subChessboardSliceX[subXID], subChessboardSliceY[subYID+1] - subChessboardSliceY[subYID]) as surface:
                            context = cairo.Context(surface)
                        
                            context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                            context.rectangle(0, 0, subChessboardSliceX[subXID+1] - subChessboardSliceX[subXID], subChessboardSliceY[subYID+1] - subChessboardSliceY[subYID])
                            context.fill()

                            for bx in range(subChessboardBlockX[subXID+1] - subChessboardBlockX[subXID]):
                                for by in range(subChessboardBlockY[subYID+1] - subChessboardBlockY[subYID]):
                                    if not MarkerPrinter.__DrawBlock(context = context,
                                                chessboardSize = chessboardSize, squareLength = squareLength, 
                                                blockX = subChessboardBlockX[subXID] + bx, blockY = subChessboardBlockY[subYID] + by,
                                                originX = subChessboardBlockX[subXID], originY = subChessboardBlockY[subYID], mode = "CHESS" ):
                                        warnings.warn("Failed draw marker") 
                                        return False 

                            ''' Too slow
                            if(ext.upper() == ".PNG"):
                                with surface.map_to_image(None) as imageSurface:
                                    imageSurface.write_to_png (os.path.join(path, subName + ext))
                            '''

                        if(ext.upper() == ".PNG"):
                            with open(os.path.join(path2, subName + MarkerPrinter.surfaceEXT[ext.upper()])) as file:
                                svg2png(bytestring=file.read(),write_to=os.path.join(path, subName + ext))

        return True 

    def PreviewArucoMarkerImage(dictionary, markerID, markerLength, borderBits=1, dpi=96):
        markerLength = markerLength * MarkerPrinter.ptPerMeter

        prevImage = None
        with tempfile.TemporaryDirectory() as tmpdirname:
            with MarkerPrinter.surface[".SVG"] (os.path.join(tmpdirname, "tempSVG.svg"), markerLength, markerLength) as surface:
                context = cairo.Context(surface)

                if not MarkerPrinter.__DrawBlock(context = context, dictionary = dictionary, markerLength = markerLength, borderBits = borderBits, firstMarkerID = markerID, mode = "ARUCO"):
                    warnings.warn("Failed draw marker") 
                    return None 

            with open(os.path.join(tmpdirname, "tempSVG.svg")) as file:
                prevImage = svg2png(bytestring=file.read(), dpi=dpi)

        if(prevImage is not None):
            prevImage = np.frombuffer(prevImage, dtype=np.uint8) 
            prevImage = cv2.imdecode(prevImage, cv2.IMREAD_GRAYSCALE)
        return prevImage

    def GenArucoMarkerImage(filePath, dictionary, markerID, markerLength, borderBits=1):
        markerLength = markerLength * MarkerPrinter.ptPerMeter

        # check
        path, nameExt = os.path.split(filePath)
        name, ext = os.path.splitext(nameExt)

        if not(os.path.isdir(path)):
            os.makedirs(path)

        if((ext.upper() != ".PNG") and (ext.upper() != ".SVG") and (ext.upper() != ".PS") and (ext.upper() != ".PDF")):
            warnings.warn("file extention is not support, must be: png, svg, ps, pdf") 
            return False 

        #
        ''' Old way
        if(ext.upper() == ".PNG"):
            markerImage = dictionary.drawMarker(markerID, int(math.ceil(markerLength)), borderBits = borderBits)
            cv2.imwrite(filePath, markerImage)
        '''

        with tempfile.TemporaryDirectory() as tmpdirname:
            path2 = path
            if(ext.upper() == ".PNG"):
                path2 = tmpdirname

            with MarkerPrinter.surface[ext.upper()] (os.path.join(path2, name + MarkerPrinter.surfaceEXT[ext.upper()]), markerLength, markerLength) as surface:
                context = cairo.Context(surface)

                if not MarkerPrinter.__DrawBlock(context = context, dictionary = dictionary, markerLength = markerLength, borderBits = borderBits, firstMarkerID = markerID, mode = "ARUCO"):
                    warnings.warn("Failed draw marker") 
                    return False 

                ''' Too slow
                if(ext.upper() == ".PNG"):
                    with surface.map_to_image(None) as imageSurface:
                        imageSurface.write_to_png (filePath)
                '''

            if(ext.upper() == ".PNG"):
                with open(os.path.join(path2, name + MarkerPrinter.surfaceEXT[ext.upper()])) as file:
                    svg2png(bytestring=file.read(),write_to=filePath)

        return True 

    def PreviewCharucoMarkerImage(charucoBoard, borderBits=1, dpi=96):
        dictionary = charucoBoard.dictionary
        chessboardSize = charucoBoard.getChessboardSize()
        squareLength = charucoBoard.getSquareLength() * MarkerPrinter.ptPerMeter
        markerLength = charucoBoard.getMarkerLength() * MarkerPrinter.ptPerMeter
        unitLength = markerLength / (float)(dictionary.markerSize + borderBits * 2)

        prevImage = None
        with tempfile.TemporaryDirectory() as tmpdirname:
            with MarkerPrinter.surface[".SVG"] (os.path.join(tmpdirname, "tempSVG.svg"), chessboardSize[0] * squareLength, chessboardSize[1] * squareLength) as surface:
                context = cairo.Context(surface)

                context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                context.rectangle(0, 0, chessboardSize[0] * squareLength, chessboardSize[1] * squareLength)
                context.fill()

                for bx in range(chessboardSize[0]):
                    for by in range(chessboardSize[1]):
                        if not MarkerPrinter.__DrawBlock(context = context,
                                    dictionary = dictionary, markerLength = markerLength, borderBits = borderBits,
                                    chessboardSize = chessboardSize, squareLength = squareLength, 
                                    blockX = bx, blockY = by, mode = "CHARUCO"):
                            warnings.warn("Failed draw marker") 
                            return False 

            with open(os.path.join(tmpdirname, "tempSVG.svg")) as file:
                prevImage = svg2png(bytestring=file.read(), dpi=dpi)

        if(prevImage is not None):
            prevImage = np.frombuffer(prevImage, dtype=np.uint8) 
            prevImage = cv2.imdecode(prevImage, cv2.IMREAD_GRAYSCALE)
        return prevImage

    def GenCharucoMarkerImage(filePath, charucoBoard, borderBits=1, subSize=None):
        # check
        path, nameExt = os.path.split(filePath)
        name, ext = os.path.splitext(nameExt)

        if not(os.path.isdir(path)):
            os.makedirs(path)

        if((ext.upper() != ".PNG") and (ext.upper() != ".SVG") and (ext.upper() != ".PS") and (ext.upper() != ".PDF")):
            warnings.warn("file extention is not support, must be: png, svg, ps, pdf") 
            return False 

        if(subSize is not None):
            if(len(subSize) != 2):
                warnings.warn("subSize is not valid") 
                return False 
            if not ((subSize[0] > 0) and (subSize[1] > 0)):
                warnings.warn("subSize is not valid") 
                return False 

        #
        dictionary = charucoBoard.dictionary
        chessboardSize = charucoBoard.getChessboardSize()
        squareLength = charucoBoard.getSquareLength() * MarkerPrinter.ptPerMeter
        markerLength = charucoBoard.getMarkerLength() * MarkerPrinter.ptPerMeter
        unitLength = markerLength / (float)(dictionary.markerSize + borderBits * 2)

        # 
        ''' Old way
        if(ext.upper() == ".PNG"):
            charucoBoardImage = charucoBoard.draw((chessboardSize[0] * int(math.ceil(squareLength)), chessboardSize[1] * int(math.ceil(squareLength))), borderBits = borderBits)
            cv2.imwrite(filePath, charucoBoardImage)

            if(subSize is not None):
                subDivide = (\
                    chessboardSize[0] // subSize[0] + int(chessboardSize[0] % subSize[0] > 0),
                    chessboardSize[1] // subSize[1] + int(chessboardSize[1] % subSize[1] > 0))

                subChessboardBlockX = np.clip ( np.arange(0, subSize[0] * subDivide[0] + 1, subSize[0]), 0, chessboardSize[0])
                subChessboardBlockY = np.clip ( np.arange(0, subSize[1] * subDivide[1] + 1, subSize[1]), 0, chessboardSize[1])
            
                subChessboardSliceX = subChessboardBlockX * int(math.ceil(squareLength))
                subChessboardSliceY = subChessboardBlockY * int(math.ceil(squareLength))

                for subXID in range(subDivide[0]):
                    for subYID in range(subDivide[1]):
                        subName = name + \
                            "_X" + str(subChessboardBlockX[subXID]) + "_" + str(subChessboardBlockX[subXID+1]) + \
                            "_Y" + str(subChessboardBlockY[subYID]) + "_" + str(subChessboardBlockY[subYID+1])

                        subCharucoBoardImage = charucoBoardImage[\
                            subChessboardSliceY[subYID] : subChessboardSliceY[subYID+1],\
                            subChessboardSliceX[subXID] : subChessboardSliceX[subXID+1]]

                        cv2.imwrite(os.path.join(path, subName + ext), subCharucoBoardImage)
        '''

        with tempfile.TemporaryDirectory() as tmpdirname:
            path2 = path
            if(ext.upper() == ".PNG"):
                path2 = tmpdirname

            with MarkerPrinter.surface[ext.upper()] (os.path.join(path2, name + MarkerPrinter.surfaceEXT[ext.upper()]), chessboardSize[0] * squareLength, chessboardSize[1] * squareLength) as surface:
                context = cairo.Context(surface)

                context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                context.rectangle(0, 0, chessboardSize[0] * squareLength, chessboardSize[1] * squareLength)
                context.fill()

                for bx in range(chessboardSize[0]):
                    for by in range(chessboardSize[1]):
                        if not MarkerPrinter.__DrawBlock(context = context,
                                    dictionary = dictionary, markerLength = markerLength, borderBits = borderBits,
                                    chessboardSize = chessboardSize, squareLength = squareLength,
                                    blockX = bx, blockY = by, mode = "CHARUCO"):
                            warnings.warn("Failed draw marker") 
                            return False 

                ''' Too slow
                if(ext.upper() == ".PNG"):
                    with surface.map_to_image(None) as imageSurface:
                        imageSurface.write_to_png (filePath)
                '''

            if(ext.upper() == ".PNG"):
                with open(os.path.join(path2, name + MarkerPrinter.surfaceEXT[ext.upper()])) as file:
                    svg2png(bytestring=file.read(),write_to=filePath)

            if(subSize is not None):
                subDivide = (\
                    chessboardSize[0] // subSize[0] + int(chessboardSize[0] % subSize[0] > 0),
                    chessboardSize[1] // subSize[1] + int(chessboardSize[1] % subSize[1] > 0))

                subChessboardBlockX = np.clip ( np.arange(0, subSize[0] * subDivide[0] + 1, subSize[0]), 0, chessboardSize[0])
                subChessboardBlockY = np.clip ( np.arange(0, subSize[1] * subDivide[1] + 1, subSize[1]), 0, chessboardSize[1])
            
                subChessboardSliceX = subChessboardBlockX.astype(np.float) * squareLength
                subChessboardSliceY = subChessboardBlockY.astype(np.float) * squareLength

                for subXID in range(subDivide[0]):
                    for subYID in range(subDivide[1]):
                        subName = name + \
                            "_X" + str(subChessboardBlockX[subXID]) + "_" + str(subChessboardBlockX[subXID+1]) + \
                            "_Y" + str(subChessboardBlockY[subYID]) + "_" + str(subChessboardBlockY[subYID+1])

                        with MarkerPrinter.surface[ext.upper()](os.path.join(path2, subName + MarkerPrinter.surfaceEXT[ext.upper()]), subChessboardSliceX[subXID+1] - subChessboardSliceX[subXID], subChessboardSliceY[subYID+1] - subChessboardSliceY[subYID]) as surface:
                            context = cairo.Context(surface)
                        
                            context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                            context.rectangle(0, 0, subChessboardSliceX[subXID+1] - subChessboardSliceX[subXID], subChessboardSliceY[subYID+1] - subChessboardSliceY[subYID])
                            context.fill()

                            for bx in range(subChessboardBlockX[subXID+1] - subChessboardBlockX[subXID]):
                                for by in range(subChessboardBlockY[subYID+1] - subChessboardBlockY[subYID]):
                                    if not MarkerPrinter.__DrawBlock(context = context,
                                                dictionary = dictionary, markerLength = markerLength, borderBits = borderBits,
                                                chessboardSize = chessboardSize, squareLength = squareLength,
                                                blockX = subChessboardBlockX[subXID] + bx, blockY = subChessboardBlockY[subYID] + by,
                                                originX = subChessboardBlockX[subXID], originY = subChessboardBlockY[subYID], mode = "CHARUCO"):
                                        warnings.warn("Failed draw marker") 
                                        return False 

                            ''' Too slow
                            if(ext.upper() == ".PNG"):
                                with surface.map_to_image(None) as imageSurface:
                                    imageSurface.write_to_png (os.path.join(path, subName + ext))
                            '''

                        if(ext.upper() == ".PNG"):
                            with open(os.path.join(path2, subName + MarkerPrinter.surfaceEXT[ext.upper()])) as file:
                                svg2png(bytestring=file.read(),write_to=os.path.join(path, subName + ext))
              

        return True

    def PreviewArucoGridMarkerImage(arucoGridBoard, borderBits=1, dpi=96):
        dictionary = arucoGridBoard.dictionary
        chessboardSize = arucoGridBoard.getGridSize()
        markerLength = arucoGridBoard.getMarkerLength() * MarkerPrinter.ptPerMeter
        markerSeparation = arucoGridBoard.getMarkerSeparation() * MarkerPrinter.ptPerMeter
        firstMarker = arucoGridBoard.ids.ravel()[0]
        squareLength = markerLength + markerSeparation
        unitLength = markerLength / (float)(dictionary.markerSize + borderBits * 2)

        prevImage = None
        with tempfile.TemporaryDirectory() as tmpdirname:
            with MarkerPrinter.surface[".SVG"] (os.path.join(tmpdirname, "tempSVG.svg"), chessboardSize[0] * markerLength + (chessboardSize[0] - 1) * markerSeparation, chessboardSize[1] * markerLength + (chessboardSize[1] - 1) * markerSeparation) as surface:
                context = cairo.Context(surface)

                context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                context.rectangle(0, 0, chessboardSize[0] * markerLength + (chessboardSize[0] - 1) * markerSeparation, chessboardSize[1] * markerLength + (chessboardSize[1] - 1) * markerSeparation)
                context.fill()

                for bx in range(chessboardSize[0]):
                    for by in range(chessboardSize[1]):
                        if not MarkerPrinter.__DrawBlock(context = context,
                                    dictionary = dictionary, markerLength = markerLength, borderBits = borderBits,
                                    chessboardSize = chessboardSize, squareLength = squareLength, firstMarkerID = firstMarker,
                                    blockX = bx, blockY = by, mode = "ARUCOGRID"):
                            warnings.warn("Failed draw marker") 
                            return False 

            with open(os.path.join(tmpdirname, "tempSVG.svg")) as file:
                prevImage = svg2png(bytestring=file.read(), dpi=dpi)

        if(prevImage is not None):
            prevImage = np.frombuffer(prevImage, dtype=np.uint8) 
            prevImage = cv2.imdecode(prevImage, cv2.IMREAD_GRAYSCALE)
        return prevImage
   
    def GenArucoGridMarkerImage(filePath, arucoGridBoard, borderBits=1, subSize=None):
        # check
        path, nameExt = os.path.split(filePath)
        name, ext = os.path.splitext(nameExt)

        if not(os.path.isdir(path)):
            os.makedirs(path)

        if((ext.upper() != ".PNG") and (ext.upper() != ".SVG") and (ext.upper() != ".PS") and (ext.upper() != ".PDF")):
            warnings.warn("file extention is not support, must be: png, svg, ps, pdf") 
            return False 

        if(subSize is not None):
            if(len(subSize) != 2):
                warnings.warn("subSize is not valid") 
                return False 
            if not ((subSize[0] > 0) and (subSize[1] > 0)):
                warnings.warn("subSize is not valid") 
                return False 

        #
        dictionary = arucoGridBoard.dictionary
        chessboardSize = arucoGridBoard.getGridSize()
        markerLength = arucoGridBoard.getMarkerLength() * MarkerPrinter.ptPerMeter
        markerSeparation = arucoGridBoard.getMarkerSeparation() * MarkerPrinter.ptPerMeter
        firstMarker = arucoGridBoard.ids.ravel()[0]
        squareLength = markerLength + markerSeparation
        unitLength = markerLength / (float)(dictionary.markerSize + borderBits * 2)

        #
        with tempfile.TemporaryDirectory() as tmpdirname:
            path2 = path
            if(ext.upper() == ".PNG"):
                path2 = tmpdirname


            with MarkerPrinter.surface[ext.upper()] (os.path.join(path2, name + MarkerPrinter.surfaceEXT[ext.upper()]), chessboardSize[0] * markerLength + (chessboardSize[0] - 1) * markerSeparation, chessboardSize[1] * markerLength + (chessboardSize[1] - 1) * markerSeparation) as surface:
                context = cairo.Context(surface)

                context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                context.rectangle(0, 0, chessboardSize[0] * markerLength + (chessboardSize[0] - 1) * markerSeparation, chessboardSize[1] * markerLength + (chessboardSize[1] - 1) * markerSeparation)
                context.fill()

                context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                context.rectangle(0, 0, chessboardSize[0] * markerLength + (chessboardSize[0] - 1) * markerSeparation, chessboardSize[1] * markerLength + (chessboardSize[1] - 1) * markerSeparation)
                context.fill()

                for bx in range(chessboardSize[0]):
                    for by in range(chessboardSize[1]):
                        if not MarkerPrinter.__DrawBlock(context = context,
                                    dictionary = dictionary, markerLength = markerLength, borderBits = borderBits,
                                    chessboardSize = chessboardSize, squareLength = squareLength, firstMarkerID = firstMarker,
                                    blockX = bx, blockY = by, mode = "ARUCOGRID"):
                            warnings.warn("Failed draw marker") 
                            return False 

            if(ext.upper() == ".PNG"):
                with open(os.path.join(path2, name + MarkerPrinter.surfaceEXT[ext.upper()])) as file:
                    svg2png(bytestring=file.read(),write_to=filePath)

            if(subSize is not None):
                subDivide = (\
                    chessboardSize[0] // subSize[0] + int(chessboardSize[0] % subSize[0] > 0),
                    chessboardSize[1] // subSize[1] + int(chessboardSize[1] % subSize[1] > 0))

                subChessboardBlockX = np.clip ( np.arange(0, subSize[0] * subDivide[0] + 1, subSize[0]), 0, chessboardSize[0])
                subChessboardBlockY = np.clip ( np.arange(0, subSize[1] * subDivide[1] + 1, subSize[1]), 0, chessboardSize[1])
            
                subChessboardSliceX = subChessboardBlockX.astype(np.float) * squareLength
                subChessboardSliceY = subChessboardBlockY.astype(np.float) * squareLength

                subChessboardSliceX[-1] -= markerSeparation
                subChessboardSliceY[-1] -= markerSeparation

                for subXID in range(subDivide[0]):
                    for subYID in range(subDivide[1]):
                        subName = name + \
                            "_X" + str(subChessboardBlockX[subXID]) + "_" + str(subChessboardBlockX[subXID+1]) + \
                            "_Y" + str(subChessboardBlockY[subYID]) + "_" + str(subChessboardBlockY[subYID+1])

                        with MarkerPrinter.surface[ext.upper()](os.path.join(path2, subName + MarkerPrinter.surfaceEXT[ext.upper()]), subChessboardSliceX[subXID+1] - subChessboardSliceX[subXID], subChessboardSliceY[subYID+1] - subChessboardSliceY[subYID]) as surface:
                            context = cairo.Context(surface)
                        
                            context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                            context.rectangle(0, 0, subChessboardSliceX[subXID+1] - subChessboardSliceX[subXID], subChessboardSliceY[subYID+1] - subChessboardSliceY[subYID])
                            context.fill()

                            for bx in range(subChessboardBlockX[subXID+1] - subChessboardBlockX[subXID]):
                                for by in range(subChessboardBlockY[subYID+1] - subChessboardBlockY[subYID]):
                                    if not MarkerPrinter.__DrawBlock(context = context,
                                                dictionary = dictionary, markerLength = markerLength, borderBits = borderBits,
                                                chessboardSize = chessboardSize, squareLength = squareLength, firstMarkerID = firstMarker,
                                                blockX = subChessboardBlockX[subXID] + bx, blockY = subChessboardBlockY[subYID] + by,
                                                originX = subChessboardBlockX[subXID], originY = subChessboardBlockY[subYID], mode = "ARUCOGRID"):
                                        warnings.warn("Failed draw marker") 
                                        return False 

                        if(ext.upper() == ".PNG"):
                            with open(os.path.join(path2, subName + MarkerPrinter.surfaceEXT[ext.upper()])) as file:
                                svg2png(bytestring=file.read(),write_to=os.path.join(path, subName + ext))
              

        return True

if __name__ == '__main__':   

    '''
    charucoBoard = aruco.CharucoBoard_create(25, 10, 0.09, 0.07, aruco.Dictionary_get(aruco.DICT_5X5_1000))
    MarkerPrinter.GenCharucoMarkerImage("./Marker_25_10_0x09_0x07_1/marker.png", charucoBoard, subSize = (5, 5))
    MarkerPrinter.GenCharucoMarkerImage("./Marker_25_10_0x09_0x07_1/marker.svg", charucoBoard, subSize = (5, 5))
    MarkerPrinter.GenCharucoMarkerImage("./Marker_25_10_0x09_0x07_1/marker.pdf", charucoBoard, subSize = (5, 5))
    MarkerPrinter.GenCharucoMarkerImage("./Marker_25_10_0x09_0x07_1/marker.ps", charucoBoard, subSize = (5, 5))

    MarkerPrinter.GenArucoMarkerImage("./Marker_25_10_0x09_0x07_1/arucoMarker0.png", aruco.Dictionary_get(aruco.DICT_5X5_1000), 0, 0.07)
    MarkerPrinter.GenArucoMarkerImage("./Marker_25_10_0x09_0x07_1/arucoMarker1.png", aruco.Dictionary_get(aruco.DICT_5X5_1000), 1, 0.07)
    MarkerPrinter.GenArucoMarkerImage("./Marker_25_10_0x09_0x07_1/arucoMarker2.png", aruco.Dictionary_get(aruco.DICT_5X5_1000), 2, 0.07)

    MarkerPrinter.GenArucoMarkerImage("./Marker_25_10_0x09_0x07_1/arucoMarker0.svg", aruco.Dictionary_get(aruco.DICT_5X5_1000), 0, 0.07)
    MarkerPrinter.GenArucoMarkerImage("./Marker_25_10_0x09_0x07_1/arucoMarker1.svg", aruco.Dictionary_get(aruco.DICT_5X5_1000), 1, 0.07)
    MarkerPrinter.GenArucoMarkerImage("./Marker_25_10_0x09_0x07_1/arucoMarker2.svg", aruco.Dictionary_get(aruco.DICT_5X5_1000), 2, 0.07)

    MarkerPrinter.GenArucoMarkerImage("./Marker_25_10_0x09_0x07_1/arucoMarker0.pdf", aruco.Dictionary_get(aruco.DICT_5X5_1000), 0, 0.07)
    MarkerPrinter.GenArucoMarkerImage("./Marker_25_10_0x09_0x07_1/arucoMarker1.pdf", aruco.Dictionary_get(aruco.DICT_5X5_1000), 1, 0.07)
    MarkerPrinter.GenArucoMarkerImage("./Marker_25_10_0x09_0x07_1/arucoMarker2.pdf", aruco.Dictionary_get(aruco.DICT_5X5_1000), 2, 0.07)

    MarkerPrinter.GenChessMarkerImage("./Marker_25_10_0x09_0x07_1/chessMarker.png", (25, 10), 0.09, subSize = (5, 5))
    MarkerPrinter.GenChessMarkerImage("./Marker_25_10_0x09_0x07_1/chessMarker.svg", (25, 10), 0.09, subSize = (36, 36))
    MarkerPrinter.GenChessMarkerImage("./Marker_25_10_0x09_0x07_1/chessMarker.pdf", (25, 10), 0.09, subSize = (36, 5))
    '''

