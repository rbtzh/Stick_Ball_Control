#############################################
# THE STICK-BALL MODEL for NUEDC at XUPT
# YEAR OF 2023
#
# 全国大学生电子设计竞赛
# 西安邮电大学校赛，2023年
# 棍球模型（控制题，C题）
#
# 队长 黄耀科 电科2102班 03212042 通信与信息工程学院
# 队员 赵彦博 通工2108班 03201274 通信与信息工程学院
# 队员 李嘉明 物联网2102班 03217041 通信与信息工程学院
# 指导教师 何在民 通信与信息工程学院
#
# 北斗智能时空信息技术实验室
#
# 主要硬件
# - OpenMV H7 running MicroPython
# - MG995 180ver
# - Matrix Keyboard
# - SSD1306 OLED Screen
# - 结构件若干（杜邦线，PVC管，etc）
# - 对生命的热爱
#
# 祝世界和平
# 最后编辑者 赵彦博
#############################################

# 1 Init Program
# 1.1 Import Packages
import sensor, image, time, math
from time import sleep as 等待
from pyb import millis as 系统运行时间
from pyb import Servo

# 1.2 Init OpenMV Sensor
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 1000) #延迟1秒等待摄像头校准亮度、白平衡
sensor.set_auto_whitebal(False) #关闭自动白平衡
sensor.set_auto_gain(True)    #降低曝光度
sensor.set_contrast(3)  #提高对比度
sensor.set_brightness(-3)   #降低亮度

# 1.3 Declare Consts

# The threshold of LAB to identify ball
ball_lab = (0, 100, -97, 127, 35 , 127) #yellow

# Consts relate to PID control
画面中点=(320/2,240/2)
舵机中点=-7
舵机范围=(-30 ,30)
比例P系数=0.4  #0.3
积分I系数=0.25 #0.18
微分D系数=0.235 #0.39
积分I最大值=5  #5

# Objects related to hardware control, GPIO, Display, etc
# Instantiate the Servo class
servo_object = Servo(1)

# Steps instruction list, contains steps=
STEP_INSTRUCTION_LIST = [
    [[1,30]],
    [[2,30]],
    [[4,30]],
    [[1,15],[2,30]],
    [[2,15],[4,30]],
    [],
    [[3,15],[1,15],[3,15],[1,15],[3,15],[1,15],[3,15],[1,15],[4,30]],
    [[2,90]]
    ]

SPECIAL_INDEX_NEED_INPUT = [5]
SPECIAL_INDEX_NEED_AGGRESSIVE_PID = [7]
SPECIAL_CHECK_LIST = [SPECIAL_INDEX_NEED_INPUT,SPECIAL_INDEX_NEED_AGGRESSIVE_PID]

# void move_platform( float:degree )
# move platform (the PVC Pipe) to given degree,
# with limit declared in 舵机范围
# and middle degree (to leveling system at init status) declared in 舵机中点
def move_platform(x):
    global 舵机范围,舵机中点

    if x<舵机范围[0]:
        x=舵机范围[0]
    if x>舵机范围[1]:
        x=舵机范围[1]

    servo_object.angle(舵机中点-x)    #x轴，向右减小
    print("platform moved")
    print("x: " + str(x))

# list get_target_pisition_list(void)
# use openmv and AprilTag to get the position of target areas in framebuffer
# return a list contains 5 int element, descending order
# example: [213,160,115,65,25], so the position of area 1 is list[0]
def get_target_pisition_list():
    #FISTHIS use openmv and AprilTag to get the position of target areas in framebuffer
    return [213,160,115,65,25]

# void display_data(string)
# 0: print to terminal
# 1: print to ssd1306
def display_data(display_content, methodlist = []):
    #FIXTHIS display someting to SSD1306 OLED
    print(display_content)

# int input_data(string)
# return [0...7], but input [1...8]
# methidlist is a list, default to 0
# 0: from terminal input function
# 1: from enternal keyboard
def input_data(input_prompt, method = 0):
    if method == 0:
        print(input_prompt)
        i = input()
    elif method == 1:
        i = 1
        while True:
            #FIXTHIS
            if pressed_key == ok_key:
                break
            elif pressed_key == up_arrow_key:
                if i+1 > len(STEP_INSTRUCTION_LIST):
                    i = 1
                else:
                    i += 1
            elif pressed_key == down_arrow_key:
                if i-1 < 1:
                    i = len(STEP_INSTRUCTION_LIST)
                else:
                    i -= 1
            else:
                pass
    else:
        pass
    return i - 1              

