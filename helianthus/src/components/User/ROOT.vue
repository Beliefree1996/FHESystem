<template>
  <div id="ROOT">
    <el-row type="flex" justify="center">
      <el-col :xs="24" :sm="24">
        <img src="/apis/static/image/default_user_head.jpg" alt="" height="130px" width="130px" align="right">
      </el-col>
      <el-col>
        <p style="margin: 20px; font-size: 30px">{{ username }}
          <el-tag
            :type="tag_type"
            effect="dark">
            {{ tag_label }}
          </el-tag>
          <el-button type="text" v-if="status" @click="Certification">去认证</el-button>
        </p>
        <p style="margin: 20px; font-size: 30px; border-bottom: 20px">{{ email }}</p>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: 'ROOT',
    data() {
      return {
        tag_type: 'success',
        tag_label: '已认证',
        user_id: 0,
        status: false,
        username: "",
        email: "",
      }
    },
    created() {
      this.$axios.get('/apis/user/getstatus?aa=60&kk=6')
        .then(response => {
          if (response.data.status === 1) {
            this.$router.push({path: "/user/login"})
          } else {
            // 验证登录后执行下面的内容！！
            this.user_id = response.data.id
            this.username = response.data.username
            this.email = response.data.email
            if (response.data.status === 2) {
              this.status = true
              this.tag_type = 'danger'
              this.tag_label = '未认证'
            }

          }
        })
    },
    methods: {
      Certification() {
        this.$prompt('请输入您的身份证号', '认证', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/,
          inputErrorMessage: '身份证号格式不正确'
        }).then(({ value }) => {
          this.$axios.get('../apis/change_data?certification=true&user_id=' + this.user_id + '&IC_num=' + value)
          .then(response => {
            if (response.data.status_code === 0) {
              this.$message.success("认证成功！")
            } else {
              this.$message.error("网络错误，认证失败")
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消认证'
          });
        });
      }
    }
  }
</script>

<style scoped>

</style>
