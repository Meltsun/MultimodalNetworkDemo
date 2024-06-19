import axiosInstance from './index'

const axios = axiosInstance

// 登录认证
export const loginapi = (loginForm) => {
  return axios.post(
    `/user/login/`,
    loginForm
  )
}

// 注册
export const registerapi = (registerForm) => {
  return axios.post(
    `/user/register/`,
    registerForm
  )
}

