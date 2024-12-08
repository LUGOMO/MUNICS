<script setup lang="ts">
import type { Convenio } from '@/models/convenio';

const props = defineProps<{
  data: Convenio[];
}>();
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 font-sans">
    <h1 class="text-center text-2xl text-white mb-5">Convenios</h1>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="institution in props.data"
        :key="institution.id"
        class="bg-secondary rounded-lg p-4 shadow-md hover:shadow-lg"
      >
        <h2 class="text-xl text-accentlight mb-2">{{ institution.nombre }}</h2>
        <p><strong>Fecha de inicio:</strong> {{ institution.fecha_inicio }}</p>
        <p><strong>Especialidades:</strong></p>
        <ul class="list-disc pl-5">
          <li v-for="specialty in institution.especialidades" :key="specialty">
            {{ specialty }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
