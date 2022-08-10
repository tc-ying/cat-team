""" Retrieve estate maps from HKHA GIS """
# pylint: disable=C0103, C0301

import sys
import requests as req
import login

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

    url = 'https://emdgis.int.housingauthority.gov.hk/DCDGIS/getEstatePlan'

    for estate in argv:
        params = {'name': estate.strip(' ') + '.pdf'}
        response = session.get(url, params=params)
        print("Request Status: ", response.status_code)
        print("File Content: ", response.headers['content-length'])

        with open('./' + estate.strip(' ') + '.pdf', 'wb') as f:
            f.write(response.content)

if __name__ == '__main__':
    main(sys.argv[1:])
