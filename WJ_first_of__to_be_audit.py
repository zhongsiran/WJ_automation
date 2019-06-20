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
        self.frame_of_jiancha_duixiang_hecha = 0

    def connect_to_existing_chrome(self):
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "debuggerAddress", "127.0.0.1:9222")
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

                print('设定了最后一个标题为“广州市市场监督管理局网络交易监督管理系统”的网页作为网监系统handle，数值为' + h)
                self.sys_found = True
        self.b.switch_to.window(self.wj_sys_handle)

    def wang_jian_system_login(self):
        if self.sys_found == False:
            self.b.get('http://10.194.188.7:7070/wljyjd/index.html')
        else:
            self.switch_to_default()

        try:
            if self.b.find_element_by_id('navbar'):  # 有NAVBAR即是已经登录
                print('已经登录')
                self.switch_to_default()
        except Exception as e:
            try:
                self.b.find_element_by_xpath(
                    "//input[@placeholder='账号']").clear()
                self.b.find_element_by_xpath(
                    "//input[@placeholder='账号']").send_keys('wjk_zsr')
                self.b.find_element_by_xpath(
                    "//input[@placeholder='密码']").clear()
                self.b.find_element_by_xpath(
                    "//input[@placeholder='密码']").send_keys('123456')
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

    def set_website_property(self, property):
        try:
            property_radio_input = self.b.find_elements_by_xpath(
                "//input[@name='websiteProperty'][@type='radio']")
            if property == '1':
                property_radio_input[1].click()
            else:
                property_radio_input[0].click()
        except Exception as e:
            print(e)
            print('找不到经营性/非经营性选项')

    def set_select_option(self, attr_name, display_name, option):
        try:
            business_type_option = self.b.find_element_by_xpath(
                "//select[@name='%s']" % (attr_name))
            Select(business_type_option).select_by_value(str(option))
        except Exception as e:
            print(e)
            print('设置“%s”类型下拉菜单出错' % (display_name))

    def set_radio_option(self, attr_name, display_name, option):
        try:
            option = int(option)
        except Exception as e:
            print(e)
            print('转换“%s”选择为INT出错' % (display_name))

        assert type(option) == int

        try:
            radio_input = self.b.find_elements_by_xpath(
                "//input[@name='%s'][@type='radio']" % (attr_name))
            radio_input[option].click()
        except Exception as e:
            print(e)
            print('设置%s选项出错' % (display_name))

    def get_dead_link(self):
        try:
            dead_link_radios = self.b.find_elements_by_xpath(
                "//input[@name='isDead'][@type='radio']")
            if dead_link_radios[1].is_selected():
                print('dead')
                return 'dead'
            else:
                print('live')
                return 'not dead'
        except Exception as e:
            print(e)
            print(dead_link_radios)
            print('找不到死链接选项')

    def audit(self, site_property=0, bt=3, st=1, signs=1, company_status=1, ads=0):

        if self.get_dead_link() == 'not dead':
            self.set_radio_option('auditStatus', '核查状态', ads)  # 0正常 1无效 2待复查
            if ads == 0:  #核查状态正常时，下面为必填项
                self.set_radio_option('signsLicenses', '亮标亮照', signs)  # 0否 1是
                self.set_select_option(
                    'companyStatus', '商事主体状态', company_status)  # 1正常 2查无 3吊销 4注销
                self.set_radio_option('websiteProperty', '网站性质',
                                      site_property)  # 0经营性 1非经营性
                if property == 1:
                    pass
                else:
                    self.set_select_option(
                        'businessType', '电子商务类型', bt)
                    if bt == 3:
                        # 1自建 2平台 3平台内经营者 4信息发布平台 5其他
                        self.set_select_option('shopType', '网店类型', st)

        else:
            self.set_radio_option('auditStatus', '核查状态', 1)  # 0正常 1无效 2待复查


if __name__ == "__main__":
    auto = WangJianAutomation()
    auto.connect_to_existing_chrome()

    choice = ''
    while 'q' not in choice:

        print('选择程序')
        choice = input()
        # if choice == 'c':
        # auto.connect_to_existing_chrome()
        # auto.set_wj_sys_handle()

        if choice == 'l':
            auto.set_wj_sys_handle()
            auto.wang_jian_system_login()
            auto.set_wj_sys_handle()
            auto.frame_of_mission_list()
            auto.frame_of_inside_mission()
            time.sleep(2)
            auto.switch_to_audit_list_and_filter()

        if choice == 'o':
            auto.set_wj_sys_handle()
            auto.frame_of_mission_list()
            auto.frame_of_inside_mission()
            time.sleep(2)
            auto.switch_to_audit_list_and_filter()
            auto.frame_of_audit_result_page()
            time.sleep(2)

        if choice == 'a':
            auto.frame_of_mission_list()
            auto.frame_of_inside_mission()
            auto.switch_to_audit_list_and_filter()
            auto.frame_of_audit_result_page()
            auto.click_open_shop_url()

        if choice == 'b':
            auto.set_wj_sys_handle()

        if choice == 'ca':
            auto.close_other_windows()

        if choice == 'f':
            auto.audit(1,)

    # time.sleep(3)
    # auto.close_other_windows()

    print('完成')
