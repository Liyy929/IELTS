# 雅思阅读生词自动化工作流 (IELTS Vocab Workflow)

一个专为雅思备考打造的全自动划词生词本工具。你只需在新东方雅思网页上划词，系统就会自动提取真题原句，利用 AI 结合语境给出精准的中文释义，并自动存入生词本，最后支持一键导出为可复习的 Excel 表格。

## ✨ 功能特性

- **网页划词即存**：支持划选单个单词或短语（如 `in spite of`）。
- **AI 智能纠错**：如果你划词时漏了一两个字母（比如漏划了 `towns` 变成 `tow`），AI 会根据真题原句自动帮你补全。
- **精准语境释义**：拒绝生搬硬套的词典翻译！AI 会根据雅思真题原句，给出最符合当前语境的词性和中文释义。
- **真题例句截取**：自动抓取网页中的整句真题原文作为复习例句。
- **一键导出 Excel**：支持自定义排版，例句中的目标单词会自动高亮红色，并留有空白复习列。
- **生词本可视化管理**：自带本地 GUI 界面，支持搜索、查看和删除生词。
- **AI 去重机制**：重复划选的单词自动跳过，不花冤枉钱，保持生词本干净。


## 🚀 安装与使用指南（只要一点耐心，包教包会！）

### 📋 准备工作
在开始部署之前，请确保你的电脑具备以下环境：
1. **Windows 10/11 系统**
2. **Python 3.8 及以上版本**（安装时请务必勾选 `Add Python to PATH`）
3. **Google Chrome 浏览器**
4. **一个 DeepSeek API Key**（获取地址：[platform.deepseek.com](https://platform.deepseek.com)，新注册有免费额度，非常便宜）

### 步骤一：下载项目
*   **方法A（推荐给非开发者）**：点击本项目页面右上角的绿色 `Code` 按钮，选择 `Download ZIP`，将项目解压到电脑某个纯英文路径下（例如 `D:\Project\IELTS_Vocab_Workflow`，**强烈建议不要放在带中文的路径下**，否则容易报错）。
*   **方法B（推荐给开发者）**：在终端运行 `git clone https://github.com/Liyy929/IELTS.git`

### 步骤二：安装 Python 依赖
打开电脑的终端（PowerShell 或 CMD），进入项目文件夹：
```bash
cd D:\Project\IELTS_Vocab_Workflow
```
然后运行以下命令安装所需的 Python 库：
```bash
pip install -r requirements.txt
```
*(如果没有 `requirements.txt`，请手动运行 `pip install flask flask-cors requests openpyxl`)*

### 步骤三：配置 API Key
1. 在项目文件夹中，找到 `config.example.env` 文件，将其**复制一份**，并重命名为 `config.env`。
2. 用记事本或 VS Code 打开 `config.env`，填入你的 DeepSeek API Key：
```env
DEEPSEEK_API_KEY=sk-你的真实API密钥填在这里
```
*(注意：请不要加引号，直接写 `sk-xxxx` 即可。保存后关闭。)*

### 步骤四：启动后端服务
1. 找到项目文件夹里的 `start.bat` 文件，**双击运行**。
2. 如果你是第一次运行，请右键 `start.bat` 点击“编辑”，确保里面的 `set PYTHON_EXE=` 后面的路径是你电脑上真实的 Python 安装路径（例如 `D:\python_app\python.exe`）。
3. 双击后，会弹出一个黑框，显示 `🚀 IELTS 生词服务已启动，监听 http://localhost:5000`。
4. **⚠️ 极其重要**：这个黑框是后台服务器，**不要关掉它！** 将它最小化即可。

### 步骤五：加载 Chrome 浏览器扩展
1. 打开 Chrome 浏览器，在地址栏输入 `chrome://extensions/` 并回车。
2. 打开右上角的 **“开发者模式”** 开关。
3. 点击左上角的 **“加载已解压的扩展程序”**。
4. 选择项目文件夹里的 `extension` 文件夹。
5. 扩展加载成功后，建议点击浏览器工具栏的拼图图标，把 `IELTS Vocab Catcher` 固定出来。

### 步骤六：开始使用
1. 打开[新东方雅思真题网页](https://ieltscat.xdf.cn/)。
2. 在阅读文章中，用鼠标左键长按并拖动，选中一个单词或短语（松开鼠标左键的瞬间即可触发）。
3. 打开项目文件夹里的 `vocab_data.json` 文件，看看是否自动存入了单词、词性和结合真题语境的释义。

### 步骤七：导出与复习
*   **导出Excel**：双击 `export.bat`（或者运行 `python export_gui.py`），在弹出的窗口设置每组单词数和空白列数，点击“一键导出”。
*   **管理生词**：双击 `manage.bat`（或者运行 `python manage_gui.py`），可以搜索或删除生词。

## ❓ 常见问题排查 (FAQ)

*   **划词没反应？**
    *   检查 `start.bat` 的黑框是否还开着。如果关了，请重新双击。
    *   去 Chrome 扩展页面刷新一下 `IELTS Vocab Catcher`。
*   **提示“查询失败”或“401错误”？**
    *   说明你的 API Key 配置不对。请检查 `config.env` 里的 Key 是否以 `sk-` 开头，有没有多余空格，以及账户是否有余额。
*   **终端提示网络错误 `Could not resolve host`？**
    *   这是 GitHub 网络波动，请尝试连接手机热点后重试。
