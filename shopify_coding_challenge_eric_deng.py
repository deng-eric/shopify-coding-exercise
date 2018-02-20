#/usr/bin/python
'''
Eric Deng, January 9th, 2018
This is my coding challenge entry for the Shopify Summer 2018 internship.
'''
import json
import requests


def get_url(page):
    """Return the url of the specified page."""
    return "https://backend-challenge-summer-2018.herokuapp.com" + \
            "/challenges.json?id=1&page="+str(page)

    ''' For the extra challenge, use the line below instead '''
#    return "https://backend-challenge-summer-2018.herokuapp.com" + \
#        "/challenges.json?id=2&page="+str(page)


def aggregate_pages(roots):
    """Return a graph of the menus by aggregating the menus on all the different pages.
    Also updates roots with the root menus."""
    aggregate = {}
    req = requests.get(get_url(0))
    json_data = req.json()

    total_pages = int(json_data['pagination']['total']/json_data['pagination']['per_page']) + 1
    page = json_data['pagination']['current_page']
    while page <= total_pages:
        req = requests.get(get_url(page))
        json_data = req.json()
        menus = json_data['menus']
        for menu in menus:
            aggregate[(menu)['id']] = menu['child_ids']
            if not 'parent_id' in menu:
                roots.append((menu)['id'])
        page += 1
    return aggregate


def dfs_helper(roots, graph):
    """Returns the final result of the program in the form below.
    Performs a depth first search starting from each root menu."""

    result = {"valid_menus":[], "invalid_menus":[]}

    for root in roots:
        path = []
        cycle = dfs(graph, root, path, roots, 1)
        if cycle:
            result["invalid_menus"].append({"root_id":root, "children":path})
        else:
            path.remove(root)
            result["valid_menus"].append({"root_id":root, "children":path})
    return result

def dfs(graph, current, path, roots, depth):
    """Returns true if a cycle is detected and false if not.
    Will continue even if a root menu is found to be invalid
    (too deep or cycle exists) since there may be "more menu"
    to invalidate. Depth parameter used to ensure the max menu
    depth is 4.
    """

    invalid = False
    if current in path:
        return True
    if depth > 4:
        invalid = True

    path.append(current)

    for child in graph[current]:
        invalid = dfs(graph, child, path, roots, depth+1) or invalid
    return invalid

if __name__ == "__main__":

    roots = []
    aggregated_pages = aggregate_pages(roots)
    result = dfs_helper(roots, aggregated_pages)
    print json.dumps(result)
    with open('solution.json', 'w') as f:
        json.dump(result, f)
