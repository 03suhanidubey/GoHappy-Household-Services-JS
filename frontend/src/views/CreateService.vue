<template>
    <NavBar />
    <div class="container">
        <div class="card">
            <div class="card-header">
                <h1>Create Service</h1>
            </div>
            <div class="card-body">
                <form @submit.prevent="create_service">

                    <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" v-model="form.name" class="form-control" id="name"
                            placeholder="Enter service name" required>
                    </div>

                    <div class="form-group">
                        <label for="baseprice">Base Price</label>
                        <input type="number" v-model="form.baseprice" class="form-control" id="baseprice"
                            placeholder="Enter base price" required>
                    </div>

                    <div class="form-group">
                        <label for="descr">Description</label>
                        <input type="text" v-model="form.descr" class="form-control" id="descr"
                            placeholder="Enter description of service" required>
                    </div>

                    <button type="submit" class="btn btn-primary mt-5">Create Service</button>
                 
                    </form>
                </div>
                    
            </div>
        </div>

</template>

<script>

import NavBar from '../components/NavBar.vue'
export default {
    components: {NavBar},
    name: 'CreateService',
    data() {
        return {
            form: {
                name: '',
                baseprice: '',
                descr: '',
            }
        };
    },
    methods: {
        async create_service() {
            const response = await fetch('http://localhost:5000/create_service', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                },
                body: JSON.stringify(this.form)
            });
            const data = await response.json();
            if (response.ok) {
                alert(data.message);
                this.$router.push('/admin_dashb');
            } else {
                alert(data.error);
            }
        }
    }
};

</script>