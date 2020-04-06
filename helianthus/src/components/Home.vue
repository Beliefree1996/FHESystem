<template>
  <div class="Home">
    <!--    <div align="right">-->
    <!--      <div style="width: 300px">-->
    <!--        <h1 style="text-align: right">每个人都有属于自己的一片森林，</h1>-->
    <!--        <h1 style="text-align: right">迷失的人迷失了， </h1>-->
    <!--        <h1 style="text-align: right">相逢的人会再相逢。</h1>-->
    <!--      </div>-->
    <!--    </div>-->
    <div class="block">
      <span class="demonstration"></span>
      <el-carousel style="height: 300px; width: 100%">
        <el-carousel-item v-for="item in news" :key="item.id">
          <!--        <h3 class="small">{{ item.tittle }}</h3>-->
          <div style="height: 300px; width: auto">
            <img :src="item.img_src">
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>
    <el-row :gutter="10">
      <el-col :xs="24" :xl="12" :lg="12" :sm="24" :md="12">
        <el-card style="min-height: 200px; max-height: 400px; ">
          <div slot="header">
            <span v-show="playm">正在播放: {{ name }}</span>
            <span v-show="!playm">点击下列音乐进行播放</span>
          </div>
          <audio :src="audio" autoplay loop></audio>
          <div style="overflow: auto; height: 200px; width: 100%;">
            <ul style="list-style: none">
              <li v-for="m in mp3.data">
                <el-link type="primany" @click="play(m.url, m.name)" style="margin: 10px">{{ m.name }}</el-link>
              </li>
            </ul>
          </div>
        </el-card>
      </el-col>

      <el-col :xl="12" :lg="12" :sm="24" :md="12" class="hidden-sm-and-down">
        <el-card style="min-height: 200px; max-height: 300px; ">
          <div slot="header">
            <span>当前授权额度</span>
          </div>
          <el-row>
            <el-card style="margin-top:20px; margin-bottom: 20px">
              <el-tag
                style="margin-left:45%"
                :key="quota"
                type="success"
                effect="dark">
                {{ quota }}元
              </el-tag>
            </el-card>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

  </div>
</template>

<script>
  import Status from '@/components/Status'

  export default {
    name: 'Home',
    components: {
      Status
    },
    data() {
      return {
        playm: false,
        mp3: '',
        audio: '',
        name: '',
        quota: 10000,
        news: [
          {id: 1, tittle: '新闻1', img_src: '/apis/static/image/1.jpg'},
          {id: 2, tittle: '新闻2', img_src: '/apis/static/image/2.jpg'},
          {id: 3, tittle: '新闻3', img_src: '/apis/static/image/3.jpg'}
        ],
      }
    },
    methods: {
      play: function (url, name) {
        console.log(name, url)
        this.audio = url
        this.name = name
        this.playm = true
      }
    },
    created() {
      // this.$http.get('apis/get_info?mp3=yep')
      //   .then(response => {
      //     this.mp3 = response.data
      //   }, error => {
      //     console.log('mp3 error')
      //   })
      fetch("apis/get_info?mp3=yep", {
        method: "get",
      })
        .then(response => {
          return response.json()
        })
        .then(data => {
          this.mp3 = data
        })
    }
  }
</script>

<style scoped>
  .grid_content {
    background: #0b2e13;
    height: auto;
    width: auto;
  }
</style>
