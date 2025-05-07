def encode_url(url):
    file_name = (url.replace('https://', '')
                 .replace('/', '_slash_')
                 .replace('\\', '_double_back_slash_')
                 .replace(':', '_colon_')
                 .replace('*', '_asterisk_')
                 .replace('?', '_question_')
                 .replace('"', '_double_quote_')
                 .replace('<', '_less_than_')
                 .replace('>', '_greater_than_')
                 .replace('|', '_pipe_'))
    return file_name



