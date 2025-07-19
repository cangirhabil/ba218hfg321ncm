import string
import random
from urllib.parse import urlencode, parse_qsl

from playwright._impl._js_handle import Serializable
from playwright.async_api import APIResponse
from playwright.sync_api import Request
import copy

from AICaller import build_prompt, AICaller, parse_response, build_expand_prompt, \
    build_generation_prompt  # parseForGettingPayloads
from HTTPRequest import HTTPRequest
from config import config
from Dictionary import dictionary
from function import compare_request
from VerificationLabel import VerificationLabel


def randomword():
    length = random.randint(1,20)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def randomstring(length=0):
    if length==0:
        length = random.randint(1,20)
    letters = string.printable
    return ''.join(random.choice(letters) for i in range(length))

def put_random(ori_data: Serializable):
    for key in ori_data:
        if key == "user_id":
            continue
        elif key == "role":
            # continue
            ori_data[key] = random.choice(['subscriber','contributor','author','editor','administrator'])
        elif key == "action":
            continue
        elif key == "_wpnonce":
            continue
        elif key == "email":
            continue
        elif key == "url":
            continue
        else:
            ori_data[key] = randomword()

    return ori_data

def parse_encoded_params(encoded_params):
    parsed_result = {}
    pairs = parse_qsl(encoded_params)
    for name, value in pairs:
            parsed_result[name] = value
    return parsed_result


def change_HTTP_method(request: HTTPRequest):
    print("----CALL change_HTTP_method-----")
    reqs = list()
    methods = ["GET","POST","PUT","PATCH","HEAD"]

    if request.method in methods:
        methods.remove(request.method)

    req = copy(request)
    req.method = random.choice(methods)
    reqs.append(req)

    req2 = copy(request)
    req2.method = random.choice(methods)
    reqs.append(req2)

    return reqs

def randomly_generated_payload_strings(request: HTTPRequest):
    print("----CALL randomly_generated_payload_strings-----")
    reqs = list()

    MAX_PAYLOAD = 5
    payload = {}
    payload_number = random.randint(1,MAX_PAYLOAD)
    for i in range (payload_number):
        payload[randomword()] = randomstring()

    req = copy(request)
    req.post_data_encoded = urlencode(payload, doseq=True)
    reqs.append(req)

    return reqs

def alter_paramval(p):
    p.is_mutated = True
    if p.type=="int":
        newvalue = int(p.value)
        newvalue +=1
        p.value = str(newvalue)
    elif p.type=="email":
        p.value = randomword()+"@yahoo.com"
    else:
        p.value = randomword()
    print("[MUTATION] After Mutation:",p)

def alter_generated_system_data(request: HTTPRequest):
    print("[MUTATION] ----CALL alter_generated_system_data-----")
    reqs = list()

    request.source="alter_generated_system_data"
    param_values = request.get_system_generated_param_vals(dropping_nonce=True)
    usergen_param_values = request.get_all_atomic_param_vals(dropping_nonce=True, only_user_param=True)
    if len(param_values)>0:
        num_mutated_param = 1
        chosen_param_values = random.choices(param_values,k=num_mutated_param) + random.choices(usergen_param_values,k=num_mutated_param)
        print(f"[MUTATION] Mutating {len(chosen_param_values)} paramvals")
        for p in chosen_param_values:
            if p.is_nonce:
                print(f"[MUTATION] Skip {p} because it is nonce")
                continue
            print("[MUTATION] Mutate",p)

            if p.is_nested():
                n = random.randint(0,len(p.paramvals)-1)
                chosen_pvs = random.choices(p.paramvals,k=n)
                print(f"[MUTATION] Mutating {len(chosen_pvs)} paramvals in nested {p}")
                for pv_nested in chosen_pvs:
                    alter_paramval(pv_nested)
            else:
                alter_paramval(p)

            p.is_mutated = True
        request.update_param_from_paramvals()
        reqs.append(request)
    else:
        """ Just adding random paramvals without mutating the values"""
        num_mutated_param = random.randint(0,4)
        paramvals = list()
        for i in range(num_mutated_param):
            pv = dictionary.get_random_system_generated_paramval()
            p = copy.deepcopy(pv)
            p.is_mutated = True
            paramvals.append(p)
        request.update_param_from_paramvals(paramvals)
        reqs.append(request)
    return reqs

