// Dùng chung mọi trang (21/10/2026): link giới thiệu ?gt=MÃ nhớ 60 ngày, nút Tài khoản hiện tên, menu ☰.
(function(){
  var q = new URLSearchParams(location.search);
  try { if (/^[A-Za-z0-9]{6}$/.test(q.get("gt") || "")) localStorage.setItem("tth_gt", JSON.stringify({ m: q.get("gt").toUpperCase(), t: Date.now() })); } catch (e) {}
  try { var tk = JSON.parse(localStorage.getItem("tth_tk") || "null"); if (tk && tk.ten) document.getElementById("nut-tk").textContent = "👤 " + tk.ten.split(" ").pop(); } catch (e) {}
  var nut = document.getElementById("nut-menu"), tha = document.getElementById("tha");
  if (nut) nut.addEventListener("click", function(){ var mo = tha.hidden; tha.hidden = !mo; nut.setAttribute("aria-expanded", mo ? "true" : "false"); });
})();
function laGt(){ try { var o = JSON.parse(localStorage.getItem("tth_gt") || "null"), toi = JSON.parse(localStorage.getItem("tth_tk") || "null"); if (o && Date.now() - o.t < 60 * 864e5 && !(toi && toi.ma_gt === o.m)) return o.m; } catch (e) {} return ""; }
