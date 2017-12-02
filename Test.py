import json
with open('D:\\json\\articles.json') as f:
    ref = json.load(f)
    # c = 1
    # for i in ref:
    #     print(i)
    #     for j in ref[i]:
    #         print(j)
    #         for k in ref[i][j]:
    #             print('\t', k)
    #             for l in ref[i][j][k]:
    #                 print('\t\t', l)
    #                 if c == 35:
    #                     break
    #                 c += 1
    print(ref['articles']['table']['columns'])
    print(ref['articles']['table']['rows'][0])
    # for i,k in ref['articles']['table']['rows'][4094].items():
    #     print('Col %s | Value "%s"' % (i, k))