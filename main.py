from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import date
from nosql import update_entry, auth_user

# app initialization
app = Flask(__name__)
postgreSQL_pass = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:'+postgreSQL_pass+'@localhost/traffic_db2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# customer table
class Customer(db.Model):
	__tablename__ = 'CUSTOMER'
	aadhar_num = db.Column(db.BigInteger, primary_key=True, nullable=False)
	first_name = db.Column(db.String(15), nullable=False)
	last_name = db.Column(db.String(15), nullable=False)
	gender = db.Column(db.String(1))
	dob = db.Column(db.Date)
	address = db.Column(db.String(100))

	def __init__(self, aadhar_num, first_name, last_name, gender, dob, address):
		self.aadhar_num = aadhar_num
		self.first_name = first_name
		self.last_name = last_name
		self.gender = gender
		self.dob = dob
		self.address = address

# camera table
class Camera(db.Model):
	__tablename__ = 'CAMERA'
	cam_num = db.Column(db.Integer, primary_key=True, nullable=False)
	cam_location = db.Column(db.String(30), nullable=False)

	def __init__(self, cam_num, cam_location):
		self.cam_num = cam_num
		self.cam_location = cam_location

# vehicle table
class Vehicle(db.Model):
	__tablename__ = 'VEHICLE'
	vehicle_num = db.Column(db.String(10), primary_key=True, nullable=False)
	name = db.Column(db.String(20))
	model = db.Column(db.String(10))
	color = db.Column(db.String(10))
	year_of_make = db.Column(db.Integer)
	engine_num = db.Column(db.String(20))
	chasis_num = db.Column(db.String(20))
	registration_expiry = db.Column(db.Date)
	insurance_expiry = db.Column(db.Date)
	emissions_expiry = db.Column(db.Date)
	customer_aadhar = db.Column(db.BigInteger, db.ForeignKey('CUSTOMER.aadhar_num'))

	def __init__(self, vehicle_num, name, model, color, year_of_make, engine_num, chasis_num, registration_expiry, insurance_expiry, emissions_expiry, customer_aadhar):
		self.vehicle_num = vehicle_num
		self.name = name
		self.model = model
		self.color = color
		self.year_of_make = year_of_make
		self.engine_num = engine_num
		self.chasis_num = chasis_num
		self.registration_expiry = registration_expiry
		self.insurance_expiry = insurance_expiry
		self.emissions_expiry = emissions_expiry
		self.customer_aadhar = customer_aadhar

# captures table
class Captures(db.Model):
	__tablename__ = 'CAPTURES'
	cam_num = db.Column(db.Integer, db.ForeignKey('CAMERA.cam_num'), primary_key=True, nullable=False)
	vehicle_num = db.Column(db.String(10), db.ForeignKey('VEHICLE.vehicle_num'), primary_key=True, nullable=False)
	clip_id = db.Column(db.Integer, nullable=False, unique=True)

	def __init__(self, cam_num, vehicle_num, clip_id):
		self.cam_num = cam_num
		self.vehicle_num = vehicle_num
		self.clip_id = clip_id

# violations table
class Violation(db.Model):
	__tablename__ = 'VIOLATION'
	violation_num = db.Column(db.Integer, primary_key=True, nullable=False)
	violation_type = db.Column(db.String(20), nullable=False)
	date = db.Column(db.Date, nullable=False)
	time = db.Column(db.Time)
	fine_amt = db.Column(db.Integer)
	fine_paid = db.Column(db.String(1), nullable=False)	# 'Y' or 'N'
	cam_num = db.Column(db.Integer, db.ForeignKey('CAMERA.cam_num'))
	clip_id = db.Column(db.Integer, db.ForeignKey('CAPTURES.clip_id'))
	vehicle_num = db.Column(db.String(10), db.ForeignKey('VEHICLE.vehicle_num'))

	def __init__(self, violation_type, date, time, fine_amt, fine_paid, cam_num, clip_id, vehicle_num):
		self.violation_type = violation_type
		self.date = date
		self.time = time
		self.fine_amt = fine_amt
		self.fine_paid = fine_paid
		self.cam_num = cam_num
		self.clip_id = clip_id
		self.vehicle_num = vehicle_num

