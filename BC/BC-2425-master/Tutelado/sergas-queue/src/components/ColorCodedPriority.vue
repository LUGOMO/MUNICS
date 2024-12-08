<template>
  <span
    class="text-lg px-2 rounded-lg inline-block mx-2 font-bold"
    :class="{
      'bg-ownred': priority == 1,
      'bg-ownorange': priority == 2,
      'bg-tertiary': priority == 3,
    }"
  >{{ priority }}</span>
</template>

<script lang="ts">
export default {
  name: 'ColorCodedPriority',
  props: {
    priority: {
      type: Number,
      required: true
    }
  }
}
</script>