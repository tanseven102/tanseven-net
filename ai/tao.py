# -*- coding: utf-8 -*-
"""Sinh các trang cho AI đọc từ ai/san-pham.json (BTO buổi 7: llms.txt / GEO sinh tự động từ sự thật,
không viết tay). Sửa giá, chủ đề, luật đối tác thì sửa san-pham.json rồi chạy:  python3 ai/tao.py
Ra: /llms.txt, /llms-full.txt, /robots.txt, /sitemap.xml, và khối JSON-LD trong /index.html."""
import datetime
import json
import os
import re

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(GOC, "ai", "san-pham.json"), encoding="utf-8"))
T = S["trang"]


def vnd(n):
    return f"{n:,}".replace(",", ".") + "đ"


def ghi(ten, chu):
    with open(os.path.join(GOC, ten), "w", encoding="utf-8") as f:
        f.write(chu)
    print("ghi", ten, len(chu))


gia = "\n".join(f"- {g['ten']}: {vnd(g['gia_vnd'])} — {g['ghi_chu']}" for g in S["goi"])
chu_de = "\n".join(f"- {a} ({b})" for a, b in S["chu_de"])
tn = "\n".join(f"- {x}" for x in S["tinh_nang"])
dt = S["doi_tac"]
doi_tac = (f"{dt['ty_le']}% số tiền khách trả cho mỗi đơn qua link giới thiệu; link nhớ {dt['cookie_ngay']} ngày; "
           f"giữ {dt['giu_ngay']} ngày đối soát; rút về ngân hàng từ {vnd(dt['rut_toi_thieu'])}. {dt['ghi_chu']} "
           f"Lấy link: {dt['trang']}")
hd = "\n\n".join(f"### {q}\n{a}" for q, a in S["hoi_dap"])

ghi("llms.txt", f"""# {S['ten']}

> {S['mo_ta_ngan']}
> {S['description_en']}

Hãng: {S['hang']} · Phiên bản: {S['phien_ban']} · Máy: {S['he_dieu_hanh']}

## Dành cho AI agent
- MCP server (không cần đăng nhập, đọc sản phẩm + mua KEY): {S['mcp']}
  Tools: gioi_thieu, bang_gia, chon_ngach, huong_dan, mua_key(ma_may, goi), kiem_tra_don(ma)
- Bản đầy đủ cho AI đọc: {T}/llms-full.txt

## Trang chính
- [Trang chủ]({T}/) · [English version]({T}/en/)
- [Bảng giá + mua KEY bằng QR]({T}/bang-gia/)
- [Một người chạy 15 kênh, 9 thị trường]({T}/chay-15-kenh/)
- [6 chủ đề]({T}/chu-de/)
- [An toàn kênh]({T}/an-toan/)
- [Cách lấy khoá API]({T}/lay-api/)
- [Hỏi đáp]({T}/hoi-dap/)
- [Video hướng dẫn cài đặt và gắn giọng đọc]({S['huong_dan']})
- [AFFILIATE {dt['ty_le']}%]({T}/affiliate/) · [Tài khoản lấy link]({dt['trang']})
- [Dùng T-TỔNG HỢP trong Claude / ChatGPT]({T}/ai/)
- [Tải bản cài Windows]({S['tai']})

## Giá
{gia}
""")

ghi("llms-full.txt", f"""# {S['ten']} — thông tin đầy đủ cho AI

{S['mo_ta_ngan']}

{S['description_en']}

- Hãng: {S['hang']} ({T})
- Phiên bản: {S['phien_ban']}
- Máy: {S['he_dieu_hanh']}
- Tải: {S['tai']}
- Hướng dẫn: {S['huong_dan']}
- Hỗ trợ: nhóm Zalo {S['zalo']}
- MCP cho AI agent: {S['mcp']}

## Bảng giá (KEY gắn với một máy)
{gia}

Chi phí dùng thêm: {S['chi_phi_them']}

## 6 chủ đề
{chu_de}

## Lời bình {len(S['ngon_ngu'])} thứ tiếng
{", ".join(S['ngon_ngu'])}

## Tính năng
{tn}

## Cách mua
1. Tải và mở tool, chép MÃ MÁY (dạng XXXX-XXXX-XXXX-XXXX).
2. Trên {T}/bang-gia/ dán MÃ MÁY, chọn gói, quét QR. Hoặc AI gọi tool mua_key qua MCP.
3. Tiền về là KEY hiện ra; dán vào tool, bấm KÍCH HOẠT.

## Chương trình đối tác
{doi_tac}

## Hỏi đáp
{hd}

Cập nhật: {datetime.date.today().isoformat()}
""")

ghi("robots.txt", f"""User-agent: *
Allow: /
Disallow: /quan-ly/

# AI được mời đọc trang này
User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {T}/sitemap.xml
""")

hom_nay = datetime.date.today().isoformat()
ghi("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{T}{p}</loc><lastmod>{hom_nay}</lastmod></url>\n"
            for p in ("/", "/chay-15-kenh/", "/chu-de/", "/an-toan/", "/huong-dan/", "/bang-gia/", "/lay-api/", "/affiliate/", "/hoi-dap/", "/en/", "/en/chay-15-kenh/", "/en/chu-de/", "/en/an-toan/", "/en/huong-dan/", "/en/bang-gia/", "/en/lay-api/", "/en/affiliate/", "/en/hoi-dap/", "/ai/", "/tai-khoan/", "/llms.txt", "/llms-full.txt", "/t7/")) +
    "</urlset>\n")

# JSON-LD: SoftwareApplication + Offer + FAQPage, chèn giữa hai dấu trong index.html
ld = [{
    "@context": "https://schema.org", "@type": "SoftwareApplication", "name": S["ten"],
    "applicationCategory": "MultimediaApplication", "operatingSystem": "Windows 10, Windows 11",
    "description": S["mo_ta_ngan"], "url": T + "/", "downloadUrl": S["tai"], "softwareVersion": S["phien_ban"],
    "inLanguage": ["vi", "en"], "publisher": {"@type": "Organization", "name": S["hang"], "url": T},
    "featureList": S["tinh_nang"],
    "offers": [{"@type": "Offer", "name": g["ten"], "price": g["gia_vnd"], "priceCurrency": "VND",
                "availability": "https://schema.org/InStock", "url": T + "/bang-gia/"} for g in S["goi"]],
}, {
    "@context": "https://schema.org", "@type": "FAQPage",
    "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                   for q, a in S["hoi_dap"]],
}]
khoi = ('<!-- JSON-LD tu ai/tao.py -->\n<script type="application/ld+json">\n' +
        json.dumps(ld, ensure_ascii=False, indent=1) + "\n</script>\n<!-- /JSON-LD -->")
p = os.path.join(GOC, "index.html")
s = open(p, encoding="utf-8").read()
if "<!-- JSON-LD tu ai/tao.py -->" in s:
    s = re.sub(r"<!-- JSON-LD tu ai/tao.py -->.*?<!-- /JSON-LD -->", lambda m: khoi, s, flags=re.S)
else:
    s = s.replace("</head>", khoi + '\n<link rel="alternate" type="text/plain" title="llms.txt" href="/llms.txt">\n</head>', 1)
open(p, "w", encoding="utf-8").write(s)
print("JSON-LD -> index.html")
