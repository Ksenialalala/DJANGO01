<script setup>
import { ref, onBeforeMount } from "vue";
import axios from "axios";

const eventMaterials = ref({});
const events = ref({});
const loading = ref(false);

const eventMaterialToAdd = ref({});
const eventMaterialToEdit = ref({});

const eventMaterialsFileRef = ref();
const eventMaterialsEditFileRef = ref();

async function fetchEventMaterials() {
  loading.value = true;

  const r = await axios.get("/api/event-materials/");

  console.log(r.data);
  eventMaterials.value = r.data;

  loading.value = false;
}

async function fetchEvents() {
  const r = await axios.get("/api/events/");

  console.log(r.data);
  events.value = r.data;
}

async function onEventMaterialEditClick(eventMaterial) {
  eventMaterialToEdit.value = { ...eventMaterial };
}

async function onUpdateEventMaterial() {
  const formData = new FormData();

  formData.append("event", eventMaterialToEdit.value.event);
  formData.append("title", eventMaterialToEdit.value.title);
  formData.append("description", eventMaterialToEdit.value.description);

  if (eventMaterialToEdit.value.file instanceof File) {
    formData.append("file", eventMaterialToEdit.value.file);
  }

  await axios.put(
    `/api/event-materials/${eventMaterialToEdit.value.id}/`,
    formData
  );

  await fetchEventMaterials();
}

async function onEventMaterialAdd() {
  const formData = new FormData();

  formData.append("event", eventMaterialToAdd.value.event);
  formData.append("title", eventMaterialToAdd.value.title);
  formData.append("description", eventMaterialToAdd.value.description);
  formData.append("file", eventMaterialsFileRef.value.files[0]);

  await axios.post("/api/event-materials/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  await fetchEventMaterials();
}

function eventMaterialsFileChange() {
  eventMaterialToAdd.value.file = eventMaterialsFileRef.value.files[0];
}

function eventMaterialsEditFileChange() {
  eventMaterialToEdit.value.file = eventMaterialsEditFileRef.value.files[0];
}

async function onRemoveClick(eventMaterial) {
  await axios.delete(`/api/event-materials/${eventMaterial.id}/`);

  await fetchEventMaterials();
}

onBeforeMount(async () => {
  await fetchEventMaterials();
  await fetchEvents();
});
</script>


<template>
  <div class="container-fluid">
    <!-- Добавление материала -->

    <div class="p-2">
      <form @submit.prevent.stop="onEventMaterialAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <select
                class="form-select"
                v-model="eventMaterialToAdd.event"
                required
              >
                <option value="" disabled>Выберите мероприятие</option>

                <option
                  v-for="event in events"
                  :key="event.id"
                  :value="event.id"
                >
                  {{ event.title }}
                </option>
              </select>

              <label>Мероприятие</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="eventMaterialToAdd.title"
                required
              />

              <label>Название материала</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="eventMaterialToAdd.description"
                required
              />

              <label>Описание</label>
            </div>
          </div>

          <div class="col">
            <label class="form-label"> Файл </label>

            <input
              class="form-control"
              type="file"
              ref="eventMaterialsFileRef"
              @change="eventMaterialsFileChange"
              required
            />
          </div>

          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>
    </div>

    <!-- Модальное окно редактирования -->

    <div class="modal fade" id="editEventMaterialModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать материал</h1>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>

          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <select
                    class="form-select"
                    v-model="eventMaterialToEdit.event"
                  >
                    <option
                      v-for="event in events"
                      :key="event.id"
                      :value="event.id"
                    >
                      {{ event.title }}
                    </option>
                  </select>

                  <label>Мероприятие</label>
                </div>
              </div>
            </div>

            <div class="row mt-2">
              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="eventMaterialToEdit.title"
                  />

                  <label>Название материала</label>
                </div>
              </div>
            </div>

            <div class="row mt-2">
              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="eventMaterialToEdit.description"
                  />

                  <label>Описание</label>
                </div>
              </div>
            </div>

            <div class="row mt-2">
              <div class="col">
                <label class="form-label"> Новый файл </label>

                <input
                  class="form-control"
                  type="file"
                  ref="eventMaterialsEditFileRef"
                  @change="eventMaterialsEditFileChange"
                />
              </div>
            </div>

            <div v-if="eventMaterialToEdit.file" class="mt-2">
              <a :href="eventMaterialToEdit.file" target="_blank">
                Открыть текущий файл
              </a>
            </div>
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Закрыть
            </button>

            <button
              type="button"
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="onUpdateEventMaterial"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Список материалов -->

    <div v-if="loading">Гружу...</div>

    <div>
      <div
        v-for="item in eventMaterials"
        :key="item.id"
        class="event-material-item"
      >
        <div>Мероприятие: {{ item.event }}</div>

        <div>
          {{ item.title }}
        </div>

        <div>
          {{ item.description }}
        </div>

        <div v-if="item.file">
          <a :href="item.file" target="_blank"> Открыть файл </a>
        </div>

        <button
          class="btn btn-success"
          @click="onEventMaterialEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editEventMaterialModal"
        >
          <i class="bi bi-pencil-fill"></i>
        </button>

        <button class="btn btn-danger" @click="onRemoveClick(item)">
          <i class="bi bi-x-circle"></i>
        </button>
      </div>
    </div>
  </div>
</template>


<style lang="scss" scoped>
.event-material-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;

  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto auto auto;

  align-content: center;
  align-items: center;

  gap: 16px;
}
</style>