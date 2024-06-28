import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    //主界面
    {
      path: '/',
      name: 'home',
      component:()=>import('../views/HomeView/HomeView.vue'),
      children: [
        {
          path:'/linear_regression',
          name:'linear_regression',
          component:()=>import('../views/HomeView/AlgView/LinearRegressionView.vue')
        },
        {
          path:'/decision_tree_id3',
          name:'decision_tree_id3',
          component:()=>import('../views/HomeView/AlgView/DecisionTreeID3View.vue')
        },
        {
          path:'/apriori',
          name:'apriori',
          component:()=>import('../views/HomeView/AlgView/AprioriView.vue')
        },
        {
          path:'/k_means',
          name:'k_means',
          component:()=>import('../views/HomeView/AlgView/KMeansView.vue')
        },
        {
          path:'/dbscan',
          name:'dbscan',
          component:()=>import('../views/HomeView/AlgView/DBSCANView.vue')
        },
        {
          path:'/svm',
          name:'svm',
          component:()=>import('../views/HomeView/AlgView/SVMView.vue')
        },
        {
          path:'/knn',
          name:'knn',
          component:()=>import('../views/HomeView/AlgView/KNNView.vue')
        },
        {
          path:'/native_bayes',
          name:'native_bayes',
          component:()=>import('../views/HomeView/AlgView/NativeBayesView.vue')
        },
        {
          path:'pca',
          name:'pca',
          component:()=>import('../views/HomeView/AlgView/PCAView.vue')
        }

      ]
    },

    //测试界面
    {
      path: '/test',
      name: 'test',
      component:()=>import('../views/TestView.vue')
    },
  ]
})

export default router
