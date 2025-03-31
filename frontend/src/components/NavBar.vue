<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link> |
    <router-link to="/signup" v-if="!authed">Signup</router-link> |
    <router-link to="/login" v-if="!authed">Login</router-link>
    <a class="nav-link" href="/" v-if="authed" @click.prevent="logout">Logout</a> |
    <router-link to="/create_service" v-if="authed && role=='admin'">Create Service</router-link> |
    <router-link to="/admin_dashb" v-if="authed && role=='admin'">Admin Dashboard</router-link>
    <router-link to="/cust_dashb" v-if="authed && role=='customer'">Customer Dashboard</router-link>
    <router-link to="/profes_dashb" v-if="authed && role=='professional'">Professional Dashboard</router-link>

  </nav>
</template>

<script>
//import router from '@/router';

import userMixin from '../mixins/userMixin';
export default {
    name:'NavBar',
    mixins:[userMixin]
} 
</script>

<!-- <li v-if="authorized" class="nav-item">
  <a class="nav-link" href="#" @click="logout">Logout</a>
</li> -->
