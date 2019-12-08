from application import utils
from application import urls
import re
import time
from application import funs_ajax


def parse_requset(request_data):

    request_text = request_data.decode()

    loc = request_text.find("\r\n")

    request_line = request_text[:loc]

    request_line_list = request_line.split(" ")

    file_path = request_line_list[1]

    if file_path == "/":
        file_path = "/index.html"

    return file_path


def application(current_dir, request_data, ip_port):

    file_path = parse_requset(request_data)

    resource_path = current_dir + file_path

    response_data = ""

    if file_path.endswith(".html"):

        # print(file_path)
    #     # if file_path in urls.route_dict:

        for key, values in urls.route_dict.items():
            print(key+"-------->")
            print(file_path)
            ls = re.match(key, file_path)
            # print(ls)
            if ls:
                # func = urls.route_dict[file_path]
                func = values

                response_body = func(file_path)

                response_data = utils.create_http_response("200 Ok", response_body.encode())

                break

            else:
                response_body = "Sorry page Not Found ! 404"

                response_data = utils.create_http_response("404 Not Found", response_body.encode())

    else:
        try:

            with open(resource_path, "rb") as file:

                response_body = file.read()

            response_data = utils.create_http_response("200 OK", response_body)

        except Exception as rs:

            response_body = "Error! (%s)" % str(rs)

            response_body = response_body.encode()

            response_data = utils.create_http_response("404 Not Found", response_body)

    return response_data
