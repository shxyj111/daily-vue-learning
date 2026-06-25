<template>
  <div id="app">
    <h1>📋 待办事项</h1>

    <div class="input-area">
      <input
        v-model="newTitle"
        @keyup.enter="addTodo"
        placeholder="输入待办内容..."
      />
      <button @click="addTodo">添加</button>
    </div>

    <ul class="todo-list" v-if="todos.length > 0">
      <li v-for="item in todos" :key="item.id">
        <span>{{ item.title }}</span>
        <button class="del-btn" @click="deleteTodo(item.id)">删除</button>
      </li>
    </ul>
    <p v-else class="empty">暂无待办事项</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      todos: [],
      newTitle: "",
    };
  },
  created() {
    this.fetchTodos();
  },
  methods: {
    async fetchTodos() {
      const res = await axios.get("/api/todos");
      this.todos = res.data.data;
    },
    async addTodo() {
      if (!this.newTitle.trim()) return;
      await axios.post("/api/todos", { title: this.newTitle });
      this.newTitle = "";
      this.fetchTodos();
    },
    async deleteTodo(id) {
      await axios.delete(`/api/todos/${id}`);
      this.fetchTodos();
    },
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  background: #f0f2f5;
  font-family: "Microsoft YaHei", sans-serif;
}
#app {
  max-width: 500px;
  margin: 60px auto;
  background: #fff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}
h1 {
  text-align: center;
  margin-bottom: 24px;
  color: #333;
}
.input-area {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}
.input-area input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}
.input-area input:focus {
  border-color: #409eff;
}
.input-area button {
  padding: 10px 20px;
  background: #409eff;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}
.input-area button:hover {
  background: #337ecc;
}
.todo-list {
  list-style: none;
}
.todo-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  border-bottom: 1px solid #ebeef5;
}
.todo-list li:last-child {
  border-bottom: none;
}
.todo-list li span {
  color: #333;
  font-size: 14px;
}
.del-btn {
  padding: 4px 12px;
  background: #f56c6c;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.2s;
}
.del-btn:hover {
  background: #e04545;
}
.empty {
  text-align: center;
  color: #999;
  font-size: 14px;
  padding: 20px 0;
}
</style>
