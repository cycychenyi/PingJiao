## 武汉大学评教脚本 v1.0

用 Python 写的脚本，用于 2019 年秋季评教。

码字过程记录在 [知乎](https://zhuanlan.zhihu.com/p/97320141) 了。

注意，由于我的课程只有 10 个，刚好在一页里显示了，多页的情况可能有所不同。

**使用**

1. 安装 Python。
2. 安装第三方库。

```bash
pip install requests lxml PyExecJS click
```

3. 克隆仓库。

```bash
git clone https://github.com/cycychenyi/PingJiao.git
```

或直接下载 pingjiao.py 和 encrypt.js，注意放在同一目录下。

4. 在 pingjiao.py 所在目录按住 Shift 右键打开 Powershell 窗口。

<div align="center"><img src="https://i.loli.net/2019/12/15/vVTMrnqWZilhgO1.png" style="zoom: 67%;" /></div>

5. 运行。

<div align="center"><img src="https://i.loli.net/2019/12/15/rj3ApLq6Zfwig9D.png" style="zoom:80%;" /></div>

## 武汉大学评教脚本 v2.0

改用 Selenium，用于 2020 年春季评教。

**使用**

1. 安装 Python。
2. 安装第三方库。

```bash
pip install click selenium
# 或者
pip install -r requirements.txt
```

3. 克隆仓库。

```bash
git clone https://github.com/cycychenyi/PingJiao.git
```

chromedriver 目录下的 chromedriver.exe 和 chromedriver 对应 83 版本的 Chrome，其它版本请自行下载。

4. 运行 pingjiao.py。