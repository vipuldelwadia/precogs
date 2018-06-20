import os

class ImageInfo:
    __fileNumber = ""
    __imageIndex = 0
    __filePath = "", ""
    __alpha = 0.00
    __topX, __topY, __bottomX, __bottomY, __angle = 0, 0, 0, 0, 0

    def __init__(self, idx, filePath, words):
        self.__fileNumber = int(os.path.basename(filePath).split(".")[0])
        self.__imageIndex = idx
        self.__filePath = filePath
        self.__angle = words[3]
        self.__topX = words[4]
        self.__topY = words[5]
        self.__bottomX = words[6]
        self.__bottomY = words[7]

    @property
    def FileNumber(self):
        return self.__fileNumber
    
    @property
    def ImageIndex(self):
        return self.__imageIndex

    @property
    def FilePath(self):
        return self.__filePath

    @property
    def FileName(self):
        return self.__fileName

    @property
    def TopX(self):
        return self.__topX

    @property
    def TopY(self):
        return self.__topY

    @property
    def BottomX(self):
        return self.__bottomX

    @property
    def BottomY(self):
        return self.__bottomY

    @property
    def Angle(self):
        return self.__angle


class ImageInfoFactory:

    def CreateListFromFile(filepath):

        result = []
        valid_cars = ["Car", "Van", "Truck"]

        fo = open(filepath, "r")
        
        lines = fo.readlines()
        for idx, line in enumerate(lines):
            words = line.split(" ")
            if words[0] in valid_cars and words[1] == "0.00" and words[2] == "0": # Ignores Invalid/Truncated/Occluded Cars
                result.append(ImageInfo(idx, filepath, words))

        fo.close()

        return result

# Example of using the code

rootdir = '/Users/rologan/Documents/Machine_learning/Datasets/cars/KITTI/training/labels'
results = []

#arrayOfLabelPaths = glob.glob("/Users/rologan/Documents/Machine_learning/Datasets/cars/KITTI/training/labels/*.txt")
# Navigate through all folders and subfolders
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir, file)
        #print("Reading file: ", path)
        results.extend(ImageInfoFactory.CreateListFromFile(path))


outputDir = "/Users/rologan/Documents/Machine_learning/Datasets/AI_precogs/labels/"
    
for r in results:
    number = "" + str(r.FileNumber)
    newfilename = outputDir + number.zfill(6) + "_" + str(r.ImageIndex) + ".txt"
    fo = open(newfilename, "w")
    fo.write(number.zfill(6) + "," + str(r.ImageIndex) + "," + str(r.Angle) + "," + str(r.TopX) + "," + str(r.TopY) + "," + str(r.BottomX)+ "," + str(r.BottomY))
    fo.close()
    #print(r.FilePath, r.ImageIndex, r.FileNumber, r.Angle, r.TopX, r.TopY, r.BottomX, r.BottomY)

