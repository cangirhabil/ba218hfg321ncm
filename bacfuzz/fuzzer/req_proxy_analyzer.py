import json
import os
import traceback
from datetime import datetime
from urllib.parse import urlparse, urlencode, parse_qs, unquote

from HTTPRequest import HTTPRequest, parse_multipart_content, convert_request_to_yaml
from config import config
from AttackSurface import AttackSurface
from GlobalAttackSurfaces import global_attack_surfaces
from Dictionary import dictionary
from general_functions import is_same_domain

from mitmproxy import io
from mitmproxy.http import HTTPFlow
import sys
from email.parser import BytesParser
from email import policy

class HAR_analyzer:
    def __init__(self):
        self.corpus = list()
        self.corpus_length = 0
        self.role = "Admin"

    def is_filtered_response(self, response):
        """
        Checks if the response should be filtered based on the Content-Type header.
        Filters out images, videos, graphics, CSS, and JavaScript.
        """
        content_type = response.headers.get("Content-Type", "").lower()
        return (
                content_type.startswith("image/") or
                content_type.startswith("video/") or
                content_type.startswith("application/octet-stream") or
                content_type.startswith("application/font-") or
                content_type.startswith("font/") or
                content_type.startswith("text/css") or
                content_type.startswith("application/javascript") or
                content_type.startswith("text/javascript")
        )

    def parse_multipart_form_data(self, body, content_type):
        """
        Parses a multipart/form-data request body into a dictionary.
        """
        headers = f"Content-Type: {content_type}\r\n\r\n"
        message = BytesParser(policy=policy.default).parsebytes(headers.encode() + body)
        parsed_data = {}

        for part in message.get_payload():
            try:
                if part.get_content_disposition() == "form-data":
                    name = part.get_param("name", header="content-disposition")
                    value = part.get_payload(decode=True).decode("utf-8", errors="replace")
                    parsed_data[name] = value
            except Exception as e:
                print(f"[ANALYZER] Error in multipart data parsing:", e)

        return parsed_data

    def extract_http_requests(self, dump_file, output_file):
        """
        Extracts raw HTTP requests from a mitmproxy dump file and saves them to a text file.
        """
        idx = 0
        try:
            with open(dump_file, "rb") as f, open(output_file, "w", encoding="utf-8") as out:
                # Create a reader for the mitmproxy dump file
                reader = io.FlowReader(f)

                # Iterate through each flow in the dump file
                for flow in reader.stream():
                    # if isinstance(flow, HTTPFlow):
                    if isinstance(flow, HTTPFlow) and flow.response and flow.response.status_code == 200:
                        # Extract the HTTP request
                        request = flow.request

                        req = self.check_and_save_req(request, flow.response)
                        if req:
                            idx += 1

                            referrer = None
                            if "referer" in request.headers:
                                referrer = request.headers['referer']

                            # Write the raw HTTP request to the output file
                            out.write(f"=== [{idx}] Request to {request.pretty_url} ===\n")
                            out.write(f"{request.method} {request.path} HTTP/{request.http_version}\n")
                            for header, value in request.headers.items():
                                out.write(f"{header}: {value}\n")
                            if request.content:
                                out.write("\nRequest Body:\n")
                                out.write(request.content.decode("utf-8", errors="replace") + "\n")
                            if req.paramvals_without_nonce and len(req.paramvals_without_nonce)>0:
                                out.write("\nIdentified Param Value:\n")
                                out.write(f"{[str(x) for x in req.paramvals_without_nonce]} \n")
                            out.write("\n" + "=" * 80 + "\n\n")

                        # self.check_and_save_req(request)

        except Exception as e:
            print(f"Error reading dump file: {e}")
            print(f"[ANALYZER] {traceback.format_exc()}")
            sys.exit(1)

    def decode_urlencoded_body(self, body):
        """
        Decodes a URL-encoded request body and returns it as a dictionary.
        """
        try:
            # Parse the URL-encoded body into a dictionary
            decoded_data = parse_qs(body)
            # Unquote the values in the dictionary
            decoded_data = {k: [unquote(v) for v in vs] for k, vs in decoded_data.items()}
            return decoded_data
        except Exception as e:
            print(f"Error decoding URL-encoded body: {e}")
            return None

    def convert_request_type(self,request,role=None) -> HTTPRequest:
        req = HTTPRequest()
        req.source = "InterceptedRequest"
        req.role = role
        req.full_url = request.pretty_url
        ##PARSE TO <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
        parsed_url = urlparse(req.full_url)
        req.url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        req.param_encoded = parsed_url.query
        req.header = self.convert_list_to_dict(request.headers)
        req.method = request.method

        if "referer" in req.header:
            req.referer = req.header['referer']

        if 'content-type' in req.header:
            req.content_type = req.header['content-type']

        if request.content:
            content_type = request.headers.get("Content-Type", "").lower()

            if content_type.startswith("application/x-www-form-urlencoded"):
                # Parse URL-encoded form data
                req.post_data_encoded = request.content.decode("utf-8", errors="replace")
                request_body_dict = parse_qs(req.post_data_encoded)
                req.post_data_json = {k: v[0] if len(v) == 1 else v for k, v in request_body_dict.items()}

            elif content_type.startswith("multipart/form-data"):
                # Parse multipart/form-data
                req.post_data_encoded = request.content.decode("utf-8", errors="replace")
                req.post_data_json = self.parse_multipart_form_data(request.content, content_type)

            else:
                # Treat as raw body
                req.post_data_encoded = request.content.decode("utf-8", errors="replace")
                request_body_dict = parse_qs(req.post_data_encoded)
                req.post_data_json = {k: v[0] if len(v) == 1 else v for k, v in request_body_dict.items()}

        req.extract_param_value()
        return req

    def check_and_save_req(self, request, response=None):
        if (is_same_domain(request.pretty_url)):
            if (response and self.is_filtered_response(response)):
                print(f"[ANALYZER] Skipping the URL of {request.path}")
            else:
                if self.is_avoided_links("TXT", request.path):
                    print(f"[ANALYZER] Abort the request because it is avoided string: {request.path}")
                else:
                    req = self.convert_request_type(request, "Admin")
                    if "referer" in req.header:
                        print(f"[ANALYZER] ---INTERCEPTING REQUEST FROM: {req.header['referer']} ---")
                    else:
                        print(f"[ANALYZER] ---INTERCEPTING REQUEST---")

                    return self.save_to_corpus(req)
        else:
            print(f"[ANALYZER] NOT SAME DOMAIN {request}")
        return None


    def get_data_from_list(self,list_data, name):
        ## We assume the value of list data = [{'name': 'host', 'value': 'localhost:8088'}, {'name': 'User-Agent', 'value': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0'}, {'name': 'Accept', 'value': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}, {'name': 'Accept-Language', 'value': 'en-US,en;q=0.5'}, {'name': 'Connection', 'value': 'keep-alive'}, {'name': 'Upgrade-Insecure-Requests', 'value': '1'}, {'name': 'Priority', 'value': 'u=0, i'}]
        for data in list_data:
            if "name" in data and data["name"]==name:
                return data
        return None

    def convert_list_to_dict(self,list_data):
        ## We assume the value of list data = [{'name': 'host', 'value': 'localhost:8088'}, {'name': 'User-Agent', 'value': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0'}, {'name': 'Accept', 'value': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}, {'name': 'Accept-Language', 'value': 'en-US,en;q=0.5'}, {'name': 'Connection', 'value': 'keep-alive'}, {'name': 'Upgrade-Insecure-Requests', 'value': '1'}, {'name': 'Priority', 'value': 'u=0, i'}]
        dict_data = {}
        for data in list_data:
            if "name" in data and "value" in data:
                dict_data[data["name"]] = data["value"]
        return dict_data

    def is_avoided_links(self, txt, url: str):
        for key in config.data["AVOIDED_LINKS"]:
            if txt.lower().find(key)>-1 or url.find(key)>-1:
                print(f"[MAINDRIVER {self.role}] {txt}[{url}] is an avoided links! Drop it.")
                return True
        return False

    def store_request_to_file_as_attack_surface(self, request, foldername="default"):
        if "PROJECT_NAME" in config.data:
            foldername = config.data["PROJECT_NAME"]
        print(f"[MAINDRIVER {self.role}] Storing the request as the attack surface to a file in dir:", foldername)
        dir_location = os.path.join(os.getcwd(), '../attack_surface', foldername, self.role)
        if not os.path.exists(dir_location):
            os.makedirs(dir_location, exist_ok=True)

        filename = f"{self.corpus_length}.yaml"
        request.saved_filename = filename
        with open(f"{dir_location}/{filename}", "w") as txt_file:
            txt_file.write(convert_request_to_yaml(request))

    def save_to_global_attack_surfaces(self, request: HTTPRequest):
        print(f"[ANALYZER] Save it to Global Attack Surface")
        attack = AttackSurface(request)
        global_attack_surfaces.add(attack, self.role)

    def save_to_corpus(self, req):
        ## CONVERT AND DROP THE COOKIE HEADER
        if req not in self.corpus:
            self.corpus.append(req)
            print(f"[ANALYZER] Save a new request to Corpus", req)
            print(f"[ANALYZER] Corpus length:", len(self.corpus))

            self.save_to_global_attack_surfaces(req)

            self.corpus_length = len(self.corpus)

            self.store_request_to_file_as_attack_surface(req)
            return req

        else:
            print(f"[ANALYZER] Drop the request because it already exists in Corpus", req)
        return None
