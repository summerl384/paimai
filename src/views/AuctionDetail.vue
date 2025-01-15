<template>
  <div class="auction-detail">
    <h1>拍卖详情</h1>
    <p v-if="auction">商品名称: {{ auction.goods_name }}</p>
    <p v-if="auction">商品描述: {{ auction.goods_description }}</p>
    <p v-if="auction">当前价格: ¥{{ auction.current_price }}</p>
    <p v-if="auction">最低加价幅度: ¥{{ auction.minimum_increment }}</p>
    <p v-if="auction">起拍价: ¥{{ auction.starting_price }}</p>
    <p v-if="auction">保留价: ¥{{ auction.reserve_price || '无' }}</p>
    <p v-if="auction">拍卖时长: {{ auction.time_long }} 分钟</p>
    <p v-if="auction">拍卖开始时间: {{ auction.start_time }}</p>
    <p v-if="auction">拍卖结束时间: {{ auction.end_time }}</p>

    <div v-if="user">
      <input v-model="bidAmount" type="number" placeholder="请输入您的出价" />
      <button @click="placeBid">出价</button>
    </div>
    <p v-else>请登录后参与竞拍。</p>
  </div>
</template>

<script>
export default {
  name: 'AuctionDetail',
  data() {
    return {
      auction: null,
      bidAmount: 0,
      user: null
    };
  },
  async mounted() {
    const auctionId = this.$route.params.id;
    this.fetchAuctionDetail(auctionId);

    const userData = localStorage.getItem("user");
    if (userData) {
      this.user = JSON.parse(userData);
    } else {
      console.log("未登录，跳转至登录页面");
      this.$router.push("/login");
    }
  },
  methods: {
    async fetchAuctionDetail(auctionId) {
      try {
        const response = await fetch(`http://localhost:5000/auction/${auctionId}`);
        if (response.ok) {
          this.auction = await response.json();
        } else {
          console.error("无法加载拍卖信息");
        }
      } catch (error) {
        console.error("无法加载拍卖信息:", error);
      }
    },
    async placeBid() {
  if (!this.auction) {
    alert("拍卖详情尚未加载，请稍后再试！");
    return;
  }

  if (this.bidAmount <= this.auction.current_price) {
    alert("您的出价必须高于当前价格！");
    return;
  }

  const bidData = {
    bid_amount: this.bidAmount,
    auction_id: this.auction.auction_id,
  };

  try {
    const response = await fetch("http://localhost:5000/bid", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bidData),
    });

    if (response.ok) {
      alert("出价成功！");
      this.fetchAuctionDetail(this.auction.auction_id);
    } else {
      const result = await response.json();
      alert(`出价失败：${result.error || "请稍后重试。"}`);
    }
  } catch (error) {
    console.error("出价失败:", error);
    alert("出价失败，请检查网络连接！");
  }
}

  }
};
</script>

<style scoped>

.auction-detail {
  padding: 20px;
}

.auction-detail p {
  margin-bottom: 10px;
}

input {
  margin-top: 10px;
  padding: 5px;
  font-size: 16px;
}

button {
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
