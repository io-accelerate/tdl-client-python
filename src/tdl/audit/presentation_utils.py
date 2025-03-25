import json
from collections.abc import Sequence


class PresentationUtils:

    @staticmethod
    def to_displayable_request(request):
        compressed_params = []
        for param in request.params:
            representation = json.dumps(param, separators=(',', ':'))

            # result is array-like, needs a bit more spacing
            if PresentationUtils.is_list(param):
                representation = representation.replace(',', ', ')
            elif PresentationUtils.is_multiline_string(representation):
                representation = PresentationUtils.suppress_extra_lines(representation)
            
            compressed_params.append(representation)
            
        params_as_string = ', '.join(compressed_params)
        return 'id = {id}, req = {method}({params})'.format(
            id=request.id,
            method=request.method,
            params=params_as_string)

    @staticmethod
    def to_displayable_response(response):
        if response.id == 'error':
            return 'error = "{0}", (NOT PUBLISHED)'.format(response.result)
        else:
            value = response.result
            representation = json.dumps(response.result, separators=(',', ':'))

            # result is array-like, needs a bit more spacing
            if PresentationUtils.is_list(value):
                representation = representation.replace(',', ', ')
            elif PresentationUtils.is_multiline_string(representation):
                representation = PresentationUtils.suppress_extra_lines(representation)

            return 'resp = {0}'.format(representation)

    @staticmethod
    def is_list(value):
        isinstance(value, Sequence) and not isinstance(value, str)

    @staticmethod
    def is_multiline_string(value):
        return "\\n" in value

    @staticmethod
    def suppress_extra_lines(parameter):
        if not isinstance(parameter, str):
            return str(parameter)
    
        parts = parameter.split("\\n")
        representation = parts[0]
    
        suppressed_parts = len(parts) - 1
        representation += " .. ( "+ str(suppressed_parts) +" more line"
    
        if suppressed_parts > 1:
            representation += "s"
    
        representation += " )\""
        return representation
