####################按xml文件裁剪图像####################
import os
import PIL.Image as Image

try:
    import xml.etree.cElementTree as ET  # 解析xml的c语言版的模块
except ImportError:
    import xml.etree.ElementTree as ET

IMAGE_DIR = "D:/u/wxq/features/hat/1234/" # 需要裁剪的图片路径
IMAGE_OUTPUT_DIR = "D:/u/wxq/features/bg_helmet_output/cut_output/" # 裁剪之后的路径
XML_DIR = 'D:/u/wxq/features/hat/Annotation1234/' # xml所在的路径

def process(image_dir, xml_dir):
    image_list = os.listdir(image_dir)
    for image_filename in image_list:
        print(image_filename)
        image_id = image_filename.split('.')[0]
        xml_path = os.path.join(xml_dir, image_id + ".xml")
        bndboxes = GetAnnotBoxLoc(xml_path)
        if bndboxes:
            CropAndSave(image_filename, image_id, bndboxes)
        # CropByBoxLoc(image_filename, bndboxes)

def GetAnnotBoxLoc(AnotPath):
    tree = ET.ElementTree(file=AnotPath)
    root = tree.getroot()
    ObjectSet = root.findall('object')
    ObjBndBoxSet = {}
    for Object in ObjectSet:
        ObjName = Object.find('name').text
        BndBox = Object.find('bndbox')

        x1 = int(BndBox.find('xmin').text)
        y1 = int(BndBox.find('ymin').text)
        x2 = int(BndBox.find('xmax').text)
        y2 = int(BndBox.find('ymax').text)
        BndBoxLoc = [x1, y1, x2, y2]
        if ObjBndBoxSet.get(ObjName):
            ObjBndBoxSet[ObjName].append(BndBoxLoc)  # 如果字典结构中含有这个类别了，那么这个目标框要追加到其值的末尾
        else:
            ObjBndBoxSet[ObjName] = [BndBoxLoc]

    return ObjBndBoxSet

def CropAndSave(img_filename, img_id, bndboxes):
    save_dir = os.path.join(IMAGE_OUTPUT_DIR) # , img_id)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    img_path = os.path.join(IMAGE_DIR, img_filename)
    print(img_filename)
    img = Image.open(img_path)

    for key in bndboxes.keys():
        boxes = bndboxes.get(key)
        print(key, boxes)
        for i, box in enumerate(boxes):
            #  进行roi裁剪
            roi_area = img.crop(box)
            # 裁剪后每个图像全路径
            save_path = os.path.join(save_dir,img_filename)
            # 保存处理图像
            roi_area = roi_area.convert("RGB")
            roi_area.save(save_path)

process(IMAGE_DIR, XML_DIR)