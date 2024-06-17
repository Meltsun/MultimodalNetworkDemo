import sys
from pathlib import Path

def setup_path():
    # 获取当前脚本的目录
    current_dir = Path(__file__).resolve().parent

    # 设置项目根目录
    project_root = current_dir

    # 将项目根目录添加到 sys.path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

# 调用函数设置路径
setup_path()