

def geoname_taxonomy_recursive_main_function(codes: dict, depth: int) -> dict:
    depth_dict = {}
    for key, items in codes.items():
        for item in items:
            if len(item) > depth + 2:
                if item[:depth+2] not in depth_dict:
                    depth_dict[item[:depth+2]] = []
                depth_dict[item[:depth+2]].append(item)
            else:
                depth_dict[item] = [item]
    return depth_dict

def geoname_taxonomy_recursive(codes, depth: int, start_depth: int=0) -> dict:
    if start_depth != depth-1:
        codes = geoname_taxonomy_recursive_main_function({"data":codes}, start_depth)
        for key, value in codes.items():
            codes[key] = geoname_taxonomy_recursive(value, depth, start_depth + 1)
    return codes