def cross_mutation_generated_system_data(request: HTTPRequest):
    print("[MUTATION] ----CALL cross_mutation_generated_system_data-----")
    reqs = list()

    request.source="cross_mutation_generated_system_data"
    param_values = request.get_system_generated_param_vals()
    usergen_param_values = request.get_all_atomic_param_vals(dropping_nonce=True, only_user_param=True)
    if len(param_values)>0:
        num_mutated_param = random.randint(0,len(param_values)-1)
        num_mutated_usergen_param = random.randint(0,len(usergen_param_values)-1)
        chosen_param_values = random.choices(param_values,k=num_mutated_param) + random.choices(usergen_param_values,k=num_mutated_usergen_param)
        print(f"[MUTATION] Mutating {len(chosen_param_values)} paramvals")
        for p in chosen_param_values:
            if p.is_nonce:
                print(f"[MUTATION] Skip {p} because it is nonce")
                continue

            if p.is_nested():
                n = random.randint(0,len(p.paramvals)-1)
                chosen_pvs = random.choices(p.paramvals,k=n)
                print(f"[MUTATION] Mutating {len(chosen_pvs)} paramvals in nested {p}")
                for pv_nested in chosen_pvs:
                    pv_nested.value = dictionary.get_random_paramval().value
                    pv_nested.is_mutated = True
            else:
                p.value = dictionary.get_random_paramval().value

            p.is_mutated = True
            print("[MUTATION] Changed! ",p)
        request.update_param_from_paramvals()
        reqs.append(request)
    else:
        num_mutated_param = random.randint(0,4)
        paramvals = list()
        for i in range(num_mutated_param):
            pv = dictionary.get_random_system_generated_paramval()
            p = copy.deepcopy(pv)
            p.is_mutated = True
            paramvals.append(p)
        request.update_param_from_paramvals(paramvals)
        reqs.append(request)
    return reqs

def add_generated_system_data(request: HTTPRequest):
    print("[MUTATION] ----CALL add_generated_system_data-----")
    reqs = list()

    request.source="add_generated_system_data"
    num_mutated_param = 1
    paramvals = list()
    for i in range(num_mutated_param):
        pv = dictionary.get_random_system_generated_paramval()
        p = copy.deepcopy(pv)
        p.is_mutated = True

        if p.is_nested():
            n = random.randint(0,len(p.paramvals)-1)
            chosen_pvs = random.choices(p.paramvals,k=n)
            print(f"[MUTATION] Mutating {len(chosen_pvs)} paramvals in nested {p}")
            for pv_nested in chosen_pvs:
                alter_paramval(pv_nested)
        else:
            alter_paramval(p)


        paramvals.append(p)
    request.update_param_from_paramvals(paramvals, is_drop_previous_paramvals=False)
    reqs.append(request)
    return reqs

def add_usergen_data(request: HTTPRequest):
    print("[MUTATION] ----CALL add_usergen_data-----")
    reqs = list()

    request.source="add_usergen_data"
    num_mutated_param = 1
    paramvals = list()
    req_params = [p.param for p in request.get_all_atomic_param_vals()]
    for i in range(num_mutated_param):
        pv = dictionary.get_random_user_generated_paramval(avoid_param_names=req_params)
        p = copy.deepcopy(pv)
        p.is_mutated = True

        if p.is_nested():
            n = random.randint(0,len(p.paramvals)-1)
            chosen_pvs = random.choices(p.paramvals,k=n)
            print(f"[MUTATION] Mutating {len(chosen_pvs)} paramvals in nested {p}")
            for pv_nested in chosen_pvs:
                alter_paramval(pv_nested)
        else:
            alter_paramval(p)

        paramvals.append(p)
    request.update_param_from_paramvals(paramvals, is_drop_previous_paramvals=False)
    reqs.append(request)
    return reqs


