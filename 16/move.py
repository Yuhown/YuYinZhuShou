from util import DCmotor_control
from util import DCservo_control

def move(info):
    if '左手' in info:
        answer_text = '举左手'
        DCservo_control.raise_left_hand()
    elif '右手' in info :
        answer_text = '举右手'
        DCservo_control.raise_right_hand()
    elif '前'in info  :
        answer_text = '前进'
        DCmotor_control.car_forward()
        DCmotor_control.stop()
    elif '后' in info :
        answer_text = '后退'
        DCmotor_control.car_backward()
        DCmotor_control.stop()
    elif '左转' in info   :
        answer_text = '左转'
        DCmotor_control.car_left()
        DCmotor_control.stop()
    elif '右转' in info  :
        answer_text = '右转'
        DCmotor_control.car_right()
        DCmotor_control.stop()
    elif '转圈' in info  :
        answer_text = '转圈'
        DCmotor_control.around_right()
        DCmotor_control.stop()
    elif '摇头' in info  :
        answer_text = '头摇得好晕啊'
        DCservo_control.shake_head()
    else:
        answer_text = None
    return answer_text

