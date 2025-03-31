<template>
    <NavBar />
    <div class="container mt-3">

        <h2>Customer Dashboard</h2>

            <div class="btn-group">
                <button @click="openBookmodall()" class="btn btn-primary">BOOK A PROFESSIONAL</button>
            </div>

        <br>
        <br>                                        
        <br>

        <div class="row">
        <h3>My Bookings</h3>
        <div v-for="booking in my_bookings" :key="booking.id" class="col-md-3 mb-3"> 
            <div class="card" shadow-sm>
                <div class="card-body">
                    <h5 class="card-title">Service: {{booking.service_name}}</h5>
                    <p class="card-text">Professional: {{booking.professional_name}}</p>
                    <p class="card-text">Contact No.: {{booking.professional_contactno}}</p>
                    <p class="card-text">Date: {{booking.date}}</p>
                    <p class="card-text">Payment Amount: {{booking.amount}}</p>
                    <p class="card-text">Status: {{booking.status}}</p>
                </div>
                <div class = "card-footer"> 
                    <div class="btn-group">
                        <div v-if="booking.status == 'pending'">
                        <button @click="openEditModal(booking)" class="btn btn-primary">Edit</button>
                        <button @click="delete_booking(booking.id)" class="btn btn-danger">Delete</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


        <!-- BOOK MODAL -->
        <div class="modal fade" id="bookModall" tabindex="-1" aria-labelledby="bookModallLabel" aria-hidden="true">
        <div class="modal-dialog">
        <div class="modal-content">

            <div class="modal-header">
            <h5 class="modal-title" id="bookModallLabel">Book a Service</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>

            <div class="modal-body">
                <form @submit.prevent="bookaservice">

                    <!-- search bar -->
                    <div class="mb-3">
                        <input v-model="searchbar" type="text" class="form-control" placeholder="Search Professionals">
                    </div>

                    <!-- filter by service -->
                    <div class="mb-3">
                        <label for="serviceFilter" class="form-label">Filter by Service</label>
                        <select v-model="filters.service" class="form-control" id="serviceFilter">
                            <option value="">All Services</option>
                            <option v-for="service in uniqueservices" :key="service" :value="service">
                            {{ service }}
                            </option>
                        </select>
                    </div>


                    <!-- filter by pincode -->
                    <div class="mb-3">
                    <label for="pincodefilter" class="form-label">Filter by Pincode</label>
                    <select v-model="filters.pincode" class="form-control" id="pincodeFilter">
                        <option value="">Locations Available</option>
                        <option v-for="pincode in uniquepincodes" :key="pincode" :value="pincode">
                        {{ pincode }}
                        </option>
                    </select>
                    </div>

                    <!-- select professional -->
                    <div class="mb-3">
                    <label for="professional" class="form-label">Select Professional</label>
                    <select v-model="requestForm.professional_id" class="form-control" id="professional"
                        @change="selected_professional_details" required>
                        <option v-for="professional in filteredprofessionals" :key="professional.id" :value="professional.id">
                        {{ professional.name }}
                        </option>
                    </select>
                    </div>

                    <!-- Displaying professional Details -->
                    <div v-if="selectedprofessional" class="professional-details">
                    <p><strong>Name:</strong> {{ selectedprofessional.name }}</p>
                    <p><strong>Service:</strong> {{ selectedprofessional.service }}</p>
                    <p><strong>Baseprice:</strong> {{ selectedprofessional.baseprice }}</p>
                    <p><strong>Experience:</strong> {{ selectedprofessional.experience }}</p>
                    <p><strong>Contact:</strong> {{ selectedprofessional.contactno }}</p>
                    <p><strong>Pincode:</strong> {{ selectedprofessional.pincode }}</p>
                    </div>

                    <!-- date booked -->
                    <div class="mb-3">
                        <label for="date" class="form-label">Date</label>
                        <input v-model="requestForm.date" type="date" class="form-control" id="date" required>
                    </div>

                    <!-- payment amount -->
                    <div class="mb-3">
                        <label for="amount" class="form-label">Payment Amount</label>
                        <input v-model="requestForm.amount" type="number" class="form-control" id="amount" required>
                    </div>

                    <button type="submit" class="btn btn-primary">Book</button>

                </form>
            </div>


        </div>
        </div>
        </div>

        <!-- Edit Modal -->
        <div class="modal fade" id="editModal" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">

            <div class="modal-header">
                <h5 class="modal-title" id="editModalLabel">Edit Booking</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>

            <div class="modal-body">
                <form @submit.prevent="saveEditedBooking">
                <div class="mb-3">
                    <label for="editDate" class="form-label">Date</label>
                    <input v-model="editBookingModal.date" type="date" class="form-control" id="editDate" required>
                </div>
                <div class="mb-3">
                    <label for="editAmount" class="form-label">Payment Amount</label>
                    <input v-model="editBookingModal.amount" type="number" class="form-control" id="editAmount" required>
                </div>
                <button type="submit" class="btn btn-primary">Save Changes</button>
                </form>
            </div>
            
            </div>
        </div>
        </div>

    </div>


