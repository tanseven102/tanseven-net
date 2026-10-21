# -*- coding: utf-8 -*-
"""Dựng site T-TỔNG HỢP nhiều trang (anh Tân 21/10/2026: "mỗi thanh trên menu một trang").
Sửa nội dung ở _nguon/phan/*.html (từng khối), CSS ở phan/kieu.css, rồi chạy:
    python3 _nguon/tao_trang.py && python3 ai/tao.py
Ra: /index.html + /<trang>/index.html. Thư mục _nguon GitHub Pages không phát (dấu gạch dưới)."""
import os
import re

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(GOC, "_nguon", "phan")
T = "https://tanseven.net"


def doc(ten, nn="vi"):
    if nn == "en" and os.path.exists(os.path.join(P + "_en", ten)):
        return open(os.path.join(P + "_en", ten), encoding="utf-8").read()
    return open(os.path.join(P, ten), encoding="utf-8").read()


# (đường dẫn, tên menu, <title>, mô tả, các khối)
TRANG = [
    ("", None, "T-TỔNG HỢP — Một người chạy 15 kênh, lời bình 9 thứ tiếng | Tân Seven",
     "T-TỔNG HỢP: tool Windows làm video tổng hợp tự động, 6 chủ đề, lời bình 9 thứ tiếng, tắt tiếng gốc tránh nhạc bản quyền. Một người chạy được nhiều kênh nhiều nước.",
     ["hero", "so-lieu", "kham-pha", "chot"]),
    ("chay-15-kenh", "Chạy 15 kênh", "Một người chạy 15 kênh, 9 thị trường | T-TỔNG HỢP",
     "Ví dụ một người chạy 15 kênh tổng hợp ở 9 thị trường với T-TỔNG HỢP: mỗi kênh một ngách, một thứ tiếng, mỗi kênh một lượt bấm.",
     ["10-kenh", "ngon-ngu", "cach-lam", "dieu-huong"]),
    ("chu-de", "6 chủ đề", "6 chủ đề video tổng hợp | T-TỔNG HỢP",
     "Tai nạn ô tô, thiên tai, máy bay & tàu biển, camera an ninh, động vật hoang dã có lời bình, và hài hước meme + tiếng động.",
     ["chu-de", "dieu-huong"]),
    ("an-toan", "An toàn", "An toàn cho kênh: tắt tiếng gốc, che mờ, chặn nguồn claim | T-TỔNG HỢP",
     "T-TỔNG HỢP lọc nhiều lớp trước khi ghép video: tắt tiếng gốc, che mờ cảnh nặng, chặn phim & CGI, né nguồn của hãng hay claim, xoá logo, bỏ cảnh tối.",
     ["an-toan", "dieu-huong"]),
    ("huong-dan", "Hướng dẫn", "Video hướng dẫn T-TỔNG HỢP — cài đặt, gắn KEY, gắn giọng đọc | Tân Seven",
     "VIDEO 1: tải tool, mua và gắn KEY, dán khoá OpenAI, ra video đầu tiên. VIDEO 2: gắn API giọng đọc ở tanseven.com. Quay trên tool thật.",
     ["video", "may-can", "dieu-huong"]),
    ("bang-gia", "Bảng giá", "Bảng giá & mua KEY T-TỔNG HỢP | Tân Seven",
     "Gói 1 tháng 1.000.000đ, vĩnh viễn 5.000.000đ. Quét QR chuyển khoản, KEY tự hiện trên trang sau vài giây.",
     ["gia", "mua"]),
    ("lay-api", "Lấy API", "Cách lấy khoá API: OpenAI, T-GIỌNG ĐỌC, GIPHY | T-TỔNG HỢP",
     "Từng bước lấy khoá OpenAI, khoá T-GIỌNG ĐỌC ở tanseven.com và khoá GIPHY, rồi dán vào nút Khoá API trong tool.",
     ["api", "dieu-huong"]),
    ("affiliate", "AFFILIATE", "AFFILIATE 20% — giới thiệu T-TỔNG HỢP nhận hoa hồng | Tân Seven",
     "Đăng nhập Google lấy link giới thiệu. Ai mua qua link, nhận 20% mỗi đơn và mỗi lần gia hạn. Rút về ngân hàng từ 200.000đ.",
     ["doi-tac", "dieu-huong"]),
    ("hoi-dap", "Hỏi đáp", "Hỏi đáp T-TỔNG HỢP | Tân Seven",
     "Câu hỏi hay gặp về T-TỔNG HỢP: dùng có khó không, chi phí, KEY, đổi máy, bản quyền, chạy nhiều kênh, affiliate.",
     ["hoi-dap", "dieu-huong"]),
]
# Bản tiếng Anh (anh Tân 21/10/2026): cùng khối, chữ ở phan_en/, đường dẫn /en/<trang>/
EN = {
    "": (None, "T-TONGHOP — One person, 15 YouTube channels, narration in 9 languages | Tân Seven",
         "T-TONGHOP: Windows app that makes YouTube compilation videos automatically. 6 topics, AI narration in 9 languages, mute source audio to avoid music claims. Run many channels in many countries."),
    "chay-15-kenh": ("Run 15 channels", "One person, 15 channels, 9 markets | T-TONGHOP",
                     "How one person runs 15 compilation channels in 9 markets with T-TONGHOP: one niche and one language per channel, one button press each."),
    "chu-de": ("6 topics", "6 compilation video topics | T-TONGHOP",
               "Car crashes, natural disasters, planes & ships, security cameras, wildlife with narration, plus funny memes + sound effects."),
    "an-toan": ("Safety", "Channel safety: mute source audio, blur, block claim sources | T-TONGHOP",
                "T-TONGHOP filters in layers before editing: mute source audio, blur graphic scenes, block movies & CGI, skip claim-happy agencies, remove logos, drop dark scenes."),
    "huong-dan": ("Guides", "Video guides — install, activate, connect the voice | T-TONGHOP",
                  "VIDEO 1: download, buy and activate a KEY, paste the OpenAI key, make your first video. VIDEO 2: connect the voice API at tanseven.com."),
    "bang-gia": ("Pricing", "Pricing & buy a KEY | T-TONGHOP",
                 "1-month plan 1,000,000 VND, lifetime 5,000,000 VND. Scan the QR, your KEY appears on the page within seconds."),
    "lay-api": ("API keys", "How to get API keys: OpenAI, T-GIỌNG ĐỌC, GIPHY | T-TONGHOP",
                "Step by step: OpenAI key, T-GIỌNG ĐỌC voice key from tanseven.com, GIPHY key, then paste them into the app."),
    "affiliate": ("AFFILIATE", "AFFILIATE 20% — refer T-TONGHOP and earn commission | Tân Seven",
                  "Sign in with Google for a referral link. Earn 20% of every order and every renewal. Withdraw to a bank from 200,000 VND."),
    "hoi-dap": ("FAQ", "FAQ | T-TONGHOP", "Common questions about T-TONGHOP: ease of use, costs, KEY, changing PC, copyright, many channels, affiliate."),
}
MUA_EN = [('"1 tháng"', '"1 month"'), ('"Vĩnh viễn"', '"Lifetime"'), ('"Đã áp mã "', '"Code "'), ('": giảm "', '" applied: "'),
          ('"Lỗi máy chủ"', '"Server error"'), ('"✓ Mã "', '"✓ Code "'), ('" giảm "', '" gives "'),
          ('"%. Giá mới đã hiện ở trên, thanh toán ở mục Cách mua."', '"% off. New prices shown above; pay below."'),
          ('"MÃ MÁY chưa đúng. Mở tool, bấm Chép rồi dán vào đây."', '"Invalid MACHINE CODE. Open the app, click Copy and paste it here."'),
          ("Mã QR chuyển khoản ", "Payment QR "), ('"Chưa tạo được mã thanh toán ("', '"Could not create payment ("'),
          ('"). Thử lại, hoặc vào nhóm Zalo hỗ trợ."', '"). Try again or ask in the Zalo group."'),
          ('"✓ Đã chép KEY"', '"✓ KEY copied"'), ('"Bôi đen KEY để chép"', '"Select the KEY to copy"'),
          ("""<div class="trong">Đơn ' + d.ma + ' đang chờ tiền. Quét lại mã: bấm "Đổi mã máy / gói" và tạo lại.</div>""",
           """<div class="trong">Order ' + d.ma + ' is waiting for payment. For a new QR, click "Change machine code / plan" and create it again.</div>""")]
