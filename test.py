from TikTokApi import TikTokApi
verifyFp = 'verify_ldtnq60a_B5wJYePu_Gy0c_4xG0_8s7y_76qzuVExbii3'
api = TikTokApi(custom_verifyFp=verifyFp)
results = 10
hashtag = 'Messi'
search_results = api.by_hashtag(count=results, hashtag=hashtag)
for tiktok in search_results:
    print(tiktok['video']['playAddr'])
