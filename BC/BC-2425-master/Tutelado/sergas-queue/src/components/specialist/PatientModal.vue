<template>
  <div
    v-if="props.visible"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    @click.self="emit('close')"
  >
    <div
      class="bg-white dark:bg-slate-800 p-6 rounded-lg shadow-xl w-100 flex flex-col items-center"
    >
      <h2 class="text-lg text-slate-600 dark:text-gray-300 font-bold mb-4">{{ props.patient?.name }}</h2>
      <p class="mb-4 break-all text-slate-500 dark:text-gray-200">{{ props.patient?.address }}</p>
      <p class="mb-4 text-slate-500 dark:text-gray-200">Prioridad: {{ props.patient?.priority }}</p>
      <p class="mb-4 text-slate-500 dark:text-gray-200">Razón: {{ props.patient?.reason }}</p>
      <div class="w-full mb-4">
        <ErrorContainer v-if="errorMessage" :errorMessage="errorMessage" />
      </div>
      <div class="flex space-x-4">
        <button
          class="bg-red-700 text-white py-2 px-4 rounded-lg shadow-lg hover:bg-red-800 transition"
          @click="handleRemoveClick"
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
      <div v-if="showDeletionReason" class="mt-4 w-full">
        <textarea
          v-model="deletionReason"
          type="text"
          placeholder="Razón de eliminación"
          class="w-full p-2 border border-gray-300 rounded-lg text-gray-800"
        />
        <div class="flex justify-center mt-2">
          <button
            class="bg-red-700 text-white py-2 px-4 rounded-lg shadow-lg hover:bg-red-800 transition"
            @click="removePatient"
          >
            Confirmar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type Patient } from '@/models/patient';
import WalletSpinner from '@/components/WalletSpinner.vue';
import { useWeb3Store } from '@/stores/web3';
import { ref } from 'vue';
import ErrorContainer from '@/components/ErrorContainer.vue';
const web3Store = useWeb3Store();

const props = defineProps<{
  visible: boolean;
  patient: Patient | null;
}>();

const loading = ref(false);
const errorMessage = ref<string | null>(null);
const showDeletionReason = ref(false);
const deletionReason = ref('');

const emit = defineEmits(['remove', 'close']);

const handleRemoveClick = () => {
  showDeletionReason.value = true;
};

const removePatient = async () => {
  try {
    if (props.patient && deletionReason.value) {
      loading.value = true;
      await web3Store.removePatient(props.patient, deletionReason.value);
      loading.value = false;
      emit('remove');
    } else {
      errorMessage.value = 'Por favor, ingrese una razón de eliminación del paciente de la cola';
    }
  } catch (error) {
    loading.value = false;
    errorMessage.value = (error as Error).message || 'Error desconocido';
  }
};
</script>
