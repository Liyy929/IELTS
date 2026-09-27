# 雅思阅读生词工作流 (IELTS Vocab Workflow)

一个自动化工具，帮助你在新东方雅思真题网页上划词，自动查询中文释义、截取真题例句，并一键导出为可复习的 Excel 表格。

## ✨ 功能特性

- 🖱️ **网页划词即存**：在新东方雅思网页上选中英文单词或短语，自动保存到生词本
- 🧠 **AI 语境释义**：结合真题原文，由大模型给出精准的中文释义和词性，
- 📝 **真题例句截取**：自动从网页中提取单词所在的完整句子作为例句辅助单词的理解和记忆
- 📊 **一键导出 Excel**：按自定义列数排列并且可以自定义空白复习列数量，例句中目标单词红色高亮
- 🗂️ **生词本管理**：提供本地管理界面，支持查看、搜索和删除词条

## 🛠️ 技术栈

- **浏览器扩展**：JavaScript (Chrome Extension Manifest V3)
- **后端服务**：Python Flask
- **AI 查词**：DeepSeek API
- **Excel 导出**：openpyxl
- **本地管理界面**：Tkinter

## 📦 安装与使用

### 1. 环境要求

- Python 3.8+
- Chrome 浏览器

### 2. 安装依赖

```bash
pip install flask requests openpyxl flask-cors
