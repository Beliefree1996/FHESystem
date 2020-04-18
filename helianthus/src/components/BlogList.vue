<template>
  <div class="BlogList" v-loading="loading">
    <el-card class="card-content" v-for="dat in blogList" :key="dat.title">
      <div slot="header" class="card-header-text">
        <span style="font-size: 18px; font-weight: bolder">{{ dat.title }}</span>
        <div style="float: right; font-size: 5px"> {{ dat.time }} -- {{ dat.user }}</div>
      </div>
      <div>
        <span class="content-style">{{ dat.content }}</span>
      </div>
    </el-card>
    <!--页码条-->
    <el-col :span="24" class="toolbar" style="position: absolute; right: 100px; bottom: 60px">
      <el-pagination style="float:right;"
                     background
                     layout="prev, pager, next"
                     @current-change="handleCurrentChange"
                     :page-size="pageSize"
                     :total="totalPage">
      </el-pagination>
    </el-col>
  </div>
</template>

<script>
  export default {
    name: 'BlogList',
    data() {
      return {
        blogList: null,
        loading: true,
        page: 1,
        totalPage: 100,
        pageSize: 5,
      }
    },
    created() {
      this.getData()
    },
    methods: {
      getData() {
        this.$http.get("apis/get_info?blog_list=true&page=" + this.page)
          // this.$http.get("apis/get_info?wage=true&aa=60&kk=6")
          .then(response => {
            this.blogList = response.data.data
            this.totalPage = response.data.total
            this.loading = false
          }, error => {
            console.log("获取bloglist出错了.");
          });
      },
      // 点击页码
      handleCurrentChange(val) {
        this.page = val;
        this.getData();
      },
    }
  }
</script>


<style scoped>
  .card-content {
    min-width: 250px;
    max-width: 550px;
    margin: auto;
    margin-bottom: 20px;
  }

  .card-header-text {
    height: 8px;
  }

  .card-header-text span {
    font-size: 9px;
    color: #909399;
  }

  .content-style {
    font-size: 14px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
  }

</style>
