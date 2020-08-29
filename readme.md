## 健康检查

### 环境要求

python == 3.7 amd64

### 虚拟环境

#### 安装虚拟环境

```bash
pip install virtualenv
virtualenv ENV
```

#### 进入虚拟环境

```powershell
# Windows
.\ENV\Scripts\activate
```

```bash
# Linux
./ENV/bin/activate
```

### 依赖安装

```bash
pip install -r requirements/develop.txt
```

### 运行

#### 运行检查

```bash
python run.py start-server
```

#### 配置再加载

```bash
python run.py reload-server
```