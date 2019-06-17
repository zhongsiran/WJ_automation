from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time

class WangJianAutomation:
    def __init__(self):
        self.b = ''
        
    def connect_to_existing_chrome(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.b = webdriver.Chrome(options=chrome_options)
        self.b.switch_to.default_content()
        self.b.maximize_window()

    def wang_jian_system_login(self):
        self.b.get('http://10.194.188.7:7070/wljyjd/index.html')
        self.b.find_element_by_xpath("//input[@placeholder='账号']").send_keys('wjk_zsr')
        self.b.find_element_by_xpath("//input[@placeholder='密码']").send_keys('123456')
        self.b.find_element_by_xpath("//button").click()
        time.sleep(3)

    def frame_of_mission_list(self): 
        outer_frame = self.b.find_elements_by_xpath("//iframe")
        if outer_frame:
            self.b.switch_to.frame(outer_frame[0])
        else:
            print('找不到“待办事项”窗口')
            exit(0)

    def open_first_mission(self):
        green_hammers = self.b.find_elements_by_xpath("//img[@title='处理']")
        green_hammers[0].click()

    def frame_of_inside_mission(self):
        inner_frame = self.b.find_elements_by_xpath("//iframe")
        if inner_frame:
            self.b.switch_to.frame(inner_frame[0])
        else:
            print('找不到“处理任务”窗口')
            exit(0)

    def choose_audit_list(self):
        try:
            self.b.find_element_by_link_text('检查对象').click()
            s = self.b.find_element_by_id("audit_status")
            Select(s).select_by_visible_text('待核查')
            self.b.find_element_by_link_text('查询').click()
        except Exception as e:
            print(e)
            print('“检查对象”页标签不可点击') 

    def frame_of_audit_result_page(self):
        result_frame = self.b.find_elements_by_xpath("//iframe")
        if result_frame:
            self.b.switch_to.frame(result_frame[0])
        else:
            print('找不到“检查对象核查”窗口')
            exit(0)


if __name__ == "__main__":
    auto = WangJianAutomation()
    auto.connect_to_existing_chrome()
    auto.wang_jian_system_login()
    auto.frame_of_mission_list()
    auto.open_first_mission()
    auto.frame_of_inside_mission()
    auto.choose_audit_list()
    
    # auto.frame_of_audit_result_page()
    print('完成')