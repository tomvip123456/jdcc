import json
import urllib.request

# ==========================================
# 请把你从网上找的接口源地址填在下面这个列表里
# 可以填多个，用英文逗号隔开
# ==========================================
SOURCE_URLS = [
    
    "https://raw.githubusercontent.com/Lightconer/tvbox-ysc-config/main/output/单仓聚合.json",
    "https://raw.githubusercontent.com/FongMi/TV/refs/heads/release/json/config.json"

]

def fetch_json(url):
    try:
        # 伪装成浏览器请求，防止被拦截
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"获取失败: {url}, 错误: {e}")
        return None

def main():
    merged_sites = []
    seen_urls = set() # 用于去重

    for url in SOURCE_URLS:
        print(f"正在抓取: {url}")
        data = fetch_json(url)
        if data:
            # 兼容不同格式的源
            sites = []
            if "sites" in data:
                sites = data["sites"]
            elif "urls" in data:
                for u in data["urls"]:
                    if "sites" in u:
                        sites.extend(u["sites"])

            for site in sites:
                # 如果接口地址存在且不重复
                if site.get("api") and site["api"] not in seen_urls:
                    seen_urls.add(site["api"])
                    merged_sites.append(site)
    
    if len(merged_sites) == 0:
        print("警告：没有抓取到任何有效接口，请检查源地址是否失效。")
        return

    # 按照你原来的 dc.json 格式生成文件
    result = {
        "name": "我的多仓聚合",
        "version": "1.0",
        "description": "自动抓取并合并",
        "urls": [
            {
                "name": "多仓合并源",
                "url": "", 
                "sites": merged_sites
            }
        ]
    }

    with open("dc.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"更新成功！共合并 {len(merged_sites)} 个接口。")

if __name__ == "__main__":
    main()
