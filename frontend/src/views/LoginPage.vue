<template>
    <NavBar />
<div class="container">
        <div class="card">
            <div class="card-header">
                <h1>Login</h1>
            </div>
            <div class="card-body">
                <form @submit.prevent="login"> 
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" v-model="email" class="form-control" id="email"
                            placeholder="Enter your email">
                    </div>
                    <div class="form-group">
                        <label for="pswd">Password</label>
                        <input type="password" v-model="pswd" class="form-control" id="pswd"
                            placeholder="Enter your password">
                    </div>
                    <button type="submit" class="btn btn-primary mt-5">Login</button>
                </form>
            </div>
            </div>
        </div>
</template>

<script>

import NavBar from '../components/NavBar.vue'

export default {
    components: {
        NavBar
    },
    data() {
        return {
            email: '',
            pswd: ''
        }
    },
    methods: {
        async login() {
            const response = await fetch('http://localhost:5000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    pswd: this.pswd
                })
            })
            const data=await response.json()
            if(response.ok){
                alert(data.message)
                localStorage.setItem('access_token', data.access_token)
                this.$router.push('/')
            }
            else{
                alert(data.error)
            }
        }
    }
}
</script>