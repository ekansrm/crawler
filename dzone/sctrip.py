import json

if __name__ == '__main__':

    with open('detail.json', 'r') as fp:
        details = json.load(fp)
        details = sorted(details, key=lambda i: int(i['number'].split('#')[1]))
        urls = list([i['number']+','+i['url'] for i in details])

    for item in details:
        item['number'] = int(item['number'].split('#')[1])


    with open('refcard_detail.json', 'w') as fp:
        json.dump(details, fp, indent=2)

    with open('refcard_url.txt', 'w') as fp:
        fp.writelines('\n'.join(urls))


