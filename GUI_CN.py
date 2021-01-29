import sys
from os.path import abspath, split, join
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import Tk, Button, StringVar, IntVar, Radiobutton, Checkbutton, Scale, HORIZONTAL
from tkinter.ttk import Progressbar
from threading import Thread
from SkyAR import SkyAR


def file_select(item, types, is_save=False):
    if not is_save:
        item.set(askopenfilename(title='choose an video', filetypes=types))
    else:
        item.set(asksaveasfilename(title='save result', filetypes=types))

def run(configs):
    skyar = SkyAR()
    skyar.MagicSky(**configs)
    bar.stop()
    start_button['bg'] = 'SystemButtonFace'
    start_button['state'] = 'normal'
    start_button['text'] = 'start'

def start():
    configs = {
        'video_path': str(video_path.get()),
        'save_path': str(save_path.get()),
        'config': config_list[int(config_choose.get())],
        'is_rainy': bool(int(is_rainy.get())),
        'preview_frames_num': 0,
        'is_video_sky': None,
        'is_show': bool(int(preview.get())),
        'skybox_img': None,
        'skybox_video': None,
        'rain_cap_path': None,
        'halo_effect': bool(int(halo_effect.get())),
        'auto_light_matching': bool(int(auto_light_matching.get())),
        'relighting_factor': float(relighting_factor.get()),
        'recoloring_factor': float(recoloring_factor.get()),
        'skybox_center_crop': float(skybox_center_crop.get())
    }
    print(configs)
    start_button['bg'] = 'red'
    start_button['text'] = 'wait'
    start_button['state'] = 'disabled'
    bar.start()
    t = Thread(target=run, args=(configs,))
    t.start()


if __name__ == "__main__":
    try:
        base_path = sys._MEIPASS
    except:
        base_path = split(abspath(__file__))[0]

    global config_list_CN, config_list
    config_list_CN = [
        '雨天', '晴天', '多云', '银河', '木星', '晚霞',
        '超级月亮', '悬浮城堡', '电闪雷鸣', '第九区飞船'
    ]
    config_list = [
        'rainy', 'sunny', 'cloudy', 'galaxy', 'jupiter', 'sunset',
        'supermoon', 'floatingcastle', 'thunderstorm', 'district9ship'
    ]
    root = Tk()

    root.title('SkyAR Paddle GUI')

    root.iconbitmap(join(base_path, 'favicon.ico'))

    root.geometry('300x800')

    video_path = StringVar()
    Button(root, text='选择视频路径', command=lambda: file_select(
        video_path, (("image", "*.mp4"), ("all", "*")))).pack()
    save_path = StringVar()
    save_path.set('result.mp4')
    Button(root, text='选择输出路径', command=lambda: file_select(
        save_path, (("image", "*.mp4"), ("all", "*")), True)).pack()
    skybox_img = StringVar()
    Button(root, text='自定义天空图像', command=lambda: file_select(
        skybox_img, (("image", "*.jpg; *.png; *.bmp; *.jpeg"), ("all", "*")))).pack()
    skybox_video = StringVar()
    Button(root, text='自定义天空视频', command=lambda: file_select(
        skybox_video, (("image", "*.mp4"), ("all", "*")))).pack()
    rain_cap_path = StringVar()
    Button(root, text='自定义下雨效果', command=lambda: file_select(
        rain_cap_path, (("image", "*.mp4"), ("all", "*")))).pack()

    config_choose = IntVar()
    config_choose.set(4)
    for i, value in enumerate(config_list_CN):
        b = Radiobutton(root, text=value, variable=config_choose, value=i)
        b.pack()

    is_rainy = StringVar()
    is_rainy.set(0)
    br = Checkbutton(root, text='下雨特效', variable=is_rainy)
    br.pack()
    halo_effect = StringVar()
    halo_effect.set(1)
    bh = Checkbutton(root, text='日晕效应', variable=halo_effect)
    bh.pack()
    preview = StringVar()
    preview.set(1)
    ba = Checkbutton(root, text='结果预览', variable=preview)
    ba.pack()
    auto_light_matching = StringVar()
    auto_light_matching.set(0)
    ba = Checkbutton(root, text='自动亮度匹配',
                     variable=auto_light_matching)
    ba.pack()

    relighting_factor = StringVar()
    relighting_factor.set(0.8)
    Scale(root,
          label='亮度重设因子',
          length=200,
          from_=0.,
          to=1.0,
          resolution=0.001,
          orient=HORIZONTAL,
          variable=relighting_factor,
          digits=3,
          ).pack()

    recoloring_factor = StringVar()
    recoloring_factor.set(0.5)
    Scale(root,
          label='颜色重设因子',
          length=200,
          from_=0.,
          to=1.0,
          resolution=0.001,
          orient=HORIZONTAL,
          variable=recoloring_factor,
          digits=3,
          ).pack()

    skybox_center_crop = StringVar()
    skybox_center_crop.set(0.5)
    Scale(root,
          label='天空裁切因子',
          length=200,
          from_=0.,
          to=1.0,
          resolution=0.001,
          orient=HORIZONTAL,
          variable=skybox_center_crop,
          digits=3,
          ).pack()
    start_button = Button(root, text='开始处理', command=start)
    start_button.pack()
    bar = Progressbar(root, length = 200, value = 0, mode = "indeterminate")
    bar.pack(pady = 10)
    root.mainloop()