import feedparser
import json
import re
from datetime import datetime

# 示例RSS源（可替换）
RSS_FEEDS = [
    'https://hnrss.org/frontpage',
    'https://www.ruanyifeng.com/blog/atom.xml',
]

KEYWORDS = ['AI', 'LLM', 'GPT', 'agent', 'MCP', 'Tailwind']

def fetch_entries(feed_url, limit=5):
    feed = feedparser.parse(feed_url)
    entries = []
    for entry in feed.entries[:limit]:
        title = entry.get('title', '')
        link = entry.get('link', '')
        summary = entry.get('summary', '')[:200]
        entries.append({'title': title, 'link': link, 'summary': summary})
    return entries

def filter_hot(entries):
    hot = []
    for e in entries:
        text = e['title'] + ' ' + e['summary']
        if any(k.lower() in text.lower() for k in KEYWORDS):
            e['hits'] = len([k for k in KEYWORDS if k.lower() in text.lower()])
            hot.append(e)
    hot.sort(key=lambda x: x['hits'], reverse=True)
    return hot[:3]

def generate_daily_report(all_hot):
    lines = [f'# AI热点日报 - {datetime.now().strftime("%Y-%m-%d")}', '']
    for i, item in enumerate(all_hot, 1):
        lines.append(f'{i}. **{item["title"]}** (热度{hits}关键词)')
        lines.append(f'   {item["link"]}')
        lines.append(f'   {item["summary"]}')
        lines.append('')
    return '\n'.join(lines)

def main():
    all_hot = []
    for feed in RSS_FEEDS:
        entries = fetch_entries(feed)
        hot = filter_hot(entries)
        all_hot.extend(hot)
    report = generate_daily_report(all_hot)
    with open('daily_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print(f'已生成报告，共{len(all_hot)}条热点')
    print(report)

if __name__ == '__main__':
    main()