def randomly_alter_existing_payload_strings(request: HTTPRequest):
    print("----CALL randomly_alter_existing_payload_strings-----")
    reqs = list()

    MAX_PAYLOAD_LENGTH = 5
    try:
        existing_payload = parse_encoded_params(request.post_data_encoded)
        if (len(existing_payload)>0):
            payload_number = random.randint(0,len(existing_payload)-1)
            payload_key = list(existing_payload.keys())[payload_number]
            existing_payload[payload_key] += randomstring(MAX_PAYLOAD_LENGTH)
        else:
            existing_payload[randomword()] = randomstring()

        req = copy(request)
        req.post_data_encoded = urlencode(existing_payload, doseq=True)
        reqs.append(req)
    except Exception as e:
        print("Error on parsing post data:", e)

    return reqs

def randomly_alter_existing_paramvals(request: HTTPRequest):
    print("----CALL randomly_alter_existing_paramvals-----")
    reqs = list()

    MAX_PAYLOAD_LENGTH = 5
    try:
        req = copy(request)
        req.update_id()
        if len(request.paramvals)>0:
            payload_number = random.randint(0,len(req.paramvals)-1)
            req.paramvals[payload_number].value = randomstring(MAX_PAYLOAD_LENGTH)
            req.update_param_from_paramvals()
        else:
            return None

        reqs.append(req)
    except Exception as e:
        print("Error on parsing post data:", e)

    return reqs

def sysgendictid_mutate_with_any_id2(param_name, role, old_val):
    print(f"[MUTATION {role}] ----CALL sysgendictid_mutate_with_any_id-----")
    iter = 0
    value = dictionary.get_random_system_generated_paramval(only_numeric=True, avoided_role=role).value
    while old_val==value and iter<10:
        value = dictionary.get_random_system_generated_paramval(only_numeric=True, avoided_role=role).value
        iter += 1

    if (old_val!=value):
        return value

    return None

def sysgendictid_mutate_iterate(param_name, role, old_val):
    print(f"[MUTATION {role}] ----CALL sysgendictid_mutate_iterate to get a mutated value-----")
    try:
        new_val = int(old_val) + 1
        role_values = dictionary.get_role_values(role,param_name)
        print(f"[MUTATION {role}] Initial old value: {old_val}, mutated value: {new_val}, and existing values: ", role_values)
        while str(new_val) in role_values:
            new_val = new_val + 1
        return str(new_val)
    except Exception as e:
        print(f"[MUTATION {role}] Failed to iterate {old_val} because", e)

    return None

def sysgendictid_mutate_with_any_id(param_name, role, old_val):
    print(f"[MUTATION {role}] ----CALL sysgendictid_mutate_with_any_id to get a mutated value-----")
    values = dictionary.get_complement_id_ref_values(param_name, role)

    if len(values)>0:
        iter = 0
        val = random.choice(values)
        while old_val==val and iter<5:
            val = random.choice(values)
            iter += 1

        if (old_val!=val):
            return val

    return None

def sysgendictid_mutate_with_same_name(param_name, role, old_val):
    print(f"[MUTATION {role}] ----CALL sysgendictid_mutate_with_same_name to get a mutated value-----")
    values = dictionary.get_complement_values(role,param_name)
    print(f"[MUTATION {role}] Getting complement_values:",str(values))

    if len(values)>0:
        iter = 0
        val = random.choice(values)
        while old_val==val and iter<5:
            val = random.choice(values)
            print(f"[MUTATION {role}] Got a value: {val}")
            iter += 1

        if (old_val!=val):
            return val

    return None

