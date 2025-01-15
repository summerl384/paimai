<template>
  <div class="user-register">
    <div class="register-container">
      <h1>用户注册</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名:</label>
          <input
            v-model="username"
            type="text"
            id="username"
            placeholder="输入用户名"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">密码:</label>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="输入密码"
            required
          />
        </div>

        <button type="submit" class="register-button">注册</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserRegister",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async handleRegister() {
      try {
        const response = await fetch("http://localhost:5000/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        const result = await response.json();
        if (response.ok) {
          // 注册成功，提示用户
          alert("注册成功！");

          // 注册后跳转到登录页面
          this.$router.push("/login");
        } else {
          alert(result.error || "注册失败");
        }
      } catch (error) {
        console.error("注册出错:", error);
      }
    },
  },
};
</script>

<style scoped>
.user-register {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f0f2f5;
}

.register-container {
  background: white;
  padding: 30px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h1 {
  color: #333;
  margin-bottom: 20px;
  font-size: 24px;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

input:focus {
  border-color: #28a745;
  outline: none;
  box-shadow: 0 0 3px rgba(40, 167, 69, 0.5);
}

.register-button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  color: white;
  background-color: #28a745;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.register-button:hover {
  background-color: #218838;
}

.register-button:focus {
  outline: none;
  box-shadow: 0 0 3px rgba(40, 167, 69, 0.5);
}
</style>
