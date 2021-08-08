import os
import sys
sys.path.append(os.getcwd())
import json
import requests
import re
from tqdm import tqdm
from app.dzone import load_cookies

# a = 'TH_CSRF=4115038411942097746; dzuuid=5103e900-d5aa-4060-96b2-d69b3f3a2266; AWSELB=2B23F73512874A984846CB61011FAE4304C7C410AC6D2BD8DA2DA380073EAD554E22B9735186545710CBA36F8982913695204F268C6CA1DCA47DC66D55D9FAB03E146CDB7B; _ga=GA1.2.715853686.1544665210; _gid=GA1.2.2111547796.1544665210; optimizelyEndUserId=oeu1544665212098r0.9122913545133489; optimizelySegments=%7B%221595101009%22%3A%22direct%22%2C%221596781023%22%3A%22gc%22%2C%221600230999%22%3A%22false%22%7D; optimizelyBuckets=%7B%7D; SESSION_STARTED=true; _omappvp=eTyze4cKKTPadDXSic2iCIMdpb7E7rQBiS2VnpRl1P1vRWk1QRK1HXoDlndJQsDl5jpMOXBqUM7nghHoIJ1bK3CSR1bKid6z; RETURNING_VISITOR=true; __gads=ID=a72cc00d099e0487:T=1544665275:S=ALNI_MZfbL__bycg_pFSK0s5FyjYm-USvA; JSESSIONID=D12111FEF1D7EDA6BD1A1F1A92D042F2; SPRING_SECURITY_REMEMBER_ME_COOKIE=cExtUjJCbUh3emJ4c09OU1NDMlNJQT09OllFU05BNU9IUDlzanVXM2MveFhNSEE9PQ; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://dzone.com/refcardz%22%2C%22sref%22:%22%22%2C%22sts%22:1544707053560%2C%22slts%22:1544665213985}; _parsely_visitor={%22id%22:%2238a8767e-9dfe-435b-a78a-75b04e7e3042%22%2C%22session_count%22:2%2C%22last_session_ts%22:1544707053560}; mp_022d397c8f6bfc6c6b289f607d96fc84_mixpanel=%7B%22distinct_id%22%3A%20%22167a538a62638d-0281de98afa83b-3f674706-1fa400-167a538a628d16%22%2C%22%24device_id%22%3A%20%22167a538a62638d-0281de98afa83b-3f674706-1fa400-167a538a628d16%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; __insp_wid=1999343779; __insp_slim=1544707316132; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly9kem9uZS5jb20vcmVmY2FyZHo%3D; __insp_targlpt=RFpvbmU6IFByb2dyYW1taW5nICYgRGV2T3BzIG5ld3MsIHR1dG9yaWFscyAmIHRvb2xz; __insp_norec_sess=true; omSeen-ptk1txj64xvw4x4u9hug=1544707327430'
# b = a.split(';')
# cookies = {}
# for bs in b:
#     bbs = bs.split('=')
#     key = bbs[0].strip()
#     val = bbs[1].strip()
#     cookies[key] = val


if __name__ == '__main__':

    cookies = load_cookies('cookies.txt')[0]

    with open('refcard_detail.json', 'r') as fp:
        details = json.load(fp)

    rstr = r"[\s\/\\\:\*\?\"\<\>\|]+"
    base_dir = os.path.join(os.getcwd(), 'refcard')
    for item in tqdm(details):
        try:
            filename = 'refcardz#' + '%03d' % item['number'] + '-' + re.sub(rstr, ' ', item['title']) + '.pdf'
            with open(os.path.join(base_dir, filename), 'wb') as fp:
                r = requests.get('https://dzone.com' + item['download'], cookies=cookies)
                fp.write(r.content)
        except Exception as e:
            print(e)

        # cnt += 1
        # if cnt == 3:
        #     break


