# tanseven.net

Trang bán hàng của **T-Youtube** — công cụ dựng video YouTube tự động.

Repo này **chỉ chứa trang web đã dựng sẵn**, không có mã nguồn công cụ.
Mã nguồn nằm ở repo riêng.

Trang là một file HTML tự chứa: ảnh và video nhúng thẳng vào, không tham
chiếu ra ngoài. Dựng lại bằng `landing/dung.py` bên repo mã nguồn.

## Thư mục

| Đường dẫn | Là gì | Dựng lại bằng |
|---|---|---|
| `/` | Trang bán MMT.AI (đăng nhập Google, mua gói, tải bộ cài) | `landing/dung.py` bên repo mã nguồn |
| `/t-ai/` | Trang T-AI + trang kết nối | `landing/t-ai/` bên repo mã nguồn |
| `/t7/` | **Web thương hiệu Tân Seven (T7)** — giới thiệu công ty, hệ sinh thái 9 công cụ, người sáng lập | viết tay, sửa thẳng `t7/index.html` |