def sysgendict_mutate_id_or_non_and_others(sysgen_param_values, role, request):
    print(f"[MUTATION {role}] ----CALL sysgendict_mutate_id_or_non_and_others-----")

    mutation_function = sysgendict_mutate
    num_mutated_param = 1
    if (mutation_function(sysgen_param_values, role, request)):
        usergen_param_values = request.get_all_atomic_param_vals(dropping_nonce=True, only_user_param=True)
        if len(usergen_param_values)>0:
            chosen_param_values = usergen_param_values
            print(f"[MUTATION {role}] Mutating {len(chosen_param_values)} user-gen paramvals")
            for p in chosen_param_values:
                if p.is_nonce:
                    print(f"[MUTATION {role}] Skip {p} because it is nonce")
                    continue
                if p.is_nested():
                    print(f"[MUTATION {role}] Skip {p} because it is nested")
                    continue

                print(f"[MUTATION {role}] Mutating user-gen paramname: {p.param}")
                alter_paramval(p)
                p.is_mutated = True
                print("[MUTATION] Changed! ",p)
        else:
            print(f"[MUTATION {role}] No user-gen paramvals, only mutating the ID")
        return True
    return False

def sysgendict_mutate_id(sysgen_param_values, role, request):
    """
    Choose one/more numeric-type param, and change its value with other numeric-type params in dictionary
    :param sysgen_param_values:
    :return:
    """
    print(f"[MUTATION {role}] ----CALL sysgendict_mutate_id-----")

    numeric_sysgen_param_values = [p for p in sysgen_param_values if p.is_id ]
    if len(numeric_sysgen_param_values)==0:
        print(f"[MUTATION {role}] The request does not have numeric sys-gen data. Aborting the mutation")
        return False

    num_mutated_param = random.randint(1,len(numeric_sysgen_param_values))
    chosen_param_values = random.choices(numeric_sysgen_param_values,k=num_mutated_param)
    print(f"[MUTATION {role}] Mutating {len(chosen_param_values)} sys-gen paramvals")

    for p in chosen_param_values:
        if p.is_nonce:
            print(f"[MUTATION {role}] Skip {p} because it is nonce")
            continue

        if p.is_nested():
            print(f"[MUTATION {role}] Skip {p} because it is nested")
            continue

        print(f"[MUTATION {role}] Mutating paramname: {p.param}")

        mutation_functions = random.choices([
            sysgendictid_mutate_with_same_name,
            sysgendictid_mutate_with_any_id],
            weights=[1,1])
        mutation_function = mutation_functions[0]

        value = mutation_function(p.param, role, p.value)

        if value is None:
            print(f"[MUTATION {role}] Failed to find a new value for {p}. Will try another mutation function")
            value = sysgendictid_mutate_with_any_id(p.param, role, p.value)


        if value:
            p.value = value
            p.is_mutated = True
            print(f"[MUTATION {role}] Changed! ",p)
            return True
        else:
            print(f"[MUTATION {role}] Still Failed to find a new value for ",p)
            return False

def sysgendictid_mutate_with_any_text(param_name, role, old_val):
    print(f"[MUTATION {role}] ----CALL sysgendictid_mutate_with_any_text to get a mutated value-----")
    values = dictionary.get_complement_non_id_values(param_name, role)

    if len(values)>0:
        iter = 0
        val = random.choice(values)
        while old_val==val and iter<5:
            val = random.choice(values)
            iter += 1

        if (old_val!=val):
            return val

    return None

