def create_http_response(status, response_body):

    response_line = "HTTP/1.1 %s\r\n" % status

    response_header = "Server: pwd/1.0\r\n"

    response_blank = "\r\n"

    response_data = (response_line + response_header + response_blank).encode() + response_body

    return response_data