import importlib
import os
import sys
import traceback
from concurrent.futures import ProcessPoolExecutor

import asyncio
from datetime import datetime

from playwright.async_api import async_playwright

from config import Config, config
from function import manual_login, exclude_certain_index, get_state_path, retrieve_arguments, \
    delete_folder_files
from active_checker import ActiveChecker
from Dictionary import dictionary
from GlobalAttackSurfaces import global_attack_surfaces
from main_driver import MainDriver

async def running_tasks(tasks):
    for task in tasks:
        await task

def init():
    args = retrieve_arguments()
    if args.config:
        config.load_config(file_path="../configs/"+args.config)
    else:
        config.load_config(file_path="../configs/config-general.yaml")
    if args.hour:
        config.data['RUNNING_TIME']['h'] = args.hour
        print(f"[FUZZER] SET RUNNING TIME {config.data['RUNNING_TIME']['h']} hours")
    if args.minute:
        config.data['RUNNING_TIME']['m'] = args.minute
        print(f"[FUZZER] SET RUNNING TIME {config.data['RUNNING_TIME']['m']} minutes")
    config.calculate_finish_time()
    if args.url:
        config.data['HOMEPAGE_URL'] = args.url
        print(f"[FUZZER] SET HOMEPAGE URL: {config.data['HOMEPAGE_URL']}")
    if args.name:
        config.data['PROJECT_NAME'] = args.name
        print(f"[FUZZER] SET PROJECT_NAME: {config.data['PROJECT_NAME']}")
    if args.roles:
        config.data['USER_ROLES'] = args.roles
        print(f"[FUZZER] SET USER_ROLES: {config.data['USER_ROLES']}")
    if args.only_driver:
        config.enable_checker = False
        print(f"[FUZZER] Only Running the Driver Module. Turn off the checker")
    if args.only_checker:
        config.enable_driver = False
        print(f"[FUZZER] Only Running the Checker Module. Turn off the driver")
    if args.without_login:
        config.without_login = True
        print(f"[FUZZER] Without Login; Only Using the stored cookie")
    if args.ignored_sql:
        config.data['IGNORING_SQL'] += args.ignored_sql
        print(f"[FUZZER] Total DB tables that should be ignored:",config.data['IGNORING_SQL'])
    if args.proxy:
        config.proxy = args.proxy
        print(f"[FUZZER] Set up a proxy server:",config.proxy)

    if os.path.exists(f"../auto_login/{config.data['PROJECT_NAME']}.py") and not config.without_login:
        sys.path.append('../auto_login/')
        mod=importlib.import_module(config.data['PROJECT_NAME'])
        meth = getattr(mod, "main", None)
        if callable(meth):
            meth(config)
    else:
        folder_name = f"../login_state/{config.data['PROJECT_NAME']}"
        os.makedirs(folder_name, exist_ok=True)

async def main():
    start_time = datetime.now()
    print("STARTING TIME:", start_time)
    
    user_roles = config.data['USER_ROLES']
    drivers = {}
    active_checkers = {}

    homepages = config.homepages
    state_paths = {}

    async with async_playwright() as playwright:
            tasks = list()
            if config.enable_driver:
                for role in user_roles:
                    if os.path.exists(f"../auto_login/{config.data['PROJECT_NAME']}.py"):
                        state_paths[role] = get_state_path(role)
                        if role in homepages:
                            print(f"[FUZZER] Specific homepage for {role} is found:",homepages[role])
                        else:
                            print(f"[FUZZER] No Homepage for {role} is found. Using the default one")
                            homepages[role] = config.data['HOMEPAGE_URL']
                    elif not config.without_login:
                        state_paths[role], homepages[role] = await manual_login(playwright, role, login_url=config.data['HOMEPAGE_URL'])
                    else:
                        state_paths[role] = get_state_path(role)
                        homepages[role] = config.data['HOMEPAGE_URL']

                    ## CAN BE SKIPPED IF YOU WANT TO RUN SEPARATED DRIVER AND CHECKER PROCESS
                    drivers[role] = MainDriver(role)

                    await drivers[role].start_with_login_state(playwright, state_paths[role])
                    tasks.append(asyncio.create_task(drivers[role].crawl(homepages[role])))

            if config.enable_checker:
                ## FOR DETECTING VERTICAL BROKEN ACCESS CONTROL
                target_idx = 0
                new_user_roles = exclude_certain_index(user_roles, target_idx)

                ## FOR LOADING DATA FROM SEPARATED EXPERIMENTS
                if config.enable_driver==False:
                    dictionary.load_captured_paramvals()
                    global_attack_surfaces.load_attack_surface_from_file()
                    for role in user_roles:
                        state_paths[role] = get_state_path(role)

                        if role in homepages:
                            print(f"[FUZZER] Specific homepage for {role} is found:",homepages[role])
                        else:
                            print(f"[FUZZER] No Homepage for {role} is found. Using the default one")
                        homepages[role] = config.data['HOMEPAGE_URL']

                ## --------------

                for role in new_user_roles:
                    active_checkers[role] = ActiveChecker(role, starting_time=start_time)
                    active_checkers[role].user_context_path = state_paths[role]
                    active_checkers[role].homepage = homepages[role]

                    await active_checkers[role].start(playwright)
                    tasks.append(asyncio.create_task(active_checkers[role].fuzz()))
                ## -------------------------

            await running_tasks(tasks)

            print(f"[FUZZER] Campaign duration: {datetime.now() - start_time}")

            try:
                if config.enable_checker:
                    global_attack_surfaces.analyse_and_print_final_result(start_time,is_finish=True)
                    delete_folder_files(config.data['COV_PATHS'])
                else:
                    dictionary.save_captured_paramvals(start_time)
                    global_attack_surfaces.print_param_ref()
            except Exception as e:
                print(f"[FUZZER] Error in printing result: {e}")
                print(f"[FUZZER] {traceback.format_exc()[:100]}")
            print(f"[FUZZER] Finishing the fuzzing campaign at: {datetime.now()}")

if __name__ == "__main__":
    init()
    asyncio.run(main())