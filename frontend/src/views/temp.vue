<script>
import NavBar from '@/components/NavBar.vue';
export default {
  components: {
    NavBar
  },
    data() {
        return {
            publicCampaigns: [],
            adRequests: [],
            requestForm: {
                campaign_id: null,
                messages: '',
                requirements: '',
                paymentAmount: '',
            },
    
            searchQuery: '', // Added for search functionality
            filteredCampaigns: [], // To store filtered campaigns
        };
    },
    methods: {

        fetchPublicCampaigns() {
            fetch('http://localhost:5000/public_campaigns', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                },
            })
                .then(response => response.json())
                .then(data => {
                    this.publicCampaigns = data;
                    this.filteredCampaigns = data; // Initialize with all campaigns
                })
                .catch(error => console.error('Error fetching campaigns:', error));
        },


        fetchAdRequests() {
            fetch('http://localhost:5000/influencer/ad-requests', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                },
            })
                .then(response => response.json())
                .then(data => {
                    this.adRequests = data;
                    console.log(this.adRequests);
                })
                .catch(error => console.error('Error fetching ad requests:', error));
        },

        filterCampaigns() {
            const query = this.searchQuery.toLowerCase();
            this.filteredCampaigns = this.publicCampaigns.filter(campaign =>
                campaign.name.toLowerCase().includes(query) ||
                campaign.description.toLowerCase().includes(query)
            );
        },
        openRequestModal(campaignId) {
            this.requestForm.campaign_id = campaignId;
            const requestModal = new bootstrap.Modal(document.getElementById('requestModal'));
            requestModal.show();
        },
        sendAdRequest() {
            fetch('http://localhost:5000/influencer/send_ad_request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                },
                body: JSON.stringify(this.requestForm),
            })
                .then(response => {
                    if (response.ok) {
                        alert('Ad request sent successfully');
                        this.resetRequestForm();
                        const requestModal = bootstrap.Modal.getInstance(document.getElementById('requestModal'));
                        requestModal.hide();
                        this.fetchAdRequests(); // Refresh the ad requests list
                    } else {
                        return response.json().then(data => {
                            alert(data.message || 'Failed to send request');
                        });
                    }
                })
                .catch(error => console.error('Error sending ad request:', error));
        },
        resetRequestForm() {
            this.requestForm = {
                campaign_id: null,
                messages: '',
                requirements: '',
                paymentAmount: '',
            };
        },

        // Method to accept an ad request
        acceptRequest(requestId) {
            fetch('http://localhost:5000/accept_ad_request', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                },
                body: JSON.stringify({ ad_request_id: requestId }),
            })
                .then(response => {
                    if (response.ok) {
                        alert('Ad request accepted successfully');
                        this.fetchAdRequests(); // Refresh the ad requests list
                    } else {
                        return response.json().then(data => {
                            alert(data.message || 'Failed to accept request');
                        });
                    }
                })
                .catch(error => console.error('Error accepting ad request:', error));
        },

        // // Method to reject an ad request
        rejectRequest(requestId) {
            fetch('http://localhost:5000/reject_ad_request', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                },
                body: JSON.stringify({ ad_request_id: requestId }),
            })
                .then(response => {
                    if (response.ok) {
                        alert('Ad request rejected successfully');
                        this.fetchAdRequests(); // Refresh the ad requests list
                    } else {
                        return response.json().then(data => {
                            alert(data.message || 'Failed to reject request');
                        });
                    }
                })
                .catch(error => console.error('Error rejecting ad request:', error));
        },
        negotiate(id){
            this.$router.push({ name: 'NegotiationPage', params: { id: id } });
        }
    },
    mounted() {
        this.fetchPublicCampaigns();
        this.fetchAdRequests(); // Fetch ad requests on component mount
    },
};
</script>