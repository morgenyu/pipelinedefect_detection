# image_preprocessing.py
import cv2
import numpy as np
from skimage import exposure

class ImagePreprocessor:
    def __init__(self):
        pass
    
    def denoise(self, image, method='gaussian', kernel_size=5):
        """
        图像去噪处理
        
        参数:
            image: 输入图像
            method: 去噪方法 ('gaussian', 'median', 'bilateral')
            kernel_size: 核大小
        """
        if method == 'gaussian':
            return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        elif method == 'median':
            return cv2.medianBlur(image, kernel_size)
        elif method == 'bilateral':
            return cv2.bilateralFilter(image, kernel_size, 75, 75)
        else:
            return image
    
    def enhance_contrast(self, image, method='clahe'):
        """
        增强图像对比度
        
        参数:
            image: 输入图像
            method: 增强方法 ('clahe', 'histogram_equalization', 'adaptive_equalization')
        """
        # 转换为灰度图像
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        if method == 'clahe':
            # 对比度受限的自适应直方图均衡化
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            return clahe.apply(gray)
        elif method == 'histogram_equalization':
            # 普通直方图均衡化
            return cv2.equalizeHist(gray)
        elif method == 'adaptive_equalization':
            # scikit-image的自适应均衡化
            return exposure.equalize_adapthist(gray, clip_limit=0.03)
        else:
            return gray
    
    def edge_detection(self, image, method='canny', threshold1=50, threshold2=150):
        """
        边缘检测
        
        参数:
            image: 输入图像
            method: 检测方法 ('canny', 'sobel')
            threshold1, threshold2: Canny边缘检测的阈值
        """
        # 确保图像是灰度的
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        if method == 'canny':
            return cv2.Canny(gray, threshold1, threshold2)
        elif method == 'sobel':
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            # 计算梯度幅值
            magnitude = np.sqrt(sobelx**2 + sobely**2).astype(np.uint8)
            return magnitude
        else:
            return gray
    
    def segment_defects(self, image, threshold_value=127, max_value=255, threshold_type=cv2.THRESH_BINARY):
        """
        使用阈值分割潜在缺陷区域
        
        参数:
            image: 输入图像
            threshold_value: 阈值
            max_value: 超过阈值时的值
            threshold_type: 阈值类型
        """
        # 确保图像是灰度的
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # 应用阈值
        _, thresh = cv2.threshold(gray, threshold_value, max_value, threshold_type)
        return thresh
    
    def preprocess_pipeline(self, image):
        """
        完整的预处理流程
        
        参数:
            image: 输入RGB图像
        """
        # 1. 去噪
        denoised = self.denoise(image, method='gaussian')
        
        # 2. 对比度增强
        enhanced = self.enhance_contrast(denoised, method='clahe')
        
        # 3. 边缘检测
        edges = self.edge_detection(enhanced, method='canny')
        
        # 4. 形态学操作 - 闭运算（先膨胀后腐蚀）填充边缘内的小洞
        kernel = np.ones((5, 5), np.uint8)
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        return {
            'denoised': denoised,
            'enhanced': enhanced,
            'edges': edges,
            'processed': closed
        }

# 使用示例
if __name__ == "__main__":
    # 加载测试图像
    image_path = "sample_pipe.jpg"  # 替换为你的管道图像路径
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"无法加载图像: {image_path}")
    else:
        # 创建预处理器
        preprocessor = ImagePreprocessor()
        
        # 应用预处理流程
        results = preprocessor.preprocess_pipeline(image)
        
        # 显示结果
        cv2.imshow('Original', image)
        cv2.imshow('Denoised', results['denoised'])
        cv2.imshow('Enhanced', results['enhanced'])
        cv2.imshow('Edges', results['edges'])
        cv2.imshow('Processed', results['processed'])
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()