def sysgendict_mutate_non_id(sysgen_param_values, role, request):
    """
    Choose one/more non numeric-type param, and change its value with other non numeric-type params in dictionary
    :param sysgen_param_values:
    :return:
    """
    print(f"[MUTATION {role}] ----CALL sysgendict_mutate_non_id-----")

    text_sysgen_param_values = [p for p in sysgen_param_values if not p.is_id ]
    if len(text_sysgen_param_values)==0:
        print(f"[MUTATION {role}] The request does not have text sys-gen data. Aborting the mutation")
        return False

    num_mutated_param = random.randint(1,len(text_sysgen_param_values))
    chosen_param_values = random.choices(text_sysgen_param_values,k=num_mutated_param)
    print(f"[MUTATION {role}] Mutating {len(chosen_param_values)} of text sys-gen paramvals")

    for p in chosen_param_values:
        if p.is_nonce:
            print(f"[MUTATION {role}] Skip {p} because it is nonce")
            continue

        if p.is_nested():
            print(f"[MUTATION {role}] Skip {p} because it is nested")
            continue

        print(f"[MUTATION {role}] Mutating paramname: {p.param}")

        mutation_functions = random.choices([
            sysgendictid_mutate_with_same_name,
            sysgendictid_mutate_with_any_text],
            weights=[1,1])
        mutation_function = mutation_functions[0]

        value = mutation_function(p.param, role, p.value)

        if value is None:
            print(f"[MUTATION {role}] Failed to find a new value for {p}. Will try another mutation function")
            value = sysgendictid_mutate_with_any_text(p.param, role, p.value)

        if value:
            p.value = value
            p.is_mutated = True
            print(f"[MUTATION {role}] Changed! ",p)
            return True
        else:
            print(f"[MUTATION {role}] Failed to find a new value for ",p)
            return False

def get_weight(sysgen_param_values):
    weights = []
    values = []
    names = []
    for p in sysgen_param_values:
        values.append(p.value)
        names.append(p.param)
        if p.is_id:
            weights.append(2)
        else:
            weights.append(1)
    print(f"[MUTATION] names, values, and weights: ", names, values,weights)
    return weights

def id_mutate(p, role):
    ## p is ParamVal
    if p.is_nonce:
        print(f"[MUTATION {role}] Skip {p} because it is nonce")
        return False

    if p.is_nested():
        print(f"[MUTATION {role}] Skip {p} because it is nested")
        return False

    print(f"[MUTATION {role}] Mutating paramname: {p.param}")
    value = sysgendictid_mutate_iterate(p.param, role, p.value)

    if value:
        print(f"[MUTATION {role}] Successfully find a new value for {p} ==> {value}")
    else:
        print(f"[MUTATION {role}] Failed to find a new value for {p}. Will try another mutation function")

        value = sysgendictid_mutate_with_same_name(p.param, role, p.value)

        if value:
            print(f"[MUTATION {role}] Finally, successfully find a new value for {p} ==> {value}")
        else:
            print(f"[MUTATION {role}] Failed again to find a new value for {p}. Will try another mutation function")

            if p.is_id:
                value = sysgendictid_mutate_with_any_id(p.param, role, p.value)
            else:
                value = sysgendictid_mutate_with_any_text(p.param, role, p.value)

    if value:
        p.value = value
        p.is_mutated = True
        print(f"[MUTATION {role}] Changed! ",p)
        return True
    else:
        print(f"[MUTATION {role}] Failed to find a new value for ",p)
        return False

def usergen_mutate(request, role):
    usergen_param_values = request.get_all_atomic_param_vals(dropping_nonce=True, only_user_param=True)
    if len(usergen_param_values)>0:
        must_be_same_value = None
        chosen_param_values = usergen_param_values
        print(f"[MUTATION {role}] Mutating {len(chosen_param_values)} user-gen paramvals")
        for p in chosen_param_values:
            if p.is_nonce:
                print(f"[MUTATION {role}] Skip {p} because it is nonce")
                continue
            if p.is_nested():
                print(f"[MUTATION {role}] Skip {p} because it is nested")
                continue

            print(f"[MUTATION {role}] Mutating user-gen paramname: {p.param}")
            alter_paramval(p)
            p.is_mutated = True

            if p.param and p.param.find("password")>-1:
                if must_be_same_value:
                    p.value = must_be_same_value
                else:
                    must_be_same_value = p.value

            print("[MUTATION] Changed! ",p)

