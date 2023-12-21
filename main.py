import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QLineEdit,QPushButton,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QMessageBox,QFileDialog
from PyQt5.QtGui import QPixmap,QIcon
import re
import tempfile
import qrcode



class QRBADGE(QMainWindow):
	def __init__(self):
		super().__init__()
		self.init_ui()
    
	def init_ui(self):
		create_icon = QIcon("icons/create.png")
		save_icon = QIcon("icons/save.png")
		cancel_icon = QIcon("icons/cancel.png")
		self.setWindowTitle('QR BADGE')
		self.setFixedSize(600,500)
		icon = QIcon("icons/badge.png")  
		self.setWindowIcon(icon)
		central_widget = QWidget()
		self.setCentralWidget(central_widget)

		self.layout = QVBoxLayout()
		central_widget.setLayout(self.layout) 



		self.name = QLineEdit()
		self.name.setPlaceholderText("NAME")

		self.email = QLineEdit()
		self.email.setPlaceholderText("EMAIL")

		self.github = QLineEdit()
		self.github.setPlaceholderText("Github")

		self.twitter = QLineEdit()
		self.twitter.setPlaceholderText("Twitter")

		self.qr_label = QLabel(self)
		self.qr_label.setFixedSize(200,200)


		
		self.qr_button = QPushButton("Create",self)
		self.qr_button.setFixedSize(130,30)
		self.qr_button.setIcon(create_icon)
		self.qr_button.clicked.connect(self.generate_qr)

		self.cancel_button = QPushButton("Cancel",self)
		self.cancel_button.setFixedSize(130,30)
		self.cancel_button.clicked.connect(self.cancel_qr)
		self.cancel_button.setIcon(cancel_icon)

		self.save_button = QPushButton("Save",self)
		self.save_button.setFixedSize(130,30)
		self.save_button.clicked.connect(self.save_qr)
		self.save_button.setIcon(save_icon)
	



		self.layout.addWidget(self.qr_label)
		self.layout.addWidget(self.name)
		self.layout.addWidget(self.email)
		self.layout.addWidget(self.twitter)	
		self.layout.addWidget(self.github)		
		self.layout.addWidget(self.qr_button)
		self.layout.addWidget(self.cancel_button)
		self.layout.addWidget(self.save_button)
		
	
	def generate_qr(self):
		self.required_check()
		name = self.name.text()
		email =self.email.text()
		twitter =self.twitter.text()
		github =self.github.text()
		if not self.is_valid_email(email):
			QMessageBox.warning(self,"INVALID EMAIL","PLEASE ENTER A VALID EMAIL")
			return
		
		if name and email:
			qr_data = f"Name: {name}\nEmail: {email}\nTwitter: https://twitter.com/{twitter}\nGithub: https://github.com/{github}"
			qr = qrcode.QRCode(
				version=1,
				error_correction=qrcode.constants.ERROR_CORRECT_L,
				box_size=10,
				border=4
				)
			qr.add_data(qr_data)
			qr.make(fit=True)
			self.img = qr.make_image(fill_color="black",back_color="white")
			

			temp_file = tempfile.NamedTemporaryFile(suffix=".png",delete=False)
			self.img.save(temp_file.name)

			pixmap = QPixmap(temp_file.name)
			self.qr_label.setPixmap(pixmap)
			self.qr_label.setScaledContents(True)
		   
	
	def cancel_qr(self):
		empty_pixmap = QPixmap()  
		self.qr_label.setPixmap(empty_pixmap)

	def save_qr(self):
		name = self.name.text()
		self.img.save(f"{name}.png")
		QMessageBox.information(self, "QR SAVED", "QR CODE HAS BEEN SAVED SUCCESSFULLY!")
		


	def required_check(self):
		name =  self.name.text().strip() 
		email =  self.email.text().strip() 

		if not name or not email:
			QMessageBox.warning(self, "Required Fields", "Please fill in both NAME and EMAIL fields.")
			return


	def is_valid_email(self,email):
		pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
		return re.match(pattern, email) is not None

			


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = QRBADGE()
	window.show()
	sys.exit(app.exec_())
