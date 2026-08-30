#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
亮哥游戏库 - 后端服务（零依赖，仅用 Python 标准库）
功能：分类 & 游戏 无限添加 / 编辑 / 删除 + 后台登录 + 数据统计
启动：python3 server.py
访问：前台 http://localhost:3000/   后台 http://localhost:3000/admin
"""
import json, os, uuid, hashlib, datetime, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie

HOST, PORT = "0.0.0.0", int(os.environ.get("PORT", "3000"))
DATA_FILE = os.environ.get("DATA_FILE") or os.path.join(os.path.dirname(__file__), "data.json")
SECRET = "liangge-session-secret"

# ---------------- 数据持久化 ----------------
_lock = threading.Lock()

def default_data():
    return {
        "admins": [{"username": "admin", "password": hashlib.md5("admin123".encode()).hexdigest()}],
        "settings": {
            "site_name": "亮哥游戏库",
            "subtitle": "小苹果乐园 · 精选正版小游戏",
            "banner_text": "亮哥精选 · 一库畅玩",
            "announce": "正规授权 · 官方渠道 · 安全下载",
            "beian": "示例备案号：京ICP备XXXXXXXX号",
        },
        "categories": [
            "亮哥推荐", "苹果游戏(IOS)", "萌灵社", "主讯", "狼来了",
            "久游", "北京柚享", "无极", "翱翔", "灵动",
            "聚合汇", "猫咪", "小鱼", "测快手专用", "栀子乐园"
        ],
        "games": [
            {"id":"1","title":"方块消除大师","icon":"🧩","cat":"亮哥推荐","tags":["三消","轻松"],"desc":"经典三消玩法，数百关卡挑战眼力与策略。","size":"12MB","date":"2026-08-29","plays":9821,"link":"#"},
            {"id":"2","title":"合成大西瓜","icon":"🍉","cat":"亮哥推荐","tags":["合成","上头"],"desc":"合成相同水果，直到种出巨型西瓜！","size":"8MB","date":"2026-08-29","plays":32105,"link":"#"},
            {"id":"3","title":"节奏音游","icon":"🎵","cat":"亮哥推荐","tags":["音乐","节奏"],"desc":"跟着节拍点击音符，享受音乐快感。","size":"35MB","date":"2026-08-28","plays":11200,"link":"#"},
            {"id":"4","title":"水果忍者","icon":"🥷","cat":"苹果游戏(IOS)","tags":["切水果","爽快"],"desc":"挥刀切水果，小心别切到炸弹！","size":"13MB","date":"2026-08-27","plays":16700,"link":"#"},
            {"id":"5","title":"萌灵小镇","icon":"🌸","cat":"萌灵社","tags":["养成","治愈"],"desc":"收集可爱灵兽，打造你的梦幻小镇。","size":"42MB","date":"2026-08-28","plays":8800,"link":"#"},
            {"id":"6","title":"狼人推理","icon":"🐺","cat":"狼来了","tags":["桌游","社交"],"desc":"语言推理社交游戏，找出隐藏的狼人。","size":"28MB","date":"2026-08-25","plays":7600,"link":"#"},
            {"id":"7","title":"久游棋牌","icon":"🀄","cat":"久游","tags":["棋牌","休闲"],"desc":"经典棋牌合集，随时随地来一局。","size":"22MB","date":"2026-08-19","plays":11300,"link":"#"},
            {"id":"8","title":"翱翔飞行","icon":"✈️","cat":"翱翔","tags":["飞行","冒险"],"desc":"驾驶飞机穿越云层，探索广阔天空。","size":"40MB","date":"2026-08-16","plays":5900,"link":"#"},
        ],
        "stats": {"pv": 0, "clicks": 0},
    }

def load():
    if not os.path.exists(DATA_FILE):
        d = default_data(); save(d); return d
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        # 文件损坏（如写入中断）→ 自动重建，避免服务崩溃
        d = default_data(); save(d); return d

def save(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

DB = load()

# ---------------- 工具 ----------------
def jdump(obj): return json.dumps(obj, ensure_ascii=False).encode("utf-8")

def send(resp, code, ctype, body):
    resp.send_response(code)
    resp.send_header("Content-Type", ctype)
    resp.send_header("Content-Length", str(len(body)))
    resp.end_headers()
    resp.wfile.write(body)

def ok(resp, obj): send(resp, 200, "application/json", jdump(obj))
def fail(resp, msg, code=400): send(resp, code, "application/json", jdump({"error": msg}))

def get_cookie(resp):
    c = SimpleCookie(resp.headers.get("Cookie", ""))
    return c

def is_login(req):
    c = SimpleCookie(req.headers.get("Cookie", ""))
    sid = c.get("session")
    return bool(sid and sid.value == SECRET)

def read_body(req):
    n = int(req.headers.get("Content-Length", 0))
    return json.loads(req.rfile.read(n).decode("utf-8") or "{}")

# ---------------- 路由 ----------------
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _serve_static(self, path):
        # 简单静态文件服务（前台 + 后台页面）
        base = os.path.dirname(__file__)
        if path in ("/", "/index.html"): path = "/index.html"
        elif path == "/admin": path = "/admin.html"
        fp = os.path.normpath(os.path.join(base, path.lstrip("/")))
        if not fp.startswith(base): return self._send(403, b"forbidden")
        if os.path.isdir(fp): fp = os.path.join(fp, "index.html")
        if not os.path.exists(fp): return self._send(404, b"not found")
        ext = fp.rsplit(".", 1)[-1]
        ct = {"html":"text/html","css":"text/css","js":"application/javascript",
              "json":"application/json","png":"image/png","svg":"image/svg+xml"}.get(ext, "text/plain")
        with open(fp, "rb") as f:
            self.send_response(200); self.send_header("Content-Type", ct)
            self.send_header("Content-Length", str(os.path.getsize(fp)))
            self.end_headers(); self.wfile.write(f.read())

    def _send(self, code, body):
        self.send_response(code); self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        p = self.path.split("?", 1)[0]
        # API
        if p == "/api/data":      # 前台拿全量数据
            with _lock: DB["stats"]["pv"] += 1; save(DB)
            return ok(self, {"categories": DB["categories"], "games": DB["games"], "settings": DB["settings"]})
        if p == "/api/stats":
            return ok(self, DB.get("stats", {}))
        if p.startswith("/api/"):
            return fail(self, "not found", 404)
        self._serve_static(p)

    def do_POST(self):
        p = self.path
        # 登录（无需鉴权）
        if p == "/api/login":
            b = read_body(self)
            u, pw = b.get("username",""), b.get("password","")
            with _lock:
                adm = DB["admins"]
            if any(a["username"]==u and a["password"]==hashlib.md5(pw.encode()).hexdigest() for a in adm):
                c = SimpleCookie(); c["session"] = SECRET
                c["session"]["path"] = "/"; c["session"]["max-age"] = "86400"
                self.send_response(200)
                # 逐个 Set-Cookie 属性单独发送，避免 "Set-Cookie: Set-Cookie:" 重复前缀
                for m in str(c).split("\r\n"):
                    if m: self.send_header("Set-Cookie", m.split(": ", 1)[1])
                self.send_header("Content-Type", "application/json")
                self.end_headers(); self.wfile.write(jdump({"ok": True}))
            else:
                fail(self, "账号或密码错误", 401)
            return

        if not is_login(self):
            return fail(self, "未登录", 401)

        b = read_body(self)
        with _lock:
            # ---- 分类：无限添加 / 删除 ----
            if p == "/api/category/add":
                name = (b.get("name") or "").strip()
                if not name: return fail(self, "分类名不能为空")
                if name in DB["categories"]: return fail(self, "分类已存在")
                DB["categories"].append(name); save(DB)
                return ok(self, {"categories": DB["categories"]})
            if p == "/api/category/delete":
                name = b.get("name", "")
                if name == "亮哥推荐": return fail(self, "默认分类不可删除")
                if name in DB["categories"]:
                    DB["categories"].remove(name)
                    DB["games"] = [g for g in DB["games"] if g["cat"] != name]  # 级联清理
                save(DB); return ok(self, {"categories": DB["categories"]})

            # ---- 游戏：添加 / 编辑 / 删除（无限）----
            if p == "/api/game/add":
                g = b; g["id"] = str(uuid.uuid4())[:8]
                g.setdefault("tags", []); g.setdefault("plays", 0)
                g.setdefault("date", datetime.date.today().isoformat())
                g.setdefault("link", "#")
                DB["games"].append(g); save(DB)
                return ok(self, {"game": g})
            if p == "/api/game/update":
                gid = str(b.get("id","")); 
                for i, g in enumerate(DB["games"]):
                    if str(g["id"]) == gid:
                        DB["games"][i] = {**g, **b, "id": gid}; save(DB)
                        return ok(self, {"game": DB["games"][i]})
                return fail(self, "游戏不存在", 404)
            if p == "/api/game/delete":
                gid = str(b.get("id",""))
                DB["games"] = [g for g in DB["games"] if str(g["id"]) != gid]; save(DB)
                return ok(self, {"ok": True})
            if p == "/api/game/click":
                gid = str(b.get("id",""))
                for g in DB["games"]:
                    if str(g["id"]) == gid: g["plays"] = int(g.get("plays",0)) + 1
                DB["stats"]["clicks"] += 1; save(DB)
                return ok(self, {"ok": True})

            # ---- 站点设置 ----
            if p == "/api/settings":
                DB["settings"].update(b); save(DB)
                return ok(self, {"settings": DB["settings"]})

            fail(self, "unknown endpoint", 404)

    def do_DELETE(self):  # 预留
        pass

if __name__ == "__main__":
    print(f"🚀 亮哥游戏库 启动中：http://localhost:{PORT}/")
    print(f"   前台：http://localhost:{PORT}/")
    print(f"   后台：http://localhost:{PORT}/admin   (默认 admin / admin123)")
    HTTPServer((HOST, PORT), Handler).serve_forever()
