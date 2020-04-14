import pygame as pg
import constant as c


class Frame():
    def __init__(self, screen_w = 0, screen_h = 0):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.border_width = 3
        self.rect_background_title_h = 280
        
        self.init_frame()

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
        self.rect_background_title_line1_w = (self.screen_w / 2) - self.border_width
        self.rect_background_title_line1_h = ((self.screen_h/2) - self.rect_background_title_h) - self.border_width
        self.rect_background_title_line1_color = c.BLACK
        self.rect_background_title_line1_border_width = 0

        # background title line2
        self.rect_background_title_line2_x = self.screen_w/2 + self.border_width
        self.rect_background_title_line2_y = 0 + self.border_width
        self.rect_background_title_line2_w = (self.screen_w/2) - self.border_width + 2
        self.rect_background_title_line2_h = ((self.screen_h/2) - self.rect_background_title_h) - self.border_width
        self.rect_background_title_line2_color = c.BLACK
        self.rect_background_title_line2_border_width = 0

        # background title line3
        self.rect_background_title_line3_x = 0 + self.border_width
        self.rect_background_title_line3_y = (self.screen_h/2) + self.border_width
        self.rect_background_title_line3_w = (self.screen_w/2) - self.border_width
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
        self.label_line1_title = self.label_line1_title.render("Line-1", 1 , c.WHITE)
        self.label_title_line1_x = (((self.screen_w/2)/2) - (label_line1_title.get_width()/2))
        self.label_title_line1_y = 20

        self.label_line2_title_template = pg.font.SysFont('comicsansms', 30)
        self.label_line2_title_template.set_bold(True)
        self.label_line2_title = self.label_line2_title.render("Line-2", 1 , c.WHITE)
        self.label_title_line2_x = (self.screen_w - ((self.screen_w/2)/2) - (label_line2_title.get_width()/2))
        self.label_title_line2_y = 20

        self.label_line3_title_template = pg.font.SysFont('comicsansms', 30)
        self.label_line3_title_template.set_bold(True)
        self.label_line3_title = self.label_line3_title.render("Line-3", 1 , c.WHITE)
        self.label_title_line3_x = (((self.screen_w/2)/2) - (label_line3_title.get_width()/2))
        self.label_title_line3_y = ((self.screen_h/2) + self.border_width) + 20

        self.label_line4_title_template = pg.font.SysFont('comicsansms', 30)
        self.label_line4_title_template.set_bold(True)
        self.label_line4_title = self.label_line4_title.render("Line-4", 1 , c.WHITE)
        self.label_title_line4_x = (self.screen_w - ((self.screen_w/2)/2) - (label_line4_title.get_width()/2))
        self.label_title_line4_y = ((self.screen_h/2) + self.border_width) + 20
        
        # label for flasher status template ( line 1 )
        self.label_flasher_status_line1_template = pg.font.SysFont('comicsansms', 35)
        self.label_flasher_status_line1_template.set_bold(False)
        self.label_flasher_status_line1 = self.label_flasher_status_line1_template.render("Status :")
        self.label_flasher_status_line1_x = (self.screen_w/2) + 20
        self.label_flasher_status_line1_y = (self.screen_h/2) + 160

        # label for flasher status value ( line 1 )
        self.label_flasher_status_value_line1_template = pg.font.SysFont('comicsansms', 50)
        self.label_flasher_status_value_line1_template.set_bold(True)
        self.label_flasher_status_value_line1_x = (self.screen_w/2) + self.label_flasher_status_line1.get_width() + 80
        self.label_flasher_status_value_line1_y = 0


        # label for progress template
        self.label_flasher_progress_template = pg.font.SysFont('comicsansms', 25)
        self.label_flasher_progress_template.set_bold(False)
        self.label_flasher_progress_x = 0
        self.label_flasher_progress_y = 0

        # label for percentage
        self.label_flasher_percentage_template = pg.font.SysFont('comicsansms', 25)
        self.label_flasher_percentage_template.set_bold(False)
        self.label_flasher_percentage = self.label_flasher_percentage_template.render("{}".format(0), 1 , c.WHITE)
        self.label_flasher_percentage_x = 0
        self.label_flasher_percentage_y = 0

        # label for filename
        self.label_filename_template = pg.font.SysFont('comicsansms', 25)
        self.label_filename_template.set_bold(False)
        self.label_filename = self.label_filename_template.render("Filename :", 1 , c.WHITE)
        self.label_filename_x = 0
        self.label_filename_y = 0

        # label for filename value
        self.label_filename_value_template = pg.font.SysFont('comicsansms', 50)
        self.label_filename_value_template.set_bold(False)
        self.label_filename_value = self.label_filename_value_template.render("{}".format("-"), 1 , c.WHITE)
        self.label_filename_value_x = 0
        self.label_filename_value_y = 0

        # label for system state
        self.label_system_state_template = pg.font.SysFont('comicsansms', 25)
        self.label_system_state_template.set_bold(False)
        self.label_system_state = self.label_system_state_template.render("{}".format("NAMA_FILE.xxx"), 1 , c.WHITE)
        self.label_system_state_x = 0
        self.label_system_state_y = 0

        # label for system state value
        self.label_system_state_value_template = pg.font.SysFont('comicsansms', 40)
        self.label_system_state_value_template.set_bold(False)
        self.label_system_state_value = self.label_system_state_value_template.render("{}".format("wkwkwkwkwkwkwkw"), 1 , c.WHITE)
        self.label_system_state_value_x = 0
        self.label_system_state_value_y = 0

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


        # rectangle for progress bar (line1)
        self.rect_progress_bar_line1_x = 0
        self.rect_progress_bar_line1_y = 0
        self.rect_progress_bar_line1_w = 0
        self.rect_progress_bar_line1_h = 0

        # rectangle for progress bar (line2)
        self.rect_progress_bar_line2_x = 0
        self.rect_progress_bar_line2_y = 0
        self.rect_progress_bar_line2_w = 0
        self.rect_progress_bar_line2_h = 0

        # rectangle for progress bar (line1)
        self.rect_progress_bar_line3_x = 0
        self.rect_progress_bar_line3_y = 0
        self.rect_progress_bar_line3_w = 0
        self.rect_progress_bar_line3_h = 0

        # rectangle for progress bar (line1)
        self.rect_progress_bar_line4_x = 0
        self.rect_progress_bar_line4_y = 0
        self.rect_progress_bar_line4_w = 0
        self.rect_progress_bar_line4_h = 0

        # rect for progress bar (line1)
        self.rect_progress_bar_border_line1_x = 0
        self.rect_progress_bar_border_line1_y = 0
        self.rect_progress_bar_border_line1_w = 0
        self.rect_progress_bar_border_line1_h = 0

        # rect for progress bar (line2)
        self.rect_progress_bar_border_line2_x = 0
        self.rect_progress_bar_border_line2_y = 0
        self.rect_progress_bar_border_line2_w = 0
        self.rect_progress_bar_border_line2_h = 0

        # rect for progress bar (line1)
        self.rect_progress_bar_border_line3_x = 0
        self.rect_progress_bar_border_line3_y = 0
        self.rect_progress_bar_border_line3_w = 0
        self.rect_progress_bar_border_line3_h = 0

        # rect for progress bar (line1)
        self.rect_progress_bar_border_line4_x = 0
        self.rect_progress_bar_border_line4_y = 0
        self.rect_progress_bar_border_line4_w = 0
        self.rect_progress_bar_border_line4_h = 0

    def draw_component(self):
        # draw label title (line1)
        pass
