export default {
    data() {
        return {
            user:null,
            role:null,
            authed:false
        }
    },
    async created() {
        await this.checkauthed();
    },
    methods: {
        async checkauthed() {
            const access_token = localStorage.getItem('access_token')
            if (!access_token) {
                this.user=null;
                this.authed=false;
                return;
            }
            this.user=await this.getuserid(access_token);
        },
        async getuserid(access_token) {
            const response = await fetch('http://localhost:5000/getuserid', {
                method: 'GET',
                headers: {
                    'Content-type': 'application/json',
                    'Authorization': `Bearer ${access_token}`
                }
            })
            const data = await response.json();
            if (response.ok) {
                this.role=data.role;
                this.authed=true;
                return data;
                //console.log(data);
            }
            else {
                this.role=null;
                this.authed=false;
                return null;
            }
        },
        logout() {
            fetch('http://localhost:5000/logout', {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            }).then(() => {
                localStorage.removeItem('access_token');
                this.user=null;
                this.role=null;
                this.authed=false;
                this.$router.push('/login');    
            }).catch(err => console.log(err));
        }
    }
}