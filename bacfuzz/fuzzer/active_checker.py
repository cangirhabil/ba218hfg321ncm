import csv
import os
import re
import threading
import time
import urllib
from collections.abc import Iterable
# from copy import copy
import copy
from datetime import datetime, timedelta
import logging
import random
from typing import Dict, List
from urllib.parse import urlencode
import traceback

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright, Request, expect, APIResponse

from AICaller import build_prompt, AICaller, parse_response
from AttackSurface import AttackSurface
from HTTPRequest import HTTPRequest, drop_cookie_from_header
from Input import Input, VerificationLabel
# from LLM_call import callLLM
from function import delete_folder_files, \
    copy_dict_excluding_key, parse_post_data
from Dictionary import dictionary
from GlobalAttackSurfaces import global_attack_surfaces
from extract_idref import find_potential_ids
from general_functions import identify_security_params, is_token_value
from main_driver import MainDriver
from mutation_function import sysgen_LLM_generation, \
    BOLA_mutator, id_mutate, usergen_mutate

from config import config

import asyncio

# class ActiveChecker(Crawler):
class ActiveChecker():
    def __init__(self, role=None, starting_time=None):
        # super().__init__()
        self.role = role
        if starting_time:
            self.start_time = starting_time
        else:
            self.start_time = datetime.now()
        self.file_name_for_log = f"{config.data['PROJECT_NAME']}-{self.start_time.day}{self.start_time.month}_{self.start_time.hour}{self.start_time.minute}"
        self.nonce_data = {}
        self.header_data = {}
        self.cookie = {}
        self.parsed_cookie = dict()
        self.page = None
        self.homepage = None
        self.browser = None
        self.context = None
        self.req_number = 0
        self.surface_data_path = "default"
        self.user_context_path = None
        self.total_time = 0
        self.iterations = 0

        logging.basicConfig(filename=f"../log/{self.file_name_for_log}.log",
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
        self.logger = logging.getLogger()

        self.security_tokens = dict()

    def get_cookie(self, cookies):
        cookie=""
        for c in cookies:
            ## Custom code to set the security level of DVWA benchmark
            if config.data["PROJECT_NAME"].find("dvwa")>-1:
                if c['value'] == "impossible":
                    c['value'] = "low"
                    print(f"[AC {self.role}] Change cookie data from impossible to {c}")

            cookie += f"{c['name']}={c['value']}; "
        self.cookie['Cookie'] = cookie
        print(f"[AC {self.role}] Save cookie from the browser context", self.cookie)

    async def start(self, playwright):
        print(f"[AC {self.role}] -------STARTING ACTIVE CHECKER--------")
        self.browser = await playwright.chromium.launch(headless=True)
        if self.user_context_path:
            print(f"[AC {self.role}] -------LOGGING IN USER--------")
            self.context = await self.browser.new_context(storage_state=self.user_context_path)
            self.page = await self.context.new_page()
            self.get_cookie(await self.context.cookies())

            if "NONCE_KEYWORD" in config.data and config.data['NONCE_KEYWORD'] != "":
                # await self.crawl_pages_to_get_nonce_data()
                pass
        else:
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()

    async def grab_nonce_from_page(self, search, page=None):
        if page:
            await self.page.goto(page)
        else:
            await self.page.goto(self.homepage)
        await self.page.wait_for_load_state()

        print(f"[AC {self.role}] Looking for {search} in {self.page.url}")
        FOCUSSED_CHARS = 100
        html_string = await self.page.content()
        for m in re.finditer('(?=%s)(?!.{1,%d}%s)' % (search, len(search)-1, search), html_string):
            nonce_pos = m.start()
            focused_string = html_string[nonce_pos-FOCUSSED_CHARS:nonce_pos+FOCUSSED_CHARS]
            print(f"[AC {self.role}] Desired NONCE is found: {focused_string}")

            strings = focused_string.split('"')
            nonce_name = ""
            for str in strings:
                clean_str = re.sub(r'\W+', '', str)
                if clean_str.find(search)>-1:
                    nonce_name = clean_str
                elif nonce_name!="" and len(clean_str)>0:
                    if clean_str.find("val")<0 and clean_str.find("type")<0 and clean_str.find("hidden")<0:
                        ## We assume the next alphanumeric string after nonce key is nonce value
                        return clean_str
        print(f"[AC {self.role}] Desired NONCE {search} is NOT found ")
        return None

    async def grab_nonce(self):
        FOCUSSED_CHARS = 100
        html_string = await self.page.content()
        if "NONCE_KEYWORD" in config.data and config.data['NONCE_KEYWORD'] != "":

            search = config.data['NONCE_KEYWORD']
            for m in re.finditer('(?=%s)(?!.{1,%d}%s)' % (search, len(search)-1, search), html_string):
                nonce_pos = m.start()
                focused_string = html_string[nonce_pos-FOCUSSED_CHARS:nonce_pos+FOCUSSED_CHARS]

                strings = focused_string.split('"')
                nonce_name = ""
                for str in strings:
                    print(f"[AC {self.role}] Captured String: {str}")
                    clean_str = re.sub(r'\W+', '', str)
                    if clean_str.find(config.data['NONCE_KEYWORD'])>-1:
                        nonce_name = clean_str
                    elif nonce_name!="" and len(clean_str)>0:
                        if clean_str.find("val")<0 and clean_str.find("type")<0 and clean_str.find("hidden")<0:
                            ## We assume the next alphanumeric string after nonce key is nonce value
                            if nonce_name not in self.nonce_data:
                                ## Only save a new nonce
                                self.nonce_data[nonce_name] = clean_str
                                print(f"[AC {self.role}] Saving Nonce data: {nonce_name} --> {self.nonce_data[nonce_name]}")
                            else:
                                print(f"[AC {self.role}] Drop Nonce data: {nonce_name} --> {self.nonce_data[nonce_name]} because it already exists")
                            break

    def drop_cookie(self, chosen_request: HTTPRequest):
        chosen_request.header = drop_cookie_from_header(chosen_request.header)
        return chosen_request

    async def update_nonce_on_pv(self, pv, look_in_dict=True, page=None):
        if pv.is_nonce:
            print(f"[AC {self.role}] Will update {pv} because it is nonce data from {pv.role}")
            values = dictionary.search_field_values(pv.param, self.role)
            if look_in_dict and len(values)>0:
                pv.value = values[0]
                print(f"[AC {self.role}] Updated result from dict: {pv}")
            else:
                print(f"[AC {self.role}] Nonce data {pv.param} is not found in the dictionary. Trying another way")
                try:
                    value = await self.grab_nonce_from_page(pv.param, page)
                except Exception as e:
                    print(e)
                    value = None
                    
                if value:
                    print(f"[AC {self.role}] Old value: {pv}")
                    pv.value = value
                    print(f"[AC {self.role}] Updated result grab_nonce_from_page: {pv}")

                    copied_pv = copy.deepcopy(pv)
                    copied_pv.role = self.role
                    dictionary.add(copied_pv)

    async def update_nonce(self, request: HTTPRequest, look_in_dict=True, page=None):
        print(f"[AC {self.role}] Checking if any nonce data in the request parameters")
        for pv in request.paramvals:
            await self.update_nonce_on_pv(pv, look_in_dict, page)
            if pv.is_nested():
                for pv_nested in pv.paramvals:
                    await self.update_nonce_on_pv(pv_nested, look_in_dict, page)


    async def get_security_token_from_page(self, page_url=None, param_key=None):
        if page_url:
            if self.security_tokens and self.security_tokens['last_update'] > datetime.now() - timedelta(minutes = 10):
                return self.security_tokens
            else:
                await self.page.goto(page_url)
                await self.page.wait_for_load_state()

                if param_key:
                    print(f"[AC {self.role}] Looking for {param_key} in the page of {page_url}")
                else:
                    print(f"[AC {self.role}] Checking if any security_token in the request parameters in the page of {page_url}")
                    current_links = await self.page.get_by_role("link", include_hidden=True).all()
                    for link in current_links:
                        href = await link.get_attribute('href')
                        print(f"[AC {self.role}] Checking {href} if there any security token")
                        self.security_tokens = identify_security_params(href)

                        if self.security_tokens:
                            self.security_tokens['last_update'] = datetime.now()
                            return self.security_tokens

        return self.security_tokens

    async def update_security_token(self, request: HTTPRequest):
        # if request.referer:
            print(f"[AC {self.role}] Checking if any security_token in the request parameters")
            for pv in request.paramvals:
                if pv.is_nested():
                    for pv_nested in pv.paramvals:
                        if is_token_value(pv_nested.value):
                            if request.referer:
                                tokens = await self.get_security_token_from_page(request.referer)
                            else:
                                tokens = await self.get_security_token_from_page()

                            if tokens:
                                for key in tokens.keys():
                                    if key!="last_update":
                                        print(f"[AC {self.role}] Update {pv_nested} with new token: {tokens}")
                                        pv_nested.param = key
                                        pv_nested.value = tokens[key][0]
                else:
                    if is_token_value(pv.value):
                        # i = 0
                        if request.referer:
                            tokens = await self.get_security_token_from_page(request.referer)
                        else:
                            tokens = await self.get_security_token_from_page()

                        if tokens:
                            for key in tokens.keys():
                                if key!="last_update":
                                    # i += 1
                                    # print(f"[AC {self.role}] Repetition: {i}")
                                    print(f"[AC {self.role}] Update {pv} with new token: {tokens}")
                                    pv.param = key
                                    pv.value = tokens[key][0]

    def drop_and_use_seclevel_cookie_from_chosen_request(self, chosen_request: HTTPRequest):
        new_header = {}
        seclevel_cookie = None
        if chosen_request.header:
            for key in chosen_request.header:
                if key.find(config.data["COOKIE_KEYWORD"])>-1:
                    cookie_str = chosen_request.header[key]
                    print("[HTTPREQUEST] Drop cookie from header", key, cookie_str)
                    if cookie_str.find(';')>-1:
                        cookie_str = cookie_str.replace(';', '&')

                    parsed_cookie = parse_post_data(cookie_str)
                    if "security" in parsed_cookie:
                        print("[HTTPREQUEST] But we keep this cookie info: security=", parsed_cookie["security"])
                        seclevel_cookie = parsed_cookie["security"]
                    pass
                else:
                    new_header[key] = chosen_request.header[key]

        if seclevel_cookie:
            ## Parse now cookie
            cookie_str = self.cookie['Cookie']
            if cookie_str.find(';')>-1:
                cookie_str = cookie_str.replace(';', '&')

            parsed_cookie = parse_post_data(cookie_str)
            # print("[HTTPREQUEST] Use the saved cookie info to current cookie: security=", parsed_cookie["security"])
            parsed_cookie["security"] = seclevel_cookie

            cookie_encoded = urllib.parse.urlencode(parsed_cookie, quote_via=urllib.parse.quote_plus)
            if cookie_encoded.find('&')>-1:
                cookie_encoded = cookie_encoded.replace('&',';')
            self.cookie['Cookie'] = cookie_encoded

        return new_header

    def update_cookie(self, chosen_request: HTTPRequest):
        new_header = drop_cookie_from_header(chosen_request.header)

        print(f"[AC {self.role}] Update Cookie with:", self.cookie)
        chosen_request.header = {**new_header, **self.cookie}

        return chosen_request

    def drop_and_add_cookie_from_header(self, headers: Dict[str, str]):
        new_header = {}
        for key in headers:
            if key.find(config.data["COOKIE_KEYWORD"])>-1:
                print(f"[AC {self.role}] Drop cookie from header", key, headers[key])
                pass
            else:
                new_header[key] = headers[key]

        return {**new_header, **self.cookie}


    async def get_response_title(self, response: APIResponse):
        html_string = await response.text()
        print(f"[AC {self.role}] Raw Response:", html_string[:200])
        if response.headers["content-type"].find("html")>-1:
            html_page = BeautifulSoup(html_string,"html5lib")
            if html_page.title:
                print(f"[AC {self.role}] Response page title:",html_page.title)
                self.logger.info(f"[{self.role}] Response Title: "+str(html_page.title))
                return html_page.title
            else:
                print(f"[AC {self.role}] No HTML Title in the Response. Returning the raw response instead")
                self.logger.info(f"[{self.role}] No HTML Title in the Response")
                self.logger.info(f"[{self.role}] Response: "+html_string[:200])
                return html_string[:200]
        else:
            print(f"[AC {self.role}] The response is not an HTML page. Returning the raw response instead")
            self.logger.info(f"[{self.role}] The response is not an HTML page")
            self.logger.info(f"[{self.role}] Response: "+html_string[:200])
            return html_string[:200]

    async def save_response_to_HTML_file(self, response: APIResponse, request=None):
        if hasattr(response, 'text'):
            if request and request.id:
                filename = f"../data/{request.id}.html"
            else:
                dt = datetime.now()
                filename = f"../data/{dt.hour}{dt.minute}{dt.second}{dt.microsecond}.html"

            print(f"[AC {self.role}] Saved in {filename}")
            with open(filename, "w") as txt_file:
                txt_file.write(await response.text())

            self.logger.info(f"[{self.role}] Response is saved in {filename}\n\n")
        else:
            print(f"[AC {self.role}] The API Response does not have a text. Unable to save to HTML file")

    def save_to_csv(self, input: Input,processing_time=0):
        mutated_request = input.request
        response = input.response
        response_title = input.response_title

        with open(f"../log/{self.file_name_for_log}.csv", "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([mutated_request.source,
                             self.role,
                             self.req_number,
                             mutated_request.id,
                             processing_time,
                             response.status,
                             response_title,
                             mutated_request.method,
                             mutated_request.url,
                             mutated_request.post_data_encoded,
                             str(input.error_report),
                             time.time(),
                             len(config.line_coverage)])

        input.error_report = None ## Free the var to save more space

    async def save_to_log(self, input: Input, new_path_found=None, testname="",processing_time=0):
        try:
            self.req_number+=1
            self.logger.info(f"-----[{self.role}] [Testname: {testname}] Sending Request number : "+str(self.req_number)+" from "+input.request.source)
            self.logger.info(f"[{self.role}] {input.request.id} [{input.request.saved_filename}]")
            self.logger.info(f"[{self.role}] {input.request}")
            self.logger.info(f"[{self.role}] {input.request.post_data_encoded}")
            self.logger.info(f"[{self.role}] Response: {str(input.response)} [{self.role}]")
            if new_path_found and new_path_found!=-1:
                self.logger.info(f"[{self.role}] New Path Set: "+str(new_path_found))
            if len(input.error_report)>0:
                self.logger.info(f"[{self.role}] SQL Reported: "+str(input.error_report))
            if input.reason_to_add:
                self.logger.info(f"[{self.role}] Reason to add to Corpus: {input.reason_to_add}")
            self.logger.info(f"[{self.role}] Mutated paramvals: {input.mutated_paramvals}")
            self.logger.info(f"[{self.role}] Processing Time: {processing_time}")

            await self.save_response_to_HTML_file(input.response, input.request)
            self.save_to_csv(input,processing_time)
            input.response = None ## Free the var to save more space
        except Exception as e:
            print(f"[AC {self.role}] Error in storing data to files:")
            print(f"[AC {self.role}] {e}")

    async def send_HTTP_request(self, request: HTTPRequest):
        request.full_url = f"{request.url}"
        if request.param_encoded:
            request.full_url = f"{request.url}?{request.param_encoded}"

        print(f"[AC {self.role}] ---SENDING THE REQUEST [{request.id}] TO : [{request.method}]", request.full_url)
        print(f"[AC {self.role}] Post data encoded: {request.post_data_encoded}")
        api_request_context = self.page.request
        try:

            if request.content_type and str(request.content_type).find("multipart/form-data")>-1:
                new_header = copy_dict_excluding_key(request.header,"content-type")
                print(f"[AC {self.role}] Send using multipart/form-data type")
                print(f"[AC {self.role}] New header: {str(new_header)}")
                response = await api_request_context.fetch(url_or_request=request.full_url,
                                                           method=request.method,
                                                           headers=new_header,
                                                           multipart=request.body_param_dict)
            else:
                response = await api_request_context.fetch(url_or_request=request.full_url,
                                                           method=request.method,
                                                           headers=request.header,
                                                           data=request.post_data_encoded)
            print(f"[AC {self.role}] Response:", response, "from request ID:",request.id)
            return response
        except Exception as e:
            print(f"[AC {self.role}] Web server is error!: ", str(e)[:2000])
            return None

    async def preparing_new_request(self, request: HTTPRequest, is_dropping_cookie=True):
        """
        We copy the original request, so that the manipulation on the copied request does not impact the original one.
        We have to drop the initial cookie header from the request.
        If active checker is not in anonymous mode, we have to put the user cookie header and its nonce string.
        :param chosen_request:
        :return:
        """
        print(f"[AC {self.role}] ---COPYING AND PREPARING NEW REQUEST FROM THE CHOSEN REQUEST---")
        chosen_request = copy.deepcopy(request)

        if is_dropping_cookie:
            if self.user_context_path:
                ## ADD THE USER COOKIE AND NONCE
                prepared_request = self.update_cookie(chosen_request)
            else:
                prepared_request = self.drop_cookie(chosen_request)
        else:
            prepared_request = chosen_request

        return prepared_request

    def select_attack_surface_from_global(self) -> AttackSurface:
        if len(global_attack_surfaces.data)>0:
            chosen_attack_surface = random.choice(global_attack_surfaces.data)
            return chosen_attack_surface
        return None

    def get_weight(self, attack_surfaces=None):
        """
        We calculate the weight for each attack surface based on the number of sysgen params plus the number of idsysgen
        :param attack_surfaces:
        :return:
        """
        if attack_surfaces:
            return [x.get_num_reference_param() for x in attack_surfaces]

        return [x.get_num_reference_param() for x in global_attack_surfaces.data]

    def select_attack_surface(self, for_obj_level=False) -> AttackSurface:
        print(f"[AC {self.role}] SELECT AN ATTACK SURFACE")
        ## select an attack surface in which attack surface with higher number of sysgen has higher probability
        if len(global_attack_surfaces.data)>0:
            if for_obj_level:
                attack_surfaces = [attack for attack in global_attack_surfaces.data if self.role in attack.roles]
                if len(attack_surfaces)>0:
                    chosen_attack_surface = random.choices(
                        attack_surfaces,
                        weights=self.get_weight(attack_surfaces=attack_surfaces))
                    print(f"[AC {self.role}] Chosen ATTACK SURFACE for Object-level test [param-ref count: {chosen_attack_surface[0].get_num_reference_param()}]:",chosen_attack_surface[0])
                    return chosen_attack_surface[0]

            chosen_attack_surface = random.choices(
                global_attack_surfaces.data,
                weights=self.get_weight())
            print(f"[AC {self.role}] Random Chosen ATTACK SURFACE [param-ref count: {chosen_attack_surface[0].get_num_reference_param()}]:",chosen_attack_surface[0])
            return chosen_attack_surface[0]
        return None



    async def check_unprotected_func(self,attack_target):
        ## Check for vertical access control vulnerability
        # target_request = attack_target.target
        target_request = attack_target.getRequest()
        print(f"[AC {self.role}] Checking vertical access vulnerability in: ",target_request)

        prepared_target_request = await self.preparing_new_request(target_request, is_dropping_cookie=True)
        prepared_target_request.source = "check_unprotected_func"

        # await self.update_nonce(prepared_target_request)
        if config.data["PROJECT_NAME"].find("smf")>-1:
            await self.update_security_token(prepared_target_request)

        prepared_target_request.update_param_from_paramvals()
        await self.send_and_analyse_mutated_request(attack_target,prepared_target_request, "vertical")


    async def send_and_analyse_mutated_request(self, attack_target, prepared_target_request, testname):
        prepared_target_request.update_id()
        prepared_target_request.header["X-FUZZER-COVID"] = prepared_target_request.id

        response_str = None
        processing_time = 0
        start_calculation = time.perf_counter()

        response = await self.send_HTTP_request(prepared_target_request)
        input = Input(prepared_target_request, response, testname)
        if response:
            try:
                end_calculation = time.perf_counter()
                processing_time = end_calculation - start_calculation ## :16 in seconds
                self.total_time += processing_time
                self.iterations += 1

                if response and response.status:
                    global_attack_surfaces.add_response_code(response.status)

                response_str = await response.text()
                input.response_title = await self.get_response_title(input.response)
            except Exception as e:
                print(f"[AC {self.role}] Error in retrieving the response:",e)
        else:
            print(f"[AC {self.role}] Getting No Response")
            response_str = None
        input.sent_role = self.role
        input.params_from_refpage, input.ids_from_refpage = await self.get_idref_from_ref_page(input, testname=="validate_BAC")
        new_paths = attack_target.analyse(input, response_str)
        if (testname!="validate_BAC") and (input.label==VerificationLabel.OBJECT_BROKEN or input.label==VerificationLabel.PROPERTY_BROKEN or input.label==VerificationLabel.FUNCTIONAL_BROKEN):
            await self.validate_BAC(input,attack_target)

        ## Save the information into a log file and a CSV file
        await self.save_to_log(input,new_paths,testname,processing_time)
        return input



    async def horizontal_test(self, chosen_attack_surface: AttackSurface):
        print(f"[AC {self.role}] Checking Horizontal Access vulnerability in: ", chosen_attack_surface.target)
        target_request = chosen_attack_surface.getRequest()
        print(f"[AC {self.role}] Target request to be mutated:", target_request)
        prepared_request = await self.preparing_new_request(target_request)
        mutation_functions = [BOLA_mutator]

        mutation_function = mutation_functions[0]
        if mutation_function == sysgen_LLM_generation:
            mutated_requests = sysgen_LLM_generation(chosen_attack_surface, self.role)
            for req in mutated_requests:
                req.update_param_from_paramvals()
        else:
            mutated_requests = mutation_function(prepared_request, self.role)

        if (mutated_requests and isinstance(mutated_requests, Iterable) and len(mutated_requests)>0):
            for mutated_request in mutated_requests:

                if config.data["PROJECT_NAME"].find("smf")>-1:
                    await self.update_security_token(mutated_request)
                    mutated_request.update_param_from_paramvals()

                await self.send_and_analyse_mutated_request(chosen_attack_surface,mutated_request,mutation_function.__name__)
        else:
            print(f"[AC {self.role}] Mutated request is NULL. It might be caused by the mutation function failure")

    def save_all_paramvals(self,start_time):
        if self.role==config.data["USER_ROLES"][1]:
            filename = f"[DATA]{self.role}_{start_time.hour}{start_time.minute}{start_time.second}{start_time.microsecond}"
            print(f"[AC {self.role}] Storing paramvals to: ../result/{filename}.txt")
            with open(f"../result/{filename}.txt", "w") as txt_file:
                i = 0
                for paramval in dictionary.data:
                    i += 1
                    txt_file.write(f"{i}. {paramval}\n")

        filename2 = f"[PARAMVALS]{self.role}_{start_time.hour}{start_time.minute}{start_time.second}{start_time.microsecond}"
        print(f"[AC {self.role}] Storing paramvals to: ../result/{filename2}.txt")
        with open(f"../result/{filename2}.txt", "w") as txt_file:
            i = 0
            for id in dictionary.paramvals[self.role]:
                i += 1
                txt_file.write(f"{i}. {id} ==> {dictionary.paramvals[self.role][id]}\n")

    def object_level_test(self):
        return self.select_attack_surface(for_obj_level=True)

    def random_level_test(self):
        return self.select_attack_surface(for_obj_level=False)

    async def validate_BAC(self, input: Input, chosen_attack_surface, validation_number=1):
        """
        Try to validate param marked as BAC by slightly mutating param
        and seeing the query whether the same query appear with different value.
        :return:
        """
        print(f"[AC {self.role}] Validating BAC by sending another request")
        prepared_request = await self.preparing_new_request(input.request)
        BAC_labelled_paramvals = prepared_request.get_BAC_labelled_paramvals()
        result = None
        for p in BAC_labelled_paramvals:
            result = id_mutate(p,self.role)

        if result:
            usergen_mutate(prepared_request, self.role) ## Also mutate the other parameters to avoid rejection from DB that only save unique data
            if config.data["PROJECT_NAME"].find("smf")>-1:
                await self.update_security_token(prepared_request)
                # time.sleep(5)
            prepared_request.update_param_from_paramvals()
            inp2 = await self.send_and_analyse_mutated_request(chosen_attack_surface,prepared_request,"validate_BAC")
            # if (input.label==VerificationLabel.FUNCTIONAL_BROKEN and inp2.label==VerificationLabel.OBJECT_BROKEN) or (inp2.label==input.label):
            if inp2.label==input.label or inp2.label==VerificationLabel.FUNCTIONAL_BROKEN or inp2.label==VerificationLabel.OBJECT_BROKEN:
                print(f"[AC {self.role}] {input.label} BAC is verified! {input}")
                if not input.is_verification_proof:
                    input.detection_order = len(global_attack_surfaces.success_inputs) + 1
                input.attack_surface_ID = chosen_attack_surface.id
                global_attack_surfaces.add_success_input(input)
                inp2.is_verification_proof = True
                inp2.detection_order = input.detection_order

                if validation_number<10:
                    print(f"[AC {self.role}] Running again the BAC validation")
                    inp2.label = input.label
                    await self.validate_BAC(inp2,chosen_attack_surface, validation_number+1)
                else:
                    print(f"[AC {self.role}] Already {validation_number} times validation. It is enough.")
                    inp2.attack_surface_ID = chosen_attack_surface.id
                    global_attack_surfaces.add_success_input(inp2)
            else:
                if input.is_verification_proof:
                    print(f"[AC {self.role}] BAC-detected label is not dropped because the source is verified")
                    input.attack_surface_ID = chosen_attack_surface.id
                    global_attack_surfaces.add_success_input(input)
                else:
                    print(f"[AC {self.role}] BAC-detected label is dropped since it is not verified")
                    input.label=VerificationLabel.UNDEFINED
                    input.detected_time = None
                    input.reason_to_add = None
                    input.vul_oracle = ""
                    input.vul_oracles = list()
                    input.mutated_values = None

                    inp2.label=VerificationLabel.UNDEFINED
                    inp2.detected_time = None
                    inp2.reason_to_add = None
                    inp2.vul_oracle = ""
                    inp2.vul_oracles = list()
                    inp2.mutated_values = None

    def get_str_mutated_param(self, input: Input):
        str = ""
        for pv in input.mutated_paramvals:
            str = str + str(pv.param) + "_"
        return str

    async def get_idref_from_ref_page(self, input: Input, is_screenshot=False):
        ref = input.request.referer
        if ref:
            page = await self.context.new_page()
            await page.goto(ref)
            await page.wait_for_load_state()

            print(f"[AC {self.role}] Opening ref_page {ref}")
            html_string = await page.content()
            if is_screenshot:
                data_title = f"../screenshots/{self.get_str_mutated_param(input)}{input.request.id[-12:]}.jpeg"
                await page.screenshot(path=data_title)
            await page.close()
            return find_potential_ids(html_string)
        return list(), list()


    async def fuzz(self):
        idx = 0
        current_time = datetime.now()
        while current_time < config.finish_time:
        # for i in range(10):
            idx +=1
            try:
                print(f"[AC {self.role}] ----ACTIVE CHECKER WILL SEND A REQUEST {idx}-----")
                print(f"[AC {self.role}] Current time: {format(current_time, '%H:%M:%S')}")

                mutation_functions = random.choices([
                    self.object_level_test,
                    self.random_level_test],
                    weights=[1,1])
                mutation_function = mutation_functions[0]
                chosen_attack_surface = mutation_function()

                if chosen_attack_surface:
                    if self.role in chosen_attack_surface.roles:
                        await self.horizontal_test(chosen_attack_surface)
                    else:
                        print(f"[AC {self.role}] Roles from the chosen attack surface: {chosen_attack_surface.roles}")
                        await self.check_unprotected_func(chosen_attack_surface)
                else:
                    print(f"[AC {self.role}] Attack surface is empty. Wait for 30 seconds")
                    await asyncio.sleep(30)
            except Exception as e:
                print(f"[AC {self.role}] Error in fuzzing: {e}")
                # print(f"[AC {self.role}] {traceback.format_exc()}")
                print(f"[AC {self.role}] {traceback.format_exc()[-1000:]}")

            try:
                chosen_role = config.data['USER_ROLES'][1]
                if self.role == chosen_role and idx % 50 == 0:
                    delete_folder_files(config.data['COV_PATHS'])

                if idx % 1000 == 0:
                    avg_time = self.total_time / self.iterations
                    global_attack_surfaces.processing_time[self.role] = avg_time

                if self.role == chosen_role and idx % 1000 == 0:
                    ## Assume 1 hour produce 1500 idx
                    print(f"[AC {self.role}] Save temporary results")
                    global_attack_surfaces.analyse_and_print_final_result(self.start_time)
            except Exception as e:
                print(f"[AC {self.role}] Error in printing result: {e}")
                print(f"[AC {self.role}] {traceback.format_exc()[-1000:]}")

            current_time = datetime.now()

        try:
            await self.context.close()
            await self.browser.close()
        except Exception as e:
            print(f"[AC {self.role}] Error in printing result: {e}")
            print(f"[AC {self.role}] {traceback.format_exc()[-1000:]}")

        print(f"[AC {self.role}] ----FUZZING CAMPAIGN IS FINISHED-----")
