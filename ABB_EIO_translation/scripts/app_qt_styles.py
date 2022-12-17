# COLORS IN RGB
color_background = f'rgb(28, 32, 34)'
color_background_dialog = f'rgb(72, 73, 72)'
color_background_label = f'rgb(28, 32, 34)'
color_background_button = f'rgb(52, 53, 52)'
color_background_button_hover = f'rgb(72, 73, 72)'
color_background_drag_and_drop = f'rgb(164, 168, 164)'
color_background_edit_line = f'rgb(164, 168, 164)'

color_font_title = f'rgb(155,166,151)'
color_font_header = f'rgb(155,166,151)'
color_font_text = f'rgb(155,166,151)'
color_font_text_black = f'rgb(28, 32, 34)'
color_font_successful = f'rgb(155,166,151)'
color_font_error = f'rgb(155,166,151)'

color_border_of_buttons = f'rgb(83, 83, 83)'
color_border_of_labels = f'rgb(130, 130, 130)'

font = " bold 'Times New Roman'"
font_size_label = '20px'
font_size_label_descriptions = '15px'

border_radius = '10px'
border_button = '1px solid'
border_error_label = '2px solid FireBrick'
border_successful_label = '2px solid Green'


style_main_screen = f" background-color: {color_background};"
style_dialog_screen =   f"QWidget {{  " \
                        f"background-color: {color_background_dialog};" \
                        f"border-radius: {border_radius};"\
                        f"}}"
style_mian_widget = f" padding :10px;"
style_description_label =   f" color: {color_font_text};" \
                            f" font-size: {font_size_label};" \
                            f" font: {font};" \
                            f" border-radius: {border_radius};"\
                            f" min-width: 600px;" \
                            f" text-align: left;"

style_button = f"QPushButton {{background-color: {color_background_button};" \
                                f" color: {color_font_text};" \
                                f" font-size: {font_size_label_descriptions};" \
                                f" font: {font};" \
                                f" max-width: 150px;" \
                                f" min-width: 100px;" \
                                f" min-height: 25px;" \
                                f" text-align: center;" \
                                f" border: {border_button};"\
                                f" border-radius: {border_radius};"\
                                f" padding: 1px;" \
                                f" }}" \
                                f" QPushButton:hover {{"\
                                f" background-color: {color_background_button_hover};" \
                                f" color: {color_font_text};" \
                                f"}}"

style_label_error =         f" QLabel {{"\
                            f" background-color: {color_background_label};" \
                            f" color: {color_font_error};" \
                            f" font-size: {font_size_label_descriptions};" \
                            f" font: {font};" \
                            f" max-width: 400px;" \
                            f" qproperty-alignment: AlignCenter;"\
                            f" border: {border_error_label};"\
                            f" border-radius: {border_radius};"\
                            f"}}"

style_label_successful =    f" QLabel {{"\
                            f" background-color: {color_background_label};" \
                            f" color: {color_font_successful};" \
                            f" font-size: {font_size_label_descriptions};" \
                            f" font: {font};" \
                            f" max-width: 400px;" \
                            f" qproperty-alignment: AlignCenter;"\
                            f" border: {border_successful_label};"\
                            f" border-radius: {border_radius};"\
                            f"}}"

style_drag_and_drop_label = f" QLabel {{"\
                            f" background-color: {color_background_drag_and_drop};" \
                            f" color: {color_font_text_black};" \
                            f" font: {font};" \
                            f" font-size: {font_size_label};" \
                            f" border: {border_button};"\
                            f" border-radius: {border_radius};"\
                            f" max-width: 300px;" \
                            f" max-height: 300px;" \
                            f" min-width: 250px;" \
                            f" min-height: 100px;" \
                            f" qproperty-alignment: AlignCenter;"\
                            f"}}"

style_edit_line_browse_file =   f" QLineEdit {{"\
                                f" background-color: {color_background_edit_line};" \
                                f" color: {color_font_text_black};" \
                                f" border: {border_button};"\
                                f" border-radius: {border_radius};"\
                                f" font: {font};" \
                                f" min-width: 300px;" \
                                f" min-height: 25px;" \
                                f"}}"
style_select_file =         f" QLabel {{"\
                            f" background-color: {color_background_label};" \
                            f" color: {color_font_text};" \
                            f" font-size: {font_size_label_descriptions};" \
                            f" font: {font};" \
                            f" max-width: 800px;" \
                            f" qproperty-alignment: AlignLeft;"\
                            f" padding :1px;" \
                            f"}}"
style_checkbox = f"QRadioButton {{background-color: {color_background_label};" \
                                f" color: {color_font_text};" \
                                f" font-size: {font_size_label_descriptions};" \
                                f" font: {font};" \
                                f" max-width: 150px;" \
                                f" min-width: 100px;" \
                                f" min-height: 25px;" \
                                f" text-align: center;" \
                                f" border : 2px solid clack;"\
                                f" padding: 1px;" \
                                f" }}" \


