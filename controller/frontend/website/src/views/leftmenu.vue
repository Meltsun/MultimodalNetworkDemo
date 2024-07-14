<template>
  <div>
    <el-menu default-active="/topology"
      class="el-menu-vertical-demo"
      background-color="#ecf5ff"
      text-color="#333"
      active-text-color="#ffd04b"
      router ><!--开启路由模式-->
      <el-menu-item index="/topology"><!--index为跳转路径-->
        <i class="el-icon-menu"></i><!--i标签-->
        <span slot="title">系统拓扑</span>
      </el-menu-item>
      <el-menu-item index="/testtask">
        <i class="el-icon-document"></i>
        <span slot="title">网络状态</span>
      </el-menu-item>
      <el-menu-item index="/flowtable">
        <i class="el-icon-setting"></i>
        <span slot="title">下发流表</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  
}
</script>

<style lang="less" scoped>
.el-menu{
  border-right:0;

 /deep/ .is-active{
   background: #1e78bf !important;
   color:#fff !important;
  }
.el-menu-item{
  font-size:20px;
}
}
</style>
<!--不折叠时的导航宽度-->