# captured vehicle table
class CapturedVehicle(db.Model):
	__tablename__ = 'CAPTURED_VEHICLE'
	vehicle_num = db.Column(db.String(10), db.ForeignKey('VEHICLE.vehicle_num'), primary_key=True)

	def __init__(self, vehicle_num):
		self.vehicle_num = vehicle_num

# missing vehicles table
class MissingVehicle(db.Model):
	__tablename__ = 'MISSING_VEHICLE'
	vehicle_num = db.Column(db.String(10), db.ForeignKey('VEHICLE.vehicle_num'), primary_key=True)
	date_of_missing = db.Column(db.Date, primary_key=True, nullable=False)
	place_of_missing = db.Column(db.String(20), nullable=False)
	is_found = db.Column(db.String(1), nullable=False) # 'Y' or 'N'

	def __init__(self, vehicle_num, date_of_missing, place_of_missing, is_found):
		self.vehicle_num = vehicle_num
		self.date_of_missing = date_of_missing
		self.place_of_missing = place_of_missing
		self.is_found = is_found

@app.route("/")
def index():
    return render_template("main_page.html", message=False)


@app.route("/select_public", methods=["POST"])
def public_view():
	username = request.form['p_username']
	password = request.form['p_password']
	# if(auth_user(username, password, 'public')):
	# 	return render_template("public_view.html")
	# else:
	# 	return render_template("main_page.html", message=True)
	return render_template("public_view.html")


@app.route("/select_td", methods=["POST"])
def td_view():
	username = request.form['t_username']
	password = request.form['t_password']
	# if(auth_user(username, password, 'transport_dept')):
	# 	return render_template("td_view.html")
	# else:
	# 	return render_template("main_page.html", message=True)
	return render_template("td_view.html")


@app.route("/pay_fine", methods=["POST", "GET"])
def pay_fine():
    return render_template("fine_payment.html", violations=[])


@app.route("/report_missing", methods=["POST"])
def report_missing_vehicles():
    return render_template("report_mveh.html", message=False)


@app.route("/mv_report", methods=["POST", "GET"])
def missing_veh_report():
    # get table content from database
    miss_entries=MissingVehicle.query.all()
    return render_template("miss_veh_report.html", miss_entries=miss_entries)


@app.route("/viol_report", methods=["POST", "GET"])
def viol_report():
    # get table content from database
    viol_entries = Violation.query.all()
    return render_template("viol_report.html", viol_entries=viol_entries)

@app.route("/update_fines", methods=["POST", "GET"])
def somethng_random132():
	return render_template("update_fines.html", message=False)

@app.route("/update_fines1", methods=["POST", "GET"])
def update_fines():
    # TODO: update NoSql database here - DONE
    fine_type = request.form["fine_type"]
    fine_amt = request.form["fine_amt"]
    if(fine_type=='insurance_expiry'):
    	update_entry('traffic_db2_v1_fines', 1, {
    		'fine_type': 'insurance_expiry',
    		'fine_amt': fine_amt
    		})
    elif(fine_type=='registration_expiry'):
    	update_entry('traffic_db2_v1_fines', 2, {
    		'fine_type': 'registration_expiry',
    		'fine_amt': fine_amt
    		})
    elif(fine_type=='emissions_expiry'):
    	update_entry('traffic_db2_v1_fines', 2, {
    		'fine_type': 'emissions_expiry',
    		'fine_amt': fine_amt
    		})
    else:
    	print("ERROR: no valid fine type found, try again!!")
    return render_template("update_fines.html", message=True)


@app.route("/get_violations", methods=["POST", "GET"])
def get_violations():
    veh_num = request.form["veh_num"]
    # get vehicle entry and all its fines
    violations = Violation.query.filter_by(vehicle_num=request.form['veh_num']).all()
    print("got entry for: ", violations[0].vehicle_num)
    return render_template("fine_payment.html", violations=violations)

@app.route("/submit_missing", methods=["POST", "GET"])
def submit_missing():
    veh_num = request.form['veh_num']
    dom = request.form['dom']
    pom = request.form['pom']
    # push into database - missing vehicle table
    if(veh_num!=None and dom!=None and pom!=None):
        missing_vehicle = MissingVehicle(veh_num, dom, pom, 'N')
        db.session.add(missing_vehicle)
        db.session.commit()
    return render_template("report_mveh.html", message=True)

if __name__=='__main__':
	app.run(debug=True)