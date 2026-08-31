# -*- coding: utf-8 -*-
"""Slug 2 follow-up: zh-TW is missing the section referenced by its TOC
(#2026-年的技術景觀). Add the section so every TOC anchor resolves."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib01 import load, save, sync_toc, cjk, h2s

SLUG = "mcp-enterprise-data-access-security-patterns"
ANCHOR = '<h2 id="技術架構與實施">'

SEC = '''<h2 id="2026-年的技術景觀">2026 年的技術景觀是什麼？</h2>
<p>2026 年企業 AI 的風險輪廓之所以發生結構性變化，根本原因不是模型變強了，而是「管線」變了。過去每一個 AI 工具都需要客製化連接器，資安團隊可以逐案審查；MCP 把這個模型顛倒過來：單一伺服器就能對外暴露數十個工具，而任何相容的用戶端——包含你無法掌握的第三方代理人——都能自行探索並呼叫它們。換句話說，一次設定錯誤的影響範圍從「單一整合」變成「系統性」。</p>
<p>經濟誘因同時放大了風險。IBM《資料外洩成本報告》指出全球平均單次外洩成本約 488 萬美元；而涉及 AI 系統的外洩通常更難察覺，因為攻擊者的行為混在正常模型流量裡，看起來與日常請求無異。防禦方因此不能再依賴「辨識異常行為」這種事後手段。</p>
<p>攻擊手法本身也已經被完整文件化。OWASP 針對大型語言模型應用的十大風險清單，把提示詞注入列為首要風險：使用者（或一份被下毒的文件）指示模型去呼叫它本不該呼叫的工具、把資料夾帶進回應中帶走，或直接改寫紀錄。由於模型遵循自然語言指令，傳統的輸入驗證在這裡幾乎派不上用場。</p>
<p>2026 年的資安回應因此是架構性的：預設模型可能被操控，並透過限制「模型能做什麼、能看見什麼、能證明自己做過什麼」，讓操控變得沒有價值。下列對比可以清楚看出兩代思維的差異。</p>
<table class="article-table">
<thead><tr><th>面向</th><th>2024 年的做法</th><th>2026 年的做法</th></tr></thead>
<tbody>
<tr><td>授權單位</td><td>以使用者身分授權，模型繼承使用者全部權限</td><td>以工具為單位授權，每次呼叫都帶獨立的短期憑證</td></tr>
<tr><td>信任邊界</td><td>信任輸入內容已過濾乾淨</td><td>假設輸入不可信，只信任結構性約束</td></tr>
<tr><td>稽核方式</td><td>事後調閱應用日誌</td><td>每次工具呼叫即時寫入不可竄改的稽核軌跡</td></tr>
<tr><td>寫入動作</td><td>模型可直接寫回來源系統</td><td>寫入需經審批佇列，並保留完整回滾路徑</td></tr>
<tr><td>故障成本</td><td>單一整合失效</td><td>同一設定錯誤同時影響所有下游代理人</td></tr>
</tbody>
</table>
<p>實務上的結論很直接：如果你的 MCP 部署仍然把「模型輸出」當成可信輸入，那麼風險不在於某一個提示詞寫得好不好，而在於整體架構缺少約束。先把權限縮到最小、把每一次呼叫都留下證據，再談功能擴充。</p>
'''


def main():
    h = load(SLUG, "TW")
    before = cjk(h)
    assert ANCHOR in h, "anchor h2 not found"
    h = h.replace(ANCHOR, SEC + ANCHOR, 1)
    h = sync_toc(h)
    save(SLUG, "TW", h)
    print("TW CJK %d -> %d" % (before, cjk(load(SLUG, "TW"))))
    print("H2:", [t for _, t in h2s(h)])


if __name__ == "__main__":
    main()