MENU = [t for t in TRANG if t[1] and t[0] != "hoi-dap"]

# Link neo cũ (khi còn một trang) → trang mới
NEO = {"#mua": "/bang-gia/#mua", "#gia": "/bang-gia/", "#api": "/lay-api/", "#video": "/huong-dan/",
       "#video-2": "/huong-dan/#video-2", "#doi-tac": "/affiliate/", "#hoi-dap": "/hoi-dap/",
       "#10-kenh": "/chay-15-kenh/", "#chu-de": "/chu-de/", "#an-toan": "/an-toan/",
       "#cach-lam": "/chay-15-kenh/#cach-lam", "#ngon-ngu": "/chay-15-kenh/#ngon-ngu", "#tinh-nang": "/chay-15-kenh/"}


def sua_link(html, duong, nn="vi"):
    goc = "/en" if nn == "en" else ""
    def thay(m):
        attr, v = m.group(1), m.group(2)
        if v.startswith("#"):
            dich = NEO.get(v)
            dich = goc + dich if dich else dich
            if not dich or dich.split("#")[0] == f"{goc}/{duong}/":   # neo trong chính trang này thì giữ
                return m.group(0)
            return f'{attr}="{dich}"'
        if re.match(r"(https?:|/|mailto:|data:|tel:)", v):
            return m.group(0)
        return f'{attr}="/{v}"'
    return re.sub(r'\b(href|src|poster)="([^"]*)"', thay, html)


