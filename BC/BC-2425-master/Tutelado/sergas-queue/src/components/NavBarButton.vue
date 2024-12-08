<script setup lang="ts">
const props = defineProps<{
  name: string
  to: string
}>()
</script>

<template>
  <router-link
    :to="props.to"
    class="text-md font-medium leading-relaxed inline-block py-2 whitespace-nowrap text-white px-3 rounded-xl hover:secondary"
    active-class="bg-tertiary"
  >
    {{ props.name }}
  </router-link>
</template>
