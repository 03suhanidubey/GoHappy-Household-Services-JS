<template>
    <NavBar />
    <div class="container">
        <div class="card">
            <div class="card-header">
                <h1>Sign Up</h1>
            </div>
            <div class="card-body">
                <form @submit.prevent="signup">
                    <div class="form-group">
                        <label for="role">Role</label>
                        <select v-model="form.role" class="form-control" id="role" for="role" required>
                            <option value="customer">Customer</option>
                            <option value="professional">Professional</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" v-model="form.name" class="form-control" id="name"
                            placeholder="Enter your name" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" v-model="form.email" class="form-control" id="email"
                            placeholder="Enter your email" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" v-model="form.pswd" class="form-control" id="pswd"
                            placeholder="Enter your password" required>
                    </div>
                    <div class="form-group">
                        <label for="contactno">Contact No.</label>
                        <input type="number" v-model="form.contactno" class="form-control" id="contactno"
                            placeholder="Enter your contact number" required>
                    </div>
                    <div class="form-group">
                        <label for="address">Address</label>
                        <input type="text" v-model="form.address" class="form-control" id="address"
                            placeholder="Enter your address" required>
                    </div>
                    <div class="form-group">
                        <label for="pincode">Pincode</label>
                        <input type="number" v-model="form.pincode" class="form-control" id="pincode"
                            placeholder="Enter your pincode" required>
                    </div>
                    <div v-if="form.role === 'professional'">
                        <div class="form-group">
                            <label for="service">Service</label>
                            <select v-model="form.service" class="form-control" id="service" required>
                                <option v-for="service in services" :key="service" :value="service">
                                {{ service }}
                                </option>
                        </select>
                        </div>
                        <div class="form-group">
                            <label for="experience">Experience (in years)</label>
                            <input type="number" v-model="form.experience" class="form-control" id="experience" placeholder="Experience" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary mt-5">Sign Up</button>
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
    name: 'SignupPage',
    data() {
        return {
            form: {
                role: '',
                name: '',
                email: '',
                pswd: '',
                number: '',
                address: '',
                pincode: '',
                //professional specific
                service: '',
                experience: '',
            },
            services: []
        }
    },
    methods: {
        async signup() {
            console.log(this.form)
            const role=this.form.role
            const response=await fetch ('http://localhost:5000/signup', 
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.form)
                })
            const data=await response.json()
            if(response.ok){
                alert(data.message)
                this.$router.push('/login')
            }
            else{
                alert(data.error)
            }
        }, 
        async fetchServices() {
                const response = await fetch('http://localhost:5000/signup/get_services', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                const data = await response.json();
                if (response.ok) {
                    this.services = data;
                } else {
                    this.message = data.message;
                    this.messageClass = 'alert-danger';
                }
            } 
        },
        mounted() {
            this.fetchServices();
        }
    } 
</script>



