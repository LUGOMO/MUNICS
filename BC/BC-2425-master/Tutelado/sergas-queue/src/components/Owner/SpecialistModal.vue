<template>
  <div
    v-if="props.visible"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
  >
    <div
      class="bg-white dark:bg-slate-800 p-6 rounded-lg shadow-xl w-80 flex flex-col items-center"
    >
      <h2 class="text-lg text-slate-600 dark:text-gray-300 font-bold mb-4">{{ props.specialist?.name }}</h2>
      <p class="mb-4 break-all text-slate-500 dark:text-gray-200">{{ props.specialist?.address }}</p>
      <div class="w-full mb-4">
        <ErrorContainer v-if="errorMessage" :errorMessage="errorMessage" />
      </div>
      <div class="flex space-x-4">
        <button
          class="bg-red-700 text-white py-2 px-4 rounded-lg shadow-lg hover:bg-red-800 transition"
          @click="removeSpecialist"
        >
          <WalletSpinner v-if="loading" />
          <span v-else>Quitar</span>
        </button>
        <button
          class="bg-gray-600 py-2 px-4 rounded-lg shadow-lg hover:bg-gray-400 transition"
          @click="emit('close')"
        >
          Cerrar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type Specialist } from '@/models/specialist';
import WalletSpinner from '@/components/WalletSpinner.vue';
import { useWeb3Store } from '@/stores/web3';
import { ref } from 'vue';
import ErrorContainer from '@/components/ErrorContainer.vue';
const web3Store = useWeb3Store();

const props = defineProps<{
  visible: boolean;
  specialist: Specialist | null;
}>();
const loading = ref(false);
const errorMessage = ref<string | null>(null);

const emit = defineEmits(['remove', 'close']);

const removeSpecialist = async () => {
  try {
    if (props.specialist) {
      loading.value = true;
      await web3Store.removeSpecialist(props.specialist);
      loading.value = false;
      emit('remove');
    }
  } catch (error) {
    loading.value = false;
    errorMessage.value = (error as Error).message || 'Error desconocido';
  }
};
</script>
