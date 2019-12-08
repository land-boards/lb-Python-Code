# Pt1-AoCDay8.py
# 2019 Advent of Code
# Day 8
# Part 1

"""
--- Day 8: Space Image Format ---
The Elves' spirits are lifted when they realize you have an opportunity to reboot one of their Mars rovers, and so they are curious if you would spend a brief sojourn on Mars. You land your ship near the rover.

When you reach the rover, you discover that it's already in the process of rebooting! It's just waiting for someone to enter a BIOS password. The Elf responsible for the rover takes a picture of the password (your puzzle input) and sends it to you via the Digital Sending Network.

Unfortunately, images sent via the Digital Sending Network aren't encoded with any normal encoding; instead, they're encoded in a special Space Image Format. None of the Elves seem to remember why this is the case. They send you the instructions to decode it.

Images are sent as a series of digits that each represent the color of a single pixel. The digits fill each row of the image left-to-right, then move downward to the next row, filling rows top-to-bottom until every pixel of the image is filled.

Each image actually consists of a series of identically-sized layers that are filled in this way. So, the first digit corresponds to the top-left pixel of the first layer, the second digit corresponds to the pixel to the right of that on the same layer, and so on until the last digit, which corresponds to the bottom-right pixel of the last layer.

For example, given an image 3 pixels wide and 2 pixels tall, the image data 123456789012 corresponds to the following image layers:

Layer 1: 123
         456

Layer 2: 789
         012
The image you received is 25 pixels wide and 6 pixels tall.

To make sure the image wasn't corrupted during transmission, the Elves would like you to find the layer that contains the fewest 0 digits. On that layer, what is the number of 1 digits multiplied by the number of 2 digits?
"""
from __future__ import print_function

