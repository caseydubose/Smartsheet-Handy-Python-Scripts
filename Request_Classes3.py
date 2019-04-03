import requests
import json
import string
import sys
import os
import maintoken
import time


class call:
    def __init__(self, url, token, package, headers=None, counter=5):
        self.url = url
        self.token = token
        self.headers = {"Authorization": str("Bearer " + self.token), 'Content-Type': 'application/json'}
        self.counter = counter
        self.package = package
        self.params = "none"

    def update_attr(self, item, newValue):
        setattr(self, item, newValue)

    def get_item(self, item):
        value = getattr(self, item)
        return value

    def execute_call(self, counter):
        1 == 1

    def error_catcher(self, output):
        if output["errorCode"] == "4003" or output["message"] == "Rate limit exceeded":
            self.rate_limit_backoff(output)
        print("Found Error")
        print(output)

    def rate_limit_backoff(self, output):
        counter = self.get_item("counter")
        counter -= 1
        time.sleep(60)
        print("rate limit backoff initiated")
        self.execute_call(counter)


class get_call(call):
    def __init__(self, url, token, params, counter=5):
        self.url = url
        self.token = token
        self.headers = {"Authorization": str("Bearer " + self.token), 'Content-Type': 'application/json'}
        self.params = params
        counter = counter

    def execute_call(self, counter):
        URL = self.get_item("url")
        headers = self.get_item("headers")
        params = self.get_item("params")
        output = requests.get(URL, headers=headers, params=params)
        output = output.json()
        if "errorCode" in output:
            self.error_catcher(output)
        return output


class put_call(call):
    def execute_call(self, counter):
        URL = self.get_item("url")
        headers = self.get_item("headers")
        package = self.get_item("package")
        output = requests.put(URL, headers=headers, data=json.dumps(package))
        output = output.json()
        if "errorCode" in output or "errorCode" in output:
            self.error_catcher(output)
        return output


class post_call(call):
    def execute_call(self, counter):
        URL = self.get_item("url")
        headers = self.get_item("headers")
        package = self.get_item("package")
        output = requests.post(URL, headers=headers, data=json.dumps(package))
        output = output.json()
        if "errorCode" in output:
            self.error_catcher(output)
        return output



