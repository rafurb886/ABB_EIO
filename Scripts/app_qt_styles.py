# COLORS IN RGB
color_background = 'Gainsboro'
color_background_label = f'Gainsboro'
color_background_button_hover = f'rgb(120, 120, 120)'
color_background_button = f'rgb(140, 140, 140)'
color_background_drag_and_drop = 'LightSlateGray'
color_border_of_buttons = f'rgb(83, 83, 83)'
color_border_of_labels = f'rgb(130, 130, 130)'
color_font_title = f'rgb(83, 83, 83)'
color_font_header = f'rgb(83, 83, 83)'
color_font_text = f'rgb(35, 35, 35)'

style_main_screen = f" background-color: {color_background};"
style_mian_widget = f" padding :140px;"
style_description_label = f" background-color: {color_background_label};" \
                          f" color: {color_font_text};" \
                          f" font-size: 25px;" \
                          f" font: bold italic 'Times New Roman';" \
                          f" min-width: 600px;" \
                          f" text-align: left;"
style_button_search_file =      f"QPushButton {{background-color: {color_background_button};" \
                    f" color: {color_font_text};" \
                    f" font-size: 15px;" \
                    f" font: bold italic 'Times New Roman';" \
                    f" max-width: 300px;" \
                    f" text-align: center;" \
                    f" }}" \
                    f" QPushButton:hover {{"\
                    f" background-color: {color_background_button_hover};" \
                    f" color: {color_font_text}" \
                    f"}}"
style_button_convert = f"QPushButton {{background-color: {color_background_button};" \
                    f" color: Black;" \
                    f" font-size: 15px;" \
                    f" font: bold italic 'Times New Roman';" \
                    f" max-width: 300px;" \
                    f" text-align: center;" \
                    f" }}" \
                    f" QPushButton:hover {{"\
                    f" background-color: {color_background_button_hover};" \
                    f" color: Black" \
                    f"}}"
style_check_box =   f" QCheckBox {{"\
                    f" color: {color_font_text};" \
                    f" font-size: 25px;" \
                    f" font: bold italic 'Times New Roman';" \
                    f" max-width: 400px;" \
                    f" mix-width: 400px;" \
                    f" text-align: center;" \
                    f" padding :10px;" \
                    f" }}"

style_label_error =         f" QLabel {{"\
                            f" background-color: {color_background_label};" \
                            f" color: FireBrick;" \
                            f" font-size: 15px;" \
                            f" font: bold italic 'Times New Roman';" \
                            f" max-width: 400px;" \
                            f" qproperty-alignment: AlignCenter;"\
                            f" border: 2px solid FireBrick"\
                            f"}}"

style_label_successful =    f" QLabel {{"\
                            f" background-color: {color_background_label};" \
                            f" color: green;" \
                            f" font-size: 15px;" \
                            f" font: bold italic 'Times New Roman';" \
                            f" max-width: 400px;" \
                            f" qproperty-alignment: AlignCenter;"\
                            f" border: 2px solid green"\
                            f"}}"

style_drag_and_drop_label = f" QLabel {{"\
                            f" background-color: {color_background_drag_and_drop};" \
                            f" color: white;"\
                            f" font: bold italic 'Times New Roman';" \
                            f" border-radius: 5px;"\
                            f" max-width: 300px;" \
                            f" max-height: 300px;" \
                            f" min-width: 250px;" \
                            f" min-height: 100px;" \
                            f" qproperty-alignment: AlignCenter;"\
                            f"}}"

style_edit_line_browse_file = f" QLineEdit {{"\
                            f" background-color: white;" \
                            f" min-width: 300px;" \
                            f"}}"
style_select_file =         f" QLabel {{"\
                            f" background-color: {color_background_label};" \
                            f" color: Black;" \
                            f" font-size: 10px;" \
                            f" font: bold italic 'Times New Roman';" \
                            f" max-width: 400px;" \
                            f" qproperty-alignment: AlignLeft;"\
                            f" padding :1px;" \
                            f"}}"