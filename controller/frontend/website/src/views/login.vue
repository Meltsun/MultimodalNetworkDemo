<template>
      <div class="content">
          <div class="form-signin" id="login" name="login">
            <div class="signin-heading">
              <a>用户系统登录</a>
            </div>
            <el-form ref="form" :model="form" label-width="20%" style="margin-top: 40px;margin-left: 25px; width:320px">
          <el-form-item label="用户名:">
            <el-input v-model="form.username" clearable></el-input>
          </el-form-item>
          <el-form-item label="密  码:">
            <el-input v-model="form.password" type="password" show-password></el-input>
          </el-form-item>
        </el-form>
            <div class="reg">
              <el-button type="primary" @click="login" class="btn">登录</el-button>
              <span @click="register" class="aniu">还没有账户？ 前往注册</span>
            </div>
          </div>
      </div>
  </template>

  <script>

import axios from 'axios'
//import {loginapi} from '../api/api.js'

  export default {
    data () {
      return {
        form: {
          username: '',
          password: ''
        },
      }
    },



    methods: {
      login () {
        if (this.form.username === '') {
          this.$message.error('用户名不能为空')
        } else if (this.form.password === '') {
          this.$message.error('密码不能为空')
        } else {
         axios.post("/user/login/",this.form).then(res=>{
           //loginapi(this.form).then(res=>{
            console.log(res);
            if (res.status ===200){
              this.$message({message:"登录成功",type:"success"});
              this.$router.push("/layout");
            }
            else{
              this.$message.error("账号密码不正确");
            }
          })
         
        }
      },
      register () {
        this.$router.push('/register')
      }
    }
  }
  </script>
  
  <style scoped>
  
    .content{
    position: absolute;
    margin-left:400px;
    margin-top:220px;
    width: 400px;
    height: 330px;
    background: #f1f1f1;
  }
    #login {
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
    color: #f1f1f1;
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
    #login {
       margin: 0 auto;
       height: 100%;
     }
     .btn {
    display: block;
    float: left;
    font-weight: normal;
    font-size: large;
    font-family: "Microsoft yahei";
    margin: 0 0 0 50px;
    background-color: #005bac;
    width: 100px;
    height: 40px;
    line-height: 10px;
    border-color: #005bac;
    }
    .aniu{
      margin-top: 40px;
      margin-left: 15px;
    }
  </style>
