from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import threading
import re  # 新增：用于数据清洗
from collins_client import lookup_word

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), "vocab_data.json")
_lock = threading.Lock()

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"words": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/add_word", methods=["POST"])
def add_word():
    data = request.get_json()
    if not data or not data.get("word"):
        return jsonify({"status": "error", "msg": "缺少 word 字段"}), 400

    # 1. 数据清洗：转小写、去首尾空格、合并连续空格
    raw_word = data["word"].strip().lower()
    word = re.sub(r'\s+', ' ', raw_word)
    sentence = data.get("sentence", "").strip()
    url = data.get("url", "")

    with _lock:
        vocab = load_data()

        # 2. 调用 AI 查词，并让 AI 顺便帮我们纠正残缺的单词
        # 注意：这里必须要传 sentence，AI 才知道这个残缺单词在句子里的完整形态是什么
        local_dict = lookup_word(word, sentence)
        corrected_word = local_dict.get("corrected_word", word).strip().lower()
        
        # 🛡️ 防错机制：如果 AI 返回了非正常状态，拒绝存入词库，并告诉前端
        if "失败" in local_dict.get("meaning", "") or "异常" in local_dict.get("meaning", "") or "超时" in local_dict.get("meaning", ""):
            return jsonify({"status": "error", "msg": f"AI查询失败，未保存。原因: {local_dict.get('meaning')}"}), 500

        # 3. 用补全后的单词去重
        existing = next((w for w in vocab["words"] if w["word"] == corrected_word), None)
        if existing:
            return jsonify({"status": "ok", "msg": f"'{corrected_word}' 已存在，已跳过"})

        # 4. 保存新单词（存储的是补全后的单词，而不是你划错的残缺单词）
        # 优先使用浏览器截取的真题原句，如果没有则留空
        example = sentence if sentence else local_dict.get("example", "")

        entry = {
            "word": corrected_word,  # 存储 AI 纠错补全后的完整单词
            "pos": local_dict.get("pos", ""),
            "meaning": local_dict.get("meaning", ""),
            "example": example,
            "source_url": url
        }
        vocab["words"].append(entry)
        save_data(vocab)

    return jsonify({"status": "ok", "msg": f"已保存：{corrected_word}"})

if __name__ == "__main__":
    print("🚀 IELTS 生词服务已启动，监听 http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)