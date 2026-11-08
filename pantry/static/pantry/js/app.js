// 1. Live search: filter the visible list while typing (no page reload)
const searchBox = document.getElementById("live-search");
const rows = document.querySelectorAll("#item-list .item");
const noMatch = document.getElementById("no-live-match");

if (searchBox) {
  searchBox.addEventListener("input", () => {
    const term = searchBox.value.trim().toLowerCase();
    let visible = 0;
    rows.forEach((row) => {
      const match = row.dataset.name.includes(term);
      row.classList.toggle("d-none", !match);
      if (match) visible++;
    });
    if (noMatch) noMatch.classList.toggle("d-none", visible !== 0 || rows.length === 0);
  });
}

// 2. Ask before tossing an item
document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!window.confirm(form.dataset.confirm)) event.preventDefault();
  });
});

// 3. Hide flash messages after a few seconds
const flash = document.getElementById("flash");
if (flash) {
  setTimeout(() => {
    flash.style.transition = "opacity 0.4s";
    flash.style.opacity = "0";
    setTimeout(() => flash.remove(), 400);
  }, 3500);
}
