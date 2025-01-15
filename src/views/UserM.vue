<template>
  <div class="create-auction">
    <h2>创建拍卖</h2>
    <form @submit.prevent="submitAuction">
      <div>
        <label for="starting_price">起拍价</label>
        <input v-model="auction.starting_price" type="number" id="starting_price" required />
      </div>
      <div>
        <label for="minimum_increment">最低增幅</label>
        <input v-model="auction.minimum_increment" type="number" id="minimum_increment" required />
      </div>
      <div>
        <label for="reserve_price">保留价</label>
        <input v-model="auction.reserve_price" type="number" id="reserve_price" />
      </div>
      <div>
        <label for="start_time">开始时间</label>
        <input v-model="auction.start_time" type="datetime-local" id="start_time" required />
      </div>
      <div>
        <label for="time_long">拍卖时长（分钟）</label>
        <input v-model="auction.time_long" type="number" id="time_long" required />
      </div>
      <div>
        <label for="goods_name">商品名字</label>
        <input v-model="auction.goods_name" type="text" id="goods_name" required />
      </div>
      <button type="submit">创建拍卖</button>
    </form>

    <div class="user-profile">
      <h1>个人信息</h1>
      <p v-if="!user">请登录以查看个人信息。</p>
      <div v-else>
        <div class="user-info">
          <h2>当前信息：</h2>
          <p><strong>用户名：</strong> {{ user.username }}</p>
          <p><strong>角色：</strong> {{ user.role }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      auction: {
        starting_price: '',
        minimum_increment: '',
        reserve_price: '',
        start_time: '',
        time_long: '',
        goods_name: '',
        user_id: ''
      },
      user: null
    };
  },
  created() {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (userData && userData.user_id) {
      this.auction.user_id = userData.user_id;
      this.user = userData;
    } else {
      console.error('未登录用户，无法获取用户ID');
    }
  },
  methods: {
async submitAuction() {
  try {
    const formattedStartTime = this.auction.start_time.replace('T', ' ');

    const goodsResponse = await fetch('http://localhost:5000/goods', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        goods_name: this.auction.goods_name,
        price: this.auction.starting_price,
        seller_id: this.auction.user_id
      })
    });

    const goodsData = await goodsResponse.json();

    if (goodsResponse.ok) {
      console.log('商品创建成功:', goodsData);

      const auctionResponse = await fetch('http://localhost:5000/auction', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          starting_price: this.auction.starting_price,
          minimum_increment: this.auction.minimum_increment,
          reserve_price: this.auction.reserve_price,
          start_time: formattedStartTime,
          time_long: this.auction.time_long,
          goods_id: goodsData.goods_id,
          user_id: this.auction.user_id
        })
      });

      const auctionData = await auctionResponse.json();
      if (auctionResponse.ok) {
        console.log('拍卖创建成功:', auctionData);
      } else {
        console.error('拍卖创建失败:', auctionData.error);
      }

    } else {
      console.error('商品创建失败:', goodsData.error);
    }
  } catch (error) {
    console.error('请求出错:', error);
  }
}

  }
};
</script>

<style scoped>
.create-auction {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.create-auction form div {
  margin-bottom: 10px;
}

.create-auction form label {
  display: block;
  margin-bottom: 5px;
}

.create-auction form input {
  width: 100%;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.create-auction button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.create-auction button:hover {
  background-color: #45a049;
}

.user-profile {
  margin-top: 30px;
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 5px;
}

.user-profile h1 {
  margin-bottom: 10px;
}

.user-profile .user-info {
  margin-top: 20px;
}

.user-profile .user-info p {
  margin: 5px 0;
}
</style>
