<template>

<NavBar/>
    <div class="container mt-5">

        <!-- Active Bookings -->
        <h2 class="text-center">Active Bookings</h2>

        <!-- search bar -->
        <div class="row mb-4">
            <div class="col-md-4 offset-md-4">
                <input v-model="searchbar" type="text" class="form-control" placeholder="Search active bookings">
            </div>                                       
        </div>                                     


        <!-- active bookings -->
        <div class="row">
            <div v-for="booking in filteredActiveBookings" :key="booking.booking_id" class="col-md-3 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ booking.cust_name }}</h5>
                        <p class="card-text">{{ booking.datebooked }}</p>
                        <p class="card-text">{{ booking.payment_amt }}</p>
                        <p class="card-text">{{ booking.cust_contactno }}</p>
                        <p class="card-text">{{ booking.cust_address }}</p>
                        <p class="card-text">{{ booking.cust_pincode }}</p>
                    </div>
                    <div class = "card-footer"> 
                        <div class="btn-group">
                            <button class="btn btn-success me-2" @click="acceptbooking(booking.booking_id)">Accept</button>
                            <button class="btn btn-danger me-2" @click="rejectbooking(booking.booking_id)">Reject</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- completed bookings -->
     <h2 class="text-center">Completed Bookings</h2>

    <div class="row">
            <div v-for="booking in completedBookings" :key="booking.booking_id" class="col-md-3 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ booking.cust_name }}</h5>
                        <p class="card-text">{{ booking.datebooked }}</p>
                        <p class="card-text">{{ booking.payment_amt }}</p>
                        <p class="card-text">{{ booking.cust_contactno }}</p>
                        <p class="card-text">{{ booking.cust_address }}</p>
                        <p class="card-text">{{ booking.cust_pincode }}</p>
                        <p class="card-text">{{ booking.status }}</p>
                    </div>
                </div>
            </div>
        </div>   

</template>


<script>

import NavBar from '@/components/NavBar.vue';
export default {
  components: {
    NavBar
  },
  data() {
    return {
        allbookings: [],
        searchbar: '',
    }
  }, 
  mounted() {
      this.fetchallbookings();
  },
  computed: {
    activeBookings() {
        console.log('Active bookings computed:', this.allbookings.filter(booking => booking.status === 'pending'));
        return this.allbookings.filter(booking => booking.status === 'pending');
    },    
    completedBookings() {
      return this.allbookings.filter(booking => booking.status !== 'pending');
    },
    filteredActiveBookings() {
        const search = this.searchbar.toLowerCase();
            return this.activeBookings.filter(booking => booking.cust_name.toLowerCase().includes(search));
    }, 
  },

  methods: {

    fetchallbookings() {
            fetch('http://localhost:5000/prof_dash/all_service_reqs', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                },
            })
                .then(response => response.json())
                .then(data => {
                    console.log('API response:', data);
                    console.log('Pending bookings:', data.filter(booking => booking.status === 'pending'));
                    console.log('Completed bookings:', data.filter(booking => booking.status !== 'pending'));
                    this.allbookings = data;
                    // this.filterActiveBookings=this.activeBookings;
                })
                .catch(error => console.error('Error fetching campaigns:', error));
        },

    acceptbooking(booking_id) {
            fetch('http://localhost:5000/prof_dash/accept', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                },
                body: JSON.stringify({ id: booking_id }),
            })
                .then(response => {
                    if (response.ok) {
                        alert('Booking accepted successfully');
                        this.fetchallbookings(); // Refresh the bookings list
                    } else {
                        return response.json().then(data => {
                            alert(data.message || 'Failed to accept booking');
                        });
                    }
                })
                .catch(error => console.error('Error accepting booking:', error));
        },

        rejectbooking(booking_id) {
            fetch('http://localhost:5000/prof_dash/reject', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                },
                body: JSON.stringify({ id: booking_id }),
            })
                .then(response => {
                    if (response.ok) {
                        alert('Booking rejected successfully');
                        this.fetchallbookings(); // Refresh the bookings list
                    } else {
                        return response.json().then(data => {
                            alert(data.message || 'Failed to reject booking');
                        });
                    }
                })
                .catch(error => console.error('Error rejecting booking:', error));
        },
  } 
}
</script>