<script setup>
import { ref, onBeforeMount } from "vue";
import axios from "axios";
import useProfileStore from "@/stores/profileStore";
import { storeToRefs } from "pinia";

const profileStore = useProfileStore();
const { role, userId } = storeToRefs(profileStore);

const reviews = ref({});
const events = ref({});
const loading = ref(false);

const reviewToAdd = ref({});
const reviewToEdit = ref({});

async function fetchReviews() {
  loading.value = true;

  const r = await axios.get("/api/reviews/");

  console.log(r.data);

  reviews.value = r.data;
  loading.value = false;
}

async function fetchEvents() {
  const r = await axios.get("/api/events/");

  console.log(r.data);

  events.value = r.data;
}

async function onReviewEditClick(review) {
  reviewToEdit.value = { ...review };
}

async function onUpdateReview() {
  await axios.put(`/api/reviews/${reviewToEdit.value.id}/`, {
    ...reviewToEdit.value,
  });

  await fetchReviews();
}

async function onReviewAdd() {
  console.log(reviewToAdd.value);

  await axios.post("/api/reviews/", reviewToAdd.value);

  await fetchReviews();
}

async function onRemoveClick(review) {
  await axios.delete(`/api/reviews/${review.id}/`);

  await fetchReviews();
}

onBeforeMount(async () => {
  await fetchReviews();
  await fetchEvents();
});
</script>


<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onReviewAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="reviewToAdd.event" required>
                <option v-for="event in events" :value="event.id">
                  {{ event.title }}
                </option>
              </select>
              <label>Мероприятие</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <input
                type="number"
                class="form-control"
                v-model="reviewToAdd.rating"
                min="1"
                max="5"
                step="0.5"
                required
              />
              <label>Оценка</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="reviewToAdd.comment"
                required
              />
              <label>Комментарий</label>
            </div>
          </div>

          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>
    </div>

    <div class="modal fade" id="editReviewModal" tabindex="-1">
      <div class="modal-dialog">
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
                  <select class="form-select" v-model="reviewToEdit.event">
                    <option v-for="event in events" :value="event.id">
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
                    type="number"
                    class="form-control"
                    v-model="reviewToEdit.rating"
                    min="1"
                    max="5"
                    step="0.5"
                  />

                  <label>Оценка</label>
                </div>
              </div>

              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="reviewToEdit.comment"
                  />

                  <label>Комментарий</label>
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
              @click="onUpdateReview"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading">Гружу...</div>

    <div>
      <div v-for="item in reviews" class="review-item">
        <div>Мероприятие: {{ item.event }}</div>

        <div>Оценка: {{ item.rating }}</div>

        <div>Комментарий: {{ item.comment }}</div>

        <div>Дата: {{ item.review_date }}</div>

        <button
          v-if="item.user === userId || role === 2"
          class="btn btn-success"
          @click="onReviewEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editReviewModal"
        >
          <i class="bi bi-pencil-fill"></i>
        </button>

        <button v-if="item.user === userId || role === 2" class="btn btn-danger" @click="onRemoveClick(item)">
          <i class="bi bi-x-circle"></i>
        </button>
      </div>
    </div>
  </div>
</template>


<style lang="scss" scoped>
.review-item {
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
</style>