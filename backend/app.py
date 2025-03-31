from flask import Flask, request, jsonify, send_file, Response
from models import *
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies
from datetime import datetime
import workers, task
from mailer import mail
from io import BytesIO, StringIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask_caching import Cache

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025   #change by seeing your port
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

CORS(app, supports_credentials=True)

celery=workers.celery

cache = Cache(app)

celery.conf.update(
    broker_url='redis://localhost:6379/1',
    result_backend='redis://localhost:6379/2'
)

celery.Task = workers.ContextTask
app.app_context().push()

db.init_app(app)
jwt = JWTManager(app)
mail.init_app(app)

def create_admin():
    admin = Users.query.filter_by(role='admin').first()
    if not admin:
        admin = Users(
            role = 'admin',
            name='Admin',
            contactno=0000000000,
            email='admin@app.com',
            pswd='123',
            address='none',
            pincode=000000
        )
        db.session.add(admin)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_admin()

######################################################################################################
@app.route('/')
def hello_world():
    return 'Hello, World!'
#####################################################################################################

#SIGNUP
@app.route('/signup', methods=['POST'])
def signup():
    data=request.get_json()

    #common data for all users
    role=data['role']
    name=data['name']
    contactno=data['contactno']
    email=data['email']
    pswd=data['pswd']
    address=data['address']
    pincode=data['pincode']

    #check if user exists
    check=Users.query.filter_by(email=email).first()
    if check:
        return jsonify({'error': 'User already exists'}), 400

    new_user=Users(role=role,name=name,contactno=contactno,email=email,pswd=pswd,address=address,pincode=pincode)
    db.session.add(new_user)
    db.session.commit()

    #for customers
    if role=='customer':
        new_cust=Customers(userid=new_user.id)
        db.session.add(new_cust)
        db.session.commit()

    #for professionals
    elif role=='professional':
        service=data['service']
        experience=data['experience']
        new_profes=Professionals(userid=new_user.id, service=service, experience=experience)
        db.session.add(new_profes)
        db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 200


@app.route('/signup/get_services', methods=['GET'])
def get_services():
    services=Services.query.all()
    services_data=[]

    for service in services:
        services_data.append(service.name)

    return jsonify(services_data), 200

#####################################################################################################

#LOGIN
@app.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    email=data['email']
    pswd=data['pswd']

    user=Users.query.filter_by(email=email).first()
    if user and user.pswd==pswd:
        access_token=create_access_token(identity=str(user.id), additional_claims={'role': user.role})
        return jsonify({'message': 'Login successful', 'access_token':access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    

#####################################################################################################

#RBAC
@app.route('/getuserid', methods=['GET'])
@jwt_required()
def getuserid():
    current_user_id = get_jwt_identity()
    role=get_jwt().get('role')
    return jsonify({'id': current_user_id, 'role':role}), 200

#####################################################################################################

#LOGOUT
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'Logged out successfully'})
    unset_jwt_cookies(response)
    return response, 200

#####################################################################################################

#CREATE SERVICE PAGE

#CREATE SERVICE
@app.route('/create_service', methods=['POST'])
@jwt_required()
def create_service():
    role=get_jwt().get('role')

    if role!='admin':
        return jsonify({'error': 'You must be Admin to create a service'}), 401
    
    data=request.get_json()
    name=data['name']
    baseprice=data['baseprice']
    descr=data['descr']

    new_service=Services(name=name, baseprice=baseprice, descr=descr)

    db.session.add(new_service)
    db.session.commit()

    return jsonify({'message': 'Service created successfully'}), 200

#####################################################################################################

#ADMIN DASHBOARD PAGE KE LINKS


#ALL SERVICES TABLE
@app.route('/admindash_services', methods=['GET'])
@jwt_required()
def all_services():

    role=get_jwt().get('role')

    if role!='admin':
        return jsonify({'error': 'You must be Admin to view all services'}), 401

    services=Services.query.all()
    services_data=[]
    for service in services:
        services_data.append({
            "id": service.id,
            "name": service.name,
            "baseprice": service.baseprice,
            "descr": service.descr
        })

    return jsonify(services_data), 200


#EDIT SERVICE
@app.route('/edit_service/<int:service_id>', methods=['PUT'])
@jwt_required()
def edit_service(service_id):
    role=get_jwt().get('role')

    if role!='admin':
        return jsonify({'error': 'You must be Admin to edit a service'}), 401
    
    service=Services.query.get_or_404(service_id)
    
    data=request.get_json()
    service.name=data['name']
    service.baseprice=data['baseprice']
    service.descr=data['descr']

    db.session.commit()

    return jsonify({'message': 'Service edited successfully'}), 200


#GET SERVICE DETAILS BY ID
#WHEN UPDATING THE SERVICE WE'LL NEED THE DETAILS TO BE ALREADY THERE
@app.route('/edit_service/<int:service_id>', methods=['GET']) 
@jwt_required()
def get_service(service_id):
    service=Services.query.get_or_404(service_id)

    service_data={
        "name": service.name,
        "baseprice": service.baseprice,
        "descr": service.descr
    }

    return jsonify(service_data), 200


