// 前台逻辑 —— 从后端 API 动态加载（分类/游戏无限扩展）
const API = ""; // 同源，空即可
let ALL_GAMES = [];
let CATS = [];
let SETTINGS = {};
let currentCat = null;
let searchTimer = null;

const $ = (s) => document.querySelector(s);

// ---- 工具：格式化数字 ----
function fmt(n){ return Number(n||0).toLocaleString("zh-CN"); }

// ---- 渲染侧边分类栏（无限分类）----
function renderSidebar() {
  const el = $("#sidebar");
  el.innerHTML = CATS.map(c => `
    <div class="cat-item ${c === currentCat ? "active" : ""}" data-cat="${c}">
      <span class="cat-dot"></span>${c}
    </div>
  `).join("");
  el.querySelectorAll(".cat-item").forEach(item => {
    item.onclick = () => { currentCat = item.dataset.cat; renderSidebar(); renderList(); };
  });
}

// ---- 渲染游戏列表（无限游戏，瀑布展示）----
function renderList() {
  const kw = ($("#searchInput").value || "").trim().toLowerCase();
  let list = ALL_GAMES.filter(g => !currentCat || g.cat === currentCat);
  if (kw) list = list.filter(g =>
    g.title.toLowerCase().includes(kw) ||
    (g.tags||[]).some(t => t.toLowerCase().includes(kw))
  );
  const el = $("#list");
  if (!list.length) {
    el.innerHTML = `<div class="empty">📭 这里还没有游戏，去后台添加一个吧～</div>`;
    return;
  }
  el.innerHTML = list.map(g => `
    <div class="game-card" data-id="${g.id}">
      <div class="game-icon" style="background:${iconBg(g.icon)}">${g.icon||"🎮"}</div>
      <div class="game-info">
        <div class="game-title">${g.title}</div>
        <div class="game-tags">${(g.tags||[]).map(t=>`<span>${t}</span>`).join("")}</div>
        <div class="game-meta">
          <span>📅 ${g.date||""}</span>
          <span>📦 ${g.size||"-"}</span>
          <span>▶ ${fmt(g.plays||0)}</span>
        </div>
      </div>
      <button class="view-btn" data-id="${g.id}">查看</button>
    </div>
  `).join("");
  el.querySelectorAll(".view-btn, .game-card").forEach(node => {
    node.onclick = (e) => {
      const id = node.dataset.id || node.closest(".game-card").dataset.id;
      const game = ALL_GAMES.find(x => x.id === id);
      if (game) openGame(game);
    };
  });
}

// 图标渐变背景（按标题哈希固定颜色）
function iconBg(icon){
  const colors = ["#FF6B6B","#FFA94D","#FFD93D","#6BCB77","#4D96FF","#9B59B6","#FF6B9D","#00C2A8"];
  let h = 0; for (let c of (icon||"")) h += c.charCodeAt(0);
  return `linear-gradient(135deg, ${colors[h%colors.length]}, ${colors[(h+3)%colors.length]})`;
}

// ---- 打开游戏（上报点击 + 跳转）----
function openGame(game){
  fetch(API+"/api/game/click", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({id: game.id})}).catch(()=>{});
  if (game.link && game.link !== "#") window.open(game.link, "_blank", "noopener");
  else alert(`【${game.title}】\n${game.desc||"暂无描述"}\n\n（演示模式：请到后台为游戏填写真实下载/跳转链接）`);
}

// ---- IP 检测弹窗 ----
function bindIp(){
  const mask = $("#ipMask"), close = $("#ipClose");
  $("#ipBtn").onclick = () => {
    mask.classList.add("show");
    $("#ipAddr").textContent = "127.0.0.1（演示）";
    $("#ipLoc").textContent = "本地网络（演示数据）";
  };
  close.onclick = () => mask.classList.remove("show");
  mask.onclick = (e) => { if (e.target === mask) mask.classList.remove("show"); };
}

// ---- 加载全量数据 ----
async function loadData(){
  try {
    const res = await fetch(API + "/api/data");
    const data = await res.json();
    CATS = data.categories || [];
    ALL_GAMES = data.games || [];
    SETTINGS = data.settings || {};
    // 应用站点设置
    if (SETTINGS.site_name) document.title = SETTINGS.site_name;
    if (SETTINGS.site_name) document.querySelector(".brand-text h1").textContent = SETTINGS.site_name;
    if (SETTINGS.subtitle) document.querySelector(".brand-text p").textContent = SETTINGS.subtitle;
    if (SETTINGS.banner_text) document.querySelector(".banner-content h2").textContent = SETTINGS.banner_text;
    if (SETTINGS.announce) document.querySelector(".banner-content p").textContent = SETTINGS.announce;
    if (SETTINGS.beian) document.querySelector(".beian").textContent = SETTINGS.beian;
    currentCat = CATS[0] || null;
    renderSidebar();
    renderList();
  } catch(e) {
    // 离线降级：若后端不可用，尝试读取本地 games.js（兼容静态模式）
    if (typeof GAMES !== "undefined") {
      CATS = CATEGORIES || []; ALL_GAMES = GAMES || []; currentCat = CATS[0] || null;
      renderSidebar(); renderList();
      console.warn("后端不可用，使用本地静态数据", e);
    }
  }
}

// ---- 初始化 ----
window.onload = () => {
  bindIp();
  loadData();
  $("#searchInput").addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(renderList, 200);
  });
  document.querySelector(".search-go").addEventListener("click", renderList);
};
