<template>
  <NavBar />

  <h1>WELCOME TO GOHAPPY HOUSEHOLD SERVICES</h1>

</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import NavBar from '../components/NavBar.vue'

export default {
  name: 'HomeView',
  components: {
    NavBar
  }
}
</script>
