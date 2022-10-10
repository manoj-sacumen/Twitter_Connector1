"""api_config module acts as placeholder of input data required to make requests for Twitter API."""
# API Url
API_URL = 'https://api.twitter.com'
# Response data storing location
STORE_DIR = './Response_data'

QUERY_TEMPLATE = {
    "recent_tweets_query": {
        "search_type": "Recent_tweets",
        "method": "GET",
        "path": "/2/tweets/search/recent",
        "query_params": {
            "query": "",
            "start_time": "",
            "end_time": "",
            "max_results": 0
        }
    },
    "tweets_by_user_id": {
        "method": "GET",
        "search_type": "By_User_ID",
        "user_id": 0,
        "path": "/2/users",
        "query_params": {
            "start_time": "",
            "end_time": "",
            "max_results": "",
            "user.fields": "created_at"
        }
    }
}
