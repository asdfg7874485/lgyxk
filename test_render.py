#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地验证脚本：启动 server.py，跑一遍核心 API，确认 Render 部署前一切正常。"""
import json, os, subprocess, sys, time, urllib.request, urllib.parse

PORT = 4567
os.environ["PORT"] = str(PORT)

# 用临时 data.json，避免污染真实数据
TMP = os.path.join(os.path.dirname(__file__), "data_test.json")
if os.path.exists(TMP):
    os.remove(TMP)

env = os.environ.copy()
env["PORT"] = str(PORT)
env["DATA_FILE"] = TMP

proc = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "server.py")],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
time.sleep(1.5)
BASE = f"http://127.0.0.1:{PORT}"
results, fails = [], 0

def call(path, method="GET", body=None, cookie=None):
    req = urllib.request.Request(BASE + path, method=method)
    if cookie: req.add_header("Cookie", cookie)
    if body is not None:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(body).encode()
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, dict(r.getheaders()), r.read()
    except urllib.error.HTTPError as e:
        return e.code, {}, e.read()

def check(name, cond):
    global fails
    status = "✅" if cond else "❌"
    if not cond: fails += 1
    results.append(f"{status} {name}")
    print(f"{status} {name}")

# 1. 健康检查：前台页面
code, _, _ = call("/")
check("前台页面 / 返回200", code == 200)

# 2. 健康检查：后台页面
code, _, _ = call("/admin")
check("后台页面 /admin 返回200", code == 200)

# 3. 初始数据
code, _, data = call("/api/data")
j = json.loads(data)
n_cat = len(j["categories"])
n_game = len(j["games"])
check(f"初始分类数={n_cat}（期望15）", n_cat == 15)
check(f"初始游戏数={n_game}（期望≥8）", n_game >= 8)

# 4. 未登录拦截
code, _, _ = call("/api/category/add", "POST", {"name": "测试"})
check("未登录添加分类→401", code == 401)

# 5. 登录（用原始 urllib 方式，避免 helper 里 cookie=None 污染）
req = urllib.request.Request(BASE + "/api/login", method="POST")
req.add_header("Content-Type", "application/json")
req.data = json.dumps({"username": "admin", "password": "admin123"}).encode()
set_cookies = []
with urllib.request.urlopen(req) as r:
    check("登录成功→200", r.status == 200)
    set_cookies = r.headers.get_all("Set-Cookie", [])
# 直接字符串截取：取 "session=xxx" 这一段（去掉 "Set-Cookie: " 前缀和属性）
ck = None
for h in set_cookies:
    body = h.split(":", 1)[-1].strip()          # "session=xxx; Max-Age=...; Path=/"
    pair = body.split(";")[0].strip()           # "session=xxx"
    if pair.startswith("session="):
        ck = pair
        break
print("DEBUG ck=", repr(ck))

# 6. 添加分类（无限）
code, _, data = call("/api/category/add", "POST", {"name": "测试新分类"}, cookie=ck)
check("添加分类→200", code == 200)
check("分类数+1", len(json.loads(data)["categories"]) == n_cat + 1)

# 7. 添加游戏（无限）
code, _, data = call("/api/game/add", "POST",
                     {"title": "测试游戏X", "cat": "测试新分类", "icon": "🎮",
                      "tags": ["测试"], "desc": "测试", "size": "10MB", "link": "https://example.com"},
                     cookie=ck)
check("添加游戏→200", code == 200)

# 8. 级联清理：删分类连带删游戏
call("/api/category/delete", "POST", {"name": "测试新分类"}, cookie=ck)
code, _, data = call("/api/data")
left = [g for g in json.loads(data)["games"] if g["title"] == "测试游戏X"]
check("删分类→级联清理游戏", len(left) == 0)

# 9. PV 统计
code, _, data = call("/api/stats")
check("PV统计接口", code == 200 and "pv" in json.loads(data))

proc.terminate()
proc.wait()
if os.path.exists(TMP): os.remove(TMP)

print("\n" + "=" * 40)
for r in results: print(r)
print(f"\n{'通过' if fails == 0 else '失败'}: {len(results)-fails}/{len(results)}")
sys.exit(1 if fails else 0)
