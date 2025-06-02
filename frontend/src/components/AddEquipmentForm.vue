<template>
  <v-form @submit.prevent="addEquipment">
    <v-select
      v-model="form.type_id"
      :items="equipmentTypes"
      label="Тип оборудования"
      item-value="id"
      item-title="name"
    ></v-select>

    <v-textarea
      v-model="form.serial_numbers"
      label="Серийные номера"
    ></v-textarea>

    <v-textarea
      v-model="form.note"
      label="Примечание"
    ></v-textarea>

    <v-btn type="submit" color="primary">Добавить</v-btn>
  </v-form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { required, minLength } from '@vuelidate/validators'
import useVuelidate from '@vuelidate/core';
import { api } from '../api/api'


interface EquipmentType {
  id: number;
  name: string;
}

interface EquipmentForm {
  type_id: number | null;
  serial_numbers: string;
  note?: string;
}

const equipmentTypes = ref<EquipmentType[]>([])
const form = ref<EquipmentForm>({
  type_id: null,
  serial_numbers: '',
  note: ''
})

const v$ = useVuelidate({
  type_id: { required },
  serial_numbers: { required }
}, form)

async function fetchEquipmentTypes() {
  try {
    const response = await api.get<EquipmentType[]>('/equipment-type/')
    equipmentTypes.value = response.data
  } catch (error) {
    console.error('Ошибка при получении типов оборудования:', error)
  }
}

async function addEquipment() {
  try {
    const isValid = await v$.value.$validate()
    if (!isValid) return

    await api.post('/equipment/', form.value)
    // Очистка формы после успешного добавления
    form.value = {
      type_id: null,
      serial_numbers: '',
      note: ''
    }
  } catch (error) {
    console.error('Ошибка при добавлении оборудования:', error)
  }
}

fetchEquipmentTypes()
</script>
