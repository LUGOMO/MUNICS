<template>
  <div
    v-if="visible"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
    @click.self="emit('close')"
  >
    <div class="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 w-full max-w-md">
      <h2 class="text-xl font-bold text-primary dark:text-white mb-4">
        Añadir nuevo especialista
      </h2>
      <form @submit.prevent="submitSpecialist">
        <!-- Error Message -->
        <div class="w-full mb-4">
          <ErrorContainer v-if="errorMessage" :errorMessage="errorMessage" />
        </div>

        <!-- Name Input -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-primary dark:text-gray-200 mb-2">
            Nombre
          </label>
          <input
            v-model="name"
            type="text"
            placeholder="Nombre del especialista"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent text-gray-800"
            required
          />
        </div>

        <!-- Address Input -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-primary dark:text-gray-200 mb-2">
            Dirección de cartera
          </label>
          <input
            v-model="address"
            type="text"
            placeholder="Dirección de la cartera del especialista"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent text-gray-800"
            required
          />
        </div>

        <!-- Buttons -->
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            class="px-4 py-2 text-sm font-medium bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400"
            @click="close"
          >
            Cerrar
          </button>
          <button
            type="submit"
            class="px-4 py-2 text-sm font-medium bg-accent text-white rounded-lg hover:bg-accentshadow"
            :disabled="loading"
          >
            <WalletSpinner v-if="loading" />
            <span v-else>Añadir especialista</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { type Specialist } from '@/models/specialist';
import { useWeb3Store } from '@/stores/web3';
import ErrorContainer from '@/components/ErrorContainer.vue';
import WalletSpinner from '@/components/WalletSpinner.vue';

const web3Store = useWeb3Store();
defineProps<{
  visible: boolean;
}>();

const emit = defineEmits(['close', 'add']);

// Form fields
const name = ref('');
const address = ref('');
const errorMessage = ref<string | null>(null);
const loading = ref(false);

// Methods
const close = () => {
  emit('close');
  clearForm();
};

const clearForm = () => {
  name.value = '';
  address.value = '';
  errorMessage.value = null;
};

const submitSpecialist = async () => {
  errorMessage.value = null; // Reset the error message
  if (name.value.trim() && address.value.trim()) {
    try {
      loading.value = true;
      const newSpecialist: Specialist = {
        name: name.value,
        address: address.value,
        short_address: `${address.value.slice(0, 6)}...${address.value.slice(-4)}`,
      };
      await web3Store.addSpecialist(newSpecialist);
      loading.value = false;
      emit('add', newSpecialist);
      close();
    } catch (error) {
      loading.value = false;
      errorMessage.value = (error as Error).message || 'An unknown error occurred';
    }
  } else {
    errorMessage.value = 'Both name and address are required.';
  }
};
</script>
