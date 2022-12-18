import geopandas as gpd
import numpy as np
from shapely.geometry import Point

## Sõpruse pst - Tammsaare tee
# Suund Õismäe: https://ristmikud.tallinn.ee/last/cam071.jpg
# Suund Kesklinn: https://ristmikud.tallinn.ee/last/cam072.jpg

## Viru väljaku ülekäigurada
# https://ristmikud.tallinn.ee/last/cam104.jpg

## Narva mnt - Pirita tee
# Suund Pirita: https://ristmikud.tallinn.ee/last/cam186.jpg
# Suund Kesklinn: https://ristmikud.tallinn.ee/last/cam185.jpg

## Merivälja tee - Kloostrimetsa tee
# Suund Kesklinn: https://ristmikud.tallinn.ee/last/cam196.jpg
# Suund Merivälja: https://ristmikud.tallinn.ee/last/cam197.jpg

gpd.options.use_pygeos = True

intersections = \
    [
        {
            "id": "intersection1",
            "name": "Sõpruse pst - Tammsaare tee",
            "coordinate": Point([24.700878, 59.405071]),
            "max_bus_distance": 100,
            "feeds": [
                "cam071",
                "cam072",
            ]
        },
        {
            "id": "intersection2",
            "name": "Viru väljaku ülekäigurada",
            "coordinate": Point([24.752478, 59.4365]),
            "max_bus_distance": 70,
            "feeds": [
                "cam104",
            ]
        },
        {
            "id": "intersection3",
            "name": "Narva mnt - Pirita tee",
            "coordinate": Point([24.795486, 59.443196]),
            "max_bus_distance": 120,
            "feeds": [
                "cam185",
                "cam186",
            ]
        },
        {
            "id": "intersection4",
            "name": "Merivälja tee - Kloostrimetsa tee",
            "coordinate": Point([24.834111, 59.468228]),
            "max_bus_distance": 100,
            "feeds": [
                "cam196",
                "cam197",
            ]
        },
    ]

