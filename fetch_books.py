import requests
import xml.etree.ElementTree as ET

def search_books(from_year, to_year, max_results=30):
    base_url = "https://ndlsearch.ndl.go.jp/api/opensearch"

    params = {
        "any": "小説",
        "ndc": 9,    # 文学
        "from": str(from_year),
        "until": str(to_year),
        "cnt": min(max_results, 30),   # 最大件数
    }

    response = requests.get(base_url, params=params, timeout=15)

    #print(response.text)

    root = ET.fromstring(response.content)
    
    ns = {
        "dc": "http://purl.org/dc/elements/1.1/",
        "dcterms": "http://purl.org/dc/terms/",
        "opensearch": "http://a9.com/-/spec/opensearchrss/1.0/"
    }

    books = []
    for item in root.findall(".//item"):
       # ページ数取得
        extent = item.findtext("dc:extent", namespaces=ns)
        page_count = None
        if extent:
            import re
            match = re.search(r'(\d+)', extent)
            if match:
                page_count = int(match.group(1))

        book = {
            "issued": item.findtext("dcterms:issued", namespaces=ns),   # 出版年
            "page_count": page_count,    # ページ数
            "title": item.findtext("title"),    # タイトル
            #"creator": item.findtext("dc:creator", namespaces=ns),
            #"publisher": item.findtext("dc:publisher", namespaces=ns),
            #"isbn": item.findtext("dc:identifier", namespaces=ns),
            #"link": item.findtext("link")
        }
        books.append(book)
    
    return books

# 使用例
books = search_books(from_year=2020, to_year=2020, max_results=30)
print(f"取得した冊数: {len(books)}")
for book in books:
    print(book)
