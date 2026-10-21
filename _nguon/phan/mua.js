var API = "https://api.tanseven.net";
var GOI = { thang: { tien: 1000000, ten: "1 tháng" }, vv: { tien: 5000000, ten: "Vĩnh viễn" } };
var goi = "thang", hen = null, maGiam = "", phanTram = 0;
function $(id){ return document.getElementById(id); }
function vnd(n){ return n.toLocaleString("vi-VN") + "đ"; }
function giaSau(g){ return Math.floor(GOI[g].tien * (100 - phanTram) / 100); }
function chonGoi(g){
  goi = g;
  document.querySelectorAll("[data-chon]").forEach(function(b){ b.classList.toggle("on", b.dataset.chon === g); });
  $("tien-nut").textContent = vnd(giaSau(g));
}
function veGia(){
  document.querySelectorAll("[data-gia]").forEach(function(el){
    var g = el.dataset.gia;
    el.innerHTML = phanTram ? "<s>" + vnd(GOI[g].tien) + "</s>" + vnd(giaSau(g)) : vnd(GOI[g].tien);
  });
  $("da-giam").hidden = !phanTram;
  $("da-giam").textContent = phanTram ? "Đã áp mã " + maGiam + ": giảm " + phanTram + "%" : "";
  chonGoi(goi);
}
$("nut-giam").addEventListener("click", function(){
  var ma = $("o-giam").value.trim().toUpperCase(), bao = $("bao-giam");
  if (!ma) { maGiam = ""; phanTram = 0; veGia(); bao.textContent = ""; return; }
  var nut = this; nut.disabled = true;
  fetch(API + "/api/tth/ma-giam/" + encodeURIComponent(ma) + "?ma_may=" + encodeURIComponent(chuanMa($("o-ma").value)))
    .then(function(r){ return r.json().then(function(d){ if (!r.ok) throw new Error(d.detail || "Lỗi máy chủ"); return d; }); })
    .then(function(d){ maGiam = d.ma; phanTram = d.phan_tram; bao.className = "bao-giam ok"; bao.textContent = "✓ Mã " + d.ma + " giảm " + d.phan_tram + "%. Giá mới đã hiện ở trên, thanh toán ở mục Cách mua."; veGia(); })
    .catch(function(e){ maGiam = ""; phanTram = 0; bao.className = "bao-giam loi"; bao.textContent = e.message; veGia(); })
    .finally(function(){ nut.disabled = false; });
});
$("o-giam").addEventListener("keydown", function(e){ if (e.key === "Enter") $("nut-giam").click(); });
function hien(khoi){ ["b-nhap","b-qr","b-key"].forEach(function(k){ $(k).hidden = (k !== khoi); }); }
function chuanMa(v){
  var c = (v || "").toUpperCase().replace(/[^0-9A-F]/g, "").slice(0, 16);
  return c.replace(/(.{4})(?=.)/g, "$1-");
}
$("o-ma").addEventListener("input", function(e){ e.target.value = chuanMa(e.target.value); $("bao-nhap").textContent = ""; });
document.querySelectorAll("[data-chon]").forEach(function(b){ b.addEventListener("click", function(){ if (!$("b-nhap").hidden) chonGoi(b.dataset.chon); }); });
document.querySelectorAll("[data-goi]").forEach(function(a){ a.addEventListener("click", function(){ if (!$("b-nhap").hidden) chonGoi(a.dataset.goi); }); });
$("nut-tao").addEventListener("click", function(){
  var ma = chuanMa($("o-ma").value);
  if (!/^[0-9A-F]{4}(-[0-9A-F]{4}){3}$/.test(ma)) { $("bao-nhap").textContent = "MÃ MÁY chưa đúng. Mở tool, bấm Chép rồi dán vào đây."; return; }
  var nut = this; nut.disabled = true; nut.style.opacity = .6;
  fetch(API + "/api/tth/don", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ma_may: ma, goi: goi, lien_he: $("o-lh").value.trim(), ma_giam: maGiam, gt: laGt() }) })
    .then(function(r){ return r.json().then(function(d){ if (!r.ok) throw new Error(d.detail || "Lỗi máy chủ"); return d; }); })
    .then(function(d){
      $("qr").innerHTML = '<img alt="Mã QR chuyển khoản ' + vnd(d.so_tien) + '" src="' + d.qr + '">';
      $("ck-nh").textContent = d.ngan_hang; $("ck-stk").textContent = d.stk; $("ck-chu").textContent = d.chu_tk || "—";
      $("ck-tien").textContent = vnd(d.so_tien); $("ck-nd").textContent = d.ma; $("ck-may").textContent = d.ma_may;
      try { localStorage.setItem("tth_don", d.ma); } catch (e) {}
      hien("b-qr"); hoi(d.ma);
    })
    .catch(function(e){ $("bao-nhap").textContent = "Chưa tạo được mã thanh toán (" + e.message + "). Thử lại, hoặc vào nhóm Zalo hỗ trợ."; })
    .finally(function(){ nut.disabled = false; nut.style.opacity = 1; });
});
function hoi(ma){
  clearTimeout(hen);
  fetch(API + "/api/tth/don/" + encodeURIComponent(ma)).then(function(r){ return r.ok ? r.json() : null; }).then(function(d){
    if (d && d.trang_thai === "da_tra" && d.key) {
      $("o-key").textContent = d.key; $("key-goi").textContent = GOI[d.goi] ? GOI[d.goi].ten : d.goi;
      hien("b-key"); return;
    }
    if (d) hen = setTimeout(function(){ hoi(ma); }, 4000);
  }).catch(function(){ hen = setTimeout(function(){ hoi(ma); }, 8000); });
}
$("nut-lai").addEventListener("click", function(){ clearTimeout(hen); try { localStorage.removeItem("tth_don"); } catch (e) {} hien("b-nhap"); });
$("nut-chep-key").addEventListener("click", function(){
  var k = $("o-key").textContent, nut = this;
  (navigator.clipboard ? navigator.clipboard.writeText(k) : Promise.reject()).then(function(){ nut.textContent = "✓ Đã chép KEY"; }, function(){ nut.textContent = "Bôi đen KEY để chép"; });
});
// tool mở trang kèm ?ma=<MÃ MÁY>; khách tải lại trang giữa chừng thì hỏi tiếp đơn cũ
var q = new URLSearchParams(location.search);
if (q.get("ma")) $("o-ma").value = chuanMa(q.get("ma"));
if (q.get("giam")) { $("o-giam").value = q.get("giam"); $("nut-giam").click(); }
if (q.get("goi") && GOI[q.get("goi")]) chonGoi(q.get("goi"));
try { var cu = localStorage.getItem("tth_don"); if (cu) fetch(API + "/api/tth/don/" + cu).then(function(r){ return r.ok ? r.json() : null; }).then(function(d){
  if (!d) return;
  if (d.trang_thai === "da_tra") { $("o-key").textContent = d.key; $("key-goi").textContent = GOI[d.goi].ten; hien("b-key"); }
  else { $("ck-nd").textContent = d.ma; $("ck-may").textContent = d.ma_may; $("ck-tien").textContent = vnd(d.so_tien); $("qr").innerHTML = '<div class="trong">Đơn ' + d.ma + ' đang chờ tiền. Quét lại mã: bấm "Đổi mã máy / gói" và tạo lại.</div>'; hien("b-qr"); hoi(d.ma); }
}).catch(function(){}); } catch (e) {}
