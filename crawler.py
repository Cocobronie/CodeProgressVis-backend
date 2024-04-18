import hashlib
import json
import time
import uuid

import requests


#修改整个cookies
cookies = {
    'gr_user_id': '85172f2f-a73c-4d71-b44f-5f917d3ceea8',
    '_gid': 'GA1.2.219816785.1713155503',
    '_bl_uid': 'h9lgbv2p1UO00hkzzk0vcqXjzhhj',
    'Hm_lvt_f0faad39bcf8471e3ab3ef70125152c3': '1713155503,1713183871,1713245189,1713250559',
    'messages': 'W1siX19qc29uX21lc3NhZ2UiLDAsMjUsIlx1NjBhOFx1NWRmMlx1N2VjZlx1NzY3Ylx1NTFmYSJdXQ:1rwcju:wDrJ22uTCtFVJvY8uPRdOHxPSYyIqCnWid1J3HJ4ITQ',
    'csrftoken': 'oQ0gvrG9IhIBcri06Z3l5pWoeYcEO9zt3aV9tGgEZChcLeT7ux6KOOBcvRL77HMX',
    'tfstk': 'f5gxg2xRMLvckYxiljtobidg6cOkqqh4exlCSR2cfYH-UvncSKz06Ne-Ql2X0KytBXDlSZ4jIABtnY2jBfR41RMsBRmDqecqgPz6KALH-juH1KhnBoZ1V_Gz_GNsqgv3aPz6KLcTlSXL7vx9MsTtNQFg6sssC51WwWFY5ZZ1lg67U5a_CAwsN7NLGRNbcZG-gde5GSQtzKTbhPX1KNbiy79aCjKRW70YMByKN8pBd4Q_DJGbeN9nfrZ0B8uBE3hrpmM0aALpeyiEeVEQWEBUM0GLP-4BvgUxZxuLl2pAo74z3ki_2ITjwreYXVE5Tg4xfxuT0mCwTbajUDyUc3Jzwq03XJrRFKGow-ZKXxvP5-mKNYEnrTb3RDk-WkaC4b0nJS95KJFGcQdRbGrbZOAs5eHRL6e0wJAvWGSaj7P8KQdRbGrba7eHMKINblVP.',
    'LEETCODE_SESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNDU2OTY0MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNmFlOWRhNDBhNGIzYmVlNDBlZWFlOTc5MmIyNGYyYzBkODA1ZjRkOTIyZDhmYmVjMGJlMTJmM2FlMjY5YTIyMCIsImlkIjo0NTY5NjQzLCJlbWFpbCI6IiIsInVzZXJuYW1lIjoiY29jb2Jyb25pZSIsInVzZXJfc2x1ZyI6ImNvY29icm9uaWUiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jbi9hbGl5dW4tbGMtdXBsb2FkL2RlZmF1bHRfYXZhdGFyLnBuZyIsInBob25lX3ZlcmlmaWVkIjp0cnVlLCJfdGltZXN0YW1wIjoxNzEzMjUwNjMyLjIyMDAwNTgsImV4cGlyZWRfdGltZV8iOjE3MTU3OTk2MDAsInZlcnNpb25fa2V5XyI6MH0.yrZyVzvFmGBci-KFHBnRjkReJrlYKoPg1mvDqKP-PVw',
    'a2873925c34ecbd2_gr_last_sent_sid_with_cs1': '75e4b176-fe9d-47ae-8fe1-87f75dec2e4d',
    'a2873925c34ecbd2_gr_last_sent_cs1': 'cocobronie',
    'a2873925c34ecbd2_gr_session_id': '75e4b176-fe9d-47ae-8fe1-87f75dec2e4d',
    '_gat': '1',
    'a2873925c34ecbd2_gr_session_id_sent_vst': '75e4b176-fe9d-47ae-8fe1-87f75dec2e4d',
    'a2873925c34ecbd2_gr_cs1': 'cocobronie',
    '_ga': 'GA1.1.621652844.1713155503',
    'Hm_lpvt_f0faad39bcf8471e3ab3ef70125152c3': '1713250646',
    '_ga_PDVPZYN3CW': 'GS1.1.1713250561.8.1.1713250676.5.0.0',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://leetcode.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://leetcode.cn/problems/minimize-malware-spread/?envType=daily-question&envId=2024-04-15',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'authorization': '',
    'baggage': 'sentry-environment=production,sentry-release=269d9afe,sentry-transaction=%2Fproblems%2F%5Bslug%5D%2F%5B%5B...tab%5D%5D,sentry-public_key=1595090ae2f831f9e65978be5851f865,sentry-trace_id=994c096e5c914119aee2f24cd468c7e8,sentry-sample_rate=0.03',
    'content-type': 'application/json',
    'random-uuid': '14fb5d84-74fa-bbdd-0a2c-09df81d47d11',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sentry-trace': '994c096e5c914119aee2f24cd468c7e8-aa725a6dd4077ae1-0',
    'uuuserid': '48e6fc0249d0dfeda351fbe4e9a86d2c',
    'x-csrftoken': 'oQ0gvrG9IhIBcri06Z3l5pWoeYcEO9zt3aV9tGgEZChcLeT7ux6KOOBcvRL77HMX',
}


