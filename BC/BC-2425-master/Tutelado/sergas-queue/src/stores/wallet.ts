import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Maybe } from 'node_modules/@metamask/providers/dist/utils.mjs'
import { useWeb3Store } from "./web3";
import { shortenAddress } from "@/utils";

export const useWalletStore = defineStore('wallet', () => {
  const web3Store = useWeb3Store()
  // State
  const address = ref('');
  const accShort = computed(() =>
    address.value
      ? shortenAddress(address.value)
      : ''
  );
  // Derived state for whether the wallet is connected
  const isConnected = computed(() => !!address.value);
  const isMetaMask = ref(window.ethereum !== undefined);


  const clearWallet = () => {
    address.value = '';
  };

  // Utility to store wallet data in sessionStorage and state
  function storeWallet(accounts: Maybe<string[]>) {
    if (accounts && accounts.length > 0 && accounts[0]) {
      sessionStorage.setItem('walletAddress', accounts[0])
      address.value = accounts[0]
      web3Store.web3.defaultAccount = accounts[0]
      return
    }
    throw new Error('No accounts found')
  }

  // Check if the wallet is connected
  async function checkWallet() {
    if (!isMetaMask.value) return
    try {
      const accounts = await web3Store.web3.eth.getAccounts()
      storeWallet(accounts)
    } catch (error) {
      clearWallet()
      console.error(error)
      return false
    }
    return true
  }

  // Connect the wallet and ensure it's on the correct network
  async function connectWallet() {
    if (!isMetaMask.value) return
    try {
      const accounts = await web3Store.web3.eth.requestAccounts()
      storeWallet(accounts)
    } catch (error) {
      console.error('Error connecting to wallet:', error)
    }
  }

  // Expose state and actions
  return {
    address,
    accShort,
    isConnected,
    isMetaMask,
    storeWallet,
    clearWallet,
    checkWallet,
    connectWallet,
  };
});
