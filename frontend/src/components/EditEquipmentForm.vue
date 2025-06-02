<template>
 <v-card>
 <v-card-title>
 <v-text-field
 v-model="searchQuery"
 label="Поиск по серийному номеру/примечанию"
 prepend-icon="mdi-magnify"
 clearable
 @input="searchEquipment"
 ></v-text-field>
 </v-card-title>

 <v-card-text v-if="selectedEquipment">
 <v-select
 v-model="selectedEquipment.type_id"
 label="Тип оборудования"
 item-value="id"
 item-title="name"
 :disabled="!isEditing"
 ></v-select>

 <v-text-field
 v-model="selectedEquipment.serial_number"
 label="Серийный номер"
 :disabled="!isEditing"
 ></v-text-field>

 <v-textarea
 v-model="selectedEquipment.note"
 label="Примечание"
 :disabled="!isEditing"
 ></v-textarea>

 <v-card-actions>
 <v-btn
 v-if="!isEditing"
 @click="startEditing"
 color="primary"
 >
 Редактировать
 </v-btn>
 <v-btn
 v-else
 @click="saveEquipment"
 color="success"
 :loading="isSaving"
 >
 Сохранить
 </v-btn>
 <v-btn
 v-if="isEditing"
 @click="cancelEditing"
 color="warning"
 >
 Отменить
 </v-btn>
 <v-btn
 v-if="!isEditing"
 @click="deleteEquipment"
 color="error"
 >
 Удалить
 </v-btn>
 </v-card-actions>
 </v-card-text>
 </v-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { required } from '@vuelidate/validators'
import useVuelidate from '@vuelidate/core'
import { api } from '../api/api'



interface EquipmentType {
 id: number;
 name: string;
}

interface Equipment {
 id: number;
 type_id: number|null;
 serial_number: string;
 note?: string;
}

const equipmentTypes = ref<EquipmentType>()
const selectedEquipment = ref<Equipment>()
const searchQuery = ref('')
const isEditing = ref(false)
const isSaving = ref(false)

const form = reactive({
 type_id: null,
 serial_number: '',
 note: ''
})

const v$ = useVuelidate({
 type_id: { required },
 serial_number: { required }
}, form)


async function searchEquipment() {
 if (searchQuery.value) {
 try {
 const response = await api.get<Equipment>(`/equipment/${searchQuery.value}`)
 selectedEquipment.value = response.data
 } catch (error) {
 console.error('Ошибка при поиске оборудования:', error)
 }
 }
}

function startEditing() {
 isEditing.value = true
}

async function saveEquipment() {
    try {
        // Проверка валидации
        const isValid = await v$.value.$validate();
        if (!isValid) return;

        // Проверка существования selectedEquipment
        if (!selectedEquipment || !selectedEquipment.value) {
            console.error('selectedEquipment не определено или его значение отсутствует');
            return;
        }

        // Установка флага сохранения
        isSaving.value = true;

        // Безопасное обращение к id и значению selectedEquipment
        const equipmentId = selectedEquipment.value.id;
        const equipmentData = selectedEquipment.value;

        // Выполнение запроса
        await api.put(`/equipment/${equipmentId}`, equipmentData);

        // Сброс флагов
        isEditing.value = false;
        isSaving.value = false;
    } catch (error) {
        console.error('Ошибка при сохранении оборудования:', error);
    }
}

function cancelEditing() {
 isEditing.value = false
 selectedEquipment.value = { ...initialEquipment }
}

async function deleteEquipment() {
 try {
 // Проверка существования selectedEquipment
 if (!selectedEquipment || !selectedEquipment.value) {
 console.error('selectedEquipment не определено или его значение отсутствует');
 return;
 }

 // Проверка существования id
 if (!selectedEquipment.value.id) {
 console.error('id в selectedEquipment не определен');
 return;
 }

 // Выполнение удаления
 await api.delete(`/equipment/${selectedEquipment.value.id}`);

 // Сброс значения selectedEquipment
 selectedEquipment.value = undefined;
 } catch (error) {
 console.error('Ошибка при удалении оборудования:', error);
 }
}


const initialEquipment = computed(() => ({
 type_id: selectedEquipment.value?.type_id, 
 serial_number: selectedEquipment.value?.serial_number
}))
</script>