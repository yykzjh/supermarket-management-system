<template>
  <div>这是商品信息页面</div>
</template>

<script>
  export default {
    data() {
      return {
        goodid: 0,
      }
    },
    created () {
      this.goodid = this.$route.query.goodid
      console.log(this.goodid)
    },
  }
</script>

<style scoped>

</style>
