
global_qt_app_run = None
global_waiting_for_user_new_param = False
global_desc_wrong_param = ''
global_new_user_param = ''

def init():
    global global_qt_app_run
    global global_waiting_for_user_new_param
    global global_desc_wrong_param
    global global_new_user_param

    global_qt_app_run = False
    global_waiting_for_user_new_param = False
    global_desc_wrong_param = ''
    global_new_user_param = ''

if __name__ == '__main__':
    init()
