class OctopusError(Exception):
    def __init__(self, response_text, response_code):
        self.response_text = response_text
        self.response_code = response_code
        self.message = self.__str__()
        super(OctopusError, self).__init__(self.message)

    def __str__(self):
        return "Error %s: %s" % (self.response_code,
                                 self.response_text)

    def __repr__(self):
        return (('<OctopusError: code=%s, '
                 'text=%s>')
                % (self.response_text,
                   self.response_code))
