import { createRouter, createWebHistory } from 'vue-router'
import LocationsView from '../views/LocationsView.vue'
import EventsView from '../views/EventsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "LocationsView",
      component: LocationsView
    },
    {
      path: "/events",
      name: "EventsView",
      component: EventsView
    }
  ],
})

export default router