def menu(duong, nn="vi"):
    goc = "/en" if nn == "en" else ""
    ten_menu = (lambda d, ten: EN[d][0]) if nn == "en" else (lambda d, ten: ten)
    lk = "\n".join(f'      <a class="lk{" on" if d == duong else ""}" href="{goc}/{d}/">{ten_menu(d, ten)}</a>' for d, ten, *_ in MENU)
    tha = "\n".join(f'    <a class="{"on" if d == duong else ""}" href="{goc}/{d}/">{ten_menu(d, ten)}</a>' for d, ten, *_ in MENU)
    sang = ("/" + (duong + "/" if duong else "")) if nn == "en" else ("/en/" + (duong + "/" if duong else ""))
    doi = (f'<a class="doi-nn" href="{sang}" hreflang="vi" title="Tiếng Việt"><b>EN</b><span>VI</span></a>' if nn == "en"
           else f'<a class="doi-nn" href="{sang}" hreflang="en" title="English"><b>VI</b><span>EN</span></a>')
    T_ = {"tk": "Account", "mua": "Buy now", "hd": "FAQ", "ai": "Use in Claude / ChatGPT"} if nn == "en" else \
         {"tk": "Tài khoản", "mua": "Mua ngay", "hd": "Hỏi đáp", "ai": "Dùng trong Claude / ChatGPT"}
    return f'''<header class="dau">
  <div class="boc">
    <a class="logo" href="{goc}/"><img src="/t7/logo.svg" alt="" width="30" height="30"><span>T-<b>{"TONGHOP" if nn == "en" else "TỔNG HỢP"}</b></span></a>
    <nav>
{lk}
      {doi}
      <a class="nut nut-vien" href="/tai-khoan/" id="nut-tk">{T_["tk"]}</a>
      <a class="nut nut-do" href="{goc}/bang-gia/">{T_["mua"]}</a>
      <button type="button" class="nut-menu" id="nut-menu" aria-label="{"Open menu" if nn == "en" else "Mở menu"}" aria-expanded="false">☰</button>
    </nav>
  </div>
  <div class="tha" id="tha" hidden>
{tha}
    <a href="{goc}/hoi-dap/">{T_["hd"]}</a>
    <a href="/ai/">{T_["ai"]}</a>
    <a href="/tai-khoan/">{T_["tk"]}</a>
  </div>
</header>'''


