<template>
  <div class="bg">
    <div class="form-signin" id="register" name="register">
          <div class="signin-heading">
            <a>用户系统注册</a>
          </div>
          <el-form ref="form" :model="form" label-width="20%" style="margin-top: 40px;margin-left: 25px; width:300px">
          <el-form-item label="用户名:">
            <el-input v-model="form.username" clearable></el-input>
          </el-form-item>
          <el-form-item label="密  码:">
            <el-input v-model="form.password" type="password" show-password></el-input>
          </el-form-item>
        </el-form>
          <div class="reg">
            <el-button type="primary" @click="register" class="btn">注册</el-button>
          </div>
        </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      form: {
        username: '',
        password: ''
      },
      isnull: false
    }
  },

  methods: {
    register () {
      if (this.form.username === '') {
        this.$message.error('用户名不能为空')
      } else if (this.form.password === '') {
        this.$message.error('密码不能为空')
      } else {
        axios.post("/user/register/".this.form).then(res => {
          if (res.data.code === 0) {
            this.$alert('是否返回登录页面', '注册成功', {
              confirmButtonText: '确定',
              callback: action => {
                this.$router.push('/login')
              }
            })
          } else if (res.data.code === 4001) {
            this.$alert('用户名已存在', '注册失败', {
              confirmButtonText: '确定',
              callback: action => {
                this.form.username = ''
                this.form.password = ''
              }
            })
          } else {
            console.log(res)
          }
        }).catch(err => {
          console.log('操作失败' + err)
        })
      }
    }
  }
}
</script>

<style scoped>
  .bg{
    position: absolute;
    margin-left:400px;
    margin-top:220px;
    width: 400px;
    background: #f1f1f1;
  }
  #register {
     margin: 0 auto;
     height: 100%;
   }
  .signin-heading {
    text-align: left;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    height: 80px;
    line-height: 60px;
    width:400px;
    background: #005bac;
    font-size: 18px;
    color: #525252;
    font-weight: normal;
  }
  .signin-heading a {
    line-height: 80px;
    font-size: 22px;
    color: #fff;
    padding: 4px 4px 0 30px;
    display: block;
    width: auto;
    float: left;
  }
  .btn {
    display: block;
    font-weight: normal;
    font-size: large;
    font-family: "Microsoft yahei";
    background-color: #005bac;
    width: 200px;
    height: 40px;
    line-height: 10px;
    border-color: #005bac;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0 ;
    margin: auto ;
  }
   .reg{
     margin-top: 50px;
     margin-bottom: 50px;
     height: 40px;
  }
</style>