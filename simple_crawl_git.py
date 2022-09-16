from github import Github
import time

access_token = "your_access_token"
query_keyword = "your_query_keyword"
g = Github(login_or_token=access_token)
# 每小时5000，每分钟30
limit = g.get_rate_limit()
print("当前token速率配置: {}, {}".format(limit.core.remaining, limit.search.remaining) )
search_res = g.search_code(query=query_keyword, highlight=True)
# 计数器
count = 0
total = search_res.totalCount
with open("search-github-result", "w") as ff:
    for res_item in search_res:
        highlight = ""
        for match_item in res_item.text_matches:
            highlight += match_item["fragment"]
        result = {
            "path": res_item.path,
            "repos": res_item.repository.full_name,
            "highlight": highlight,
            "html_url": res_item.html_url
        }
        print("==============\nrepos:{}\npath:{}\nhtml_url:{}\nmatch:{}\n==============\n".format(
            result["repos"], result["path"], result["html_url"], result["highlight"]
        ), file=ff)
        # 记录条数
        count += 1
        print("count:{} total:{}".format(count, total))
        # 避免命中second rate limit
        time.sleep(2)