inStr = '222222022222220222222021020222222022222222022222202222222222222222022222222222222200222002222222222202102202221002222222220222222012122222222222222220222222022222220222222021122222222122222222222222222222222222222222222222222222222200222222222222222202012222220222222222220222222012222222222222222220222222122222222222222121022222222022222222122222212222222222222222022222222222222211222102222222222202112202220202222222220222222012022222222222222222222222122222222222222220220222222022222222022220212222222222222222022222222222202220222222222222222212202222220002222222221222222102122222222222222221222222122222220222222122121222222022222222122220222222222222222222122222222222212201222222222222221212102222220022222222220222222202222222222222222222222222222222221222022120221222222222222022022222222222222222222222222222222222212212222202222222222202222212222212222222220222222202222222222222222221222222122222220222122220122222222022222222122222202222222222222222222222222222212212222112222222222202202202220102222222220222222112022222222222222220222222022222221222122020222222222122222022222220222222222222222222022222222222212201222022222222222202102212221212222222222222222101022222222222222220222222022222221222022122120222222022222022022222222222222222222222122222222222222202222202222222220212012122222222222222222222222201122222222222222220222022222222221222022120120222222222222122122222212222222222222222022222222222212200222202222222222222222202220012222222222222222021022222202222222222222222122222220222022221122222222122222122122222202222222222222222222222222222212210222022222222222212122102220212222222220222222111022222222222222220222022222222220222022022022222222222222122022220212222222222222222222222222222222220222102222222222212122112220122222222220222222212022222222222222222222222222222221222022222122222222222222122122221202222222222222222022222222222212201222012222222220202002102220212222222222222222101222222212222222220222122022222220222222220020222222222222022122220212222222222222222022222222222202220222002222222220202212112222212222222222222222001222222202222222220222022122222222222122022122222222122222122022222222222222222222222122222222222222210222202221222220212102012220102222222222222222101122222212222222222222122222222221222022221020222222222222222022222222222222222222222122222222222202200222112222222221222222212220112222222220222222021222222212222222222222222222222222222122220221022222122222222222221202222222222222222022222222222202212222002221222221202022122222222222222220222222222222222212222222221222222022222221222022121020222222122222022122222212222222222222222222222222222202201220102221222222212222102222012222222222222222220022222212222222221222022222222221222122120121222222222222222122222212222222222222222022222222222202211221022220222220222212222222222222222220222220221222222212222222220222022122222221222222022021021222122222222022221202222222222222222222222222222212212220222221222221212112002222122222222222222222000222222202222222221222022022222220222222221222122222122222122222221222222222222222222122222222222202210220122222222220202012002220122222222221222221211212222222222222221222222222222220222222122120122222022222122022222212222222222222222022222222222212221222102220222221212202012221002022222221222220002012222212222222222222022222222221222022120221121222022222022122221202222222222222222022222222222202010020102220222220222202012202112022222220222221111102222212222222221222222022222221222122120222120222122222122222222202222222222222222122222222222202101120112222222220212112122222122022222220222221022102222212222222220222022122222222222222122222220222222222222122220202222222222222222222222222222222101022022221222220212212212210202022222220222220120102222202222222222222122222222220222222220021122222022222022222222202222222222222222122222222222212210020202220222220222102222221022022222202222222111012222212222222221222122022222221222022220022221222122222122022221222222222222222222222222222222202001222022221222222202122222210112122222201222221000112222212222222220222222122222221222122122221221222022222022222222202222222222222222022222222222222002020002220222222202122202202012022222202222222210112222222222222220122122122222220222022120120122222122222122122220222222222222222202022222222222202102121112221222222212212222210102022222220222221222002222222222222221022122122222220222022021120220222122222122022221222222222222222222022222222222212110121022222222222212222212211122022222202222222211002222212222222220222122022222220222022020021221222022222022022221222222222222222202222222222222222102120012221222221222002102221112222222200222222100102222212222222222122122222222220222222222022020222122222222222222212222222222222202022222222222212021012122220222221222002012220222212222220222220110222222212222222221122122022222222222022220121120122022202222122221222222222222222202022222222222202210020222220222222222222122222222022222201222222112112222212222222220122122022222222222222221020021122222222022122222202222222222222222122222222222202211111212221202222222202002222112102222222222222121022222212222222221222212122222220222122022020022122122222222222222212222222222222222122222222222222002102202222202222212012012222022222222210222221012012222202222222221122002022222221222122121220220222022202022022222212222222222222222122220222222202011000212220222221202112202202212212222200222222111002222202222222220022012222222220222122122222121022022202122222222202222222222222222122221222202202201220212220222221222202202212202022222221222221102022222212222222221022202222222221222122122220222222122212122122221212222222222222222122220222222212100220202222212220202002222200012202222211222221212212222202222222222222222122222222222122221221122122222212222022222222222222222222212122222222222222122101112222212220222002022201002212222201222222220222222212222222222122012222212222222222022221122222122222122022220222222222222222222222220222202222020012112220212222212012112212112112222202222220200202222012222222222222012222202220222022022021022222222212222222220212222222222222222022221222202222021000012221222220222112022220002002222200222221111112222102222222220122022022222220222022220021021122222202122122220212222222222222222222220222212222010102002220202221212122122200112212222112222220102022222122222222220122012022222221222122221221121122222222222122221222222222222222222022220222212222122002022222222220202202002211212002222211222222200222222002222222222122102122202211221122122121021222122222122122220202222222222222222122222222202222211202212221212221212102122201202212202101122222012012222112222222220122122022222220220122021021221022022212122222220212222222222222211022222222222022112211102121202221222112102212202222202111222220211022222102222222220122212022212212222122222222120122022222022022221202222222222222222222221222202102220202212112202221222122012200222212202201022222020012222112222222220022112122212210220222221120220122022222022022201212222222022222210122222222202122021020012222212220202112002211002202222202122020211222222112222222222220122022222212221222220022021022022202122222220210222222122222200122222222212002002000102020212222222222102211112102202022222220202112222002220222222022022220202202220222121221021222122212222222211200222222222222212022222222212222212002112001222022222002122210102012202121022122111112222102220222221222102022212201220122220022221022022202022022200200222222122222201022221222012102202101112021212020212222002222112102222112222122122012222002222222222221112222202211222022120220121222022202122122211202222222022222220222221222102012211200222202222120222202222200202112212011202021101122222022220222221220202222222200221022121120121222222212122222220210222222022222212122221222212202002010122012222220212202212222112002202001212220000212222102220222220122212122212211221022221121022102222212022222222220222222022222221122220222212122210202222012222221202100102221202212202001202221211002222212220202222222002021212221222022120221122112222202222022020212222222022222220022221222212202021122202110202020222220122201122022212021122222220222222022220222221122022020202201221222020120021002022202122220100211222222122222201122220222022012011220222112212120202211122210022002212210202120122112222112221202222021022021222222220222221221120202122202222020112220222222222222202022222222022102121002122101222222212110112201102002212021222120200022222202222222221222022222222212221022221022222022222222022122102211221220222222202222220222212022101012012202220021212021022220012112202002102121000022222112221222220020022222202211221222020021221212222222222220222222222220022222210122222222012212122000002202212221222111022221022012202022122020121222222222200202221022202020212212222222221221121212121212022121112222220222122222222222220222122022211122102100201120202001202210202112202121222121022222222222210212121121102122202222220222120020221012221222122121220102221220222222220022220222012012112211212021221022212110122221212102222121002021201102222222210202022121122120222202220122121020221202020222022021202000222220222222220222222222212002221102122020200121212222012212112002222000122121020212222222222222221220122221202201220222121020020222022212022020102100222221122222222122222222222102000001222112220220212121102211202102212002102222110202222002222202122022222021212202221022222021122202220202022121121200220222022222202022220222022122022001022211200221212020102200102102202111110220100212222112200212021122212222222200222122122022120202220212020221202010220221120222201222222222202112021120002101201121202010112221202102212220112222022022222212202222222020102220202220222122222220120112021212020222001222221021221222221222222222002112111101122202222021202111012202022212212101020120211202222012220202221220222121202210222022122221222202221202021022122120221221222222202122220222002222112212112222221122222111122222212212222102022020120122222112201202121122222022212211220222221121120212220212122121011120220221222222212122221222002022220220112222202020212102112200212202202020001122122222222222212202022020112122212200222022121122220012222212121022202110221220020222222222222222122002222222202000201222202210112211122122222002001221210122222002200212020021022122212211220222220221220202100222021121111022222120220222220222221222202112212200102011221020202020212220122022222222112022221102222102212212021022221122202212220122121020220012020202220220100002222222222222211122222222212012010211222122220222202102212220102202212201111222000122222222221222020022112222202221222122121020022222010222220020021001222012122222212022221222102112001011112212211220222211122011112212222000102122110012222212212212221022211020202220221022221121221210120202122022021020222212120222221222221222112022220121202221210021222221102200212112212121102220222202222002202202021120111021202202222222221220021222010202120220102221221211021222220222200222002002112120022222200120222212112022222012212211200020211012222022222212220121001222202222222122221122222120012212220220221102222210122212201122211222212202020010122112220221202021202110222002212120022021010002222012202212220121110022212201220022021221121100122212221022110211220102122222212022202220102022101000002122200022212222012210102122222120210120211012222202201212222021022221222212221122022222021212022202122120222200222101121222201122200222022012111121222121212120222022212200222022212112012122100112222022210022220222102222222212220222220022221012202212222021111021220121221202221122222220002002100011002102202022002112202010202102202121201021112112222222211002121020102020202201220122120121122121212212121122222102220120120222222222211211001012012010212012201121212220202101222202222121220221221012222012222202220122020120202201222122222021120010000202122020001001220220121222210222200200210212210201012102010120212101122020112122222100020121112002222202211102121220010121222210220022020021120100122222022021211101220210020222221122211201201202212001002122121021212100212102202122202202201121200122222022221102220021202221212220221222022022221222100212020120201112220002220222221122220222101022012211102101112220012111202000012022212101102021222022220222200202222221112220212212222122121122221002220212021221102220221012220212222022212212200212111221012202110021222112022022122022222210221022110222221212202222021221210020222200222222022220020101000202021121021100222202222202221122210210000202121020022110001022212100112011002212212112022021210212220212202012020021021121212222220222220021120021211222121121210220220101121212220222201212012012210210012201001020102120012221212012222221000120001022220022212102120201120122202221220122022021121200200212012022002100220111222222220222210210021102021110002011101222202020022101012212202220102220010202220202212201122220122221012211222222222021022001100222210121122011221122122212211102211212011102020102122012022022012102112111112122022110111121012102222102201020120012012220022211221022121121122121212212022122110112222022120112211012220200210202202011012021010021202210112220002002102121212121212222222022220202221102120022222200222222221222221102011212220120220112222021222112202212202220120012102011222102220222022210112021102202012120010020022222222202202110221110021021102101222222022222220022102212001220122001220121220102212222210211100022021011012120210221022112012212212002212020011120110002220112222012020122111021001111220222220012121222122212121020212100222021022212202202211202112112112201002122121222202221102121002112012022110021110212222002201100120122210220220001220122021212120210212202021220020112220210021002201122221200220222021022122111002222002022012111002222002021121222212002221022210211220220102222101200221122021010121121020212222222122001220112121122222222202201012102100100012210221222112010222121212122022201120021201022222012202122220202122020210122220122221002021110001212022020102200220220222112222012212202010112022121012011102121022111012121102100222122012122200002220022210201020222210021121120220122020212220201202212111021212121222021022202221002200211102222010210022010202222012212022111012022002122012221221212222122220102222010100222111011220022120011222201011202211020200001222222120222201222212202220122200000222000010102202102212100122222222212101120212022221022210120020211020022202222221022222000221222220222021122111112221222021112222112220202120002000001002220211200020120212021212001022011221020221122222212210102121100102220100022220022212000222121212202011010220121221211220102222012220202220002000010222010021001202121222110212200112000120122111202200112200210221011102222201202220022121110022002010222102210212120222212121102012222200201020022212000212101011122222022022010002021022002212221012022211202200202220001202221112121222022002022121221120210220011002121220002022002001022201210221222021121202221221100022120002001222010112212010121020202201022202110021100020200012021110100000212101100120000221211202121102220002001020111011021022201112011000011201010111000210102000112120100201110001110112221020202000'

