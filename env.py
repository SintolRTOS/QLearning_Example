# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 23:21:46 2019

@author: wangjingyi
"""


"""
 3Q Learning 例子的 Maze（迷宫） 环境
 4黄色圆形 :   机器人
 5红色方形 :   炸弹     [reward = -1]
 6绿色方形 :   宝藏     [reward = +1]
 7其他方格 :   平地     [reward = 0]
"""
import sys
import time
import numpy as np
# Python2 和 Python3 中 Tkinter 的名称不一样
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

WIDTH = 4   # 迷宫的宽度
HEIGHT = 3  # 迷宫的高度
UNIT = 40   # 每个方块的大小（像素值）

# 迷宫 类
class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']  # 上，下，左，右 四个 action（动作）
        self.n_actions = len(self.action_space)   # action 的数目
        self.title('Q Learning')
        self.geometry('{0}x{1}'.format(WIDTH * UNIT, HEIGHT * UNIT))  # Tkinter 的几何形状
        self.build_maze()

    #创建迷宫
    def build_maze(self):
        # 创建画布 Canvas.白色背景，宽高。
        self.canvas = tk.Canvas(self, bg='white',
                                width=WIDTH * UNIT,
                                height=HEIGHT * UNIT)
        # 绘制横纵方格线。创建线条。
        for c in range(0, WIDTH * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, HEIGHT * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, HEIGHT * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, WIDTH * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)
        
        # 零点（左上角） 往右是x增长的方向。往左是y增长的方向。
        # 因为每个方格是40像素，20,20是中心位置。
        origin = np.array([20, 20])
        
        # 创建我们的探索者 机器人（robot）
        robot_center = origin + np.array([0, UNIT * 2])
        # 创建椭圆，指定起始位置。填充颜色
        self.robot = self.canvas.create_oval(
            robot_center[0] - 15, robot_center[1] - 15,
            robot_center[0] + 15, robot_center[1] + 15,
            fill='yellow')
        
        # 炸弹 1
        bomb1_center = origin + UNIT
        self.bomb1 = self.canvas.create_rectangle(
            bomb1_center[0] - 15, bomb1_center[1] - 15,
            bomb1_center[0] + 15, bomb1_center[1] + 15,
            fill='red')
        
        # 炸弹 2
        bomb2_center = origin + np.array([UNIT * 3, UNIT])
        self.bomb2 = self.canvas.create_rectangle(
            bomb2_center[0] - 15, bomb2_center[1] - 15,
            bomb2_center[0] + 15, bomb2_center[1] + 15,
            fill='red')
        
        # 宝藏
        treasure_center = origin + np.array([UNIT * 3, 0])
        self.treasure = self.canvas.create_rectangle(
            treasure_center[0] - 15, treasure_center[1] - 15,
            treasure_center[0] + 15, treasure_center[1] + 15,
            fill='green')
        
        # 设置好上面配置的场景
        self.canvas.pack()

    #reset方法表示游戏重新开始，机器人回到左下角
    # 重置（游戏重新开始，将机器人放到左下角）
    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.robot)  # 删去机器人
        origin = np.array([20, 20])
        robot_center = origin + np.array([0, UNIT * 2])
        # 重新创建机器人
        self.robot = self.canvas.create_oval(
            robot_center[0] - 15, robot_center[1] - 15,
            robot_center[0] + 15, robot_center[1] + 15,
            fill='yellow')
        # 返回 观测（observation）
        return self.canvas.coords(self.robot)
    
    # 走一步（机器人实施 action）
    def step(self, action):
        # s表示一个state状态值
        s = self.canvas.coords(self.robot)
        # 基准动作
        base_action = np.array([0, 0])
        if action == 0:     # 上
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # 下
            if s[1] < (HEIGHT - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # 右
            if s[0] < (WIDTH - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # 左
            if s[0] > UNIT:
                base_action[0] -= UNIT
        
        # 移动机器人，移动到baseation横向纵向坐标值
        self.canvas.move(self.robot, base_action[0], base_action[1])
        
        # 取得下一个 state
        s_ = self.canvas.coords(self.robot)
        
        # 奖励机制。
        if s_ == self.canvas.coords(self.treasure):
            reward = 1  # 找到宝藏，奖励为 1
            done = True
            s_ = 'terminal'   # 终止
            print("找到宝藏，好棒!")
        elif s_ == self.canvas.coords(self.bomb1):
            reward = -1  # 踩到炸弹1，奖励为 -1
            done = True
            s_ = 'terminal'   # 终止
            print("炸弹 1 爆炸...")
        elif s_ == self.canvas.coords(self.bomb2):
            reward = -1  # 踩到炸弹2，奖励为 -1
            done = True
            s_ = 'terminal'   # 终止
            print("炸弹 2 爆炸...")
        else:
            reward = 0   # 其他格子，没有奖励
            done = False
        
        return s_, reward, done
    
    # 调用 Tkinter 的 update 方法
    def render(self):
        time.sleep(0.1)
        self.update()