def get_error_codes(submissionId):
    json_data = {
        'query': '\n    query submissionDetails($submissionId: ID!) {\n  submissionDetail(submissionId: $submissionId) {\n    code\n    timestamp\n    statusDisplay\n    isMine\n    runtimeDisplay: runtime\n    memoryDisplay: memory\n    memory: rawMemory\n    lang\n    langVerboseName\n    question {\n      questionId\n      titleSlug\n      hasFrontendPreview\n    }\n    user {\n      realName\n      userAvatar\n      userSlug\n    }\n    runtimePercentile\n    memoryPercentile\n    submissionComment {\n      flagType\n    }\n    passedTestCaseCnt\n    totalTestCaseCnt\n    fullCodeOutput\n    testDescriptions\n    testInfo\n    testBodies\n    stdOutput\n    ... on GeneralSubmissionNode {\n      outputDetail {\n        codeOutput\n        expectedOutput\n        input\n        compileError\n        runtimeError\n        lastTestcase\n      }\n    }\n    ... on ContestSubmissionNode {\n      outputDetail {\n        codeOutput\n        expectedOutput\n        input\n        compileError\n        runtimeError\n        lastTestcase\n      }\n    }\n  }\n}\n    ',
        'variables': {
            'submissionId': submissionId,
        },
        'operationName': 'submissionDetails',
    }
    time.sleep(1)
    response = requests.post('https://leetcode.cn/graphql/', cookies=cookies, headers=headers, json=json_data)

    lang_name = response.json()['data']['submissionDetail']['langVerboseName']
    codes = response.json()['data']['submissionDetail']['code']
    print('成功获取错题：', submissionId)
    return '{}\n{}\n\n'.format(codes, lang_name)


def get_error_id(questionSlug):
    json_data = {
        'query': '\n    query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!, $lang: String, $status: SubmissionStatusEnum) {\n  submissionList(\n    offset: $offset\n    limit: $limit\n    lastKey: $lastKey\n    questionSlug: $questionSlug\n    lang: $lang\n    status: $status\n  ) {\n    lastKey\n    hasNext\n    submissions {\n      id\n      title\n      status\n      statusDisplay\n      lang\n      langName: langVerboseName\n      runtime\n      timestamp\n      url\n      isPending\n      memory\n      submissionComment {\n        comment\n        flagType\n      }\n    }\n  }\n}\n    ',
        'variables': {
            'questionSlug': questionSlug,
            'offset': 0,
            'limit': 20,
            'lastKey': None,
            'status': None,
        },
        'operationName': 'submissionList',
    }
    time.sleep(1)
    response = requests.post('https://leetcode.cn/graphql/', cookies=cookies, headers=headers, json=json_data)
    ids = []
    submissionList = response.json()['data']['submissionList']['submissions']
    for i in submissionList:
        ids.append(i['id'])
    return ids


# 获取错题
def save_error_codes(questionSlug):
    error_id = get_error_id(questionSlug)
    for i in error_id:
        filename = uuid.uuid1()
        with open('submissions_error/{}.txt'.format(filename), 'w', encoding='utf') as f:
            f.write(get_error_codes(i))
        print('成功获取错解文件名：', filename)

