def get_level1_based_on_level2(level):
    return level[:7].replace("2", "1@") + ''.join(level[8:].split('@')[0])

def get_level1_based_on_level3(level):
    return level[:7].replace("3", "1@") + ''.join(level[8:].split('@')[0].split("-")[0])

def get_level2_based_on_level3(level):
    return level[:7].replace("3", "2-") + '@'.join(level[8:].split('@')[0].split("-"))

def make_levels_cleaner_fb(df):
    level1_ref, level2_ref, level3_ref = [], [], []
    for level1, level2, level3 in zip(df['level-1'], df['level-2'], df['level-3']):
        if len(level1) == 0:
            if len(level2) != 0:
                level1_based_on_level2 = []
                for level in level2:
                    level1_based_on_level2.append(get_level1_based_on_level2(level))
                level1_temp = list(set(level1_based_on_level2))
            elif len(level3) != 0:
                level1_based_on_level3 = []
                for level in level3:
                    level1_based_on_level3.append(get_level1_based_on_level3(level))
                level1_temp = list(set(level1_based_on_level2))
        else:
            level1_temp = list(set(level1))

        if len(level2) == 0 and len(level3) != 0:
            level2_based_on_level3 = []
            for level in level3:
                level2_based_on_level3.append(get_level2_based_on_level3(level))
            level2_temp = list(set(level2_based_on_level3))

        else:
            level2_temp = list(set(level2))
        level3_temp = list(set(level3))

        #‌ LEVEL 1 11111111111111111111111111111111111111111111
        if len(level1_temp) == 1:
            level1_ref.append(level1_temp[0])    
        elif len(level1_temp) == 0:
            level1_ref.append(None)
        else:
            if level2_temp == ['Level-2-event@social_event', 'Level-2-event@show']:
                level1_ref.append("Level-1@event")
            elif level2_temp == ['Level-2-event@social_event']:
                level1_ref.append("Level-1@event")

        #‌ LEVEL 2 22222222222222222222222222222222222222222222
        if len(level2_temp) == 1:
            level2_ref.append(level2_temp[0])
        elif len(level2_temp) == 0:
            level2_ref.append(None)
        else:
            level2_based_on_level3_2nd = []
            for level in level3_temp:
                level2_based_on_level3_2nd.append(get_level2_based_on_level3(level))

            level2_based_on_level3_2nd = list(set(level2_based_on_level3_2nd))
            intersection_lst = list(set(level2_based_on_level3_2nd).intersection(set(level2_temp)))

            if len(intersection_lst) == 1:
                level2_temp = intersection_lst.copy()
                new_level3_temp = []
                for level in level3_temp:
                    if get_level2_based_on_level3(level) in intersection_lst:
                        new_level3_temp.append(level)

                level3_temp = list(set(new_level3_temp)).copy()
                level2_ref.append(level2_temp[0])

            else:
                if len(intersection_lst) == 0:
                    level3_temp = []
                    level2_ref.append(level2_temp[0])
                else:
                    level2_temp = intersection_lst[:1].copy()
                    new_level3_temp = []
                    for level in level3_temp:
                        if get_level2_based_on_level3(level) in level2_temp:
                            new_level3_temp.append(level)
                    level2_ref.append(level2_temp[0])
                    level3_temp = new_level3_temp.copy()

                    # for l in new_level3_temp:
                    #     if "Level-3" in l:
                    #         print(l)
        #‌ LEVEL 3 3333333333333333333333333333333333333333333333333333
        if len(level3_temp) == 1:
            level3_ref.append(level3_temp[0])
        elif len(level3_temp) == 0:
            level3_ref.append(None)
        else:
            # for l in level3_temp:
            #     level3_temp_fq_dict[l] += 1
            level3_ref.append(level3_temp[0])
            # print("level3_temp:", level3_temp)
            # print("-"*70)
            # level3_ref.append(level3_temp)
    df['level-1-cleaned'] = level1_ref
    df['level-2-cleaned'] = level2_ref
    df['level-3-cleaned'] = level3_ref
    return df
