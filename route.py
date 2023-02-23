from pyroutelib3 import Router


mode_map = {
    'Voiture': 'car',
    'Vélo': 'cycle',
    'Pédestre': 'foot',
    'Cheval': 'horse'
}

def get_route(start, end, mode):
    router = Router(mode_map[mode])
    node_start = router.findNode(*start)
    node_end = router.findNode(*end)
    status, route = router.doRoute(node_start, node_end)
    if status == 'success':
        return list(map(router.nodeLatLon, route))
    return []