lights = {
    "foor1": [
        {
            "type": "direct",
            "feed": "cam072",
            "red_pos": (201, 107),
            "green_pos": (202, 119),
            "color_multiplier": 0,
            "confidence": 0.7,
        },
        {
            "type": "condition",
            "state": "red",
            "if": "jfoor1b",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor11",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor12",
            "has_state": "green",
        },
    ],
    "foor2": [
        {
            "type": "direct",
            "feed": "cam072",
            "red_pos": (195, 109),
            "green_pos": (196, 120),
            "confidence": 0.7,
        },
        {
            "type": "condition",
            "state": "red",
            "if": "jfoor1b",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor11",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor12",
            "has_state": "green",
        },
    ],
    "foor3": [  # Otse Sõpruse pst-l
        {
            "type": "direct",
            "feed": "cam071",
            "red_pos": (359, 57),
            "green_pos": (360, 67)
        },
        {
            "type": "condition",
            "state": "red",
            "if": "jfoor2b",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor1",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor2",
            "has_state": "green",
        },
    ],
    "foor4": [  # Vasakule Sõpruse pst-lt Tammsaare teele
        {
            "type": "direct",
            "feed": "cam071",
            "red_pos": (354, 56),
            "green_pos": (354, 67),
        },
        {
            "type": "condition",
            "state": "red",
            "if": "jfoor1a",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "jfoor2b",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor1",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor2",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor12",
            "has_state": "green",
        },
    ],
    "jfoor1a": [
        {
            "type": "direct",
            "feed": "cam071",
            "red_pos": (109, 118),
            "green_pos": (109, 125),
        },
    ],
    "jfoor1b": [
        {
            "type": "direct",
            "feed": "cam071",
            "red_pos": (179, 155),
            "green_pos": (179, 165),
        },
        {
            "type": "direct",
            "feed": "cam072",
            "red_pos": (1211, 251),
            "green_pos": (1206, 263),
        },
    ],
    "jfoor2a": [
        {
            "type": "direct",
            "feed": "cam072",
            "red_pos": (763, 78),
            "green_pos": (762, 84),
        },
    ],
    "jfoor2b": [
        {
            "type": "direct",
            "feed": "cam071",
            "red_pos": (1269, 226),
            "green_pos": (1268, 231),
        },
        {
            "type": "direct",
            "feed": "cam072",
            "red_pos": (528, 52),
            "green_pos": (528, 56),
        }
    ],
    "foor11": [
        {
            "type": "direct",
            "feed": "cam072",
            "red_pos": (667, 75),
            "green_pos": (666, 91),
            "brightness_multiplier": 0,
            "confidence": 0.7,
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor1",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor2",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "jfoor2a",
            "has_state": "green",
        },
    ],
    "foor12": [
        {
            "type": "direct",
            "feed": "cam072",
            "red_pos": (660, 75),
            "green_pos": (660, 89),
            "brightness_multiplier": 0,
            "confidence": 0.7,
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor1",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor2",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor3",
            "has_state": "green",
        },
    ],
    "foor5": [
        {
            "type": "direct",
            "feed": "cam104",
            # "dist_from_camera": 10,
            "red_pos": (1131, 334),
            "green_pos": (1127, 376),
        },
        {
            "type": "condition",
            "state": "red",
            "if": "jfoor3",
            "has_state": "green",
        },
        {
            "type": "traffic",
            "feed": "cam104",
            "polygons": [np.array([[
                (317, 247),
                (620, 347),
                (1092, 374),
                (1139, 210),
                (1016, 136),
                (731, 234),
                (511, 187)
            ]], dtype=np.int32), np.array([[
                (0, 374),
                (36, 354),
                (141, 719),
                (0, 719)
            ]], dtype=np.int32)],
            "angleRanges": [(30, 83)]
        }
    ],
    "jfoor3": [
        {
            "type": "direct",
            "feed": "cam104",
            # "dist_from_camera": 25,
            "red_pos": (249, 175),
            "green_pos": (249, 182),
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor5",
            "has_state": "green",
        }
    ],
    "foor6": [
        {
            "type": "direct",
            "feed": "cam185",
            "red_pos": (472, 169),
            "green_pos": (472, 190),
        },
        {
            "type": "direct",
            "feed": "cam185",
            "red_pos": (522, 156),
            "green_pos": (522, 174),
        },
        {
            "type": "direct",
            "feed": "cam185",
            "red_pos": (739, 52),
            "green_pos": (738, 72),
        },
        {
            "type": "direct",
            "feed": "cam185",
            "red_pos": (924, 193),
            "green_pos": (924, 212),
        },
        {
            "type": "traffic",
            "feed": "cam185",
            "polygons": [np.array([[
                (499, 270),
                (309, 364),
                (900, 420),
                (894, 285)
            ]], dtype=np.int32), np.array([[
                (554, 237),
                (874, 256),
                (868, 243),
                (606, 204)
            ]], dtype=np.int32)],
            "angleRanges": [(45, 90)]
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor8",
            "has_state": "green"
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor7",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor10",
            "has_state": "green",
        },
    ],
    "jfoor4": [
        {
            "type": "direct",
            "feed": "cam185",
            "red_pos": (1271, 168),
            "green_pos": (1271, 180),
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor10",
            "has_state": "green",
        },
    ],
    "jfoor5": [
        {
            "type": "direct",
            "feed": "cam185",
            "red_pos": (1162, 172),
            "green_pos": (1161, 186),
            "slice_size": 2
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor8",
            "has_state": "green"
        },
    ],
    "foor7": [
        {
            "type": "direct",
            "feed": "cam185",
            "red_pos": (1020, 127),
            "green_pos": (1020, 135),
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor6",
            "has_state": "green",
        },
    ],
    "foor8": [
        {
            "type": "direct",
            "feed": "cam186",
            "red_pos": (911, 111),
            "green_pos": (911, 123),
        },
        {
            "type": "direct",
            "feed": "cam186",
            "red_pos": (763, 11),
            "green_pos": (763, 25),
        },
        {
            "type": "direct",
            "feed": "cam186",
            "red_pos": (708, 73),
            "green_pos": (709, 81),
        },
        {
            "type": "direct",
            "feed": "cam186",
            "red_pos": (632, 96),
            "green_pos": (632, 107),
        },
        {
            "type": "traffic",
            "feed": "cam186",
            "polygons": [np.array([[
                (580, 164),
                (401, 213),
                (713, 292),
                (907, 132),
                (659, 156)
            ]], dtype=np.int32)],
            "angleRanges": [(45, 90)]
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor10",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "jfoor5",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor6",
            "has_state": "green",
        },
    ],
    "foor9": [
        {
            "type": "direct",
            "feed": "cam186",
            "red_pos": (1037, 97),
            "green_pos": (1037, 106),
        },
        {
            "type": "direct",
            "feed": "cam186",
            "red_pos": (1075, 88),
            "green_pos": (1075, 95),
        },
        {
            "type": "direct",
            "feed": "cam186",
            "red_pos": (1088, 47),
            "green_pos": (1089, 55),
        },
        {
            "type": "direct",
            "feed": "cam186",
            "red_pos": (1182, 116),
            "green_pos": (1183, 125),
        },
        {
            "type": "traffic",
            "feed": "cam186",
            "polygons": [np.array([[
                (940, 180),
                (1160, 218),
                (1176, 155),
                (1033, 141),
                (921, 144)
            ]], dtype=np.int32)],
            "angleRanges": [(45, 90)]
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor10",
            "has_state": "green",
        },
    ],
    "foor10": [
        {
            "type": "condition",
            "state": "red",
            "if": "foor8",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "foor9",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "red",
            "if": "jfoor4",
            "has_state": "green",
        },
        {
            "type": "condition",
            "state": "green",
            "if": "jfoor4",
            "has_state": "red",
        },
    ],
    "jfoor6": [
        {
            "type": "direct",
            "feed": "cam196",
            "red_pos": (464, 273),
            "green_pos": (467, 294),
        },
    ],
    "jfoor7": [
        {
            "type": "direct",
            "feed": "cam197",
            "red_pos": (579, 79),
            "green_pos": (579, 84),
            "slice_size": 2
        },
    ]
}
