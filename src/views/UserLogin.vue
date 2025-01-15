<template>
  <div class="user-login">
    <div class="login-container">
      <h1>用户登录</h1>
      <form @submit.prevent="handleLogin">
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

        <button type="submit" class="login-button" :disabled="loading">
          {{ loading ? "登录中..." : "登录" }}
        </button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserLogin",
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
      loading: false,
    };
  },
  methods: {
    async handleLogin() {
      if (!this.username || !this.password) {
        this.errorMessage = "用户名和密码不能为空！";
        return;
      }

      this.errorMessage = "";
      this.loading = true;

      try {
        const response = await fetch("http://localhost:5000/login", {
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
          alert("登录成功！");

          const userData = result.user;
          if (userData) {
            console.log("登录返回的用户数据:", userData);
            localStorage.setItem("user", JSON.stringify(userData));
            localStorage.setItem("isLoggedIn", true);

            if (userData.role === '超级用户') {
              this.$router.push("/admin-dashboard");
            } else {
              this.$router.push("/goods-list");
            }
          } else {
            this.errorMessage = "登录失败，请检查用户名或密码！";
          }
        } else {
          this.errorMessage = result.error || "登录失败，请检查用户名或密码！";
        }
      } catch (error) {
        console.error("登录出错:", error);
        this.errorMessage = "网络错误，请稍后再试！";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
<style scoped>
.user-login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f0f2f5;
}

.login-container {
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
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 3px rgba(0, 123, 255, 0.5);
}

.login-button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:disabled {
  background-color: #a0c4ff;
  cursor: not-allowed;
}

.login-button:hover {
  background-color: #0056b3;
}

.login-button:focus {
  outline: none;
  box-shadow: 0 0 3px rgba(0, 123, 255, 0.5);
}

.error {
  color: red;
  margin-top: 10px;
  font-size: 14px;
}
</style>
