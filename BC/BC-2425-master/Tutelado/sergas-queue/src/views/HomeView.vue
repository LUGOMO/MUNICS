<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useWeb3Store } from '@/stores/web3';
import ErrorContainer from '@/components/ErrorContainer.vue';
import SpinnerButton from '@/components/SpinnerButton.vue';
import ConveniosData from '@/components/ConveniosData.vue';
import type { Convenio } from '@/models/convenio';

const web3Store = useWeb3Store();
const IPFS_GATEWAY = import.meta.env.VITE_IPFS_GATEWAY;
const loading = ref(false);

const queueName = ref('');
const queueLengths = ref<{ [priority: string]: number }>({ 1: 0, 2: 0, 3: 0 });
const specialistCount = ref(0);

const IPFSHash = ref('');
const IPFSUpdateErrorMessage = ref('');

const IPFSData = ref<Convenio[] | null>(null);
const IPFSViewErrorMessage = ref('');

const fetchData = async () => {
  const name = await web3Store.getQueueName();
  queueName.value = typeof name === 'string' ? name : '';

  queueLengths.value[1] = await web3Store.getQueueLength(1);
  queueLengths.value[2] = await web3Store.getQueueLength(2);
  queueLengths.value[3] = await web3Store.getQueueLength(3);

  specialistCount.value = (await web3Store.getSpecialists()).length;
  getIPFSHash();
};

const updateIPFSHash = async (hash: string) => {
  if (!hash) {
    IPFSUpdateErrorMessage.value = 'IPFS hash requerido';
    return;
  }
  try {
    loading.value = true;
    await web3Store.updateConveniosIPFSHash(hash);
    IPFSUpdateErrorMessage.value = '';
  } catch (error) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    IPFSUpdateErrorMessage.value = (error as any).message;
  } finally {
    loading.value = false;
  }
};

const getIPFSHash = async () => {
  IPFSHash.value = await web3Store.getConveniosIPFSHash();
};

const fetchIPFSData = async () => {
  if (!IPFSHash.value) {
    await getIPFSHash();
  }
  try {
    loading.value = true;
    const response = await fetch(`${IPFS_GATEWAY}${IPFSHash.value}`,{ "mode": "cors"})
    if (!response.ok) {
      throw new Error('Error al cargar datos desde IPFS');
    }
    IPFSData.value = await response.json();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  } catch (error) {
    IPFSViewErrorMessage.value = "Error al cargar datos desde IPFS";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="p-8">
    <!-- Queue Type -->
    <div class="text-center ">
      <h1 class="text-2xl font-semibold text-white mb-4 inline-block">
        Cola para:
      </h1>
      <h1 class="text-2xl font-bold text-accent mb-4 inline-block ml-2">
        {{ queueName }}
      </h1>
    </div>

    <!-- Priority Queue Lengths -->
    <div class="grid gap-4 sm:grid-cols-4">
      <div class="bg-ownred text-white p-4 rounded-lg shadow-md">
        <h2 class="font-bold text-xl">Prioridad 1</h2>
        <p class="text-lg">{{ queueLengths[1] }} paciente{{ queueLengths[1] == 1 ? '' : 's' }}</p>
      </div>
      <div class="bg-ownorange text-white p-4 rounded-lg shadow-md">
        <h2 class="font-bold text-xl">Prioridad 2</h2>
        <p class="text-lg">{{ queueLengths[2] }} paciente{{ queueLengths[2] == 1 ? '' : 's' }}</p>
      </div>
      <div class="bg-tertiary text-white p-4 rounded-lg shadow-md">
        <h2 class="font-bold text-xl">Prioridad 3</h2>
        <p class="text-lg">{{ queueLengths[3] }} paciente{{ queueLengths[3] == 1 ? '' : 's' }}</p>
      </div>
      <div class="bg-primary text-white p-4 rounded-lg shadow-md">
        <h2 class="font-bold text-xl">Especialistas</h2>
        <p class="text-lg">{{ specialistCount }} especialistas registrados</p>
      </div>
    </div>

    <!-- Centered text div in a rounded rectangle -->
    <div class="flex justify-center mt-8">
      <div class="bg-secondary text-white p-4 rounded-lg shadow-md max-w-lg w-full">
      <p class="text-lg text-center">
        Muchas operaciones son derivadas a convenios con seguros privados para agilizar las colas. Si se rechaza dicha derivación su posición en la cola se verá penalizada. Puede ver los seguros con los que trabajamos y sus especialidades.
      </p>
      </div>
    </div>

    <!-- "Convenios" Button -->
    <div class="text-center mt-8 place-items-center">
      <button 
      class="px-4 py-2 text-sm font-medium bg-accent text-white rounded-lg hover:bg-accentshadow"
      :class="{ 'cursor-pointer': !loading }"
      :disabled="loading"
      @click="fetchIPFSData"
      >
        <SpinnerButton v-if="loading" />
        <span v-else>Ver convenios</span>
      </button>
      <ErrorContainer class="max-w-prose m-2" :errorMessage="IPFSViewErrorMessage" />
    </div>

    <!-- IPFS Data Viewer -->
    <div v-if="IPFSData" class="mt-8">
      <ConveniosData :data="IPFSData" />
    </div>

    <!-- Update Convenios IPFS hash -->
    <div v-if="(web3Store.roleCode >> 3) & 0b1" class="text-center mt-8 flex flex-col place-items-center gap-2">
      <span class="text-md font-medium text-white">
        Actualizar convenios:
      </span>
      <input 
        type="text" 
        class="p-2 mx-10 rounded-lg max-w-screen-md w-full text-center text-black" 
        placeholder="IPFS hash" 
        v-model="IPFSHash"
        required
      />
      <ErrorContainer class="max-w-prose" :errorMessage="IPFSUpdateErrorMessage" />
      <button 
      class="px-4 py-2 text-sm font-medium bg-accent text-white rounded-lg hover:bg-accentshadow"
      :class="{ 'cursor-pointer': !loading }"
      @click="updateIPFSHash(IPFSHash)"
      :disabled="loading"
      >
        <SpinnerButton v-if="loading" />
        <span v-else>Confirmar</span>
      </button>
    </div> 

  </div>
</template>
