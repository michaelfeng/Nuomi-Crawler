#!/bin/bash

while IFS='' read -r city || [[ -n "$line" ]]; do
    wget -O "./data/$city.html" "http://api.nuomi.com/api/dailydeal?version=v1&city=$city" &
done < pinyin.txt

#awk '{ getline b < "GB2260.txt"; print $0, b}' pureCity.txt

