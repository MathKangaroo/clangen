import random
from random import choice, randint
from re import sub

import i18n

import scripts.game_structure.screen_settings
from scripts.cat.sprites import sprites
from scripts.game_structure import constants
from scripts.game_structure.game_essentials import game
from scripts.game_structure.localization import get_lang_config
from scripts.utility import adjust_list_text
from scripts.game_structure.game.settings import game_setting_get


class Pelt:
    sprites_names = {
        "SingleColour": "single",
        "TwoColour": "single",
        "Tabby": "tabby",
        "Marbled": "marbled",
        "Rosette": "rosette",
        "Smoke": "smoke",
        "Ticked": "ticked",
        "Speckled": "speckled",
        "Bengal": "bengal",
        "PrideBengal": "pridebengal",
        "Mackerel": "mackerel",
        "PrideMackerel": "pridemackerel",
        "Classic": "classic",
        "PrideClassic": "prideclassic",
        "Sokoke": "sokoke",
        "Agouti": "agouti",
        "PrideAgouti": "prideagouti",
        "Singlestripe": "singlestripe",
        "Masked": "masked",
        "Brindle": "brindle",
        "Wolf": "wolf",
        "Wildcat": "wildcat",
        "Spots": "spots",
        "Smokepoint": "smokepoint",
        "Finleappatches": "finleappatches",
        "Tortie": None,
        "Calico": None,
        "Stain": "stain",
        "Maned": "maned",
        "Ocelot": "ocelot",
        "Lynx": "lynx",
        "Dalmatian": "dalmatian",
        "Royal": "royal",
        "Bobcat": "bobcat",
        "Cheetah": "cheetah",
        "Abyssinian": "abyssinian",
        "Clouded": "clouded",
        "Doberman": "doberman",
        "GhostTabby": "ghosttabby",
        "Merle": "merle",
        "Monarch": "monarch",
        "Oceloid": "oceloid",
        "PinstripeTabby": "pinstripetabby",
        "Snowflake": "snowflake",
        "Dot": "dot",
        "Caliisokoke": "caliisokoke",
        "Caliispeckled": "caliispeckled",
        "Kintsugi": "kintsugi",
        "Dotfade": "dotfade",
        "Circletabby": "circletabby",
        "Colourpoint": "colourpoint",
        "Lynxpoint": "lynxpoint",
        "Ncrestedcaracara": "ncrestedcaracara",
        "Birchtabby": "birchtabby"
    }

    # ATTRIBUTES, including non-pelt related
    pelt_colours = [
        "WHITE",
        "PALEGREY",
        "SILVER",
        "GREY",
        "DARKGREY",
        "GHOST",
        "BLACK",
        "CREAM",
        "PALEGINGER",
        "GOLDEN",
        "GINGER",
        "DARKGINGER",
        "SIENNA",
        "LIGHTBROWN",
        "LILAC",
        "BROWN",
        "GOLDEN-BROWN",
        "DARKBROWN",
        "CHOCOLATE",
    ]

    # sparkle cats
    minecraft_colors = [
        'ACACIALOG', 'BAMBOO', 'BIRCHLOG', 'CHERRYLOG', 'CRIMSONSTEM', 'DARKOAKLOG', 'JUNGLELOG', 'MANGROVELOG',
        'OAKLOG', 'SPRUCELOG', 'WARPEDSTEM', 'ACACIAPLANKS', 'BAMBOOPLANKS', 'BIRCHPLANKS', 'CHERRYPLANKS',
        'CRIMSONPLANKS', 'DARKOAKPLANKS', 'JUNGLEPLANKS', 'MANGROVEPLANKS', 'OAKPLANKS', 'SPRUCEPLANKS', 'WARPEDPLANKS',
        'AMETHYST', 'BLACKGLAZEDTERRACOTTA', 'BLUEGLAZEDTERRACOTTA', 'BROWNGLAZEDTERRACOTTA', 'BROWN MUSHROOM',
        'COPPER', 'CRYING OBSIDIAN', 'CYANGLAZEDTERRACOTTA', 'EXPOSEDCOPPER', 'GRAYGLAZEDTERRACOTTA',
        'GREENGLAZEDTERRACOTTA', 'LIGHTBLUEGLAZED TERRACOTTA', 'LIGHTGRAYGLAZEDTERRACOTTA', 'LIMEGLAZEDTERRACOTTA',
        'MAGENTAGLAZEDTERRACOTTA', 'MUSHROOMINSIDE', 'MUSHROOMSTEM', 'OBSIDIAN', 'ORANGEGLAZEDTERRACOTTA',
        'OXIDIZEDCOPPER', 'PINKGLAZEDTERRACOTTA', 'PURPLEGLAZEDTERRACOTTA', 'PURPUR', 'QUARTZ', 'REDGLAZEDTERRACOTTA',
        'REDMUSHROOM', 'WEATHEREDCOPPER', 'WHITEGLAZEDTERRACOTTA', 'YELLOWGLAZEDTERRACOTTA'
    ]

    anju_colors = [
        'PINK', 'RED', 'LIGHTGREEN', 'GREEN', 'CYAN', 'BLUE', 'PURPLE'
    ]

    cs2_colors = [
        'LIGHTLIME', 'PINKGREY', 'YELLOWBROWN', 'REDGREY', 'BLUEBROWN', 'GHOSTBROWN', 'BLACKPURPLE', 'BLUECREAM',
        'PALEPINKPURPLE', 'ICEBLUE', 'BLUECS2', 'GREENBROWN', 'NAVYBLUE', 'PURPLECREAM', 'INDIGOBLUSH', 'VIOLETBLUSH',
        'MAGENTA', 'NAVYBROWN', 'MULBERRY'
    ]

    cs_colors = [
        'ICEWHITE', 'CRYSTAL', 'ORCHID', 'CERULEAN', 'GRAPE', 'GHOSTBLUE', 'BLACKBLUE', 'THISTLE', 'SUNYELLOW',
        'BUBBLEGUM', 'REDSTAIN', 'ROSE', 'DUSKBROWN', 'FROZENSUN', 'GREENGOLD', 'OCEAN', 'TEAL', 'REDBLUE', 'TREE'
    ]

    heta_colors = [
        'REDHETA', 'ORANGEHETA', 'YELLOWHETA', 'NEONYELLOW', 'NEONGREEN', 'GREENHETA', 'MINTGREEN', 'DARKMINT',
        'NEONTEAL', 'CYANHETA', 'BLUEHETA', 'NAVYHETA', 'INDIGOHETA', 'PURPLEHETA', 'VIOLETHETA', 'MAGENTAHETA',
        'PINKHETA', 'SCARLETPINK', 'DARKREDHETA'
    ]

    hive_colors = [
        'GREENH', 'TEALH', 'BLUEH', 'NAVYH', 'INDIGOH', 'PURPLEH', 'VIOLETH', 'PINKH', 'ROSEH', 'DARKPINKH', 'REDH',
        'ORANGEH', 'GOLDH', 'PASTELPURPLEH', 'DARKGREENH', 'BROWN-PURPLE', 'YELLOWH', 'DARKMOSS', 'PURPLESWIRL'
    ]

    kris_colors = [
        'PINKCREAM', 'BLUEMINT', 'SUNSET', 'PINK-BLUE', 'INDIGOK', 'BLUEGHOSTK', 'PINKK', 'PASTELPINKBLUE',
        'RUSTYGREEN', 'OURPLE', 'BLUE-YELLOW', 'BLUE-PURPLE', 'DARKSUNSET', 'BANANABERRY', 'BRIGHTBLUEK', 'SUNRISE',
        'GREEN-NAVY', 'PINKSHADOW', 'REDK'
    ]

    meteor_colors = [
        'SILVERMETEOR', 'SILVERNAVY', 'CREAMSILVER', 'GREYSTAR', 'DARKGREYSTAR', 'BLACK-BROWN', 'BLUESPOTTED',
        'CREAMMETEOR', 'PINK-WHITE', 'TANSPOTTED', 'REVERSESUN', 'WARM-BLUE', 'INDIGO-VIOLET', 'GREYMETEOR',
        'ICESPOTTED', 'SHADOW', 'BLUE-EARTH', 'EARTHSPOTTED', 'BROWN-TAN'
    ]

    pastel_colors = [
        'PALEPINK-PURPLE', 'PALEGREY-PINK', 'PALEBLUE-YELLOW', 'PALEMINT-PURPLE', 'PALEGREEN-INDIGO',
        'PALEYELLOW-INDIGO', 'PALEORANGE-BLUE', 'PALEPURPLE-GOLD', 'PALECYAN-GOLD', 'PALEMINT-MAGENTA',
        'PALEMINT-VIOLET', 'PALEGREEN-BLUE', 'PALEGREEN-NAVY', 'PALEBLUE-INDIGO', 'PALECYAN-PURPLE', 'PALECYAN-NAVY',
        'PALECYAN-BLUE', 'PALEYELLOWGREEN', 'PALEYELLOW-BLUE'
    ]

    pepper_colors = [
        'ICEPEPPER', 'CYANPEPPER', 'BLUEPEPPER', 'OCEANPEPPER', 'DARKBLUEPEPPER', 'BLUEGHOSTPEPPER', 'BLACKBLUEPEPPER',
        'GOLDCREAM', 'GOLDPEPPER', 'YELLOW-RED', 'BRIGHTYELLOW-RED', 'NEONRED', 'REDBLACK', 'PALEBLUE-GOLD',
        'INDIGOPEPPER', 'RUSTBLUEPEPPER', 'REDPEPPER', 'REDBLUEBLACK', 'SCARLETPEPPER'
    ]

    sparkle_colors = [
        'REDS', 'RED-ORANGES', 'DARKYELLOWS', 'GREENREDS', 'CYANPINKG', 'INDIGOREDS', 'REVERSERAINBOW', 'PINKREDS',
        'RUSTYS', 'GREENORANGES', 'REDCYANS', 'MINTBLUES', 'BLACKBLUES', 'BANANAS', 'WHITEGREENS', 'BROWNREDS',
        'RAINBOW', 'GREENDARKREDS', 'SUNNYS'
    ]

    # mega colors mod

    dance_colours = [
        'LIGHTCINNAMON', 'CINNAMON', 'SILVERFAWN', 'DARKCINNAMON', 'DARKFAWN', 'FAWN', 'LIGHTFAWN', 'PALEFAWN',
        'PALECREAM', 'LIGHTCREAM', 'DANCECREAM', 'DARKCREAM', 'DARKGOLD', 'GOLD', 'LIGHTGOLD', 'SILVERCREAM',
        'PALEGOLD', 'SUNSHINE', 'BRONZE'
    ]

    silly_colours = [
        'LIGHTLILAC', 'LILACSILLY', 'DARKLILAC', 'DARKASH', 'ASH', 'LIGHTASH', 'PALEASH', 'SILVERCINNAMON', 'SILVERRED',
        'PALEBROWN', 'LIGHTBROWNSILLY', 'BROWNSILLY', 'DARKBROWNSILLY', 'EBONY', 'DARKCHOCOLATE', 'CHOCOLATESILLY',
        'LIGHTCHOCOLATE', 'PALECHOCOLATE', 'PALECINNAMON'
    ]

    ster_colours = [
        'WHITESTER', 'PALEGREYSTER', 'LIGHTGREY', 'GREYSTER', 'DARKGREYSTER', 'BLACKSTER', 'OBSIDIANSTER', 'GHOSTSTER',
        'PALEBLUE', 'LIGHTBLUE', 'BLUESTER', 'DARKBLUE', 'SILVERCHOCOLATE', 'SILVERORANGE', 'DARKSLATE', 'SLATE',
        'LIGHTSLATE', 'PALESLATE', 'PALELILAC'
    ]

    mimi_colours = [
        'COPPERMIMI', 'DARKORANGE', 'ORANGE', 'LIGHTORANGE', 'PALEORANGE', 'PALEGINGERMIMI', 'LIGHTGINGER',
        'GINGERMIMI', 'DARKGINGERMIMI', 'SILVERGOLD', 'RUSSET', 'DARKRED', 'REDMIMI', 'LIGHTRED', 'PALERED',
        'SILVERMIMI', 'SILVERGREY', 'SILVERBLUE', 'SILVERSLATE'
    ]

    no_masked = heta_colors + minecraft_colors + anju_colors + pastel_colors + pepper_colors

    pelt_c_no_white = [
        "PALEGREY",
        "SILVER",
        "GREY",
        "DARKGREY",
        "GHOST",
        "BLACK",
        "CREAM",
        "PALEGINGER",
        "GOLDEN",
        "GINGER",
        "DARKGINGER",
        "SIENNA",
        "LIGHTBROWN",
        "LILAC",
        "BROWN",
        "GOLDEN-BROWN",
        "DARKBROWN",
        "CHOCOLATE",
    ]
    pelt_c_no_bw = [
        "PALEGREY",
        "SILVER",
        "GREY",
        "DARKGREY",
        "CREAM",
        "PALEGINGER",
        "GOLDEN",
        "GINGER",
        "DARKGINGER",
        "SIENNA",
        "LIGHTBROWN",
        "LILAC",
        "BROWN",
        "GOLDEN-BROWN",
        "DARKBROWN",
        "CHOCOLATE",
    ]

    tortiepatterns = [
        'ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR',
        'HALF', 'OREO', 'SWOOP', 'MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'ORIOLE',
        'CHIMERA', 'DAUB', 'EMBER', 'BLANKET', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'SMUDGED',
        'DAPPLENIGHT', 'STREAK', 'MASK', 'CHEST', 'ARMTAIL', 'SMOKE', 'GRUMPYFACE', 'BRIE', 'BELOVED', 'BODY', 'SHILOH',
        'FRECKLED', 'HEARTBEAT',

        'MINKLITTLE', 'MINKLIGHTTUXEDO', 'MINKBUZZARDFANG', 'MINKTIP', 'MINKBLAZE', 'MINKBIB', 'MINKVEE', 'MINKPAWS',
        'MINKBELLY', 'MINKTAILTIP', 'MINKTOES', 'MINKBROKENBLAZE', 'MINKLILTWO', 'MINKSCOURGE', 'MINKTOESTAIL',
        'MINKRAVENPAW', 'MINKHONEY', 'MINKLUNA', 'MINKEXTRA', 'MINKMUSTACHE', 'MINKREVERSEHEART', 'MINKSPARKLE',
        'MINKRIGHTEAR', 'MINKLEFTEAR', 'MINKESTRELLA', 'MINKREVERSEEYE', 'MINKBACKSPOT', 'MINKEYEBAGS', 'MINKLOCKET',
        'MINKBLAZEMASK', 'MINKTEARS', 'MINKTUXEDO', 'MINKFANCY', 'MINKUNDERS', 'MINKDAMIEN', 'MINKSKUNK', 'MINKMITAINE',
        'MINKSQUEAKS', 'MINKSTAR', 'MINKWINGS', 'MINKDIVA', 'MINKSAVANNAH', 'MINKFADESPOTS', 'MINKBEARD',
        'MINKDAPPLEPAW', 'MINKTOPCOVER', 'MINKWOODPECKER', 'MINKMISS', 'MINKBOWTIE', 'MINKVEST', 'MINKFADEBELLY',
        'MINKDIGIT', 'MINKFCTWO', 'MINKFCONE', 'MINKMIA', 'MINKROSINA', 'MINKPRINCESS', 'MINKDOUGIE', 'MINKANY',
        'MINKANYTWO', 'MINKBROKEN', 'MINKFRECKLES', 'MINKRINGTAIL', 'MINKHALFFACE', 'MINKPANTSTWO', 'MINKGOATEE',
        'MINKPRINCE', 'MINKFAROFA', 'MINKMISTER', 'MINKPANTS', 'MINKREVERSEPANTS', 'MINKHALFWHITE', 'MINKAPPALOOSA',
        'MINKPIEBALD', 'MINKCURVED', 'MINKGLASS', 'MINKMASKMANTLE', 'MINKMAO', 'MINKPAINTED', 'MINKSHIBAINU', 'MINKOWL',
        'MINKBUB', 'MINKSPARROW', 'MINKTRIXIE', 'MINKSAMMY', 'MINKFRONT', 'MINKBLOSSOMSTEP', 'MINKBULLSEYE', 'MINKFINN',
        'MINKSCAR', 'MINKBUSTER', 'MINKHAWKBLAZE', 'MINKCAKE', 'MINKVAN', 'MINKONEEAR', 'MINKLIGHTSONG', 'MINKTAIL',
        'MINKHEART', 'MINKMOORISH', 'MINKAPRON', 'MINKCAPSADDLE', 'MINKCHESTSPECK', 'MINKBLACKSTAR', 'MINKPETAL',
        'MINKHEARTTWO', 'MINKPEBBLESHINE', 'MINKBOOTS', 'MINKCOW', 'MINKCOWTWO', 'MINKLOVEBUG', 'MINKSHOOTINGSTAR',
        'MINKEYESPOT', 'MINKPEBBLE', 'MINKTAILTWO', 'MINKBUDDY', 'MINKKROPKA', 'MINKCOLOURPOINT', 'MINKRAGDOLL',
        'MINKSEPIAPOINT', 'MINKMINKPOINT', 'MINKSEALPOINT', 'MINKVITILIGO', 'MINKVITILIGOTWO', 'MINKMOON',
        'MINKPHANTOM', 'MINKKARPATI', 'MINKPOWDER', 'MINKBLEACHED', 'MINKSMOKEY', 'MINKFULLWHITE',

        'CHAOSONE', 'CHAOSTWO', 'CHAOSTHREE', 'CHAOSFOUR', 'ERROR', 'WAVE', 'PONINTTORITE', 'MASKTORITE', 'LITTLESTAR',
        'TANBUNNY', 'STRIPES', 'PINITO', 'SKULL', 'SIGHT', 'BRINDLETORITE', 'SNOW', 'ROSETTESTORITE', 'AMBERONE',
        'KINTSUGIONE', 'BENGALMASK', 'SHADOW', 'RAIN', 'MGLA', 'MOONLIGHT', 'MOUSE', 'SATURN', 'MARBLETORINE',
        'AMBERTWO', 'PATTERN', 'MOSS', 'MONKEY', 'BUMBLEBEE', 'KINTSUGITWO', 'STORM', 'CLASSICTORNIE',
        'STRIPEONETORITE', 'MACKERELTORITE', 'AMBERTHREE', 'SHADE', 'GRAFFITI', 'AGOUTITORIE', 'BENGALTORITE',
        'TABBYTORITE', 'SOKKOKETORITE', 'SPECKLEDTORITE', 'TICKEDTORIE', 'MORRO', 'AMBERFOUR', 'DOG', 'ONESPOT', 'INK',
        'WOLF', 'EYEV', 'GEM', 'FOX', 'ORCA', 'PINTO', 'FRECKLESTWO', 'SOLDIER', 'AKITA', 'CHESSBORAD', 'ANT', 'CREAMV',
        'BUNNY', 'MOJO', 'STAINSONE', 'STAINST', 'HALFHEART', 'FRECKLESTHREE', 'KITTY', 'SUNRISE', 'HUSKY',
        'STATNTHREE', 'ERAMASK', 'S', 'PAW', 'SWIFTPAW', 'BOOMSTAR', 'MIST', 'LEON', 'LADY', 'LEGS', 'MEADOW', 'SALT',
        'BAMBI', 'PRIMITVE', 'SKUNKSTRIPE', 'NEPTUNE', 'KARAPATITWO', 'CHAOS', 'MOSCOW', 'ERAHALF', 'CAPETOWN', 'SUN',
        'BANAN', 'PANDA', 'DOVE', 'PINTOTWO', 'SNOWSHOE', 'SKY', 'MOONSTONE', 'DRIP', 'CRESCENT', 'ETERNAL', 'WINGTWO',
        'STARBORN', 'SPIDERLEGS', 'APPEL', 'RUG', 'LUCKY', 'SOCKS', 'BRAMBLEBERRY', 'LATKA', 'ASTRONAUT', 'STORK'
    ]

    tortiebases = [
        'single', 'tabby', 'bengal', 'marbled', 'ticked', 'smoke', 'rosette', 'speckled', 'mackerel', 'classic',
        'sokoke', 'agouti', 'singlestripe', 'masked', 'maned', 'ocelot', 'lynx', 'royal', 'bobcat', 'cheetah',
        'dalmatian', 'wolf', 'brindle', 'spots', 'smokepoint', 'finleappatches', 'wildcat', 'abyssinian', 'clouded',
        'doberman', 'ghosttabby', 'merle', 'monarch', 'oceloid', 'pinstripetabby', 'snowflake', 'caliisokoke',
        'caliispeckled', 'circletabby', 'birchtabby', 'dot', 'dotfade', 'kintsugi', 'colourpoint', 'lynxpoint',
        'ncrestedcaracara', 'prideagouti', 'pridebengal', 'prideclassic', 'pridemackerel'
    ]

    pelt_length = ["short", "medium", "long"]
    # please don't judge the eye_colours section
    eye_colours = [
        'YELLOW', 'AMBER', 'HAZEL', 'PALEGREEN', 'GREEN', 'BLUE', 'DARKBLUE', 'GREY', 'CYAN', 'EMERALD', 'PALEBLUE',
        'PALEYELLOW', 'GOLD', 'HEATHERBLUE', 'COPPER', 'SAGE', 'COBALT', 'SUNLITICE', 'GREENYELLOW', 'BRONZE', 'SILVER',
        'ROSE', 'ALGAE', 'SEAFOAM', 'LIGHT FLAME', 'CLOUDY', 'RED', 'TURQUOISE', 'SWAMP', 'RAINY', 'AQUAMARINE',
        'EARTH', 'PUMPKIN', 'LILAC', 'PERIWINKLE', 'VIOLET', 'POND', 'DIRT', 'BROWN', 'CEDAR', 'CHRISTMAS',
        'COTTON CANDY', 'DARK PINE', 'FALL', 'FOREST FIRE', 'GOLD MOON', 'HALLOWEEN', 'LOBELIA', 'MIDNIGHT',
        'MOONSTONE', 'OXIDIZED', 'SNOW', 'BERRY BANANA', 'DAWN SKY', 'TWILIGHT SKY', 'WORMY', 'BLUE HAZEL',
        'THUNDERBOLT', 'VOLCANO', 'SEASHELL', 'PARADOX', 'CURSE', 'BLESSING', 'VALENTINE', 'FIREWORK', 'LUCKY', 'LIME',
        'PALE BROWN', 'CRIMSON', 'DARK HAZEL', 'ROSE GOLD', 'DARK ROSE', 'REVERSE SUNLITICE', 'ICY', 'SUNSET',
        'LAVENDER', 'ECLIPSE', 'BLACK', 'MUDDY', 'DARK TURQUOISE', 'BLACKBERRY', 'RUSTY', 'PASTEL', 'AVOCADO',
        'PASTEL LAVENDER', 'ALBINO', 'WINTER ROSE', 'BULLET', 'LIGHT YELLOW', 'SUNSHINE', 'GOLD ORE',
        'FOSSILIZED AMBER', 'DUSKY', 'LICHEN', 'SPRING', 'TREE', 'LEAVES', 'EMERALD ORE', 'HAZELNUT', 'BLUE SKY',
        'OCEAN', 'OVERCAST', 'AQUA', 'IRIS', 'ROBIN', 'GREY SILVER', 'SAND', 'MUSTARD', 'BRONZE ORE', 'TIMBER',
        'COPPER ORE', 'FERN', 'APPLE', 'MOSS', 'THICKET', 'PEACOCK', 'OLIVE', 'STORMY BLUE', 'DEPTHS', 'STORMY', 'TEAL',
        'INDIGO', 'STEEL', 'PEACH', 'DAFFODIL', 'MARIGOLD', 'BRASS', 'DARKAMBER', 'DAWN SKIES', 'MINT', 'CHARTREUSE',
        'MEADOW', 'LEAF', 'LIGHT TURQUOISE', 'SAP', 'ALBINISTIC', 'COBALT ORE', 'RAIN', 'CYAN DYE', 'PERIWINKLE PURPLE',
        'ICY CRACK', 'PINK', 'MORNING', 'DARK BROWN', 'BAY', 'NEON GREEN', 'SEA', 'DISCORD', 'AUTUMN LEAF', 'RUBY',
        'PHANTOM', 'RIVER MOSS', 'WICKED', 'ORANGE'
    ]

    yellow_eyes = [
        'BULLET', 'GREY SILVER', 'PEACH', 'LIGHT YELLOW', 'SAND', 'DAFFODIL', 'SUNSHINE', 'MUSTARD', 'MARIGOLD',
        'GOLD ORE', 'BRONZE ORE', 'BRASS', 'FOSSILIZED AMBER', 'TIMBER', 'COPPER ORE', 'DAWN SKY', 'YELLOW', 'AMBER',
        'PALEYELLOW', 'GOLD', 'COPPER', 'GREENYELLOW', 'BRONZE', 'SILVER', 'ROSE', 'LIGHT FLAME', 'PUMPKIN', 'BROWN',
        'DARK PINE', 'FALL', 'GOLD MOON', 'OXIDIZED', 'BERRY BANANA', 'WORMY', 'THUNDERBOLT', 'PALE BROWN', 'MORNING',
        'BLACK', 'ROSE GOLD', 'DARK BROWN', 'MUDDY', 'RUSTY', 'BAY', 'DISCORD', 'ORANGE', 'AUTUMN LEAF'
    ]

    blue_eyes = [
        'BLUE SKY', 'STORMY BLUE', 'OCEAN', 'DEPTHS', 'COBALT ORE', 'OVERCAST', 'STORMY', 'RAIN', 'AQUA', 'TEAL',
        'CYAN DYE', 'IRIS', 'INDIGO', 'PERIWINKLE PURPLE', 'ROBIN', 'STEEL', 'DAWN SKIES', 'ICY CRACK', 'BLUE',
        'DARKBLUE', 'CYAN', 'PALEBLUE', 'COBALT', 'SUNLITICE', 'GREY', 'SEAFOAM', 'CLOUDY', 'TURQUOISE', 'RAINY',
        'POND', 'MIDNIGHT', 'MOONSTONE', 'SNOW', 'WICKED', 'PHANTOM', 'DAWN SKY', 'BLUE HAZEL', 'CURSE', 'FIREWORK',
        'REVERSE SUNLITICE', 'ICY', 'WINTER ROSE'
    ]

    green_eyes = [
        'LICHEN', 'FERN', 'MINT', 'SPRING', 'APPLE', 'CHARTREUSE', 'LEAVES', 'MOSS', 'MEADOW', 'RIVER MOSS', 'TREE',
        'THICKET', 'LEAF', 'EMERALD ORE', 'PEACOCK', 'LIGHT TURQUOISE', 'HAZELNUT', 'OLIVE', 'SAP', 'PALEGREEN',
        'GREEN', 'EMERALD', 'SAGE', 'HAZEL', 'ALGAE', 'SWAMP', 'AQUAMARINE', 'EARTH', 'DIRT', 'FOREST FIRE', 'LIME',
        'LUCKY', 'DARK HAZEL', 'DARK TURQUOISE', 'AVOCADO', 'NEON GREEN', 'SEA'
    ]

    red_eyes = [
        'BLESSING', 'CEDAR', 'CHRISTMAS', 'COTTON CANDY', 'CRIMSON', 'DARK ROSE', 'DARKAMBER', 'ECLIPSE', 'PINK', 'RED',
        'ROSE', 'RUBY', 'SUNSET', 'VALENTINE', 'VOLCANO'
    ]

    purple_eyes = [
        'ALBINISTIC', 'BLACKBERRY', 'DUSKY', 'HALLOWEEN', 'HEATHERBLUE', 'LAVENDER', 'LILAC', 'LOBELIA', 'PARADOX',
        'PASTEL', 'PASTEL LAVENDER', 'PERIWINKLE', 'SEASHELL', 'TWILIGHT SKY', 'VIOLET'
    ]

    neos_eyes = [
        'NEO FIRE', 'NEO AMETHYST', 'NEO LIME', 'NEO VIOLET', 'NEO SUN', 'NEO TURQUOISE', 'NEO YELLOW', 'NEO SCARLET',
        'NEO PINKPURPLE', 'NEO LIGHTBLUE', 'NEO DARKBLUE', 'NEO CYAN', 'NEO YELLOWRED', 'NEO PINK', 'NEO INDIGO',
        'NEO PURPLE', 'NEO YELLOWGREEN', 'NEO ICEBLUE', 'NEO PALEPINK', 'NEO MINT', 'NEO BLACKBLUE'
    ]

    flutter_eyes = [
        'FLUTTER SUNSET', 'FLUTTER MONARCH', 'FLUTTER PEACOCK', 'FLUTTER LUNAR', 'FLUTTER GREENORANGE', 'FLUTTER BEACH',
        'FLUTTER REDADMIRAL', 'FLUTTER DARK', 'FLUTTER RAINBOW', 'FLUTTER LIGHTBLUE', 'FLUTTER GALAXY',
        'FLUTTER STAINEDGLASS', 'FLUTTER GLASSWING', 'FLUTTER GREENSTRIPE', 'FLUTTER BLUEYELLOW',
        'FLUTTER PASTELGALAXY', 'FLUTTER MOTH', 'FLUTTER SPARKLYDUST', 'FLUTTER IMPERIAL', 'FLUTTER PINKHEARTS',
        'FLUTTER DUSTOX'
    ]

    lamp_eyes = [
        'LAMP YELLOW', 'LAMP ORANGE', 'LAMP HAZEL', 'LAMP YELLOWGREEN', 'LAMP GREEN', 'LAMP BLUE', 'LAMP DARKBLUE',
        'LAMP GRAY', 'LAMP CYAN', 'LAMP TURQUOISE', 'LAMP PURPLE', 'LAMP GOLD', 'LAMP ORANGE2', 'LAMP DARKHAZEL',
        'LAMP DARKBLUE2', 'LAMP BLUE2', 'LAMP BROWN', 'LAMP PALEYELLOW', 'LAMP LIGHTYELLOW', 'LAMP DARKYELLOW',
        'LAMP GOLDEGREEN'
    ]

    angel_eyes = [
        'ANGEL YELLOW', 'ANGEL ORANGE', 'ANGEL HAZEL', 'ANGEL YELLOWGREEN', 'ANGEL GREEN', 'ANGEL BLUE',
        'ANGEL DARKBLUE', 'ANGEL GRAY', 'ANGEL CYAN', 'ANGEL TURQUOISE', 'ANGEL PURPLE', 'ANGEL GOLD', 'ANGEL COPPER',
        'ANGEL MINT', 'ANGEL DARKBLUE2', 'ANGEL BLUE2', 'ANGEL BROWN', 'ANGEL SILVER', 'ANGEL LIGHTYELLOW',
        'ANGEL DARKYELLOW', 'ANGEL GOLDENGREEN'
    ]

    snail_eyes = [
        'SNAIL YELLOW', 'SNAIL ORANGE', 'SNAIL HAZEL', 'SNAIL YELLOWGREEN', 'SNAIL GREEN', 'SNAIL BLUE',
        'SNAIL DARKBLUE', 'SNAIL GRAY', 'SNAIL CYAN', 'SNAIL TURQUOISE', 'SNAIL PURPLE', 'SNAIL GOLD', 'SNAIL COPPER',
        'SNAIL MINT', 'SNAIL DARKBLUE2', 'SNAIL BLUE2', 'SNAIL BROWN', 'SNAIL SILVER', 'SNAIL LIGHTYELLOW',
        'SNAIL DARKYELLOW', 'SNAIL GOLDENGREEN'
    ]

    physical_trait_teeth = ['TEETHUPPER', 'TEETHSABRE', 'TEETHUNDERBITE', 'TEETHOVERBITE', 'TEETHHANG', 'TEETHJAGGED',
                            'TEETHTUSK', 'TEETHGONE', 'TEETHCHIPPED']

    physical_trait_ear_type = ['EARSMALL', 'EARBIG', 'EARTALL', 'EARPANTHER', 'EARWIDE', 'EARFLUFFY', 'EARRABBIT',
                               'EARDROOPY']

    physical_trait_ear_fold = ['FOLDBOTH', 'FOLDONE', 'EARCURL']

    physical_trait_headfur = ['HEADFORELOCK', 'HEADCOWLICK', 'HEADMOHAWK', 'HEADTUFT', 'HEADEMO', 'HEADJOWLS',
                              'HEADMULLET']

    physical_trait_cheekfur = ['CHEEKLONG', 'CHEEKPOINTED', 'CHEEKFLUFF', 'CHEEKCURL']

    physical_trait_mane = ['MANESILKY', 'MANEFLUFFY', 'MANERUFF', 'MANEHORSE', 'MANELION', 'MANEBRAIDED', 'MANECOBRA']

    physical_trait_fur_type = ['FURWAVY', 'FURCURLY', 'FURPATCHY', 'FURKINK', 'FURSHAGGY']

    physical_trait_muzzle_type = ['MUZZLESHORT', 'MUZZLEBROAD', 'MUZZLELONG']

    physical_trait_tail = ['TAILCROOKED', 'TAILLONG', 'TAILFEATHER', 'TAILCURL', 'TAILTUFT', 'TAILFORKED', 'TAILFOX']

    physical_trait_bodyfur = ['BACKFLUFF', 'BACKRIDGE', 'SHOULDERTUFT']

    physical_trait_misc = ['EARTUFTS', 'POLYDACTYL', 'LASHESUPPER', 'LASHESLOWER', 'WHISKERSLONG', 'CLAWSLONG',
                           'LEGTUFT', 'LARGEPAWS', 'SMALLPAWS', 'CLAWLESS', 'CLAWSSHORT', 'PAWTUFT', 'BIGEYES',
                           'SMALLEYES', 'BIGNOSE', 'HEARTSHAPEDNOSE', 'LONGLEGS', 'SHORTLEGS', 'CROSSEYED', 'LAZYEYE',
                           'OVERGROWNTONGUE', 'LONGCHINFUR', 'SHORTCHINFUR', 'LONGMUZZLEFUR', 'LONGINNEREARFUR',
                           'WEBBEDPAWS', 'MISSINGTOE', 'UNDERSIZEDJAW', 'OVERSIZEDJAW', 'FURBARBELS']

    # bite scars by @wood pank on discord

    # scars from other cats, other animals
    scars1 = [
        "ONE",
        "TWO",
        "THREE",
        "TAILSCAR",
        "SNOUT",
        "CHEEK",
        "SIDE",
        "THROAT",
        "TAILBASE",
        "BELLY",
        "LEGBITE",
        "NECKBITE",
        "FACE",
        "MANLEG",
        "BRIGHTHEART",
        "MANTAIL",
        "BRIDGE",
        "RIGHTBLIND",
        "LEFTBLIND",
        "BOTHBLIND",
        "BEAKCHEEK",
        "BEAKLOWER",
        "CATBITE",
        "RATBITE",
        "QUILLCHUNK",
        "QUILLSCRATCH",
        "HINDLEG",
        "BACK",
        "QUILLSIDE",
        "SCRATCHSIDE",
        "BEAKSIDE",
        "CATBITETWO",
        "FOUR",
    ]

    # missing parts
    scars2 = [
        "LEFTEAR",
        "RIGHTEAR",
        "NOTAIL",
        "HALFTAIL",
        "NOPAW",
        "NOLEFTEAR",
        "NORIGHTEAR",
        "NOEAR",
    ]

    # "special" scars that could only happen in a special event
    scars3 = [
        "SNAKE",
        "TOETRAP",
        "BURNPAWS",
        "BURNTAIL",
        "BURNBELLY",
        "BURNRUMP",
        "FROSTFACE",
        "FROSTTAIL",
        "FROSTMITT",
        "FROSTSOCK",
        "TOE",
        "SNAKETWO",
    ]

    # make sure to add plural and singular forms of new accs to acc_display.json so that they will display nicely
    bone_accessories = [
        "SNAKE", "BAT WINGS", "CANIDAE SKULL", "DEER ANTLERS", "RAM HORN", "GOAT HORN", "OX SKULL", "RAT SKULL",
        "TEETH COLLAR", "ROE SKULL", "BIRD SKULL1", "RIBS", "FISH BONES"
    ]

    butterflies_accessories = [
        "PEACOCK BUTTERFLY", "DEATH HEAD HAWKMOTH", "GARDEN TIGER MOTH", "ATLAS MOTH", "CECOROPIA MOTH",
        "WHITE ERMINE MOTH", "IO MOTH", "COMET MOTH", "JADE HAWKMOTH", "HUMMINGBIRD HAWKMOTH", "OWL BUTTERFLY",
        "GLASSWING BUTTERFLY", "QUEEN ALEXANDRA BIRDWING BUTTERFLY", "GREEN DRAGONTAIL BUTTERFLY",
        "MENELAUS BLUE MORPHO BUTTERFLY", "DEAD LEAF BUTTERFLY"
    ]

    stuff_accessories = [
        "OLD SILVER WATCH", "OLD GOLD WATCH", "GOLDEN KEY", "SILVER KEY", "DVD", "OLD PENCIL", "OLD BRUSH",
        "BANANA PEEL", "BROKEN VHS TAPE", "OLD NEWSPAPER", "SEA GLASS", "BAUBLES", "MUD AND DIRT"
    ]

    plant_accessories = [
        "MAPLE LEAF",
        "HOLLY",
        "BLUE BERRIES",
        "FORGET ME NOTS",
        "RYE STALK",
        "CATTAIL",
        "POPPY",
        "ORANGE POPPY",
        "CYAN POPPY",
        "WHITE POPPY",
        "PINK POPPY",
        "BLUEBELLS",
        "LILY OF THE VALLEY",
        "SNAPDRAGON",
        "HERBS",
        "PETALS",
        "NETTLE",
        "HEATHER",
        "GORSE",
        "JUNIPER",
        "RASPBERRY",
        "LAVENDER",
        "OAK LEAVES",
        "CATMINT",
        "MAPLE SEED",
        "LAUREL",
        "BULB WHITE",
        "BULB YELLOW",
        "BULB ORANGE",
        "BULB PINK",
        "BULB BLUE",
        "CLOVERTAIL",
        "DAISYTAIL",
        "DRY HERBS",
        "DRY CATMINT",
        "DRY NETTLES",
        "DRY LAURELS",
        "WISTERIA2",
        "ROSE MALLOW",
        "PICKLEWEED",
        "GOLDEN CREEPING JENNY",
        "DESERT WILLOW",
        "CACTUS FLOWER",
        "PRAIRIE FIRE",
        "VERBENA EAR",
        "VERBENA PELT",
    ]

    wild_accessories = [
        "RED FEATHERS",
        "BLUE FEATHERS",
        "JAY FEATHERS",
        "GULL FEATHERS",
        "SPARROW FEATHERS",
        "MOTH WINGS",
        "ROSY MOTH WINGS",
        "MORPHO BUTTERFLY",
        "MONARCH BUTTERFLY1",
        "CICADA WINGS",
        "BLACK CICADA",
        "ROAD RUNNER FEATHER",
    ]
    
    bows_accessories = ["CRIMSONBOWS", "BLUEBOWS", "YELLOWBOWS", "CYANBOWS", "REDBOWS", "LIMEBOWS", "GREENBOWS",
                        "RAINBOWBOWS", "BLACKBOWS", "SPIKESBOWS", "WHITEBOWS", "PINKBOWS", "PURPLEBOWS", "MULTIBOWS",
                        "INDIGOBOWS"]
    
    ster_accessories = ["POPPYFLOWER", "JUNIPERBERRY", "DAISYFLOWER", "BORAGEFLOWER", "OAK", "BEECH", "LAURELLEAVES",
                        "COLTSFOOT", "BINDWEED", "TORMENTIL", "BRIGHTEYE", "LAVENDERWREATH", "YARROW"]
    
    beetle_accessories = ["FROG FRIEND", "MOUSE FRIEND", "BUNNY HAT", "SMILEY HAT", "PARTY HAT", "SANTA HAT",
                          "STICK FRIEND", "BAT WING SUIT", "PINK BOWTIE", "GRAY BOWTIE", "PINK SCARF",
                          "BLUETAILED SKINK", "BLACKHEADED ORIOLE", "MILKSNAKE", "WORM FRIEND"]

    beetle_feathers = ["THRUSH FEATHERS", "GOLDFINCH FEATHERS", "DOVE FEATHERS", "PEACOCK FEATHERS", "HAWK FEATHERS",
                       "BLUE JAY FEATHERS", "ROBIN FEATHERS", "FIERY FEATHERS", "SUNSET FEATHERS", "SILVER FEATHERS"]
    # dad accessories
    toy_accessories = ["BALL", "MOUSE", "BONE"]

    blankie_accessories = ["MOSSBLANKIE"]

    flag_accessories = ["AUTISMFLAG", "DISFLAG", "ZEBFLAG"]

    booties = [
        "CRIMSONBOOT", "BLUEBOOT", "YELLOWBOOT", "CYANBOOT", "REDBOOT", "LIMEBOOT", "GREENBOOT", "RAINBOWBOOT",
        "BLACKBOOT", "BROWNBOOT", "WHITEBOOT", "PINKBOOT", "PURPLEBOOT", "MULTIBOOT", "INDIGOBOOT"
    ]

    wheels = ["WHEELS"]
    
    collars = [
        "CRIMSON",
        "BLUE",
        "YELLOW",
        "CYAN",
        "RED",
        "LIME",
        "GREEN",
        "RAINBOW",
        "BLACK",
        "SPIKES",
        "WHITE",
        "PINK",
        "PURPLE",
        "MULTI",
        "INDIGO",
        "CRIMSONBELL",
        "BLUEBELL",
        "YELLOWBELL",
        "CYANBELL",
        "REDBELL",
        "LIMEBELL",
        "GREENBELL",
        "RAINBOWBELL",
        "BLACKBELL",
        "SPIKESBELL",
        "WHITEBELL",
        "PINKBELL",
        "PURPLEBELL",
        "MULTIBELL",
        "INDIGOBELL",
        "CRIMSONBOW",
        "BLUEBOW",
        "YELLOWBOW",
        "CYANBOW",
        "REDBOW",
        "LIMEBOW",
        "GREENBOW",
        "RAINBOWBOW",
        "BLACKBOW",
        "SPIKESBOW",
        "WHITEBOW",
        "PINKBOW",
        "PURPLEBOW",
        "MULTIBOW",
        "INDIGOBOW",
        "CRIMSONNYLON",
        "BLUENYLON",
        "YELLOWNYLON",
        "CYANNYLON",
        "REDNYLON",
        "LIMENYLON",
        "GREENNYLON",
        "RAINBOWNYLON",
        "BLACKNYLON",
        "SPIKESNYLON",
        "WHITENYLON",
        "PINKNYLON",
        "PURPLENYLON",
        "MULTINYLON",
        "INDIGONYLON",
        "CRIMSONBANDANA",
        "BLUEBANDANA",
        "YELLOWBANDANA",
        "CYANBANDANA",
        "REDBANDANA",
        "LIMEBANDANA",
        "GREENBANDANA",
        "RAINBOWBANDANA",
        "BLACKBANDANA",
        "SPIKESBANDANA",
        "WHITEBANDANA",
        "PINKBANDANA",
        "PURPLEBANDANA",
        "MULTIBANDANA",
        "INDIGOBANDANA",
        "CRIMSONTEETHCOLLAR",
        "BLUETEETHCOLLAR",
        "YELLOWTEETHCOLLAR",
        "CYANTEETHCOLLAR",
        "REDTEETHCOLLAR",
        "LIMETEETHCOLLAR",
        "GREENTEETHCOLLAR",
        "RAINBOWTEETHCOLLAR",
        "BLACKTEETHCOLLAR",
        "SPIKESTEETHCOLLAR",
        "WHITETEETHCOLLAR",
        "PINKTEETHCOLLAR",
        "PURPLETEETHCOLLAR",
        "MULTITEETHCOLLAR",
        "INDIGOTEETHCOLLAR",
        "CRIMSONTIE",
        "BLUETIE",
        "YELLOWTIE",
        "CYANTIE",
        "ORANGETIE",
        "LIMETIE",
        "GREENTIE",
        "RAINBOWTIE",
        "BLACKTIE",
        "SPIKESTIE",
        "WHITETIE",
        "PINKTIE",
        "PURPLETIE",
        "MULTITIE",
        "INDIGOTIE",
        "CRIMSONS",
        "BLUES",
        "YELLOWS",
        "CYANS",
        "ORANGES",
        "LIMES",
        "GREENS",
        "RAINBOWS",
        "BLACKS",
        "SPIKESS",
        "WHITES",
        "PINKS",
        "PURPLES",
        "MULTIS",
        "INDIGOS",
        "CRIMSONH",
        "BLUEH",
        "YELLOWH",
        "CYANH",
        "REDH",
        "LIMEH",
        "GREENH",
        "RAINBOWH",
        "BLACKH",
        "SPIKESH",
        "WHITEH",
        "PINKH",
        "PURPLEH",
        "MULTIH",
        "INDIGOH",
        "CRIMSONBOO",
        "MAGENTABOO",
        "PINKBOO",
        "BLOODORANGEBOO",
        "ORANGEBOO",
        "YELLOWBOO",
        "LIMEBOO",
        "DARKGREENBOO",
        "GREENBOO",
        "TEALBOO",
        "LIGHTBLUEBOO",
        "BLUEBOO",
        "DARKBLUEBOO",
        "LIGHTPURPLEBOO",
        "DARKPURPLEBOO",
        "VIBRANTPURPLEBOO",
        "PINKREDBOO",
        "WHITEBOO",
        "LIGHTGRAYBOO",
        "GRAYBOO",
        "BROWNBOO",
        "BLACKBOO",
        
    ]

    # this is used for acc-giving events, only change if you're adding a new category tag to the event filter
    # adding a category here will automatically update the event editor's options
    acc_categories = {
        "PLANT": plant_accessories,
        "WILD": wild_accessories,
        "COLLAR": collars,
    }

    neckerchiefs = ["WHITE NECKERCHIEF", "BABYBLUE NECKERCHIEF", "LIGHTPURPLE NECKERCHIEF", "BLUE NECKERCHIEF",
                    "PURPLE NECKERCHIEF", "DARKPURPLE NECKERCHIEF", "LIGHTPINK NECKERCHIEF", "LIGHTYELLOW NECKERCHIEF",
                    "PINK NECKERCHIEF", "ORANGE NECKERCHIEF", "RED NECKERCHIEF", "CYAN NECKERCHIEF",
                    "YELLOWGREEN NECKERCHIEF", "TURQUOISE NECKERCHIEF", "GREEN NECKERCHIEF"]

    witchhats = ["WHITE WITCHHAT", "BABYBLUE WITCHHAT", "LIGHTPURPLE WITCHHAT", "BLUE WITCHHAT", "PURPLE WITCHHAT",
                 "DARKPURPLE WITCHHAT", "LIGHTPINK WITCHHAT", "LIGHTYELLOW WITCHHAT", "PINK WITCHHAT",
                 "ORANGE WITCHHAT", "RED WITCHHAT", "CYAN WITCHHAT", "YELLOWGREEN WITCHHAT", "TURQUOISE WITCHHAT",
                 "GREEN WITCHHAT"]

    randomaccessories = ["DOGWOOD", "TREESTAR", "RACCOON LEAF", "WHITE RACCOON LEAF", "CHERRY BLOSSOM", "DAISY BLOOM",
                         "FEATHERS", "RED ROSE", "WHITE ROSE", "PEBBLE", "PEBBLE COLLECTION", "GOLDEN FLOWER",
                         "DANDELIONS", "DANDELION PUFFS", "DICE", "GOLDEN EARRINGS"]

    flower_accessories = ["DAISY", "DIANTHUS", "BLEEDING HEARTS", "FRANGIPANI", "BLUE GLORY", "CATNIP FLOWER",
                          "BLANKET FLOWER", "ALLIUM", "LACELEAF", "PURPLE GLORY", "YELLOW PRIMROSE", "HESPERIS",
                          "MARIGOLD", "WISTERIA"]

    plant2_accessories = ["CLOVER", "STICK", "PUMPKIN", "MOSS", "IVY", "ACORN", "MOSS PELT", "REEDS", "BAMBOO"]

    snake_accessories = ["GRASS SNAKE", "BLUE RACER", "WESTERN COACHWHIP", "KINGSNAKE"]

    smallAnimal_accessories = ["GRAY SQUIRREL", "RED SQUIRREL", "CRAB", "WHITE RABBIT", "BLACK RABBIT", "BROWN RABBIT",
                               "INDIAN GIANT SQUIRREL", "FAWN RABBIT", "BROWN AND WHITE RABBIT",
                               "BLACK AND WHITE RABBIT", "WHITE AND FAWN RABBIT", "BLACK VITILIGO RABBIT",
                               "BROWN VITILIGO RABBIT", "FAWN VITILIGO RABBIT", "BLACKBIRD", "ROBIN", "JAY", "THRUSH",
                               "CARDINAL", "MAGPIE", "CUBAN TROGON", "TAN RABBIT", "TAN AND WHITE RABBIT",
                               "TAN VITILIGO RABBIT", "RAT", "WHITE MOUSE", "BLACK MOUSE", "GRAY MOUSE", "BROWN MOUSE",
                               "GRAY RABBIT", "GRAY AND WHITE RABBIT", "GRAY VITILIGO RABBIT"]

    deadInsect_accessories = ["LUNAR MOTH", "ROSY MAPLE MOTH", "OGMONARCH BUTTERFLY", "DAPPLED MONARCH",
                              "POLYPHEMUS MOTH", "MINT MOTH"]

    aliveInsect_accessories = ["BROWN SNAIL", "RED SNAIL", "WORM", "BLUE SNAIL", "ZEBRA ISOPOD", "DUCKY ISOPOD",
                               "DAIRY COW ISOPOD", "BEETLEJUICE ISOPOD", "BEE", "RED LADYBUG", "ORANGE LADYBUG",
                               "YELLOW LADYBUG"]

    fruit_accessories = ["OGRASPBERRY", "BLACKBERRY", "GOLDEN RASPBERRY", "CHERRY", "YEW"]

    sailormoon = ["MOON", "MERCURY", "MARS", "JUPITER", "VENUS", "TUXEDO MASK", "URANUS", "NEPTUNE", "PLUTO", "SATURN",
                  "MINI MOON", "CRYSTAL BALL"]

    crafted_accessories = ["WILLOWBARK BAG", "CLAY DAISY POT", "CLAY AMANITA POT", "CLAY BROWNCAP POT", "BIRD SKULL",
                           "LEAF BOW"]

    tail2_accessories = ["SEAWEED", "DAISY CORSAGE"]

    chime_accessories = ["SILVER MOON", "GOLD STAR", "GOLD MOON", "MOON AND STARS"]

    lantern_accessories = ["LANTERN"]

    colorsplash_accessories = ["CSYELLOWHORN", "CSORANGEHORN", "CSGREENHORN", "CSFROSTHORN", "CSSILVERHORN",
                               "CSCYANHORN", "CSMAROONHORN", "CSVIOLETHORN", "CSINDIGOHORN", "CSBLUEHORN",
                               "CSBLACKHORN", "CSLIMEHORN", "CSGOLDHORN", "CSMOSSHORN", "CSBROWNHORN",
                               "CSYELLOWKITSUNE", "CSORANGEKITSUNE", "CSGREENKITSUNE", "CSFROSTKITSUNE",
                               "CSSILVERKITSUNE", "CSCYANKITSUNE", "CSMAROONKITSUNE", "CSVIOLETKITSUNE",
                               "CSINDIGOKITSUNE", "CSBLUEKITSUNE", "CSBLACKKITSUNE", "CSLIMEKITSUNE", "CSGOLDKITSUNE",
                               "CSMOSSKITSUNE", "CSBROWNKITSUNE", "CSYELLOWMERMAID", "CSORANGEMERMAID",
                               "CSGREENMERMAID", "CSFROSTMERMAID", "CSSILVERMERMAID", "CSCYANMERMAID",
                               "CSMAROONMERMAID", "CSVIOLETMERMAID", "CSINDIGOMERMAID", "CSBLUEMERMAID",
                               "CSBLACKMERMAID", "CSLIMEMERMAID", "CSGOLDMERMAID", "CSMOSSMERMAID", "CSBROWNMERMAID"]

    pokemon_accessories = ["PIKACHU", "SQUIRTLE", "CHARMANDER", "SPHEAL", "GROWLITHE", "BULBASAUR", "SENTRET",
                           "SHAYMIN", "EMOLGA", "HISUI GROWLITHE", "ALOLAN VULPIX", "VULPIX", "LUXRAY", "ALTARIA",
                           "AZUMARILL"]

    tail_accessories = [
        "RED FEATHERS",
        "BLUE FEATHERS",
        "JAY FEATHERS",
        "GULL FEATHERS",
        "SPARROW FEATHERS",
        "CLOVERTAIL",
        "DAISYTAIL",
        "DAISY CORSAGE",
        "CLOVERTAIL",
        "OLD SILVER WATCH",
        "OLD GOLD WATCH",
        "BAUBLES",
        "DOGWOOD",
        "TREESTAR",
        "SEAWEED",
        "CRIMSONBOWS",
        "BLUEBOWS",
        "YELLOWBOWS",
        "CYANBOWS",
        "REDBOWS",
        "LIMEBOWS",
        "GREENBOWS",
        "RAINBOWBOWS",
        "BLACKBOWS",
        "SPIKESBOWS",
        "WHITEBOWS",
        "PINKBOWS",
        "PURPLEBOWS",
        "MULTIBOWS",
        "INDIGOBOWS",
        "THRUSH FEATHERS",
        "GOLDFINCH FEATHERS",
        "DOVE FEATHERS",
        "PEACOCK FEATHERS",
        "HAWK FEATHERS",
        "BLUE JAY FEATHERS",
        "ROBIN FEATHERS",
        "FIERY FEATHERS",
        "SUNSET FEATHERS",
        "SILVER FEATHERS",
        "WISTERIA2",
        "GOLDEN CREEPING JENNY",
    ]

    head_accessories = [
        "MOTH WINGS",
        "ROSY MOTH WINGS",
        "MORPHO BUTTERFLY",
        "MONARCH BUTTERFLY",
        "CICADA WINGS",
        "BLACK CICADA",
        "MAPLE LEAF",
        "HOLLY",
        "BLUE BERRIES",
        "FORGET ME NOTS",
        "RYE STALK",
        "CATTAIL",
        "POPPY",
        "ORANGE POPPY",
        "CYAN POPPY",
        "WHITE POPPY",
        "PINK POPPY",
        "BLUEBELLS",
        "LILY OF THE VALLEY",
        "SNAPDRAGON",
        "BUNNY HAT",
        "SMILEY HAT",
        "PARTY HAT",
        "SANTA HAT",
        "STICK FRIEND",
        "PINK SCARF",
        "BLUETAILED SKINK",
        "BLACKHEADED ORIOLE",
        "MILKSNAKE",
        "WORM FRIEND",
        "NETTLE",
        "HEATHER",
        "GORSE",
        "JUNIPER",
        "RASPBERRY",
        "LAVENDER",
        "OAK LEAVES",
        "CATMINT",
        "MAPLE SEED",
        "LAUREL",
        "BULB WHITE",
        "BULB YELLOW",
        "BULB ORANGE",
        "BULB PINK",
        "BULB BLUE",
        "DRY CATMINT",
        "DRY NETTLES",
        "DRY LAURELS",
        "ROSE MALLOW",
        "PICKLEWEED",
        "DESERT WILLOW",
        "CACTUS FLOWER",
        "PRAIRIE FIRE",
        "VERBENA EAR",
        "RAT SKULL",
        "FISH BONES",
        "PEACOCK BUTTERFLY",
        "DEATH HEAD HAWKMOTH",
        "GARDEN TIGER MOTH",
        "ATLAS MOTH",
        "CECOROPIA MOTH",
        "WHITE ERMINE MOTH",
        "IO MOTH",
        "COMET MOTH",
        "JADE HAWKMOTH",
        "HUMMINGBIRD HAWKMOTH",
        "OWL BUTTERFLY",
        "GLASSWING BUTTERFLY",
        "QUEEN ALEXANDRA BIRDWING BUTTERFLY",
        "GREEN DRAGONTAIL BUTTERFLY",
        "MENELAUS BLUE MORPHO BUTTERFLY",
        "DEAD LEAF BUTTERFLY",
        "DVD",
        "OLD PENCIL",
        "OLD BRUSH",
        "BANANA PEEL",
        "BROKEN VHS TAPE",
        "CLOVER",
        "STICK",
        "MOSS",
        "IVY",
        "ACORN",
        "OGMONARCH BUTTERFLY",
        "DAISY",
        "DIANTHUS",
        "BLEEDING HEARTS",
        "FRANGIPANI",
        "BLUE GLORY",
        "CATNIP FLOWER",
        "BLANKET FLOWER",
        "ALLIUM",
        "LACELEAF",
        "PURPLE GLORY",
        "YELLOW PRIMROSE",
        "MARIGOLD",
        "WISTERIA",
        "GRAY SQUIRREL",
        "RED SQUIRREL",
        "CRAB",
        "WORM",
        "OGRASPBERRY",
        "BLACKBERRY",
        "GOLDEN RASPBERRY",
        "CHERRY",
        "YEW",
        "BIRD SKULL",
        "LEAF BOW",
        "LUNAR MOTH",
        "DAPPLED MONARCH",
        "POLYPHEMUS MOTH",
        "MINT MOTH",
        "ROSY MAPLE MOTH",
        "POPPYFLOWER",
        "JUNIPERBERRY",
        "DAISYFLOWER",
        "BORAGEFLOWER",
        "OAK",
        "BEECH",
        "LAURELLEAVES",
        "COLTSFOOT",
        "BINDWEED",
        "TORMENTIL",
        "BRIGHTEYE",
        "LAVENDERWREATH",
        "YARROW",
        "MOON",
        "MERCURY",
        "MARS",
        "JUPITER",
        "VENUS",
        "URANUS",
        "NEPTUNE",
        "PLUTO",
        "SATURN",
        "MINI MOON",
        "CHERRY BLOSSOM",
        "DAISY BLOOM",
        "PEBBLE", 
        "GOLDEN FLOWER",
        "DANDELIONS",
        "DANDELION PUFFS",
        "DICE",
        "GOLDEN EARRINGS",
        "SILVER MOON",
        "GOLD STAR",
        "GOLD MOON",
        "MOON AND STARS",
        "WHITE WITCHHAT",
        "BABYBLUE WITCHHAT",
        "LIGHTPURPLE WITCHHAT",
        "BLUE WITCHHAT",
        "PURPLE WITCHHAT",
        "DARKPURPLE WITCHHAT",
        "LIGHTPINK WITCHHAT",
        "LIGHTYELLOW WITCHHAT",
        "PINK WITCHHAT",
        "ORANGE WITCHHAT",
        "RED WITCHHAT",
        "CYAN WITCHHAT",
        "YELLOWGREEN WITCHHAT",
        "TURQUOISE WITCHHAT",
        "GREEN WITCHHAT",
    ]

    body_accessories = [
        "HERBS",
        "PETALS",
        "DRY HERBS",
        "VERBENA PELT",
        "ROAD RUNNER FEATHER",
        "RED ROSE",
        "WHITE ROSE",
        "PEBBLE COLLECTION",
        "FEATHERS",
        "SNAKE",
        "RIBS",
        "BAT WINGS",
        "CANIDAE SKULL",
        "DEER ANTLERS",
        "RAM HORN",
        "GOAT HORN",
        "OX SKULL",
        "TEETH COLLAR",
        "BIRD SKULL1",
        "ROE SKULL",
        "GOLDEN KEY",
        "SILVER KEY",
        "OLD NEWSPAPER",
        "SEA GLASS",
        "MUD AND DIRT",
        "PUMPKIN",
        "MOSS PELT",
        "REEDS",
        "BAMBOO",
        "BAT WING SUIT",
        "PINK BOWTIE",
        "GRAY BOWTIE",
        "FROG FRIEND",
        "MOUSE FRIEND",
        "HESPERIS",
        "GRASS SNAKE",
        "BLUE RACER",
        "WESTERN COACHWHIP",
        "KINGSNAKE",
        "WHITE RABBIT",
        "BLACK RABBIT",
        "BROWN RABBIT",
        "INDIAN GIANT SQUIRREL",
        "FAWN RABBIT",
        "BROWN AND WHITE RABBIT",
        "BLACK AND WHITE RABBIT",
        "WHITE AND FAWN RABBIT",
        "BLACK VITILIGO RABBIT",
        "BROWN VITILIGO RABBIT",
        "FAWN VITILIGO RABBIT",
        "BLACKBIRD",
        "ROBIN",
        "JAY",
        "THRUSH",
        "CARDINAL",
        "MAGPIE",
        "CUBAN TROGON",
        "TAN RABBIT",
        "TAN AND WHITE RABBIT",
        "TAN VITILIGO RABBIT",
        "RAT", "WHITE MOUSE",
        "BLACK MOUSE",
        "GRAY MOUSE",
        "BROWN MOUSE",
        "GRAY RABBIT",
        "GRAY AND WHITE RABBIT",
        "GRAY VITILIGO RABBIT",
        "BROWN SNAIL",
        "RED SNAIL",
        "BLUE SNAIL",
        "ZEBRA ISOPOD",
        "DUCKY ISOPOD",
        "DAIRY COW ISOPOD",
        "BEETLEJUICE ISOPOD",
        "BEE",
        "RED LADYBUG",
        "ORANGE LADYBUG",
        "YELLOW LADYBUG",
        "WILLOWBARK BAG",
        "CLAY DAISY POT",
        "CLAY AMANITA POT",
        "CLAY BROWNCAP POT",
        "CRYSTAL BALL",
        "TUXEDO MASK",
        "RACCOON LEAF",
        "WHITE RACCOON LEAF",
        "LANTERN",
        "WHEELS",
        "BALL",
        "MOUSE",
        "BONE",
        "MOSSBLANKIE",
        "AUTISMFLAG",
        "DISFLAG",
        "ZEBFLAG",
        "CRIMSONBOOT",
        "BLUEBOOT",
        "YELLOWBOOT",
        "CYANBOOT",
        "REDBOOT",
        "LIMEBOOT",
        "GREENBOOT",
        "RAINBOWBOOT",
        "BLACKBOOT",
        "BROWNBOOT",
        "WHITEBOOT",
        "PINKBOOT",
        "PURPLEBOOT",
        "MULTIBOOT",
        "INDIGOBOOT",
        "WHITE NECKERCHIEF",
        "BABYBLUE NECKERCHIEF",
        "LIGHTPURPLE NECKERCHIEF",
        "BLUE NECKERCHIEF",
        "PURPLE NECKERCHIEF",
        "DARKPURPLE NECKERCHIEF",
        "LIGHTPINK NECKERCHIEF",
        "LIGHTYELLOW NECKERCHIEF",
        "PINK NECKERCHIEF",
        "ORANGE NECKERCHIEF",
        "RED NECKERCHIEF",
        "CYAN NECKERCHIEF",
        "YELLOWGREEN NECKERCHIEF",
        "TURQUOISE NECKERCHIEF",
        "GREEN NECKERCHIEF",
        "PIKACHU",
        "SQUIRTLE",
        "CHARMANDER",
        "SPHEAL",
        "GROWLITHE",
        "BULBASAUR",
        "SENTRET",
        "SHAYMIN",
        "EMOLGA",
        "HISUI GROWLITHE",
        "ALOLAN VULPIX",
        "VULPIX",
        "LUXRAY",
        "ALTARIA",
        "AZUMARILL",
    ]

    # double base game pelts bc more colors
    tabbies = [
        "Tabby", "Ticked", "Mackerel", "Classic", "Sokoke", "Agouti",
        "Tabby", "Ticked", "Mackerel", "Classic", "Sokoke", "Agouti",
        "Royal", "Brindle", "GhostTabby", "PinstripeTabby", "Caliisokoke", "Circletabby", "Birchtabby"
    ]
    spotted = [
        "Speckled", "Rosette",
        "Speckled", "Rosette",
        "Lynx", "Bobcat", "Spots", "Merle", "Dot", "Caliispeckled", "Dotfade"
    ]
    plain = [
        "SingleColour", "Smoke", "Singlestripe",
        "SingleColour", "Smoke", "Singlestripe",
        "Smokepoint", "Doberman", "Stain", "Colourpoint"
    ]
    exotic = [
        "Bengal", "Marbled", "Masked",
        "Bengal", "Marbled", "Masked",
        "Maned", "Ocelot", "Cheetah", "Wildcat", "Wolf", "Finleappatches", "Dalmatian", "Abyssinian", "Clouded",
        "Snowflake", "Oceloid", "Monarch", "Kintsugi", "Lynxpoint", "Ncrestedcaracara"
    ]
    torties = [
        "Tortie", "Calico"
    ]
    magic = [
        "PrideAgouti", "PrideBengal", "PrideClassic", "PrideMackerel"
    ]

    pelt_categories = [tabbies, spotted, plain, exotic, magic, torties]

    # SPRITE NAMES
    single_colours = [
        "WHITE", "PALEGREY", "SILVER", "GREY", "DARKGREY", "GHOST", "BLACK", "CREAM", "PALEGINGER", "GOLDEN", "GINGER",
        "DARKGINGER", "SIENNA", "LIGHTBROWN", "LILAC", "BROWN", "GOLDEN-BROWN", "DARKBROWN", "CHOCOLATE",
        # minecraft
        "ACACIALOG", "BAMBOO", "BIRCHLOG", "CHERRYLOG", "CRIMSONSTEM", "DARKOAKLOG", "JUNGLELOG", "MANGROVELOG",
        "OAKLOG", "SPRUCELOG", "WARPEDSTEM", "ACACIAPLANKS", "BAMBOOPLANKS", "BIRCHPLANKS", "CHERRYPLANKS",
        "CRIMSONPLANKS", "DARKOAKPLANKS", "JUNGLEPLANKS", "MANGROVEPLANKS", "OAKPLANKS", "SPRUCEPLANKS", "WARPEDPLANKS",
        "AMETHYST", "BLACKGLAZEDTERRACOTTA", "BLUEGLAZEDTERRACOTTA", "BROWNGLAZEDTERRACOTTA", "BROWN MUSHROOM",
        "COPPER", "CRYING OBSIDIAN", "CYANGLAZEDTERRACOTTA", "EXPOSEDCOPPER", "GRAYGLAZEDTERRACOTTA",
        "GREENGLAZEDTERRACOTTA", "LIGHTBLUEGLAZED TERRACOTTA", "LIGHTGRAYGLAZEDTERRACOTTA", "LIMEGLAZEDTERRACOTTA",
        "MAGENTAGLAZEDTERRACOTTA", "MUSHROOMINSIDE", "MUSHROOMSTEM", "OBSIDIAN", "ORANGEGLAZEDTERRACOTTA",
        "OXIDIZEDCOPPER", "PINKGLAZEDTERRACOTTA", "PURPLEGLAZEDTERRACOTTA", "PURPUR", "QUARTZ", "REDGLAZEDTERRACOTTA",
        "REDMUSHROOM", "WEATHEREDCOPPER", "WHITEGLAZEDTERRACOTTA", "YELLOWGLAZEDTERRACOTTA",
        # anju
        "PINK", "RED", "LIGHTGREEN", "GREEN", "CYAN", "BLUE", "PURPLE",
        # dance
        "LIGHTCINNAMON", "CINNAMON", "SILVERFAWN", "DARKCINNAMON", "DARKFAWN", "FAWN", "LIGHTFAWN", "PALEFAWN",
        "PALECREAM", "LIGHTCREAM", "DANCECREAM", "DARKCREAM", "DARKGOLD", "GOLD", "LIGHTGOLD", "SILVERCREAM",
        "PALEGOLD", "SUNSHINE", "BRONZE",
        # mimi
        "COPPERMIMI", "DARKORANGE", "ORANGE", "LIGHTORANGE", "PALEORANGE", "PALEGINGERMIMI", "LIGHTGINGER",
        "GINGERMIMI", "DARKGINGERMIMI", "SILVERGOLD", "RUSSET", "DARKRED", "REDMIMI", "LIGHTRED", "PALERED",
        "SILVERMIMI", "SILVERGREY", "SILVERBLUE", "SILVERSLATE",
        # silly
        "LIGHTLILAC", "LILACSILLY", "DARKLILAC", "DARKASH", "ASH", "LIGHTASH", "PALEASH", "SILVERCINNAMON", "SILVERRED",
        "PALEBROWN", "LIGHTBROWNSILLY", "BROWNSILLY", "DARKBROWNSILLY", "EBONY", "DARKCHOCOLATE", "CHOCOLATESILLY",
        "LIGHTCHOCOLATE", "PALECHOCOLATE", "PALECINNAMON"
        # ster
        "WHITESTER", "PALEGREYSTER", "LIGHTGREY", "GREYSTER", "DARKGREYSTER", "BLACKSTER", "OBSIDIANSTER", "GHOSTSTER",
        "PALEBLUE", "LIGHTBLUE", "BLUESTER", "DARKBLUE", "SILVERCHOCOLATE", "SILVERORANGE", "DARKSLATE", "SLATE",
        "LIGHTSLATE", "PALESLATE", "PALELILAC",
        # colorsplash
        "LIGHTLIME", "PINKGREY", "YELLOWBROWN", "REDGREY", "BLUEBROWN", "GHOSTBROWN", "BLACKPURPLE", "BLUECREAM",
        "PALEPINKPURPLE", "ICEBLUE", "BLUECS2", "GREENBROWN", "NAVYBLUE", "PURPLECREAM", "INDIGOBLUSH", "VIOLETBLUSH",
        "MAGENTA", "NAVYBROWN", "MULBERRY", "ICEWHITE", "CRYSTAL", "ORCHID", "CERULEAN", "GRAPE", "GHOSTBLUE",
        "BLACKBLUE", "THISTLE", "SUNYELLOW", "BUBBLEGUM", "REDSTAIN", "ROSE", "DUSKBROWN", "FROZENSUN", "GREENGOLD",
        "OCEAN", "TEAL", "REDBLUE", "TREE"
        # heta rainbow cats
        "REDHETA", "ORANGEHETA", "YELLOWHETA", "NEONYELLOW", "NEONGREEN", "GREENHETA", "MINTGREEN", "DARKMINT",
        "NEONTEAL", "CYANHETA", "BLUEHETA", "NAVYHETA", "INDIGOHETA", "PURPLEHETA", "VIOLETHETA", "MAGENTAHETA",
        "PINKHETA", "SCARLETPINK", "DARKREDHETA",
        # hive
        "GREENH", "TEALH", "BLUEH", "NAVYH", "INDIGOH", "PURPLEH", "VIOLETH", "PINKH", "ROSEH", "DARKPINKH", "REDH",
        "ORANGEH", "GOLDH", "PASTELPURPLEH", "DARKGREENH", "BROWN-PURPLE", "YELLOWH", "DARKMOSS", "PURPLESWIRL"
        # kris
        "PINKCREAM", "BLUEMINT", "SUNSET", "PINK-BLUE", "INDIGOK", "BLUEGHOSTK", "PINKK", "PASTELPINKBLUE",
        "RUSTYGREEN", "OURPLE", "BLUE-YELLOW", "BLUE-PURPLE", "DARKSUNSET", "BANANABERRY", "BRIGHTBLUEK", "SUNRISE",
        "GREEN-NAVY", "PINKSHADOW", "REDK",
        # meteor
        "SILVERMETEOR", "SILVERNAVY", "CREAMSILVER", "GREYSTAR", "DARKGREYSTAR", "BLACK-BROWN", "BLUESPOTTED",
        "CREAMMETEOR", "PINK-WHITE", "TANSPOTTED", "REVERSESUN", "WARM-BLUE", "INDIGO-VIOLET", "GREYMETEOR",
        "ICESPOTTED", "SHADOW", "BLUE-EARTH", "EARTHSPOTTED", "BROWN-TAN",
        # pastel
        "PALEPINK-PURPLE", "PALEGREY-PINK", "PALEBLUE-YELLOW", "PALEMINT-PURPLE", "PALEGREEN-INDIGO",
        "PALEYELLOW-INDIGO", "PALEORANGE-BLUE", "PALEPURPLE-GOLD", "PALECYAN-GOLD", "PALEMINT-MAGENTA",
        "PALEMINT-VIOLET", "PALEGREEN-BLUE", "PALEGREEN-NAVY", "PALEBLUE-INDIGO", "PALECYAN-PURPLE", "PALECYAN-NAVY",
        "PALECYAN-BLUE", "PALEYELLOWGREEN", "PALEYELLOW-BLUE"
        # pepper
        "ICEPEPPER", "CYANPEPPER", "BLUEPEPPER", "OCEANPEPPER", "DARKBLUEPEPPER", "BLUEGHOSTPEPPER", "BLACKBLUEPEPPER",
        "GOLDCREAM", "GOLDPEPPER", "YELLOW-RED", "BRIGHTYELLOW-RED", "NEONRED", "REDBLACK", "PALEBLUE-GOLD",
        "INDIGOPEPPER", "RUSTBLUEPEPPER", "REDPEPPER", "REDBLUEBLACK", "SCARLETPEPPER"
        # sparkle
        "REDS", "RED-ORANGES", "DARKYELLOWS", "GREENREDS", "CYANPINKG", "INDIGOREDS", "REVERSERAINBOW", "PINKREDS",
        "RUSTYS", "GREENORANGES", "REDCYANS", "MINTBLUES", "BLACKBLUES", "BANANAS", "WHITEGREENS", "BROWNREDS",
        "RAINBOW", "GREENDARKREDS", "SUNNYS"
    ]

    # REALISTIC COLORS
    ginger_colours = ["CREAM", "PALEGINGER", "GOLDEN", "GINGER", "DARKGINGER", "SIENNA", "ACACIAPLANKS", "BIRCHPLANKS",
                      "COPPER", "REDGLAZEDTERRACOTTA", "SUNSHINE", "BRONZE", "LIGHTCREAM", "DANCECREAM", "DARKCREAM",
                      "DARKGOLD", "GOLD", "LIGHTGOLD", "PALEGOLD", "DARKORANGE", "ORANGE", "LIGHTORANGE", "PALEORANGE",
                      "PALEGINGERMIMI", "LIGHTGINGER", "GINGERMIMI", "DARKGINGERMIMI", "RUSSET", "DARKRED", "REDMIMI",
                      "LIGHTRED", "PALERED", "SILVERGOLD", "SILVERORANGE", "SILVERRED", "YELLOWBROWN", "BANANAS",
                      "CREAMSILVER"]

    black_colours = ["GREY", "DARKGREY", "GHOST", "BLACK", "ACACIALOG", "GRAYGLAZEDTERRACOTTA", "LIGHTGREY", "GREYSTER",
                     "DARKGREYSTER", "BLACKSTER", "OBSIDIANSTER", "GHOSTSTER", "LIGHTSLATE", "SLATE", "DARKSLATE",
                     "LIGHTBLUE", "BLUESTER", "DARKBLUE", "LIGHTLILAC", "LILACSILLY", "DARKLILAC", "DARKASH", "EBONY",
                     "BLACKPURPLE", "BLACKBLUE", "GREYSTAR", "DARKGREYSTAR", "GREYMETEOR"]

    white_colours = ["WHITE", "PALEGREY", "SILVER", "BIRCHLOG", "MUSHROOMSTEM", "QUARTZ", "WHITESTER", "PALEGREYSTER",
                     "PALESLATE", "PALEBLUE", "PALELILAC", "PALEASH", "PALEFAWN", "PALECREAM", "SILVERMIMI",
                     "SILVERGREY", "SILVERBLUE", "SILVERSLATE", "SILVERFAWN", "SILVERCREAM", "SILVERMETEOR"]

    brown_colours = ["LIGHTBROWN", "LILAC", "BROWN", "GOLDEN-BROWN", "DARKBROWN", "CHOCOLATE", "CHERRYLOG",
                     "DARKOAKLOG", "JUNGLELOG", "MANGROVELOG", "OAKLOG", "SPRUCELOG", "DARKOAKPLANKS", "JUNGLEPLANKS",
                     "OAKPLANKS", "SPRUCEPLANKS", "BROWN MUSHROOM", "MUSHROOMINSIDE", "LIGHTASH", "ASH", "PALEBROWN",
                     "LIGHTBROWNSILLY", "BROWNSILLY", "DARKBROWNSILLY", "DARKCHOCOLATE", "CHOCOLATESILLY",
                     "LIGHTCHOCOLATE", "PALECHOCOLATE", "LIGHTCINNAMON", "CINNAMON", "PALECINNAMON", "DARKCINNAMON",
                     "COPPERMIMI", "DARKFAWN", "FAWN", "LIGHTFAWN", "SILVERCHOCOLATE", "SILVERCINNAMON", "BLUEBROWN",
                     "GHOSTBROWN", "NAVYBROWN", "DUSKBROWN", "TANSPOTTED", "EARTHSPOTTED", "BROWN-TAN"]

    # FANTASY COLORS
    red_colors = ["PINK", "RED", "CRIMSONSTEM", "CHERRYPLANKS", "PINKGLAZEDTERRACOTTA", "REDMUSHROOM", "MANGROVEPLANKS",
                  "REDHETA", "PINKHETA", "SCARLETPINK", "DARKREDHETA", "PINKGREY", "REDGREY", "PALEPINKPURPLE",
                  "BUBBLEGUM", "REDSTAIN", "ROSE", "REDBLUE", "REDS", "RED-ORANGES", "PINKREDS", "RUSTYS", "REDCYANS",
                  "BROWNREDS", "NEONRED", "REDBLACK", "RUSTBLUEPEPPER", "REDPEPPER", "REDBLUEBLACK", "SCARLETPEPPER",
                  "PALEGREY-PINK", "PINK-WHITE", "PINKCREAM", "PINK-BLUE", "PINKK", "PASTELPINKBLUE", "PINKSHADOW",
                  "REDK", "PINKH", "ROSEH", "DARKPINKH", "REDH"]

    orange_colors = ["EXPOSEDCOPPER", "ORANGEGLAZEDTERRACOTTA", "ORANGEHETA", "PALEYELLOW-INDIGO", "PALEORANGE-BLUE",
                     "CREAMMETEOR", "REVERSESUN", "SUNSET", "OURPLE", "SUNRISE", "ORANGEH"]

    yellow_colors = ["BAMBOOPLANKS", "YELLOWGLAZEDTERRACOTTA", "YELLOWHETA", "NEONYELLOW", "SUNYELLOW", "FROZENSUN",
                     "DARKYELLOWS", "SUNNYS", "GOLDCREAM", "GOLDPEPPER", "YELLOW-RED", "BRIGHTYELLOW-RED",
                     "PALEYELLOWGREEN", "PALEYELLOW-BLUE", "PALEPURPLE-GOLD", "PALECYAN-GOLD", "PALEBLUE-YELLOW",
                     "BANANABERRY", "GOLDH", "YELLOWH"]

    green_colors = ["LIGHTGREEN", "GREEN", "BAMBOO", "WARPEDSTEM", "GREENGLAZEDTERRACOTTA", "LIMEGLAZEDTERRACOTTA",
                    "OXIDIZEDCOPPER", "WEATHEREDCOPPER", "NEONGREEN", "GREENHETA", "MINTGREEN", "DARKMINT", "LIGHTLIME",
                    "GREENBROWN", "GREENGOLD", "TREE", "GREENREDS", "GREENORANGES", "WHITEGREENS", "GREENDARKREDS",
                    "RUSTYGREEN", "GREEN-NAVY", "GREENH", "DARKGREENH", "DARKMOSS"]

    blue_colors = ["CYAN", "BLUE", "WARPEDPLANKS", "CYANGLAZEDTERRACOTTA", "LIGHTBLUEGLAZED TERRACOTTA",
                   "LIGHTGRAYGLAZEDTERRACOTTA", "WHITEGLAZEDTERRACOTTA", "BROWNGLAZEDTERRACOTTA", "NEONTEAL",
                   "CYANHETA", "BLUEHETA", "NAVYHETA", "BLUECREAM", "ICEBLUE", "CSBLUE2", "NAVYBLUE", "ICEWHITE",
                   "CERULEAN", "GHOSTBLUE", "OCEAN", "TEAL", "CYANPINKG", "MINTBLUES", "BLACKBLUES", "ICEPEPPER",
                   "CYANPEPPER", "BLUEPEPPER", "OCEANPEPPER", "DARKBLUEPEPPER", "BLUEGHOSTPEPPER", "PALEBLUE-GOLD",
                   "PALEBLUE-INDIGO", "PALECYAN-PURPLE", "PALECYAN-NAVY", "PALECYAN-BLUE", "SILVERNAVY", "BLACK-BROWN",
                   "BLUESPOTTED", "ICESPOTTED", "BLUE-EARTH", "BLUEMINT", "BLUEGHOSTK", "BLUE-YELLOW", "BLUE-PURPLE",
                   "BRIGHTBLUEK", "TEALH", "BLUEH", "NAVYH"]

    purple_colors = ["PURPLE", "CRIMSONPLANKS", "AMETHYST", "PURPLEGLAZEDTERRACOTTA", "PURPUR", "INDIGOHETA",
                     "PURPLEHETA", "VIOLETHETA", "MAGENTAHETA", "PURPLECREAM", "INDIGOBLUSH", "VIOLETBLUSH", "MAGENTA",
                     "MULBERRY", "GRAPE", "CRYSTAL", "ORCHID", "THISTLE", "INDIGOREDS", "INDIGOPEPPER",
                     "PALEMINT-MAGENTA", "PALEMINT-VIOLET", "PALEPINK-PURPLE", "PALEMINT-PURPLE", "PALEGREEN-INDIGO",
                     "WARM-BLUE", "INDIGO-VIOLET", "INDIGOK", "DARKSUNSET", "INDIGOH", "PURPLEH", "VIOLETH",
                     "PASTELPURPLEH", "BROWN-PURPLE", "PURPLESWIRL"]

    # not to be confused with black_coloUrs. ew british
    black_colors = ["BLACKGLAZEDTERRACOTTA", "CRYING OBSIDIAN", "OBSIDIAN", "REVERSERAINBOW", "RAINBOW",
                    "BLACKBLUEPEPPER", "SHADOW"]

    colour_categories = [ginger_colours, black_colours, white_colours, brown_colours, red_colors, orange_colors,
                         yellow_colors, green_colors, blue_colors, purple_colors, black_colors]

    eye_sprites = [
        "YELLOW", "AMBER", "HAZEL", "PALEGREEN", "GREEN", "BLUE", "DARKBLUE", "GREY", "CYAN", "EMERALD", "PALEBLUE",
        "PALEYELLOW", "GOLD", "HEATHERBLUE", "COPPER", "SAGE", "COBALT", "SUNLITICE", "GREENYELLOW", "BRONZE", "SILVER",
        "ROSE", "ALGAE", "SEAFOAM", "LIGHT FLAME", "CLOUDY", "RED", "TURQUOISE", "SWAMP", "RAINY", "AQUAMARINE",
        "EARTH", "PUMPKIN", "LILAC", "PERIWINKLE", "VIOLET", "POND", "DIRT", "BROWN", "CEDAR", "CHRISTMAS",
        "COTTON CANDY", "DARK PINE", "FALL", "FOREST FIRE", "GOLD MOON", "HALLOWEEN", "LOBELIA", "MIDNIGHT",
        "MOONSTONE", "OXIDIZED", "SNOW", "BERRY BANANA", "DAWN SKY", "TWILIGHT SKY", "WORMY", "BLUE HAZEL",
        "THUNDERBOLT", "VOLCANO", "SEASHELL", "PARADOX", "CURSE", "BLESSING", "VALENTINE", "FIREWORK", "LUCKY", "LIME",
        "PALE BROWN", "CRIMSON", "DARK HAZEL", "ROSE GOLD", "REVERSE SUNLITICE", "ICY", "SUNSET", "DARKBLUE",
        "LAVENDER", "ECLIPSE", "BLACK", "MUDDY", "DARK ROSE", "DARK TURQUOISE", "BLACKBERRY", "RUSTY", "PASTEL",
        "AVOCADO", "PASTEL LAVENDER", "BULLET", "LIGHT YELLOW", "SUNSHINE", "GOLD ORE", "FOSSILIZED AMBER", "DUSKY",
        "LICHEN", "SPRING", "TREE", "LEAVES", "EMERALD ORE", "HAZELNUT", "BLUE SKY", "OCEAN", "OVERCAST", "AQUA",
        "IRIS", "ROBIN", "GREY SILVER", "SAND", "MUSTARD", "BRONZE ORE", "TIMBER", "COPPER ORE", "FERN", "APPLE",
        "MOSS", "THICKET", "PEACOCK", "OLIVE", "STORMY BLUE", "DEPTHS", "STORMY", "TEAL", "INDIGO", "STEEL", "PEACH",
        "DAFFODIL", "MARIGOLD", "BRASS", "DARKAMBER", "DAWN SKIES", "MINT", "CHARTREUSE", "MEADOW", "LEAF",
        "LIGHT TURQUOISE", "SAP", "ALBINISTIC", "COBALT ORE", "RAIN", "CYAN DYE", "PERIWINKLE PURPLE", "ICY CRACK",
        "ALBINO", "WINTER ROSE", "PINK", "MORNING", "DARK BROWN", "BAY", "NEON GREEN", "SEA", "DISCORD", "ORANGE",
        "AUTUMN LEAF", "RUBY", "PHANTOM", "RIVER MOSS", "WICKED", "NEO FIRE", "NEO AMETHYST", "NEO LIME", "NEO VIOLET",
        "NEO SUN", "NEO TURQUOISE", "NEO YELLOW", "NEO SCARLET", "NEO PINKPURPLE", "NEO LIGHTBLUE", "NEO DARKBLUE",
        "NEO CYAN", "NEO YELLOWRED", "NEO PINK", "NEO INDIGO", "NEO PURPLE", "NEO YELLOWGREEN", "NEO ICEBLUE",
        "NEO PALEPINK", "NEO MINT", "NEO BLACKBLUE"
    ]
    little_white = [
        'LITTLE', 'LIGHTTUXEDO', 'BUZZARDFANG', 'TIP', 'BLAZE', 'BIB', 'VEE', 'PAWS', 'BELLY', 'TAILTIP', 'TOES',
        'BROKENBLAZE', 'LILTWO', 'SCOURGE', 'TOESTAIL', 'RAVENPAW', 'HONEY', 'LUNA', 'EXTRA', 'MUSTACHE',
        'REVERSEHEART', 'SPARKLE', 'RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'REVERSEEYE', 'BACKSPOT', 'EYEBAGS', 'LOCKET',
        'BLAZEMASK', 'TEARS',

        'MINKMINIMALONE', 'MINKMINIMALTWO', 'MINKMINIMALTHREE', 'MINKMINIMALFOUR', 'MINKMASK', 'MINKCHEST',
        'MINKSIDEMASK', 'MINKEMBER', 'MINKORIOLE', 'MINKONE', 'MINKDAPPLENIGHT', 'MINKSAFI',

        'SOLDIER', 'AKITA', 'FRECKLESTHREE', 'KITTY', 'ERAMASK', 'PAW', 'BOOMSTAR', 'LEGS', 'DOVE', 'CRESCENT',
        'SPIDERLEGS', 'APPEL', 'BODYSTRIPE', 'BLACKBODYSTRIPE', 'BROWNBODYSTRIPE', 'GINGERBODYSTRIPE',
        'SPRAYEDBODYSTRIPE', 'BLACKSPRAYEDBODYSTRIPE', 'BROWNSPRAYEDBODYSTRIPE', 'GINGERSPRAYEDBODYSTRIPE',
        'LITTLESTAR', 'SKULL', 'SIGHT', 'SHADOW', 'MOUSE', 'MOSS', 'BUMBLEBEE'
    ]
    mid_white = [
        'TUXEDO', 'FANCY', 'UNDERS', 'DAMIEN', 'SKUNK', 'MITAINE', 'SQUEAKS', 'STAR', 'WINGS', 'DIVA', 'SAVANNAH',
        'FADESPOTS', 'BEARD', 'DAPPLEPAW', 'TOPCOVER', 'WOODPECKER', 'MISS', 'BOWTIE', 'VEST', 'FADEBELLY', 'DIGIT',
        'FCTWO', 'FCONE', 'MIA', 'ROSINA', 'PRINCESS', 'DOUGIE',

        'MINKROSETAIL', 'MINKTWO', 'MINKFOUR', 'MINKREDTAIL', 'MINKSTREAK', 'MINKARMTAIL', 'MINKSTREAMSTRIKE',
        'MINKDAUB', 'MINKBRIE', 'MINKROBIN', 'MINKBLANKET', 'MINKBELOVED', 'MINKHEARTBEAT', 'MINKCHIMERA', 'MINKEYEDOT',
        'MINKSHILOH',

        'INK', 'GEM', 'FOX', 'ORCA', 'MOJO', 'HALFHEART', 'LEON', 'MEADOW', 'BAMBI', 'SKUNKSTRIPE', 'BANAN',
        'MOONSTONE', 'WINGTWO', 'STARBORN', 'RUG', 'CHAOSONE', 'STRIPES', 'PINITO', 'SNOW', 'KINTSUGIONE', 'RAIN',
        'MGLA', 'SATURN', 'PATTERN', 'MONKEY', 'CLASSICTORNIE', 'GRAFFITI', 'AGOUTITORIE', 'MORRO', 'DOG', 'ONESPOT'
    ]
    high_white = [
        'ANY', 'ANYTWO', 'BROKEN', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO', 'GOATEE', 'PRINCE', 'FAROFA',
        'MISTER', 'PANTS', 'REVERSEPANTS', 'HALFWHITE', 'APPALOOSA', 'PIEBALD', 'CURVED', 'GLASS', 'MASKMANTLE', 'MAO',
        'PAINTED', 'SHIBAINU', 'OWL', 'BUB', 'SPARROW', 'TRIXIE', 'SAMMY', 'FRONT', 'BLOSSOMSTEP', 'BULLSEYE', 'FINN',
        'SCAR', 'BUSTER', 'HAWKBLAZE', 'CAKE',

        'MINKTHREE', 'MINKOREO', 'MINKGRUMPYFACE', 'MINKPACMAN', 'MINKPAIGE', 'MINKMOTTLED', 'MINKDELILAH',

        'CHITAL', 'WOLF', 'PINTO', 'CHESSBORAD', 'SUNRISE', 'HUSKY', 'S', 'STATNTHREE', 'MIST', 'LADY', 'ERAHALF',
        'SUN', 'PINTOTWO', 'SKY', 'TIGERBODYSTRIPE', 'BLACKTIGERBODYSTRIPE', 'BROWNTIGERBODYSTRIPE',
        'GINGERTIGERBODYSTRIPE', 'CHAOSTWO', 'CHAOSFOUR', 'MASKTORITE', 'TANBUNNY', 'ROSETTESTORITE', 'BENGALMASK',
        'MOONLIGHT', 'MARBLETORINE', 'KINTSUGITWO', 'STORM', 'BENGALTORITE', 'TABBYTORITE', 'SOKKOKETORITE',
        'SPECKLEDTORITE'
    ]
    mostly_white = [
        'VAN', 'ONEEAR', 'LIGHTSONG', 'TAIL', 'HEART', 'MOORISH', 'APRON', 'CAPSADDLE', 'CHESTSPECK', 'BLACKSTAR',
        'PETAL', 'HEARTTWO', 'PEBBLESHINE', 'BOOTS', 'COW', 'COWTWO', 'LOVEBUG', 'SHOOTINGSTAR', 'EYESPOT', 'PEBBLE',
        'TAILTWO', 'BUDDY', 'KROPKA',

        'MINKHALF', 'MINKBANDANA', 'MINKSWOOP',

        'BUNNY', 'STAINSONE', 'STAINST', 'SWIFTPAW', 'DRIP', 'PRIMITVE', 'KARAPATITWO', 'CHAOS', 'MOSCOW', 'PANDA',
        'LUCKY',  'REVERSEBODYSPRITE', 'BLACKREVERSEBODYSPRITE', 'BROWNREVERSEBODYSPRITE', 'GINGERREVERSEBODYSPRITE',
        'REVERSETIGERBODYSPRITE', 'BLACKREVERSETIGERBODYSPRITE', 'BROWNREVERSETIGERBODYSPRITE',
        'GINGERREVERSETIGERBODYSPRITE', 'REVERSELEOPARDBODYSPRITE', 'BLACKREVERSELEOPARDBODYSPRITE',
        'BROWNREVERSELEOPARDBODYSPRITE', 'GINGERREVERSELEOPARDBODYSPRITE', 'CHAOSTHREE', 'ERROR', 'WAVE',
        'BRINDLETORITE', 'PONINTTORITE', 'MACKERELTORITE'
    ]
    point_markings = [
        'COLOURPOINT', 'RAGDOLL', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT',

        'MINKSMOKE', 'MINKBODY',

        'ANT', 'CAPETOWN', 'SNOWSHOE', 'ETERNAL'
    ]
    vit = [
        'VITILIGO', 'VITILIGOTWO', 'MOON', 'PHANTOM', 'KARPATI', 'POWDER', 'BLEACHED', 'SMOKEY',

        'MINKBRINDLE', 'MINKFRECKLED', 'MINKSMUDGED',

        'JACKAL', 'EYEV', 'FRECKLESTWO', 'CREAMV', 'SALT', 'NEPTUNE', 'AMBERONE', 'AMBERTWO', 'STRIPEONETORITE',
        'AMBERTHREE', 'SHADE', 'TICKEDTORIE', 'AMBERFOUR'
    ]
    white_sprites = [
        little_white, mid_white, high_white, mostly_white, point_markings, vit, 'FULLWHITE'
    ]

    skin_sprites = ['BLACK', 'PINK', 'DARKBROWN', 'BROWN', 'LIGHTBROWN', 'DARK', 'DARKGREY', 'GREY', 'DARKSALMON',
                    'SALMON', 'PEACH', 'DARKMARBLED', 'MARBLED', 'LIGHTMARBLED', 'DARKBLUE', 'BLUE', 'LIGHTBLUE', 'RED']
    
    skin_sprites_magic = ['FLAMES', 'FLOWERS', 'LIGHT1', 'SPARKLES', 'INK', 'MIST', 'MAGMA', 'SMOKE', 'PURPLEFLAMES',
                          'INK2', 'THUNDERSTORM', 'LIGHT2', 'DEATHBERRIES', 'SKELETON', 'FLESH', 'POWERLESS1',
                          'POWERLESS2', 'BUBBLES']
    
    skin_sprites_elemental = ['FLAMES2', 'BUBBLES2', 'VINES', 'WIND', 'LIGHTNING', 'BLUEFLAMES', 'FROZEN', 'STONE',
                              'TREE', 'PURPLESPARKS', 'PURPLEGLOW', 'SHADOW', 'YELLOWGLOW', 'FAEMANE', 'GREENGLOW',
                              'SHADOWBEAST', 'SPARKLES2', 'ROOTS']
    
    skin_sprites_bingle = ['GREENCHIMERA', 'CORALCHIMERA', 'FROSTGLOW', 'THIRDEYE', 'CRYSTALS', 'FOXTAIL', 'BATWINGS',
                           'CLOUDS', 'TRANSCLOUDS', 'SPOOKYCRYSTALS', 'MAGEGIFT', 'DEVILWINGS', 'SPARROWGIFT',
                           'DOVEWINGS', 'ANTLERS', 'BLUECORALCHIMERA', 'ICECRYSTALS', 'BLACKFOX']
    
    skin_colors_bingle2 = ['SHADOWSELF', 'FIRETAIL', 'BLUEFIRETAIL', 'SCORPION', 'SNOWFOX', 'KITSUNE', 'FENNECKITSUNE',
                           '006', '007', '008', '009', '010', '011', '012', '013', '014', '015', '016']

    skin_sprites_math = ['LIGHTPURPLE', 'BLUE2', 'DARKPURPLE', 'DARKBLUE', 'NEONGREEN', 'BLUESPECKLED', 'BRIGHTPINK',
                         'BRIGHTORANGE', 'MAGENTA', 'PINKBLUE', 'PURPLEYELLOW', 'BLUEORANGE', 'WHITE', 'BLACK2', 'AQUA',
                         'DARKGREEN', 'BRIGHTYELLOW', 'NULL1']

    skin_sprites_turtle = ['BLACKTURTLE', 'PINKTURTLE', 'DARKBROWNTURTLE', 'BROWNTURTLE', 'LIGHTBROWNTURTLE',
                           'DARKTURTLE', 'DARKGREYTURTLE', 'GREYTURTLE', 'DARKSALMONTURTLE', 'SALMONTURTLE',
                           'PEACHTURTLE', 'DARKMARBLEDTURTLE', 'MARBLEDTURTLE', 'LIGHTMARBLEDTURTLE', 'DARKBLUETURTLE',
                           'BLUETURTLE', 'LIGHTBLUETURTLE', 'REDTURTLE']

    skin_sprites_stain = ['STAINDUST', 'STAINICEBLUE', 'STAININDIGO', 'STAINBLUE', 'STAINPURPLE', 'STAINDARKBLUE',
                          'STAINLIGHTPINK', 'STAINYELLOW', 'STAINPINK', 'STAINGOLD', 'STAINHOTPINK', 'STRAINDIRT',
                          'STAINCYAN', 'STAINLIME', 'STAINTURQUOISE', 'STAINGREEN', 'STAINBLUEGREEN', 'STAINPEACOCK']

    """Holds all appearance information for a cat. """

    def __init__(
        self,
        name: str = "SingleColour",
        length: str = "short",
        colour: str = "WHITE",
        white_patches: str = None,
        eye_color: str = "BLUE",
        eye_colour2: str = None,
        tortiebase: str = None,
        tortiecolour: str = None,
        pattern: list = None,
        tortiepattern: str = None,
        tortie_tint: list = None,
        displays_2nd_tortie: bool = False,
        tortiecolour2: str = None,
        pattern2: list = None,
        tortiepattern2: str = None,
        tortie_tint2: list = None,
        vitiligo: str = None,
        points: str = None,
        physical_trait_1: str = None,
        physical_trait_2: str = None,
        physical_trait_3: str = None,
        physical_trait_4: str = None,
        physical_trait_hidden: str = None,
        physical_trait_hidden_2: str = None,
        physical_trait_hidden_3: str = None,
        physical_trait_hidden_4: str = None,
        accessory: list = None,
        paralyzed: bool = False,
        opacity: int = 100,
        scars: list = None,
        tint: list = None,
        skin: str = "BLACK",
        white_patches_tint: list = None,
        kitten_sprite: int = None,
        adol_sprite: int = None,
        adult_sprite: int = None,
        senior_sprite: int = None,
        para_adult_sprite: int = None,
        reverse: bool = False,
        fur_texture: str = None,
        build: str = None,
        height: str = None,
    ) -> None:
        self.name = name
        self.colour = colour
        self.white_patches = white_patches
        self.eye_colour = eye_color
        self.eye_colour2 = eye_colour2
        self.tortiebase = tortiebase
        self.pattern = pattern
        self.tortiepattern = tortiepattern
        self.tortiecolour = tortiecolour
        self.tortie_tint = tortie_tint
        self.displays_2nd_tortie = displays_2nd_tortie
        self.pattern2 = pattern2
        self.tortiepattern2 = tortiepattern2
        self.tortiecolour2 = tortiecolour2
        self.tortie_tint2 = tortie_tint2
        self.vitiligo = vitiligo
        self.length = length
        self.points = points
        self.rebuild_sprite = True
        self._accessory = accessory
        self._paralyzed = paralyzed
        self.opacity = opacity
        self.scars = scars if isinstance(scars, list) else []
        self.tint = tint
        self.physical_trait_1 = physical_trait_1
        self.physical_trait_2 = physical_trait_2
        self.physical_trait_3 = physical_trait_3
        self.physical_trait_4 = physical_trait_4
        self.physical_trait_hidden = physical_trait_hidden
        self.physical_trait_hidden_2 = physical_trait_hidden_2
        self.physical_trait_hidden_3 = physical_trait_hidden_3
        self.physical_trait_hidden_4 = physical_trait_hidden_4
        self.white_patches_tint = white_patches_tint
        self.screen_scale = scripts.game_structure.screen_settings.screen_scale
        self.cat_sprites = {
            "kitten": kitten_sprite if kitten_sprite is not None else 0,
            "adolescent": adol_sprite if adol_sprite is not None else 0,
            "young adult": adult_sprite if adult_sprite is not None else 0,
            "adult": adult_sprite if adult_sprite is not None else 0,
            "senior adult": adult_sprite if adult_sprite is not None else 0,
            "senior": senior_sprite if senior_sprite is not None else 0,
            "para_adult": para_adult_sprite if para_adult_sprite is not None else 0,
            "newborn": 20,
            "para_young": 17,
            "sick_adult": 18,
            "sick_young": 19,
        }

        self.reverse = reverse
        self.skin = skin
        self.fur_texture = fur_texture if fur_texture is not None else choice(["soft", "curly", "rough", "silky", "sleek", "wavy", "sparse", "tangled", "fuzzy", "spiky"])
        self.build = build if build is not None else choice(["stocky", "slender", "lithe", "wiry", "muscular", "lanky", "delicate", "hunched", "hefty", "burly", "bulky", "plump", "brawny", "stout", "broad", "chubby", "fat", "stocky", "chunky", "big-boned"])
        self.height = height if height is not None else choice(["petite", "short", "average", "average", "tall", "towering"])

    @property
    def accessory(self):
        return self._accessory

    @accessory.setter
    def accessory(self, val):
        self.rebuild_sprite = True
        self._accessory = val

    @property
    def paralyzed(self):
        return self._paralyzed

    @paralyzed.setter
    def paralyzed(self, val):
        self.rebuild_sprite = True
        self._paralyzed = val

    @staticmethod
    def generate_new_pelt(gender: str, parents: tuple = (), age: str = "adult"):
        new_pelt = Pelt()

        pelt_white = new_pelt.init_pattern_color(parents, gender)
        new_pelt.init_white_patches(pelt_white, parents)
        new_pelt.init_sprite()
        new_pelt.init_scars(age)
        new_pelt.init_accessories(age)
        new_pelt.init_eyes(parents)
        new_pelt.init_pattern(parents, gender)
        new_pelt.init_tint()
        new_pelt.init_physical_traits(parents)

        return new_pelt

    def check_and_convert(self, convert_dict):
        """Checks for old-type properties for the appearance-related properties
        that are stored in Pelt, and converts them. To be run when loading a cat in."""

        # converting modded pelt colors from categories to colors. oh god
        cs2_dict = {
                'WHITE': 'LIGHTLIME',
                'PALEGREY': 'PINKGREY',
                'SILVER': 'YELLOWBROWN',
                'GREY': 'REDGREY',
                'DARKGREY': 'BLUEBROWN',
                'GHOST': 'GHOSTBROWN',
                'BLACK': 'BLACKPURPLE',
                'CREAM': 'BLUECREAM',
                'PALEGINGER': 'PALEPINKPURPLE',
                'GOLDEN': 'ICEBLUE',
                'GINGER': 'BLUECS2',
                'DARKGINGER': 'GREENBROWN',
                'SIENNA': 'NAVYBLUE',
                'LIGHTBROWN': 'PURPLECREAM',
                'LILAC': 'INDIGOBLUSH',
                'BROWN': 'VIOLETBLUSH',
                'GOLDEN-BROWN': 'MAGENTA',
                'DARKBROWN': 'NAVYBROWN',
                'CHOCOLATE': 'MULBERRY'
            }
        cs_dict = {
                'WHITE': 'ICEWHITE',
                'PALEGREY': 'CRYSTAL',
                'SILVER': 'ORCHID',
                'GREY': 'CERULEAN',
                'DARKGREY': 'GRAPE',
                'GHOST': 'GHOSTBLUE',
                'BLACK': 'BLACKBLUE',
                'CREAM': 'THISTLE',
                'PALEGINGER': 'SUNYELLOW',
                'GOLDEN': 'BUBBLEGUM',
                'GINGER': 'REDSTAIN',
                'DARKGINGER': 'ROSE',
                'SIENNA': 'DUSKBROWN',
                'LIGHTBROWN': 'FROZENSUN',
                'LILAC': 'GREENGOLD',
                'BROWN': 'OCEAN',
                'GOLDEN-BROWN': 'TEAL',
                'DARKBROWN': 'REDBLUE',
                'CHOCOLATE': 'TREE'
            }
        heta_dict = {
                'WHITE': 'REDHETA',
                'PALEGREY': 'ORANGEHETA',
                'SILVER': 'YELLOWHETA',
                'GREY': 'NEONYELLOW',
                'DARKGREY': 'NEONGREEN',
                'GHOST': 'GREENHETA',
                'BLACK': 'MINTGREEN',
                'CREAM': 'DARKMINT',
                'PALEGINGER': 'NEONTEAL',
                'GOLDEN': 'CYANHETA',
                'GINGER': 'BLUEHETA',
                'DARKGINGER': 'NAVYHETA',
                'SIENNA': 'INDIGOHETA',
                'LIGHTBROWN': 'PURPLEHETA',
                'LILAC': 'VIOLETHETA',
                'BROWN': 'MAGENTAHETA',
                'GOLDEN-BROWN': 'PINKHETA',
                'DARKBROWN': 'SCARLETPINK',
                'CHOCOLATE': 'DARKREDHETA'
            }
        dance_dict = {
                'WHITE': 'LIGHTCINNAMON',
                'PALEGREY': 'CINNAMON',
                'SILVER': 'SILVERFAWN',
                'GREY': 'DARKCINNAMON',
                'DARKGREY': 'DARKFAWN',
                'GHOST': 'FAWN',
                'BLACK': 'LIGHTFAWN',
                'CREAM': 'PALEFAWN',
                'PALEGINGER': 'PALECREAM',
                'GOLDEN': 'LIGHTCREAM',
                'GINGER': 'DANCECREAM',
                'DARKGINGER': 'DARKCREAM',
                'SIENNA': 'DARKGOLD',
                'LIGHTBROWN': 'GOLD',
                'LILAC': 'LIGHTGOLD',
                'BROWN': 'SILVERCREAM',
                'GOLDEN-BROWN': 'PALEGOLD',
                'DARKBROWN': 'SUNSHINE',
                'CHOCOLATE': 'BRONZE'
            }
        silly_dict = {
                'WHITE': 'LIGHTLILAC',
                'PALEGREY': 'LILACSILLY',
                'SILVER': 'DARKLILAC',
                'GREY': 'DARKASH',
                'DARKGREY': 'ASH',
                'GHOST': 'LIGHTASH',
                'BLACK': 'PALEASH',
                'CREAM': 'SILVERCINNAMON',
                'PALEGINGER': 'SILVERRED',
                'GOLDEN': 'PALEBROWN',
                'GINGER': 'LIGHTBROWNSILLY',
                'DARKGINGER': 'BROWNSILLY',
                'SIENNA': 'DARKBROWNSILLY',
                'LIGHTBROWN': 'EBONY',
                'LILAC': 'DARKCHOCOLATE',
                'BROWN': 'CHOCOLATESILLY',
                'GOLDEN-BROWN': 'LIGHTCHOCOLATE',
                'DARKBROWN': 'PALECHOCOLATE',
                'CHOCOLATE': 'PALECINNAMON'
            }
        ster_dict = {
                'WHITE': 'WHITESTER',
                'PALEGREY': 'PALEGREYSTER',
                'SILVER': 'LIGHTGREY',
                'GREY': 'GREYSTER',
                'DARKGREY': 'DARKGREYSTER',
                'GHOST': 'BLACKSTER',
                'BLACK': 'OBSIDIANSTER',
                'CREAM': 'GHOSTSTER',
                'PALEGINGER': 'PALEBLUE',
                'GOLDEN': 'LIGHTBLUE',
                'GINGER': 'BLUESTER',
                'DARKGINGER': 'DARKBLUE',
                'SIENNA': 'SILVERCHOCOLATE',
                'LIGHTBROWN': 'SILVERORANGE',
                'LILAC': 'DARKSLATE',
                'BROWN': 'SLATE',
                'GOLDEN-BROWN': 'LIGHTSLATE',
                'DARKBROWN': 'PALESLATE',
                'CHOCOLATE': 'PALELILAC'
            }
        mimi_dict = {
                'WHITE': 'COPPERMIMI',
                'PALEGREY': 'DARKORANGE',
                'SILVER': 'ORANGE',
                'GREY': 'LIGHTORANGE',
                'DARKGREY': 'PALEORANGE',
                'GHOST': 'PALEGINGERMIMI',
                'BLACK': 'LIGHTGINGER',
                'CREAM': 'GINGERMIMI',
                'PALEGINGER': 'DARKGINGERMIMI',
                'GOLDEN': 'SILVERGOLD',
                'GINGER': 'RUSSET',
                'DARKGINGER': 'DARKRED',
                'SIENNA': 'REDMIMI',
                'LIGHTBROWN': 'LIGHTRED',
                'LILAC': 'PALERED',
                'BROWN': 'SILVERMIMI',
                'GOLDEN-BROWN': 'SILVERGREY',
                'DARKBROWN': 'SILVERBLUE',
                'CHOCOLATE': 'SILVERSLATE'
            }
        hive_dict = {
                'WHITE': 'GREENH',
                'PALEGREY': 'TEALH',
                'SILVER': 'BLUEH',
                'GREY': 'NAVYH',
                'DARKGREY': 'INDIGOH',
                'GHOST': 'PURPLEH',
                'BLACK': 'VIOLETH',
                'CREAM': 'PINKH',
                'PALEGINGER': 'ROSEH',
                'GOLDEN': 'DARKPINKH',
                'GINGER': 'REDH',
                'DARKGINGER': 'ORANGEH',
                'SIENNA': 'GOLDH',
                'LIGHTBROWN': 'PASTELPURPLEH',
                'LILAC': 'DARKGREENH',
                'BROWN': 'BROWN-PURPLE',
                'GOLDEN-BROWN': 'YELLOWH',
                'DARKBROWN': 'DARKMOSS',
                'CHOCOLATE': 'PURPLESWIRL'
            }
        kris_dict = {
                'WHITE': 'PINKCREAM',
                'PALEGREY': 'BLUEMINT',
                'SILVER': 'SUNSET',
                'GREY': 'PINK-BLUE',
                'DARKGREY': 'INDIGOK',
                'GHOST': 'BLUEGHOSTK',
                'BLACK': 'PINKK',
                'CREAM': 'PASTELPINKBLUE',
                'PALEGINGER': 'RUSTYGREEN',
                'GOLDEN': 'OURPLE',
                'GINGER': 'BLUE-YELLOW',
                'DARKGINGER': 'BLUE-PURPLE',
                'SIENNA': 'DARKSUNSET',
                'LIGHTBROWN': 'BANANABERRY',
                'LILAC': 'BRIGHTBLUEK',
                'BROWN': 'SUNRISE',
                'GOLDEN-BROWN': 'GREEN-NAVY',
                'DARKBROWN': 'PINKSHADOW',
                'CHOCOLATE': 'REDK'
            }
        meteor_dict = {
                'WHITE': 'SILVERMETEOR',
                'PALEGREY': 'SILVERNAVY',
                'SILVER': 'CREAMSILVER',
                'GREY': 'GREYSTAR',
                'DARKGREY': 'DARKGREYSTAR',
                'GHOST': 'BLACK-BROWN',
                'BLACK': 'BLUESPOTTED',
                'CREAM': 'CREAMMETEOR',
                'PALEGINGER': 'PINK-WHITE',
                'GOLDEN': 'TANSPOTTED',
                'GINGER': 'REVERSESUN',
                'DARKGINGER': 'WARM-BLUE',
                'SIENNA': 'INDIGO-VIOLET',
                'LIGHTBROWN': 'GREYMETEOR',
                'LILAC': 'ICESPOTTED',
                'BROWN': 'SHADOW',
                'GOLDEN-BROWN': 'BLUE-EARTH',
                'DARKBROWN': 'EARTHSPOTTED',
                'CHOCOLATE': 'BROWN-TAN'
            }
        pastel_dict = {
                'WHITE': 'PALEPINK-PURPLE',
                'PALEGREY': 'PALEGREY-PINK',
                'SILVER': 'PALEBLUE-YELLOW',
                'GREY': 'PALEMINT-PURPLE',
                'DARKGREY': 'PALEGREEN-INDIGO',
                'GHOST': 'PALEYELLOW-INDIGO',
                'BLACK': 'PALEORANGE-BLUE',
                'CREAM': 'PALEPURPLE-GOLD',
                'PALEGINGER': 'PALECYAN-GOLD',
                'GOLDEN': 'PALEMINT-MAGENTA',
                'GINGER': 'PALEMINT-VIOLET',
                'DARKGINGER': 'PALEGREEN-BLUE',
                'SIENNA': 'PALEGREEN-NAVY',
                'LIGHTBROWN': 'PALEBLUE-INDIGO',
                'LILAC': 'PALECYAN-PURPLE',
                'BROWN': 'PALECYAN-NAVY',
                'GOLDEN-BROWN': 'PALECYAN-BLUE',
                'DARKBROWN': 'PALEYELLOWGREEN',
                'CHOCOLATE': 'PALEYELLOW-BLUE'
            }
        pepper_dict = {
                'WHITE': 'ICEPEPPER',
                'PALEGREY': 'CYANPEPPER',
                'SILVER': 'BLUEPEPPER',
                'GREY': 'OCEANPEPPER',
                'DARKGREY': 'DARKBLUEPEPPER',
                'GHOST': 'BLUEGHOSTPEPPER',
                'BLACK': 'BLACKBLUEPEPPER',
                'CREAM': 'GOLDCREAM',
                'PALEGINGER': 'GOLDPEPPER',
                'GOLDEN': 'YELLOW-RED',
                'GINGER': 'BRIGHTYELLOW-RED',
                'DARKGINGER': 'NEONRED',
                'SIENNA': 'REDBLACK',
                'LIGHTBROWN': 'PALEBLUE-GOLD',
                'LILAC': 'INDIGOPEPPER',
                'BROWN': 'RUSTBLUEPEPPER',
                'GOLDEN-BROWN': 'REDPEPPER',
                'DARKBROWN': 'REDBLUEBLACK',
                'CHOCOLATE': 'SCARLETPEPPER'
            }
        sparkle_dict = {
                'WHITE': 'REDS',
                'PALEGREY': 'RED-ORANGES',
                'SILVER': 'DARKYELLOWS',
                'GREY': 'GREENREDS',
                'DARKGREY': 'CYANPINKG',
                'GHOST': 'INDIGOREDS',
                'BLACK': 'REVERSERAINBOW',
                'CREAM': 'PINKREDS',
                'PALEGINGER': 'RUSTYS',
                'GOLDEN': 'GREENORANGES',
                'GINGER': 'REDCYANS',
                'DARKGINGER': 'MINTBLUES',
                'SIENNA': 'BLACKBLUES',
                'LIGHTBROWN': 'BANANAS',
                'LILAC': 'WHITEGREENS',
                'BROWN': 'BROWNREDS',
                'GOLDEN-BROWN': 'RAINBOW',
                'DARKBROWN': 'GREENDARKREDS',
                'CHOCOLATE': 'SUNNYS'
            }

        if "Ster" in self.name:
            self.name = self.name[4:]
            self.name = self.name.capitalize()
            self.colour = ster_dict[self.colour]
        if "Silly" in self.name:
            self.name = self.name[5:]
            self.name = self.name.capitalize()
            self.colour = silly_dict[self.colour]
        if "Dance" in self.name:
            self.name = self.name[5:]
            self.name = self.name.capitalize()
            self.colour = dance_dict[self.colour]
        if "Mimi" in self.name:
            self.name = self.name[4:]
            self.name = self.name.capitalize()
            self.colour = mimi_dict[self.colour]
        if "CS2" in self.name:
            self.name = self.name[3:]
            self.name = self.name.capitalize()
            self.colour = cs2_dict[self.colour]
        if "CS" in self.name:
            self.name = self.name[2:]
            self.name = self.name.capitalize()
            self.colour = cs_dict[self.colour]
        if "Heta" in self.name:
            self.name = self.name[4:]
            self.name = self.name.capitalize()
            self.colour = heta_dict[self.colour]
        if "Hive" in self.name:
            self.name = self.name[4:]
            self.name = self.name.capitalize()
            self.colour = hive_dict[self.colour]
        if "Kris" in self.name:
            self.name = self.name[4:]
            self.name = self.name.capitalize()
            self.colour = kris_dict[self.colour]
        if "Meteor" in self.name:
            self.name = self.name[6:]
            self.name = self.name.capitalize()
            self.colour = meteor_dict[self.colour]
        if "Pastel" in self.name:
            self.name = self.name[6:]
            self.name = self.name.capitalize()
            self.colour = pastel_dict[self.colour]
        if "Pepper" in self.name:
            self.name = self.name[6:]
            self.name = self.name.capitalize()
            self.colour = pepper_dict[self.colour]
        if "Sparkle" in self.name:
            self.name = self.name[7:]
            self.name = self.name.capitalize()
            self.colour = sparkle_dict[self.colour]

        if self.name == "Stripe":
            self.name = "Singlestripe"
        if self.name == "Single":
            self.name = "SingleColour"

        if self.name in ["Tortie", "Calico"]:
            if "ster" in self.tortiebase:
                self.tortiebase = self.tortiebase[4:]
                self.colour = ster_dict[self.colour]
            if "ster" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[4:]
                self.tortiecolour = ster_dict[self.tortiecolour]

            if "dance" in self.tortiebase:
                self.tortiebase = self.tortiebase[5:]
                self.colour = dance_dict[self.colour]
            if "dance" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[5:]
                self.tortiecolour = dance_dict[self.tortiecolour]

            if "silly" in self.tortiebase:
                self.tortiebase = self.tortiebase[5:]
                self.colour = silly_dict[self.colour]
            if "silly" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[5:]
                self.tortiecolour = silly_dict[self.tortiecolour]

            if "mimi" in self.tortiebase:
                self.tortiebase = self.tortiebase[4:]
                self.colour = mimi_dict[self.colour]
            if "mimi" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[4:]
                self.tortiecolour = mimi_dict[self.tortiecolour]

            if "cs_" in self.tortiebase and "2" in self.tortiebase:
                self.tortiebase = self.tortiebase[3:]
                self.tortiebase = self.tortiebase.replace('2', '')
                self.colour = cs2_dict[self.colour]
            if "cs_" in self.tortiepattern and "2" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[3:]
                self.tortiepattern = self.tortiepattern.replace('2', '')
                self.tortiecolour = cs2_dict[self.tortiecolour]

            if "cs_" in self.tortiebase:
                self.tortiebase = self.tortiebase[3:]
                self.colour = cs_dict[self.colour]
            if "cs_" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[3:]
                self.tortiecolour = cs_dict[self.tortiecolour]

            if "kris" in self.tortiebase:
                self.tortiebase = self.tortiebase[4:]
                self.colour = kris_dict[self.colour]
            if "kris" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[4:]
                self.tortiecolour = kris_dict[self.tortiecolour]

            if "heta" in self.tortiebase:
                self.tortiebase = self.tortiebase[4:]
                self.colour = heta_dict[self.colour]
            if "heta" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[4:]
                self.tortiecolour = heta_dict[self.tortiecolour]

            if "hive" in self.tortiebase:
                self.tortiebase = self.tortiebase[4:]
                self.colour = hive_dict[self.colour]
            if "hive" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[4:]
                self.tortiecolour = hive_dict[self.tortiecolour]

            if "meteor" in self.tortiebase:
                self.tortiebase = self.tortiebase[6:]
                self.colour = meteor_dict[self.colour]
            if "meteor" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[6:]
                self.tortiecolour = meteor_dict[self.tortiecolour]

            if "pastel" in self.tortiebase:
                self.tortiebase = self.tortiebase[6:]
                self.colour = pastel_dict[self.colour]
            if "pastel" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[6:]
                self.tortiecolour = pastel_dict[self.tortiecolour]

            if "pepper" in self.tortiebase:
                self.tortiebase = self.tortiebase[6:]
                self.colour = pepper_dict[self.colour]
            if "pepper" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[6:]
                self.tortiecolour = pepper_dict[self.tortiecolour]

            if "sparkle" in self.tortiebase:
                self.tortiebase = self.tortiebase[7:]
                self.colour = sparkle_dict[self.colour]
            if "sparkle" in self.tortiepattern:
                self.tortiepattern = self.tortiepattern[7:]
                self.tortiecolour = sparkle_dict[self.tortiecolour]

            if self.tortiepattern == "stripe":
                self.tortiepattern = "singlestripe"
            if self.tortiebase == "stripe":
                self.tortiebase = "singlestripe"

        if type(self.tint) != list:
            self.tint = [self.tint]
        if type(self.tortie_tint) != list:
            self.tortie_tint = [self.tortie_tint]
        if type(self.tortie_tint2) != list:
            self.tortie_tint2 = [self.tortie_tint2]
        if type(self.white_patches_tint) != list:
            self.white_patches_tint = [self.white_patches_tint]

        if "none" in self.tint:
            self.tint = ["none"]
        if "none" in self.tortie_tint:
            self.tortie_tint = ["none"]
        if "none" in self.tortie_tint2:
            self.tortie_tint2 = ["none"]
        if "none" in self.white_patches_tint:
            self.white_patches_tint = ["none"]

        # First, convert from some old names that may be in white_patches. 
        if self.white_patches == 'POINTMARK':
            self.white_patches = "SEALPOINT"
        elif self.white_patches == "PANTS2":
            self.white_patches = "PANTSTWO"
        elif self.white_patches == "ANY2":
            self.white_patches = "ANYTWO"
        elif self.white_patches == "VITILIGO2":
            self.white_patches = "VITILIGOTWO"

        if self.vitiligo == "VITILIGO2":
            self.vitiligo = "VITILIGOTWO"

        # Move white_patches that should be in vit or points.
        if self.white_patches in Pelt.vit:
            self.vitiligo = self.white_patches
            self.white_patches = None
        elif self.white_patches in Pelt.point_markings:
            self.points = self.white_patches
            self.white_patches = None

        if self.tortiepattern and "tortie" in self.tortiepattern:
            self.tortiepattern = sub("tortie", "", self.tortiepattern.lower())
            if self.tortiepattern == "solid":
                self.tortiepattern = "single"
        
        '''
        if self.white_patches in convert_dict["old_creamy_patches"]:
            self.white_patches = convert_dict["old_creamy_patches"][self.white_patches]
            self.white_patches_tint = "darkcream"
        elif self.white_patches in ("SEPIAPOINT", "MINKPOINT", "SEALPOINT"):
            self.white_patches_tint = "none"
        '''

        # Eye Color Convert Stuff
        if self.eye_colour == "BLUE2":
            self.eye_colour = "COBALT"
        if self.eye_colour2 == "BLUE2":
            self.eye_colour2 = "COBALT"
        if self.eye_colour2 == "VIOLET2":
            self.eye_colour2 = "BLACKBERRY"
        if self.eye_colour2 == "ROSE2":
            self.eye_colour2 = "DARK ROSE"
        if self.eye_colour2 == "TURQUOISE2":
            self.eye_colour2 = "DARK TURQUOISE"

        if self.eye_colour in ["BLUEYELLOW", "BLUEGREEN"]:
            if self.eye_colour == "BLUEYELLOW":
                self.eye_colour2 = "YELLOW"
            elif self.eye_colour == "BLUEGREEN":
                self.eye_colour2 = "GREEN"
            self.eye_colour = "BLUE"
        
        if self.colour == "Lynx2":
            self.colour = "Dalmatian"

        if self.length == "long":
            if self.cat_sprites["adult"] not in (9, 10, 11):
                if self.cat_sprites["adult"] == 0:
                    self.cat_sprites["adult"] = 9
                elif self.cat_sprites["adult"] == 1:
                    self.cat_sprites["adult"] = 10
                elif self.cat_sprites["adult"] == 2:
                    self.cat_sprites["adult"] = 11
                self.cat_sprites["young adult"] = self.cat_sprites["adult"]
                self.cat_sprites["senior adult"] = self.cat_sprites["adult"]
                self.cat_sprites["para_adult"] = 16
        else:
            self.cat_sprites["para_adult"] = 15
        if self.cat_sprites["senior"] not in (12, 13, 14):
            if self.cat_sprites["senior"] == 3:
                self.cat_sprites["senior"] = 12
            elif self.cat_sprites["senior"] == 4:
                self.cat_sprites["senior"] = 13
            elif self.cat_sprites["senior"] == 5:
                self.cat_sprites["senior"] = 14

        if self.accessory is None:
            self.accessory = []
        elif isinstance(self.accessory, str):
            self.accessory = [self.accessory]

        if self.pattern is not None:
            if isinstance(self.pattern, str):
                self.pattern = [self.pattern]
        if self.white_patches is not None:
            if isinstance(self.white_patches, str):
                self.white_patches = [self.white_patches]

            if "HALF" in self.white_patches:
                self.white_patches.remove("HALF")
                self.white_patches.append("ERAHALF")
            if "MASK" in self.white_patches:
                self.white_patches.remove("MASK")
                self.white_patches.append("ERAMASK")

    def init_eyes(self, parents):
        """Sets eye color for this cat's pelt. Takes parents' eye colors into account.
        Heterochromia is possible based on the white-ness of the pelt, so the pelt color and white_patches must be
        set before this function is called.

        :param parents: List[Cat] representing this cat's parents

        :return: None
        """
        highest_white = ""
        if self.white_patches:
            for patch in self.white_patches:
                if patch in Pelt.little_white and highest_white not in ["little", "mid", "high", "mostly", "full"]:
                    highest_white = "little"
                if patch in Pelt.mid_white and highest_white not in ["mid", "high", "mostly", "full"]:
                    highest_white = "mid"
                if patch in Pelt.high_white and highest_white not in ["high", "mostly", "full"]:
                    highest_white = "high"
                if patch in Pelt.mostly_white and highest_white not in ["mostly", "full"]:
                    highest_white = "mostly"
                if patch == "FULLWHITE" and highest_white != "full":
                    highest_white = "full"
                    break

        if not parents:
            self.eye_colour = choice(Pelt.eye_colours)
        else:
            colour_wheel = [Pelt.yellow_eyes, Pelt.blue_eyes, Pelt.green_eyes, Pelt.red_eyes, Pelt.purple_eyes,
                            Pelt.neos_eyes, Pelt.flutter_eyes, Pelt.lamp_eyes, Pelt.angel_eyes, Pelt.snail_eyes]
            similar_colors = []
            for i in parents:
                for colour in colour_wheel:
                    if i.pelt.eye_colour in colour:
                        for color in colour:
                            similar_colors.append(color)

            self.eye_colour = choice(
                [i.pelt.eye_colour for i in parents] + [choice(similar_colors)] +[choice(similar_colors)] + [choice(Pelt.eye_colours)]
            )

        # White patches must be initalized before eye color.
        num = constants.CONFIG["cat_generation"]["base_heterochromia"]
        if (
            highest_white in ["high", "mostly", "full"]
            or self.colour == "WHITE"
        ):
            num = num - 90
        if highest_white == "full" or self.colour == "WHITE":
            num -= 10
        for _par in parents:
            if _par.pelt.eye_colour2:
                num -= 10

        if num < 0:
            num = 1

        if not random.randint(0, num):
            colour_wheel = [Pelt.yellow_eyes, Pelt.blue_eyes, Pelt.green_eyes, Pelt.red_eyes, Pelt.purple_eyes]
            for colour in colour_wheel[:]:
                if self.eye_colour in colour:
                    colour_wheel.remove(
                        colour
                    )  # removes the selected list from the options
                    self.eye_colour2 = choice(
                        choice(colour_wheel)
                    )  # choose from the remaining two lists
                    break

    def pattern_color_inheritance(self, parents: tuple = (), gender="female"):
        # setting parent pelt categories
        # We are using a set, since we don't need this to be ordered, and sets deal with removing duplicates.
        par_peltlength = set()
        par_peltcolours = set()
        par_peltnames = set()
        par_pelts = []
        par_white = []
        for p in parents:
            if p:
                # Gather pelt color.
                par_peltcolours.add(p.pelt.colour)

                # Gather pelt length
                par_peltlength.add(p.pelt.length)

                # Gather pelt name
                if p.pelt.name in Pelt.torties:
                    par_peltnames.add(p.pelt.tortiebase.capitalize())
                else:
                    par_peltnames.add(p.pelt.name)

                # Gather exact pelts, for direct inheritance.
                par_pelts.append(p.pelt)

                # Gather if they have white in their pelt.
                par_white.append(p.pelt.white)
            else:
                # If order for white patches to work correctly, we also want to randomly generate a "pelt_white"
                # for each "None" parent (missing or unknown parent)
                par_white.append(bool(random.getrandbits(1)))

                # Append None
                # Gather pelt color.
                par_peltcolours.add(None)
                par_peltlength.add(None)
                par_peltnames.add(None)

        # If this list is empty, something went wrong.
        if not par_peltcolours:
            print("Warning - no parents: pelt randomized")
            return self.randomize_pattern_color(gender)

        # There is a 1/10 chance for kits to have the exact same pelt as one of their parents
        if constants.CONFIG["cat_generation"]["direct_inheritance"] != 0 and not random.randint(
            0, constants.CONFIG["cat_generation"]["direct_inheritance"]
        ):  # 1/10 chance
            selected = choice(par_pelts)
            self.name = selected.name
            self.length = selected.length
            self.colour = selected.colour
            self.tortiebase = selected.tortiebase
            return selected.white

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT
        # ------------------------------------------------------------------------------------------------------------#

        # Determine pelt.
        weights = [
            0,
            0,
            0,
            0,
            0
        ]  # Weights for each pelt group. It goes: (tabbies, spotted, plain, exotic, magic)
        for p_ in par_peltnames:
            if p_ in Pelt.tabbies:
                add_weight = (50, 10, 5, 7, 0)
            elif p_ in Pelt.spotted:
                add_weight = (10, 50, 5, 5, 0)
            elif p_ in Pelt.plain:
                add_weight = (5, 5, 50, 0, 0)
            elif p_ in Pelt.exotic:
                add_weight = (15, 15, 1, 45, 0)
            elif p_ in Pelt.magic:
                add_weight = (15, 15, 5, 25, 50)
            elif (
                p_ is None
            ):  # If there is at least one unknown parent, a None will be added to the set.
                add_weight = (35, 20, 30, 15, 0)
            else:
                add_weight = (0, 0, 0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

        # A quick check to make sure all the weights aren't 0
        if all([x == 0 for x in weights]):
            weights = [1, 1, 1, 1, 1]

        # Now, choose the pelt category and pelt. The extra 0 is for the tortie pelts,
        chosen_pelt = choice(
            random.choices(Pelt.pelt_categories, weights=weights + [0], k=1)[0]
        )

        # Tortie chance
        tortie_chance_f = constants.CONFIG["cat_generation"][
            "base_female_tortie"
        ]  # There is a default chance for female tortie
        tortie_chance_m = constants.CONFIG["cat_generation"]["base_male_tortie"]
        for p_ in par_pelts:
            if p_.name in Pelt.torties:
                tortie_chance_f = int(tortie_chance_f / 2)
                tortie_chance_m = tortie_chance_m - 1
                break
        if tortie_chance_f <= 1:
            tortie_chance_f = 2
        if tortie_chance_m <= 1:
            tortie_chance_m = 2

        # Determine tortie:
        if gender == "female" or (gender == "intersex" and random.randint(1, 2) == 1):
            torbie = random.getrandbits(tortie_chance_f) == 1
        else:
            torbie = random.getrandbits(tortie_chance_m) == 1

        chosen_tortie_base = None
        if torbie:
            # If it is tortie, the chosen pelt above becomes the base pelt.
            chosen_tortie_base = chosen_pelt
            if chosen_tortie_base in ("TwoColour", "SingleColour"):
                chosen_tortie_base = "Single"
            chosen_tortie_base = chosen_tortie_base.lower()
            chosen_pelt = random.choice(Pelt.torties)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT COLOUR
        # ------------------------------------------------------------------------------------------------------------#
        # Weights for each colour group. It goes: (ginger_colours, black_colours, white_colours, brown_colours)
        base_game_pelts = ["Tabby", "Ticked", "Mackerel", "Classic", "Sokoke", "Agouti", "Speckled", "Rosette",
                           "SingleColour", "Smoke", "Singlestripe", "Bengal", "Marbled"]
        base_game_pelts_masked = ["Tabby", "Ticked", "Mackerel", "Classic", "Sokoke", "Agouti", "Speckled", "Rosette",
                                  "SingleColour", "Smoke", "Singlestripe", "Bengal", "Marbled", "Masked"]

        # colour_categories = [ginger_colours, black_colours, white_colours, brown_colours,
        # red_colors, orange_colors, yellow_colors, green_colors, blue_colors, purple_colors, black_colors]

        weights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for p_ in par_peltcolours:
            if p_ in Pelt.ginger_colours:
                add_weight = (40, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0)
            elif p_ in Pelt.black_colours:
                add_weight = (0, 40, 2, 5, 2, 0, 0, 0, 0, 0, 0)
            elif p_ in Pelt.white_colours:
                add_weight = (0, 5, 40, 0, 0, 0, 0, 0, 0, 0, 0)
            elif p_ in Pelt.brown_colours:
                add_weight = (10, 5, 0, 35, 0, 0, 0, 0, 0, 0, 0)
            elif p_ in Pelt.red_colors:
                add_weight = (30, 0, 0, 20, 50, 40, 15, 0, 0, 20, 0)
            elif p_ in Pelt.orange_colors:
                add_weight = (20, 0, 0, 35, 30, 50, 30, 0, 0, 0, 0)
            elif p_ in Pelt.yellow_colors:
                add_weight = (30, 0, 0, 15, 5, 25, 50, 25, 0, 0, 0)
            elif p_ in Pelt.green_colors:
                add_weight = (0, 0, 0, 10, 0, 0, 30, 50, 30, 10, 0)
            elif p_ in Pelt.blue_colors:
                add_weight = (0, 25, 0, 0, 0, 0, 0, 30, 50, 30, 25)
            elif p_ in Pelt.purple_colors:
                add_weight = (5, 10, 0, 0, 20, 0, 0, 0, 30, 50, 30)
            elif p_ in Pelt.black_colors:
                add_weight = (0, 40, 2, 2, 0, 0, 0, 0, 3, 3, 50)
            elif p_ is None:
                add_weight = (40, 40, 40, 40, 40, 0, 0, 0, 0, 0, 0)
            else:
                add_weight = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

            # A quick check to make sure all the weights aren't 0
            if all([x == 0 for x in weights]):
                weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        chosen_pelt_color = choice(
            random.choices(Pelt.colour_categories, weights=weights, k=1)[0]
        )
        # print('INIT COLOR: ' + chosen_pelt_color)

        if chosen_pelt not in base_game_pelts_masked:
            chosen_pelt_color = choice(Pelt.pelt_colours)
        elif chosen_pelt == "Masked":
            if chosen_pelt_color in Pelt.no_masked:
                chosen_pelt_color = choice(Pelt.pelt_colours)

        # print('FINAL COLOR: ' + chosen_pelt_color)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT LENGTH
        # ------------------------------------------------------------------------------------------------------------#

        weights = [0, 0, 0]  # Weights for each length. It goes (short, medium, long)
        for p_ in par_peltlength:
            if p_ == "short":
                add_weight = (50, 10, 2)
            elif p_ == "medium":
                add_weight = (25, 50, 25)
            elif p_ == "long":
                add_weight = (2, 10, 50)
            elif p_ is None:
                add_weight = (10, 10, 10)
            else:
                add_weight = (0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

        # A quick check to make sure all the weights aren't 0
        if all([x == 0 for x in weights]):
            weights = [1, 1, 1]

        chosen_pelt_length = random.choices(Pelt.pelt_length, weights=weights, k=1)[0]

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT WHITE
        # ------------------------------------------------------------------------------------------------------------#

        # There are 94 percentage points that can be added by
        # parents having white. If we have more than two, this
        # will keep that the same.
        percentage_add_per_parent = int(94 / len(par_white))
        chance = 3
        for p_ in par_white:
            if p_:
                chance += percentage_add_per_parent

        chosen_white = random.randint(1, 100) <= chance

        # Adjustments to pelt chosen based on if the pelt has white in it or not.
        if chosen_pelt in ("TwoColour", "SingleColour"):
            if chosen_white:
                chosen_pelt = "TwoColour"
            else:
                chosen_pelt = "SingleColour"
        elif chosen_pelt == "Calico":
            if not chosen_white:
                chosen_pelt = "Tortie"

        # SET THE PELT
        self.name = chosen_pelt
        self.colour = chosen_pelt_color
        self.length = chosen_pelt_length
        self.tortiebase = (
            chosen_tortie_base  # This will be none if the cat isn't a tortie.
        )
        return chosen_white

    def randomize_pattern_color(self, gender):
        # ------------------------------------------------------------------------------------------------------------#
        #   PELT
        # ------------------------------------------------------------------------------------------------------------#
        base_game_pelts = ["Tabby", "Ticked", "Mackerel", "Classic", "Sokoke", "Agouti", "Speckled", "Rosette",
                           "SingleColour", "Smoke", "Singlestripe", "Bengal", "Marbled"]

        # Determine pelt.
        chosen_pelt = choice(
            random.choices(Pelt.pelt_categories, weights=(35, 20, 30, 15, 1, 1), k=1)[0]
        )

        # Tortie chance
        # There is a default chance for female tortie, slightly increased for completely random generation.
        tortie_chance_f = constants.CONFIG["cat_generation"]["base_female_tortie"] - 1
        tortie_chance_m = constants.CONFIG["cat_generation"]["base_male_tortie"]
        if gender == "female" or (gender == "intersex" and random.randint(1, 2) == 1):
            torbie = random.getrandbits(tortie_chance_f) == 1
        else:
            torbie = random.getrandbits(tortie_chance_m) == 1

        chosen_tortie_base = None
        if torbie:
            # If it is tortie, the chosen pelt above becomes the base pelt.
            chosen_tortie_base = chosen_pelt
            if chosen_tortie_base in ("TwoColour", "SingleColour"):
                chosen_tortie_base = "Single"
            chosen_tortie_base = chosen_tortie_base.lower()
            chosen_pelt = random.choice(Pelt.torties)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT COLOUR
        # ------------------------------------------------------------------------------------------------------------#
        sparkle_chance = constants.CONFIG["cat_generation"]["sparkle_chance"]
        if randint(1,sparkle_chance) == 1:
            chosen_pelt_color = choice(
                random.choices(Pelt.colour_categories, k=1)[0]
            )
        else:
            chosen_pelt_color = choice(Pelt.pelt_colours)

        if chosen_pelt == 'Masked':
            while chosen_pelt_color in Pelt.no_masked:
                chosen_pelt_color = choice(
                    random.choices(Pelt.colour_categories, k=1)[0]
                )
        elif chosen_pelt not in base_game_pelts:
            while chosen_pelt_color not in Pelt.pelt_colours:
                chosen_pelt_color = choice(
                    random.choices(Pelt.colour_categories, k=1)[0]
                )

        # if somehow it escapes the while loop
        base_and_masked = base_game_pelts + ['Masked']
        if chosen_pelt not in base_and_masked and chosen_pelt_color not in Pelt.pelt_colours:
            chosen_pelt_color = 'GOLDEN'

        if chosen_tortie_base:
            if chosen_tortie_base == 'masked':
                while chosen_pelt_color in Pelt.no_masked:
                    chosen_pelt_color = choice(
                        random.choices(Pelt.colour_categories, k=1)[0]
                    )
            elif chosen_tortie_base not in base_game_pelts:
                while chosen_pelt_color not in Pelt.pelt_colours:
                    chosen_pelt_color = choice(
                        random.choices(Pelt.colour_categories, k=1)[0]
                    )

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT LENGTH
        # ------------------------------------------------------------------------------------------------------------#

        chosen_pelt_length = random.choice(Pelt.pelt_length)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT WHITE
        # ------------------------------------------------------------------------------------------------------------#

        chosen_white = random.randint(1, 100) <= 40

        # Adjustments to pelt chosen based on if the pelt has white in it or not.
        if chosen_pelt in ("TwoColour", "SingleColour"):
            if chosen_white:
                chosen_pelt = "TwoColour"
            else:
                chosen_pelt = "SingleColour"
        elif chosen_pelt == "Calico":
            if not chosen_white:
                chosen_pelt = "Tortie"

        self.name = chosen_pelt
        self.colour = chosen_pelt_color
        self.length = chosen_pelt_length
        self.tortiebase = (
            chosen_tortie_base  # This will be none if the cat isn't a tortie.
        )
        return chosen_white

    def init_pattern_color(self, parents, gender) -> bool:
        """Inits self.name, self.colour, self.length,
        self.tortiebase and determines if the cat
        will have white patche or not.
        Return TRUE is the cat should have white patches,
        false is not."""

        if parents:
            # If the cat has parents, use inheritance to decide pelt.
            chosen_white = self.pattern_color_inheritance(parents, gender)
        else:
            chosen_white = self.randomize_pattern_color(gender)

        return chosen_white

    def init_sprite(self):
        self.cat_sprites = {
            "newborn": 20,
            "kitten": random.randint(0, 2),
            "adolescent": random.randint(3, 5),
            "senior": random.randint(12, 14),
            "sick_young": 19,
            "sick_adult": 18,
        }
        self.reverse = bool(random.getrandbits(1))
        # skin chances
        self.skin = choice(Pelt.skin_sprites)

        if self.length != "long":
            self.cat_sprites["adult"] = random.randint(6, 8)
            self.cat_sprites["para_adult"] = 16
        else:
            self.cat_sprites["adult"] = random.randint(9, 11)
            self.cat_sprites["para_adult"] = 15
        self.cat_sprites["young adult"] = self.cat_sprites["adult"]
        self.cat_sprites["senior adult"] = self.cat_sprites["adult"]

    def init_scars(self, age):
        if age == "newborn":
            return

        if age in ("kitten", "adolescent"):
            scar_choice = random.randint(0, 50)  # 2%
        elif age in ("young adult", "adult"):
            scar_choice = random.randint(0, 20)  # 5%
        else:
            scar_choice = random.randint(0, 15)  # 6.67%

        if scar_choice == 1:
            self.scars.append(choice([choice(Pelt.scars1), choice(Pelt.scars3)]))

        if "NOTAIL" in self.scars and "HALFTAIL" in self.scars:
            self.scars.remove("HALFTAIL")

    def init_accessories(self, age):
        if age == "newborn":
            self.accessory = []
            return

        acc_display_choice = random.randint(0, 80)
        if age in ("kitten", "adolescent"):
            acc_display_choice = random.randint(0, 180)
        elif age in ("young adult", "adult"):
            acc_display_choice = random.randint(0, 100)

        if acc_display_choice == 1:
            self.accessory = [
                choice([choice(Pelt.plant_accessories), choice(Pelt.wild_accessories), choice(Pelt.flower_accessories),
                        choice(Pelt.plant2_accessories), choice(Pelt.snake_accessories),
                        choice(Pelt.smallAnimal_accessories), choice(Pelt.deadInsect_accessories),
                        choice(Pelt.aliveInsect_accessories), choice(Pelt.fruit_accessories),
                        choice(Pelt.crafted_accessories), choice(Pelt.tail2_accessories), choice(Pelt.bone_accessories),
                        choice(Pelt.butterflies_accessories), choice(Pelt.stuff_accessories),
                        choice(Pelt.ster_accessories)])]
        else:
            self.accessory = []

    def init_pattern(self, parents, gender):
        base_game_patterns = [
            "tabby", "ticked", "mackerel", "classic", "sokoke", "agouti", "speckled", "rosette", "single", "smoke",
            "singlestripe", "bengal", "marbled"
        ]

        if self.name in Pelt.torties:
            if not self.tortiebase:
                self.tortiebase = choice(Pelt.tortiebases)
            if not self.pattern:
                chosen_pattern = set()
                chosen_pattern.add(choice(Pelt.tortiepatterns))

                num = constants.CONFIG["cat_generation"]["base_extra_tortie"]

                for x in range(constants.CONFIG["cat_generation"]["max_tortie_amount"] - 1):
                    if not random.randint(0, num):

                        chosen_pattern.add(choice(Pelt.tortiepatterns))
                        num += 3

                self.pattern = list(chosen_pattern)

            self.displays_2nd_tortie = True if randint(1, constants.CONFIG["cat_generation"]["double_tortie"]) == 1 else False
            if not self.pattern2:
                chosen_pattern = set()
                chosen_pattern.add(choice(Pelt.tortiepatterns))

                num = constants.CONFIG["cat_generation"]["base_extra_tortie"] - int(constants.CONFIG["cat_generation"]["base_extra_tortie"] / 3)

                for x in range(constants.CONFIG["cat_generation"]["max_tortie_amount"] - 1):
                    if not random.randint(0, num):
                        chosen_pattern.add(choice(Pelt.tortiepatterns))
                        num += 3

                self.pattern2 = list(chosen_pattern)

            wildcard_chance = constants.CONFIG["cat_generation"]["wildcard_tortie"]

            if parents:
                for p in parents:
                    if Pelt.check_wildcard(p.pelt.name, p.pelt.colour, p.pelt.tortiebase, p.pelt.tortiecolour,
                                           p.pelt.tortiepattern) is True:
                        wildcard_chance /= 2

            if gender == "male":
                print("Male tortie!")
                wildcard_chance /= 3
                wildcard_chance = int(wildcard_chance)

            if wildcard_chance <= 1:
                wildcard_chance = 2

            if self.colour:
                # This is the "wildcard" chance, where you can get funky combinations.
                # The "not wildcard_chance" allows users to set wildcard_tortie to 0,
                # and always get wildcard torties.
                if not wildcard_chance or random.getrandbits(wildcard_chance) == 1:
                    self.tortiecolour = choice(Pelt.pelt_colours)
                    if self.colour == self.tortiecolour:
                        possible_patterns = Pelt.tortiebases.copy()
                        possible_patterns.remove(self.tortiebase)
                        self.tortiepattern = choice(possible_patterns)
                    else:
                        self.tortiepattern = choice(Pelt.tortiebases)

                    self.tortiecolour2 = choice(Pelt.pelt_colours)
                    if self.colour == self.tortiecolour2:
                        possible_patterns = Pelt.tortiebases.copy()
                        possible_patterns.remove(self.tortiebase)
                        self.tortiepattern2 = choice(possible_patterns)
                    elif self.tortiecolour == self.tortiecolour2:
                        possible_patterns = Pelt.tortiebases.copy()
                        possible_patterns.remove(self.tortiepattern)
                        self.tortiepattern2 = choice(possible_patterns)
                    else:
                        self.tortiepattern2 = choice(Pelt.tortiebases)

                    # people are fans of the print message, so I'm putting it back
                    print(f"Wildcard tortie!\n\ncolor: {self.colour}\ntortie_base: {self.tortiebase}\n\n\nFIRST:\n\npattern(s): {str(self.pattern)}\ntortie_color: {self.tortiecolour}\ntortie_pattern: {self.tortiepattern}\n\n\nSECOND:\n\npattern(s): {str(self.pattern2)}\ntortie_color: {self.tortiecolour2}\ntortie_pattern: {self.tortiepattern2}")
                else:
                    # Normal generation
                    if self.tortiebase in ("singlestripe", "smoke", "single", "smokepoint"):
                        self.tortiepattern = choice(
                            [
                                "tabby",
                                "mackerel",
                                "classic",
                                "single",
                                "smoke",
                                "agouti",
                                "ticked",
                                "brindle",
                                "spots"
                            ]
                        )
                        self.tortiepattern2 = choice(
                            [
                                "tabby",
                                "mackerel",
                                "classic",
                                "single",
                                "smoke",
                                "agouti",
                                "ticked",
                                "brindle",
                                "spots"
                            ]
                        )
                    else:
                        self.tortiepattern = random.choices(
                            [self.tortiebase, "single"], weights=[97, 3], k=1
                        )[0]
                        self.tortiepattern2 = random.choices(
                            [self.tortiebase, "single"], weights=[97, 3], k=1
                        )[0]

                    if self.colour == "WHITE":
                        possible_colors = Pelt.white_colours.copy()
                        possible_colors.remove("WHITE")
                        self.colour = choice(possible_colors)

                    # Ginger is often duplicated to increase its chances
                    if (self.colour in Pelt.black_colours) or (
                        self.colour in Pelt.white_colours
                    ):
                        self.tortiecolour = choice(
                            (Pelt.ginger_colours * 2) + Pelt.brown_colours
                        )
                    elif self.colour in Pelt.ginger_colours:
                        self.tortiecolour = choice(
                            Pelt.brown_colours + Pelt.black_colours * 2
                        )
                    elif self.colour in Pelt.brown_colours:
                        possible_colors = Pelt.brown_colours.copy()
                        possible_colors.remove(self.colour)
                        possible_colors.extend(
                            Pelt.black_colours + (Pelt.ginger_colours * 2)
                        )
                        self.tortiecolour = choice(possible_colors)
                    else:
                        self.tortiecolour = "GOLDEN"

                    if (self.colour in Pelt.black_colours) or (
                            self.colour in Pelt.white_colours
                    ):
                        self.tortiecolour2 = choice(
                            (Pelt.ginger_colours * 2) + Pelt.brown_colours
                        )
                    elif self.colour in Pelt.ginger_colours:
                        self.tortiecolour2 = choice(
                            Pelt.brown_colours + Pelt.black_colours * 2
                        )
                    elif self.colour in Pelt.brown_colours:
                        possible_colors = Pelt.brown_colours.copy()
                        possible_colors.remove(self.colour)
                        possible_colors.extend(
                            Pelt.black_colours + (Pelt.ginger_colours * 2)
                        )
                        self.tortiecolour2 = choice(possible_colors)
                    else:
                        self.tortiecolour2 = "GOLDEN"

            else:
                self.tortiecolour = "GOLDEN"
                self.tortiecolour2 = "GOLDEN"
        else:
            self.tortiebase = None
            self.tortiepattern = None
            self.tortiecolour = None
            self.pattern = None
            self.displays_2nd_tortie = False
            self.tortiepattern2 = None
            self.tortiecolour2 = None
            self.pattern2 = None
            return

        if self.tortiebase not in base_game_patterns:
            if self.colour not in Pelt.pelt_colours:
                self.colour = choice(Pelt.pelt_colours)

        if self.tortiepattern not in base_game_patterns:
            if self.tortiecolour not in Pelt.pelt_colours:
                self.tortiecolour = choice(Pelt.pelt_colours)

    def white_patches_inheritance(self, parents: tuple):
        par_whitepatches = set()
        par_points = []
        for p in parents:
            if p:
                if p.pelt.white_patches:
                    par_whitepatches.add(choice(p.pelt.white_patches))
                if p.pelt.points:
                    par_points.append(p.pelt.points)

        if not parents:
            print("Error - no parents. Randomizing white patches.")
            self.randomize_white_patches()
            return

        # Direct inheritance. Will only work if at least one parent has white patches, otherwise continue on.
        if par_whitepatches and constants.CONFIG["cat_generation"]["direct_inheritance"] != 0 and not random.randint(
            0, constants.CONFIG["cat_generation"]["direct_inheritance"]
        ):
            # This ensures Torties and Calicos won't get direct inheritance of incorrect white patch types
            _temp = par_whitepatches.copy()
            if self.name == "Tortie":
                for p in _temp.copy():
                    if p in Pelt.high_white + Pelt.mostly_white + ["FULLWHITE"]:
                        _temp.remove(p)
            elif self.name == "Calico":
                for p in _temp.copy():
                    if p in Pelt.little_white + Pelt.mid_white:
                        _temp.remove(p)

            chosen_white_patches = set()
            # Only proceed with the direct inheritance if there are white patches that match the pelt.
            if _temp:
                chosen_white_patches.add(choice(list(_temp)))
                for x in range(constants.CONFIG["cat_generation"]["max_white_amount"] - 1):
                    if not random.randint(0, constants.CONFIG["cat_generation"]["base_extra_white"]):
                        for p in chosen_white_patches:
                            if p in _temp:
                                _temp.remove(p)
                        if _temp:
                            chosen_white_patches.add(choice(list(_temp)))

                self.white_patches = list(chosen_white_patches)
                # Direct inheritance also effect the point marking.
                if par_points:
                    self.points = choice(par_points)
                else:
                    self.points = None

                return

        # dealing with points
        if par_points:
            chance = 10 - len(par_points)
        else:
            chance = 40
        # Chance of point is 1 / chance.
        if not int(random.random() * chance):
            self.points = choice(Pelt.point_markings)
        else:
            self.points = None

        white_list = [
            Pelt.little_white,
            Pelt.mid_white,
            Pelt.high_white,
            Pelt.mostly_white,
            ["FULLWHITE"],
        ]

        weights = [0, 0, 0, 0, 0]  # Same order as white_list
        for p_ in par_whitepatches:
            if p_ in Pelt.little_white:
                add_weights = (40, 20, 15, 5, 0)
            elif p_ in Pelt.mid_white:
                add_weights = (10, 40, 15, 10, 0)
            elif p_ in Pelt.high_white:
                add_weights = (15, 20, 40, 10, 1)
            elif p_ in Pelt.mostly_white:
                add_weights = (5, 15, 20, 40, 5)
            elif p_ == "FULLWHITE":
                add_weights = (0, 5, 15, 40, 10)
            else:
                add_weights = (0, 0, 0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weights[x]

        # If all the weights are still 0, that means none of the parents have white patches.
        if not any(weights):
            if not all(
                parents
            ):  # If any of the parents are None (unknown), use the following distribution:
                weights = [20, 10, 10, 5, 0]
            else:
                # Otherwise, all parents are known and don't have any white patches. Focus distribution on little_white.
                weights = [50, 5, 0, 0, 0]

        # Adjust weights for torties, since they can't have anything greater than mid_white:
        if self.name == "Tortie":
            weights = weights[:2] + [0, 0, 0]
            # Another check to make sure not all the values are zero. This should never happen, but better
            # safe than sorry.
            if not any(weights):
                weights = [2, 1, 0, 0, 0]
        elif self.name == "Calico":
            weights = [0, 0, 0] + weights[3:]
            # Another check to make sure not all the values are zero. This should never happen, but better
            # safe than sorry.
            if not any(weights):
                weights = [2, 1, 0, 0, 0]

        chosen_white_patches = set()
        chosen_white_patches.add(choice(
            random.choices(white_list, weights=weights, k=1)[0]
        ))

        num = constants.CONFIG["cat_generation"]["base_extra_white"]

        if any(white in Pelt.high_white for white in chosen_white_patches):
            num -= 2
        elif any(white in Pelt.little_white for white in chosen_white_patches) or any(white in Pelt.mid_white for white in chosen_white_patches):
            num -= 5

        for p in parents:
            if p:
                if not p.pelt.white_patches:
                    num += 1
                elif len(p.pelt.white_patches) >= 2:
                    num -= 1

        if num < 0:
            num = 1

        for x in range(constants.CONFIG["cat_generation"]["max_white_amount"] - 1):
            if not random.randint(0, num):

                weights = (12, 10, 3, 0, 0)
                chosen_white_patches.add(choice(
                    random.choices(white_list, weights=weights, k=1)[0]
                ))
                num += 1

        self.white_patches = list(chosen_white_patches)

    def randomize_white_patches(self):
        # Points determination. Tortie can't be pointed
        if not random.getrandbits(
            constants.CONFIG["cat_generation"]["random_point_chance"]
        ):
            # Cat has colorpoint!
            self.points = choice(Pelt.point_markings)
        else:
            self.points = None

        # Adjust weights for torties, since they can't have anything greater than mid_white:
        if self.name == "Tortie":
            weights = (2, 1, 0, 0, 0)
        elif self.name == "Calico":
            weights = (0, 0, 20, 15, 1)
        else:
            weights = (10, 10, 10, 10, 1)

        chosen_white_patches = set()
        white_list = [Pelt.little_white, Pelt.mid_white, Pelt.high_white, Pelt.mostly_white, ['FULLWHITE']]
        chosen_white_patches.add(choice(
            random.choices(white_list, weights=weights, k=1)[0]
        ))

        num = constants.CONFIG["cat_generation"]["base_extra_white"]
        highest_white = ""
        if chosen_white_patches:
            for patch in chosen_white_patches:
                if patch in Pelt.little_white and highest_white not in ["little", "mid", "high", "mostly", "full"]:
                    highest_white = "little"
                if patch in Pelt.mid_white and highest_white not in ["mid", "high", "mostly", "full"]:
                    highest_white = "mid"
                if patch in Pelt.high_white and highest_white not in ["high", "mostly", "full"]:
                    highest_white = "high"
                if patch in Pelt.mostly_white and highest_white not in ["mostly", "full"]:
                    highest_white = "mostly"
                if patch == "FULLWHITE" and highest_white != "full":
                    highest_white = "full"
                    break

        if highest_white == "high":
            num -= 2
        elif highest_white in ["little", "mid"]:
            num -= 5

        if num < 0:
            num = 1

        if highest_white != "full":
            for x in range(constants.CONFIG["cat_generation"]["max_white_amount"] - 1):
                if not random.randint(0, num):

                    weights = (12, 10, 3, 0, 0)
                    chosen_white_patches.add(choice(
                        random.choices(white_list, weights=weights, k=1)[0]
                    ))
                    num += 1

        self.white_patches = list(chosen_white_patches)
        if len(self.white_patches) > 1 and "FULLWHITE" in self.white_patches:
            self.white_patches = ["FULLWHITE"]

    def init_white_patches(self, pelt_white, parents: tuple):
        # Vit can roll for anyone, not just cats who rolled to have white in their pelt.
        par_vit = []
        for p in parents:
            if p:
                if p.pelt.vitiligo:
                    par_vit.append(p.pelt.vitiligo)

        vit_chance = max(
            constants.CONFIG["cat_generation"]["vit_chance"] - len(par_vit), 0
        )
        if not random.getrandbits(vit_chance):
            self.vitiligo = choice(Pelt.vit)

        # If the cat was rolled previously to have white patches, then determine the patch they will have
        # these functions also handle points.
        if pelt_white:
            if parents:
                self.white_patches_inheritance(parents)
            else:
                self.randomize_white_patches()
        else:
            self.white_patches = None
            self.points = None

    def init_tint(self):
        """Sets tint for pelt and white patches"""

        # PELT TINT
        # Basic tints as possible for all colors.
        base_tints = sprites.cat_tints["possible_tints"]["basic"]
        if self.colour in sprites.cat_tints["colour_groups"]:
            color_group = sprites.cat_tints["colour_groups"].get(self.colour, "warm")
            color_tints = sprites.cat_tints["possible_tints"][color_group]
        else:
            color_tints = []

        '''
        if base_tints or color_tints:
            self.tint = choice(base_tints + color_tints)
        else:
            self.tint = "none"
        '''

        self.tint = "none"
        weighted_tints = sprites.cat_tints["weighted_tints"]
        all_tints = weighted_tints["dilute"] + weighted_tints["light_cool"] + weighted_tints["cool"] + weighted_tints["dark_cool"] + weighted_tints["light_warm"] + weighted_tints["warm"] + weighted_tints["dark_warm"] + weighted_tints["black"]

        self.tint = choice([choice(weighted_tints["dilute"]), choice(weighted_tints["light_cool"]), choice(weighted_tints["light_warm"]), choice(all_tints)])

        # TORTIE TINT
        # Basic tints as possible for all colors.
        if self.name in ["Tortie", "Calico"]:
            base_tints = sprites.cat_tints["possible_tints"]["basic"]
            if self.tortiecolour in sprites.cat_tints["colour_groups"]:
                color_group = sprites.cat_tints["colour_groups"].get(self.tortiecolour, "warm")
                color_tints = sprites.cat_tints["possible_tints"][color_group]
            else:
                color_tints = []

            while self.tint in base_tints:
                if self.tint not in base_tints:
                    break
                base_tints.remove(self.tint)
            while self.tint in color_tints:
                if self.tint not in color_tints:
                    break
                color_tints.remove(self.tint)

            if (base_tints or color_tints) and random.randint(1, 10) == 1:
                self.tortie_tint = choice(base_tints + color_tints)
            else:
                self.tortie_tint = self.tint
        else:
            self.tortie_tint = "none"

        if self.name in ["Tortie", "Calico"]:
            base_tints = sprites.cat_tints["possible_tints"]["basic"]
            if self.tortiecolour2 in sprites.cat_tints["colour_groups"]:
                color_group = sprites.cat_tints["colour_groups"].get(self.tortiecolour2, "warm")
                color_tints = sprites.cat_tints["possible_tints"][color_group]
            else:
                color_tints = []

            while self.tint in base_tints:
                if self.tint not in base_tints:
                    break
                base_tints.remove(self.tint)
            while self.tint in color_tints:
                if self.tint not in color_tints:
                    break
                color_tints.remove(self.tint)

            if (base_tints or color_tints) and random.randint(1, 10) == 1:
                self.tortie_tint2 = choice(base_tints + color_tints)
            else:
                self.tortie_tint2 = self.tint
        else:
            self.tortie_tint2 = "none"

        # WHITE PATCHES TINT
        if self.white_patches or self.points or self.vitiligo:
            # Now for white patches
            base_tints = sprites.white_patches_tints["possible_tints"]["basic"]
            if self.colour in sprites.cat_tints["colour_groups"]:
                color_group = sprites.white_patches_tints["colour_groups"].get(
                    self.colour, "white"
                )
                color_tints = sprites.white_patches_tints["possible_tints"][color_group]
            else:
                color_tints = []

            if base_tints or color_tints:
                all_whitetints = base_tints + color_tints + sprites.white_patches_tints["possible_tints"]["dark"]
                self.white_patches_tint = choice(base_tints + base_tints + color_tints + color_tints + all_whitetints)
            else:
                self.white_patches_tint = "none"
        else:
            self.white_patches_tint = "none"

        if type(self.tint) != list:
            self.tint = [self.tint]
        if type(self.tortie_tint) != list:
            self.tortie_tint = [self.tortie_tint]
        if type(self.tortie_tint2) != list:
            self.tortie_tint2 = [self.tortie_tint2]
        if type(self.white_patches_tint) != list:
            self.white_patches_tint = [self.white_patches_tint]

    def init_physical_traits(self, parents: tuple = ()):
        trait_categories = [
            Pelt.physical_trait_teeth,
            Pelt.physical_trait_ear_type,
            Pelt.physical_trait_ear_fold,
            Pelt.physical_trait_headfur,
            Pelt.physical_trait_cheekfur,
            Pelt.physical_trait_mane,
            Pelt.physical_trait_fur_type,
            Pelt.physical_trait_muzzle_type,
            Pelt.physical_trait_tail,
            Pelt.physical_trait_bodyfur,
            Pelt.physical_trait_misc
        ]

        trait_pool = [(trait, category) for category in trait_categories for trait in category]

        par_traits = set()
        for p in parents:
            par_traits.add(p.pelt.physical_trait_1)
            par_traits.add(p.pelt.physical_trait_2)
            par_traits.add(p.pelt.physical_trait_3)
            par_traits.add(p.pelt.physical_trait_4)
            par_traits.add(p.pelt.physical_trait_hidden)
            par_traits.add(p.pelt.physical_trait_hidden_2)
            par_traits.add(p.pelt.physical_trait_hidden_3)
            par_traits.add(p.pelt.physical_trait_hidden_4)

        # Remove any None values from par_traits
        par_traits.discard(None)

        if par_traits:
            # Check for conflicting traits from the same category
            for category in trait_categories:
                clash_traits = par_traits.intersection(category)
                if len(clash_traits) > 1:
                    chosen_trait = random.choice(list(clash_traits))
                    par_traits = par_traits.difference(clash_traits)
                    par_traits.add(chosen_trait)
            inherit_trait_chance = int(random.random() * 100)
            if inherit_trait_chance <= constants.CONFIG["cat_generation"]["physical_trait_inherit_chance"]:
                # Roll to inherit first trait, and if so, remove it from the list
                self.physical_trait_1 = random.choice(list(par_traits))
                par_traits.remove(self.physical_trait_1)
                if len(par_traits) > 0:
                    # If we have a first trait, roll to inherit a second, and if we do, remove it from the list
                    inherit_trait_chance = int(random.random() * 100)
                    if inherit_trait_chance <= constants.CONFIG["cat_generation"]["physical_trait_inherit_chance"]:
                        self.physical_trait_2 = random.choice(list(par_traits))
                        par_traits.remove(self.physical_trait_2)
                        if len(par_traits) > 0:
                            # If we have a second trait, roll to inherit a third, and if we do, remove it from the list
                            inherit_trait_chance = int(random.random() * 100)
                            if inherit_trait_chance <= constants.CONFIG["cat_generation"]["physical_trait_inherit_chance"]:
                                self.physical_trait_3 = random.choice(list(par_traits))
                                par_traits.remove(self.physical_trait_3)
                                if len(par_traits) > 0:
                                    # If we have a third trait, roll to inherit a fourth, and if we do, remove it from
                                    # the list
                                    inherit_trait_chance = int(random.random() * 100)
                                    if inherit_trait_chance <= constants.CONFIG["cat_generation"]["physical_trait_inherit_chance"]:
                                        self.physical_trait_4 = random.choice(list(par_traits))
                                        par_traits.remove(self.physical_trait_4)
            if len(par_traits) > 0:
                # If there are still leftover traits, roll to inherit as hidden with a +50% chance
                inherit_trait_chance = int((random.random() * 100) - 50)
                if inherit_trait_chance <= constants.CONFIG["cat_generation"]["physical_trait_inherit_chance"]:
                    self.physical_trait_hidden = random.choice(list(par_traits))
                    par_traits.remove(self.physical_trait_hidden)
                    if len(par_traits) > 0:
                        # If there are still leftover traits, roll to inherit as hidden with a +50% chance
                        inherit_trait_chance = int((random.random() * 100) - 50)
                        if inherit_trait_chance <= constants.CONFIG["cat_generation"]["physical_trait_inherit_chance"]:
                            self.physical_trait_hidden_2 = random.choice(list(par_traits))
                            par_traits.remove(self.physical_trait_hidden_2)
                            if len(par_traits) > 0:
                                # If there are still leftover traits, roll to inherit as hidden with a +50% chance
                                inherit_trait_chance = int((random.random() * 100) - 50)
                                if inherit_trait_chance <= constants.CONFIG["cat_generation"]["physical_trait_inherit_chance"]:
                                    self.physical_trait_hidden_3 = random.choice(list(par_traits))
                                    par_traits.remove(self.physical_trait_hidden_3)
                                    if len(par_traits) > 0:
                                        # If there are still leftover traits, roll to inherit as hidden with a +50%
                                        # chance
                                        inherit_trait_chance = int((random.random() * 100) - 50)
                                        if inherit_trait_chance <= constants.CONFIG["cat_generation"]["physical_trait_inherit_chance"]:
                                            self.physical_trait_hidden_4 = random.choice(list(par_traits))
                                            par_traits.remove(self.physical_trait_hidden_4)
            
        # Giving cats that inherited nothing a 50% of base chance roll for new traits
        if not self.physical_trait_1:
            trait_chance = int(random.random() * 100)
            if trait_chance <= constants.CONFIG["cat_generation"]["physical_trait_chance"]:
                if trait_chance <= (0.5 * constants.CONFIG["cat_generation"]["physical_trait_chance"]):
                    traitcount = 2
                    trait_chance = int(random.random() * 100)
                    if trait_chance <= (0.5 * constants.CONFIG["cat_generation"]["physical_trait_chance"]):
                        traitcount = 3
                        trait_chance = int(random.random() * 100)
                        if trait_chance <= (0.5 * constants.CONFIG["cat_generation"]["physical_trait_chance"]):
                            traitcount = 4
                else:
                    traitcount = 1
            else:
                traitcount = 0
                
            if traitcount > 0:
                # Select the first trait and its category
                trait1, category1 = random.choice(trait_pool)
                self.physical_trait_1 = trait1
                
                # Remove traits from the same category as the first trait
                trait_pool = [(trait, category) for trait, category in trait_pool if category != category1]
                
                if traitcount >= 2 and trait_pool:
                    # Select the second trait from the remaining pool
                    trait2, category2 = random.choice(trait_pool)
                    self.physical_trait_2 = trait2
                    
                    # Remove traits from the same category as the second trait
                    trait_pool = [(trait, category) for trait, category in trait_pool if category != category2]
                    
                    if traitcount >= 3 and trait_pool:
                        # Select the third trait from the remaining pool
                        trait3, category3 = random.choice(trait_pool)
                        self.physical_trait_3 = trait3
                        
                        # Remove traits from the same category as the third trait
                        trait_pool = [(trait, category) for trait, category in trait_pool if category != category3]
                        
                        if traitcount == 4 and trait_pool:
                            # Select the fourth trait from the remaining pool
                            trait4, category4 = random.choice(trait_pool)
                            self.physical_trait_4 = trait4
                        else:
                            self.physical_trait_4 = None
                    else:
                        self.physical_trait_3 = None
                        self.physical_trait_4 = None
                else:
                    self.physical_trait_2 = None
                    self.physical_trait_3 = None
                    self.physical_trait_4 = None
            else:
                self.physical_trait_1 = None
                self.physical_trait_2 = None
                self.physical_trait_3 = None
                self.physical_trait_4 = None

    @staticmethod
    def check_wildcard(pelt_type, base_color, base_pattern, tortie_color, tortie_pattern):
        if pelt_type not in Pelt.torties:
            return False

        # Pattern
        if base_pattern in ["singlestripe", "smoke", "single", "smokepoint"]:
            if tortie_pattern not in ["tabby", "mackerel", "classic", "single", "smoke", "agouti", "ticked", "brindle",
                                      "spots"]:
                return True
        elif tortie_pattern not in [f"{base_pattern}", "single"]:
            return True

        # Color
        if base_color == "WHITE":
            return True
        elif base_color in Pelt.black_colours or base_color in Pelt.white_colours:
            if tortie_color not in Pelt.ginger_colours and tortie_color not in Pelt.brown_colours:
                return True
        elif base_color in Pelt.ginger_colours:
            if tortie_color not in Pelt.brown_colours and tortie_color not in Pelt.black_colours:
                return True
        elif base_color in Pelt.brown_colours:
            if base_color == tortie_color or (
                    tortie_color not in Pelt.brown_colours and
                    tortie_color not in Pelt.black_colours and
                    tortie_color not in Pelt.ginger_colours
            ):
                return True

        return False

    @property
    def white(self):
        return self.white_patches or self.points

    @white.setter
    def white(self, val):
        print("Can't set pelt.white")
        return

    def describe_eyes(self):
        return (
            adjust_list_text(
                [
                    i18n.t(f"cat.eyes.{self.eye_colour}"),
                    i18n.t(f"cat.eyes.{self.eye_colour2}"),
                ]
            )
            if self.eye_colour2
            else i18n.t(f"cat.eyes.{self.eye_colour}")
        )

    @staticmethod
    def describe_appearance(cat, short=False):
        """Return a description of a cat

        :param Cat cat: The cat to describe
        :param bool short: Whether to return a heavily-truncated description, default False
        :return str: The cat's description
        """

        config = get_lang_config()["description"]
        ruleset = config["ruleset"]
        output = []
        pelt_pattern, pelt_color = _describe_pattern(cat, short)
        for rule, args in ruleset.items():
            temp = unpack_appearance_ruleset(cat, rule, short, pelt_pattern, pelt_color)

            if args == "" or temp == "":
                output.append(temp)
                continue

            # handle args
            argpool = {
                arg: unpack_appearance_ruleset(
                    cat, arg, short, pelt_pattern, pelt_color
                )
                for arg in args
            }
            argpool["key"] = temp
            argpool["count"] = 1 if short else 2
            output.append(i18n.t(**argpool))

        # don't forget the count argument!
        groups = []
        for grouping in config["groups"]:
            temp = ""
            items = [
                i18n.t(output[i], count=1 if short else 2)
                for i in grouping["values"]
                if output[i] != ""
            ]
            if len(items) == 0:
                continue
            if "pre_value" in grouping:
                temp = grouping["pre_value"]

            if grouping["format"] == "list":
                temp += adjust_list_text(items)
            else:
                temp += grouping["format"].join(items)

            if "post_value" in grouping:
                temp += grouping["post_value"]
            groups.append(temp)

        return "".join(groups)

    def get_sprites_name(self):
        return Pelt.sprites_names[self.name]


def _describe_pattern(cat, short=False):
    color_name = [f"cat.pelts.{str(cat.pelt.colour)}"]
    pelt_name = f"cat.pelts.{cat.pelt.name}{'' if short else '_long'}"
    if cat.pelt.name in Pelt.torties:
        pelt_name, color_name = _describe_torties(cat, color_name, short)

    color_name = [i18n.t(piece, count=1) for piece in color_name]
    color_name = "".join(color_name)

    if cat.pelt.white_patches:
        if cat.pelt.white_patches == "FULLWHITE":
            # If the cat is fullwhite, discard all other information. They are just white
            color_name = i18n.t("cat.pelts.FULLWHITE")
            pelt_name = ""
        elif cat.pelt.name != "Calico":
            white = i18n.t("cat.pelts.FULLWHITE")
            if i18n.t("cat.pelts.WHITE", count=1) in color_name:
                color_name = white
            elif cat.pelt.white_patches in Pelt.mostly_white:
                color_name = adjust_list_text([white, color_name])
            else:
                color_name = adjust_list_text([color_name, white])

    if cat.pelt.points:
        color_name = i18n.t("cat.pelts.point", color=color_name)
        if "ginger point" in color_name:
            color_name.replace("ginger point", "flame point")
            # look, I'm leaving this as a quirk of the english language, if it's a problem elsewhere lmk

    return pelt_name, color_name


def _describe_torties(cat, color_name, short=False) -> [str, str]:
    # Calicos and Torties need their own desciptions
    if short:
        # If using short, don't describe the colors of calicos and torties.
        # Just call them calico, tortie, or mottled
        if (
            cat.pelt.colour
            in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours
            and cat.pelt.tortiecolour
            in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours
        ):
            return "cat.pelts.mottled", ""
        else:
            return f"cat.pelts.{cat.pelt.name}", ""

    base = cat.pelt.tortiebase.lower()

    patches_color = f"cat.pelts.{cat.pelt.tortiecolour}"
    color_name.append("/")
    color_name.append(patches_color)

    if (
        cat.pelt.colour in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours
        and cat.pelt.tortiecolour
        in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours
    ):
        return "cat.pelts.mottled_long", color_name
    else:
        if base in tuple(tabby.lower() for tabby in Pelt.tabbies) + (
            "bengal",
            "rosette",
            "speckled",
        ):
            base = f"cat.pelts.{cat.pelt.tortiebase.capitalize()}_long"  # the extra space is intentional
        else:
            base = ""
        return base, color_name


_scar_details = [
    "NOTAIL",
    "HALFTAIL",
    "NOPAW",
    "NOLEFTEAR",
    "NORIGHTEAR",
    "NOEAR",
]


def unpack_appearance_ruleset(cat, rule, short, pelt, color):
    if rule == "scarred":
        if not short and len(cat.pelt.scars) >= 3:
            return "cat.pelts.scarred"
    elif rule == "fur_length":
        if not short and cat.pelt.length == "long":
            return "cat.pelts.long_furred"
    elif rule == "pattern":
        return pelt
    elif rule == "color":
        return color
    elif rule == "cat":
        if cat.genderalign in ("female", "trans female"):
            return "general.she-cat"
        elif cat.genderalign in ("male", "trans male"):
            return "general.tom"
        else:
            return "general.cat"
    elif rule == "vitiligo":
        if not short and cat.pelt.vitiligo:
            return "cat.pelts.vitiligo"
    elif rule == "amputation":
        if not short:
            scarlist = []
            for scar in cat.pelt.scars:
                if scar in _scar_details:
                    scarlist.append(i18n.t(f"cat.pelts.{scar}"))
            return (
                adjust_list_text(list(set(scarlist))) if len(scarlist) > 0 else ""
            )  # note: this doesn't preserve order!
    else:
        raise Exception(f"Unmatched ruleset item {rule} in describe_appearance!")
    return ""
