#!/bin/bash

app_id=$(cat app_id)
app_token=$(cat app_token)

curl -X GET 'https://cloud.estimote.com/v2/devices' -u $app_id:$app_token -H "Accept: application/json"

