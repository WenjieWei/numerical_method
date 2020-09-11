def countCandies(friends_nodes, friends_from, friends_to, friends_weight):
    dict = {}
    for i in range(0, len(friends_weight)):
        if friends_weight[i] in dict:
            groups = dict[friends_weight[i]]
            found = False
            for group in groups:
                if friends_from[i] in group and friends_to[i] not in group:
                    group.append(friends_to[i])
                    found = True
                    break
                elif friends_to[i] in group and friends_from[i] not in group:
                    group.append(friends_from[i])
                    found = True
                    break
                elif friends_to[i] in group and friends_from[i] in group:
                    found = True
                    break
            if not found:
                groups.append([friends_to[i], friends_from[i]])

        else:
            dict[friends_weight[i]] = [[friends_from[i], friends_to[i]]]
    max_size = 0
    max_product = 0
    for groups in dict.values():
        for group in groups:
            if len(group) >= max_size:
                num1 = max(group)
                new_group = []
                for x in group:
                    if x != num1:
                        new_group.append(x)
                num2 = max(new_group)
                product = num1 * num2
                if product > max_product:
                    max_product = product
    return max_product

if __name__ == "__main__":
    friends_nodes = []
    friends_from = [1, 2, 4, 5]
    friends_to = [2, 3, 2, 4]
    friends_weight = [20, 30, 20, 30]
    countCandies(friends_nodes, friends_from, friends_to, friends_weight)