from wj_selenium_main import first_todo_mission_automation as first_todo_auto
import time

if __name__ == "__main__":
    auto = first_todo_auto()
    auto.connect_to_existing_chrome()

    choice = ''
    while 'q' not in choice:
        print("*" * 20)
        print('选择程序')
        choice = input()
        # if choice == 'c':
        # auto.connect_to_existing_chrome()
        # auto.set_wj_sys_handle()

        if choice == 'l':  #  进入第一个待办任务的待核查列表
            auto.set_wj_sys_handle()
            auto.wang_jian_system_login()
            auto.set_wj_sys_handle()
            auto.frame_of_mission_list()
            auto.frame_of_inside_mission()
            time.sleep(2)
            auto.switch_to_audit_list_and_filter()

        if choice == 'o':
            auto.set_wj_sys_handle()
            auto.goto_core_frame()
            auto.get_credit_code()
            if auto.credit_code == '':
                auto.get_company_name()
            time.sleep(2)

        if choice == 'gsa':
            auto.set_gsxt_handle()
            auto.set_wj_sys_handle()
            auto.goto_core_frame(0.1)
            auto.get_credit_code()
            if auto.credit_code == '':
                auto.get_company_name()
            auto.click_open_shop_url()
            auto.switch_to_gsxt()

        if choice == 'a':
            auto.set_wj_sys_handle()
            auto.goto_core_frame(0.1)
            auto.get_credit_code()
            if auto.credit_code == '':
                auto.get_company_name()
            auto.click_open_shop_url()
            auto.switch_to_gsxt()

        if choice == 'b':
            auto.set_wj_sys_handle()

        if choice == 'ca':
            auto.close_other_windows()

        # '核查通过。',
        # '经核查，该主体与网站（网店）实际开办者不符。',
        # '经核查，该主体已注销/已吊销。',
        # '经核查，该网站（网店）的网页无法正常打开。',
        # '经核查，该网店未发布商品信息，无经营活动迹象。',
        # '经核查，该网站（网店）有部分信息暂无法核实，拟作进一步调查。'

        if choice == 'f':  # 非经营
            auto.goto_core_frame(0.1)
            auto.audit(0, 1, 0, 1)
            auto.set_textarea('opinion')
            print('正常，非经，无亮照，开业')
            print('核查通过')

        if choice == 'zz':  # 正常 自建
            auto.goto_core_frame(0.1)
            auto.audit(0, 0, 0, 1, 1, dl=0)
            auto.set_textarea('opinion')
            print('正常，经营性，无亮照，开业，自建')
            print('核查通过')

        if choice == 'zzc':  # 正常 自建
            auto.goto_core_frame(0.1)
            auto.audit(0, 0, 0, 1, 1, dl=0)
            auto.set_textarea('opinion')
            print('正常，经营性，无亮照，开业，自建')
            print('核查通过')

            auto.click_confirm_audit()
            time.sleep(1)
            auto.click_confirm()
            

        if choice == 'zx': #  正 三方
            auto.goto_core_frame(0.1)
            auto.audit(0, 0, 1, 1, dl=0)
            auto.set_radio_option('isMatching', '主体资格', 0)
            auto.set_textarea('opinion')
            print('正常，经营性，亮照，开业，第三方， 平台内经营者')
            print('核查通过')

        if choice == 'zxc':
            auto.goto_core_frame(0.1)
            auto.audit(0, 0, 1, 1, dl=0)
            auto.set_radio_option('isMatching', '主体资格', 0)
            auto.set_textarea('opinion')
            print('正常，经营性，亮照，开业，第三方， 平台内经营者')
            print('核查通过')
            
            auto.click_confirm_audit()
            time.sleep(1)
            auto.click_confirm()

        if choice == 'zw':  # 正 无
            auto.goto_core_frame(0.1)
            auto.audit(0, 0, 1, 1, dl=0)
            auto.set_radio_option('isMatching', '主体资格', 0)
            auto.set_textarea('opinion', 4)
            print('正常，经营性，亮照，开业，第三方， 平台内经营者')
            print('无商品')

        if choice == 'zwc':
            auto.goto_core_frame(0.1)
            auto.audit(0, 0, 1, 1, dl=0)
            auto.set_radio_option('isMatching', '主体资格', 0)
            auto.set_textarea('opinion', 4)
            print('正常，经营性，亮照，开业，第三方， 平台内经营者')
            print('无商品')
            auto.click_confirm_audit()
            time.sleep(1)
            auto.click_confirm()

        if choice == 'zs':  # 正 商
            auto.goto_core_frame(0.1)
            auto.audit(0, 0, 1, 1, dl=0)
            auto.set_radio_option('isMatching', '主体资格', 0)
            auto.set_textarea('opinion', 4)
            print('正常，经营性，亮照，开业，第三方， 平台内经营者')
            print('无商品')

        if choice == 'zsc':
            auto.goto_core_frame(0.1)
            auto.audit(0, 0, 1, 1, dl=0)
            auto.set_radio_option('isMatching', '主体资格', 0)
            auto.set_textarea('opinion')
            auto.set_textarea('remark',0,'留意商标侵权')
            print('正常，经营性，亮照，开业，第三方， 平台内经营者')
            print('无商品')
            auto.click_confirm_audit()
            time.sleep(1)
            auto.click_confirm()

        if choice == 'wx':
            auto.goto_core_frame(0.1)
            auto.audit(1, dl=0)
            auto.set_textarea('opinion', 3)
            print('无效')
            print('无法打开')

        if choice == 'wxc':
            auto.goto_core_frame(0.1)
            auto.audit(1, dl=0)
            auto.set_textarea('opinion', 3)
            print('无效')
            print('无法打开')
            auto.click_confirm_audit()
            time.sleep(1)
            auto.click_confirm()

        if choice == 'cf':
            auto.b.switch_to.window(auto.wj_sys_handle)
            auto.click_confirm_audit()
            time.sleep(1)
            auto.click_confirm()

        if choice == 'gs':
            auto.set_gsxt_handle()

    # time.sleep(3)
    # auto.close_other_windows()
    print('=*=' * 6)
    print('完成')
    print('=*=' * 6)
