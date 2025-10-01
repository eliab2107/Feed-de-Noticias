class Little_Parser():
    def __init__(self, data):
        self.data = data
        self.method = None
        self.path = None
        self.version = None
        self.headers = {}
        self.unique_name = None
        self.body = None
        self.parse_request()

    def parse_request(self):
        lines = self.data.split("\r\n")
        request_line = lines[0].split(" ")
        #Method, Path e Version
        if len(request_line) == 3:
            self.method, self.path, self.version = request_line
        else:
            raise ValueError("Invalid HTTP request line")

        header_lines = []
        body_lines = []
        is_body = False

        for line in lines[1:]:
            if line == "":
                is_body = True
                continue
            if is_body:
                body_lines.append(line)
            else:
                header_lines.append(line)

        for header in header_lines:
            key, value = header.split(":", 1)
            self.headers[key.strip()] = value.strip()

        self.body = "\r\n".join(body_lines) if body_lines else None

    def get_method(self):
        return self.method

    def get_path(self):
        return self.path

    def get_version(self):
        return self.version

    def get_headers(self):
        return self.headers

    def get_body(self):
        return self.body
    
    def get_unique_name(self):
        return self.body["unique_name"]
    
    
class Builder_Message():
    def __init__(self, status_code=200, reason_phrase="OK", headers=None, body=""):
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.headers = headers if headers is not None else {}
        self.body = body

    def build_response(self):
        response_line = f"HTTP/1.1 {self.status_code} {self.reason_phrase}\r\n"
        header_lines = ""
        
        if self.body:
            self.headers["Content-Length"] = str(len(self.body))
        
        for key, value in self.headers.items():
            header_lines += f"{key}: {value}\r\n"
        
        blank_line = "\r\n"
        response_body = self.body if self.body else ""
        
        return response_line + header_lines + blank_line + response_body
    
    def build_request(self, method, path, version="HTTP/1.1"):
        request_line = f"{method} {path} {version}\r\n"
        header_lines = ""
        
        if self.body:
            self.headers["Content-Length"] = str(len(self.body))
        
        for key, value in self.headers.items():
            header_lines += f"{key}: {value}\r\n"
        
        blank_line = "\r\n"
        request_body = self.body if self.body else ""
        
        return request_line + header_lines + blank_line + request_body