</template>


<script>

import NavBar from '../components/NavBar.vue'
export default {
    components: {NavBar},
    name: 'CustomerDashboard',
    data() {
        return{
            all_services: [],
            my_bookings: [],
            searchbar: '',
            filters: {
                service: '',
                pincode: ''
            },
            professionals: [],
            selectedprofessional: null,
            requestForm: {
                professional_id: null,
                customer_id: '',
                date: '',
                amount: ''
            }, 
            bookModall: null, 
            editBookingModal: {
                id: null,
                date: '',
                amount: ''
            }
        }
    },
    mounted() {
        this.fetchServices();
        this.fetchProfessionals();
        this.fetchMyBookings();
    },
    computed: {
        uniqueservices() {
            const services = this.professionals.map(professional => professional.service);
            return [...new Set(services)];
        },
        filteredprofessionals() {
            return this.professionals.filter(professional => {
                const isinSearch = professional.name.toLowerCase().includes(this.searchbar.toLowerCase());
                const isinService = !this.filters.service || professional.service === this.filters.service;
                const isinPincode = !this.filters.pincode || professional.pincode === this.filters.pincode;
                return isinService && isinPincode && isinSearch;
            });
        },
        uniquepincodes() {
            const pincodes = this.professionals.map(professional => professional.pincode);
            return [...new Set(pincodes)];
        }
    },
    methods: {
        resetForm() {
        this.requestForm = {
            professional_id: null,
            customer_id: '',
            date: '',
            amount: ''
        };
        this.selectedprofessional = null;
        },
        async fetchServices() {
            const response = await fetch('http://localhost:5000/custdash_get_services', {
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
        openBookmodall() {
            const bookModall=new bootstrap.Modal(document.getElementById('bookModall'));
            bookModall.show();
        },
        selected_professional_details() {
            this.selectedprofessional = this.professionals.find(professional => professional.id === this.requestForm.professional_id); 
        },
        async fetchProfessionals() {
            const response = await fetch('http://localhost:5000/cust_dash/get_professionals', {
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
                this.professionals=data;
            }
        },
        async bookaservice() {
            //this.requestForm.customer_id = this.user.id;
            const response = await fetch('http://localhost:5000/cust_dash/send_service_request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                },
                body: JSON.stringify(this.requestForm)
            })
            const data = await response.json();
            if (!response.ok) {
                alert(data.error);f
            } else {
                alert(data.message);
                const bookModall = bootstrap.Modal.getInstance(document.getElementById('bookModall'));
                bookModall.hide();
                this.resetForm();
                this.fetchMyBookings();
            }
        }, 
        async fetchMyBookings() {
            const response = await fetch('http://localhost:5000/cust_dash/get_service_requests', {
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
                this.my_bookings=data;
            }
        }, 
        openEditModal(booking) {
            this.editBookingModal = {
                id: booking.id,
                date: booking.date,
                amount: booking.amount
            };
            const editModal = new bootstrap.Modal(document.getElementById('editModal'));
            editModal.show();
        }, 
        async saveEditedBooking() {
            const response = await fetch(`http://localhost:5000/edit_booking/${this.editBookingModal.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                },
            body: JSON.stringify({date: this.editBookingModal.date,
                                amount: this.editBookingModal.amount})
            });

            if (!response.ok) {
            throw new Error('Failed to update booking');
            }

            const updatedBooking = await response.json();
            this.fetchMyBookings();

            const editModal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
            if (editModal) {
                editModal.hide();
            }

            this.editBookingModal = {
                id: null,
                date: '',
                amount: ''
            };
        }, 


        async delete_booking(booking_id) {
            const response = await fetch(`http://localhost:5000/cust_dash/delete_booking/${booking_id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            });
            if (!response.ok) {
                const errorData = await response.json();
                alert(errorData.error);
                return;
            }
            alert('Booking deleted successfully');
            // Remove the deleted booking from the list
            this.my_bookings = this.my_bookings.filter(booking => booking.id !== booking_id);
        }
    }
}    

</script>