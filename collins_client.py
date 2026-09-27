import requests
import json
import os

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "YOUR_API_KEY_HERE")
API_URL = "https://api.deepseek.com/chat/completions"

def lookup_word(word, sentence=""):
    prompt = f"""你是一个雅思词典助手。请完成以下任务：
1. **单词纠错**：用户划选的单词是 '{word}'。请检查这个单词在下面这个句子中是否是一个残缺片段（用户可能漏划了字母）。
   - 如果 '{word}' 在句子中作为完整单词出现，则 corrected_word 就是 '{word}'。
   - 如果 '{word}' 是句子中某个更长单词的前缀或后缀（例如用户划了 'tow'，但句子中是 'towns'），请将 corrected_word 设为句子中那个完整的单词。
   - 如果 '{word}' 在句子中找不到任何匹配，则 corrected_word 保持为 '{word}'。
2. **释义**：给出 corrected_word 的词性（如 n., v., adj.）和简短精准的中文释义。如果 corrected_word 是残缺单词补全后的结果，请基于补全后的单词给出释义。

句子：{sentence}

请严格按照 JSON 格式输出，不要包含任何其他文字：
{{"corrected_word": "补全后的单词", "pos": "词性", "meaning": "中文释义"}}"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }

    try:
        # 把 timeout 从 15 秒延长到 30 秒，给 AI 充足的时间处理复杂语境
        resp = requests.post(API_URL, headers=headers, json=data, timeout=30)
        
        if resp.status_code != 200:
            print(f"API 响应异常，状态码: {resp.status_code}, 响应: {resp.text}")
            return {"corrected_word": word, "pos": "", "meaning": "API接口异常", "example": ""}
        
        result = resp.json()
        content = result["choices"][0]["message"]["content"].strip()
        
        # 强力清理 markdown 格式
        content = content.replace("```json", "").replace("```", "").strip()
        
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            print(f"AI 返回格式异常，无法解析为 JSON。原始内容: {content}")
            return {"corrected_word": word, "pos": "", "meaning": "AI格式解析失败", "example": ""}

        return {
            "corrected_word": parsed.get("corrected_word", word),
            "pos": parsed.get("pos", ""),
            "meaning": parsed.get("meaning", ""),
            "example": ""
        }
    except requests.exceptions.Timeout:
        print("调用大模型超时，请检查网络。")
        return {"corrected_word": word, "pos": "", "meaning": "AI响应超时", "example": ""}
    except Exception as e:
        print(f"调用大模型出错: {e}")
        return {"corrected_word": word, "pos": "", "meaning": "AI服务未连接", "example": ""}