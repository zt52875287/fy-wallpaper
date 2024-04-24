
import random
import time
import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading

IMAGE_SOURCE = {
    '风云4A': 'http://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_DISK.JPG',
    '风云4B': 'http://img.nsmc.org.cn/CLOUDIMAGE/FY4B/AGRI/GCLR/FY4B_DISK_GCLR.JPG',
}

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_label_frame_lv3mxpdk = self.__tk_label_frame_lv3mxpdk(self)
        self.tk_label_frame_lv3n3ou0 = self.__tk_label_frame_lv3n3ou0(self)
        self.tk_label_frame_lv3p37s0 = self.__tk_label_frame_lv3p37s0(self)
        self.tk_label_lv4z7jxj = self.__tk_label_lv4z7jxj( self.tk_label_frame_lv3p37s0)
        self.tk_label_frame_lv3pe4ql = self.__tk_label_frame_lv3pe4ql(self)
        self.tk_label_frame_lv3p7evj = self.__tk_label_frame_lv3p7evj(self)
        self.tk_label_lv4z7x8h = self.__tk_label_lv4z7x8h( self.tk_label_frame_lv3p7evj)
        self.tk_input_lv3lfdhv = self.__tk_input_lv3lfdhv(self)
        self.tk_radio_button_lv3lhwrw = self.__tk_radio_button_lv3lhwrw(self)
        self.tk_radio_button_lv3li3ir = self.__tk_radio_button_lv3li3ir(self)
        self.tk_scale_lv3lig4v = self.__tk_scale_lv3lig4v(self)
        self.tk_text_lv3liwr8 = self.__tk_text_lv3liwr8(self)
        self.tk_scale_lv3p7ip2 = self.__tk_scale_lv3p7ip2(self)
        self.tk_button_lv3pa699 = self.__tk_button_lv3pa699(self)
        self.tk_label_frame_lv3pmibu = self.__tk_label_frame_lv3pmibu(self)
        self.tk_input_lv3pot7g = self.__tk_input_lv3pot7g(self)
        self.tk_button_lv3pp7jn = self.__tk_button_lv3pp7jn(self)
    def __win(self):
        self.title("风云卫星壁纸")

        # 设置窗口大小、居中
        width = 400
        height = 600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_label_frame_lv3mxpdk(self,parent):
        frame = LabelFrame(parent,text="更新背景的时间间隔，单位：秒",)
        frame.place(x=20, y=10, width=360, height=60)
        return frame
    def __tk_label_frame_lv3n3ou0(self,parent):
        frame = LabelFrame(parent,text=" 图源",)
        frame.place(x=20, y=80, width=360, height=60)
        return frame
    def __tk_label_frame_lv3p37s0(self,parent):
        frame = LabelFrame(parent,text="图片上移幅度",)
        frame.place(x=20, y=150, width=360, height=60)
        return frame
    def __tk_label_lv4z7jxj(self,parent):
        label = Label(parent,text="60%",anchor="center", )
        label.place(x=285, y=0, width=50, height=30)
        return label
    def __tk_label_frame_lv3pe4ql(self,parent):
        frame = LabelFrame(parent,text="日志",)
        frame.place(x=20, y=410, width=360, height=170)
        return frame
    def __tk_label_frame_lv3p7evj(self,parent):
        frame = LabelFrame(parent,text="左右两侧留白，占屏幕宽度的比例",)
        frame.place(x=20, y=220, width=360, height=60)
        return frame
    def __tk_label_lv4z7x8h(self,parent):
        label = Label(parent,text="30%",anchor="center", )
        label.place(x=285, y=0, width=50, height=30)
        return label
    def __tk_input_lv3lfdhv(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=40, y=30, width=325, height=30)
        return ipt
    def __tk_radio_button_lv3lhwrw(self,parent):
        rb = Radiobutton(parent,)
        rb.place(x=77, y=98, width=80, height=30)
        return rb
    def __tk_radio_button_lv3li3ir(self,parent):
        rb = Radiobutton(parent,)
        rb.place(x=232, y=98, width=80, height=30)
        return rb
    def __tk_scale_lv3lig4v(self,parent):
        scale = tkinter.Scale(parent, orient=HORIZONTAL, )
        scale.place(x=40, y=170, width=245, height=30)
        return scale
    def __tk_text_lv3liwr8(self,parent):
        text = Text(parent)
        text.place(x=40, y=434, width=325, height=131)
        return text
    def __tk_scale_lv3p7ip2(self,parent):
        scale = tkinter.Scale(parent, orient=HORIZONTAL, )
        scale.place(x=40, y=240, width=245, height=30)
        return scale
    def __tk_button_lv3pa699(self,parent):
        btn = Button(parent, text="应用配置", takefocus=False,)
        btn.place(x=295, y=365, width=75, height=30)
        return btn
    def __tk_label_frame_lv3pmibu(self,parent):
        frame = LabelFrame(parent,text="图片暂存文件夹（下载完即清理，不会占用磁盘空间）",)
        frame.place(x=20, y=290, width=360, height=60)
        return frame
    def __tk_input_lv3pot7g(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=40, y=310, width=245, height=30)
        return ipt
    def __tk_button_lv3pp7jn(self,parent):
        btn = Button(parent, text="选择文件夹", takefocus=False,)
        btn.place(x=295, y=310, width=75, height=30)
        return btn

    # 显示 Tkinter 窗口
    def show_window(self):
        self.after(0, self.deiconify)  # 在 Tkinter 的事件循环中重新显示窗口

    def destroy(self):
        super().destroy()

    # 最小化到托盘
    def minimize_to_tray(self):
        self.withdraw()