# Treat the input as a string
strLen=len(inStr)

# Print statistics
print("\nStatistics\nlen :",strLen)
width = 25
height = 6
pixelsPerLayer = width * height
print("Pixels/layer :",pixelsPerLayer)
layers = strLen/pixelsPerLayer
print("Layers :",layers)

# Things that I want to know 
layerWithLowestNumberZeros = 0
numZeroLowestLevel = pixelsPerLayer
pixelOff = 0

# Count the number of Zero Digits in each frame
for layer in range(layers):
	zeroDigits = 0
	for pixels in range(pixelsPerLayer):
		if inStr[(layer*pixelsPerLayer)+pixels] == '0':
			zeroDigits = zeroDigits + 1
	#print("Layer",layer,"zeroDigits",zeroDigits)
	if zeroDigits < numZeroLowestLevel:
		layerWithLowestNumberZeros = layer
		numZeroLowestLevel = zeroDigits
#print("layerWithLowestNumberZeros",layerWithLowestNumberZeros,"numZeroLowestLevel",numZeroLowestLevel)

# Now that I know the frame number, go through just that frame
numberOfOnes = 0
numberOfTwos = 0
for pixels in range(pixelsPerLayer):
	if inStr[(layerWithLowestNumberZeros*pixelsPerLayer)+pixels] == '1':
		numberOfOnes = numberOfOnes + 1
	elif inStr[(layerWithLowestNumberZeros*pixelsPerLayer)+pixels] == '2':
		 numberOfTwos = numberOfTwos + 1
print("\n*** Product =",numberOfOnes*numberOfTwos," ***")

		