def sysgendict_mutate(sysgen_param_values, role, request):
    print(f"[MUTATION {role}] ----CALL sysgendict_mutate-----")

    num_mutated_param = 1
    chosen_param_values = random.choices(sysgen_param_values,k=num_mutated_param,weights=get_weight(sysgen_param_values))
    print(f"[MUTATION {role}] Mutating {len(chosen_param_values)} of sys-gen paramvals")

    for p in chosen_param_values:
        if p.is_nonce:
            print(f"[MUTATION {role}] Skip {p} because it is nonce")
            continue

        if p.is_nested():
            print(f"[MUTATION {role}] Skip {p} because it is nested")
            continue

        print(f"[MUTATION {role}] Mutating paramname: {p.param}")

        if p.is_id:
            mutation_functions = random.choices([
                sysgendictid_mutate_with_same_name,
                sysgendictid_mutate_with_any_id,
                sysgendictid_mutate_iterate],
                weights=[1,1,2])
        else:
            mutation_functions = random.choices([
                sysgendictid_mutate_with_same_name,
                sysgendictid_mutate_with_any_text],
                weights=[1,1])

        mutation_function = mutation_functions[0]
        value = mutation_function(p.param, role, p.value)

        if value:
            print(f"[MUTATION {role}] Successfully find a new value for {p} ==> {value}")
        else:
            print(f"[MUTATION {role}] Failed to find a new value for {p}. Will try another mutation function")

            if p.is_id:
                value = sysgendictid_mutate_with_any_id(p.param, role, p.value)
            else:
                value = sysgendictid_mutate_with_any_text(p.param, role, p.value)

        if value:
            p.value = value
            p.is_mutated = True
            print(f"[MUTATION {role}] Changed! ",p)
            return True
        else:
            print(f"[MUTATION {role}] Failed to find a new value for ",p)
            return False

def sysgen_dictionary_mutation(request: HTTPRequest, role):
    print(f"[MUTATION {role}] ----CALL sysgen_dictionary_mutation-----")
    reqs = list()

    request.source="sysgen_dictionary_mutation"
    param_values = request.get_system_generated_param_vals(dropping_nonce=True, atomic_val_only=True)

    if len(param_values)==0:
        print(f"[MUTATION {role}] Request {request} does not have sysgen data. Drop it")
        return reqs

    ## [See the root cause analysis! There are several options: mutate object ID (numeric-type) or supply new params
    ## TASK: CREATE NON ID SYS GEN MUTATION

    mutation_functions = random.choices([
        sysgendict_mutate,
        sysgendict_mutate_id_or_non_and_others],
        weights=[1,1])
    mutation_function = mutation_functions[0]

    if mutation_function(param_values, role=role, request=request):
        request.update_param_from_paramvals()
        reqs.append(request)

    return reqs

def sysgen_dictionary_insertion(request: HTTPRequest, role):
    print(f"[MUTATION {role}] ----CALL sysgen_dictionary_insertion-----")
    reqs = list()

    request.source="sysgen_dictionary_insertion"
    existing_param_values = request.get_system_generated_param_vals()
    existing_paramnames = [p.param for p in existing_param_values]
    chosen_sysgen_paramval = dictionary.get_random_system_generated_paramval(avoided_paramnames=existing_paramnames)
    if chosen_sysgen_paramval:
        copied_chosen_sysgen_paramval = copy.deepcopy(chosen_sysgen_paramval)
        copied_chosen_sysgen_paramval.is_mutated = True
        copied_chosen_sysgen_paramval.BAC_label = VerificationLabel.UNDEFINED

        print(f"[MUTATION {role}] Inserting paramname: {copied_chosen_sysgen_paramval}")
        request.update_param_from_paramvals([copied_chosen_sysgen_paramval], is_drop_previous_paramvals=False)
        reqs.append(request)
    else:
        print(f"[MUTATION {role}] Failed to get sysgen param. Will try another mutation function")
        reqs = sysgen_dictionary_mutation(request, role)

    return reqs

