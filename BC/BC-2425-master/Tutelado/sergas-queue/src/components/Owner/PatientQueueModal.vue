<template>
  <div
    v-if="isVisible"
    class="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50"
    @click.self="closeModal"
  >
    <div
      class="bg-white dark:bg-slate-800 p-6 rounded-lg shadow-xl flex flex-col items-center mx-3"
    >
      <h2 class="text-lg text-slate-600 dark:text-gray-300 font-bold mb-4">
        Manejar paciente
      </h2>
      <p class="mb-4 break-all max-w-80 text-slate-500 dark:text-gray-200">
        {{ patient?.name }}
      </p>
      <h3
        class="text-md break-all max-w-80 text-slate-600 dark:text-gray-300 font-semibold mb-2"
      >
        Dirección: {{ props.patient?.address }}
      </h3>
      <p class="mb-4 break-all max-w-80 text-slate-500 dark:text-gray-200 text-center">
        Dirección anónima: {{ props.patient?.hashed_address }}
      </p>
      <p class="mb-4 break-all max-w-80 text-slate-500 dark:text-gray-200">
        Prioridad: {{ props.patient?.priority }}
      </p>
      <p class="mb-4 break-all max-w-80 text-slate-500 dark:text-gray-200">
        Razón: {{ props.patient?.reason }}
      </p>
      <textarea
        v-model="reason"
        placeholder="Escriba una razón para la operación"
        class="w-full p-2 border border-gray-300 rounded-lg text-gray-800 mb-4"
      ></textarea>
      <div class="w-full mb-4">
        <ErrorContainer v-if="showErrorMessage" :errorMessage="errorMessage" />
      </div>
      <div class="flex space-x-4 mb-4">
        <button
          class="bg-red-700 text-white py-3 px-4 rounded-lg shadow-lg hover:bg-red-800 transition"
          @click="removePatient"
          :disabled="loading"
        >
          <span>Quitar de la cola</span>
        </button>
        <button
          class="bg-gray-600 text-white py-3 px-4 rounded-lg shadow-lg hover:bg-gray-400 transition"
          @click="closeModal"
        >
          Cerrar
        </button>
      </div>
      <div class="grid grid-cols-2 gap-x-2 gap-y-3 w-80">
        <button
          class="bg-yellow-600 text-white py-3 px-4 rounded-lg shadow-lg hover:bg-yellow-700 transition"
          @click="attendPatient"
          :disabled="loading"
        >
          <span>Atender</span>
        </button>
        <button
          class="bg-purple-600 text-white py-3 px-4 rounded-lg shadow-lg hover:bg-purple-700 transition"
          @click="derivePatient"
          :disabled="loading"
        >
          <span>Derivar</span>
        </button>
        <input
          v-model="newPosition"
          type="number"
          placeholder="Nueva posición"
          class="w-full p-2 border border-gray-300 rounded-lg text-gray-800"
        />
        <button
          class="bg-green-600 text-white py-3 px-4 rounded-lg shadow-lg hover:bg-green-700 transition"
          @click="movePosition"
          :disabled="loading"
        >
          <span>Mover posición</span>
        </button>
        <div
          v-if="movePositionEmpty"
          class="flex items-center gap-2 justify-center col-span-2"
        >
          <ErrorContainer :errorMessage="`Introduzca una nueva posición`" />
        </div>
        <select
          v-model="newPriority"
          class="w-full p-2 border border-gray-300 rounded-lg text-gray-800"
        >
          <option
            v-for="priority in filteredPriorities"
            :key="priority"
            :value="priority"
          >
            {{ priority }}
          </option>
        </select>
        <button
          class="bg-blue-600 text-white px-4 py-3 rounded-lg shadow-lg hover:bg-blue-700 transition"
          @click="changePriority"
          :disabled="loading"
        >
          <span>Cambiar prioridad</span>
        </button>
        <div v-if="changePriorityEmpty" class="flex items-center gap-2 justify-center col-span-2">
          <ErrorContainer :errorMessage="`Introduzca una nueva prioridad`"
        />
        </div>
      </div>
      <div class="w-full m-2 text-center">
        <WalletSpinner v-if="loading" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, computed } from 'vue';
import { type Patient } from '@/models/patient';
import ErrorContainer from '@/components/ErrorContainer.vue';
import WalletSpinner from '@/components/WalletSpinner.vue';
import { useWeb3Store } from '@/stores/web3'

const web3Store = useWeb3Store()
const props = defineProps<{
  patient: Patient | null;
}>();

const filteredPriorities = computed(() => {
  return [1, 2, 3].filter(priority => priority != props.patient?.priority);
});

const emit = defineEmits(['remove', 'update', 'close']);

const isVisible = ref(true);
const reason = ref('');
const showErrorMessage = ref(false);
const movePositionEmpty = ref(false);
const changePriorityEmpty = ref(false);
const errorMessage = ref('');
const loading = ref(false);
const newPriority = ref<number>();
const newPosition = ref<number>();

const patient = props.patient || null;

const closeModal = () => {
  isVisible.value = false;
  emit('close');
};

const check = (patient: Patient | null, move: boolean = false, prio: boolean = false) => {
  if (!reason.value || (patient == null)) {
    showErrorMessage.value = true;
    if (move) {
      movePositionEmpty.value = true;
    }
    if (prio) {
      changePriorityEmpty.value = true;
    }
    errorMessage.value = 'Por favor indique una razón de la operación';
    return false;
  }
  showErrorMessage.value = false;
  movePositionEmpty.value = false;
  changePriorityEmpty.value = false;
  return true;
}

const removePatient = () => {
  if (check(patient)) {
    loading.value = true;
    web3Store.removePatient(patient!, reason.value)
      .then(() => {
        emit('remove', patient)
        closeModal()
      }).catch((error) => {
        loading.value = false;
        errorMessage.value = error.message;
        showErrorMessage.value = true;
      });
  }
}

const changePriority = () => {
  if (check(patient, false, true)) {
    loading.value = true;
    web3Store.changePatientPriority(patient!, newPriority.value || 0, reason.value)
      .then(() => {
        emit('remove', patient)
        closeModal()
      }).catch((error) => {
        loading.value = false;
        errorMessage.value = error.message;
        showErrorMessage.value = true;
      });
  }
}

const movePosition = () => {
  if (check(patient, true, false)) {
    loading.value = true;
    web3Store.movePatientInQueue(patient!, (newPosition.value ?? 0) -1, reason.value)
      .then(() => {
        emit('update', patient)
        closeModal()
      }).catch((error) => {
        loading.value = false;
        errorMessage.value = error.message;
        showErrorMessage.value = true;
      });
  }
}

const attendPatient = () => {
  if (check(patient)) {
    loading.value = true;
    web3Store.attendPatient(patient!, reason.value)
      .then(() => {
        emit('remove', patient)
        closeModal()
      }).catch((error) => {
        loading.value = false;
        errorMessage.value = error.message;
        showErrorMessage.value = true;
      });
  }
}

const derivePatient = () => {
  if (check(patient)) {
    loading.value = true;
    web3Store.derivePatient(patient!, reason.value)
      .then(() => {
        emit('remove', patient)
      }).catch((error) => {
        loading.value = false;
        errorMessage.value = error.message;
        showErrorMessage.value = true;
      });
  }
}
</script>