#DELETE SERVICE
@app.route('/edit_service/<int:service_id>', methods=['DELETE'])
@jwt_required()
def delete_service(service_id):
    role=get_jwt().get('role')

    if role!='admin':
        return jsonify({'error': 'You must be Admin to delete a service'}), 401
    
    service=Services.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()

    return jsonify({'message': 'Service deleted successfully'}), 200


#ALL PROFESSIONALS TABLE
@app.route('/admindash_professionals', methods=['GET'])
@jwt_required()
def all_professionals():

    role=get_jwt().get('role')

    if role!='admin':
        return jsonify({'error': 'You must be Admin to view all professionals'}), 401

    professionals=db.session.query(Professionals.id, Professionals.service, Professionals.experience, Users.name, Users.email, Users.pincode).join(Users, Professionals.userid == Users.id).all()
    professionals_data=[]
    for professional in professionals:
        professionals_data.append({
            "id": professional.id,
            "name": professional.name,
            "service": professional.service,
            "experience": professional.experience,
            "email": professional.email,
            "pincode": professional.pincode
        })

    return jsonify(professionals_data), 200


#ALL CUSTOMERS TABLE
@app.route('/admindash_customers', methods=['GET'])
@jwt_required()
def all_customers():

    role=get_jwt().get('role')

    if role!='admin':
        return jsonify({'error': 'You must be Admin to view all customers'}), 401

    customers=db.session.query(Customers.id, Users.name, Users.email, Users.pincode).join(Users, Customers.userid == Users.id).all()
    customers_data=[]
    for customer in customers:
        customers_data.append({
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "pincode": customer.pincode
        })

    return jsonify(customers_data), 200



#DELETE PROFESSIONAL
@app.route('/delete_prof/<int:professional_id>', methods=['DELETE'])
@jwt_required()
def delete_professional(professional_id):
    role=get_jwt().get('role')

    if role!='admin':
        return jsonify({'error': 'You must be Admin to delete a professional'}), 401
    
    professional=Professionals.query.get_or_404(professional_id)
    db.session.delete(professional)
    db.session.commit()

    return jsonify({'message': 'Professional deleted successfully'}), 200


#DELETE CUSTOMER
@app.route('/delete_cust/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    role=get_jwt().get('role')

    if role!='admin':
        return jsonify({'error': 'You must be Admin to delete a customer'}), 401
    
    customer=Customers.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()

    return jsonify({'message': 'Customer deleted successfully'}), 200


#SEE STATS
@app.route('/admin/stats', methods=['GET'])
@cache.cached(timeout=180)
@jwt_required()
def get_stats():

    total_users = Users.query.count()
    total_services = Services.query.count()
    total_service_requests = Servicerequest.query.count()

    stats = {
        "total_users": total_users,
        "total_services": total_services,
        "total_service_requests": total_service_requests
    }

    return jsonify(stats), 200


#SEE GRAPH
@cache.cached(timeout=60)
@app.route('/admin/stats/graph', methods=['GET'])
@jwt_required()
def get_stats_graph():

        labels = ['Customers', 'Professionals']
        count = [Customers.query.count(), Professionals.query.count()]
        
        fig, ax = plt.subplots()
        ax.pie(count, labels=labels, autopct='%1.1f%%')
        ax.axis('equal')

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return send_file(img, mimetype='image/png')

###############################################################################################

#CUSTOMER DASHBOARD

#SEES ALL SERVICES
@app.route('/custdash_get_services', methods=['GET'])
@jwt_required()
def see_services():

    current_cust_id=get_jwt_identity()
    role=get_jwt().get('role')

    services=Services.query.all()
    services_data=[]
    for service in services:
        services_data.append({
            "id": service.id,
            "name": service.name,
            "baseprice": service.baseprice,
            "descr": service.descr
        })

    return jsonify(services_data), 200


#MODAL TO SELECT PROFESSIONAL


#SEE ALL PROFESSIONALS IN MODAL
@app.route('/cust_dash/get_professionals', methods=['GET'])
@jwt_required()
def get_professionals():
    
    professionals=db.session.query(Professionals.id, Professionals.service, Professionals.experience, 
                                   Users.name, Users.email, Users.pincode, Users.contactno, 
                                   Services.baseprice).join(Users, Professionals.userid == Users.id).join(Services, 
                                   Professionals.service == Services.name).all()
    professionals_data=[]
    for professional in professionals:
        professionals_data.append({
            "id": professional.id,
            "name": professional.name,
            "service": professional.service,
            "baseprice": professional.baseprice,
            "experience": professional.experience,
            "email": professional.email,
            "pincode": professional.pincode,
            "contactno": professional.contactno
        })

    return jsonify(professionals_data), 200


#SEND SERVICE REQUEST
@app.route('/cust_dash/send_service_request', methods=['POST'])
@jwt_required()
def send_service_request():

    current_cust_id = get_jwt_identity()
    role=get_jwt().get('role')

    customer=Customers.query.filter_by(userid=current_cust_id).first()

    data=request.get_json()

    new_request=Servicerequest(
        custid=customer.id,
        profesid=data['professional_id'],
        status='pending',
        payment_amt=data['amount'],
        datebooked=datetime.strptime(data['date'], '%Y-%m-%d').date()
    )

    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'Service request sent successfully'}), 200


