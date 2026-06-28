from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 内存数据存储
todos = []
todo_id_counter = 1

# ==================== 管理页面模板 ====================
ADMIN_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>后台管理 - 待办事项</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #1a1a2e; color: #eee; font-family: 'Microsoft YaHei', sans-serif; }
        .container { max-width: 700px; margin: 40px auto; padding: 30px; }
        h1 { text-align: center; margin-bottom: 8px; color: #e94560; }
        .subtitle { text-align: center; color: #888; font-size: 13px; margin-bottom: 24px; }
        .add-area { display: flex; gap: 10px; margin-bottom: 20px; }
        .add-area input { flex: 1; padding: 10px 14px; border: 1px solid #333; border-radius: 6px; font-size: 14px; background: #16213e; color: #eee; outline: none; }
        .add-area input:focus { border-color: #e94560; }
        .add-area button { padding: 10px 20px; background: #e94560; color: #fff; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; }
        .add-area button:hover { background: #c73652; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px 14px; text-align: left; border-bottom: 1px solid #333; }
        th { color: #888; font-size: 12px; text-transform: uppercase; }
        td { font-size: 14px; }
        .del-btn { padding: 4px 12px; background: #e94560; color: #fff; border: none; border-radius: 4px; font-size: 12px; cursor: pointer; }
        .del-btn:hover { background: #c73652; }
        .empty { text-align: center; color: #666; padding: 40px 0; }
        .stats { text-align: center; font-size: 13px; color: #666; margin-top: 20px; }
        .flash { position: fixed; top: 20px; right: 20px; padding: 12px 20px; border-radius: 6px; font-size: 14px; display: none; }
        .flash.success { background: #27ae60; color: #fff; }
    </style>
</head>
<body>
    <div class="flash" id="flash"></div>
    <div class="container">
        <h1>后台管理</h1>
        <p class="subtitle">此处修改数据，前端页面会自动刷新看到变化</p>

        <div class="add-area">
            <input id="titleInput" placeholder="输入待办内容..." onkeyup="if(event.key==='Enter')addTodo()">
            <button onclick="addTodo()">添加</button>
        </div>

        <table>
            <thead>
                <tr><th>ID</th><th>内容</th><th>操作</th></tr>
            </thead>
            <tbody id="todoBody">
                <tr><td colspan="3" class="empty">暂无数据</td></tr>
            </tbody>
        </table>
        <p class="stats" id="stats"></p>
    </div>

    <script>
        async function fetchTodos() {
            const res = await fetch('/api/todos');
            const json = await res.json();
            const tbody = document.getElementById('todoBody');
            if (json.data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" class="empty">暂无数据</td></tr>';
            } else {
                tbody.innerHTML = json.data.map(t =>
                    `<tr>
                        <td>${t.id}</td>
                        <td>${t.title}</td>
                        <td><button class="del-btn" onclick="delTodo(${t.id})">删除</button></td>
                    </tr>`
                ).join('');
            }
            document.getElementById('stats').textContent = `共 ${json.data.length} 条待办`;
        }

        async function addTodo() {
            const input = document.getElementById('titleInput');
            const title = input.value.trim();
            if (!title) return;
            await fetch('/api/todos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title })
            });
            input.value = '';
            fetchTodos();
            showFlash('添加成功');
        }

        async function delTodo(id) {
            await fetch(`/api/todos/${id}`, { method: 'DELETE' });
            fetchTodos();
            showFlash('删除成功');
        }

        function showFlash(msg) {
            const el = document.getElementById('flash');
            el.textContent = msg;
            el.className = 'flash success';
            el.style.display = 'block';
            setTimeout(() => el.style.display = 'none', 1500);
        }

        fetchTodos();
    </script>
</body>
</html>
"""


# ==================== API 接口（给前端 Vue 调用） ====================

@app.route("/api/todos", methods=["GET"])
def get_todos():
    """获取所有待办事项"""
    return jsonify({"code": 0, "data": todos, "message": "ok"})


@app.route("/api/todos", methods=["POST"])
def add_todo():
    """新增待办事项"""
    global todo_id_counter
    data = request.get_json()
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"code": 1, "data": None, "message": "内容不能为空"}), 400

    todo = {"id": todo_id_counter, "title": title}
    todo_id_counter += 1
    todos.append(todo)
    return jsonify({"code": 0, "data": todo, "message": "添加成功"})


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """删除待办事项"""
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"code": 0, "data": None, "message": "删除成功"})


# ==================== 后台管理页面 ====================

@app.route("/admin")
def admin():
    """后端独立管理页面"""
    return render_template_string(ADMIN_PAGE)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
