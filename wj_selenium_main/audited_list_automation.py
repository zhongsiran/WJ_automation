from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time


class AuditedListAutomation:
    def __init__(self):
        self.b = ''
        self.sys_found = False
        self.gsxt_handle = ''
        self.wj_sys_handle = ''
        self.first_layer_frame = 0
        self.frame_of_jiancha_duixiang_hecha = 0
        self.credit_code = ''
        self.com_name = ''

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

    def goto_audited_list_frame(self):
        self.switch_to_default()

        if self.first_layer_frame:
            try:
                self.b.switch_to.frame(self.first_layer_frame)
            except Exception as e:
                print(73)
                print(e)
        else:
            #  点击 已审档案 按钮
            try:
                self.b.find_element_by_id('menuitemG0401').click()
                verification = self.b.find_element_by_xpath(
                    "//a[@href='#tab_menuitemG0401']")
            except Exception as e:
                print(82)
                print(e)
            try:
                # 已审档案专属iframe,以scr确定
                outer_frame = self.b.find_elements_by_xpath(
                    "//iframe[@src='modules/mainFile/trialFiles.html?menuId=G0401']")
                self.first_layer_frame = outer_frame[0]
                self.b.switch_to.frame(self.first_layer_frame)
                print('90:进入“已审档案”iframe')
            except Exception as e:
                print('95')
                print(e)
                exit(0)

    def click_item_to_be_audit(self, idx, title):
        try:
            todos = self.b.find_elements_by_xpath(
                "//img[@title='%s']" % (title))
            todos[idx].click()
        except Exception as e:
            print(e)
            # print('尝试点击第%d个锤子时出错' % (idx))

    def frame_of_audit_result_page(self, audit_idx=0):
        if self.b.find_elements_by_xpath("//iframe[contains(@id,'frame')]") == []:
            print('107:未打开核查窗口，需要点击打开。')
            self.click_item_to_be_audit(audit_idx, '修改')

        result_frames = self.b.find_elements_by_xpath(
            "//iframe[contains(@id,'frame')]")

        try:
            self.b.switch_to.frame(result_frames[0])
            print('114:switching to audit page frame', end='')
            print(result_frames[0])
            self.b.find_element_by_id("subjectAction")
            self.frame_of_jiancha_duixiang_hecha = result_frames[0]
            print('119:进入“检查对象核查”iframe')
        except Exception as e:
            print('找不到“检查对象核查”窗口')
            print(e)
            exit(0)

    def goto_core_frame(self, sleep_time=2, audit_idx=0):
        self.goto_audited_list_frame()
        time.sleep(sleep_time)
        self.frame_of_audit_result_page(audit_idx)

    def get_shop_url(self):
        shop_url = self.b.find_element_by_id('shopUrl')
        print(shop_url.get_attribute('value'))

    # the icon is in the parent frame of the audit frame
    def click_close_audit_icon(self):
        try:
            self.b.find_element_by_link_text("取消").click()
        except selenium.common.exceptions.NoSuchElementException:
            self.goto_core_frame(0.1)
            print(140)
            self.b.find_element_by_link_text("取消").click()

    def click_open_shop_url(self):
        self.b.find_element_by_link_text("打开网页").click()

    def click_confirm_audit(self):
        try:
            self.b.find_element_by_link_text("确定核对").click()
        except selenium.common.exceptions.NoSuchElementException:
            self.goto_core_frame(0.1)
            print(151)
            self.b.find_element_by_link_text("确定核对").click()

    def click_confirm(self):
        try:
            self.goto_core_frame(1)
            print('156:goto parent frame')
            self.b.switch_to.parent_frame()
            self.b.find_element_by_xpath(
                "//a[contains(@class, 'layui')][text()='确定']").click()
        except Exception as e:
            print(157, end=':')
            print(e)

    def close_other_windows(self):
        for handle in self.b.window_handles:
            if handle != self.wj_sys_handle:
                if handle == self.gsxt_handle:
                    pass
                else:
                    self.b.switch_to.window(handle)
                    time.sleep(0.3)
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

    def set_textarea(self, textarea_id, pt_idx=0, addition=''):
        try:
            target_textarea = self.b.find_element_by_xpath(
                "//textarea[@id='%s']" % (textarea_id)
            )
        except selenium.common.exceptions.NoSuchElementException:
            print('找不到id为%s的text area' % (textarea_id))

        if textarea_id == 'opinion':
            predefined_text_list = [
                '核查通过。',
                '经核查，该主体与网站（网店）实际开办者不符。',
                '经核查，该主体已注销/已吊销。',
                '经核查，该网站（网店）的网页无法正常打开。',
                '经核查，该网店未发布商品信息，无经营活动迹象。',
                '经核查，该网站（网店）有部分信息暂无法核实，拟作进一步调查。'
            ]
        elif textarea_id == 'remark':
            predefined_text_list = [
                ''
            ]

        try:
            target_textarea.send_keys(predefined_text_list[pt_idx] + addition)
        except Exception as e:
            print(e)

    def get_dead_link(self):
        try:
            dead_link_radios = self.b.find_elements_by_xpath(
                "//input[@name='isDead'][@type='radio']")
            if dead_link_radios[1].is_selected():
                print('死链')
                return 'dead'
            elif dead_link_radios[0].is_selected():
                print('非死链')
                return 'not dead'
            else:
                print('死链选项未选择')
                return 'blank'
        except Exception as e:
            print(e)
            print(dead_link_radios)
            print('找不到死链接选项')

    def set_dead_link(self, dl_idx):
        try:
            dead_link_radios = self.b.find_elements_by_xpath(
                "//input[@name='isDead'][@type='radio']")
            try:
                dead_link_radios[dl_idx].click()
            except Exception as e:
                print('error while setting dead link')
                print(e)
        except Exception as e:
            print(e)
            print(dead_link_radios)
            print('找不到死链接选项')

    def get_credit_code(self):
        try:
            t = self.b.find_element_by_xpath(
                "//input[@name='creditCode']"
            )
            self.b.execute_script(
                "results = document.getElementsByName('creditCode');" +
                "results[0].removeAttribute('readonly');" +
                "results[0].select();" +
                "document.execCommand('Copy');")
            self.credit_code = t.get_attribute("value")
            print('统一信用代码：' + self.credit_code)
        except Exception as e:
            print(e)

    def get_company_name(self):
        try:
            t = self.b.find_element_by_xpath(
                "//input[@name='companyName']"
            )
            self.b.execute_script(
                "results = document.getElementsByName('companyName');" +
                "results[0].removeAttribute('readonly');" +
                "results[0].select();" +
                "document.execCommand('Copy');")
            self.com_name = t.get_attribute("value")
            print('商事主体名称：' + self.com_name)
        except Exception as e:
            print(e)

    def switch_to_gsxt(self, ):
        try:
            if self.gsxt_handle != '':
                self.b.switch_to.window(
                    self.gsxt_handle
                )
                self.b.find_element_by_xpath(
                    "//input[@name='searchword'][@id='keyword']").send_keys(self.credit_code if self.credit_code else self.com_name)
            else:
                print('随便点个链接')
                self.b.find_element_by_xpath("//a").click()
                print('切换到最新窗口')
                self.b.switch_to.window(self.b.window_handles[
                    len(self.b.window_handles) - 1])
                print('进入公示平台')
                self.b.get("http://www.gsxt.gov.cn")
                self.set_gsxt_handle()

        except Exception as e:
            print('277')
            print(e)

    def audit(self, ads=0, site_property=0, signs=1, company_status=1, bt=3, st=1, dl=0):
        if self.get_dead_link() == 'blank':
            self.set_dead_link(dl)

        if self.get_dead_link() == 'not dead':
            self.set_radio_option('auditStatus', '核查状态', ads)  # 0正常 1无效 2待复查
            if ads == 0:  # 核查状态正常时，下面为必填项
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
