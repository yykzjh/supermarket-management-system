<template>
  <div>这是普通管理员的员工页面</div>
</template>

<script>
export default {
  data() {
    return {
      AdminiList: []
    }
  },
  created () {
    this.getAdminiList()
  },
  methods: {
    async getAdminiList() {
      const {data: res} = await this.$http.get('Users/AllUsers',{
        params:{
          name:"superadmin"
        }
      })
      console.log(res)
    }
  }
}
</script>

<style scoped>

</style>
