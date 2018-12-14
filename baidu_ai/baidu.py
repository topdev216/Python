#!/usr/bin/env python
#coding: utf-8


import os
import sys
import json
import requests


def json_string(string):
    return json.dumps(string, ensure_ascii=False)

def json_object(obj):
    return json.loads(obj)


if __name__ == '__main__':
    file_token = 'token.json'
    app_id = ''
    api_key = ''
    api_secret = ''

    try:
        if not os.path.exists(file_token):
            print('>>> get access token')
            response = requests.get(
                url='https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
                    api_key, api_secret
                ),
            ).json()
            print(json_string(response))

            print('>>> dump token to file')
            with open(file_token, 'w') as f:
                f.write(json_string(response))

        print('>>> load token file')
        params = json_object(open(file_token, 'r').read())

        if len(sys.argv) == 2:
            print('>>> get result')
            try:
                response = requests.post(
                    url='https://aip.baidubce.com/rpc/2.0/search/info?access_token=%s' % params.get('access_token', ''),
                    data=({
                        'category': 'OFFLINE_ASR_RESULT',
                        'paras': {
                            'appId': app_id,
                            'callId': 'reserch-tom-s%s' % sys.argv[1],
                        }
                    }),
                    headers={
                        'Content-Type': 'application/json',
                    }
                )
            except Exception as e:
                print(e)
            exit(0)

        print('>>> uploading wav file')
        response = requests.post(
            url='https://aip.baidubce.com/rpc/2.0/session/offline/upload/asr?access_token=%s' % (params.get('access_token', '')),
            data=json_string({
                'appId': app_id,
                'callId': 'reserch-tom-s13',
                'companyName': 'afanti',
                'agentFileUrl': 'https://x.x.x.x/3.wav',
                'clientFileUrl': '',
                'callbackUrl': 'http://x.x.x.x:11019/baidu',
                'suffix': 'wav',
            }),
            headers={
                'Content-Type': 'application/json',
            },
        ).json()
        print(response)
    except Exception as e:
        print(e)

