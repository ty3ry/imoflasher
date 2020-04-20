import pygame as pg
import constant as c


class Frame():
	def __init__(self, screen, screen_w = 0, screen_h = 0):
    
		self.screen_w = screen_w
		self.screen_h = screen_h - 100

		self.screen = screen
		self.border_width = 3
		self.progress_bar_border_width = 3
		self.rect_background_title_h = 280
		
		self.init_frame()
		self.draw_component(self.screen)


		# percentage value
		self.percentage_line1 = 20
		self.percentage_line2 = 30
		self.percentage_line3 = 50
		self.percentage_line4 = 100

	def init_frame(self):
		# rectangle for line 1 control
		self.rect_line1_x = 0
		self.rect_line1_y = 0
		self.rect_line1_w = (self.screen_w/2)
		self.rect_line1_h = (self.screen_h/2)
		self.rect_line1_color = c.WHITE
		self.rect_line1_border_width = self.border_width

		# rectangle for line 2 control
		self.rect_line2_x = self.screen_w/2
		self.rect_line2_y = 0
		self.rect_line2_w = self.screen_w/2
		self.rect_line2_h = self.screen_h/2
		self.rect_line2_color = c.WHITE
		self.rect_line2_border_width = self.border_width

		# rectangle for line 3 control
		self.rect_line3_x = 0
		self.rect_line3_y = self.screen_h/2
		self.rect_line3_w = self.screen_w/2
		self.rect_line3_h = self.screen_h/2
		self.rect_line3_color = c.WHITE
		self.rect_line3_border_width = self.border_width

		# rectangle for line 4 control
		self.rect_line4_x = self.screen_w/2
		self.rect_line4_y = self.screen_h/2
		self.rect_line4_w = self.screen_w/2
		self.rect_line4_h = self.screen_h/2
		self.rect_line4_color = c.WHITE
		self.rect_line4_border_width = self.border_width

		# background title line1
		self.rect_background_title_line1_x = 0 + self.border_width
		self.rect_background_title_line1_y = 0 + self.border_width
		self.rect_background_title_line1_w = (self.screen_w / 2) - self.border_width -2
		self.rect_background_title_line1_h = ((self.screen_h/2) - self.rect_background_title_h) - self.border_width
		self.rect_background_title_line1_color = c.BLACK
		self.rect_background_title_line1_border_width = 0

		# background title line2
		self.rect_background_title_line2_x = self.screen_w/2 + self.border_width
		self.rect_background_title_line2_y = 0 + self.border_width
		self.rect_background_title_line2_w = (self.screen_w/2) - self.border_width - 2
		self.rect_background_title_line2_h = ((self.screen_h/2) - self.rect_background_title_h) - self.border_width
		self.rect_background_title_line2_color = c.BLACK
		self.rect_background_title_line2_border_width = 0

		# background title line3
		self.rect_background_title_line3_x = 0 + self.border_width
		self.rect_background_title_line3_y = (self.screen_h/2) + self.border_width
		self.rect_background_title_line3_w = (self.screen_w/2) - self.border_width -2
		self.rect_background_title_line3_h = ((self.screen_h/2) - self.rect_background_title_h) - self.border_width
		self.rect_background_title_line3_color = c.BLACK
		self.rect_background_title_line3_border_width = 0

		# background title line4
		self.rect_background_title_line4_x = self.screen_w/2 + self.border_width
		self.rect_background_title_line4_y = self.screen_h/2 + self.border_width
		self.rect_background_title_line4_w = self.screen_w/2 - self.border_width - 2
		self.rect_background_title_line4_h = ((self.screen_h/2) - self.rect_background_title_h) - self.border_width + 2
		self.rect_background_title_line4_color = c.BLACK
		self.rect_background_title_line4_border_width = 0

		# title label
		self.label_line1_title_template = pg.font.SysFont('comicsansms', 30)
		self.label_line1_title_template.set_bold(True)
		self.label_line1_title = self.label_line1_title_template.render("Line-1", 1 , c.WHITE)
		self.label_title_line1_x = (((self.screen_w/2)/2) - (self.label_line1_title.get_width()/2))
		self.label_title_line1_y = self.rect_background_title_line1_h/2/2

		self.label_line2_title_template = pg.font.SysFont('comicsansms', 30)
		self.label_line2_title_template.set_bold(True)
		self.label_line2_title = self.label_line2_title_template.render("Line-2", 1 , c.WHITE)
		self.label_title_line2_x = (self.screen_w - ((self.screen_w/2)/2) - (self.label_line2_title.get_width()/2))
		self.label_title_line2_y = self.rect_background_title_line2_h/2/2

		self.label_line3_title_template = pg.font.SysFont('comicsansms', 30)
		self.label_line3_title_template.set_bold(True)
		self.label_line3_title = self.label_line3_title_template.render("Line-3", 1 , c.WHITE)
		self.label_title_line3_x = (((self.screen_w/2)/2) - (self.label_line3_title.get_width()/2))
		self.label_title_line3_y = ((self.screen_h/2) + self.border_width) + (self.rect_background_title_line3_h/2/2)

		self.label_line4_title_template = pg.font.SysFont('comicsansms', 30)
		self.label_line4_title_template.set_bold(True)
		self.label_line4_title = self.label_line4_title_template.render("Line-4", 1 , c.WHITE)
		self.label_title_line4_x = (self.screen_w - ((self.screen_w/2)/2) - (self.label_line4_title.get_width()/2))
		self.label_title_line4_y = ((self.screen_h/2) + self.border_width) + (self.rect_background_title_line4_h/2/2)
		
		## status
		# label for flasher status template ( line 1 )
		self.label_flasher_status_line1_template = pg.font.SysFont('comicsansms', 35)
		self.label_flasher_status_line1_template.set_bold(False)
		self.label_flasher_status_line1 = self.label_flasher_status_line1_template.render("Status :", 1 , c.WHITE)
		self.label_flasher_status_line1_x = 20
		self.label_flasher_status_line1_y = 0 + 120

		# label for flasher status value ( line 1 )
		self.label_flasher_status_value_line1_template = pg.font.SysFont('comicsansms', 50)
		self.label_flasher_status_value_line1_template.set_bold(True)
		self.label_flasher_status_value_line1 = self.label_flasher_status_value_line1_template.render("{}:".format("---"), 1 , c.WHITE)
		self.label_flasher_status_value_line1_x = self.label_flasher_status_line1.get_width() + 80
		self.label_flasher_status_value_line1_y = 0 + 120

		# label for flasher status template ( line 2 )
		self.label_flasher_status_line2_template = pg.font.SysFont('comicsansms', 35)
		self.label_flasher_status_line2_template.set_bold(False)
		self.label_flasher_status_line2 = self.label_flasher_status_line2_template.render("Status :", 1 , c.WHITE)
		self.label_flasher_status_line2_x = (self.screen_w/2) + 20
		self.label_flasher_status_line2_y = 0 + 120

		# label for flasher status value ( line 2 )
		self.label_flasher_status_value_line2_template = pg.font.SysFont('comicsansms', 50)
		self.label_flasher_status_value_line2_template.set_bold(True)
		self.label_flasher_status_value_line2 = self.label_flasher_status_value_line2_template.render("{}:".format("---"), 1 , c.WHITE)
		self.label_flasher_status_value_line2_x = (self.screen_w/2) + self.label_flasher_status_line2.get_width() + 80
		self.label_flasher_status_value_line2_y = 0 + 120

		# label for flasher status template ( line 3 )
		self.label_flasher_status_line3_template = pg.font.SysFont('comicsansms', 35)
		self.label_flasher_status_line3_template.set_bold(False)
		self.label_flasher_status_line3 = self.label_flasher_status_line3_template.render("Status :", 1 , c.WHITE)
		self.label_flasher_status_line3_x = 20
		self.label_flasher_status_line3_y = (self.screen_h/2) + 120

		# label for flasher status value ( line 3 )
		self.label_flasher_status_value_line3_template = pg.font.SysFont('comicsansms', 50)
		self.label_flasher_status_value_line3_template.set_bold(True)
		self.label_flasher_status_value_line3 = self.label_flasher_status_value_line3_template.render("{}:".format("---"), 1 , c.WHITE)
		self.label_flasher_status_value_line3_x = self.label_flasher_status_line3.get_width() + 80
		self.label_flasher_status_value_line3_y = (self.screen_h/2) + 120

		# label for flasher status template ( line 4 )
		self.label_flasher_status_line4_template = pg.font.SysFont('comicsansms', 35)
		self.label_flasher_status_line4_template.set_bold(False)
		self.label_flasher_status_line4 = self.label_flasher_status_line4_template.render("Status :", 1 , c.WHITE)
		self.label_flasher_status_line4_x = (self.screen_w/2) + 20
		self.label_flasher_status_line4_y = (self.screen_h/2) + 120

		# label for flasher status value ( line 4 )
		self.label_flasher_status_value_line4_template = pg.font.SysFont('comicsansms', 50)
		self.label_flasher_status_value_line4_template.set_bold(True)
		self.label_flasher_status_value_line4 = self.label_flasher_status_value_line4_template.render("{}:".format("---"), 1 , c.WHITE)
		self.label_flasher_status_value_line4_x = (self.screen_w/2) + self.label_flasher_status_line4.get_width() + 80
		self.label_flasher_status_value_line4_y = (self.screen_h/2) + 120

		## label for time (line1)
		self.label_time_line1_template = pg.font.SysFont('comicsansms', 35)
		self.label_time_line1_template.set_bold(False)
		self.label_time_line1 = self.label_time_line1_template.render("{}".format("Time :"), 1 , c.WHITE)
		self.label_time_line1_x = 20
		self.label_time_line1_y = 160

		## label for time value (line1)
		self.label_time_value_line1_template = pg.font.SysFont('comicsansms', 50)
		self.label_time_value_line1_template.set_bold(False)
		self.label_time_value_line1 = self.label_time_value_line1_template.render("{}".format("12s"), 1 , c.WHITE)
		self.label_time_value_line1_x = self.label_flasher_status_line1.get_width() + 80          # relatif to label status
		self.label_time_value_line1_y = 160

		## label for time (line2)
		self.label_time_line2_template = pg.font.SysFont('comicsansms', 35)
		self.label_time_line2_template.set_bold(False)
		self.label_time_line2 = self.label_time_line2_template.render("{}".format("Time :"), 1 , c.WHITE)
		self.label_time_line2_x = (self.screen_w/2) + 20
		self.label_time_line2_y = 160

		## label for time value (line2)
		self.label_time_value_line2_template = pg.font.SysFont('comicsansms', 50)
		self.label_time_value_line2_template.set_bold(False)
		self.label_time_value_line2 = self.label_time_value_line2_template.render("{}".format("12s"), 1 , c.WHITE)
		self.label_time_value_line2_x = (self.screen_w/2) + (self.label_flasher_status_line1.get_width() + 80) # relatif to label status
		self.label_time_value_line2_y = 160

		## label for time (line3)
		self.label_time_line3_template = pg.font.SysFont('comicsansms', 35)
		self.label_time_line3_template.set_bold(False)
		self.label_time_line3 = self.label_time_line3_template.render("{}".format("Time :"), 1 , c.WHITE)
		self.label_time_line3_x = 20
		self.label_time_line3_y = (self.screen_h/2) + 160

		## label for time value (line3)
		self.label_time_value_line3_template = pg.font.SysFont('comicsansms', 50)
		self.label_time_value_line3_template.set_bold(False)
		self.label_time_value_line3 = self.label_time_value_line3_template.render("{}".format("12s"), 1 , c.WHITE)
		self.label_time_value_line3_x = self.label_flasher_status_line1.get_width() + 80        # relatif to label status
		self.label_time_value_line3_y = (self.screen_h/2) + 160

		## label for time (line4)
		self.label_time_line4_template = pg.font.SysFont('comicsansms', 35)
		self.label_time_line4_template.set_bold(False)
		self.label_time_line4 = self.label_time_line4_template.render("{}".format("Time :"), 1 , c.WHITE)
		self.label_time_line4_x = (self.screen_w/2) + 20
		self.label_time_line4_y = (self.screen_h/2) + 160

		## label for time value (line4)
		self.label_time_value_line4_template = pg.font.SysFont('comicsansms', 50)
		self.label_time_value_line4_template.set_bold(False)
		self.label_time_value_line4 = self.label_time_value_line4_template.render("{}".format("---"), 1 , c.WHITE)
		self.label_time_value_line4_x = (self.screen_w/2) + (self.label_flasher_status_line1.get_width() + 80)     # relatif to label status
		self.label_time_value_line4_y = (self.screen_h/2) + 160


		# label for progress template (line 1)
		self.label_flasher_progress_line1_template = pg.font.SysFont('comicsansms', 25)
		self.label_flasher_progress_line1_template.set_bold(False)
		self.label_flasher_progress_line1 = self.label_flasher_progress_line1_template.render("Progress", 1, c.WHITE)
		self.label_flasher_progress_line1_x = 20
		self.label_flasher_progress_line1_y = (self.screen_h/2) - 55

		# label for percentage (line1)
		self.label_flasher_percentage_line1_template = pg.font.SysFont('comicsansms', 25)
		self.label_flasher_percentage_line1_template.set_bold(False)
		self.label_flasher_percentage_line1 = self.label_flasher_percentage_line1_template.render("{}".format(0), 1 , c.WHITE)
		self.label_flasher_percentage_line1_x = (self.label_flasher_progress_line1.get_width() + 40 + (self.screen_w/3) + 20)
		self.label_flasher_percentage_line1_y = (self.screen_h/2) - 55

		# label for progress template (line 2)
		self.label_flasher_progress_line2_template = pg.font.SysFont('comicsansms', 25)
		self.label_flasher_progress_line2_template.set_bold(False)
		self.label_flasher_progress_line2 = self.label_flasher_progress_line2_template.render("Progress", 1, c.WHITE)
		self.label_flasher_progress_line2_x = (self.screen_w/2) + 20
		self.label_flasher_progress_line2_y = (self.screen_h/2) - 55

		# label for percentage (line 2)
		self.label_flasher_percentage_line2_template = pg.font.SysFont('comicsansms', 25)
		self.label_flasher_percentage_line2_template.set_bold(False)
		self.label_flasher_percentage_line2 = self.label_flasher_percentage_line2_template.render("{}".format(0), 1 , c.WHITE)
		self.label_flasher_percentage_line2_x = ((self.screen_w/2) + self.label_flasher_progress_line2.get_width() + 40 + (self.screen_w/3) + 20)
		self.label_flasher_percentage_line2_y = (self.screen_h/2) - 55

		# label for progress template (line 3)
		self.label_flasher_progress_line3_template = pg.font.SysFont('comicsansms', 25)
		self.label_flasher_progress_line3_template.set_bold(False)
		self.label_flasher_progress_line3 = self.label_flasher_progress_line3_template.render("Progress", 1, c.WHITE)
		self.label_flasher_progress_line3_x = 20
		self.label_flasher_progress_line3_y = ((self.screen_h/2)*2) - 55

		# label for percentage (line 3)
		self.label_flasher_percentage_line3_template = pg.font.SysFont('comicsansms', 25)
		self.label_flasher_percentage_line3_template.set_bold(False)
		self.label_flasher_percentage_line3 = self.label_flasher_percentage_line3_template.render("{}".format(0), 1 , c.WHITE)
		self.label_flasher_percentage_line3_x = (self.label_flasher_progress_line3.get_width() + 40 + (self.screen_w/3) + 20)
		self.label_flasher_percentage_line3_y = ((self.screen_h/2) *2) - 55

		# label for progress template (line 4)
		self.label_flasher_progress_line4_template = pg.font.SysFont('comicsansms', 25)
		self.label_flasher_progress_line4_template.set_bold(False)
		self.label_flasher_progress_line4 = self.label_flasher_progress_line4_template.render("Progress", 1, c.WHITE)
		self.label_flasher_progress_line4_x = (self.screen_w/2) + 20
		self.label_flasher_progress_line4_y = ((self.screen_h/2)*2) - 55

		# label for percentage (line 4)
		self.label_flasher_percentage_line4_template = pg.font.SysFont('comicsansms', 25)
		self.label_flasher_percentage_line4_template.set_bold(False)
		self.label_flasher_percentage_line4 = self.label_flasher_percentage_line4_template.render("{}".format(0), 1 , c.WHITE)
		self.label_flasher_percentage_line4_x = ((self.screen_w/2) + self.label_flasher_progress_line4.get_width() + 40 + (self.screen_w/3) + 20)
		self.label_flasher_percentage_line4_y = ((self.screen_h/2)*2) - 55


		# label for filename
		self.label_filename_template = pg.font.SysFont('comicsansms', 25)
		self.label_filename_template.set_bold(False)
		self.label_filename = self.label_filename_template.render("Filename :", 1 , c.WHITE)
		self.label_filename_x = 20
		self.label_filename_y =  ((self.screen_h/2) * 2) + 20

		# label for filename value
		self.label_filename_value_template = pg.font.SysFont('comicsansms', 70)
		self.label_filename_value_template.set_bold(False)
		self.label_filename_value = self.label_filename_value_template.render("{}".format("NAMA_FILE.xxx"), 1 , c.YELLOW)
		self.label_filename_value_x = self.label_filename.get_width() + 80
		self.label_filename_value_y = (((self.screen_h/2) * 2) + 35)

		# label for system state
		self.label_system_state_template = pg.font.SysFont('comicsansms', 25)
		self.label_system_state_template.set_bold(False)
		self.label_system_state = self.label_system_state_template.render("{}".format("State :"), 1 , c.WHITE)
		self.label_system_state_x = (self.screen_w/2) + 20
		self.label_system_state_y = ((self.screen_h/2) * 2) + 20

		# label for system state value
		self.label_system_state_value_template = pg.font.SysFont('comicsansms', 40)
		self.label_system_state_value_template.set_bold(False)
		self.label_system_state_value = self.label_system_state_value_template.render("{}".format("wkwkwkwkwkwkwkw"), 1 , c.WHITE)
		self.label_system_state_value_x = (self.screen_w/2) + 20
		self.label_system_state_value_y = (((self.screen_h/2) * 2) + 20) + 20

		# label for system error code (line1)
		self.label_line1_error_code_template = pg.font.SysFont('comicsansms', 30)
		self.label_line1_error_code_template.set_bold(False)
		self.label_line1_error_code = self.label_line1_error_code_template.render("E{}".format('--'), 1 , c.RED)
		self.label_line1_error_code_x = 0
		self.label_line1_error_code_y = 0

		# label for system error code (line2)
		self.label_line2_error_code_template = pg.font.SysFont('comicsansms', 30)
		self.label_line2_error_code_template.set_bold(False)
		self.label_line2_error_code = self.label_line2_error_code_template.render("E{}".format('--'), 1 , c.RED)
		self.label_line2_error_code_x = 0
		self.label_line2_error_code_y = 0

		# label for system error code (line3)
		self.label_line3_error_code_template = pg.font.SysFont('comicsansms', 30)
		self.label_line3_error_code_template.set_bold(False)
		self.label_line3_error_code = self.label_line3_error_code_template.render("E{}".format('--'), 1 , c.RED)
		self.label_line3_error_code_x = 0
		self.label_line3_error_code_y = 0

		# label for system error code (line4)
		self.label_line4_error_code_template = pg.font.SysFont('comicsansms', 30)
		self.label_line4_error_code_template.set_bold(False)
		self.label_line4_error_code = self.label_line4_error_code_template.render("E{}".format('--'), 1 , c.RED)
		self.label_line4_error_code_x = 0
		self.label_line4_error_code_y = 0

		# taskbar rectangle
		self.rect_taskbar_x = 0
		self.rect_taskbar_y = (self.screen_h/2) * 2
		self.rect_taskbar_w = self.screen_w
		self.rect_taskbar_h = self.screen_h - (self.screen_h-(self.screen_h/2*2))

		# taskbar border
		self.rect_taskbar_border_x = 0
		self.rect_taskbar_border_y = (self.screen_h/2) * 2
		self.rect_taskbar_border_w = self.screen_w
		self.rect_taskbar_border_h = self.screen_h - (self.screen_h-(self.screen_h/2*2))
		self.rect_taskbar_border_width = 3


		# rectangle for progress bar (line1)
		self.rect_progress_bar_line1_x = self.label_flasher_progress_line1.get_width() + 40
		self.rect_progress_bar_line1_y = (self.screen_h/2) - 60
		self.rect_progress_bar_line1_w = ((self.screen_w/3) - self.border_width)* 0
		self.rect_progress_bar_line1_h = 30

		# rectangle for progress bar (line2)
		self.rect_progress_bar_line2_x = (self.screen_w/2) + self.label_flasher_progress_line2.get_width() + 40
		self.rect_progress_bar_line2_y = (self.screen_h/2) - 60
		self.rect_progress_bar_line2_w = ((self.screen_w/3) - self.border_width)*0
		self.rect_progress_bar_line2_h = 30

		# rectangle for progress bar (line3)
		self.rect_progress_bar_line3_x = self.label_flasher_progress_line3.get_width() + 40
		self.rect_progress_bar_line3_y = ((self.screen_h/2) *2) - 60
		self.rect_progress_bar_line3_w = ((self.screen_w/3) - self.border_width)*0
		self.rect_progress_bar_line3_h = 30

		# rectangle for progress bar (line4)
		self.rect_progress_bar_line4_x = ((self.screen_w/2) + self.label_flasher_progress_line4.get_width() + 40)
		self.rect_progress_bar_line4_y = ((self.screen_h/2) *2) - 60
		self.rect_progress_bar_line4_w = ((self.screen_w/3) - self.border_width)*0
		self.rect_progress_bar_line4_h = 30

		# rect for progress bar (line1)
		self.rect_progress_bar_border_line1_x = self.label_flasher_progress_line1.get_width() + 40
		self.rect_progress_bar_border_line1_y = (self.screen_h/2) - 60
		self.rect_progress_bar_border_line1_w = ((self.screen_w/3) - self.border_width)* 1
		self.rect_progress_bar_border_line1_h = 30

		# rect for progress bar (line2)
		self.rect_progress_bar_border_line2_x = (self.screen_w/2) + self.label_flasher_progress_line2.get_width() + 40
		self.rect_progress_bar_border_line2_y = (self.screen_h/2) - 60
		self.rect_progress_bar_border_line2_w = ((self.screen_w/3) - self.border_width)*1
		self.rect_progress_bar_border_line2_h = 30

		# rect for progress bar (line3)
		self.rect_progress_bar_border_line3_x = self.label_flasher_progress_line3.get_width() + 40
		self.rect_progress_bar_border_line3_y = ((self.screen_h/2) *2) - 60
		self.rect_progress_bar_border_line3_w = ((self.screen_w/3) - self.border_width)*1
		self.rect_progress_bar_border_line3_h = 30

		# rect for progress bar (line4)
		self.rect_progress_bar_border_line4_x = ((self.screen_w/2) + self.label_flasher_progress_line4.get_width() + 40)
		self.rect_progress_bar_border_line4_y = ((self.screen_h/2) *2) - 60
		self.rect_progress_bar_border_line4_w = ((self.screen_w/3) - self.border_width)*1
		self.rect_progress_bar_border_line4_h = 30

	def update_progress_bar(self, progbar_line1, progbar_line2, progbar_line3, progbar_line4):

		progbar_line1 = (progbar_line1 / 100)
		progbar_line2 = (progbar_line2 / 100)
		progbar_line3 = (progbar_line3 / 100)
		progbar_line4 = (progbar_line4 / 100)

		# rectangle progress bar
		self.rect_progress_bar_line1_w = ((self.screen_w/3) - self.border_width)* progbar_line1
		self.rect_progress_bar_line2_w = ((self.screen_w/3) - self.border_width)* progbar_line2
		self.rect_progress_bar_line3_w = ((self.screen_w/3) - self.border_width)* progbar_line3
		self.rect_progress_bar_line4_w = ((self.screen_w/3) - self.border_width)* progbar_line4

		# percentage
		self.label_flasher_percentage_line1 = self.label_flasher_percentage_line1_template.render("{} % ".format(round(progbar_line1*100)), 1 , c.WHITE)
		self.label_flasher_percentage_line2 = self.label_flasher_percentage_line2_template.render("{} % ".format(round(progbar_line2*100)), 1 , c.WHITE)
		self.label_flasher_percentage_line3 = self.label_flasher_percentage_line3_template.render("{} % ".format(round(progbar_line3*100)), 1 , c.WHITE)
		self.label_flasher_percentage_line4 = self.label_flasher_percentage_line1_template.render("{} % ".format(round(progbar_line4*100)), 1 , c.WHITE)

	def update_status(self, status_line1, status_line2, status_line3, status_line4):
		# status value
		self.label_flasher_status_value_line1 = self.label_flasher_status_value_line1_template.render("{}".format(status_line1), 1 , c.WHITE)
		self.label_flasher_status_value_line2 = self.label_flasher_status_value_line2_template.render("{}".format(status_line2), 1 , c.WHITE)
		self.label_flasher_status_value_line3 = self.label_flasher_status_value_line3_template.render("{}".format(status_line3), 1 , c.WHITE)
		self.label_flasher_status_value_line4 = self.label_flasher_status_value_line4_template.render("{}".format(status_line4), 1 , c.WHITE)

	def update_filename(self, filename):
		self.label_filename_value = self.label_filename_value_template.render("{}".format(filename), 1 , c.YELLOW)

	def update_system_state(self, sys_state):
		self.label_system_state_value = self.label_system_state_value_template.render("{}".format(sys_state), 1 , c.WHITE)

	def update_time(self, time_line1, time_line2, time_line3, time_line4):
		self.label_time_value_line1 = self.label_time_value_line1_template.render("{}".format(time_line1), 1 , c.WHITE)
		self.label_time_value_line2 = self.label_time_value_line2_template.render("{}".format(time_line2), 1 , c.WHITE)
		self.label_time_value_line3 = self.label_time_value_line3_template.render("{}".format(time_line3), 1 , c.WHITE)
		self.label_time_value_line4 = self.label_time_value_line4_template.render("{}".format(time_line4), 1 , c.WHITE)

	def draw_component(self, screen):

		# draw label status
		screen.blit(self.label_flasher_status_line1, (self.label_flasher_status_line1_x, self.label_flasher_status_line1_y))
		screen.blit(self.label_flasher_status_line2, (self.label_flasher_status_line2_x, self.label_flasher_status_line2_y))
		screen.blit(self.label_flasher_status_line3, (self.label_flasher_status_line3_x, self.label_flasher_status_line3_y))
		screen.blit(self.label_flasher_status_line4, (self.label_flasher_status_line4_x, self.label_flasher_status_line4_y))

		# draw label status value
		screen.blit(self.label_flasher_status_value_line1, (self.label_flasher_status_value_line1_x, self.label_flasher_status_value_line1_y))
		screen.blit(self.label_flasher_status_value_line2, (self.label_flasher_status_value_line2_x, self.label_flasher_status_value_line2_y))
		screen.blit(self.label_flasher_status_value_line3, (self.label_flasher_status_value_line3_x, self.label_flasher_status_value_line3_y))
		screen.blit(self.label_flasher_status_value_line4, (self.label_flasher_status_value_line4_x, self.label_flasher_status_value_line4_y))

		# draw label progress
		screen.blit(self.label_flasher_progress_line1, (self.label_flasher_progress_line1_x, self.label_flasher_progress_line1_y))
		screen.blit(self.label_flasher_progress_line2, (self.label_flasher_progress_line2_x, self.label_flasher_progress_line2_y))
		screen.blit(self.label_flasher_progress_line3, (self.label_flasher_progress_line3_x, self.label_flasher_progress_line3_y))
		screen.blit(self.label_flasher_progress_line4, (self.label_flasher_progress_line4_x, self.label_flasher_progress_line4_y))

		# draw label percentage
		screen.blit(self.label_flasher_percentage_line1, (self.label_flasher_percentage_line1_x, self.label_flasher_percentage_line1_y))
		screen.blit(self.label_flasher_percentage_line2, (self.label_flasher_percentage_line2_x, self.label_flasher_percentage_line2_y))
		screen.blit(self.label_flasher_percentage_line3, (self.label_flasher_percentage_line3_x, self.label_flasher_percentage_line3_y))
		screen.blit(self.label_flasher_percentage_line4, (self.label_flasher_percentage_line4_x, self.label_flasher_percentage_line4_y))

		# draw label time
		screen.blit(self.label_time_line1, (self.label_time_line1_x, self.label_time_line1_y))
		screen.blit(self.label_time_line2, (self.label_time_line2_x, self.label_time_line2_y))
		screen.blit(self.label_time_line3, (self.label_time_line3_x, self.label_time_line3_y))
		screen.blit(self.label_time_line4, (self.label_time_line4_x, self.label_time_line4_y))

		# draw label time value
		screen.blit(self.label_time_value_line1, (self.label_time_value_line1_x, self.label_time_value_line1_y))
		screen.blit(self.label_time_value_line2, (self.label_time_value_line2_x, self.label_time_value_line2_y))
		screen.blit(self.label_time_value_line3, (self.label_time_value_line3_x, self.label_time_value_line3_y))
		screen.blit(self.label_time_value_line4, (self.label_time_value_line4_x, self.label_time_value_line4_y))

		# draw rect control
		pg.draw.rect(screen, c.WHITE, (
				self.rect_line1_x,
				self.rect_line1_y,
				self.rect_line1_w,
				self.rect_line1_h,
				
		),self.border_width)

		pg.draw.rect(screen, c.WHITE, (
				self.rect_line2_x,
				self.rect_line2_y,
				self.rect_line2_w,
				self.rect_line2_h,
				
		), self.border_width)
		pg.draw.rect(screen, c.WHITE, (
				self.rect_line3_x,
				self.rect_line3_y,
				self.rect_line3_w,
				self.rect_line3_h,
				
		), self.border_width)
		pg.draw.rect(screen, c.WHITE, (
				self.rect_line4_x,
				self.rect_line4_y,
				self.rect_line4_w,
				self.rect_line4_h,
				
		), self.border_width)

		# draw title bar
		pg.draw.rect(screen, c.BLACK, (
				self.rect_background_title_line1_x,
				self.rect_background_title_line1_y,
				self.rect_background_title_line1_w,
				self.rect_background_title_line1_h,
		))

		pg.draw.rect(screen, c.BLACK, (
				self.rect_background_title_line2_x,
				self.rect_background_title_line2_y,
				self.rect_background_title_line2_w,
				self.rect_background_title_line2_h,
		))

		pg.draw.rect(screen, c.BLACK,(
				self.rect_background_title_line3_x,
				self.rect_background_title_line3_y,
				self.rect_background_title_line3_w,
				self.rect_background_title_line3_h,
		))

		pg.draw.rect(screen, c.BLACK, (
				self.rect_background_title_line4_x,
				self.rect_background_title_line4_y,
				self.rect_background_title_line4_w,
				self.rect_background_title_line4_h,
		))

		# draw label title (line1)
		screen.blit(self.label_line1_title, (self.label_title_line1_x, self.label_title_line1_y))
		screen.blit(self.label_line2_title, (self.label_title_line2_x, self.label_title_line2_y))
		screen.blit(self.label_line3_title, (self.label_title_line3_x, self.label_title_line3_y))
		screen.blit(self.label_line4_title, (self.label_title_line4_x, self.label_title_line4_y))

		# draw taskbar rectangle
		pg.draw.rect(screen, c.BLACK,(
				self.rect_taskbar_x,
				self.rect_taskbar_y,
				self.rect_taskbar_w,
				self.rect_taskbar_h
		))

		# draw taskbar border
		pg.draw.rect(screen, c.WHITE,(
				self.rect_taskbar_border_x,
				self.rect_taskbar_border_y,
				self.rect_taskbar_border_w,
				self.rect_taskbar_border_h
		), 
		self.progress_bar_border_width)

		# draw progress bar
		pg.draw.rect(screen, c.WHITE,(
				self.rect_progress_bar_line1_x,
				self.rect_progress_bar_line1_y,
				self.rect_progress_bar_line1_w,
				self.rect_progress_bar_line1_h
		))

		pg.draw.rect(screen, c.WHITE,(
				self.rect_progress_bar_line2_x,
				self.rect_progress_bar_line2_y,
				self.rect_progress_bar_line2_w,
				self.rect_progress_bar_line2_h
		))

		pg.draw.rect(screen, c.WHITE,(
				self.rect_progress_bar_line3_x,
				self.rect_progress_bar_line3_y,
				self.rect_progress_bar_line3_w,
				self.rect_progress_bar_line3_h
		))

		pg.draw.rect(screen, c.WHITE,(
				self.rect_progress_bar_line4_x,
				self.rect_progress_bar_line4_y,
				self.rect_progress_bar_line4_w,
				self.rect_progress_bar_line4_h
		))

		# draw progressbar border
		pg.draw.rect(screen, c.GRAY,(
				self.rect_progress_bar_border_line1_x,
				self.rect_progress_bar_border_line1_y,
				self.rect_progress_bar_border_line1_w,
				self.rect_progress_bar_border_line1_h
		),
		self.progress_bar_border_width)

		pg.draw.rect(screen, c.GRAY,(
				self.rect_progress_bar_border_line2_x,
				self.rect_progress_bar_border_line2_y,
				self.rect_progress_bar_border_line2_w,
				self.rect_progress_bar_border_line2_h
		),
		self.progress_bar_border_width)

		pg.draw.rect(screen, c.GRAY,(
				self.rect_progress_bar_border_line3_x,
				self.rect_progress_bar_border_line3_y,
				self.rect_progress_bar_border_line3_w,
				self.rect_progress_bar_border_line3_h
		),
		self.progress_bar_border_width)

		pg.draw.rect(screen, c.GRAY,(
				self.rect_progress_bar_border_line4_x,
				self.rect_progress_bar_border_line4_y,
				self.rect_progress_bar_border_line4_w,
				self.rect_progress_bar_border_line4_h
		),
		self.progress_bar_border_width)

		# draw label filename
		screen.blit(self.label_filename, (self.label_filename_x, self.label_filename_y))
		
		# draw label filename value
		screen.blit(self.label_filename_value, (self.label_filename_value_x, self.label_filename_value_y))

		# draw label system state
		screen.blit(self.label_system_state, (self.label_system_state_x, self.label_system_state_y))

		# draw label system state value
		screen.blit(self.label_system_state_value, (self.label_system_state_value_x, self.label_system_state_value_y))

	def run(self):
		self.screen.fill(c.NAVYBLUE) 

		# draw component
		# self.update_filename("ABCDEF.xxx")
		# self.update_progress_bar(self.percentage_line1, self.percentage_line2, self.percentage_line3, self.percentage_line4)
		# self.update_status("IDLE", "IDLE", "RUN", "BUSY")
		# self.update_system_state("Lorem Dolor Ipsum,...")

		self.draw_component(self.screen)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				return
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					pg.quit()
					return

		pg.display.update()
