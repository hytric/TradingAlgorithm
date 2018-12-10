# 프로그램 실행 전 번개 업데이트 프로그램
from pywinauto import application
from pywinauto import timings
import time
import os
app = application.Application()
app.start("C:/KiwoomFlash3/bin/nkministarter.exe")
title = "번개3 Login"
timings.always_wait_until(20, 0.5)
dlg = app.window(title = title)
pass_ctrl = dlg.Edit2
pass_ctrl.set_focus()
pass_ctrl.type_keys('WnrWnr14')

cert_ctrl = dlg.Edit3
cert_ctrl.set_focus()
cert_ctrl.type_keys('WnrWnrdl-2853')

btn_ctrl = dlg.Button0
btn_ctrl.click()

time.sleep(50)
os.system("taskkill /im nkmini.exe")