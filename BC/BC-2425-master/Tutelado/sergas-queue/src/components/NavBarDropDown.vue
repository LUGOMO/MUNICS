<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

defineProps<{
  name: string
  to: string
}>()

const isOpen = ref(false)
const priorities = [1, 2, 3]

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.dropdown-container')) {
    isOpen.value = false
  }
}

const handleSelection = () => {
  isOpen.value = false
}

onMounted(() => {
  document.addEventListener('click', closeDropdown)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', closeDropdown)
})
</script>

<template>
  <div class="dropdown-container w-full custom-lg:w-auto">
    <div class="relative inline-block w-full custom-lg:w-auto">
      <div>
        <button
          type="button"
          class="text-md font-medium leading-relaxed inline-block py-2 whitespace-nowrap text-white px-3 rounded-xl transition-colors duration-500 ease-in-out hover:bg-secondary w-full custom-lg:w-auto text-left"
          @click="toggleDropdown"
        >
          {{ name }}
        </button>
      </div>
      <div
        v-if="isOpen"
        class="absolute mt-2 w-56 max-w-[90vw] rounded-md shadow-lg bg-gray-200 ring-1 ring-black ring-opacity-5 z-50"
      >
        <div class="py-1">
          <router-link
            v-for="priority in priorities"
            :key="priority"
            :to="`${to}/${priority}`"
            class="block px-4 py-2 text-sm text-black font-medium hover:bg-tertiary"
            @click="handleSelection"
          >
            Prioridad {{ priority }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dropdown-container .absolute {
  left: 0;
  right: auto;
}
@media (min-width: 640px) {
  .dropdown-container .absolute {
    left: auto;
    right: 0;
  }
}
</style>