CHUYEN_CU = """<script>
// Link cũ (tool, Zalo, MCP) trỏ vào trang chủ kèm ?ma= / #mua / #api… → sang đúng trang mới
(function(){var h=location.hash,q=location.search,m=%s;
var p=/[?&](ma|giam|goi)=/.test(q)?"/bang-gia/"+(h||"#mua"):m[h];
if(p){var a=p.split("#");location.replace(a[0]+q+(a[1]?"#"+a[1]:""));}})();
</script>""" % str(NEO).replace("'", '"')

CHUONG_JS = """<script>
document.querySelectorAll(".chuong a").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();var v=document.getElementById("vd1");v.currentTime=+a.dataset.t;v.play();v.scrollIntoView({behavior:"smooth",block:"center"});});});
</script>"""


def dung(duong, ten, tieu_de, mo_ta, khoi, nn="vi"):
    goc = "/en" if nn == "en" else ""
    if nn == "en":
        tieu_de, mo_ta = EN[duong][1], EN[duong][2]
    than = "\n".join(doc(k + ".html", nn) for k in khoi)
    if duong:   # trang con: tiêu đề lớn đầu tiên là h1
        than = re.sub(r"<h2>(.*?)</h2>", r'<h1 class="tieu">\1</h1>', than, count=1, flags=re.S)
    than = sua_link(than, duong, nn)
    duoi = duong + "/" if duong else ""
    url = f"{T}{goc}/{duoi}"
    anh = f"{T}/huong-dan/bia.jpg"
    og_video = ('\n<meta property="og:video" content="https://tanseven.net/huong-dan/t-tong-hop-huong-dan.mp4">'
                '\n<meta property="og:video:type" content="video/mp4">') if duong == "huong-dan" else ""
    js = "<script>\n" + doc("chung.js") + "</script>"
    if duong == "bang-gia":
        mua = doc("mua.js")
        if nn == "en":
            for a, b in MUA_EN:
                assert a in mua, a
                mua = mua.replace(a, b)
        js += "\n<script>\n" + mua + "</script>"
    if duong == "huong-dan":
        js += "\n" + CHUONG_JS
    html = f'''<!doctype html>
<html lang="{nn}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{tieu_de}</title>
<meta name="description" content="{mo_ta}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="vi" href="{T}/{duoi}">
<link rel="alternate" hreflang="en" href="{T}/en/{duoi}">
<link rel="alternate" hreflang="x-default" href="{T}/{duoi}">
<meta property="og:type" content="{'video.other' if duong == 'huong-dan' else 'website'}">
<meta property="og:locale" content="{'en_US' if nn == 'en' else 'vi_VN'}">
<meta property="og:title" content="{tieu_de.split(' | ')[0]}">
<meta property="og:description" content="{mo_ta}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{anh}">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="720">{og_video}
<link rel="icon" href="/t7/logo.svg">
<link rel="alternate" type="text/plain" title="llms.txt" href="/llms.txt">
{CHUYEN_CU if not duong and nn == "vi" else ""}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>
{doc("kieu.css")}</style>
</head>
<body class="{'trang-con' if duong else 'trang-chu'}">

{menu(duong, nn)}

<main>
{than}
</main>

{sua_link(doc("chan.html", nn), duong, nn)}
{js}
</body>
</html>
'''
    thu_muc = os.path.join(GOC, "en") if nn == "en" else GOC
    ra = os.path.join(thu_muc, duong, "index.html") if duong else os.path.join(thu_muc, "index.html")
    os.makedirs(os.path.dirname(ra), exist_ok=True)
    open(ra, "w", encoding="utf-8").write(html)
    print("ghi", os.path.relpath(ra, GOC), len(html))


for t in TRANG:
    dung(*t)
    dung(*t, nn="en")
