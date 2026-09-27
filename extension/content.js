// 提取选中单词所在的完整句子
function getSentenceFromSelection(selection) {
    let node = selection.anchorNode;
    while (node && node.nodeType !== 1) node = node.parentNode;
    while (node && !['P', 'DIV', 'LI', 'TD', 'ARTICLE', 'SECTION'].includes(node.tagName)) {
        node = node.parentNode;
    }
    if (!node) return '';

    const fullText = node.innerText || '';
    const word = selection.toString().trim();
    const idx = fullText.toLowerCase().indexOf(word.toLowerCase());
    if (idx === -1) return fullText.slice(0, 300);

    let start = idx;
    while (start > 0 && !'.!?\n'.includes(fullText[start - 1])) start--;
    let end = idx + word.length;
    while (end < fullText.length && !'.!?\n'.includes(fullText[end])) end++;

    return fullText.slice(start, Math.min(end + 1, fullText.length)).trim();
}

document.addEventListener('mouseup', async () => {
    const selection = window.getSelection();
    if (!selection || !selection.toString().trim()) return;

    // 1. 原始划词
    let word = selection.toString().trim();
    
    // 2. 基础清洗（去首尾标点、合并连续空格）
    word = word.replace(/^[^a-zA-Z]+/, '').replace(/[^a-zA-Z]+$/, '').trim();
    word = word.replace(/\s+/g, ' ');

    // 3. 正则校验（支持纯单词和短语，最多5个词）
    if (!/^[a-zA-Z][a-zA-Z\s'-]*[a-zA-Z]$/.test(word)) return;
    if (word.length < 2 || word.length > 50) return;
    if (word.split(/\s+/).length > 5) return;

    // 4. 提取真题原句
    const sentence = getSentenceFromSelection(selection);

    const sourceUrl = window.location.href;

    try {
        const resp = await fetch('http://localhost:5000/add_word', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                word: word.toLowerCase(), // 统一转小写发送
                sentence: sentence,
                url: sourceUrl
            })
        });
        const result = await resp.json();
        if (result.status === 'ok') {
            console.log(`✅ ${result.msg}`);
        }
    } catch (err) {
        console.warn('本地服务未启动，单词未保存:', err.message);
    }
});