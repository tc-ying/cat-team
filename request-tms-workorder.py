""" Login FLBWMASS, sniff desktop Chrome's cookie, and request TIMS Order JSONs """
# pylint: disable=C0103, C0301

import login
import sys
import time
import requests as req
import browser_cookie3
import pandas as pd

def main(argv):
    """ Main """
    session = req.session()
    adapter = req.adapters.HTTPAdapter(max_retries=5)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})

    url = 'https://ehousing.housing.gov.hk/pkmslogin.form'
    form = {'login-form-type': 'pwd', 'username': login.username, 'password': login.password}
    session.post(url, data=form, verify=False)

    cj = browser_cookie3.chrome(cookie_file='C:\\Users\\TCYing\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies')

    cstr = 'PD-ID-HAC-PRD=' + str(cj._cookies['.int.housingauthority.gov.hk']['/']['PD-ID-HAC-PRD'].value) + '; ' + 'PD-S-SESSION-ID-HAC-PRD=' + str(cj._cookies['.int.housingauthority.gov.hk']['/']['PD-S-SESSION-ID-HAC-PRD'].value) + '; ' + 'JSESSIONID=' + str(cj._cookies['tomctms.int.housingauthority.gov.hk']['/ctms']['JSESSIONID'].value) + '; ' + '57b994ed1097bdfbea2c0ef08719557c=' + str(cj._cookies['tomctms.int.housingauthority.gov.hk']['/']['57b994ed1097bdfbea2c0ef08719557c'].value) + '; ' + 'PD_STATEFUL_28834284-2002-11ec-921c-005056a03795=' + str(cj._cookies['tomctms.int.housingauthority.gov.hk']['/']['PD_STATEFUL_28834284-2002-11ec-921c-005056a03795'].value) + '; ' + 'tms_current_post=' + str(cj._cookies['.int.housingauthority.gov.hk']['/']['tms_current_post'].value) + '; ' + 'tms_last_login_ts=' + str(cj._cookies['.int.housingauthority.gov.hk']['/']['tms_last_login_ts'].value)

    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36", "Cookie": cstr})

    url = 'https://tomctms.int.housingauthority.gov.hk/ctms/workorder.rpc'
    params = {'ctmsAction': 'getList'}
    df = pd.read_excel('//bvba16841/CAT DataMart/FLBWMASS/Estate List.xlsm', converters={'id': str})
    # mntSchmCode: T represents TMS orders
    for estate in argv:
        e = estate.strip(' ').upper()
        if df.loc[df['id'] == e, 'id'].empty:
            if df.loc[df['flCode'] == e, 'id'].empty:
                print("Estate is not found")
                continue
            else:
                print("Estate: ", df.loc[df['flCode'] == e, 'hseEstEngName'].values[0])
                hseEstKey = df.loc[df['flCode'] == e, 'id'].values[0]
                flCode = e
        else:
            print("Estate: ", df.loc[df['id'] == e, 'hseEstEngName'].values[0])
            hseEstKey = e
            flCode = df.loc[df['id'] == e, 'flCode'].values[0]

        form = {'pageProgramTypeCode': 'W', 'woCreDateFrom': '01072020', 'woCreDateTo': '30062023', 'hseEstKey': hseEstKey, 'woTypeCode': 'C', 'mntSchmCode': 'T', 'max': '7000', 'page': '1', 'sort': '', 'order': 'asc'}
        response = session.post(url, params=params, data=form, verify=False, timeout=480)
        print("Request Status: ", response.status_code)

        with open('./__EWO Handling (TMSS)/' + flCode + '_tms.json', 'wb') as f:
            f.write(response.content)

        time.sleep(3)

if __name__ == '__main__':
    main(sys.argv[1:])
