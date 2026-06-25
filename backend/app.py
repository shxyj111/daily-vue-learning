from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 内存数据存储
todos = []
todo_id_counter = 1


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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
