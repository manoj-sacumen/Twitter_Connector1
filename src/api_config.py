"""api_config module acts as placeholder of input data required to make requests for Twitter API."""
# API Url
API_URL = 'api.twitter.com'  # https://
# Response data storing location
STORE_DIR = './Response_data'

QUERY_TEMPLATE = {
    "recent_tweets_query": {
        "search_type": "Recent_tweets",
        "method": "GET",
        "path": "/2/tweets/search/recent",
        "query_params": {
            "query": "",
        }
    },
    "tweets_by_user_id": {
        "method": "GET",
        "search_type": "By_User_ID",
        "user_id": 0,
        "path": "/2/users",
        "query_params": {
            "user.fields": "created_at"
        }
    }
}
