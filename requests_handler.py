def parse_input_data(data: str):
    result = {}
    if data:
        params = data.split('&')
        for param in params:
            key, value = param.split('=')
            result[key] = value
    return result


class GetRequests:

    @staticmethod
    def get_request_params(env):
        query_string = env['QUERY_STRING']
        request_params = parse_input_data(query_string)
        return request_params


class PostRequests:

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        print(env)
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        print(data)
        return data

    @staticmethod
    def parse_wsgi_input_data(data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = parse_input_data(data_str)
        return result

    def get_request_params(self, env):
        data = self.get_wsgi_input_data(env)
        data = self.parse_wsgi_input_data(data)
        return data
