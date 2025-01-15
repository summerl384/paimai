<template>
  <div class="auction-result">
    <h1>拍卖结果</h1>
    <p v-if="result.message">{{ result.message }}</p>
    <p v-if="result.winner">中标者: {{ result.winner }}</p>
    <p v-if="result.winning_bid">中标价: {{ result.winning_bid }}</p>
  </div>
</template>

<script>
export default {
  name: "AuctionResult",
  data() {
    return {
      result: {},
    };
  },
  async created() {
    const auctionId = this.$route.params.id;
    try {
      const response = await fetch(`http://localhost:5000/auction/${auctionId}/close`, {
        method: "POST",
      });
      this.result = await response.json();
    } catch (error) {
      console.error("获取拍卖结果失败:", error);
    }
  },
};
</script>

<style scoped>
.auction-result {
  padding: 20px;
}
</style>
