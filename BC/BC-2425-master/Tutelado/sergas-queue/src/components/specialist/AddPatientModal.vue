<template>
  <div v-if="visible" 
  class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
  @click.self="emit('close')"
  >
    <div class="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 w-full max-w-md">
      <h2 class="text-xl font-bold text-primary dark:text-white mb-4">Añadir nuevo paciente</h2>
      <form @submit.prevent="submitPatient">
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
            placeholder="Nombre del paciente"
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
            placeholder="Dirección de la cartera del paciente"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent text-gray-800"
            required
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-primary dark:text-gray-200 mb-2">
            Razón
          </label>
          <textarea
            v-model="reason"
            type="text"
            placeholder="Escriba la razón de la inserción en la lista de espera"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent text-gray-800"
            required
          />
        </div>

        <!-- Priority Selector -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-primary dark:text-gray-200 mb-2">
            Prioridad
          </label>
          <select
            v-model="priority"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent text-gray-800"
          >
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
          </select>
        </div>

        <!-- Buttons -->
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            class="px-4 py-2 text-sm font-medium bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400"
            @click="closedWillingly = true; close()"
          >
            Cerrar
          </button>
          <button
            type="submit"
            class="px-4 py-2 text-sm font-medium bg-accent text-white rounded-lg hover:bg-accentshadow"
            :disabled="loading"
          >
            <WalletSpinner v-if="loading" />
            <span v-else>Añadir paciente</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { type Patient } from '@/models/patient'
import { useWeb3Store } from '@/stores/web3'
import ErrorContainer from '@/components/ErrorContainer.vue'
import WalletSpinner from '@/components/WalletSpinner.vue'
import { shortenAddress } from '@/utils'

const web3Store = useWeb3Store()
defineProps<{
  visible: boolean
}>()

const emit = defineEmits(['close', 'add'])

// Form fields
const name = ref('')
const address = ref('')
const priority = ref(null)
const reason = ref('')
const errorMessage = ref<string | null>(null)
const loading = ref(false)
const closedWillingly = ref(false)

// Methods
const close = () => {
  emit('close')
  clearForm()
}

const clearForm = () => {
  name.value = ''
  address.value = ''
  priority.value = null
  errorMessage.value = null
}

const submitPatient = async () => {
  errorMessage.value = null // Reset the error message
  if (name.value.trim() && address.value.trim()) {
    try {
      loading.value = true
      const newPatient: Patient = {
        address: address.value,
        name: name.value,
        priority: priority.value || 0,
        hashed_address: '',
        short_address: shortenAddress(address.value),
        specialist: '',
        reason: reason.value,
      }
      await web3Store.addPatient(newPatient, reason.value)
      loading.value = false
      emit('add', newPatient)
      if (!closedWillingly.value) close()
      else closedWillingly.value = false
    } catch (error) {
      loading.value = false
      errorMessage.value = (error as Error).message || 'An unknown error occurred'
    }
  } else {
    errorMessage.value = 'Both name and address are required.'
  }
}
</script>
