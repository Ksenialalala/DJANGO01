<script setup>
import { ref, onBeforeMount } from "vue";
import axios from "axios";

const organizers = ref({});
const loading = ref(false);

const organizerToAdd = ref({});
const organizerToEdit = ref({});

const organizersPictureRef = ref();
const organizerAddImageUrl = ref();
const organizersEditPictureRef = ref();

const selectedImage = ref();

async function fetchOrganizers() {
  loading.value = true;

  const r = await axios.get("/api/organizers/");

  console.log(r.data);

  organizers.value = r.data;
  loading.value = false;
}

async function onOrganizerEditClick(organizer) {
  organizerToEdit.value = { ...organizer };
}

async function onUpdateOrganizer() {
  const formData = new FormData();

  formData.append("name", organizerToEdit.value.name);
  formData.append("position", organizerToEdit.value.position);
  formData.append("phone", organizerToEdit.value.phone);
  formData.append("email", organizerToEdit.value.email);

  if (organizerToEdit.value.image instanceof File) {
    formData.append("image", organizerToEdit.value.image);
  }

  await axios.put(`/api/organizers/${organizerToEdit.value.id}/`, formData);

  await fetchOrganizers();
}

async function onOrganizerAdd() {
  console.log(organizerToAdd.value);

  const formData = new FormData();

  formData.append("name", organizerToAdd.value.name);
  formData.append("position", organizerToAdd.value.position);
  formData.append("phone", organizerToAdd.value.phone);
  formData.append("email", organizerToAdd.value.email);

  formData.append("image", organizersPictureRef.value.files[0]);

  await axios.post("/api/organizers/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  await fetchOrganizers();
}

async function organizersAddPictureChange() {
  organizerAddImageUrl.value = URL.createObjectURL(
    organizersPictureRef.value.files[0]
  );
}

function onImageClick(image) {
  selectedImage.value = image;
}

function organizersEditPictureChange() {
  organizerToEdit.value.image = organizersEditPictureRef.value.files[0];
}

function onImageChange(event) {
  organizerToAdd.value.image = event.target.files[0];
}

function onEditImageChange(event) {
  organizerToEdit.value.image = event.target.files[0];
}

async function onRemoveClick(organizer) {
  await axios.delete(`/api/organizers/${organizer.id}/`);

  await fetchOrganizers();
}

onBeforeMount(async () => {
  await fetchOrganizers();
});
</script>


<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onOrganizerAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="organizerToAdd.name"
                required
              />
              <label>Имя</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="organizerToAdd.position"
                required
              />
              <label>Должность</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="organizerToAdd.phone"
                required
              />
              <label>Телефон</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <input
                type="email"
                class="form-control"
                v-model="organizerToAdd.email"
                required
              />
              <label>Email</label>
            </div>
          </div>
        </div>

        <div class="row mt-2">
          <div class="col">
            <label class="form-label">Изображение</label>

            <input
              type="file"
              class="form-control"
              ref="organizersPictureRef"
              @change="organizersAddPictureChange"
            />
          </div>

          <div class="col-auto">
            <img :src="organizerAddImageUrl" style="max-height: 60px" alt="" />
          </div>

          <div class="col-auto d-flex align-items-end">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>
    </div>

    <div class="modal fade" id="editOrganizerModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать</h1>

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
                  <input
                    type="text"
                    class="form-control"
                    v-model="organizerToEdit.name"
                  />
                  <label>Имя</label>
                </div>
              </div>

              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="organizerToEdit.position"
                  />
                  <label>Должность</label>
                </div>
              </div>
            </div>

            <div class="row mt-2">
              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="organizerToEdit.phone"
                  />
                  <label>Телефон</label>
                </div>
              </div>

              <div class="col">
                <div class="form-floating">
                  <input
                    type="email"
                    class="form-control"
                    v-model="organizerToEdit.email"
                  />
                  <label>Email</label>
                </div>
              </div>
            </div>

            <div class="row mt-2">
              <div class="col">
                <label class="form-label"> Изображение </label>

                <input
                  type="file"
                  class="form-control"
                  ref="organizersEditPictureRef"
                  @change="organizersEditPictureChange"
                />
              </div>

              <div class="col">
                <label class="form-label"> Текущая картинка </label>

                <div v-if="organizerToEdit.image">
                  <img
                    :src="organizerToEdit.image"
                    style="max-height: 100px"
                    alt=""
                  />
                </div>
              </div>
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
              @click="onUpdateOrganizer"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imageModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Просмотр изображения</h1>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>

          <div class="modal-body text-center">
            <img :src="selectedImage" class="img-fluid" alt="" />
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading">Гружу...</div>

    <div>
      <div v-for="item in organizers" class="organizer-item">
        <div>
          <b>{{ item.name }}</b>
        </div>

        <div>Должность: {{ item.position }}</div>

        <div>Телефон: {{ item.phone }}</div>

        <div>Email: {{ item.email }}</div>

        <div v-show="item.image">
          <img
            :src="item.image"
            style="max-height: 60px; cursor: pointer"
            @click="onImageClick(item.image)"
            data-bs-toggle="modal"
            data-bs-target="#imageModal"
          />
        </div>

        <button
          class="btn btn-success"
          @click="onOrganizerEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editOrganizerModal"
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
.organizer-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;

  display: grid;
  grid-template-columns: 1fr auto auto;
  align-content: center;
  align-items: center;
  gap: 16px;
}

.organizer-image {
  max-width: 200px;
  max-height: 150px;
}
</style>