def get_data(skip, questionSlug):
    json_data = {
        'query': '\n    query questionTopicsList($questionSlug: String!, $skip: Int, $first: Int, $orderBy: SolutionArticleOrderBy, $userInput: String, $tagSlugs: [String!]) {\n  questionSolutionArticles(\n    questionSlug: $questionSlug\n    skip: $skip\n    first: $first\n    orderBy: $orderBy\n    userInput: $userInput\n    tagSlugs: $tagSlugs\n  ) {\n    totalNum\n    edges {\n      node {\n        ipRegion\n        rewardEnabled\n        canEditReward\n        uuid\n        title\n        slug\n        sunk\n        chargeType\n        status\n        identifier\n        canEdit\n        canSee\n        reactionType\n        hasVideo\n        favoriteCount\n        upvoteCount\n        reactionsV2 {\n          count\n          reactionType\n        }\n        tags {\n          name\n          nameTranslated\n          slug\n          tagType\n        }\n        createdAt\n        thumbnail\n        author {\n          username\n          profile {\n            userAvatar\n            userSlug\n            realName\n            reputation\n          }\n        }\n        summary\n        topic {\n          id\n          commentCount\n          viewCount\n          pinned\n        }\n        byLeetcode\n        isMyFavorite\n        isMostPopular\n        isEditorsPick\n        hitCount\n        videosInfo {\n          videoId\n          coverUrl\n          duration\n        }\n      }\n    }\n  }\n}\n    ',
        'variables': {
            'questionSlug': questionSlug,
            'skip': skip,
            'first': 500,
            'orderBy': 'DEFAULT',
            'userInput': '',
            'tagSlugs': [],
        },
        'operationName': 'questionTopicsList',
    }
    time.sleep(1)
    response = requests.post('https://leetcode.cn/graphql/', cookies=cookies, headers=headers, json=json_data)
    data = response.json()['data']['questionSolutionArticles']
    totalNum = data['totalNum']
    # print(totalNum)
    # print(len(data['edges']))
    slugs = []
    for edge in data['edges']:
        slugs.append(edge['node']['slug'])
    print('成功：', skip)
    return [totalNum, slugs]


# 获取正解参数
def slugs(questionSlug):
    skip = 1
    totalNum = 10
    slugs = []
    while skip <= totalNum and skip <= 50:   #修改这个能控制爬取数量
        data = get_data(skip, questionSlug)
        totalNum = data[0]
        slugs = slugs + data[1]
        skip = skip + 50
    with open('slugs.json', 'w', encoding='utf') as f:
        f.write(json.dumps(slugs))


def format_data(data):
    data = data.split('**代码**')
    text = ''
    for i in data:
        contents = i.split('```')
        if len(contents) > 1:
            contents.pop(0)
            contents.pop(-1)
            for i in contents:
                text = '{}{}\n'.format(text, i)
    return text


def get_text(slug):  # 获取正解数据并保存
    time.sleep(2)
    json_data = {
        'query': '\n    query discussTopic($slug: String) {\n  solutionArticle(slug: $slug, orderBy: DEFAULT) {\n    ...solutionArticle\n    content\n    next {\n      slug\n      title\n    }\n    prev {\n      slug\n      title\n    }\n  }\n}\n    \n    fragment solutionArticle on SolutionArticleNode {\n  ipRegion\n  rewardEnabled\n  canEditReward\n  uuid\n  title\n  content\n  slateValue\n  slug\n  sunk\n  chargeType\n  status\n  identifier\n  canEdit\n  canSee\n  reactionType\n  reactionsV2 {\n    count\n    reactionType\n  }\n  tags {\n    name\n    nameTranslated\n    slug\n    tagType\n  }\n  createdAt\n  thumbnail\n  author {\n    username\n    isDiscussAdmin\n    isDiscussStaff\n    profile {\n      userAvatar\n      userSlug\n      realName\n      reputation\n    }\n  }\n  summary\n  topic {\n    id\n    subscribed\n    commentCount\n    viewCount\n    post {\n      id\n      status\n      voteStatus\n      isOwnPost\n    }\n  }\n  byLeetcode\n  isMyFavorite\n  isMostPopular\n  favoriteCount\n  isEditorsPick\n  hitCount\n  videosInfo {\n    videoId\n    coverUrl\n    duration\n  }\n  question {\n    titleSlug\n    questionFrontendId\n  }\n}\n    ',
        'variables': {
            'slug': slug,
        },
        'operationName': 'discussTopic',
    }
    response = requests.post('https://leetcode.cn/graphql/', cookies=cookies, headers=headers, json=json_data)
    data = response.json()['data']['solutionArticle']['content']
    data = format_data(data)
    filename = uuid.uuid1()
    with open('submissions_correct/{}.txt'.format(filename), 'w', encoding='utf') as f:
        f.write(data)
    print('成功获取正解slug：', slug)
    print('文件名：', filename)


# 获取正确题解
def get_right_answer(questionSlug):
    slugs(questionSlug)
    with open('slugs.json', 'r', encoding='utf') as f:
        data = json.loads(f.read())
    for i in data:
        get_text(i)

# if __name__ == '__main__':
def crawler(questionSlug):
    save_error_codes(questionSlug)
    get_right_answer(questionSlug)
