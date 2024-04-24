from tkinter import filedialog
import tkinter as tk
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import screeninfo
import requests
from PIL import Image
from io import BytesIO
import time
import ctypes
import os

Image.MAX_IMAGE_PIXELS = 500000000


# 示例下载 https://www.pytk.net/blog/1702564569.html
class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: object

    def __init__(self):
        pass

    def init(self, ui, log_widget, apply_config_btn, interval_widget):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        self.job_scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
        self.job_scheduler.start()
        self.log_widget = log_widget
        self.apply_config_btn = apply_config_btn
        self.interval_widget = interval_widget

        self.GET_IMAGE_MAX_RETRY = 3
        self.GET_IMAGE_MAX_RETRY_TIME_GAP = 1
        self.has_running_task = False

    def destroy(self):
        if self.job_scheduler.running:
            self.job_scheduler.shutdown()

    def choose_tmp_dir(self, evt, entry_widget):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.append_log(f'更改暂存文件夹为：{folder_path}')
            entry_widget.set(folder_path)

    def isPositiveNum(self, new_value):
        if new_value == '':
            return True
        try:
            if int(new_value) > 0:
                return True
            else:
                return False
        except ValueError:
            return False

    def update_label_for_scale(self, label_widget, value):
        label_widget.config(text=value + '%')

    def apply_config(self, evt, interval, image_source, shift_up_rate, side_padding_rate, tmp_dir):

        if int(interval) < 60:
            self.append_log('更改壁纸的时间间隔最小为60秒，自动修改为60秒')
            self.interval_widget.delete(0, tk.END)
            self.interval_widget.insert(0, '60')
            interval = '60'

        self.append_log(
            f'启动定时器，每{interval}秒更换壁纸，图源：{image_source}，上移比率：{shift_up_rate}，边距占比：{side_padding_rate}，暂存路径：{tmp_dir}')

        jobs = self.job_scheduler.get_jobs()
        # 防止重复启动，添加多个任务
        if len(jobs) > 0:
            for job in jobs:
                job.remove()
        self.job_scheduler.add_job(self.run_fy,
                                   'interval',
                                   seconds=int(interval),
                                   next_run_time=datetime.now() + timedelta(seconds=2),
                                   args=[shift_up_rate, side_padding_rate, image_source, tmp_dir])

    def run_fy(self, curr_shift_up_rate, curr_side_padding_rate, curr_image_source, curr_tmp_dir):

        try:
            global screen_width
            global screen_height
            monitors = screeninfo.get_monitors()
            screen_width = monitors[0].width
            screen_height = monitors[0].height

            # # 下载图片
            self.append_log('开始下载壁纸...')
            image = self.download_image(curr_image_source)
            if image is not None:
                # 根据分辨率 resize
                resized_path = self.resize_image(image, curr_shift_up_rate, curr_side_padding_rate, curr_tmp_dir)
                # 设置壁纸
                ctypes.windll.user32.SystemParametersInfoW(20, 0, resized_path, 1 | 2)
                self.append_log('壁纸设置成功！！！')
                # 删除下载的图片
                os.remove(resized_path)
        finally:
            self.append_log('==== 本次任务结束 ====')

    def append_log(self, logStr):
        curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logStr = f'{curr_time}  {logStr}\n'
        self.log_widget.insert(tk.END, logStr)

        content = self.log_widget.get("1.0", tk.END).strip()
        lines = content.split("\n")  # 将文本拆分为行
        # 如果行数超过5行，移除最早的一行
        if len(lines) > 10:
            # 删除第一行
            self.log_widget.delete("1.0", "2.0")  # 删除第一行到第二行的范围

        self.log_widget.see('end')

    def download_image(self, curr_image_source):
        """
        下载图片
        :return: PIL.Image
        """
        retry = 0
        while retry < self.GET_IMAGE_MAX_RETRY:
            try:
                response = requests.get(curr_image_source)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    saved_image = Image.open(image_data)
                    return saved_image
                else:
                    self.append_log(f"下载图片失败，错误代码：{response.status_code}，自动重试ing")
                    retry += 1
                    time.sleep(self.GET_IMAGE_MAX_RETRY_TIME_GAP)
            except Exception as e:
                print(f"Ex:{e}")
                retry += 1
                time.sleep(self.GET_IMAGE_MAX_RETRY_TIME_GAP)
        self.append_log(f"重试下载失败，下一轮任务再试")
        return None

    def resize_image(self, pil_image, curr_shift_up_rate, curr_side_padding_rate, curr_tmp_dir):
        """
        调整图片大小，适配显示器
        :param curr_side_padding_rate: 左右两侧留白的比率
        :param curr_shift_up_rate: 壁纸上移的比率
        :param curr_show_type: 壁纸平铺模式
        :param pil_image: PLI.Image
        :return: 调整后的图片文件的保存路径
        """
        image_width, image_height = pil_image.size

        # 等比例放大，左右稍微留一点距离，要不然地球就顶到屏幕左右边缘了
        new_width = int(screen_width * (1 - curr_side_padding_rate / 100))
        new_height = int(image_height * (new_width / image_width))
        resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)

        # 按照屏幕尺寸进行截取，需要稍微往上偏一点，才能将中国全部显示出来
        cut_len = (new_height - screen_height) // 2
        offset = new_height / 2 * curr_shift_up_rate / 100
        resized_image = resized_image.crop((
            0,
            cut_len - offset,
            new_width,
            cut_len - offset + screen_height
        ))

        # 设置一个黑色的画布，将上面剪出来的图片，放置在中央
        bk_image = Image.new("RGB", (screen_width, screen_height), (0, 0, 0))
        w1, h1 = resized_image.size
        w2, h2 = bk_image.size

        bk_image.paste(resized_image, (int((w2 - w1) / 2), int((h2 - h1) / 2)))
        resized_image = bk_image

        resized_saved_path = f"{curr_tmp_dir}//{datetime.now().strftime('%Y%m%d_%H%M%S')}.JPG"
        resized_image.save(resized_saved_path)
        return resized_saved_path
