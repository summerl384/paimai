<template>
  <div class="admin-dashboard">
    <h1>超级用户管理界面</h1>

    <section>
      <h2>用户管理</h2>
      <button @click="toggleUserForm" v-if="!isUserFormVisible">添加用户</button>
      <div v-if="isUserFormVisible">
        <form @submit.prevent="addUser">
          <input v-model="newUser.username" placeholder="用户名" required />
          <input v-model="newUser.password" type="password" placeholder="密码" required />
          <input v-model="newUser.role" placeholder="角色" required />
          <button type="submit">添加</button>
        </form>
        <button @click="toggleUserForm">取消</button>
      </div>

      <ul>
        <li v-for="user in users" :key="user.user_id">
          <p>{{ user.username }} ({{ user.role }})</p>
          <button @click="editUser(user)">编辑</button>
          <button @click="deleteUser(user.user_id)">删除</button>
        </li>
      </ul>
    </section>

    <section>
      <h2>商品管理</h2>
      <button @click="toggleGoodsForm" v-if="!isGoodsFormVisible">添加商品</button>
      <div v-if="isGoodsFormVisible">
        <form @submit.prevent="addGoods">
          <input v-model="newGoods.name" placeholder="商品名称" required />
          <input v-model="newGoods.price" type="number" placeholder="价格" required />
          <input v-model="newGoods.seller_id" placeholder="卖家ID" required />
          <button type="submit">添加</button>
        </form>
        <button @click="toggleGoodsForm">取消</button>
      </div>
      <ul>
        <li v-for="item in goods" :key="item.id">
          <p>{{ item.name }} - ¥{{ item.price }}</p>
          <button @click="editGoods(item)">编辑</button>
          <button @click="deleteGoods(item.id)">删除</button>
        </li>
      </ul>
    </section>

    <div v-if="showUserEditModal" class="modal">
      <div class="modal-content">
        <h3>编辑用户</h3>
        <form @submit.prevent="submitUserEdit">
          <input v-model="editUserForm.username" placeholder="用户名" required />
          <input v-model="editUserForm.password" type="password" placeholder="密码" required />
          <input v-model="editUserForm.role" placeholder="角色" required />
          <button type="submit">保存</button>
          <button @click="showUserEditModal = false">取消</button>
        </form>
      </div>
    </div>

    <div v-if="showGoodsEditModal" class="modal">
      <div class="modal-content">
        <h3>编辑商品</h3>
        <form @submit.prevent="submitGoodsEdit">
          <input v-model="editGoodsForm.name" placeholder="商品名称" required />
          <input v-model="editGoodsForm.price" type="number" placeholder="价格" required />
          <input v-model="editGoodsForm.seller_id" placeholder="卖家ID" required />
          <button type="submit">保存</button>
          <button @click="showGoodsEditModal = false">取消</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "AdminDashboard",
  data() {
    return {
      users: [],
      goods: [],
      newUser: { username: "", password: "", role: "" },
      newGoods: { name: "", price: 0, seller_id: "" },
      isUserFormVisible: false,
      isGoodsFormVisible: false,
      editUserForm: { username: "", password: "", role: "" },
      editGoodsForm: { name: "", price: 0, seller_id: "" },
      showUserEditModal: false,
      showGoodsEditModal: false,
    };
  },
  mounted() {
    this.fetchUsers();
    this.fetchGoods();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await fetch("http://localhost:5000/users");
        const result = await response.json();
        if (response.ok) {
          this.users = result;
        } else {
          console.error("无法加载用户信息");
        }
      } catch (error) {
        console.error("获取用户失败:", error);
      }
    },
    async fetchGoods() {
      try {
        const response = await fetch("http://localhost:5000/all_goods");
        const result = await response.json();
        console.log(result);
        if (response.ok) {
          this.goods = result;
        } else {
          console.error("无法加载商品信息");
        }
      } catch (error) {
        console.error("获取商品失败:", error);
      }
    },
    toggleUserForm() {
      this.isUserFormVisible = !this.isUserFormVisible;
    },
    toggleGoodsForm() {
      this.isGoodsFormVisible = !this.isGoodsFormVisible;
    },
    async addUser() {
      try {
        const response = await fetch("http://localhost:5000/users", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.newUser),
        });
        const result = await response.json();
        if (response.ok) {
          this.fetchUsers();
          this.newUser = { username: "", password: "", role: "" };
        } else {
          console.error(result.error || "添加用户失败");
        }
      } catch (error) {
        console.error("添加用户失败:", error);
      }
    },

async addGoods() {
   try {
     if (!this.newGoods.name || this.newGoods.price <= 0 || !this.newGoods.seller_id) {
       console.error("商品名称、价格和卖家ID不能为空");
       return;
     }

     console.log(this.newGoods);

     const response = await fetch("http://localhost:5000/goods", {
       method: "POST",
       headers: {
         "Content-Type": "application/json",
       },
       body: JSON.stringify({
         goods_name: this.newGoods.name,
         price: this.newGoods.price,
         seller_id: this.newGoods.seller_id,
       }),
     });

     const result = await response.json();

     if (response.ok) {
       this.fetchGoods();
       this.newGoods = { name: "", price: 0, seller_id: "" };
     } else {
       console.error(result.error || "添加商品失败");
     }
   } catch (error) {
     console.error("添加商品失败:", error);
   }
}

,
    editUser(user) {
      console.log("编辑用户", user);
      this.editUserForm = { ...user };
      this.showUserEditModal = true;
    },

    async submitUserEdit() {
      try {
        const response = await axios.put(`http://localhost:5000/user/${this.editUserForm.user_id}`, this.editUserForm);
        console.log("用户编辑成功", response.data);
        this.showUserEditModal = false;
        this.fetchUsers();
      } catch (error) {
        console.error("用户编辑失败", error.response.data);
      }
    },

editGoods(item) {
  console.log("编辑商品", item);

  this.editGoodsForm = { ...item };
  this.showGoodsEditModal = true;
},

async submitGoodsEdit() {
  if (!this.editGoodsForm.id) {
    console.error("商品ID不能为空");
    return;
  }
  try {
    const response = await axios.put(`http://localhost:5000/goods/${this.editGoodsForm.id}`, this.editGoodsForm);
    console.log("商品编辑成功", response.data);
    this.showGoodsEditModal = false;
    this.fetchGoods();
  } catch (error) {
    console.error("商品编辑失败", error.response ? error.response.data : error.message);
  }
}
,

    async deleteUser(user_id) {
      try {
        const response = await fetch(`http://localhost:5000/users/${user_id}`, {
          method: "DELETE",
        });
        if (response.ok) {
          this.fetchUsers();
        } else {
          console.error("删除用户失败");
        }
      } catch (error) {
        console.error("删除用户失败:", error);
      }
    },
    // 删除商品
    async deleteGoods(goods_id) {
      try {
        const response = await fetch(`http://localhost:5000/goods/${goods_id}`, {
          method: "DELETE",
        });
        if (response.ok) {
          this.fetchGoods();
        } else {
          console.error("删除商品失败");
        }
      } catch (error) {
        console.error("删除商品失败:", error);
      }
    },
  },
};
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

section {
  margin-bottom: 30px;
}

button {
  padding: 5px 10px;
  margin-top: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
}

button:hover {
  background-color: #0056b3;
}

form {
  display: flex;
  gap: 10px;
}

form input {
  padding: 5px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background-color: #f8f8f8;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
}

li button {
  background-color: #ff4d4d;
}

li button:hover {
  background-color: #ff1a1a;
}
/* 样式可以根据实际情况调整 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
}
</style>
