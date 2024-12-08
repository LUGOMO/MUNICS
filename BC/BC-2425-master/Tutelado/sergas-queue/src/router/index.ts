import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useWeb3Store } from '@/stores/web3' // Import your store

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/queue/:id',
      name: 'queue-detail',
      component: () => import('@/views/QueueView.vue'),
      props: true,
    },
    {
      path: '/historial',
      name: 'historial',
      component: () => import('@/views/HistoryView.vue'),
    },
    {
      path: '/patient',
      name: 'patient',
      component: () => import('@/views/patient/PatientHomeView.vue'),
      meta: { patientRole: 1 },
    },
    {
      path: '/specialist/patients',
      name: 'specialist',
      component: () => import('@/views/specialist/PatientsView.vue'),
      meta: { specialistRole: 1 },
    },
    {
      path: '/owner/queue/:id',
      name: 'queue-manager',
      component: () => import('@/views/owner/QueueManager.vue'),
      props: true,
      meta: { ownerRole: 1 },
    },
    {
      path: '/owner/especialists',
      name: 'specialists-manager',
      component: () => import('@/views/owner/SpecialistsManager.vue'),
      meta: { ownerRole: 1 },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const web3Store = useWeb3Store()
  const patientRole = (web3Store.cachedRoleCode >> 1) & 0b1
  const specialistRole = (web3Store.cachedRoleCode >> 2) & 0b1
  const ownerRole = (web3Store.cachedRoleCode >> 3) & 0b1
  console.log(web3Store.cachedRoleCode)
  if (to.matched.some(record => record.meta.patientRole) && !patientRole) {
    next({ name: 'home' })
  } else if (to.matched.some(record => record.meta.specialistRole) && !specialistRole) {
    next({ name: 'home' })
  } else if (to.matched.some(record => record.meta.ownerRole) && !ownerRole) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
