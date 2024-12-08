<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import WalletConnect from './WalletConnect.vue'
import NavBarButton from './NavBarButton.vue'
import NavBarDropDown from './NavBarDropDown.vue'
import { useWeb3Store } from '@/stores/web3'

const name = import.meta.env.VITE_PROJECT_NAME
const web3Store = useWeb3Store()
const queue_name = ref('')

// Reactive State
const showMenu = ref(false)

// Methods
const toggleNavbar = () => {
  showMenu.value = !showMenu.value
}

onMounted(() => {
  web3Store.getQueueName().then((name) => {
    queue_name.value = typeof name === 'string' ? name : ''
  })
})
</script>

<template>
  <nav class="absolute flex-wrap w-full px-2 py-3 bg-primary mb-3 lg:shadow-none shadow-2xl z-40">
    <div class="px-4 mx-auto w-full inline-flex flex-wrap items-center z-40">
      <div class="inline-flex w-full custom-lg:w-auto px-4 place-content-between z-40">
        <router-link
          class="text-sm font-extrabold leading-relaxed inline-block py-2 whitespace-nowrap uppercase text-white px-3 rounded-xl items-center z-40"
          to="/"
        >
          {{ name }}
        </router-link>
        <span class="text-md font-semibold text-gray-200 pl-3 pr-0 flex items-center z-40">{{ queue_name }}</span>
        <button
          class="text-white cursor-pointer text-xl leading-none px-3 py-1 border border-solid border-transparent rounded bg-transparent block custom-lg:hidden outline-none focus:outline-none z-40"
          type="button"
          @click="toggleNavbar"
        >
          <font-awesome-icon :icon="['fas', 'bars']" />
        </button>
      </div>

      <!-- Middle portion -->
      <div
        class="custom-lg:flex flex-grow grid items-center px-4 py-2 w-full custom-lg:w-auto gap-2"
        :class="{ hidden: !showMenu }"
      >
        <NavBarButton
          v-if="(web3Store.roleCode >> 3) & 0b1"
          name="Especialistas"
          to="/owner/especialists"
        />
        <NavBarDropDown
          v-if="(web3Store.roleCode >> 3) & 0b1"
          name="Manejar colas ↓"
          to="/owner/queue"
        />

        <NavBarButton
          v-if="(web3Store.roleCode >> 2) & 0b1"
          name="Manejar pacientes"
          to="/specialist/patients"
        />

        <NavBarButton
          v-if="(web3Store.roleCode >> 1) & 0b1"
          name="Zona de pacientes"
          to="/patient"
        />
        <NavBarDropDown name="Cola pública ↓" to="/queue" />
        <NavBarButton name="Historiales" to="/historial" />
      </div>

      <!-- End portion -->
      <div :class="{ hidden: !showMenu }" class="custom-lg:flex w-full custom-lg:w-auto items-center px-4 py-2">
        <ul class="flex flex-col custom-lg:flex-row list-none ml-auto">
          <li class="nav-item">
            <WalletConnect />
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
