# PyGeogebra - 强大的几何绘图工具

一个功能完整、类似 GeoGebra 的 Python 几何绘图工具，具有精美的用户界面和强大的功能。

## 🌟 主要功能

### 基础形状
- ✅ 点、线段、射线、直线
- ✅ 圆、椭圆、圆弧
- ✅ 多边形、矩形、正多边形
- ✅ 自由曲线

### 几何变换
- ✅ 平移（Translation）
- ✅ 旋转（Rotation）
- ✅ 缩放（Scaling）
- ✅ 反射（Reflection）
- ✅ 剪切变换（Shear）
- ✅ 对称变换

### 测量工具
- ✅ 距离测量
- ✅ 角度测量
- ✅ 周长计算
- ✅ 面积计算
- ✅ 坐标显示

### 高级功能
- ✅ 交点自动检测
- ✅ 对象命名和标签
- ✅ 几何约束（平行、垂直、相切）
- ✅ 参数化和动画
- ✅ 轨迹追踪
- ✅ 撤销/重做
- ✅ 导出 PNG/SVG/PDF

### UI 特性
- ✅ 现代化界面
- ✅ 工具栏和菜单
- ✅ 属性编辑面板
- ✅ 图层管理
- ✅ 网格和坐标系
- ✅ 主题切换

## 📦 安装

```bash
pip install -r requirements.txt
python main.py
```

## 🚀 使用方法

1. 启动应用程序
2. 从工具栏选择绘图工具
3. 在画布上点击创建对象
4. 使用属性面板编辑对象属性
5. 导出结果

## 📁 项目结构

```
PyGeogebra/
├── main.py                 # 主程序入口
├── core/
│   ├── geometry.py        # 几何对象基类
│   ├── shapes.py          # 形状类定义
│   ├── transforms.py      # 变换模块
│   ├── measurements.py    # 测量工具
│   └── constraints.py     # 约束系统
├── ui/
│   ├── main_window.py     # 主窗口
│   ├── canvas.py          # 绘图画布
│   ├── toolbar.py         # 工具栏
│   └── panels.py          # 侧面板
├── utils/
│   ├── math_utils.py      # 数学工具函数
│   ├── export.py          # 导出功能
│   └── config.py          # 配置文件
└── requirements.txt       # 依赖列表
```

## 🎨 技术栈

- **GUI框架**: PyQt6
- **数学计算**: NumPy
- **可视化**: Matplotlib
- **导出**: Pillow, ReportLab
- **语言**: Python 3.9+

## 📝 许可证

MIT License

## 👨‍💻 开发者

zhangjinzhi215-netizen

---

**让我们开始画几何图形吧！** ✨
