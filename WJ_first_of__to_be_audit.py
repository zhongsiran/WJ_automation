from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time

class WangJianAutomation:
    def __init__(self):
        self.b = ''
        self.sys_found = False
        self.wj_sys_handle = ''
        self.frames_of_daiban_shixiang = 0
        self.frame_of_chuli_renwu = 0
        self.frame_of_jiancha_duixiang_hecha= 0
        
    def connect_to_existing_chrome(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.b = webdriver.Chrome(options=chrome_options)
    
    def switch_to_default(self):
        self.b.switch_to.window(self.wj_sys_handle)
        self.b.switch_to.default_content()
        self.b.maximize_window()

    def set_wj_sys_handle(self):
        for h in self.b.window_handles:
            self.b.switch_to.window(h)
            if '广州市市场监督管理局网络交易监督管理系统' == self.b.title:
                self.wj_sys_handle = h
                self.b.switch_to.window(h)
                print('设定了最后一个标题为“广州市市场监督管理局网络交易监督管理系统”的网页作为网监系统handle，数值为' + h)
                self.sys_found = True

    def wang_jian_system_login(self):
        if self.sys_found == False:
            self.b.get('http://10.194.188.7:7070/wljyjd/index.html')
        else:
            self.switch_to_default()

        try:
            if self.b.find_element_by_id('navbar'): #有NAVBAR即是已经登录
                print('已经登录')
                self.switch_to_default()
        except Exception as e:
            try:
                self.b.find_element_by_xpath("//input[@placeholder='账号']").clear()
                self.b.find_element_by_xpath("//input[@placeholder='账号']").send_keys('wjk_zsr')
                self.b.find_element_by_xpath("//input[@placeholder='密码']").clear()
                self.b.find_element_by_xpath("//input[@placeholder='密码']").send_keys('123456')
                self.b.find_element_by_xpath("//button").click()
                time.sleep(3)
            except Exception as e:
                print('尝试登录时的问题：')
                print(e)

    def frame_of_mission_list(self): 
        self.switch_to_default()

        outer_frame = self.b.find_elements_by_xpath("//iframe")
        print(self.b.current_window_handle)
        print(outer_frame)
        try:
            self.b.switch_to.frame(outer_frame[0])
            self.b.find_element_by_id("toDoList")
            self.frame_of_daiban_shixiang = outer_frame[0]
            print('进入“待办事项”iframe')
        except Exception as e:
            print('找不到“待办事项”窗口')
            print(e)
            exit(0)

    def open_first_mission(self):
        green_hammers = self.b.find_elements_by_xpath("//img[@title='处理']")
        green_hammers[0].click()

    def frame_of_inside_mission(self):
        if self.b.find_elements_by_xpath("//iframe") == []:
            print('open first mission')
            self.open_first_mission()
        
        inner_frame = self.b.find_elements_by_xpath("//iframe")

        try:
            self.b.switch_to.frame(inner_frame[0])
            self.b.find_element_by_id("createTask")
            self.frame_of_chuli_renwu = inner_frame[0]
            print('进入“处理任务”iframe')
        except Exception as e:
            print('找不到“处理任务”窗口')
            print(e)
            exit(0)

    def switch_to_audit_list_and_filter(self):
        try:
            self.b.find_element_by_link_text('检查对象').click()
            s = self.b.find_element_by_id("audit_status")
            Select(s).select_by_visible_text('待核查')
            self.b.find_element_by_link_text('查询').click()
        except Exception as e:
            print(e)
            print('“检查对象”页标签不可点击') 

    def click_first_to_be_audit(self):
        try:
            todos = self.b.find_elements_by_xpath("//img[@title='核查']")
            todos[0].click()
        except Exception as e:
            print(e)
            print('尝试点击第一个锤子时出错') 

    def frame_of_audit_result_page(self):
        if self.b.find_elements_by_xpath("//iframe") == []:
            self.switch_to_audit_list_and_filter()
            self.click_first_to_be_audit()

        result_frame = self.b.find_elements_by_xpath("//iframe")

        try:
            self.b.switch_to.frame(result_frame[0])
            self.b.find_element_by_id("subjectAction")
            self.frame_of_jiancha_duixiang_hecha = result_frame[0]
            print('进入“检查对象核查”iframe')
        except Exception as e:
            print('找不到“检查对象核查”窗口')
            print(e)
            exit(0)

    def get_shop_url(self):
        shop_url = self.b.find_element_by_id('shopUrl')
        print(shop_url.get_attribute('value'))

    def click_open_shop_url(self):
        self.b.find_element_by_link_text("打开网页").click()

    def close_other_windows(self):
        self.b.switch_to.window(self.wj_sys_handle)
        for handle in self.b.window_handles:
            if handle != self.wj_sys_handle:
                self.b.switch_to.window(handle)
                self.b.close()
        self.b.switch_to.window(self.wj_sys_handle)

    def get_current_iframe(self):
        frames = [self.frames_of_daiban_shixiang, self.frame_of_chuli_renwu, self.frame_of_jiancha_duixiang_hecha]
        for idx, frame in enumerate(frames):
            if self.b == frame:
                print(idx)
                

if __name__ == "__main__":
    auto = WangJianAutomation()
    auto.connect_to_existing_chrome()
    auto.set_wj_sys_handle()
    auto.wang_jian_system_login()
    auto.set_wj_sys_handle()
    auto.frame_of_mission_list()

    # auto.open_first_mission()
    auto.frame_of_inside_mission()

    time.sleep(2)
    auto.switch_to_audit_list_and_filter()

    # auto.click_first_to_be_audit()
    auto.frame_of_audit_result_page()
    time.sleep(2)
    auto.b.find_element_by_link_text("打开网页").click()

    # time.sleep(3)
    # auto.close_other_windows()


    print('完成')