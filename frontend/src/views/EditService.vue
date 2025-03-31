<template>
    <NavBar />
    <div class="container">
        <div class="card">
            <div class="card-header">
                <h1>Edit Service</h1>
            </div>
            <div class="card-body">
                <form @submit.prevent="edit_service">

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
                            placeholder="Enter descr of service" required>
                    </div>

                    <button type="submit" class="btn btn-primary mt-5">Edit Service</button>
                 
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
    created() {
        const service_id=this.$route.params.id;
        this.fetchService(service_id);
    },
    methods: {
        async fetchService(service_id) {
            const response = await fetch(`http://localhost:5000/edit_service/${service_id}`, {
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
                this.form={
                    name: data.name,
                    baseprice: data.baseprice,
                    descr: data.descr
                }
            }
        },
        async edit_service() {
            const service_id=this.$route.params.id;
            const response = await fetch(`http://localhost:5000/edit_service/${service_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                },
                body: JSON.stringify(this.form)
            });
            const data=await response.json();
            if(!response.ok){
                alert(data.error);
            }
            else{
                alert(data.message);
                this.$router.push('/admin_dashb');
            }
        }
    }
};

</script>