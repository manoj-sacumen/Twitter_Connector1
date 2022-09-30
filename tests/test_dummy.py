import requests_mock
import requests

def fun2():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='resp')
        return requests.get('http://test.com')
print(fun2())