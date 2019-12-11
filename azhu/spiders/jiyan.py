
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: yanzhipeng
# @Date:   2019-12-04 15:56:28
# @Last Modified by:   yanzhipeng
# @Last Modified time: 2019-12-10 16:20:49

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import base64, random, sys
from PIL import Image
import cv2
import numpy as np


class ZhuFang():

    def __init__(self):
        self.url = "https://callback.58.com/antibot/verifycode?serialId=411b215e22e6032936692fa9030a8f89_a347edf6009d483094dfb4fda36dfaf1&code=22&sign=8acdbf7abf3a34f4a8516a24a6687b54&namespace=chuzulistphp&url=sh.58.com%2Fchuzu%2F0%2F%3FPGTID%3D0d3090a7-0000-2d1a-2a2b-0670cb32f27e%26ClickID%3D2"
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        self.browser = webdriver.Chrome(options=option)
        self.wait = WebDriverWait(self.browser, 20)

    def __del__(self):
        cv2.destroyAllWindows()
        self.browser.close()

    def get_distance(self, image):
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        # 边缘检测
        canny = cv2.Canny(blurred, 200, 400)
        cv2.imshow('canny', canny)
        is_true = 0
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i, contour in enumerate(contours):
            M = cv2.moments(contour)
            print("----->", cv2.contourArea(contour), cv2.arcLength(contour, True))
            if 1250 < cv2.contourArea(contour) < 1900 and 150 < cv2.arcLength(contour, True) < 250:
                is_true = 1
                draw_img = image.copy()
                # print(">>>>>", type(contour), contour)
                ret = cv2.drawContours(draw_img, [contour], -1, (0, 0, 255), 1)
                cv2.imshow('ret', ret)
                contour.sort(axis=0)

                min_x_road = contour[0, 0][0]

                print("min load is -", min_x_road)
                return min_x_road

        if 0 == is_true:
            cv2.destroyAllWindows()
            # self.browser.close()
            time.sleep(2)
            print("重新开始了")

            self.main()

    def get_track(self, x_distance):
        x_distance += 20
        track = []  # 移动轨迹
        current = 0  # 当前位移
        # 减速阈值
        mid = x_distance * (4 / 5)  # 前4/5段加速 后1/5段减速
        t = 0.08  # 计算间隔
        v = 0  # 初速度
        while current < x_distance:
            if current < mid:
                a = random.randint(9, 15)  # 加速度 a = 3
            else:
                a = random.randint(-20, -15)  # 加速度 a = -3

            v0 = v  # 初速度v0
            v = v0 + a * t  # 当前速度
            # 移动距离
            move = v0 * t + 1 / 2 * a * t * t
            current += move  # 当前位移
            # 加入轨迹
            track.append(round(move))

        # 模拟人类 抖动

        track.append(-5)
        track.append(-8)
        track.append(-2)
        track.append(-7)
        track.append(3)
        if current > x_distance:
            track.append(x_distance - current)

        return track

    def get_track_2(self, x_distance):
        track = []  # 移动轨迹
        for i in range(18):
            tem = random.randint(3, 10)
            track.append(tem)
            current_total = sum(track)
            if current_total > x_distance:
                track.append(x_distance - current_total)
                break

        print("total is ---> %d" % (current_total,))
        if current_total < x_distance:
            track.append(x_distance - current_total)

        track.append(6)
        track.append(-4)
        track.append(-4)
        track.append(2)
        return track

    def go_move(self, track, btn_slider):
        ActionChains(self.browser).click_and_hold(btn_slider).perform()
        time.sleep(0.3)
        for x in track:
            # 开始滑动
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
            # ActionChains(self.browser).move_to_element_with_offset(btn_slider, xoffset=x, yoffset=0).perform()
            # time.sleep(round(random.uniform(0.7, 1.5), 2))

        time.sleep(0.6)
        ActionChains(self.browser).release().perform()  # 松开鼠标
        return

    def do_slider(self, x_distance):
        track = self.get_track(x_distance)
        # track = self.get_track_2(x_distance)
        print("slider line is ", track)
        btn_slider = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dvc-slider__handler')))
        self.go_move(track, btn_slider)
        return

    def new_do_slider(self, x_distance):
        print("new slider start")
        btn_slider = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dvc-slider__handler')))
        ActionChains(self.browser).click_and_hold(btn_slider).perform()
        time.sleep(0.2)
        '''
        ActionChains(self.browser).move_to_element_with_offset(btn_slider, xoffset=50, yoffset=1).perform()
        ActionChains(self.browser).move_to_element_with_offset(btn_slider, xoffset=52, yoffset=1).perform()
        ActionChains(self.browser).move_to_element_with_offset(btn_slider, xoffset=-52, yoffset=1).perform()
        ActionChains(self.browser).move_to_element_with_offset(btn_slider, xoffset=-50, yoffset=1).perform()
        '''

        '''
        for i in range(14):
            s = -20
            if i % 2 == 0:
                s = 20
            print("move_to_element_with_offset --- %s" % (s,))
            ActionChains(self.browser).move_to_element_with_offset(btn_slider, xoffset=s, yoffset=1).perform()
            time.sleep(random.uniform(0.2, 0.7))
        '''
        ActionChains(self.browser).move_by_offset(xoffset=x_distance, yoffset=1).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()  # 松开鼠标
        return

    def do_opencv(self):
        img_0 = cv2.imread("./captcha_58.png", 0)
        x_distance_1 = self.get_distance(img_0)
        img_1 = cv2.imread("./slider.png", 0)
        x_distance_2 = self.get_distance(img_1)
        # slider滑动
        if None == x_distance_1 or None == x_distance_2:
            return

        self.do_slider(round(x_distance_1 - x_distance_2))
        # self.new_do_slider(x_distance)
        return

    def main(self):
        self.browser.get(self.url)
        # btnSubmit
        button1 = self.wait.until(EC.element_to_be_clickable((By.ID, 'btnSubmit')))
        button1.click()
        time.sleep(1.2)

        JS_TEM = 'document.getElementsByClassName("dvc-captcha__puzzleImg")[0].style.display="none"'
        JS_TEM_RE = 'document.getElementsByClassName("dvc-captcha__puzzleImg")[0].style.display="inline-block"'
        JS_BG = 'document.getElementsByClassName("dvc-captcha__bgImg")[0].style.display="none"'
        JS_BG_RE = 'document.getElementsByClassName("dvc-captcha__bgImg")[0].style.display="inline-block"'

        self.browser.execute_script(JS_TEM)
        time.sleep(0.5)

        img_bg = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dvc-captcha__bgImg')))
        img_bg.screenshot('./captcha_58.png')  # 截图带缺口的图片

        self.browser.execute_script(JS_TEM_RE)  # 恢复
        self.browser.execute_script(JS_BG)
        time.sleep(0.3)
        img_slider = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dvc-captcha__puzzleImg')))
        img_slider.screenshot('./slider.png')  # 截取滑块的图片
        time.sleep(0.3)
        self.browser.execute_script(JS_BG_RE)
        time.sleep(0.2)
        self.do_opencv()

        time.sleep(20)


if __name__ == "__main__":
    foo = ZhuFang()
    foo.main()