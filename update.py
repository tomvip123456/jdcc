import json
import urllib.request

# ==========================================
# 请把你从网上找的接口源地址填在下面这个列表里
# 建议尽量填纯英文的链接，避免编码问题
# ==========================================
SOURCE_URLS = [
    "https://raw.githubusercontent.com/gaotianliuyun/gao/master/js.json",
    "http://ztha.top/TVBox/GYCK.json"
]

def fetch_json(url):
    """获取并解析 JSON 数据"""
    try:
        # 使用更完整的 User-Agent 伪装，防止部分源拦截
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"❌ 获取失败: {url}\n   错误信息: {e}")
        return None

def main():
    merged_sites = []
    seen_apis = set()  # 用于根据 API 地址去重

    for url in SOURCE_URLS:
        print(f"🔄 正在抓取: {url}")
        data = fetch_json(url)
        
        if not data:
            continue

        # 兼容单仓和多仓格式提取 sites
        sites = []
        if "sites" in data:
            sites = data["sites"]
        elif "urls" in data:
            # 如果抓到的是多仓，遍历里面的子仓提取 sites
            for u in data["urls"]:
                if "sites" in u:
                    sites.extend(u["sites"])

        # 去重合并
        for site in sites:
            api_url = site.get("api")
            # 确保 api 存在且没有重复
            if api_url and api_url not in seen_apis:
                seen_apis.add(api_url)
                merged_sites.append(site)
                
        print(f"   ✅ 当前源提取到 {len(sites)} 个接口，总计已合并 {len(merged_sites)} 个。")

    if len(merged_sites) == 0:
        print("⚠️ 警告：没有抓取到任何有效接口，请检查源地址是否失效。")
        return

    # 生成 TVBox 纯正的单仓格式 (关键修改点)
    result = {
        "name": "我的自动更新单仓",
        "version": "1.0",
        "description": "由 GitHub Actions 自动抓取、去重、合并生成",
        "sites": merged_sites
    }

    # 写入文件
    with open("dc.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"🎉 更新成功！共合并 {len(merged_sites)} 个有效接口。")

if __name__ == "__main__":
    main()
