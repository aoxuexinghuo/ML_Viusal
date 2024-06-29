<template>
  <el-container>
    <el-header height="70px" style="background-color: rgba(116,122,216,0.89);border-radius: 5px">
      <el-container>
        <el-aside
            style="text-align: left; font-size: 20px; font-weight: 1000; color: #271783"
            width="500px"
        >
          <div style="margin-top: 20px">
            <span>机器学习可视化平台</span>
          </div>
        </el-aside>
        <el-main style="text-align: right; font-size: 18px">
          <div>
            <span>{{ username }}</span>
            <el-dropdown>
              <el-icon style="margin-left: 8px; margin-top: 1px; font-size: 20px">
                <setting/>
              </el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-if="username === '未登录'">
                    <span @click="loginDialog = true">登录</span>
                  </el-dropdown-item>
                  <el-dropdown-item v-if="username === '未登录'">
                    <span @click="registerDialog = true">注册</span>
                  </el-dropdown-item>
                  <el-dropdown-item v-if="username !=='未登录'">
                    <span @click="get_user_info">个人信息</span>
                  </el-dropdown-item >
                  <el-dropdown-item v-if="username !=='未登录'">
                    <span @click="logout">退出登录</span>
                  </el-dropdown-item >
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-main>
      </el-container>
    </el-header>
    <el-container>
      <el-aside height="640px" width="220px">
        <el-container >
          <el-main>
            <el-menu>
              <el-menu-item index="1">
                <template #title>
                  <el-icon class="custom-icon">
                    <StarFilled/>
                  </el-icon>
                  <div @click="router.push('/linear_regression')" class="custom-text">线性回归</div>
                </template>
              </el-menu-item>
              <el-menu-item index="2">
                <template #title>
                  <el-icon class="custom-icon">
                    <StarFilled/>
                  </el-icon>
                  <div @click="router.push('/decision_tree_id3')" class="custom-text">决策树（ID3）</div>
                </template>
              </el-menu-item>
              <el-menu-item index="3">
                <template #title>
                  <el-icon class="custom-icon">
                    <StarFilled/>
                  </el-icon>
                  <div @click="router.push('/svm')" class="custom-text">支持向量机</div>
                </template>
              </el-menu-item>
              <el-menu-item index="4">
                <template #title>
                  <el-icon class="custom-icon">
                    <StarFilled/>
                  </el-icon>
                  <div @click="router.push('/native_bayes')" class="custom-text">朴素贝叶斯</div>
                </template>
              </el-menu-item>
              <el-menu-item index="5">
                <template #title>
                  <el-icon class="custom-icon">
                    <StarFilled/>
                  </el-icon>
                  <div @click="router.push('/knn')" class="custom-text">K 最近邻</div>
                </template>
              </el-menu-item>
              <el-menu-item index="6">
                <template #title>
                  <el-icon class="custom-icon">
                    <Grid/>
                  </el-icon>
                  <div @click="router.push('/k_means')" class="custom-text">K means</div>
                </template>
              </el-menu-item>
              <el-menu-item index="7">
                <template #title>
                  <el-icon class="custom-icon">
                    <Grid/>
                  </el-icon>
                  <div @click="router.push('/dbscan')" class="custom-text">DBScan</div>
                </template>
              </el-menu-item>
              <el-menu-item index="8">
                <template #title>
                  <el-icon class="custom-icon">
                    <Grid/>
                  </el-icon>
                  <div @click="router.push('/pca')" class="custom-text">PCA</div>
                </template>
              </el-menu-item>
              <el-menu-item index="9">
                <template #title>
                  <el-icon class="custom-icon">
                    <Grid/>
                  </el-icon>
                  <div @click="router.push('/apriori')" class="custom-text">Apriori</div>
                </template>
              </el-menu-item>
            </el-menu>
          </el-main>
        </el-container>
      </el-aside>
      <el-main height="605px">
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>

