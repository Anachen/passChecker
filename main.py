import requests, hashlib
from tkinter import filedialog,Tk

def req_api_data(query_ch):
    url = 'https://api.pwnedpasswords.com/range/' + query_ch
    res = requests.get(url)
    if res.status_code !=200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res

def get_pass_leaks_count(hashes,hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:

       if h == hash_to_check:
           return count
    return 0


def check_pass(passw):
    shaPass = hashlib.sha1(passw.encode('utf-8')).hexdigest().upper()
    first_five,tail =shaPass[:5],shaPass[5:]
    response = req_api_data(first_five)
    return get_pass_leaks_count(response,tail)

def begin_check_passes(args):
    for pasw in args:
        count = check_pass(pasw)
        if count:
            print(f'{pasw} was found {count} many times. Change it!')
        else:
            print(f'{pasw} was not found. Seems good.')
    return 'Finished'

def start_pass_checker():
    Tk().withdraw()
    o_file = filedialog.askopenfilename()

    with open(o_file, 'r') as passes:
        begin_check_passes(passes.read().splitlines())



if __name__ == '__main__':
    start_pass_checker()
