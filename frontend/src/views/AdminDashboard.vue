<template>
    <NavBar />
    <div class="container mt-3">

        <h2>Admin Dashboard</h2>
                                              
        <div class = "row">
            <h3>All Services</h3>
            <div v-for="service in all_services" :key="service.id" class="col-md-3 mb-3"> 
                <div class="card" shadow-sm>
                    <div class="card-body">
                        <h5 class="card-title">{{service.name}}</h5>
                        <p class="card-text">Baseprice: {{service.baseprice}}</p>
                        <p class="card-text">Description: {{service.descr}}</p>
                    </div>
                    <div class = "card-footer"> 
                        <div class="btn-group">
                            <router-link :to="{name: 'edit_service', params: {id: service.id}}" class="btn btn-primary">Edit</router-link>
                            <button @click="delete_service(service.id)" class="btn btn-danger">Delete</button>
                        </div>
                    </div>
                </div>
            </div>          
        </div>

        <br>

        <div class = "row">
            <h3>All Professionals</h3>
            <div v-for="professional in all_professionals" :key="professional.id" class="col-md-3 mb-3"> 
                <div class="card" shadow-sm>
                    <div class="card-body">
                        <h5 class="card-title">{{professional.name}}</h5>
                        <p class="card-text">Service: {{professional.service}}</p>
                        <p class="card-text">Experience: {{professional.experience}} years</p>
                        <p class="card-text">Email: {{professional.email}}</p>
                        <p class="card-text">Pincode: {{professional.pincode}}</p>
                    </div>
                    <div class = "card-footer"> 
                        <div class="btn-group">
                            <button @click="delete_professional(professional.id)" class="btn btn-danger">Delete</button>
                        </div>
                    </div>
                </div>
            </div>          
        </div>

        <br>

        <div class = "row">
            <h3>All Customers</h3>
            <div v-for="customer in all_customers" :key="customer.id" class="col-md-3 mb-3"> 
                <div class="card" shadow-sm>
                    <div class="card-body">
                        <h5 class="card-title">{{customer.name}}</h5>
                        <p class="card-text">Email: {{customer.email}}</p>
                        <p class="card-text">Pincode: {{customer.pincode}}</p>
                    </div>
                    <div class = "card-footer"> 
                        <div class="btn-group">
                            <button @click="delete_customer(customer.id)" class="btn btn-danger">Delete</button>
                        </div>
                    </div>
                </div>
            </div>          
        </div>


        <h2 class="my-5">App Statistics</h2>
        <div class="row">

            <!-- <div class="col-md-6 mb-4">
                <div class="statistics mt-5">
                    <div class="stat-card card mb-3" v-for="(value, key) in stats" :key="key">
                        <div class="card-body">
                            <h5 class="card-title">{{ key }}</h5>
                            <p class="card-text">{{ value }}</p>
                        </div>
                    </div>
                </div>
            </div> -->

            <div class="col-md-6 mb-4">
                <div class="statistics mt-5">
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Group</th>
                                <th>Count</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(value, key) in stats" :key="key">
                                <td>{{ key }}</td>
                                <td>{{ value }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="col-md-6 mb-4 d-flex justify-content-center align-items-center">
                <div class="graph">
                    <img :src="graphSrc" style="height: 80%;" alt="Graph" class="img-fluid img-thumbnail" />
                </div>
            </div> 

        </div>

    </div>
    


</template>

<script>    

import NavBar from '../components/NavBar.vue'
export default {
    components: {NavBar},
    name: 'AdminDashboard',
    data() {
        return{
            all_services: [],
            all_professionals: [],
            all_customers: [],
            stats: {},
            graphSrc: ''
        }
    },
    mounted() {
        this.fetchServices();
        this.fetchProfessionals();  
        this.fetchCustomers();
        this.fetchStats();
        this.fetchGraph();
    },
    methods: {
        async fetchServices() {
            const response = await fetch('http://localhost:5000/admindash_services', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            })
            const data=await response.json();
            if(!response.ok){
                alert(data.error);
            }
            else{
                this.all_services=data;
            }
        },
        async delete_service(service_id) {
            const response = await fetch(`http://localhost:5000/edit_service/${service_id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            });
            const data=await response.json();
            if(!response.ok){
                alert(data.error);
            }
            else{
                alert(data.message);
                this.fetchServices();
            }
        },
        async fetchProfessionals() {
            const response = await fetch('http://localhost:5000/admindash_professionals', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            })
            const data=await response.json();
            if(!response.ok){
                alert(data.error);
            }
            else{
                this.all_professionals=data;
            }
        },
        async fetchCustomers() {
            const response = await fetch('http://localhost:5000/admindash_customers', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            })
            const data=await response.json();
            if(!response.ok){
                alert(data.error);
            }
            else{
                this.all_customers=data;
            }
        }, 

        async delete_professional(professional_id) {
            const response = await fetch(`http://localhost:5000/delete_prof/${professional_id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            });
            const data=await response.json();
            if(!response.ok){
                alert(data.error);
            }
            else{
                alert(data.message);
                this.fetchProfessionals();
            }
        },

        async delete_customer(customer_id) {
            const response = await fetch(`http://localhost:5000/delete_cust/${customer_id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            });
            const data=await response.json();
            if(!response.ok){
                alert(data.error);
            }
            else{
                alert(data.message);
                this.fetchCustomers();
            }
        },

        async fetchStats() {
            const response = await fetch('http://localhost:5000/admin/stats', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            });
            const data=await response.json();
            if(!response.ok){
                alert(data.error);
            }
            else{
                this.stats=data;
            }
        },

        async fetchGraph() {
            const response = await fetch('http://localhost:5000/admin/stats/graph', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            });
            // const data=await response.json();
            if(!response.ok){
                alert(data.error);
            }
            else{
                const blob = await response.blob();
                this.graphSrc = URL.createObjectURL(blob);
                }
            }
    }   
}

</script>