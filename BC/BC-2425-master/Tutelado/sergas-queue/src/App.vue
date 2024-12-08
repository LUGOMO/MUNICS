<script setup lang="ts">
import NavBar from './components/NavBar.vue'
import { useWalletStore } from './stores/wallet'

const walletStore = useWalletStore()
</script>

<template>
  <div class="w-full absolute left-0 top-0">
    <NavBar />
    <main v-if="walletStore.isMetaMask" class="w-full mt-20">
      <router-view />
    </main>
    <main v-else class="w-full flex-grow">
      <div class="flex flex-col items-center justify-center h-full mt-24">
        <span class="text-white font-bold text-2xl"
          >Esta aplicación requiere de MetaMask para sus funcionalidades</span
        >
      </div>
    </main>
  </div>
</template>
