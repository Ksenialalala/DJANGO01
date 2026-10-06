import { createRouter, createWebHistory } from 'vue-router'
import LocationsView from '../views/LocationsView.vue'
import EventsView from '../views/EventsView.vue'
import OrganizersView from '../views/OrganizersView.vue'
import ReviewsView from '../views/ReviewsView.vue'

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
    },
    {
      path: "/organizers",
      name: "OrganizersView",
      component: OrganizersView
    },
    {
      path: "/reviews",
      name: "ReviewsView",
      component: ReviewsView
    }
  ],
})

export default router
