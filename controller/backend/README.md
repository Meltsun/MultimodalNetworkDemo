## 后端文件开启：
在fastapi_work1文件中运行
```python
python main.py
```
在ubuntu服务器上，我们目前使用的ubuntu版本为20.04.1 LTS，python版本为Python 3.10.10
在运行之前需要先下载fastapi和sqlmodel

```python
pip install fastapi
pip install sqlmodel
```

## 错误解决：
如果服务器python版本为3.8.10，可能会出现：
```python
TypeError: 'type' object is not subscriptable
```
这是因为在 Python 3.9 之前的版本中，list 不能直接用于类型注解，
解决方法为
```python
从 typing 模块中导入 List
from typing import List
将错误提示中的list替换为 List
```