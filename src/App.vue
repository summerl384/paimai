<template>
  <div id="app">
    <header>
      <h1>拍卖系统</h1>
      <nav>
        <router-link v-if="!isLoggedIn" to="/login">登录</router-link>
        <router-link v-if="!isLoggedIn" to="/register">注册</router-link>
        <router-link v-if="isLoggedIn" to="/goods-list">商品列表</router-link>
        <router-link to="/user-profile" class="user-profile-link">个人信息</router-link> <!-- 新增个人信息按钮 -->
        <button v-if="isLoggedIn" @click="logout">退出登录</button>
      </nav>
    </header>
    <main>
      <router-view @login-success="handleLoginSuccess" />
    </main>
    <footer>
      <p>© 20220441228</p>
    </footer>
  </div>
</template>

<script>
import { reactive } from "vue";

export default {
  name: "App",
  setup() {
    const state = reactive({
      isLoggedIn: false,
    });

    const handleLoginSuccess = () => {
      state.isLoggedIn = true;
    };

    const logout = () => {
      state.isLoggedIn = false;
    };

    return {
      isLoggedIn: state.isLoggedIn,
      handleLoginSuccess,
      logout,
    };
  },
};
</script>

<style>
#app {
  text-align: center;
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
.user-profile-link {
    display: inline-block;
    margin: 0 10px;
    color: white;
    text-decoration: none;
}
header {
  background-color: #333;
  color: white;
  padding: 10px 0;
}

header nav a {
  margin: 0 10px;
  color: white;
  text-decoration: none;
}

header nav a:hover {
  text-decoration: underline;
}

main {
  padding: 20px;
}

footer {
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}
</style>