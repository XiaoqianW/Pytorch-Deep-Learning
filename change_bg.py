import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# 建立显示图片的函数
def show(image):
    plt.imshow(image)
    plt.axis('off')
    plt.show()

or_path = "D:/u/wxq/features/bg_helmet_output/cut_output/" # 原图所在路径
file = os.walk(or_path)

for path, dir, filelist in file:
    for filename in filelist:
        if filename.endswith('.jpg') or filename.endswith(".JPG"):
            filepath = os.path.join(path, filename)
            img = cv2.imread(filepath)
            # print(filename)

            # 导入前景图
            # img = cv2.imread('D:/u/wxq/features/hat/1/part_A0001.jpg')  # 图片导入
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换颜色模型
            print("前景图规格",img.shape)  # 打印图片规格
            # show(img)  # 显示图片

            # 裁剪图片
            # img = img[0:1000,150:550] #裁剪图片大小
            # print("裁剪前景图后的规格",img.shape) #打印图片规格
            # show(img) #显示图片

            # 缩放图片
            img = cv2.resize(img, None, fx=0.5, fy=0.5)  # 图片缩小50%
            print("缩放前景图后的规格", img.shape)  # 打印图片规格
            # 拆分图片信息
            rows, cols, channels = img.shape  # 拆分图片信息
            w = rows/2
            h = cols/2
            # 转换格式
            img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)  # 把图片转换成HSV格式，用于抠图
            # show(img_hsv)  # 显示图片
            # 抠图
            lower_blue = np.array([0, 0, 0])  # 获取最小阈值
            upper_blue = np.array([0, 255, 255])  # 获取最大阈值
            mask = cv2.inRange(img_hsv, lower_blue, upper_blue)  # 创建遮罩
            show(mask)  # 显示遮罩
            erode = cv2.erode(mask, None, iterations=3)  # 图像腐蚀
            # show(erode)  # 显示图片
            dilate = cv2.dilate(erode, None, iterations=1)  # 图像膨胀
            # show(dilate)  # 显示图片
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8)))  # 开运算
            # show(opening)  # 显示图片
            a = 0

            bg_path = "D:/u/wxq/features/bg_helmet_output/bg/" # 背景图所在路径
            bg_file = os.walk(bg_path)
            # 读取背景
            for bg_path, bg_dir, bg_filelist in bg_file:
                for bg_filename in bg_filelist:
                    a = a+1
                    if bg_filename.endswith('.jpg') or bg_filename.endswith(".JPG"):
                        bg_filepath = os.path.join(bg_path, bg_filename)
                        back_img = cv2.imread(bg_filepath)
                        print(bg_filename)
                        # 导入背景图
                        # back_img = cv2.imread('D:/123.jpg')  # 图片导入
                        back_img = cv2.cvtColor(back_img, cv2.COLOR_BGR2RGB)  # 转换颜色模型
                        print("背景图规格", back_img.shape)  # 打印图片规格
                        bg_rows, bg_cols, channels = back_img.shape  # 拆分图片信息
                        # show(back_img)  # 显示图片
                        bg_w = int((bg_rows/2)-w)
                        bg_h = int((bg_cols/2)-h)
                        center = [bg_w, bg_h]  # 设置前景图开始位置
                        try:
                            for i in range(rows):
                                for j in range(cols):
                                    if opening[i, j] == 0:  # 代表黑色
                                        back_img[center[0] + i, center[1] + j] = img[i, j]  # 赋值颜色
                        except:
                            print(bg_filename)
                        # show(back_img)  # 显示图片

                        back_img = cv2.cvtColor(back_img, cv2.COLOR_RGB2BGR)  # 图像格式转换
                        # back_img = cv2.resize(back_img, None, fx=0.8, fy=0.8)  # 图像缩放20%
                        # cv2.imwrite('result.png', back_img)  # 保存图像
                        cv2.imwrite(os.path.join("D:/u/wxq/features/bg_helmet_output/bg_cut_output/", str(a)+"_"+filename), back_img) # 需要修改保存路径