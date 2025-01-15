<template>
  <div class="goods-list">
    <h1>商品列表</h1>

    <p v-if="!user">请登录以查看商品列表。</p>

    <div v-if="goods.length > 0" :key="goodsKey">
      <div class="goods-item" v-for="item in goods" :key="item.id">
        <h2>{{ item.name }}</h2>
        <p>商品 ID: {{ item.id }}</p>
        <p>卖家 ID: {{ item.seller_id || '无卖家信息' }}</p>
        <p>起拍价: ¥{{ item.price }}</p>
        <router-link :to="`/auction-detail/${item.id}`" class="view-auction-button">
          查看拍卖
        </router-link>
      </div>
    </div>
    <p v-else>暂无商品信息。</p>
  </div>
</template>

<script>
export default {
  name: "GoodsList",
  data() {
    return {
      user: null,
      goods: [],
      goodsKey: 0
    };
  },
  mounted() {
    const userData = localStorage.getItem("user");
    if (!userData) {
      console.log("没有找到用户数据");
      this.user = null;
    } else {
      console.log("读取的用户数据:", userData);
      try {
        this.user = JSON.parse(userData);
      } catch (e) {
        console.error("解析用户数据时出错:", e);
        this.user = null;
      }
    }
    if (!this.user) {
      console.log("用户未登录，跳转到登录页面");
      this.$router.push("/login");
    } else {
      this.fetchGoods();
    }
  },
  methods: {
    async fetchGoods() {
      try {
        const response = await fetch("http://localhost:5000/all_goods");
        const result = await response.json();
        console.log("获取的商品数据:", result);
        if (response.ok) {
          this.goods = [];
          result.forEach(item => {
            this.goods.push(item);
          });
          console.log("商品数据已成功加载:", this.goods);
          this.goodsKey++;
        } else {
          console.error(result.error || "无法加载商品信息");
        }
      } catch (error) {
        console.error("获取商品列表失败:", error);
        console.error("详细错误信息:", error.message);
      }
    }
  }
};
</script>

<style scoped>
.goods-list {
  padding: 20px;
}

.goods-item {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
}

.goods-item h2 {
  font-size: 18px;
  color: #333;
}

.goods-item p {
  color: #555;
}

.view-auction-button {
  display: inline-block;
  margin-top: 10px;
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.view-auction-button:hover {
  background-color: #0056b3;
}
</style>