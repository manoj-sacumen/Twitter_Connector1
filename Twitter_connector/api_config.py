# API Url
API_URL = 'https://api.twitter.com'
# Response data storing location
STORE_DIR = './Response_data'

Data_on_25th_Recent_tweets = {'search_type': 'Recent_tweets',
                              'method': 'GET',
                              'path': '/2/tweets/search/recent',
                              'query_params': {'query': 'Manoj',
                                               'start_time': '2022-09-25T00:00:00Z',
                                               'end_time': '2022-09-25T01:00:00Z',
                                               'max_results': 10
                                               }}
Data_on_24th_Recent_tweets = {'method': 'GET',
                              'search_type': 'Recent_tweets',
                              'path': '/2/tweets/search/recent',
                              'query_params': {'query': 'India',
                                              'start_time': '2022-09-24T00:00:00Z',
                                              'end_time': '2022-09-24T01:00:00Z',
                                              'max_results': 10
                                              }}
Data_on_25th_By_User_ID= {'method': 'GET',
                          'search_type': 'By_User_ID',
                          'user_id': 54829997,
                          'path': '/2/users',
                          'query_params': {'start_time': '2022-09-25T00:00:00Z',
                                          'end_time': '2022-09-26T00:00:00Z',
                                          'user.fields': 'created_at'}}
Data_on_20th_By_User_ID_error_400= {'method': 'GET',
                                    'search_type': 'By_User_ID',
                                    'user_id': 'dawdwf',
                                    'path': '/2/users',
                                    'query_params': {'start_time': '2022-09-25T00:00:00Z',
                                                    'end_time': '2022-09-26T00:00:00Z',
                                                    'user.fields': 'created_at',
                                                    }}
Data_on_20th_By_User_ID_error_404 = {
        'method': 'GET',
        'search_type': 'By_User_ID',
        'user_id': 123354,
        'path': '/2/userss',
        'query_params': {'start_time': '2022-09-25T00:00:00Z',
                         'end_time': '2022-09-26T00:00:00Z',
                         'user.fields': 'created_at',
                         }}
                         
Data_on_20th_By_User_ID_error_404 = {'method': 'GET',
                                      'search_type': 'By_User_ID',
                                      'user_id': 123354,
                                      'path': '/2/users',
                                      'query_params': {'start_time': '2022-09-25T00:00:00Z',
                                                      'end_time': '2022-09-26T00:00:00Z',
                                                      'user.fields': 'created_at',
                                                      }}
PARAMS = {
    # For Recent tweets Search
    'Data_on_25th_Recent_tweets': Data_on_25th_Recent_tweets,
    'Data_on_24th_Recent_tweets': Data_on_24th_Recent_tweets,
    #  User ID based tweets Search
    'Data_on_25th_By_User_ID': Data_on_25th_By_User_ID,
    # Negative scenario
    'Data_on_20th_By_User_ID_error_400': Data_on_20th_By_User_ID_error_400,
    'Data_on_20th_By_User_ID_error_404': Data_on_20th_By_User_ID_error_404,
    
}
