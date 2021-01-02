# supermarket

## 项目依赖安装
```
npm install
```
### 项目启动
```
npm run dev
```
### 项目后台接口主配置
```
/src/main.js
```
### 项目路由配置
```
/src/router/index.js
```
### 项目各组件
```
/src/components/
```

## 注意几点
* elemntUI 已全局导入，在```/src/plugins```文件夹下
* 全局css文件在```/src/assets/css/global.css```, 注意每个组件的style样式中应声明***scoped*** 避免全局样式污染
* http方法已挂载，可通过this.$http方法进行网络请求

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
