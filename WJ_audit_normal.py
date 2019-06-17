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
    
    def switch_to_default(self):
        self.b.switch_to.default_content()
        self.b.maximize_window()

    def frame_of_mission_list(self): 
        outer_frame = self.b.find_elements_by_xpath("//iframe")
        if outer_frame:
            self.b.switch_to.frame(outer_frame[0])
        else:
            print('找不到“待办事项”窗口')
            exit(0)

    def frame_of_inside_mission(self):
        inner_frame = self.b.find_elements_by_xpath("//iframe")
        if inner_frame:
            self.b.switch_to.frame(inner_frame[0])
        else:
            print('找不到“处理任务”窗口')
            exit(0)

    def frame_of_audit_result_page(self):
        result_frame = self.b.find_elements_by_xpath("//iframe")
        if result_frame:
            self.b.switch_to.frame(result_frame[0])
        else:
            print('找不到“检查对象核查”窗口')
            exit(0)

    def set_website_property(self, property):
        try:
            property_radio_input = self.b.find_elements_by_xpath("//input[@name='websiteProperty'][@type='radio']")
            if property == '1':
                property_radio_input[1].click()
            else:
                property_radio_input[0].click()
        except Exception as e:
            print(e)
            print('找不到经营性/非经营性选项')
            
    def set_select_option(self, attr_name, display_name, option):
        try:
            business_type_option = self.b.find_element_by_xpath("//select[@name='%s']" %(attr_name))
            Select(business_type_option).select_by_value(str(option))
        except Exception as e:
            print(e)
            print('设置“%s”类型下拉菜单出错' % (display_name))

    def set_radio_option(self, attr_name, display_name, option):
        try:
            option = int(option)
        except Exception as e:
            print(e)
            print('转换“%s”选择为INT出错'% (display_name))

        assert type(option) == int

        try:
            radio_input = self.b.find_elements_by_xpath("//input[@name='%s'][@type='radio']" %(attr_name))
            radio_input[option].click()
        except Exception as e:
            print(e)
            print('设置%s选项出错' %(display_name))

    def get_dead_link(self):
        try:
            dead_link_radios = self.b.find_elements_by_xpath("//input[@name='isDead'][@type='radio']")
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

    def audit(self, site_property=0, bt=3, st=1, signs=1, company_status=1):

        if self.get_dead_link() == 'not dead':
            self.set_radio_option('websiteProperty', '网站性质', site_property)
            if property == 1:
                pass
            else:
                self.set_select_option('businessType', '电子商务类型', bt) #  1经营性 2非经营性
                if bt == 3:
                    self.set_select_option('shopType', '网店类型', st) #  1自建 2平台 3平台内经营者 4信息发布平台 5其他
                self.set_radio_option('signsLicenses', '亮标亮照', signs) #  0否 1是
                self.set_radio_option('auditStatus', '核查状态', 0) #  0正常 1无效 2待复查
                self.set_select_option('companyStatus', '商事主体状态', company_status) #  1正常 2查无 3吊销 4注销
        else:
            self.set_radio_option('auditStatus', '核查状态', 1) #  0正常 1无效 2待复查


if __name__ == "__main__":
    auto = WangJianAutomation()
    auto.connect_to_existing_chrome()
    auto.switch_to_default()
    auto.frame_of_mission_list()
    auto.frame_of_inside_mission()
    auto.frame_of_audit_result_page()
    auto.audit()
    # auto.get_deal_link()
    print('完成')