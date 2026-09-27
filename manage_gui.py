import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "vocab_data.json")

class VocabManager:
    def __init__(self, root):
        self.root = root
        self.root.title("雅思生词本管理")
        self.root.geometry("800x500")
        
        self.all_words = []
        self.load_data()

        # 顶部搜索框
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(top_frame, text="🔍 搜索:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_data)
        entry_search = tk.Entry(top_frame, textvariable=self.search_var, width=30)
        entry_search.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(top_frame, text="🔄 刷新列表", command=self.refresh)
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # 表格区域
        columns = ("word", "pos", "meaning", "example")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("word", text="单词 / 短语")
        self.tree.heading("pos", text="词性")
        self.tree.heading("meaning", text="中文释义")
        self.tree.heading("example", text="真题例句")
        
        self.tree.column("word", width=120, anchor="w")
        self.tree.column("pos", width=60, anchor="center")
        self.tree.column("meaning", width=180, anchor="w")
        self.tree.column("example", width=400, anchor="w")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 底部按钮
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        btn_delete = tk.Button(bottom_frame, text="🗑️ 删除选中词条", bg="#FF4C4C", fg="white", command=self.delete_selected)
        btn_delete.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(bottom_frame, text=f"总计: {len(self.all_words)} 条", fg="gray")
        self.status_label.pack(side=tk.RIGHT)

        self.refresh()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.all_words = data.get("words", [])
        else:
            self.all_words = []

    def refresh(self):
        """重新加载数据并刷新表格"""
        self.load_data()
        self.search_var.set("") # 清空搜索框
        self.populate_table(self.all_words)
        self.status_label.config(text=f"总计: {len(self.all_words)} 条")

    def populate_table(self, words):
        """把数据填入表格"""
        # 清空旧数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 填入新数据
        for w in words:
            example = w.get("example", "")
            # 如果例句太长，稍微截断显示，但完整数据还在 JSON 里
            display_example = (example[:80] + "...") if len(example) > 80 else example
            self.tree.insert("", tk.END, values=(w["word"], w.get("pos", ""), w.get("meaning", ""), display_example))

    def filter_data(self, *args):
        """根据搜索框内容过滤"""
        keyword = self.search_var.get().strip().lower()
        if not keyword:
            self.populate_table(self.all_words)
        else:
            filtered = [w for w in self.all_words if keyword in w["word"].lower() or keyword in w.get("meaning", "").lower()]
            self.populate_table(filtered)

    def delete_selected(self):
        """直接从本地 JSON 文件中删除选中的单词"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("未选择", "请先在表格中点击选中要删除的词条。")
            return

        # 提取选中的单词
        word_to_delete = self.tree.item(selected[0])["values"][0]

        # 确认删除
        confirm = messagebox.askyesno("确认删除", f"确定要删除 '{word_to_delete}' 吗？")
        if not confirm:
            return

        try:
            # 1. 读取当前 JSON 文件
            if not os.path.exists(DATA_FILE):
                messagebox.showerror("错误", "生词数据文件不存在！")
                return

            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 2. 过滤掉要删除的单词
            original_len = len(data.get("words", []))
            data["words"] = [w for w in data.get("words", []) if w["word"] != word_to_delete]
            new_len = len(data["words"])

            if original_len == new_len:
                messagebox.showwarning("未找到", f"在数据文件中找不到 '{word_to_delete}'，可能已被删除。")
                self.refresh()
                return

            # 3. 写回文件
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("成功", f"'{word_to_delete}' 已从生词本中删除！")
            self.refresh() # 刷新表格视图

        except Exception as e:
            messagebox.showerror("错误", f"删除失败，发生异常:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabManager(root)
    root.mainloop()