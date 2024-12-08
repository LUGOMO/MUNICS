<template>
  <div v-if="loading" class="text-center p-4">
    <SpinnerButton />
  </div>
  <div v-else class="grid gap-4 p-8 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
    <!-- Add Specialist Button -->
    <div
      class="flex flex-col items-center justify-center p-4 bg-accent text-white font-bold text-3xl rounded-xl shadow-lg cursor-pointer transition-transform hover:translate-y-[-5px] hover:shadow-xl"
      @click="showAddModal = true"
    >
      <span>+</span>
    </div>

    <!-- Specialist Items -->
    <div
      v-for="specialist in specialists"
      :key="specialist.address"
      class="flex flex-col items-center justify-center p-4 bg-primary text-white rounded-xl shadow-lg transition-transform hover:translate-y-[-5px] hover:shadow-xl cursor-pointer"
      @click="selectSpecialist(specialist)"
    >
      <h3 class="text-accentlight font-bold text-lg mb-2">{{ specialist.name }}</h3>
      <p class="text-sm break-words">{{ specialist.short_address }}</p>
    </div>

    <!-- Specialist Modal -->
    <SpecialistModal
      v-if="showModal"
      :visible="showModal"
      :specialist="selectedSpecialist"
      @close="closeModal"
      @remove="removeSpecialist"
    />

    <!-- Add Specialist Modal -->
    <AddSpecialistModal :visible="showAddModal" @close="closeAddModal" @add="addSpecialist" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import SpecialistModal from '@/components/owner/SpecialistModal.vue'
import AddSpecialistModal from '@/components/owner/AddSpecialistModal.vue'
import { type Specialist } from '@/models/specialist'
import { useWeb3Store } from '@/stores/web3'
import SpinnerButton from '@/components/SpinnerButton.vue'
const web3Store = useWeb3Store()

const specialists = ref<Specialist[]>([])

const loading = ref(true)
const showModal = ref(false)
const showAddModal = ref(false)
const selectedSpecialist = ref<Specialist | null>(null)

const addSpecialist = (specialist: Specialist) => {
  specialists.value = [...specialists.value, specialist]
}

const closeAddModal = () => {
  showAddModal.value = false
}

const selectSpecialist = (specialist: Specialist) => {
  selectedSpecialist.value = specialist
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedSpecialist.value = null
}

const removeSpecialist = () => {
  specialists.value = specialists.value.filter(
    (specialist) => specialist.address !== selectedSpecialist.value?.address,
  )
  closeModal()
}

onMounted(() => {
  web3Store
    .getSpecialists()
    .then((sps) => (specialists.value = sps))
    .finally(() => (loading.value = false))
})
</script>
