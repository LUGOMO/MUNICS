import './assets/main.css'
// import "vue-connect-wallet/dist/style.css";

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import "./assets/style.css";

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faBars, faRotate } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faBars)
library.add(faRotate)

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(createPinia())
app.use(router)

app.mount('#app')
