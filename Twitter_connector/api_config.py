# API Url
API_URL = 'https://api.twitter.com'


PARAMS = {
          # For Recent tweets Search
          'Data_on_25th_Recent_tweets': {
              'search_type':'Recent_tweets',
              'method': 'GET',
              'path': '/2/tweets/search/recent',
              'query_params': {'query': 'India',
                               'start_time': '2022-09-25T00:00:00Z',
                               'end_time': '2022-09-26T00:00:00Z'
                               }
              },
          'Data_on_24th_Recent_tweets': {
              'method': 'GET',
              'search_type':'Recent_tweets',
              'path': '/2/tweets/search/recent',
              'query_params': {'query': 'India',
                               'start_time': '2022-09-24T00:00:00Z',
                               'end_time': '2022-09-25T00:00:00Z'
                               }
              },
              
            #  User ID based tweets Search
           'Data_on_25th_By_User_ID' : {
              'method': 'GET',
              'search_type':'By_User_ID',
              'user_id':12365,    
              'path': '/2/users',
              'query_params': {'start_time': '2022-09-25T00:00:00Z',
                               'end_time': '2022-09-26T00:00:00Z',
                               'user.fields': 'created_at'}

           }
          }


# "https://api.twitter.com/2/users/54829997/tweets?max_results=5&start_time=2022-08-29T00:00:00Z&end_time=2022-08-30T00:00:00Z&user.fields=created_at"

# Response data storing location
STORE_DIR ='./Response_data'

