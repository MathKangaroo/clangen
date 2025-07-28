from copy import copy
import random
from random import randint, choice


import os.path

import pygame
import ujson
import pygame_gui
from pygame import Rect
from pygame_gui.elements import UIDropDownMenu, UITextBox

from scripts.cat.cats import Cat
from scripts.cat.pelts import Pelt
from scripts.cat.sprites import sprites
from scripts.game_structure.game_essentials import game
from scripts.game_structure.screen_settings import MANAGER
from scripts.game_structure.ui_elements import UISurfaceImageButton, UIImageButton
from scripts.game_structure.game.switches import switch_set_value, switch_get_value, Switch
from ..game_structure.windows import CustomizeFilterWindow
from scripts.screens.Screens import Screens
from scripts.ui.generate_box import get_box, BoxStyles
from scripts.ui.generate_button import get_button_dict, ButtonStyles
from scripts.ui.get_arrow import get_arrow
from scripts.utility import ui_scale, generate_sprite, ui_scale_dimensions, get_text_box_theme, update_sprite

from scripts.game_structure.game.settings import game_setting_get

""" Cat customization UI """


# generate UI elements
def create_text_box(text, pos, size, theme, anchors=None):
    return UITextBox(
        text,
        ui_scale(Rect(pos, size)),
        manager=MANAGER,
        object_id=get_text_box_theme(theme),
        anchors=anchors
    )


def create_button(pos, size, text, style, anchors=None, sound_id=None):
    return UISurfaceImageButton(
        ui_scale(Rect(pos, size)),
        text,
        get_button_dict(style, size),
        object_id=f"@buttonstyles_{style.name.lower()}",
        manager=MANAGER,
        anchors=anchors,
        sound_id=sound_id
    )


def create_dropdown(pos, size, options, selected_option, style=None):
    return UIDropDownMenu(
        options,
        selected_option,
        ui_scale(Rect(pos, size)),
        object_id=f"#{style}",
        manager=MANAGER
    )


# creates a list with display names and values of cat pelt attributes
def create_options_list(attribute, case):
    if case == "upper":
        return [(option.capitalize(), option.upper()) for option in attribute]
    elif case == "lower":
        return [(option.capitalize(), option.lower()) for option in attribute]
    else:
        return [(option.capitalize(), option) for option in attribute]


# returns the name and value; returns none if dropdown is disabled
def get_selected_option(attribute, case, exception=False):
    if isinstance(attribute, list):
        if len(attribute) > 0:  # selects an option in scar dropdowns for any existing scars
            if exception:
                return attribute[0].capitalize(), attribute[0].lower()
            else:
                return attribute[0].capitalize(), attribute[0].upper()
        else:
            if exception:
                return "None", "none"
            else:
                return "None", "NONE"
    if attribute:
        if case == "upper":
            return attribute.capitalize(), attribute.upper()
        elif case == "lower":
            return attribute.capitalize(), attribute.lower()
        else:
            return attribute.capitalize(), attribute
    else:
        if case == "upper":
            return "None", "NONE"
        elif case == "lower":
            return "None", "none"
        else:
            return "None", "None"

