from wj_selenium_main import audited_list_automation as audit_auto
import time

if __name__ == "__main__":
    auto = audit_auto.AuditedListAutomation()
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
            time.sleep(2)
            auto.goto_core_frame()

        if choice == 'o':
            auto.set_wj_sys_handle()
            auto.goto_core_frame()
            auto.get_credit_code()
            if auto.credit_code == '':
                auto.get_company_name()

        if choice == 'cl':
            auto.click_close_audit_icon()

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