<!-- 交互式组件 -->
  <el-dialog
      v-model="loginDialog"
      align-center
      style="text-align: center"
      title="登录"
      width="350"
  >
    <el-form ref="userLoginForm" :model="user_login" :rules="rules">
      <el-form-item prop="username">
        <el-input
            v-model="user_login.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
        ></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
            v-model="user_login.password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
            size="large"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button autocomplete="off" size="default" type="primary" @click="login">登录</el-button>
        <el-button autocomplete="off" style="position: absolute;right: 0" type="warning"
                   @click="loginDialog=false">返回
        </el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog
      v-model="registerDialog"
      align-center
      style="text-align: center"
      title="注册"
      width="350"
  >
    <el-form ref="userRegisterForm" :model="user_register" :rules="rules">
      <el-form-item prop="username">
        <el-input
            v-model="user_register.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
        ></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
            v-model="user_register.password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
            size="large"
        ></el-input>
      </el-form-item>
      <el-form-item prop="email">
        <el-input
            v-model="user_register.email"
            placeholder="请输入邮箱"
            prefix-icon="Message"
            size="large"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button autocomplete="off" size="default" type="primary" @click="register">注册</el-button>
        <el-button autocomplete="off" style="position: absolute;right: 0" type="warning"
                   @click="registerDialog=false">返回
        </el-button>
      </el-form-item>
    </el-form>

  </el-dialog>
  <el-drawer v-model="user_info_drawer" title="个人信息">
    <el-descriptions :items="user_info" column="1" border>
      <el-descriptions-item label="用户名：">{{ user_info.username }}</el-descriptions-item>
      <el-descriptions-item label="邮箱：">{{ user_info.email }}</el-descriptions-item>
      <el-descriptions-item label="注册日期：">{{ user_info.register_date }}
      </el-descriptions-item>
    </el-descriptions>
  </el-drawer>
</template>

<script>

export default {
  name: "home_view",
  data() {
    return {
      username: localStorage.getItem("username")? JSON.parse(localStorage.getItem("username"))
          : '未登录',
      loginDialog: false,
      registerDialog: false,
      user_info_drawer: false,
      user_login: {
        username: null,
        password: null,
      },
      user_register: {
        username: null,
        password: null,
        email: null,
      },
      user_info:{
        username: null,
        email: null,
        register_date: null,
      },
      rules: {
        username: [
          {required: true, message: "用户名不能为空", trigger: "blur"},
          {min: 2, max: 20, message: "长度在 2 到 20 个字符", trigger: "blur"}
        ],
        password: [
          {required: true, message: "密码不能为空", trigger: "blur"},
          {min: 5, max: 50, message: "长度在 5 到 50 个字符", trigger: "blur"}
        ],
        email: [
          {required: true, message: "邮箱不能为空", trigger: "blur"},
          {type: "email", message: "请输入正确的邮箱地址", trigger: "blur"}
        ],
      },
    };
  },
  created() {
  },
  methods: {
    login() {
      this.$refs["userLoginForm"].validate((valid) => {
        if (valid) {
          // 表单校验合法
          this.request.post("/login", this.user_login).then((res) => {
            if (res.status === 200) {
              localStorage.setItem("token", JSON.stringify(res.data.access));
              localStorage.setItem("username", JSON.stringify(this.user_login.username));
              this.username = this.user_login.username;
              if (this.user_login.type === "admin") {
                this.$router.push("/admin");
              }
              this.$message.success(res.data.message);
              this.loginDialog = false;
            } else {
              this.$message.error(res.message);
            }
          }).catch(error => {
            this.$message.error(error.response.data.message);
          });
        }
      });
    },
    register() {
      this.$refs["userRegisterForm"].validate((valid) => {
        if (valid) {
          // 表单校验合法
          this.request.post("/register", this.user_register).then((res) => {
            if (res.status === 200) {
              this.$message.success(res.data.message);
              this.registerDialog = false;
            } else {
              this.$message.error(res.message);
            }
          }).catch(error => {
            this.$message.error(error.response.data.message);
          });
        }
      });
    },
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      this.$message.success("退出成功");
      this.username = '未登录';
      },
    get_user_info() {
      this.request.get("/user_info").then((res) => {
        if (res.status === 200) {
          this.user_info = res.data;
          this.user_info_drawer = true;
        } else {
          this.$message.error(res.message);
        }
      }).catch(error => {
        this.$message.error(error.response.data.message);
      });
    },
  }
};
</script>

<script setup>
// eslint-disable-next-line no-unused-vars
import { Grid, Setting, StarFilled } from '@element-plus/icons-vue'
import router from "@/router";

</script>

<style>
.custom-icon {
  font-size: 15px;
  margin-right: 8px;
}

.custom-text {
  font-size: 15px;
}
</style>
