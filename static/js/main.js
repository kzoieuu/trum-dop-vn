/* ════════════════════════════════════════════════════════════
   TRÙM ĐỚP VN — main.js (JS dùng chung)
════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

    // ── Nút hamburger menu (mobile) ──────────────────────
    const toggle = document.querySelector('.navbar-toggle');
    const menu   = document.querySelector('.navbar-menu');
    if (toggle && menu) {
        toggle.addEventListener('click', function () {
            const isOpen = menu.classList.toggle('open');
            toggle.setAttribute('aria-expanded', isOpen);
            toggle.textContent = isOpen ? '✕' : '☰';
        });
    }

    // ── Nút lọc nhanh (pills) ────────────────────────────
    const pills = document.querySelectorAll('.quick-filters .pill');
    pills.forEach(pill => {
        pill.addEventListener('click', function () {
            pills.forEach(p => p.classList.remove('active'));
            this.classList.add('active');
            // TODO (F4): lọc danh sách quán theo loại món
        });
    });

    // ── Tabs Xem nhiều nhất / Gần đây ───────────────────
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            tabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            // TODO (F4): sắp xếp lại danh sách theo tab
        });
    });

    // ── Smooth scroll cho các anchor link ───────────────
    document.querySelectorAll('a[href*="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            // Chỉ xử lý nếu là cùng trang (href bắt đầu bằng # hoặc là trang chủ)
            const hash = href.includes('#') ? '#' + href.split('#')[1] : null;
            if (!hash) return;
            const target = document.querySelector(hash);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

});

// ── User dropdown menu ───────────────────────────────────
const userMenuBtn  = document.getElementById('user-menu-btn');
const userDropdown = document.getElementById('user-dropdown');
if (userMenuBtn && userDropdown) {
    userMenuBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        userDropdown.classList.toggle('open');
    });
    document.addEventListener('click', function () {
        userDropdown.classList.remove('open');
    });
}

// ── Pref chips (toggle active class khi tick checkbox) ───
document.querySelectorAll('.pref-chip').forEach(chip => {
    const cb = chip.querySelector('input[type="checkbox"]');
    if (!cb) return;
    // Trạng thái ban đầu
    if (cb.checked) chip.classList.add('pref-chip--active');
    chip.addEventListener('click', function () {
        // Đợi trình duyệt cập nhật checked rồi mới đổi class
        setTimeout(() => {
            chip.classList.toggle('pref-chip--active', cb.checked);
        }, 0);
    });
});
