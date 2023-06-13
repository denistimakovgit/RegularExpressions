import datetime

def logger(old_function):

    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        function_date_time = str(datetime.datetime.now())
        function_name = old_function.__name__
        with open('main.log', 'a', encoding='utf-8') as f:
            f.write(f'{function_date_time}\n')
            f.write(f'{function_name}\n')
            f.write(f'args {args}, kwargs {kwargs}\n')
            f.write(f'{result}\n')
        return result
    return new_function