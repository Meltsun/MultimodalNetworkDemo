<template>
    <div class="Layout">
      <div class="Menu">
      <leftmenu></leftmenu>
      </div>
    <!--右侧内容-->
      <div class="Content">
       <rightcontent></rightcontent>
      </div>
      <div class="Header">
       <top></top>
      </div>
    </div>
  </template>
  <script>
  import rightcontent from '../views/rightcontent.vue'
  import leftmenu from '../views/leftmenu.vue'
  import top from '../views/top.vue'

  export default {
    components:{
        rightcontent,
        leftmenu,
        top
    },
  }
  </script>
  
  <style lang="less" scoped>
    .Layout{
      .Header{
        position:fixed;
        height:70px;
        width:100%;
        top:0;
        background:#f2f2f2;
        line-height:50px;
      
      }
      .Menu{
        position:fixed;
        left:0;
        padding-top: 70px;
        top:0;
        bottom:0;
        width:200px;
        background:#ecf5ff;
      }
      .Content{
        top:0;
        padding-top: 70px;
        padding-left: 200px;
        background:#f2f2f2;
      }
    }
  </style>