项目结构
pipeline_defect_detection/            # 项目根目录
│
├── main.py                           # 主程序入口
├── requirements.txt                  # 项目依赖包列表
├── README.md                         # 项目说明文档
│
├── config/                           # 配置文件目录
│   ├── camera_config.json            # 相机参数配置
│   ├── detection_config.json         # 检测算法参数配置
│   └── system_config.json            # 系统全局配置
│
├── data/                             # 数据目录
│   ├── dataset/                      # 数据集
│   │   ├── images/                   # 原始图像
│   │   ├── depth/                    # 深度图像
│   │   └── labels/                   # 标注数据
│   ├── models/                       # 预训练模型
│   └── results/                      # 检测结果保存
│
├── src/                              # 源代码目录
│   ├── __init__.py
│   │
│   ├── acquisition/                  # 图像采集模块
│   │   ├── __init__.py
│   │   ├── image_acquisition.py      # 相机图像采集
│   │   └── camera_calibration.py     # 相机标定
│   │
│   ├── preprocessing/                # 预处理模块
│   │   ├── __init__.py
│   │   └── image_preprocessing.py    # 图像预处理
│   │
│   ├── detection/                    # 缺陷检测模块
│   │   ├── __init__.py
│   │   ├── defect_detection.py       # 缺陷检测算法
│   │   └── models.py                 # 深度学习模型定义
│   │
│   ├── reconstruction/               # 三维重建模块
│   │   ├── __init__.py
│   │   └── point_cloud_processing.py # 点云处理
│   │
│   ├── utils/                        # 工具函数
│   │   ├── __init__.py
│   │   ├── visualization.py          # 可视化工具
│   │   └── file_utils.py             # 文件操作工具
│   │
│   └── ui/                           # 用户界面
│       ├── __init__.py
│       ├── main_window.py            # 主窗口
│       ├── detection_panel.py        # 检测面板
│       └── visualization_panel.py    # 可视化面板
│
├── tests/                            # 测试代码
│   ├── test_acquisition.py
│   ├── test_preprocessing.py
│   ├── test_detection.py
│   └── test_reconstruction.py
│
└── docs/                             # 文档
    ├── user_manual.md                # 用户手册
    ├── development_guide.md          # 开发指南
    └── api_reference.md              # API参考文档