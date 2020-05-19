<template>
  <div id="app">
    <el-container>
      <!--  header -->
      <el-header>
        <el-col :xs="24" :sm="24">
          <el-menu :default-active="$route.path" class="el-menu-vertical-demo" mode="horizontal" router>
            <el-menu-item class="hidden-sm-and-down"><img src="./assets/logo.jpg" style="width: 30px; height: 30px;">
              <span v-if="identity===0">客户端</span>
              <span v-else-if="identity===1">企业端</span>
              <span v-else-if="identity===2">政府端</span>
            </el-menu-item>
            <el-menu-item index="/"><i class="el-icon-house"></i><span class="hidden-sm-and-down">首页</span>
            </el-menu-item>
            <el-menu-item index="/usermanage" v-if="identity===1"><i class="el-icon-set-up"></i><span class="hidden-sm-and-down">用户管理</span>
            </el-menu-item>
            <el-menu-item index="/manage" v-if="identity===2"><i class="el-icon-guide"></i><span class="hidden-sm-and-down">风控模型管理</span>
            </el-menu-item>
            <el-menu-item index="/socialsecurity" v-if="identity===0"><i class="el-icon-money"></i><span
              class="hidden-sm-and-down">个人社保</span></el-menu-item>
            <el-menu-item index="/addblog" v-if="identity!==0"><i class="el-icon-edit"></i><span
              class="hidden-sm-and-down">添加公告</span></el-menu-item>
            <el-menu-item index="/bloglist"><i class="el-icon-tickets"></i><span class="hidden-sm-and-down">公告</span>
            </el-menu-item>
            <el-menu-item index="/uploaddata" v-if="identity===2"><i class="el-icon-document-add"></i><span
              class="hidden-sm-and-down">上传信息</span></el-menu-item>
            <el-submenu index="1">
              <template slot="title"><i class="el-icon-user"></i><span class="hidden-sm-and-down">个人中心</span></template>
              <div>
                <el-menu-item index="/user/login" v-if="!islogin">登陆</el-menu-item>
                <el-menu-item index="/user/register" v-if="!islogin">注册</el-menu-item>
                <div v-else>
                  <el-menu-item index="/user/root">{{ username }}
                    <el-tag
                      size="small"
                      :type="tag_type"
                      effect="dark">
                      {{ tag_label }}
                    </el-tag>
                  </el-menu-item>
                  <el-menu-item @click="logout">退出</el-menu-item>
                </div>

              </div>
            </el-submenu>
          </el-menu>
        </el-col>
      </el-header>

      <!--        导航栏-->
      <el-main :xs="24">

        <router-view></router-view>

      </el-main>

      <el-footer>
        <el-divider content-position="left">
          <router-link to="/about"><i class="el-icon-user"></i>© 2020 Beliefree. All rights reserved.</router-link>
          &nbsp; 今日访问数: {{ num }}
        </el-divider>
      </el-footer>
    </el-container>

  </div>
</template>

<script>
  export default {
    name: 'App',
    data() {
      return {
        identity: 0,
        tag_type: 'success',
        tag_label: '已认证',
        loading: true,
        num: null,
        islogin: false,
        username: ""
      }
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath)
      },
      logout: function () {
        this.$axios.get("/apis/user/logout")
          .then(response => {
            // 重载界面
            this.$message.success("退出成功！")
            window.location.reload()
          })
      }
    },
    created() {

      this.$axios.post("/apis/add?access=add_access&aa=32&kk=34", {access: "access"})
        .then(response => {
          this.$axios.get("/apis/get_info?num=true&aa=66")
            .then(response => {
              this.loading = false
              this.num = response.data.num
            })
        }, error => {
          console.log("这里出错了.")
        })
      this.$axios.get('/apis/user/getstatus?aa=60&kk=6')
        .then(response => {
          if (response.data.status !== 1) {
            this.islogin = true
            this.username = response.data.username
            if (response.data.is_superuser) {
              this.identity = 2
            } else {
              if (response.data.is_staff) {
                this.identity = 1
              }
            }
            if (response.data.status === 2) {
              this.tag_type = 'danger'
              this.tag_label = '未认证'
            }
          }
        })


      console.log(' _______________########_______________________\n' +
        ' ______________##########_______________________\n' +
        '______________############_____________________\n' +
        '______________#############____________________\n' +
        '_____________##__###########___________________\n' +
        '____________###__######_#####__________________\n' +
        '____________###_#######___####_________________\n' +
        '___________###__##########_####________________\n' +
        '__________####__###########_####_______________\n' +
        '________#####___###########__#####_____________\n' +
        '_______######___###_########___#####___________\n' +
        '_______#####___###___########___######_________\n' +
        '______######___###__###########___######_______\n' +
        '_____######___####_##############__######______\n' +
        '____#######__#####################_#######_____\n' +
        '____#######__##############################____\n' +
        '___#######__######_#################_#######___\n' +
        '___#######__######_######_#########___######___\n' +
        '___#######____##__######___######_____######___\n' +
        '___#######________######____#####_____#####____\n' +
        '____######________#####_____#####_____####_____\n' +
        '_____#####________####______#####_____###______\n' +
        '______#####______;###________###______#________\n' +
        '________##_______####________####______________\n \n \n \n ' +
        '     HeliantHuS:    Vue就是这么酷！  qq:1984441370          ')

    }
  }
</script>

<style>
  footer {
    width: 100%;
    position: absolute;
    bottom: 0
  }
</style>
