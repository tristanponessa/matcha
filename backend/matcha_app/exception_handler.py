import traceback
import sys

def get_exception(extra_info='', verbose=True):
    
    exc_type, exc_value, exc_traceback = sys.exc_info()
    
    filename = exc_traceback.tb_frame.f_code.co_filename
    lineno   = exc_traceback.tb_lineno
    name     = exc_traceback.tb_frame.f_code.co_name
    type_     = exc_type.__name__
    message  = str(exc_value) # or see traceback._some_str()

    #
    trace_back = traceback.extract_tb(exc_traceback)
    # Format stacktrace
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(trace)
    st = '\n'.join(str(x) for x in stack_trace)
    #

    deco_top = 'MATCHA ERROR'.center(50, '#')
    deco_bottom = ''.center(50, '#')
    if verbose:
        err_msg = f">exception<:\n\t{type_}\n>personal info<:\n\t{extra_info}\n>msg<:\n\t{message}\n>traceback_stack<:\n\t{st}"
        output = f'\n{deco_top}\n{err_msg}\n{deco_bottom}\n'
    else:
        cut_msg = message[0:200]
        cut_msg = cut_msg.replace('\n', '').replace('\r', '') #uses \r while windows \r
        output = f'exception: {type_} -> {filename} {lineno} {extra_info} : {cut_msg} ...'
    return output