class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self, log_widget=self.tk_text_lv3liwr8, apply_config_btn=self.tk_button_lv3pa699, interval_widget=self.tk_input_lv3lfdhv)
    def __event_bind(self):

        self.tk_input_lv3lfdhv.configure(validate="key", validatecommand=(self.tk_input_lv3lfdhv.register(self.ctl.isPositiveNum), '%P'))
        # self.tk_input_lv3lfdhv.configure(validate="key", validatecommand=(self.ctl.isPositiveNum))
        self.tk_input_lv3lfdhv.insert(0, '3600')

        self.image_source = StringVar(value=list(IMAGE_SOURCE.values())[1])
        self.tk_radio_button_lv3lhwrw.configure(variable=self.image_source, value=list(IMAGE_SOURCE.values())[1], text=list(IMAGE_SOURCE.keys())[1])
        self.tk_radio_button_lv3li3ir.configure(variable=self.image_source, value=list(IMAGE_SOURCE.values())[0], text=list(IMAGE_SOURCE.keys())[0])


        self.shift_up_rate = IntVar(value=30)
        self.ctl.update_label_for_scale(self.tk_label_lv4z7jxj, str(self.shift_up_rate.get()))
        self.tk_scale_lv3lig4v.configure(variable=self.shift_up_rate,from_=0,to=100,resolution=1,showvalue=False,command=lambda value: self.ctl.update_label_for_scale(self.tk_label_lv4z7jxj, value))
        self.side_padding_rate = IntVar(value=30)
        self.ctl.update_label_for_scale(self.tk_label_lv4z7x8h, str(self.side_padding_rate.get()))
        self.tk_scale_lv3p7ip2.configure(variable=self.side_padding_rate, from_=0, to=90, resolution=1, showvalue=False, command=lambda value: self.ctl.update_label_for_scale(self.tk_label_lv4z7x8h, value))

        self.tmp_dir = StringVar()
        self.tmp_dir.set("C:/")
        self.tk_input_lv3pot7g.configure(state='readonly', textvariable=self.tmp_dir)
        self.tk_button_lv3pp7jn.bind('<Button>', lambda event: self.ctl.choose_tmp_dir(event, self.tmp_dir))

        self.tk_button_lv3pa699.bind('<Button>', lambda event: self.ctl.apply_config(event,
                                                                                     self.tk_input_lv3lfdhv.get(),
                                                                                     self.image_source.get(),
                                                                                     self.shift_up_rate.get(),
                                                                                     self.side_padding_rate.get(),
                                                                                     self.tmp_dir.get()))

        # 绑定最小化按钮
        self.bind("<Unmap>", lambda e: self.minimize_to_tray() if e.widget == self else None)
        # 绑定关闭按钮
        self.protocol("WM_DELETE_WINDOW", self.exit_app)

        # 创建icon
        icon_image = Image.new("RGB", (16, 16), "white")
        dc = ImageDraw.Draw(icon_image)
        dc.rectangle((16 // 2, 0, 16, 16 // 2),fill='red')
        dc.rectangle((0, 16 // 2, 16 // 2, 16),fill='red')
        self.stray_icon = Icon('test name', icon=icon_image, menu=Menu(
            MenuItem('显示', self.show_window),
            MenuItem('退出', self.exit_app)
        ))
        threading.Thread(daemon=True,target=self.stray_icon.run).start()

        pass

    def exit_app(self):
        self.ctl.destroy()
        self.stray_icon.stop()
        self.stray_icon.__del__()
        super().destroy()

    def __style_config(self):
        pass
if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()