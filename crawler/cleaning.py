import pandas as pd

if __name__ == '__main__':
    douban_data = pd.read_csv('data/raw/豆瓣.csv')
    maoyan_data = pd.read_csv('data/raw/猫眼每日票房.csv')
    endata_data = pd.read_csv('data/raw/艺恩年度票房.csv')

    data = {}
    daily_data = []
    director_data = {}
    actor_data = {}
    type_data = {}
    daily_data_dict = {}

    for i, view in douban_data.iterrows():
        tmp_list = [None for _ in range(13)]
        tmp_list[0] = i
        tmp_list[12] = 0

        if str(view['导演']) == 'nan':
            tmp_list[1] = None
        else:
            tmp_list[1] = [x.strip().split()[0] for x in view['导演'].split('/')]
            if tmp_list[1][-1].startswith('更多'):
                tmp_list[1].pop()

        if str(view['主演']) == 'nan':
            tmp_list[2] = None
        else:
            tmp_list[2] = [x.strip() for x in view['主演'].split('/')]
            if tmp_list[2][-1].startswith('更多'):
                tmp_list[2].pop()

        if str(view['类型']) == 'nan':
            tmp_list[3] = None
        else:
            tmp_list[3] = [x.strip() for x in view['类型'].split('/')]

        if str(view['综合评分']) == 'nan':
            tmp_list[4] = None
        else:
            tmp_list[4] = view['综合评分']

        tmp_list[5] = view['剧情简介']

        data[view['影片']] = tmp_list

    for _, view in endata_data.iterrows():
        if view['影片'] not in data:
            continue

        data[view['影片']][6] = float(view['总票房（万）'].replace(',', '')) * 10000
        data[view['影片']][7] = view['平均票价']
        data[view['影片']][8] = view['国家及地区'].split('\n')[0].strip().split('/')[0].strip()
        data[view['影片']][9] = view['上映日期']

    for _, view in maoyan_data.iterrows():
        if view['影片'] not in data:
            continue

        if str(view['总票房']) != 'nan':
            if view['总票房'].endswith('亿'):
                data[view['影片']][6] = float(view['总票房'][:-1]) * 100000000
            elif view['总票房'].endswith('万'):
                data[view['影片']][6] = float(view['总票房'][:-1]) * 10000
            else:
                data[view['影片']][6] = float(view['总票房'])

        if data[view['影片']][10] is None:
            data[view['影片']][10] = int(view['排片场次'])
        else:
            data[view['影片']][10] += int(view['排片场次'])

        attendance_rate = view['上座率'].strip()
        if attendance_rate.endswith('%'):
            if data[view['影片']][11] is None:
                data[view['影片']][11] = float(attendance_rate[:-1])
            else:
                data[view['影片']][11] += float(attendance_rate[:-1])
            data[view['影片']][12] += 1

        if view['日期'] not in daily_data_dict:
            daily_data_dict[view['日期']] = set()
        if view['影片'] in daily_data_dict[view['日期']]:
            continue
        daily_data_dict[view['日期']].add(view['影片'])

        tmp_list = [None for _ in range(4)]
        tmp_list[0] = view['日期']
        tmp_list[1] = data[view['影片']][0]
        tmp_list[2] = float(view['当日综合票房'][:-1])
        if view['场均人次'].startswith('<') or view['场均人次'].startswith('--'):
            tmp_list[3] = 0
        else:
            tmp_list[3] = int(int(view['排片场次']) * float(view['场均人次']))

        daily_data.append(tmp_list)

    director_id = 0
    for val in data.values():
        if val[1] is not None:
            for director in val[1]:
                if director not in director_data:
                    director_data[director] = [director_id, []]
                    director_id += 1
                director_data[director][1].append(val[0])

    actor_id = 0
    for val in data.values():
        if val[2] is not None:
            for actor in val[2]:
                if actor not in actor_data:
                    actor_data[actor] = [actor_id, []]
                    actor_id += 1
                actor_data[actor][1].append(val[0])

    type_id = 0
    for val in data.values():
        if val[3] is not None:
            for t in val[3]:
                if t not in type_data:
                    type_data[t] = [type_id, []]
                    type_id += 1
                type_data[t][1].append(val[0])

    actor_df = []
    actor_movie_df = []
    director_df = []
    director_movie_df = []
    type_df = []
    type_movie_df = []
    movie_df = []

    for name, val in actor_data.items():
        actor_df.append([val[0], name])
        for movie_id in val[1]:
            actor_movie_df.append([movie_id, val[0]])

    for name, val in director_data.items():
        director_df.append([val[0], name])
        for movie_id in val[1]:
            director_movie_df.append([movie_id, val[0]])

    for name, val in type_data.items():
        type_df.append([val[0], name])
        for movie_id in val[1]:
            type_movie_df.append([movie_id, val[0]])

    for name, val in data.items():
        tmp_list = [None for _ in range(10)]
        tmp_list[0] = val[0]
        tmp_list[1] = name
        tmp_list[2] = val[9]
        tmp_list[3] = val[6]
        tmp_list[4] = val[7]
        tmp_list[5] = val[10]
        if val[12] > 0:
            tmp_list[6] = val[11] / val[12]
        tmp_list[7] = val[8]
        tmp_list[8] = val[4]
        tmp_list[9] = val[5]
        movie_df.append(tmp_list)

    pd.DataFrame(movie_df, columns=[
        'movie_id',
        'title',
        'release_date',
        'total_box_office',
        'avg_ticket_price',
        'screening_count',
        'attendance_rate',
        'country',
        'overall_rating',
        'description'
    ]).to_csv('data/cleaned/movies.csv', index=False)

    pd.DataFrame(daily_data, columns=[
        'date_time',
        'movie_id',
        'box_office',
        'attendees'
    ]).to_csv('data/cleaned/daily_box_office.csv', index=False)

    pd.DataFrame(type_df, columns=['genre_id', 'name']).to_csv('data/cleaned/categories.csv', index=False)
    pd.DataFrame(actor_df, columns=['actor_id', 'name']).to_csv('data/cleaned/actors.csv', index=False)
    pd.DataFrame(director_df, columns=['director_id', 'name']).to_csv('data/cleaned/directors.csv', index=False)
    pd.DataFrame(actor_movie_df, columns=['movie_id', 'actor_id']).to_csv('data/cleaned/movie_actors.csv', index=False)
    pd.DataFrame(type_movie_df, columns=['movie_id', 'genre_id']).to_csv('data/cleaned/movie_categories.csv', index=False)
    pd.DataFrame(director_movie_df, columns=['movie_id', 'director_id']).to_csv('data/cleaned/movie_directors.csv', index=False)