#SEE ALL SERVICE REQUESTS SEND BY THE CUSTOMER
@app.route('/cust_dash/get_service_requests', methods=['GET'])
@jwt_required()
def get_service_requests():

    current_cust_id = get_jwt_identity()

    customer=Customers.query.filter_by(userid=current_cust_id).first()

    serv_reqs=Servicerequest.query.filter_by(custid=customer.id).all()
    serv_reqs_data=[]

    for req in serv_reqs:
        professional = Professionals.query.get(req.profesid)
        user= Users.query.filter_by(id=professional.userid).first()
        serv_reqs_data.append({
            "id": req.bookingid,
            "service_name": professional.service,
            "professional_name": user.name,
            "professional_contactno": user.contactno,
            "date": req.datebooked,
            "amount": req.payment_amt,
            "status": req.status
        })

    return jsonify(serv_reqs_data), 200

#EDIT BOOKING
@app.route('/edit_booking/<int:booking_id>', methods=['PUT'])
@jwt_required()
def edit_booking(booking_id):
    
    booking=Servicerequest.query.get_or_404(booking_id)
    
    data=request.get_json()
    booking.datebooked=data['date']
    booking.payment_amt=data['amount']

    db.session.commit()

    return jsonify({'message': 'Booking edited successfully'}), 200


#GET BOOKING DETAILS BY ID
#WHEN UPDATING THE BOOKING WE'LL NEED THE DETAILS TO BE ALREADY THERE
@app.route('/edit_booking/<int:booking_id>', methods=['GET']) 
@jwt_required()
def get_booking(booking_id):
    booking=Servicerequest.query.get_or_404(booking_id)

    booking_data={
        "datebooked": booking.datebooked,
        "payment_amt": booking.payment_amt,
    }

    return jsonify(booking_data), 200


#DELETE BOOKING
@app.route('/cust_dash/delete_booking/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def delete_booking(booking_id):
    
    booking=Servicerequest.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()

    return jsonify({'message': 'Booking deleted successfully'}), 200

###############################################################################################

#PROFESSIONAL DASHBOARD

#SEES ALL THEIR SERVICE REQUESTS
@app.route('/prof_dash/all_service_reqs', methods=['GET'])
@jwt_required()
def all_service_reqs():
    current_user_id = get_jwt_identity()
    
    # Find the professional record for this user
    professional = Professionals.query.filter_by(userid=current_user_id).first()
    
    # Get service requests for this professional
    serv_reqs = Servicerequest.query.filter_by(profesid=professional.id).all()
    
    # Debug info
    print(f"User ID: {current_user_id}, Professional ID: {professional.id}")
    print(f"Found {len(serv_reqs)} service requests")
    
    serv_reqs_data = []
    
    for req in serv_reqs:
        print(req)
        customer = Customers.query.filter_by(id=req.custid).first()
        print(customer)
        if customer:
            user = Users.query.filter_by(id=customer.userid).first()
            print(user)
            if user:
                serv_reqs_data.append({
                    "booking_id": req.bookingid,
                    "custid": req.custid,
                    "profesid": req.profesid,
                    "status": req.status,
                    "payment_amt": req.payment_amt,
                    "datebooked": req.datebooked,
                    "cust_name": user.name,
                    "cust_contactno": user.contactno,
                    "cust_pincode": user.pincode,
                    "cust_address": user.address
                })
    
    print(serv_reqs_data)
    return jsonify(serv_reqs_data), 200


#ACCEPT BOOKING
@app.route('/prof_dash/accept', methods=['PUT'])
@jwt_required()
def accept_booking():
    current_prof_id = get_jwt_identity()
    role=get_jwt().get('role')

    if role!='professional':
        return jsonify({'error': 'You must be Professional to accept a booking'}), 401

    data=request.get_json()
    booking=Servicerequest.query.get_or_404(data['id'])

    booking.status='accepted'

    db.session.commit()

    return jsonify({'message': 'Booking accepted successfully'}), 200


#REJECT BOOKING
@app.route('/prof_dash/reject', methods=['PUT'])
@jwt_required()
def reject_booking():
    current_prof_id = get_jwt_identity()
    role=get_jwt().get('role')

    if role!='professional':
        return jsonify({'error': 'You must be Professional to reject a booking'}), 401

    data=request.get_json()
    booking=Servicerequest.query.get_or_404(data['id'])

    booking.status='rejected'

    db.session.commit()

    return jsonify({'message': 'Booking rejected successfully'}), 200


###############################################################################################
if __name__ == '__main__':
    app.run(debug=True)