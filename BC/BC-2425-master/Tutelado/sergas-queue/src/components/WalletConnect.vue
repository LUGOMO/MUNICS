<script lang="ts" setup>
import { onMounted } from 'vue'
import { useWalletStore } from '@/stores/wallet'
import { useWeb3Store } from '@/stores/web3'

const walletStore = useWalletStore()
const web3 = useWeb3Store()

// On component mount, restore session data and check the connection/network
onMounted(() => {
  walletStore.checkWallet().then((res) => {
    if (res) {
      // walletStore.connectWallet()
      web3.setDefaultAccount(walletStore.address)
      web3.getRole()
    }
  })
  if (walletStore.isMetaMask) {
    window.ethereum.on('accountsChanged', (accounts) => {
      if ((accounts as string[]).length === 0) {
        walletStore.clearWallet()
      } else {
        walletStore.storeWallet(accounts as string[])
        web3.setDefaultAccount(walletStore.address)
        web3.getRole()
      }
    })
  }
})
</script>

<template>
  <div v-if="walletStore.isMetaMask">
    <!-- Connect Wallet Button -->
    <button
      :disabled="walletStore.isConnected"
      :class="walletStore.isConnected ? 'connected-animation' : 'hover-effect'"
      @click="walletStore.connectWallet()"
      class="relative inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary focus:outline-none transition-transform duration-300 ease-in-out float-right lg:float-none"
    >
      <span class="text-white font-bold">
        {{
          walletStore.isConnected ? `Cuenta conectada: ${walletStore.accShort}` : `Conectar Wallet`
        }}
      </span>
    </button>
    <!-- Force reload role button -->
    <!-- <button @click="web3.forceGetRole()" class="text-white font-bold pl-4">
      <font-awesome-icon :icon="['fas', 'rotate']" class="text-lg align-center justify-center" />
    </button> -->
  </div>
  <div v-else>
    <span class="text-white font-bold">MetaMask no detectado!</span>
  </div>
</template>

<style scoped>
/* Glow animation */
.connected-animation {
  animation: glow 10s infinite;
  border: 2px solid #34d399; /* Tailwind emerald-400 */
  box-shadow: 0 0 15px #34d399b3;
}

/* Glow effect */
@keyframes glow {
  0%,
  100% {
    box-shadow: 0 0 15px rgba(52, 211, 153, 0.7);
  }
  50% {
    box-shadow: 0 0 25px rgba(52, 211, 153, 1);
  }
}

/* Ensure content remains above ::before glare */
button > span {
  position: relative;
  z-index: 2;
}

/* Add hover grow animation for unconnected state */
button:hover:not([disabled]) {
  transition: transform 0.3s ease-in-out;
  transform: scale(1.05);
}
</style>