# screen rendering
class CustomizeCatScreen(Screens):
    def __init__(self, name=None):
        super().__init__(name)
        self.the_cat = None
        self.next_cat = None
        self.previous_cat = None
        self.life_stage = None
        self.initial_state = None
        self.previous_pelt_name = None
        self.heterochromia = False
        self.initial_scar_selection = {}
        self.previous_scar_selection = {}
        self.cat_elements = {}

        # UI elements
        self.frame_image = None
        self.cat_image = None
        self.previous_cat_button = None
        self.back_button = None
        self.next_cat_button = None

        self.pelt_names = list(Pelt.sprites_names.keys())
        self.pelt_names.sort()
        self.pelt_name_label = None
        self.pelt_name_dropdown = None
        
        self.base_game_pelts = ["Tabby", "Ticked", "Mackerel", "Classic", "Sokoke", "Agouti", "Speckled",
                           "Rosette", "SingleColour", "Smoke", "Singlestripe", "Bengal", "Marbled"]
        self.base_game_colors = ['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK', 'CREAM', 'PALEGINGER',
                            'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA', 'LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN',
                            'CHOCOLATE']
        self.base_game_patterns = ["tabby", "ticked", "mackerel", "classic", "sokoke", "agouti", "speckled",
                           "rosette", "single", "smoke", "singlestripe", "bengal", "marbled"]
        
        minecraft_colors = [
            'ACACIALOG', 'BAMBOO', 'BIRCHLOG', 'CHERRYLOG', 'CRIMSONSTEM', 'DARKOAKLOG', 'JUNGLELOG', 'MANGROVELOG', 'OAKLOG', 'SPRUCELOG', 'WARPEDSTEM',
            'ACACIAPLANKS', 'BAMBOOPLANKS', 'BIRCHPLANKS', 'CHERRYPLANKS', 'CRIMSONPLANKS', 'DARKOAKPLANKS', 'JUNGLEPLANKS', 'MANGROVEPLANKS', 'OAKPLANKS', 'SPRUCEPLANKS', 'WARPEDPLANKS',
            'AMETHYST', 'BLACKGLAZEDTERRACOTTA', 'BLUEGLAZEDTERRACOTTA', 'BROWNGLAZEDTERRACOTTA', 'BROWN MUSHROOM', 'COPPER', 'CRYING OBSIDIAN', 'CYANGLAZEDTERRACOTTA', 'EXPOSEDCOPPER', 'GRAYGLAZEDTERRACOTTA', 'GREENGLAZEDTERRACOTTA',
            'LIGHTBLUEGLAZED TERRACOTTA', 'LIGHTGRAYGLAZEDTERRACOTTA', 'LIMEGLAZEDTERRACOTTA', 'MAGENTAGLAZEDTERRACOTTA', 'MUSHROOMINSIDE', 'MUSHROOMSTEM', 'OBSIDIAN', 'ORANGEGLAZEDTERRACOTTA', 'OXIDIZEDCOPPER', 'PINKGLAZEDTERRACOTTA', 'PURPLEGLAZEDTERRACOTTA',
            'PURPUR', 'QUARTZ', 'REDGLAZEDTERRACOTTA', 'REDMUSHROOM', 'WEATHEREDCOPPER', 'WHITEGLAZEDTERRACOTTA', 'YELLOWGLAZEDTERRACOTTA'
        ]
        
        anju_colors = ['PINK', 'RED', 'LIGHTGREEN', 'GREEN', 'CYAN', 'BLUE', 'PURPLE']
        
        cs2_colors = [
            'LIGHTLIME', 'PINKGREY', 'YELLOWBROWN', 'REDGREY', 'BLUEBROWN', 'GHOSTBROWN', 'BLACKPURPLE',
            'BLUECREAM', 'PALEPINKPURPLE', 'ICEBLUE', 'BLUECS2', 'GREENBROWN', 'NAVYBLUE',
            'PURPLECREAM', 'INDIGOBLUSH', 'VIOLETBLUSH', 'MAGENTA', 'NAVYBROWN', 'MULBERRY'
        ]
        
        cs_colors = [
                'ICEWHITE', 'CRYSTAL', 'ORCHID', 'CERULEAN', 'GRAPE', 'GHOSTBLUE', 'BLACKBLUE',
                'THISTLE', 'SUNYELLOW', 'BUBBLEGUM', 'REDSTAIN', 'ROSE', 'DUSKBROWN',
                'FROZENSUN', 'GREENGOLD', 'OCEAN', 'TEAL', 'REDBLUE', 'TREE'
        ]
        
        heta_colors = [
            'REDHETA', 'ORANGEHETA', 'YELLOWHETA', 'NEONYELLOW', 'NEONGREEN', 'GREENHETA', 'MINTGREEN',
            'DARKMINT', 'NEONTEAL','CYANHETA', 'BLUEHETA', 'NAVYHETA', 'INDIGOHETA',
            'PURPLEHETA', 'VIOLETHETA', 'MAGENTAHETA', 'PINKHETA', 'SCARLETPINK','DARKREDHETA'
        ]
        
        cs3_colors = [
            'BERBERIDA', 'RANUNCULA', 'CAPPARIDA', 'VIOLA', 'FUMARIA', 'PAPAVERA', 'MAGNOLIA', 
            'POLYGALA', 'RESEDA', 'CISTA', 'NYMPHEA', 'DIPTEROCARPA', 'DILLENIA', 'AMYGDALA', 
            'ANONA', 'MYRTA', 'TILIA', 'PITTOSPORA', 'MALVA', 'SARRACENIA', 'DROSERA', 
            'HIPPOCASTANA', 'TROPAEOLA', 'PASSIFLORA', 'OLACA', 'CRUCIA', 'LOASA', 'MALPIGHIA', 
            'MESEMBRYA', 'VITA', 'MARCGRAVIA', 'CLUSIA', 'BOMBA', 'SAMYDA', 'BIXA', 
            'GERANIA', 'COMPOSITA', 'RHAMNA', 'OXALIDA', 'ARALIA', 'TEREBINTHA', 'MELIA', 
            'SAXIFRAGA', 'LINA', 'CAPRIFOLIA', 'CARYOPHYLLA', 'LEGUMINOSAE', 'CAMELLIA', 'CACTACEA', 
            'JASMINEA', 'LYTHRA', 'ACANTHA', 'CRASSULA', 'RUBIA', 'HYPERICA', 'LORANTHA', 
            'AURANTIA', 'RHIZOPHORA', 'BORAGINA', 'TAMARICA', 'MELASTOMA', 'LECYTHIDA', 'VALERIANA', 
            'COMBRETA', 'APOCYNA', 'DIPSA', 'STYLIDIA', 'RUTA', 'SOLANA', 'PLUMBAGINA', 
            'LAMIA', 'BEGONIA', 'GROSSULARIA', 'GENTIANA', 'ERICA', 'CAMPANULA', 'POMA', 
            'BIGNONIA', 'AMARANTA', 'VACCINIA', 'ONAGRA', 'PRIMULA', 'SAPOTA', 'LOBELIA', 
            'MYRSINA', 'PORTULA', 'PLANTAGINA', 'ELAEAGNA', 'OLEA', 'POLEMONIA', 'ORCHIDA', 
            'EUPHORBIA', 'SCROPHULARIA', 'CONVOLVULA', 'MUSA', 'UTRICULARIA', 'UMBELLA', 'PROTEA', 
            'GOODENIA', 'THYMELA', 'URTICA', 'OROBANCHA', 'HYDROPHYLLA', 'AMARYLLIDA', 'CONIFERA', 
            'PHYTOLACCA', 'PAEONIA', 'IRIDA', 'DIOSCORA', 'GESNERIA', 'SANTALA', 'HYDROCHARIDA', 
            'ZINGIBERA', 'ALISMA', 'POLYGONA', 'NYCTAGINA', 'BROMELIA', 'SMILA', 'EBENA', 
            'ROSA', 'LILIA', 'JUNCA', 'VERBENA', 'HAEMODORA', 'COMMELINA', 'COLCHICA'
        ]

        
        
        #mega colors mod
        
        dance_colors = [
            'LIGHTCINNAMON', 'CINNAMON', 'SILVERFAWN', 'DARKCINNAMON', 'DARKFAWN','FAWN', 'LIGHTFAWN',
            'PALEFAWN', 'PALECREAM','LIGHTCREAM', 'DANCECREAM', 'DARKCREAM', 'DARKGOLD',
            'GOLD', 'LIGHTGOLD', 'SILVERCREAM', 'PALEGOLD', 'SUNSHINE','BRONZE'
        ]
        
        silly_colors = [
            'LIGHTLILAC', 'LILACSILLY', 'DARKLILAC', 'DARKASH', 'ASH', 'LIGHTASH', 'PALEASH',
            'SILVERCINNAMON', 'SILVERRED','PALEBROWN', 'LIGHTBROWNSILLY', 'BROWNSILLY', 'DARKBROWNSILLY',
            'EBONY', 'DARKCHOCOLATE', 'CHOCOLATESILLY', 'LIGHTCHOCOLATE', 'PALECHOCOLATE','PALECINNAMON'
        ]
        
        ster_colors = [
            'WHITESTER', 'PALEGREYSTER', 'LIGHTGREY', 'GREYSTER', 'DARKGREYSTER', 'BLACKSTER', 'OBSIDIANSTER',
            'GHOSTSTER', 'PALEBLUE','LIGHTBLUE', 'BLUESTER', 'DARKBLUE', 'SILVERCHOCOLATE',
            'SILVERORANGE', 'DARKSLATE', 'SLATE', 'LIGHTSLATE', 'PALESLATE','PALELILAC'
        ]
        
        mimi_colors = [
            'COPPERMIMI', 'DARKORANGE', 'ORANGE', 'LIGHTORANGE', 'PALEORANGE', 'PALEGINGERMIMI', 'LIGHTGINGER',
            'GINGERMIMI', 'DARKGINGERMIMI','SILVERGOLD', 'RUSSET', 'DARKRED', 'REDMIMI',
            'LIGHTRED', 'PALERED', 'SILVERMIMI', 'SILVERGREY', 'SILVERBLUE','SILVERSLATE'
        ]
        
        hive_colors = [
        'GREENH', 'TEALH', 'BLUEH', 'NAVYH', 'INDIGOH', 'PURPLEH', 'VIOLETH',
        'PINKH', 'ROSEH','DARKPINKH', 'REDH', 'ORANGEH', 'GOLDH',
        'PASTELPURPLEH', 'DARKGREENH', 'BROWN-PURPLE', 'YELLOWH', 'DARKMOSS','PURPLESWIRL'
        ]
        
        kris_colors = [
            'PINKCREAM', 'BLUEMINT', 'SUNSET', 'PINK-BLUE', 'INDIGOK', 'BLUEGHOSTK', 'PINKK',
            'PASTELPINKBLUE', 'RUSTYGREEN','OURPLE', 'BLUE-YELLOW', 'BLUE-PURPLE', 'DARKSUNSET',
            'BANANABERRY', 'BRIGHTBLUEK', 'SUNRISE', 'GREEN-NAVY', 'PINKSHADOW','REDK'
        ]
        
        meteor_colors = [
            'SILVERMETEOR', 'SILVERNAVY', 'CREAMSILVER', 'GREYSTAR', 'DARKGREYSTAR', 'BLACK-BROWN', 'BLUESPOTTED',
            'CREAMMETEOR', 'PINK-WHITE','TANSPOTTED', 'REVERSESUN', 'WARM-BLUE', 'INDIGO-VIOLET',
            'GREYMETEOR', 'ICESPOTTED', 'SHADOW', 'BLUE-EARTH', 'EARTHSPOTTED','BROWN-TAN'
        ]
        
        pastel_colors = [
            'PALEPINK-PURPLE', 'PALEGREY-PINK', 'PALEBLUE-YELLOW', 'PALEMINT-PURPLE', 'PALEGREEN-INDIGO', 'PALEYELLOW-INDIGO', 'PALEORANGE-BLUE',
            'PALEPURPLE-GOLD', 'PALECYAN-GOLD','PALEMINT-MAGENTA', 'PALEMINT-VIOLET', 'PALEGREEN-BLUE', 'PALEGREEN-NAVY',
            'PALEBLUE-INDIGO', 'PALECYAN-PURPLE', 'PALECYAN-NAVY', 'PALECYAN-BLUE', 'PALEYELLOWGREEN','PALEYELLOW-BLUE'
        ]
        
        pepper_colors = [
            'ICEPEPPER', 'CYANPEPPER', 'BLUEPEPPER', 'OCEANPEPPER', 'DARKBLUEPEPPER', 'BLUEGHOSTPEPPER', 'BLACKBLUEPEPPER',
            'GOLDCREAM', 'GOLDPEPPER','YELLOW-RED', 'BRIGHTYELLOW-RED', 'NEONRED', 'REDBLACK',
            'PALEBLUE-GOLD', 'INDIGOPEPPER', 'RUSTBLUEPEPPER', 'REDPEPPER', 'REDBLUEBLACK','SCARLETPEPPER'
        ]
        
        sparkle_colors = [
            'REDS', 'RED-ORANGES', 'DARKYELLOWS', 'GREENREDS', 'CYANPINKG', 'INDIGOREDS', 'REVERSERAINBOW',
            'PINKREDS', 'RUSTYS','GREENORANGES', 'REDCYANS', 'MINTBLUES', 'BLACKBLUES',
            'BANANAS', 'WHITEGREENS', 'BROWNREDS', 'RAINBOW', 'GREENDARKREDS','SUNNYS'
        ]
        
        self.special_colors_masked = mimi_colors + ster_colors + silly_colors + dance_colors + cs_colors + cs2_colors + cs3_colors + hive_colors + kris_colors + meteor_colors + sparkle_colors
        self.special_colors_nomasked = minecraft_colors + anju_colors + heta_colors + pastel_colors + pepper_colors

        self.pelt_colours = copy(Pelt.pelt_colours)
        self.white_patches = copy(Pelt.little_white + Pelt.mid_white + Pelt.high_white + Pelt.mostly_white)
        self.white_patches.append(Pelt.white_sprites[6]) # add fullwhite patch
        self.white_patches.sort()
        self.white_patches.insert(0, "None")
        self.white_patches_label = None
        self.white_patches_dropdown = None
        
        self.pelt_colours.sort()
        self.pelt_colour_label = None
        self.pelt_colour_dropdown = None

        self.patterns = copy(Pelt.tortiepatterns)
        self.patterns.sort()
        self.patterns.insert(0, "None")
        self.pattern_label = None
        self.pattern_dropdown = None

        self.tortie_bases = copy(Pelt.tortiebases)
        self.tortie_bases.sort()
        self.tortie_base_label = None
        self.tortie_base_dropdown = None

        self.tortie_colours = copy(Pelt.pelt_colours)
        self.tortie_colours.sort()
        self.tortie_colour_label = None
        self.tortie_colour_dropdown = None

        self.tortie_patterns = copy(Pelt.tortiepatterns)
        self.tortie_patterns.sort()
        self.tortie_pattern_label = None
        self.tortie_pattern_dropdown = None

        self.white_patches = copy(Pelt.little_white + Pelt.mid_white + Pelt.high_white + Pelt.mostly_white)
        self.white_patches.append(Pelt.white_sprites[6]) # add fullwhite patch
        self.white_patches.sort()
        self.white_patches.insert(0, "None")
        self.white_patches_label = None
        self.white_patches_dropdown = None

        self.vitiligo_patterns = copy(Pelt.vit)
        self.vitiligo_patterns.sort()
        self.vitiligo_patterns.insert(0, "None")
        self.vitiligo_label = None
        self.vitiligo_dropdown = None

        self.points_markings = copy(Pelt.point_markings)
        self.points_markings.sort()
        self.points_markings.insert(0, "None")
        self.points_label = None
        self.points_dropdown = None

        self.white_patches_tints =[tint for tint in list(sprites.white_patches_tints["tint_colours"].keys()) if tint != "none"]
        self.white_patches_tints.sort()
        self.white_patches_tints.insert(0, "None")
        self.white_patches_tint_label = None
        self.white_patches_tint_dropdown = None

        self.tints = [tint for tint in list(sprites.cat_tints["tint_colours"].keys()) +
                      list(sprites.cat_tints["dilute_tint_colours"].keys()) if tint != "none"]
        self.tints.insert(0, "None")
        self.tints.sort()
        self.tint_label = None
        self.tint_dropdown = None

        self.skins = copy(Pelt.skin_sprites)
        magic_skins = copy(Pelt.skin_sprites_magic) + copy(Pelt.skin_sprites_elemental) + copy(Pelt.skin_sprites_math) + copy(Pelt.skin_sprites_bingle) + copy(Pelt.skin_sprites_stain) + ['SHADOWSELF', 'FIRETAIL', 'BLUEFIRETAIL', 'SCORPION', 'SNOWFOX', 'KITSUNE', 'FENNECKITSUNE']
        magic_skins.sort()
        self.skins.sort()
        self.skins += magic_skins
        self.skin_label = None
        self.skin_dropdown = None

        self.reset_message = None
        self.reset_button = None
        self.sparkle_button = None
        self.sparkle_cats = True

        self.eye_colours = [colour.capitalize() for colour in copy(Pelt.eye_colours)]
        self.eye_colours.sort()
        self.eye_colour1_label = None
        self.eye_colour1_dropdown = None
        self.heterochromia_text = None
        self.eye_colour2_label = None
        self.eye_colour2_dropdown = None

        self.reverse_label = None
        self.reverse_button = None

        self.pelt_lengths = copy(Pelt.pelt_length)
        self.pelt_length_label = None
        self.pelt_length_left_button = None
        self.pelt_length_right_button = None

        self.poses = None
        self.pose_label = None
        self.pose_right_button = None
        self.pose_left_button = None

        self.accessories = list(
            dict.fromkeys(Pelt.plant_accessories + Pelt.flower_accessories + Pelt.bows_accessories + Pelt.plant2_accessories + Pelt.ster_accessories + Pelt.wild_accessories + Pelt.tail_accessories + Pelt.collars + Pelt.snake_accessories + Pelt.smallAnimal_accessories + Pelt.deadInsect_accessories + Pelt.aliveInsect_accessories + Pelt.fruit_accessories + Pelt.crafted_accessories + Pelt.tail2_accessories + Pelt.bone_accessories + Pelt.butterflies_accessories + Pelt.stuff_accessories + Pelt.toy_accessories + Pelt.blankie_accessories + Pelt.flag_accessories + Pelt.wheels + Pelt.booties + Pelt.randomaccessories + Pelt.sailormoon + Pelt.beetle_feathers + Pelt.beetle_accessories + Pelt.chime_accessories+ Pelt.lantern_accessories + Pelt.neckerchiefs +  Pelt.witchhats + Pelt.pokemon_accessories))
        self.accessories.sort()
        self.accessories.insert(0, "None")
        self.accessories += copy(Pelt.colorsplash_accessories)
        self.accessory_label = None
        self.accessory_dropdown = None

        self.scars = copy(Pelt.scars1 + Pelt.scars2 + Pelt.scars3)
        self.scars.sort()
        self.scars.insert(0, "None")
        self.scar_message = None
        self.scar1_label = None
        self.scar1_dropdown = None
        self.scar2_label = None
        self.scar2_dropdown = None
        self.scar3_label = None
        self.scar3_dropdown = None
        self.scar4_label = None
        self.scar4_dropdown = None
        
        self.eye_filter = "all"
        self.pelt_filter = "all"
        self.acc_filter = "all"
        self.white_filter = "all"
        

    # prints attributes for testing
    #def print_pelt_attributes(self):
        #print("\n*** PELT START ***")
        #pelt_attributes = vars(self.the_cat.pelt)
        #for attribute, value in pelt_attributes.items():
            #print(f"{attribute}: {value}")
        #print("*** PELT END ***")

    def screen_switches(self):
        super().screen_switches()
        self.setup_labels()
        self.frame_image = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((25, 120), (270, 270))), get_box(BoxStyles.FRAME, (250, 250)), starting_height=1
        )
        self.build_cat_page()

    def build_cat_page(self):
        self.the_cat = Cat.all_cats.get(switch_get_value(Switch.cat))
        (self.next_cat, self.previous_cat) = self.the_cat.determine_next_and_previous_cats()
        self.cat_elements["cat_name"] = create_text_box("customize " + str(self.the_cat.name), (0, 40), (400, 40),
                                                        "#text_box_34_horizcenter", {"centerx": "centerx"})
        self.setup_buttons()
        self.setup_next_and_previous_cat()
        self.setup_dropdowns()
        self.setup_cat()
        self.capture_initial_state()

    def setup_labels(self):
        """------------------------------------------------------------------------------------------------------------#
        #                                              LABEL SETUP START                                               #
        # ------------------------------------------------------------------------------------------------------------"""
        self.pelt_name_label = create_text_box("pelt name", (320, 100), (135, 40), "#text_box_22_horizleft")
        self.pelt_colour_label = create_text_box("pelt colour", (480, 100), (135, 40), "#text_box_22_horizleft")
        self.pelt_length_label = create_text_box("pelt length", (224, 500), (135, 40), "#text_box_22_horizleft")
        self.pattern_label = create_text_box("pattern", (640, 100), (135, 40), "#text_box_22_horizleft")
        self.tortie_base_label = create_text_box("tortie base", (320, 175), (135, 40), "#text_box_22_horizleft")
        self.tortie_colour_label = create_text_box("tortie colour", (480, 175), (135, 40), "#text_box_22_horizleft")
        self.tortie_pattern_label = create_text_box("tortie pattern", (640, 175), (135, 40), "#text_box_22_horizleft")
        self.white_patches_label = create_text_box("white patches", (320, 260), (135, 40), "#text_box_22_horizleft")
        self.vitiligo_label = create_text_box("vitiligo", (480, 260), (135, 40), "#text_box_22_horizleft")
        self.points_label = create_text_box("point", (640, 260), (135, 40), "#text_box_22_horizleft")
        self.white_patches_tint_label = create_text_box("white patches tint", (320, 335), (135, 40),
                                                        "#text_box_22_horizleft")
        self.tint_label = create_text_box("tint", (480, 335), (135, 40), "#text_box_22_horizleft")
        self.skin_label = create_text_box("skin", (640, 335), (135, 40), "#text_box_22_horizleft")
        self.reset_message = create_text_box("Changes cannot be reset after leaving this page.",
                                             (5, 395), (315, 60), "#text_box_26_horizcenter")
        self.eye_colour1_label = create_text_box("eye colour 1", (320, 420), (135, 40), "#text_box_22_horizleft")
        self.heterochromia_text = create_text_box("heterochromia", (495, 451), (135, 40), "#text_box_26_horizcenter")
        self.eye_colour2_label = create_text_box("eye colour 2", (640, 420), (135, 40), "#text_box_22_horizleft")
        self.accessory_label = create_text_box("accessory", (568, 500), (135, 40), "#text_box_22_horizleft")
        self.pose_label = create_text_box("pose", (406, 500), (110, 40), "#text_box_22_horizleft")
        self.reverse_label = create_text_box("reverse", (52, 500), (135, 40), "#text_box_22_horizleft")
        self.scar_message = create_text_box("Adding/removing scars will not affect a cat's conditions or history.",
                                            (52, 650), (500, 40), "#text_box_26_horizleft")
        self.scar1_label = create_text_box("scar 1", (46, 580), (135, 40), "#text_box_22_horizleft")
        self.scar2_label = create_text_box("scar 2", (196, 580), (135, 40), "#text_box_22_horizleft")
        self.scar3_label = create_text_box("scar 3", (346, 580), (135, 40), "#text_box_22_horizleft")
        self.scar4_label = create_text_box("scar 4", (496, 580), (135, 40), "#text_box_22_horizleft")
        
        #tortie tints
        
        self.tortie_tints_label = create_text_box("tortie tint", (646, 580), (135, 40), "#text_box_22_horizleft")
        
        """------------------------------------------------------------------------------------------------------------#
        #                                              LABEL SETUP END                                                 #
        # ------------------------------------------------------------------------------------------------------------"""

    def setup_buttons(self):
        self.previous_cat_button = create_button((25, 25), (153, 30), get_arrow(2, arrow_left=True) + " Previous Cat",
                                                 ButtonStyles.SQUOVAL, sound_id="page_flip")
        self.back_button = create_button((25, 60), (105, 30), get_arrow(2) + " Back", ButtonStyles.SQUOVAL)
        self.next_cat_button = create_button((622, 25), (153, 30), "Next Cat " + get_arrow(3, arrow_left=False),
                                             ButtonStyles.SQUOVAL, sound_id="page_flip")
        self.pelt_length_left_button = create_button((224, 530), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.pelt_length_right_button = create_button((324, 530), (30, 30), get_arrow(1, False),
                                                      ButtonStyles.ROUNDED_RECT)
        self.pose_left_button = create_button((406, 530), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.pose_right_button = create_button((486, 530), (30, 30), get_arrow(1, False), ButtonStyles.ROUNDED_RECT)
        self.reverse_button = create_button((105, 530), (70, 30), "Reverse", ButtonStyles.ROUNDED_RECT)
        self.reset_button = create_button((60, 425), (105, 30), "Reset", ButtonStyles.SQUOVAL)
        if self.sparkle_cats:
            self.sparkle_button = create_button((170, 425), (105, 30), "Sparkle On", ButtonStyles.SQUOVAL)
        else:
            self.sparkle_button = create_button((170, 425), (105, 30), "Sparkle Off", ButtonStyles.SQUOVAL)

        self.filter_button = create_button((115, 460), (105, 30), "Filters", ButtonStyles.SQUOVAL)
        
    def setup_dropdowns(self):
        """------------------------------------------------------------------------------------------------------------#
        #                                              DROPDOWN SETUP START                                            #
        # ------------------------------------------------------------------------------------------------------------"""
        
        
        self.pelt_name_dropdown = create_dropdown((320, 125), (135, 40),
                                                  create_options_list(self.pelt_names, "capitalize"),
                                                  get_selected_option(self.the_cat.pelt.name, "capitalize"))
        if self.the_cat.pelt.name in self.base_game_pelts or self.the_cat.pelt.tortiebase in self.base_game_patterns:
            if 'GREEN' not in self.pelt_colours:
                self.pelt_colours = copy(Pelt.pelt_colours) + self.special_colors_nomasked + self.special_colors_masked
        elif self.the_cat.pelt.name == 'Masked' or self.the_cat.pelt.tortiebase == 'masked':
            if 'GREEN' in self.pelt_colours:
                self.pelt_colours = copy(Pelt.pelt_colours)
            if 'ASH' not in self.pelt_colours:
                self.pelt_colours = copy(Pelt.pelt_colours) + self.special_colors_masked
        elif 'GREEN' in self.pelt_colours or 'ASH' in self.pelt_colours:
            self.pelt_colours = copy(Pelt.pelt_colours)
        
        realistic_colors = Pelt.ginger_colours + Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours
        if not self.sparkle_cats:
            for color in self.pelt_colours:
                if color not in realistic_colors:
                     self.pelt_colours = realistic_colors
                     break
                    
            if self.the_cat.pelt.colour not in realistic_colors:
                self.the_cat.pelt.colour = "BLACK"
        self.pelt_colours.sort()
        self.pelt_colour_dropdown = create_dropdown((480, 125), (135, 40),
                                                    create_options_list(self.pelt_colours, "upper"),
                                                    get_selected_option(self.the_cat.pelt.colour, "upper"))
        self.pattern_dropdown = create_dropdown((640, 125), (135, 40), create_options_list(self.patterns, "upper"),
                                                get_selected_option(self.the_cat.pelt.pattern, "upper"))
        self.tortie_base_dropdown = create_dropdown((320, 200), (135, 40),
                                                    create_options_list(self.tortie_bases, "lower"),
                                                    get_selected_option(self.the_cat.pelt.tortiebase, "lower"))
        
        if self.the_cat.pelt.tortiepattern in self.base_game_patterns:
            if 'GREEN' not in self.tortie_colours:
                self.tortie_colours = copy(Pelt.pelt_colours) + self.special_colors_nomasked + self.special_colors_masked
        elif self.the_cat.pelt.tortiepattern == 'masked':
            if 'GREEN' in self.pelt_colours:
                self.tortie_colours = copy(Pelt.pelt_colours) + self.special_colors_masked
            if 'ASH' not in self.tortie_colours:
                self.tortie_colours = copy(Pelt.pelt_colours) + self.special_colors_masked
        elif 'GREEN' in self.tortie_colours or 'ASH'  in self.tortie_colours:
            self.tortie_colours = copy(Pelt.pelt_colours)
            
        if not self.sparkle_cats:
            for color in self.tortie_colours:
                if color not in realistic_colors:
                     self.tortie_colours = realistic_colors
                     break
                    
            if self.the_cat.pelt.colour not in realistic_colors:
                self.the_cat.pelt.colour = "BLACK"
        self.tortie_colours.sort()    
        self.tortie_colour_dropdown = create_dropdown((480, 200), (135, 40),
                                                      create_options_list(self.tortie_colours, "upper"),
                                                      get_selected_option(self.the_cat.pelt.tortiecolour, "upper"))
        self.tortie_pattern_dropdown = create_dropdown((640, 200), (135, 40),
                                                       create_options_list(self.tortie_bases, "lower"),
                                                       get_selected_option(self.the_cat.pelt.tortiepattern, "lower"))
        self.white_patches_dropdown = create_dropdown((320, 285), (135, 40),
                                                      create_options_list(self.white_patches, "upper"),
                                                      get_selected_option(self.the_cat.pelt.white_patches, "upper"), "smaller_font")
        self.vitiligo_dropdown = create_dropdown((480, 285), (135, 40),
                                                 create_options_list(self.vitiligo_patterns, "upper"),
                                                 get_selected_option(self.the_cat.pelt.vitiligo, "upper"))
        self.points_dropdown = create_dropdown((640, 285), (135, 40),
                                               create_options_list(self.points_markings, "upper"),
                                               get_selected_option(self.the_cat.pelt.points, "upper"))
        self.white_patches_tint_dropdown = create_dropdown((320, 360), (135, 40),
                                                           create_options_list(self.white_patches_tints, "lower"),
                                                           get_selected_option(self.the_cat.pelt.white_patches_tint,
                                                                               "lower", exception=True))
        self.tint_dropdown = create_dropdown((480, 360), (135, 40), create_options_list(self.tints, "lower"),
                                             get_selected_option(self.the_cat.pelt.tint, "lower", exception=True))

        self.skin_dropdown = create_dropdown((640, 360), (135, 40), create_options_list(self.skins, "upper"),
                                             get_selected_option(self.the_cat.pelt.skin, "upper"))
        
        if self.sparkle_cats:
            self.eye_colours = [colour.capitalize() for colour in copy(Pelt.eye_colours)]
            self.eye_colours.sort()
            self.eye_colours += [colour.capitalize() for colour in copy(Pelt.flutter_eyes)]
            self.eye_colours += [colour.capitalize() for colour in copy(Pelt.lamp_eyes)]
            self.eye_colours += [colour.capitalize() for colour in copy(Pelt.neos_eyes)]
            self.eye_colours += [colour.capitalize() for colour in copy(Pelt.angel_eyes)]
            self.eye_colours += [colour.capitalize() for colour in copy(Pelt.snail_eyes)]
        else:
            self.eye_colours = [colour.capitalize() for colour in copy(Pelt.eye_colours)]
            self.eye_colours.sort()
            if self.the_cat.pelt.eye_colour.capitalize() not in self.eye_colours:
                self.the_cat.pelt.eye_colour = "YELLOW"
            if self.the_cat.pelt.eye_colour2:
                if self.the_cat.pelt.eye_colour2.capitalize() not in self.eye_colours:
                    self.the_cat.pelt.eye_colour2 = "YELLOW"
        
        self.eye_colour1_dropdown = create_dropdown((320, 445), (135, 40),
                                                    create_options_list(self.eye_colours, "upper"),
                                                    get_selected_option(self.the_cat.pelt.eye_colour, "upper"), "dropup")
        self.eye_colour2_dropdown = create_dropdown((640, 445), (135, 40),
                                                    create_options_list(self.eye_colours, "upper"), (
                                                        get_selected_option(self.the_cat.pelt.eye_colour2,
                                                                            "upper") if self.the_cat.pelt.eye_colour2 else get_selected_option(
                                                                            self.the_cat.pelt.eye_colour, "upper")), "dropup")
        self.accessory_dropdown = create_dropdown((568, 525), (180, 40), create_options_list(self.accessories, "upper"),
                                                  get_selected_option(self.the_cat.pelt.accessory, "upper"), "dropup")

        scars = self.the_cat.pelt.scars
        self.scar1_dropdown = create_dropdown((42, 605), (135, 40), create_options_list(self.scars, "upper"),
                                              get_selected_option(scars, "upper"), "dropup")
        self.scar2_dropdown = create_dropdown((192, 605), (135, 40), create_options_list(self.scars, "upper"),
                                              get_selected_option(scars[1:], "upper"), "dropup")
        self.scar3_dropdown = create_dropdown((342, 605), (135, 40), create_options_list(self.scars, "upper"),
                                              get_selected_option(scars[2:], "upper"), "dropup")
        self.scar4_dropdown = create_dropdown((492, 605), (135, 40), create_options_list(self.scars, "upper"),
                                              get_selected_option(scars[3:], "upper"), "dropup")

        self.tortie_tint_dropdown = create_dropdown((640, 605), (135, 40), create_options_list(self.tints, "lower"),
                                             get_selected_option(self.the_cat.pelt.tortie_tint, "lower", exception=True), "dropup")

        """------------------------------------------------------------------------------------------------------------#
        #                                              DROPDOWN SETUP END                                              #
        # ------------------------------------------------------------------------------------------------------------"""

        # stores current scar state
        self.initial_scar_selection[self.scar1_dropdown] = self.scar1_dropdown.selected_option[1]
        self.initial_scar_selection[self.scar2_dropdown] = self.scar2_dropdown.selected_option[1]
        self.initial_scar_selection[self.scar3_dropdown] = self.scar3_dropdown.selected_option[1]
        self.initial_scar_selection[self.scar4_dropdown] = self.scar4_dropdown.selected_option[1]

    def setup_cat(self):
        self.get_cat_age()
        self.make_cat_sprite()
        self.setup_cat_elements()
        self.previous_pelt_name = self.the_cat.pelt.name

    def setup_next_and_previous_cat(self):
        if self.next_cat == 0:
            self.next_cat_button.disable()
        else:
            self.next_cat_button.enable()

        if self.previous_cat == 0:
            self.previous_cat_button.disable()
        else:
            self.previous_cat_button.enable()

    def setup_cat_elements(self):
        (self.setup_pelt_length(), self.setup_tortie(), self.setup_white_patches_tint(), self.setup_eye_colours(),
         self.setup_accessory(), self.setup_poses(), self.setup_reverse())

    def setup_pelt_length(self):
        self.cat_elements["pelt_length_index"] = self.pelt_lengths.index(self.the_cat.pelt.length)
        self.update_pelt_length_display()

    def setup_tortie(self):
        if self.the_cat.pelt.name not in ["Calico", "Tortie"]:
            self.pattern_dropdown.disable()
            self.tortie_base_dropdown.disable()
            self.tortie_colour_dropdown.disable()
            self.tortie_pattern_dropdown.disable()
            self.tortie_tint_dropdown.disable()

    def setup_white_patches_tint(self):
        if game_setting_get("vit tint"):
            if self.the_cat.pelt.white_patches is None and self.the_cat.pelt.points is None and self.the_cat.pelt.vitiligo is None:
                self.white_patches_tint_dropdown.disable()
        else:
            if self.the_cat.pelt.white_patches is None and self.the_cat.pelt.points is None:
                self.white_patches_tint_dropdown.disable()

    def setup_eye_colours(self):
        if self.eye_colour2_dropdown.selected_option[1] == self.eye_colour1_dropdown.selected_option[1]:
            self.heterochromia = False
            self.eye_colour2_dropdown.disable()
        else:
            self.heterochromia = True
        self.make_heterochromia_checkbox()

    def setup_accessory(self):
        if self.life_stage == "newborn":
            self.accessory_dropdown.disable()

    def setup_poses(self):
        if self.life_stage == "newborn" or self.the_cat.pelt.paralyzed:
            self.pose_left_button.disable()
            self.pose_right_button.disable()
        self.set_poses()
        self.cat_elements["current_pose"] = self.the_cat.pelt.cat_sprites[self.life_stage]
        self.update_pose_display()

    def setup_reverse(self):
        self.cat_elements["reverse_value"] = self.the_cat.pelt.reverse
        self.update_reverse_display()

    # store state for reset
    # TODO: append values to a list with identifier to retain values between cat pages
    def capture_initial_state(self):
        self.initial_state = {
            "name": self.the_cat.pelt.name,
            "colour": self.the_cat.pelt.colour,
            "length": self.the_cat.pelt.length,
            "pattern": self.the_cat.pelt.pattern,
            "tortiebase": self.the_cat.pelt.tortiebase,
            "tortiecolour": self.the_cat.pelt.tortiecolour,
            "tortiepattern": self.the_cat.pelt.tortiepattern,
            "white_patches": self.the_cat.pelt.white_patches,
            "vitiligo": self.the_cat.pelt.vitiligo,
            "points": self.the_cat.pelt.points,
            "white_patches_tint": self.the_cat.pelt.white_patches_tint,
            "tortie_tint": self.the_cat.pelt.tortie_tint,
            "tint": self.the_cat.pelt.tint,
            "skin": self.the_cat.pelt.skin,
            "eye_colour": self.the_cat.pelt.eye_colour,
            "eye_colour2": self.the_cat.pelt.eye_colour2,
            "accessory": self.the_cat.pelt.accessory,
            "scars": self.the_cat.pelt.scars.copy(),
            "reverse": self.the_cat.pelt.reverse,
            "pose": self.cat_elements["current_pose"],
            "cat_sprites": {
                "young_adult": self.the_cat.pelt.cat_sprites.get("young adult"),
                "adult": self.the_cat.pelt.cat_sprites.get("adult"),
                "senior_adult": self.the_cat.pelt.cat_sprites.get("senior adult")
            }
        }

    def reset_attributes(self):
        for attribute, value in self.initial_state.items():
            if attribute == "scars":
                self.the_cat.pelt.scars = value.copy()
            elif attribute == "pose":
                self.cat_elements["current_pose"] = value
                self.the_cat.pelt.cat_sprites[self.life_stage] = value
            elif attribute == "cat_sprites":
                self.the_cat.pelt.cat_sprites["young adult"] = value["young_adult"]
                self.the_cat.pelt.cat_sprites["adult"] = value["adult"]
                self.the_cat.pelt.cat_sprites["senior adult"] = value["senior_adult"]
            else:
                setattr(self.the_cat.pelt, attribute, value)
        self.update_ui_elements()

    def update_ui_elements(self):
        self.kill_cat_elements()
        self.kill_buttons()
        self.kill_dropdowns()
        self.cat_elements["cat_name"] = create_text_box("customize " + str(self.the_cat.name), (0, 40), (400, 40), "#text_box_34_horizcenter", {"centerx": "centerx"})
        self.setup_buttons()
        self.setup_dropdowns()
        self.setup_cat_elements()
        self.make_cat_sprite()

    def get_cat_age(self):
        self.life_stage = "adult" if self.the_cat.age in ["young adult", "adult", "senior adult"] else self.the_cat.age

    def make_cat_sprite(self):
        if "cat_image" in self.cat_elements:
            self.cat_elements["cat_image"].kill()
        self.cat_image = generate_sprite(self.the_cat, self.life_stage, False, False, True, True)
        self.cat_elements["cat_image"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((35, 130), (250, 250))),
            pygame.transform.scale(self.cat_image, ui_scale_dimensions((250, 250))),
            manager=MANAGER
        )
        update_sprite(self.the_cat)

    # TODO: create a subclass for dropdowns, create a function to regenerate dropdowns with specific data
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.previous_cat_button:
                if isinstance(Cat.fetch_cat(self.previous_cat), Cat):
                    switch_set_value(Switch.cat, self.previous_cat)
                    self.kill_cat_elements()
                    self.kill_buttons()
                    self.kill_dropdowns()
                    self.build_cat_page()
                else:
                    print("invalid previous cat", self.previous_cat)
            elif event.ui_element == self.next_cat_button:
                if isinstance(Cat.fetch_cat(self.next_cat), Cat):
                    switch_set_value(Switch.cat, self.next_cat)
                    self.kill_cat_elements()
                    self.kill_buttons()
                    self.kill_dropdowns()
                    self.build_cat_page()
                else:
                    print("invalid next cat", self.previous_cat)
            elif event.ui_element == self.back_button:
                self.handle_back_button()
            elif event.ui_element == self.reset_button:
                self.reset_attributes()
            elif event.ui_element == self.sparkle_button:
                self.sparkle_cats = not self.sparkle_cats
                self.sparkle_button.kill()
                if self.sparkle_cats:
                    self.sparkle_button = create_button((170, 450), (105, 30), "Sparkle On", ButtonStyles.SQUOVAL)
                else:
                    self.sparkle_button = create_button((170, 450), (105, 30), "Sparkle Off", ButtonStyles.SQUOVAL)
                self.update_ui_elements()
            elif event.ui_element == self.filter_button:
                CustomizeFilterWindow(self.eye_filter, self.pelt_filter, self.acc_filter, self.white_filter)
            elif event.ui_element in [self.pelt_length_left_button, self.pelt_length_right_button]:
                self.handle_pelt_length_buttons(event.ui_element)
            elif event.ui_element == self.heterochromia_checkbox:
                self.handle_heterochromia_checkbox()
            elif event.ui_element in [self.pose_left_button, self.pose_right_button]:
                self.handle_pose_buttons(event.ui_element)
            elif event.ui_element == self.reverse_button:
                self.change_reverse()
            # self.print_pelt_attributes() # for testing purposes
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.pelt_name_dropdown:
                self.handle_pelt_name_dropdown()
            elif event.ui_element == self.pelt_colour_dropdown:
                self.handle_dropdown_change(self.pelt_colour_dropdown, "colour")
            elif event.ui_element == self.pattern_dropdown:
                self.handle_dropdown_change(self.pattern_dropdown, "pattern")
            elif event.ui_element == self.tortie_base_dropdown:
                self.handle_dropdown_change(self.tortie_base_dropdown, "tortiebase")
            elif event.ui_element == self.tortie_colour_dropdown:
                self.handle_dropdown_change(self.tortie_colour_dropdown, "tortiecolour")
            elif event.ui_element == self.tortie_pattern_dropdown:
                self.handle_dropdown_change(self.tortie_pattern_dropdown, "tortiepattern")
            elif event.ui_element == self.white_patches_dropdown:
                self.handle_white_patches_dropdown()
            elif event.ui_element == self.vitiligo_dropdown:
                self.handle_vitiligo_dropdown()
            elif event.ui_element == self.points_dropdown:
                self.handle_points_dropdown()
            elif event.ui_element == self.white_patches_tint_dropdown:
                self.handle_dropdown_change(self.white_patches_tint_dropdown, "white_patches_tint")
            elif event.ui_element == self.tint_dropdown:
                self.handle_dropdown_change(self.tint_dropdown, "tint")
            elif event.ui_element == self.skin_dropdown:
                self.handle_dropdown_change(self.skin_dropdown, "skin")
            elif event.ui_element in [self.eye_colour1_dropdown, self.eye_colour2_dropdown]:
                self.handle_eye_colour_dropdown(event.ui_element)
            elif event.ui_element == self.accessory_dropdown:
                self.handle_accessory_dropdown()
            elif event.ui_element in [self.scar1_dropdown, self.scar2_dropdown, self.scar3_dropdown,
                                      self.scar4_dropdown]:
                self.handle_scar_dropdown(event.ui_element)
            elif event.ui_element == self.tortie_tint_dropdown:
                self.handle_dropdown_change(self.tortie_tint_dropdown, "tortie_tint")
            # self.print_pelt_attributes() # for testing purposes

    def handle_dropdown_change(self, dropdown, attribute):
        selected_option = dropdown.selected_option[1]

        # convert to list
        if attribute == "pattern":
            if selected_option == "NONE":
                self.the_cat.pelt.pattern = None
            elif self.the_cat.pelt.pattern is None:
                self.the_cat.pelt.pattern = [selected_option]
            elif isinstance(self.the_cat.pelt.pattern, list):
                self.the_cat.pelt.pattern.append(selected_option)
            else:
                self.the_cat.pelt.pattern = [selected_option]
        elif attribute == "tortiepattern":
            if self.the_cat.pelt.tortiepattern in self.base_game_patterns:
                if selected_option not in self.base_game_patterns:
                    self.tortie_colours = copy(Pelt.pelt_colours)
                    if self.the_cat.pelt.tortiecolour not in self.base_game_colors:
                        self.the_cat.pelt.tortiecolour = 'BLACK'
            elif selected_option in self.base_game_patterns:
                if 'GREEN' not in self.tortie_colours:
                     self.tortie_colours = copy(Pelt.pelt_colours) + self.special_colors_nomasked + self.special_colors_masked
            setattr(self.the_cat.pelt, attribute, selected_option)
            self.update_ui_elements()
        elif attribute == "tortiebase":
            if self.the_cat.pelt.tortiebase in self.base_game_patterns:
                if selected_option not in self.base_game_patterns:
                    self.pelt_colours = copy(Pelt.pelt_colours)
                    if self.the_cat.pelt.colour not in self.base_game_colors:
                        self.the_cat.pelt.colour = 'BLACK'
            elif selected_option in self.base_game_patterns:
                if 'GREEN' not in self.pelt_colours:
                    self.tortie_colours = copy(Pelt.pelt_colours) + self.special_colors_nomasked + self.special_colors_masked
            setattr(self.the_cat.pelt, attribute, selected_option)
            self.update_ui_elements()
        elif attribute == "tint":
            if selected_option == "None":
                self.the_cat.pelt.tint = "none"
            elif self.the_cat.pelt.tint == ["none"]:
                self.the_cat.pelt.tint = [selected_option]
            elif isinstance(self.the_cat.pelt.tint, list):
                self.the_cat.pelt.tint.append(selected_option)
            else:
                self.the_cat.pelt.tint = [selected_option]
            if "none" in self.the_cat.pelt.tint:
                self.the_cat.pelt.tint = ["none"]
        elif attribute == "white_patches_tint":
            if selected_option == "None":
                self.the_cat.pelt.white_patches_tint = "none"
            elif self.the_cat.pelt.white_patches_tint == ["none"]:
                self.the_cat.pelt.white_patches_tint = [selected_option]
            elif isinstance(self.the_cat.pelt.white_patches_tint, list):
                self.the_cat.pelt.white_patches_tint.append(selected_option)
            else:
                self.the_cat.pelt.white_patches_tint = [selected_option]
            if "none" in self.the_cat.pelt.white_patches_tint:
                self.the_cat.pelt.white_patches_tint = ["none"]
        elif attribute == "tortie_tint":
            if selected_option == "None":
                self.the_cat.pelt.tortie_tint = "none"
            elif self.the_cat.pelt.tortie_tint == ["none"]:
                self.the_cat.pelt.tortie_tint = [selected_option]
            elif isinstance(self.the_cat.pelt.tortie_tint, list):
                self.the_cat.pelt.tortie_tint.append(selected_option)
            else:
                self.the_cat.pelt.tortie_tint = [selected_option]
            if "none" in self.the_cat.pelt.tortie_tint:
                self.the_cat.pelt.tortie_tint = ["none"]
        else:
            setattr(self.the_cat.pelt, attribute, selected_option)

        self.make_cat_sprite()
        self.update_ui_elements()

    def handle_back_button(self):
        if self.the_cat.pelt.eye_colour2 == self.the_cat.pelt.eye_colour: # remove second eye colour if same as first
            self.the_cat.pelt.eye_colour2 = None

        self.the_cat.pelt.scars = list(set(self.the_cat.pelt.scars)) # deduplicate scars

        self.change_screen("profile screen")

    def handle_pelt_name_dropdown(self):
        new_pelt_name = self.pelt_name_dropdown.selected_option[1]
        self.check_if_tortie(new_pelt_name, self.previous_pelt_name)
        redo_dropdowns = False
        if new_pelt_name in self.base_game_pelts:
            if self.the_cat.pelt.name not in self.base_game_pelts:
                redo_dropdowns = True
        elif new_pelt_name == 'Masked':
            if self.the_cat.pelt.name not in self.base_game_pelts:
                redo_dropdowns = True
                self.the_cat.pelt.colour = 'BLACK'
        else:
            if self.the_cat.pelt.name in self.base_game_pelts:
                redo_dropdowns = True
                self.the_cat.pelt.colour = 'BLACK'
        self.the_cat.pelt.name = new_pelt_name
        self.previous_pelt_name = new_pelt_name
        self.make_cat_sprite()
        if redo_dropdowns:
            self.update_ui_elements()

    def handle_pelt_length_buttons(self, button):
        direction = -1 if button == self.pelt_length_left_button else 1
        self.change_pelt_length(direction)

    def handle_white_patches_dropdown(self):
        selected_option = self.white_patches_dropdown.selected_option
        if selected_option[0] == "None":
            self.the_cat.pelt.white_patches = []
        else:
            if isinstance(self.the_cat.pelt.white_patches, list):
                self.the_cat.pelt.white_patches.append(selected_option[1])
            else:
                self.the_cat.pelt.white_patches = [selected_option[1]]
        self.make_cat_sprite()
        self.check_white_patches_tint()

    def handle_vitiligo_dropdown(self):
        selected_option = self.vitiligo_dropdown.selected_option
        if selected_option[0] == "None":
            self.the_cat.pelt.vitiligo = None
        else:
            self.the_cat.pelt.vitiligo = selected_option[1]
        self.make_cat_sprite()
        self.check_white_patches_tint()

    def handle_points_dropdown(self):
        selected_option = self.points_dropdown.selected_option
        if selected_option[0] == "None":
            self.the_cat.pelt.points = None
        else:
            self.the_cat.pelt.points = selected_option[1]
        self.make_cat_sprite()
        self.check_white_patches_tint()

    def handle_eye_colour_dropdown(self, dropdown):
        if dropdown == self.eye_colour1_dropdown:
            self.the_cat.pelt.eye_colour = self.eye_colour1_dropdown.selected_option[1]
        else:
            self.the_cat.pelt.eye_colour2 = self.eye_colour2_dropdown.selected_option[1]
        self.make_cat_sprite()

    def handle_pose_buttons(self, button):
        direction = -1 if button == self.pose_left_button else 1
        self.change_pose(direction)

    def handle_accessory_dropdown(self):
        selected_option = self.accessory_dropdown.selected_option
        if not isinstance(self.the_cat.pelt.accessory, list):
            self.the_cat.pelt.accessory = []
        if selected_option[0] == "None":
            self.the_cat.pelt.accessory = []
        else:
            if selected_option[1] not in self.the_cat.pelt.accessory:
                self.the_cat.pelt.accessory.append(selected_option[1])
        self.make_cat_sprite()

    def handle_scar_dropdown(self, dropdown):
        selected_option = dropdown.selected_option[1]
        previous_selection = self.previous_scar_selection.get(dropdown, self.initial_scar_selection[dropdown])

        if previous_selection != "NONE" and previous_selection in self.the_cat.pelt.scars:
            self.the_cat.pelt.scars.remove(previous_selection) # remove previous selection

        if selected_option != "NONE":
            self.the_cat.pelt.scars.append(selected_option) # add new selection

        self.previous_scar_selection[dropdown] = selected_option

        self.make_cat_sprite()
    
            

    def handle_sprites_for_pelt_length(self, previous_length):
        # check if pelt length has changed from or to long
        is_long_to_not_long = previous_length == "long" and self.the_cat.pelt.length != "long"
        is_not_long_to_long = previous_length != "long" and self.the_cat.pelt.length == "long"

        if is_long_to_not_long or is_not_long_to_long:
            self.set_poses()
            if self.life_stage != "newborn" and not self.the_cat.pelt.paralyzed: # check for special statuses
                self.cat_elements["current_pose"] = self.poses[0]

            if self.life_stage == "adult":
                if not self.the_cat.pelt.paralyzed: # update adult sprites to current pose if not paralyzed
                    self.the_cat.pelt.cat_sprites["young adult"] = self.cat_elements["current_pose"]
                    self.the_cat.pelt.cat_sprites["adult"] = self.cat_elements["current_pose"]
                    self.the_cat.pelt.cat_sprites["senior adult"] = self.cat_elements["current_pose"]
                else: # update adult sprites to random value if paralyzed
                    random_adult_sprite = random.randint(6, 8) if previous_length == "long" else random.randint(9, 11)
                    self.the_cat.pelt.cat_sprites["young adult"] = random_adult_sprite
                    self.the_cat.pelt.cat_sprites["adult"] = random_adult_sprite
                    self.the_cat.pelt.cat_sprites["senior adult"] = random_adult_sprite
            else: # update adult sprites to random value based on pelt length
                random_adult_sprite = random.randint(6, 8) if previous_length == "long" else random.randint(9, 11)
                self.the_cat.pelt.cat_sprites["young adult"] = random_adult_sprite
                self.the_cat.pelt.cat_sprites["adult"] = random_adult_sprite
                self.the_cat.pelt.cat_sprites["senior adult"] = random_adult_sprite

            self.update_pose_display()
            self.make_cat_sprite()

    def change_pelt_length(self, direction):
        previous_length = self.the_cat.pelt.length
        self.cat_elements["pelt_length_index"] = (self.cat_elements["pelt_length_index"] + direction) % len(
            self.pelt_lengths)
        self.the_cat.pelt.length = self.pelt_lengths[self.cat_elements["pelt_length_index"]]
        self.update_pelt_length_display()
        self.handle_sprites_for_pelt_length(previous_length)

    def update_pelt_length_display(self):
        self.kill_cat_element("pelt_length")
        self.cat_elements["pelt_length"] = create_text_box(self.the_cat.pelt.length.lower(), (254, 530), (70, 40),
                                                           "#text_box_26_horizcenter")

    def check_if_tortie(self, new_pelt_name, previous_pelt_name):
        dropdowns = [
            self.pattern_dropdown,
            self.tortie_base_dropdown,
            self.tortie_colour_dropdown,
            self.tortie_pattern_dropdown,
            self.tortie_tint_dropdown
        ]
        if new_pelt_name in ["Calico", "Tortie"]:
            if previous_pelt_name not in ["Calico", "Tortie"]:
                for dropdown in dropdowns:
                    dropdown.kill()

                self.the_cat.pelt.pattern = None

                if previous_pelt_name in ['SingleColour', 'TwoColour']:
                    self.the_cat.pelt.tortiebase = "single"
                else:
                    self.the_cat.pelt.tortiebase = previous_pelt_name.lower()
                self.the_cat.pelt.tortiecolour = self.tortie_colours[0]
                self.the_cat.pelt.tortiepattern = self.tortie_bases[0]

                self.pattern_dropdown = create_dropdown((640, 125), (135, 40),
                                                        create_options_list(self.patterns, "upper"),
                                                        get_selected_option(self.the_cat.pelt.pattern, "upper"))
                self.tortie_base_dropdown = create_dropdown((320, 200), (135, 40),
                                                            create_options_list(self.tortie_bases, "lower"),
                                                            get_selected_option(self.the_cat.pelt.tortiebase, "lower"))
                self.tortie_colour_dropdown = create_dropdown((480, 200), (135, 40),
                                                              create_options_list(self.tortie_colours, "upper"),
                                                              get_selected_option(self.the_cat.pelt.tortiecolour,
                                                                                  "upper"))
                self.tortie_pattern_dropdown = create_dropdown((640, 200), (135, 40),
                                                               create_options_list(self.tortie_bases, "lower"),
                                                               get_selected_option(self.the_cat.pelt.tortiepattern,
                                                                                   "lower"))
                self.tortie_tint_dropdown = create_dropdown((640, 605), (135, 40), create_options_list(self.tints, "lower"),
                                             get_selected_option(self.the_cat.pelt.tortie_tint, "lower", exception=True), "dropup")

                for dropdown in dropdowns:
                    dropdown.enable()
        else:
            for dropdown in dropdowns:
                dropdown.kill()

            self.pattern_dropdown = create_dropdown((640, 125), (135, 40), "None", "None")
            self.tortie_base_dropdown = create_dropdown((320, 200), (135, 40), "None", "None")
            self.tortie_colour_dropdown = create_dropdown((480, 200), (135, 40), "None", "None")
            self.tortie_pattern_dropdown = create_dropdown((640, 200), (135, 40), "None", "None")
            self.tortie_tint_dropdown = create_dropdown((640, 605), (135, 40), "None", "none")

            self.the_cat.pelt.pattern = None
            self.the_cat.pelt.tortiebase = None
            self.the_cat.pelt.tortiecolour = None
            self.the_cat.pelt.tortiepattern = None
            
            self.the_cat.pelt.tortie_tint = ["none"]

            for dropdown in [self.pattern_dropdown, self.tortie_base_dropdown, self.tortie_colour_dropdown,
                             self.tortie_pattern_dropdown, self.tortie_tint_dropdown]:
                dropdown.disable()

    def check_white_patches_tint(self):
        if game_setting_get("vit tint"):
            if self.the_cat.pelt.vitiligo is None and self.the_cat.pelt.points is None and self.the_cat.pelt.white_patches is None:
                self.the_cat.pelt.white_patches_tint = ["none"]
                self.white_patches_tint_dropdown.kill()
                self.white_patches_tint_dropdown = create_dropdown((320, 360), (135, 40),
                                                                   create_options_list(self.white_patches_tints, "lower"),
                                                                   get_selected_option(self.the_cat.pelt.white_patches_tint,
                                                                                       "lower"))
                self.white_patches_tint_dropdown.disable()
            else:
                self.white_patches_tint_dropdown.enable()
        else:
            if self.the_cat.pelt.points is None and self.the_cat.pelt.white_patches is None:
                self.the_cat.pelt.white_patches_tint = ["none"]
                self.white_patches_tint_dropdown.kill()
                self.white_patches_tint_dropdown = create_dropdown((320, 360), (135, 40),
                                                                   create_options_list(self.white_patches_tints, "lower"),
                                                                   get_selected_option(self.the_cat.pelt.white_patches_tint,
                                                                                       "lower"))
                self.white_patches_tint_dropdown.disable()
            else:
                self.white_patches_tint_dropdown.enable()

    def make_heterochromia_checkbox(self):
        self.kill_cat_element("heterochromia_checkbox")
        checkbox_id = "@checked_checkbox" if self.heterochromia else "@unchecked_checkbox"
        self.heterochromia_checkbox = UIImageButton(
            ui_scale(pygame.Rect((480, 450), (30, 30))),
            "",
            object_id=checkbox_id,
            starting_height=2
        )
        self.cat_elements["heterochromia_checkbox"] = self.heterochromia_checkbox

    def handle_heterochromia_checkbox(self):
        self.heterochromia = not self.heterochromia
        if self.heterochromia:
            self.the_cat.pelt.eye_colour2 = self.eye_colour2_dropdown.selected_option[1]
            self.eye_colour2_dropdown.enable()
        else:
            self.the_cat.pelt.eye_colour2 = None
            self.eye_colour2_dropdown.kill()
            self.eye_colour2_dropdown = create_dropdown((640, 445), (135, 40),
                                                        create_options_list(self.eye_colours, "upper"), (
                                                            get_selected_option(self.the_cat.pelt.eye_colour2,
                                                                                "upper") if self.the_cat.pelt.eye_colour2 else get_selected_option(
                                                                self.the_cat.pelt.eye_colour, "upper")))
            self.eye_colour2_dropdown.disable()
        self.make_heterochromia_checkbox()
        self.make_cat_sprite()

    def set_poses(self):
        age_poses = {
            "kitten": [0, 1, 2],
            "adolescent": [3, 4, 5],
            "adult": [6, 7, 8] if self.the_cat.pelt.length != "long" else [9, 10, 11],
            "senior": [12, 13, 14]
        }
        self.poses = age_poses.get(self.life_stage, [])

    def change_pose(self, direction):
        current_index = self.poses.index(self.cat_elements["current_pose"])
        new_index = (current_index + direction) % len(self.poses)
        self.cat_elements["current_pose"] = self.poses[new_index]
        self.the_cat.pelt.cat_sprites[self.life_stage] = self.cat_elements["current_pose"]
        if self.life_stage == "adult":
            self.the_cat.pelt.cat_sprites["young adult"] = self.cat_elements["current_pose"]
            self.the_cat.pelt.cat_sprites["senior adult"] = self.cat_elements["current_pose"]
        self.update_pose_display()
        self.make_cat_sprite()

    def update_pose_display(self):
        self.kill_cat_element("pose")
        pose_text = "none" if (self.the_cat.pelt.paralyzed or self.life_stage == "newborn") else str(
            self.cat_elements["current_pose"])
        self.cat_elements["pose"] = create_text_box(pose_text, (436, 530), (50, 40), "#text_box_26_horizcenter")

    def change_reverse(self):
        self.the_cat.pelt.reverse = not self.the_cat.pelt.reverse
        self.update_reverse_display()
        self.make_cat_sprite()

    def update_reverse_display(self):
        self.kill_cat_element("reverse")
        reverse_text = "true" if self.the_cat.pelt.reverse else "false"
        self.cat_elements["reverse"] = create_text_box(reverse_text, (52, 530), (45, 40), "#text_box_26_horizcenter")

    def exit_screen(self):
        self.kill_cat_elements()
        self.kill_labels()
        self.kill_buttons()
        self.kill_dropdowns()
        self.frame_image.kill()

    def kill_cat_elements(self):
        elements_to_kill = [
            "cat_name", "cat_image", "pelt_length", "pose", "heterochromia_checkbox", "reverse"
        ]
        for element in elements_to_kill:
            self.kill_cat_element(element)

    def kill_cat_element(self, element_name):
        if element_name in self.cat_elements:
            self.cat_elements[element_name].kill()

    def kill_labels(self):
        labels = [
            self.pelt_name_label, self.pelt_colour_label, self.pelt_length_label,
            self.pattern_label, self.tortie_base_label, self.tortie_colour_label, self.tortie_pattern_label,
            self.white_patches_label, self.vitiligo_label, self.points_label, self.white_patches_tint_label,
            self.tint_label, self.skin_label, self.eye_colour1_label, self.eye_colour2_label, self.heterochromia_text,
            self.reset_message, self.pose_label, self.reverse_label, self.accessory_label, self.scar_message,
            self.scar1_label, self.scar2_label, self.scar3_label, self.scar4_label, self.tortie_tints_label 
        ]
        for label in labels:
            label.kill()

    def kill_buttons(self):
        buttons = [
            self.previous_cat_button, self.back_button, self.next_cat_button, self.reset_button, self.sparkle_button,
            self.pelt_length_left_button, self.pelt_length_right_button, self.pose_left_button,
            self.pose_right_button, self.reverse_button, self.filter_button
        ]
        for button in buttons:
            button.kill()

    def kill_dropdowns(self):
        dropdowns = [
            self.pelt_name_dropdown, self.pelt_colour_dropdown, self.pattern_dropdown, self.tortie_base_dropdown,
            self.tortie_colour_dropdown, self.tortie_pattern_dropdown, self.white_patches_dropdown,
            self.vitiligo_dropdown,
            self.points_dropdown, self.skin_dropdown, self.white_patches_tint_dropdown, self.tint_dropdown,
            self.eye_colour1_dropdown, self.eye_colour2_dropdown, self.accessory_dropdown,
            self.scar1_dropdown, self.scar2_dropdown, self.scar3_dropdown, self.scar4_dropdown, self.tortie_tint_dropdown 
        ]
        for dropdown in dropdowns:
            dropdown.kill()