# class of a mission
# a mission is an independent program, run given step list step by step
class Mission:
    '所有 mission 的基类'
    def __init__(self, question_index, step_instruction_list, special_check_list):
        self.question_index = question_index
        self.step_instruction_list = step_instruction_list
        self.special_check_list = special_check_list

        #Pre-Modify-Check
        self.check_special_index()
        self.steps = self.get_steps_from_step_instruction_list()

    # Check if index is in SPECIAL_CHECK_LIST, if so, change properties
    def check_special_index(self):
        if self.question_index in self.special_check_list[0]:
            self.isNeedInput = True
        else:
            self.isNeedInput = False
        if self.question_index in self.special_check_list[1]:
            self.isNeedAggressivePID = True
        else:
            self.isNeedAggressivePID = False

    def get_steps_from_step_instruction_list(self):
        stepslist = []
        if self.isNeedInput:
            for c in ["A","B","C","D"]:
                stepslist.append(input_data("Please input " + c))
        else:
            stepslist = self.step_instruction_list[self.question_index]
        return stepslist

    #smallest cycle
    #[target:int, timeout_us:int]
    def one_step(step_info):
        target_position = target_position_list[step_info[0]]

        ball_position=0
        比例P=0
        积分I=0
        微分D=0
        偏差量=0
        上一次偏差量=0
        执行量=0
        计时=系统运行时间()
        time_step_start = 系统运行时间()

        while(True):
            时刻 = 系统运行时间()
            display_data("Time in one step: " + str(时刻 - time_step_start))
            if 时刻 > time_step_start + step_info[1]:
                return "Timeout"
            else:
                img = sensor.snapshot()
                ball_blobs = img.find_blobs([ball_lab])
                if ball_blobs:#如果找到结果
                    ball_blob = max(ball_blobs, key = lambda b: b.pixels())#按结果的像素值，找最大值的数据。也就是找最大的色块。
                    if ball_blob.w()>5 and ball_blob.h()>5:#过滤掉长宽小于10的结果 #FIXTHIS
                        #img.draw_rectangle(ball_blob[0:4],color=(255,0,0))#按寻找色块结果的前四个值，绘制方形，框选识别结果。
                        img.draw_line(0,ball_blob.cy(), 320, ball_blob.cy(),color=(255,0,0))#用结果的中心值坐标，绘制十字
                        ball_position=ball_blob.cy()
                    else:#没有找到小球
                        积分I=0   #积分I清零
                        ball_position=target_position #告知系统小球达到目标，使系统停转
                else:#没有找到小球
                    积分I=0   #积分I清零
                    ball_position=target_position

                运行时间=(系统运行时间()-计时)/1000
                计时=系统运行时间()
                控制时间_ms = (系统运行时间() - 程序开启时刻)
                print("runtime" + str(控制时间_ms))
                偏差量=target_position-ball_position

                比例P=偏差量*比例P系数

                积分I=积分I+偏差量*积分I系数*运行时间

                if 积分I>积分I最大值:
                    积分I=积分I最大值
                elif 积分I<-积分I最大值:
                    积分I=-积分I最大值

                微分D=(偏差量-上一次偏差量)*微分D系数/运行时间
                上一次偏差量=偏差量

                执行量=比例P+积分I+微分D
            #4）控制平台-执行量输入执行器
                move_platform(执行量)
                #手动调平
                #move_platform(10,-18)
                img.draw_string(0,0,'ERR:'+str(偏差量),color=(255,0,0))
                img.draw_string(0,10,'P:'+str(比例P),color=(255,0,0))
                img.draw_string(0,20,'I:'+str(积分I),color=(255,0,0))
                img.draw_string(0,30,'D:'+str(微分D),color=(255,0,0))
                for target_pos in target_position_list:
                    img.draw_line(0,target_pos,320,target_pos,thickness=1,color=(255,255,0))#用结果的中心值坐标，绘制十字

    #step: [target:int, timeout_ms:int]
    def step_by_step(self):
        for step in self.steps:
            self.one_step(step)

    def run(self):
        self.step_by_step()

#System Startup Routine
move_platform(0)
target_position_list = get_target_pisition_list()
程序开启时刻 = 系统运行时间()

while(True):
    mission_index = input_data("Which mission do you want to experience?")
    current_mission = Mission(mission_index, STEP_INSTRUCTION_LIST, SPECIAL_CHECK_LIST)
    current_mission.run()
