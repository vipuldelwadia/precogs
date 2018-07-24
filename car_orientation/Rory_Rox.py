from PIL import Image
import glob

cars_images_dir = '/Users/rologan/Documents/Machine_learning/Datasets/cars/KITTI/training/images'
car_labels_dir = '/Users/rologan/Documents/Machine_learning/Datasets/cars/KITTI/training/labels'  


# Read in the label text file

# Get the CAR, VAN OR TRUCK LINES and generate cropped images for each 
    
# generate new label files for each line

# print(glob.glob("/Users/rologan/Documents/Machine_learning/Datasets/cars/KITTI/training/labels/*.txt"))

arrayOfImagePaths = glob.glob("/Users/rologan/Documents/Machine_learning/Datasets/cars/KITTI/training/images/*.png")
arrayOfLabelPaths = glob.glob("/Users/rologan/Documents/Machine_learning/Datasets/cars/KITTI/training/labels/*.txt")

count = 0

box = "498.85 149.49 551.40 204.32"

boundingBoxes = [list(map(float, box.split(" ")))]

for idx, val in enumerate(boundingBoxes):
    print(arrayOfImagePaths[idx])
    print(val)
    if len(val) == 0:
        continue
    image = Image.open(arrayOfImagePaths[idx])
    cropped = image.crop(val)
    cropped.save(arrayOfImagePaths[idx])
   

'''
image_obj = Image.open(image_path)
cropped_image = image_obj.crop(coords)
cropped_image.save(saved_location)
cropped_image.show()
  


if __name__ == '__main__':
    image = 'grasshopper.jpg'
    crop(image, (161, 166, 706, 1050), 'cropped.jpg')
'''