from PicoBorgRev import PicoBorgRev

class basic_controls():
	def __init__(self):
	    self.ctl = PicoBorgRev()
	    self.ctl.Init()

	def go(self, power=0.25):
	    self.ctl.SetMotors(power)

	def stop(self):
	    self.ctl.SetMotors(0)
	    
	def right(self, power=0.5):
	    self.ctl.SetMotor1(power)
	    
	def left(self, power=0.5):
	    self.ctl.SetMotor2(power)
	    
	def back(self, power=-0.25):
	    self.ctl.SetMotors(power)
