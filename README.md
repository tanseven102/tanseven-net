# tanseven.net

Trang bán hàng của **T-TỔNG HỢP** — tool Windows dựng video tổng hợp hài tự động (từ 17/10/2026; trước đó gốc là trang bán MMT.AI, xem lịch sử git).

Repo này **chỉ chứa trang web đã dựng sẵn**, không có mã nguồn công cụ.
Mã nguồn nằm ở repo riêng.

Trang là một file HTML tự chứa: ảnh và video nhúng thẳng vào, không tham
chiếu ra ngoài. Dựng lại bằng `landing/dung.py` bên repo mã nguồn.

## Thư mục

| Đường dẫn | Là gì | Dựng lại bằng |
|---|---|---|
| `/` | **Sale page T-TỔNG HỢP** (gói 1 tháng 1tr, vĩnh viễn 5tr). Mua: khách nhập MÃ MÁY → `api.tanseven.net/api/tth/don` ra QR SePay → tiền về tự hiện KEY. Nhóm Zalo hỗ trợ | viết tay, sửa thẳng `index.html` |
| `/t-ai/` | Trang T-AI + trang kết nối | `landing/t-ai/` bên repo mã nguồn |
| `/quan-ly/` | Trang quản lý khách T-TỔNG HỢP (noindex, cần mã quản lý; gọi `api.tanseven.net/api/tth/quan-ly`) | viết tay |
| `/t7/` | **Web thương hiệu Tân Seven (T7)** — giới thiệu công ty, hệ sinh thái 9 công cụ, người sáng lập | viết tay, sửa thẳng `t7/index.html` |
