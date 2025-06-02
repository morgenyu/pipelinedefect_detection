# image_acquisition.py
import pyrealsense2 as rs
import numpy as np
import cv2
import time

class PipelineImageAcquisition:
    def __init__(self):
        # 初始化RealSense相机
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        
        # 配置相机流
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        
        # 初始化对齐对象
        self.align = rs.align(rs.stream.color)
        
        print("初始化相机完成")
        
    def start(self):
        """启动相机流"""
        self.profile = self.pipeline.start(self.config)
        print("相机已启动")
        
    def stop(self):
        """停止相机流"""
        self.pipeline.stop()
        print("相机已停止")
        
    def get_frames(self):
        """获取一帧图像和深度数据"""
        # 等待获取图像帧
        frames = self.pipeline.wait_for_frames()
        
        # 对齐深度帧与彩色帧
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        
        if not depth_frame or not color_frame:
            return None, None
            
        # 转换为numpy数组
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        return color_image, depth_image
    
    def capture_dataset(self, num_frames=10, save_dir="./dataset"):
        """捕获多帧图像作为数据集"""
        import os
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        print(f"开始采集{num_frames}帧图像...")
        for i in range(num_frames):
            color_img, depth_img = self.get_frames()
            if color_img is not None and depth_img is not None:
                # 保存图像
                cv2.imwrite(f"{save_dir}/color_{i}.jpg", color_img)
                np.save(f"{save_dir}/depth_{i}.npy", depth_img)
                print(f"已保存第{i+1}帧")
                time.sleep(1)  # 等待1秒
        
        print("数据集采集完成")

# 使用示例
if __name__ == "__main__":
    try:
        # 创建图像采集对象
        acquisition = PipelineImageAcquisition()
        acquisition.start()
        
        # 显示实时预览
        print("按'q'退出预览, 's'保存当前帧")
        while True:
            color_img, depth_img = acquisition.get_frames()
            if color_img is not None:
                # 将深度图转换为伪彩色图像以便显示
                depth_colormap = cv2.applyColorMap(
                    cv2.convertScaleAbs(depth_img, alpha=0.03), 
                    cv2.COLORMAP_JET
                )
                
                # 显示图像
                cv2.imshow('Color Image', color_img)
                cv2.imshow('Depth Image', depth_colormap)
                
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
                elif key & 0xFF == ord('s'):
                    # 保存当前帧
                    cv2.imwrite(f"color_frame.jpg", color_img)
                    np.save(f"depth_frame.npy", depth_img)
                    print("已保存当前帧")
                    
        # 采集数据集
        # acquisition.capture_dataset(num_frames=20)
                    
    finally:
        # 关闭相机
        acquisition.stop()
        cv2.destroyAllWindows()