def sysgen_LLM_generation(chosen_attack_surface, role):
    print(f"[MUTATION {chosen_attack_surface.target.role}] ----CALL sysgen_LLM_generation-----")
    chosen_reqs, response_titles = chosen_attack_surface.getAllRequests(maxNumber=5)
    prompt = build_generation_prompt(chosen_reqs, response_titles)

    print(f"[MUTATION {chosen_attack_surface.target.role}] Prompt:", prompt)

    try:
        ai_caller = AICaller(config.AIModel, "test-api")
        response, prompt_tokens, response_tokens = ai_caller.call_model(
            prompt, max_tokens=4096
        )

        payloads, urls = parse_response(response)
        print(f"[MUTATION {chosen_attack_surface.target.role}] LLM results: URL: {urls} and payloads: {payloads}")

        if len(chosen_reqs)>0:
            reqs = list()
            idx = -1
            for payload in payloads:
                idx +=1
                if idx>=len(chosen_reqs):
                    idx = 0


                req = copy.deepcopy(chosen_reqs[idx])
                if req.extract_additional_param_value_from_post_encode(payload,is_mutated=True, source="LLM"):
                    if req==chosen_reqs[idx]:
                        print(f"[MUTATION {chosen_attack_surface.target.role}] Drop this request from LLM because it is the same with the existing", req)
                    else:
                        print(f"[MUTATION {chosen_attack_surface.target.role}] Save the new mutated request from LLM")
                        print(f"[MUTATION {chosen_attack_surface.target.role}] Inserting paramname: {payload}")
                        reqs.append(req)
            return reqs
    except Exception as e:
        print(e)
    return None


## -------------------

def BOLA_mutator(request: HTTPRequest, role=None):
    print(f"[MUTATION {role}] ----CALL BOLA_mutator-----")
    reqs = list()

    if role==None:
        role = request.role

    request.source = "BOLA_mutator"
    param_values = request.get_reference_param_vals(dropping_nonce=True, atomic_val_only=True)

    if len(param_values)==0:
        print(f"[MUTATION {role}] Request {request} does not have param reference data. Drop it")
        return reqs

    mutation_functions = random.choices([
        sysgendict_mutate,
        sysgendict_mutate_id_or_non_and_others],
        weights=[1,1])
    mutation_function = mutation_functions[0]

    if mutation_function(param_values, role=role, request=request):
        request.update_param_from_paramvals()
        reqs.append(request)

    return reqs

def BOPLA_mutator(request: HTTPRequest, role):
    print(f"[MUTATION {role}] ----CALL BOPLA_mutator-----")
    reqs = list()

    request.source = "BOPLA_mutator"
    existing_param_values = request.get_reference_param_vals()
    if len(existing_param_values)==0:
        print(f"[MUTATION {role}] Request {request} does not have param reference data. Drop it")
        return reqs

    existing_paramnames = [p.param for p in existing_param_values]
    chosen_sysgen_paramval = dictionary.get_random_reference_paramval(avoided_paramnames=existing_paramnames)
    if chosen_sysgen_paramval:
        copied_chosen_sysgen_paramval = copy.deepcopy(chosen_sysgen_paramval)
        copied_chosen_sysgen_paramval.is_mutated = True
        copied_chosen_sysgen_paramval.is_added_property = True
        copied_chosen_sysgen_paramval.BAC_label = VerificationLabel.UNDEFINED

        print(f"[MUTATION {role}] Inserting paramname: {copied_chosen_sysgen_paramval}")
        request.update_param_from_paramvals([copied_chosen_sysgen_paramval], is_drop_previous_paramvals=False)
        reqs.append(request)
    else:
        print(f"[MUTATION {role}] Failed to get sysgen param. Will try another mutation function")
        reqs = BOLA_mutator(request, role)

    return reqs