def write_log(txt):
    with open('./log.txt', 'w+') as log:
        log.writelines(txt)