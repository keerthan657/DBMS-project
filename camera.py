import random
from main import db, Customer, Camera, Violation, Vehicle, CapturedVehicle, Captures, MissingVehicle
from datetime import date
import datetime
import cv2 as cv
import time
from nosql import get_amt
from ocr import get_numberplate
import smtplib
from alert import send_alert

# this script runs for one camera
# each camera has a unique camera number and some location info
class Camera_physical:
	# parameters
	camera_number = 0
	location_info = 'default location'

	# constructor
	def __init__(self, camera_number, location_info):
		self.camera_number = camera_number
		self.location_info = location_info

	# functions

	# it will get text by OCR
	def read_ocr(self):
		# some code to be written
		# TODO
		# for now, just return a random static value
		# vehicles = ['KA51H7654', 'KA47KL0098', 'KA41TI9098']
		# return random.choice(vehicles)
		img_path =  input('Enter image name / vehicle number: ')
		if('png' in img_path):
			return(get_numberplate(img_path))
		else:
			return(img_path)

	
	# helper function to print details of vehicle properly formatted
	def display_details(self, vehicle_entry):
		# number
		print('Vehicle Number : ', vehicle_entry.vehicle_num)
		# name
		print('Vehicle Name   : ', vehicle_entry.name)
		# color
		print('Color          : ', vehicle_entry.color)
		# customer's aadhar
		print('Customer aadhar: ', vehicle_entry.customer_aadhar)
		# customer's name
		temp = Customer.query.filter_by(aadhar_num=vehicle_entry.customer_aadhar).first()
		print('Customer name  : ', temp.first_name+' '+temp.last_name)
	
	# it will take update server database with info
	def update_database(self, vehicle_num, database):
		# add vehicle number to captured vehicle table
		# captured_vehicle = CapturedVehicle(vehicle_num)
		# database.session.add(captured_vehicle)
		# database.session.commit()

		# clip id
		clip_id = random.randint(1000, 9999)
		# temp = Captures.query.filter_by(vehicle_num=vehicle_num).all()
		db.session.add(Captures(self.camera_number, vehicle_num, clip_id))
		db.session.commit()

		# add vehicle number to captured vehicle table
		# try:
		# 	captured_vehicle = CapturedVehicle(vehicle_num)
		# 	db.session.add(captured_vehicle)
		# 	db.session.commit()
		# except Exception as e:
		# 	print("Warning : ", e)

		# check entry in VEHICLE table
		vehicle_entry = Vehicle.query.filter_by(vehicle_num=vehicle_num).first()
		# if found, print owner info and vehicle info
		if(vehicle_entry == None):
			print('No vehicle data found in database')
		else:
			print('Vehicle entry found - printing details...')
			self.display_details(vehicle_entry)

		# and check for any violations
		present_date = date.today()
		registration_expiry_date = vehicle_entry.registration_expiry
		insurance_expiry_date = vehicle_entry.insurance_expiry
		emissions_expiry_date = vehicle_entry.emissions_expiry

		# if any date surpassed - then violaiton - alco calculate fine amt and update appropriate tables
		# TODO: get fine rate from NoSql database - DONE
		total_fine_amt = 0
		if(insurance_expiry_date < present_date):
			print("Insurance expired!!    (Rs.",get_amt(1),")")
			#total_fine_amt = total_fine_amt + 100
			total_fine_amt = total_fine_amt + int(get_amt(1))
		if(registration_expiry_date < present_date):
			print("Registration expired!! (Rs.",get_amt(2),")")
			#total_fine_amt = total_fine_amt + 100
			total_fine_amt = total_fine_amt + int(get_amt(2))
		if(emissions_expiry_date < present_date):
			print("Emissions expired!!    (Rs.",get_amt(3),")")
			#total_fine_amt = total_fine_amt + 100
			total_fine_amt = total_fine_amt + int(get_amt(3))
		
		# update to VIOLATIONS table
		if(total_fine_amt>0):
			new_violation = Violation('license expiry', date.today(), datetime.datetime.now().time(), total_fine_amt, 'N', self.camera_number, clip_id, vehicle_num)
			database.session.add(new_violation)
			database.session.commit()
		else:
			print("No violations found")

		# and also check if the vehicle is missing
		missing_entry = MissingVehicle.query.filter_by(vehicle_num=vehicle_num).first()
		# if found as missing
		if(missing_entry!=None):
			print('Oh!! A stolen vehicle. Alerting now!!')
			# TODO: alert public and transport department - DONE
			# update as found in missing vehicle table
			missing_entry.is_found = 'Y'
			# send mail as alert
			try:
				send_alert(self.location_info)
			except Exception as e:
				print("Warning @ mail : ", e)
			database.session.commit()

if __name__=='__main__':
	my_camera = Camera_physical(12, 'somewhere')

	# camera will work continuously and fetch video
	# vid = cv.VideoCapture(0)
	while(True):
		# _, frame = vid.read()
		v_num = my_camera.read_ocr()
		my_camera.update_database(v_num, db)
		time.sleep(5)
		# if cv.waitKey(1) & 0xFF == ord('q'):
		# 	break
		print("")
	# vid.release()