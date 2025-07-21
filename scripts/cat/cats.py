"""
Contains the Cat and Personality classes
"""

from __future__ import annotations
from copy import copy

import bisect
import itertools
import os.path
import sys
from random import choice, randint, sample, random, getrandbits, randrange
from typing import Dict, List, Any, Union, Callable, Optional, TYPE_CHECKING

import i18n
import ujson  # type: ignore

import scripts.game_structure.localization as pronouns
from scripts.cat import save_load
from scripts.cat.enums import CatAge, CatRank, CatSocial, CatGroup
from scripts.cat.history import History
from scripts.cat.names import Name
from scripts.cat.pelts import Pelt
from scripts.cat.personality import Personality
from scripts.cat.skills import CatSkills
from scripts.cat.status import Status, StatusDict
from scripts.cat.thoughts import Thoughts
from scripts.cat_relations.inheritance import Inheritance
from scripts.cat_relations.relationship import Relationship
from scripts.clan_package.settings import get_clan_setting
from scripts.conditions import (
    Illness,
    Injury,
    PermanentCondition,
    get_amount_cat_for_one_medic,
    medicine_cats_can_cover_clan,
)
from scripts.event_class import Single_Event
from scripts.events_module.generate_events import GenerateEvents
from scripts.game_structure import image_cache, constants
from scripts.game_structure.game.save_load import safe_save
from scripts.game_structure.game.settings import game_setting_get
from scripts.game_structure.game.switches import switch_get_value, Switch
from scripts.game_structure.game_essentials import game
from scripts.game_structure.localization import load_lang_resource
from scripts.game_structure.screen_settings import screen
from scripts.housekeeping.datadir import get_save_dir
from scripts.utility import (
    clamp,
    find_alive_cats_with_rank,
    get_personality_compatibility,
    event_text_adjust,
    update_sprite,
    leader_ceremony_text_adjust,
    update_mask,
)

import scripts.game_structure.screen_settings

if TYPE_CHECKING:
    import pygame


class Cat:
    """The cat class."""

    dead_cats = []
    used_screen = screen
    current_pronoun_lang = None

    age_moons = {
        CatAge.NEWBORN: constants.CONFIG["cat_ages"]["newborn"],
        CatAge.KITTEN: constants.CONFIG["cat_ages"]["kitten"],
        CatAge.ADOLESCENT: constants.CONFIG["cat_ages"]["adolescent"],
        CatAge.YOUNG_ADULT: constants.CONFIG["cat_ages"]["young adult"],
        CatAge.ADULT: constants.CONFIG["cat_ages"]["adult"],
        CatAge.SENIOR_ADULT: constants.CONFIG["cat_ages"]["senior adult"],
        CatAge.SENIOR: constants.CONFIG["cat_ages"]["senior"],
    }

    # This in is in reverse order: top of the list at the bottom
    rank_sort_order = [
        CatRank.NEWBORN,
        CatRank.KITTEN,
        CatRank.CARETAKER_APPRENTICE,
        CatRank.CARETAKER,
        CatRank.ELDER,
        CatRank.APPRENTICE,
        CatRank.WARRIOR,
        CatRank.STORYTELLER_APPRENTICE,
        CatRank.STORYTELLER,
        CatRank.MESSENGER_APPRENTICE,
        CatRank.MESSENGER,
        CatRank.DENKEEPER_APPRENTICE,
        CatRank.DENKEEPER,
        CatRank.MEDIATOR_APPRENTICE,
        CatRank.MEDIATOR,
        CatRank.GARDENER_APPRENTICE,
        CatRank.GARDENER,
        CatRank.MEDICINE_APPRENTICE,
        CatRank.MEDICINE_CAT,
        CatRank.DEPUTY,
        CatRank.LEADER,
    ]
    
    dad_names = {
        "prismatic mind": "autism",
        "obsessive mind": "OCD",
        "weighted heart": "MDD",
        "comet spirit": "ADHD",
        "antisocial": "ASPD",
        "constant roaming pain": "fibromyalgia",
        "ongoing sleeplessness": "chronic insomnia",
        "body biter": "BFRD",
        "thunderous spirit": "BPD",
        "otherworldly mind": "schizophrenia",
        "snow vision": "visual snow",
        "kitten regressor": "age regressor",
        "puppy regressor": "pet regressor",
        "irritable bowels": "IBS",
        "jellyfish joints": "HSD",
        "loose body": "hEDS",
        "burning light": "chronic light sensitivity",
        "jumbled noise": "APD",
        "disrupted senses": "SPD",
        "constant rash": "eczema",
        "confused body": "tourette's",
        "falling paws": "orthostatic hypotension",
        "shattered soul": "DID",
        "budding spirit": "OSDD-1b",
        "fractured spirit": "OSDD-1a",
        "curved spine": "scoliosis",
        "jumbled mind": "dyslexia",
        "counting fog": "dyscalculia",
        "spirited heart": "hyperempathy",
        "puzzled heart": "low empathy",
        "parrot chatter": "echolalia",
        "thought blind": "aphantasia",
        "vivid daydreamer": "maladaptive daydreamer",
        "frequent fainting": "vasovagal syncope",
        "flooded paws": "POTS",
        "bad knee": "meniscus tear",
        "foggy mind": "DPDR",
        "emotionally numb": "alexithymia",
        "being emotionally numb": "having alexithymia",
        "double tongue": "chronic lying",
        "murky mind": "dysthemia",

        "sunblindness": "light sensitivity",
        "faux pregnant": "phantom pregnancy",

        "seasonal lethargy": "seasonal depression",
        "lethargy": "depression",
        "turmoiled litter": "postpartum",
        "sleeplessness": "insomnia",
        "ear buzzing": "tinnitus",
        "kittenspace": "littlespace",
        "puppyspace": "petspace",
        "parroting": "echolalia",
        "deer tick fever": "Lyme disease",
        "deer tick disease": "post-treatment Lyme disease"
    }

    all_adult_personalities = [
        "troublesome", "lonesome", "fierce", "bloodthirsty", "cold", "childish", "playful", "charismatic", "bold",
        "daring", "nervous", "righteous", "insecure", "strict", "compassionate", "thoughtful", "ambitious", "confident",
        "adventurous", "calm", "careful", "faithful", "loving", "loyal", "responsible", "shameless", "sneaky",
        "strange", "vengeful", "wise", "arrogant", "competitive", "grumpy", "cunning", "oblivious", "gloomy", "sincere",
        "flamboyant", "alert", "angry", "appreciative", "bubbly", "absent-minded", "carefree", "cryptic", "dedicated",
        "distracted", "dramatic", "dynamic", "easy-going", "elegant", "escapist", "fair", "forceful", "forgiving",
        "casual", "dry", "chummy", "complex", "emotional", "folksy", "hypnotic", "intense", "nurturing",
        "old-fashioned", "neutral", "moralistic", "soft", "unaggressive", "gentle", "unreligious", "reserved",
        "generous", "gracious", "hearty", "heroic", "humorous", "idealistic", "innocent", "logical", "benevolent",
        "farsighted", "fun-loving", "open", "optimistic", "gallant", "free-thinking", "passive-aggressive",
        "pessimistic", "passionate", "hardworking", "genuine", "peaceful", "polished", "protective", "relaxed",
        "sarcastic", "high-minded", "incisive", "sassy", "secretive", "sensitive", "serious", "incorruptible",
        "leaderly", "stoic", "tidy", "warm", "organized", "patient", "persuasive", "principled", "practical", "goofy",
        "romantic", "scholarly", "destructive", "grim", "forgetful", "greedy", "judgemental", "thoughtless", "nerdy",
        "philosophical", "overthinker", "cheeky", "snobbish", "reliable", "punctual", "supportive", "spiteful",
        "remorseless", "weak-willed", "hyper", "superficial", "fearful", "clumsy", "unpredictable", "cool",
        "cooperative", "energetic", "talkative", "amoral", "tranquil", "antagonistic", "wrongful", "fatalistic",
        "rebellious", "silly", "confused", "sleepy", "chaotic", "scary", "cheerful", "coward", "manipulative",
        "delicate", "hypocrite", "flirty", "honest", "mysterious", "polite", "enthusiastic", "vulnerable", "creative",
        "perfectionist", "sappy", "sentient", "annoying", "lazy", "faithless", "moody", "aloof", "whimsical", "fancy",
        "methodical", "malicious", "frustrated", "self-reliant", "sentimental", "spontainious", "stable", "strong",
        "fox-hearted", "sympathetic", "macabre", "civil", "teacherly", "tolerant", "unfoolable", "witty", "youthful",
        "enigmatic", "ordinary", "private", "loud", "questioning", "predictable", "airy", "anxious", "argumentative",
        "bizarre", "blunt", "calculating", "crude", "deceitful", "cruel", "devious", "messy", "opinionated",
        "overimaginative", "power-hungry", "quirky", "reactive", "resentful", "regretful", "ritualistic", "selfish",
        "sadistic", "scheming", "sloppy", "suspicious", "thievish", "transparent", "vague", "venomous", "envious"
    ]

    all_kit_personalities = [
        "troublesome", "lonesome", "impulsive", "bullying", "attention-seeker", "daydreamer", "dreary", "abrupt",
        "solemn", "wishful", "indecisive", "entitled", "distrusting", "charming", "nervous", "quiet", "insecure",
        "sweet", "goody-no-claws", "chaotic", "nosy", "moody", "nasty", "silly", "know-it-all", "spoiled", "sly",
        "mature", "apologetic", "salty", "whiny", "spicy", "bubbly", "picky", "cheeky", "shy", "fearless", "skittish",
        "self-conscious", "impressionable", "high-spirited", "crybaby", "tiny", "morbid", "obedient", "colorful",
        "zoomy", "clingy", "curious", "slug", "defiant", "sinister", "prim", "tender", "jokester", "wild", "bright",
        "earnest", "rowdy", "sloppy", "complex", "emotional", "protective", "bossy"
    ]

    gender_tags = {"female": "F", "male": "M", "intersex": "I"}

    # EX levels and ranges.
    # Ranges are inclusive to both bounds
    experience_levels_range = {
        "untrained": (0, 0),
        "trainee": (1, 49),
        "beginner": (50, 60),
        "novice": (61, 90), 
        "prepared": (91, 130),
        "competent": (131, 170),
        "skilled": (171, 210),
        "proficient": (211, 250),
        "advanced": (251, 290), 
        "expert": (291, 330),
        "adept": (331, 370), 
        "master": (371, 410),
        "grandmaster": (411, 411)
    }

    all_cats: Dict[str, Cat] = {}  # ID: object
    outside_cats: Dict[str, Cat] = {}  # cats outside the clan
    id_iter = itertools.count()

    all_cats_list: List[Cat] = []
    ordered_cat_list: List[Cat] = []

    grief_strings = {}

    def __init__(
        self,
        prefix=None,
        gender=None,
        status_dict: StatusDict = None,
        backstory="clanborn",
        parent1=None,
        parent2=None,
        past_life = None,
        reincarnation = None,
        adoptive_parents=None,
        suffix=None,
        specsuffix_hidden=False,
        ID=None,
        moons=None,
        example=False,
        faded=False,
        skill_dict=None,
        pelt: Pelt = None,
        loading_cat=False,  # Set to true if you are loading a cat at start-up.
        **kwargs,
    ):
        """Initialise the cat.

        :param prefix: Cat's prefix (e.g. Fire- for Fireheart)
        :param gender: Cat's gender, default None
        :param status_dict: Dict containing information for Cat's status, default None
        :param backstory: Cat's origin, default "clanborn"
        :param parent1: ID of parent 1, default None
        :param parent2: ID of parent 2, default None
        :param suffix: Cat's suffix (e.g. -heart for Fireheart)
        :param specsuffix_hidden: Whether cat has a special suffix (-kit, -paw, etc.), default False
        :param ID: Cat's unique ID, default None
        :param moons: Cat's age, default None
        :param example: If cat is an example cat, default False
        :param faded: If cat is faded, default False
        :param skill_dict: TODO find a good definition for this
        :param pelt: Body details, default None
        :param loading_cat: If loading a cat rather than generating a new one, default False
        :param kwargs: TODO what are the possible args here? ["biome", ]
        """

        self._history = None

        if (
            faded
        ):  # This must be at the top. It's a smaller list of things to init, which is only for faded cats
            self.init_faded(ID, status_dict, prefix, suffix, moons, **kwargs)
            return

        self.generate_events = GenerateEvents()

        # Private attributes
        self._mentor = None  # plz
        self._experience = None
        self._moons = None

        # Public attributes
        self.gender = gender
        self.status: Status = Status(**status_dict) if status_dict else Status()
        self.backstory = backstory
        self.age = None
        self.skills = CatSkills(skill_dict=skill_dict)
        self.personality = Personality(
            trait="troublesome", trait2="strange", lawful=0, aggress=0, stable=0, social=0
        )
        self.parent1 = parent1
        self.parent2 = parent2
        self.past_life = past_life
        self.reincarnation = reincarnation
        self.adoptive_parents = adoptive_parents if adoptive_parents else []
        self.pelt = pelt if pelt else Pelt()
        self.former_mentor = []
        self.patrol_with_mentor = 0
        self.apprentice = []
        self.former_apprentices = []
        self.relationships = {}
        self.mate = []
        self.bestie = []
        self.enemy = []
        self.previous_mates = []
        self.previous_besties = []
        self.previous_enemies = []
        self._pronouns: Dict[str, List[Dict[str, Union[str, int]]]] = {}
        self.placement = None
        self.example = example
        self.dead = False
        self.dead_for = 0  # moons
        self.thought = ""
        self.genderalign = None
        self.birth_cooldown = 0
        self.illnesses = {}
        self.injuries = {}
        self.healed_condition = None
        self.leader_death_heal = None
        self.also_got = False
        self.permanent_condition = {}
        self.alters = []
        self.front = None
        self.awakened = None
        self.guided = False
        self.experience_level = None

        # Various behavior toggles
        self.no_kits = False
        self.no_mates = False
        self.no_retire = False

        self.prevent_fading = False  # Prevents a cat from fading
        self.immortality = False

        self.faded_offspring = (
            []
        )  # Stores of a list of faded offspring, for relation tracking purposes

        self.faded = faded  # This is only used to flag cats that are faded, but won't be added to the faded list until
        # the next save.

        self.favourite = False
        self.favourite_moon = False
        self.favourite_star = False

        self.specsuffix_hidden = specsuffix_hidden
        self.inheritance = None

        # setting ID
        if ID is None:
            potential_id = str(next(Cat.id_iter))

            if game.clan:
                faded_cats = save_load.get_faded_ids()
            else:
                faded_cats = []

            while potential_id in self.all_cats or potential_id in faded_cats:
                potential_id = str(next(Cat.id_iter))
            self.ID = potential_id
        else:
            self.ID = ID

        # age and status
        if status_dict is None and moons is None:
            self.age = choice(list(CatAge))
            self.status.generate_new_status(age=self.age)
        elif moons is not None:
            self.moons = moons
            if moons > 300:
                # Out of range, always elder
                self.age = CatAge.SENIOR
            elif moons == 0:
                self.age = CatAge.NEWBORN
            else:
                # In range
                for key_age in self.age_moons.keys():
                    if moons in range(
                        self.age_moons[key_age][0], self.age_moons[key_age][1] + 1
                    ):
                        self.age = key_age
            if status_dict is None:
                self.status.generate_new_status(age=self.age)
        else:
            if self.status.rank == CatRank.NEWBORN:
                self.age = CatAge.NEWBORN
            elif self.status.rank == CatRank.KITTEN:
                self.age = CatAge.KITTEN
            elif self.status.rank == CatRank.ELDER:
                self.age = CatAge.SENIOR
            elif self.status.rank.is_any_apprentice_rank():
                self.age = CatAge.ADOLESCENT
            else:
                self.age = choice(
                    [
                        CatAge.YOUNG_ADULT,
                        CatAge.ADULT,
                        CatAge.ADULT,
                        CatAge.SENIOR_ADULT,
                    ]
                )
        if moons is None:
            self.moons = randint(
                self.age_moons[self.age][0], self.age_moons[self.age][1]
            )

        # backstory
        if self.backstory is None:
            self.backstory = "clanborn"
        else:
            self.backstory = self.backstory

        # sex!?!??!?!?!??!?!?!?!??
        if self.gender is None:
            intersexchance = randint(1, 25)
            # probability that the cat will be intersex... base chance around 8%
            if intersexchance < 3 and example is False:
                self.gender = "intersex"
                intersex_condition = choice(["excess testosterone", "testosterone deficiency", "aneuploidy",
                                             "mosaicism", "chimerism"])
                self.get_permanent_condition(intersex_condition, born_with=True)
            else:
                self.gender = choice(["female", "male"])
        self.g_tag = self.gender_tags[self.gender]

        """if self.genderalign == "":
            self.genderalign = self.gender"""

        # These things should only run when generating a new cat, rather than loading one in.
        if not loading_cat:
            self.init_generate_cat(skill_dict)

        # In camp status
        self.in_camp = 1
        secondary_biome = None
        tertiary_biome = None
        secondary_biome_weight = None
        tertiary_biome_weight = None
        if "biome" in kwargs:
            biome = kwargs["biome"]
            # ^ idk what these are. Hopefully not putting other biome stuff here won't mess things up ^
        elif game.clan is not None:
            old_to_new = {
                "Equal": 2,
                "Third": 3,
                "Fourth": 4
            }
            biome = game.clan.biome
            secondary_biome = game.clan.secondary_biome if game.clan.secondary_biome else game.clan.biome
            tertiary_biome = game.clan.tertiary_biome if game.clan.tertiary_biome else game.clan.biome
            """
            commenting this out for now since it isn't working :/
            if "biome_weights" in game.clan:
                secondary_biome_weight = old_to_new.get(game.clan.biome_weights)
            else:
            """
            secondary_biome_weight = game.clan.secondary_biome_weight if game.clan.secondary_biome_weight else 2
            tertiary_biome_weight = game.clan.tertiary_biome_weight if game.clan.tertiary_biome_weight else 2

            if game.clan.override_biome:
                biome = game.clan.override_biome
        else:
            biome = None
        # NAME
        # load_existing_name is needed so existing cats don't get their names changed/fixed for no reason
        if self.pelt is not None:
            self.name = Name(
                prefix,
                suffix,
                biome=biome,
                secondary_biome=secondary_biome,
                tertiary_biome=tertiary_biome,
                secondary_biome_weight=secondary_biome_weight,
                tertiary_biome_weight=tertiary_biome_weight,
                specsuffix_hidden=self.specsuffix_hidden,
                load_existing_name=loading_cat,
                cat=self,
            )
        else:
            self.name = Name(
                self.status.rank,
                prefix,
                suffix,
                specsuffix_hidden=self.specsuffix_hidden,
                load_existing_name=loading_cat,
                cat=self,
            )
        # FOR TESTING CONDITIONS
        # if not self.example:
            # new_condition = choice(["fractured spirit", "budding spirit", "shattered soul"])
            # self.get_permanent_condition(new_condition,born_with=True)
        
        if self.awakened and self.pelt.skin in Pelt.skin_sprites:
            if os.path.exists('resources/dicts/esper.json'):
                with open('resources/dicts/esper.json') as read_file:
                    powers_dict = ujson.loads(read_file.read())
            if self.awakened["type"] == "guide":
                # powerless shows twice bc we want it to be twice as common. visible guides
                
                self.pelt.skin = choice(['LIGHTPURPLE', 'BLUE2', 'DARKPURPLE', 'DARKBLUE', 'NEONGREEN', 'BLUESPECKLED',
                                         'BRIGHTPINK', 'BRIGHTORANGE', 'MAGENTA', 'PINKBLUE', 'PURPLEYELLOW',
                                         'BLUEORANGE', 'WHITE', 'BLACK2', 'AQUA', 'DARKGREEN', 'BRIGHTYELLOW', 'MIST',
                                         'LIGHT1', 'SPARKLES', 'SPARKLES2', 'STAINDUST', 'STAINICEBLUE', 'STAININDIGO',
                                         'STAINBLUE', 'STAINPURPLE', 'STAINDARKBLUE', 'MIST', 'LIGHT1', 'SPARKLES',
                                         'SPARKLES2', 'STAINLIGHTPINK', 'STAINYELLOW', 'STAINPINK', 'STAINGOLD',
                                         'STAINHOTPINK', 'STRAINDIRT', 'STAINCYAN', 'STAINLIME', 'STAINTURQUOISE',
                                         'STAINGREEN', 'STAINBLUEGREEN', 'STAINPEACOCK', 'LIGHTPURPLE', 'BLUE2',
                                         'DARKPURPLE', 'DARKBLUE', 'NEONGREEN', 'BLUESPECKLED', 'BRIGHTPINK',
                                         'BRIGHTORANGE', 'MAGENTA', 'PINKBLUE', 'PURPLEYELLOW', 'BLUEORANGE', 'WHITE',
                                         'BLACK2', 'AQUA', 'DARKGREEN', 'BRIGHTYELLOW', 'MIST', 'LIGHT1', 'SPARKLES',
                                         'SPARKLES2'])
            elif self.awakened["type"] == "esper":
                self.pelt.skin = choice(powers_dict[self.awakened["ability"]]["skin"])
            elif self.awakened["type"] == "enhanced esper":
                self.pelt.skin = choice(powers_dict[self.awakened["ability"][0]]["skin"])

        neos_eyes = ['NEO FIRE', 'NEO AMETHYST', 'NEO LIME', 'NEO VIOLET', 'NEO SUN', 'NEO TURQUOISE', 'NEO YELLOW',
                     'NEO SCARLET', 'NEO PINKPURPLE', 'NEO LIGHTBLUE', 'NEO DARKBLUE', 'NEO CYAN', 'NEO YELLOWRED',
                     'NEO PINK', 'NEO INDIGO', 'NEO PURPLE', 'NEO YELLOWGREEN', 'NEO ICEBLUE', 'NEO PALEPINK',
                     'NEO MINT', 'NEO BLACKBLUE']

        flutter_eyes = ['FLUTTER SUNSET', 'FLUTTER MONARCH', 'FLUTTER PEACOCK', 'FLUTTER LUNAR', 'FLUTTER GREENORANGE',
                        'FLUTTER BEACH', 'FLUTTER REDADMIRAL', 'FLUTTER DARK', 'FLUTTER RAINBOW', 'FLUTTER LIGHTBLUE',
                        'FLUTTER GALAXY', 'FLUTTER STAINEDGLASS', 'FLUTTER GLASSWING', 'FLUTTER GREENSTRIPE',
                        'FLUTTER BLUEYELLOW', 'FLUTTER PASTELGALAXY', 'FLUTTER MOTH', 'FLUTTER SPARKLYDUST',
                        'FLUTTER IMPERIAL', 'FLUTTER PINKHEARTS', 'FLUTTER DUSTOX']

        lamp_eyes = ['LAMP YELLOW', 'LAMP ORANGE', 'LAMP HAZEL', 'LAMP YELLOWGREEN', 'LAMP GREEN', 'LAMP BLUE',
                     'LAMP DARKBLUE', 'LAMP GRAY', 'LAMP CYAN', 'LAMP TURQUOISE', 'LAMP PURPLE', 'LAMP GOLD',
                     'LAMP ORANGE2', 'LAMP DARKHAZEL', 'LAMP DARKBLUE2', 'LAMP BLUE2', 'LAMP BROWN', 'LAMP PALEYELLOW',
                     'LAMP LIGHTYELLOW', 'LAMP DARKYELLOW', 'LAMP GOLDENGREEN']

        angel_eyes = ['ANGEL YELLOW', 'ANGEL ORANGE', 'ANGEL HAZEL', 'ANGEL YELLOWGREEN', 'ANGEL GREEN', 'ANGEL BLUE',
                      'ANGEL DARKBLUE', 'ANGEL GRAY', 'ANGEL CYAN', 'ANGEL TURQUOISE', 'ANGEL PURPLE', 'ANGEL GOLD',
                      'ANGEL COPPER', 'ANGEL MINT', 'ANGEL DARKBLUE2', 'ANGEL BLUE2', 'ANGEL BROWN', 'ANGEL SILVER',
                      'ANGEL LIGHTYELLOW', 'ANGEL DARKYELLOW', 'ANGEL GOLDENGREEN']

        snail_eyes = ['SNAIL YELLOW', 'SNAIL ORANGE', 'SNAIL HAZEL', 'SNAIL YELLOWGREEN', 'SNAIL GREEN', 'SNAIL BLUE',
                      'SNAIL DARKBLUE', 'SNAIL GRAY', 'SNAIL CYAN', 'SNAIL TURQUOISE', 'SNAIL PURPLE', 'SNAIL GOLD',
                      'SNAIL COPPER', 'SNAIL MINT', 'SNAIL DARKBLUE2', 'SNAIL BLUE2', 'SNAIL BROWN', 'SNAIL SILVER',
                      'SNAIL LIGHTYELLOW', 'SNAIL DARKYELLOW', 'SNAIL GOLDENGREEN']

        neon_eyes_chance = 16
        if self.awakened and self.awakened["type"] == "guide":
            neon_eyes_chance = 4
        if self.awakened and randint(1,neon_eyes_chance) == 1:
            self.pelt.eye_colour = choice(neos_eyes)
        elif self.awakened and randint(1, 25) == 1:
            self.pelt.eye_colour = choice(angel_eyes)
        elif self.awakened and randint(1, 25) == 1:
            self.pelt.eye_colour = choice(flutter_eyes)
        elif self.awakened and randint(1, 25) == 1:
            self.pelt.eye_colour = choice(lamp_eyes)
        elif self.awakened and randint(1, 25) == 1:
            self.pelt.eye_colour = choice(snail_eyes)
                
        # Private Sprite
        self._sprite: Optional["pygame.Surface"] = None
        self._sprite_mask: Optional["pygame.Mask"] = None
        self._sprite_working: bool = self.not_working()
        """used to store whether we should be displaying sick sprite or not"""

        # SAVE CAT INTO ALL_CATS DICTIONARY IN CATS-CLASS
        self.all_cats[self.ID] = self

        if self.ID is not None and self.ID != "0":
            Cat.insert_cat(self)

    def init_faded(self, ID, status, prefix, suffix, moons, **kwargs):
        """Perform faded-specific initialization

        :param ID: Cat ID
        :param status: Cat status
        :param prefix: Cat's prefix
        :param suffix: Cat's suffix
        :param moons: Age in moons
        :param kwargs:

        :return: None
        """
        self.ID = ID
        self.parent1 = None
        self.parent2 = None
        self.adoptive_parents = []
        self.mate = []
        self.bestie = []
        self.enemy = []
        self.status = Status(**status) if status else Status()
        self._pronouns = {}  # Needs to be set as a dict
        self.moons = moons
        self.inheritance = None  # This should never be used, but just for safety
        self.name = Name(prefix=prefix, suffix=suffix, cat=self)

        self.init_moons_age(moons)

        self.set_faded()  # Sets the faded sprite and faded tag (self.faded = True)
        return True

    def init_moons_age(self, moons):
        """
        Gets the correct life stage for associated moons

        :param moons: Age in moons
        :return: None
        """
        if moons > 300:
            # Out of range, always elder
            self.age = CatAge.SENIOR
        elif moons == 0:
            self.age = CatAge.NEWBORN
        else:
            # In range
            for key_age in self.age_moons.keys():
                if moons in range(
                    self.age_moons[key_age][0], self.age_moons[key_age][1] + 1
                ):
                    self.age = key_age
    
    def generate_ability(self):
        if os.path.exists('resources/dicts/esper.json'):
            with open('resources/dicts/esper.json') as read_file:
                powers_dict = ujson.loads(read_file.read())
        template = {
            "type": "esper",
            "class": "C",
            "ability": "none",
            "desc": "none"
            }
        strength = randint(1, 10)
        if strength == 10:
            template["class"] = "S"
        elif strength > 7:
            template["class"] = "A"
        elif strength > 4:
            template["class"] = "B"
            
        guide_or_esp = randint(1, 2)
        if guide_or_esp == 1 and not self.awakened:
            template["type"] = "guide"
        else:
            power = choice(["pyrokinesis", "hydrokinesis", "cyrokinesis", "geokinesis", "aerokinesis", "illusions",
                            "shapeshifting", "super strength", "enhanced senses", "telekinesis", "chimera",
                            "invisibility", "incorporeal", "mind control", "flight", "teleportation",
                            "electromagnetic control", "light manipulation", "beast speak", "dendrokinesis",
                            "electrokinesis", "telempathy", "astral projection", "flesh manipulation",
                            "spatial manipulation"])
            template["desc"] = choice(powers_dict[power][template["class"]])
            template["ability"] = power
        
        if self.awakened:
            template["type"] = "enhanced esper"
            classes = [self.awakened["class"], template["class"]]
            power2 = choice(["pyrokinesis", "hydrokinesis", "cyrokinesis", "geokinesis", "aerokinesis", "illusions",
                             "shapeshifting", "super strength", "enhanced senses", "telekinesis", "chimera",
                             "invisibility", "incorporeal", "mind control", "flight", "teleportation",
                             "electromagnetic control", "light manipulation", "beast speak", "dendrokinesis",
                             "electrokinesis", "telempathy", "astral projection", "flesh manipulation",
                             "spatial manipulation"])
            abilities = [self.awakened["ability"], power2]
            template["desc"] = choice(powers_dict[power2][template["class"]])
            while template["desc"] == self.awakened["desc"]:
               template["desc"] = choice(powers_dict[power2][template["class"]])
            powers = [self.awakened["desc"], template["desc"]]

            template["class"] = classes
            template["ability"] = abilities
            template["desc"] = powers

        self.awakened = template

    def init_generate_cat(self, skill_dict):
        """
        Used to roll a new cat
        :param skill_dict: TODO what is a skill dict exactly
        :return: None
        """
        # trans cat chances
        nonbiney_list = ["nonbinary", "genderfluid", "demigirl", "demiboy", "genderfae", "genderfaun", "bigender",
                         "genderqueer", "agender", "???", "deminonbinary", "trigender", "genderflux", "polygender"]
        enby_masc = ["trans male", "demiboy", "genderfaun", "trans masc"]
        enby_fem = ["trans female", "demigirl", "genderfae", "trans femme"]

        self.genderalign = self.gender
        trans_chance = randint(1, 30)
        nb_chance = randint(1, 40)
        if trans_chance == 1 and nb_chance == 1:
            if randint(1, 2) == 1:
                trans_chance = 0
            else:
                nb_chance = 0

        prob_awake = constants.CONFIG["cat_generation"]["esper_chance"]

        if self.parent1 is not None:
            par1 = Cat.fetch_cat(self.parent1)
            if par1.awakened:
                prob_awake = int(prob_awake / 2)

        if self.parent2 is not None:
            par2 = Cat.fetch_cat(self.parent2)
            if par2.awakened:
                prob_awake = int(prob_awake / 2)

        if prob_awake < 1:
            prob_awake = 1

        awakened_chance = randint(1, prob_awake)
        if awakened_chance == 1:
            self.generate_ability()
            # self.generate_ability()
            double_powers = randint(1, (prob_awake * 3))
            if double_powers == 1 and self.awakened["type"] == "esper":
                self.generate_ability()

        # GENDER IDENTITY
        if self.gender == "female" and not self.age.is_baby():
            if trans_chance == 1:
                binary_chance = randint(1, 10)
                if binary_chance > 2:
                    self.genderalign = "trans male"
                else:
                    self.genderalign = choice(enby_masc)
            elif nb_chance == 1:
                self.genderalign = choice(nonbiney_list)
        elif self.gender == "male" and not self.age.is_baby():
            if trans_chance == 1:
                binary_chance = randint(1, 10)
                if binary_chance > 2:
                    self.genderalign = "trans female"
                else:
                    self.genderalign = choice(enby_fem)
            elif nb_chance == 1:
                self.genderalign = choice(nonbiney_list)
        elif self.gender == "intersex" and not self.age.is_baby():
            if trans_chance == 1:
                binary_chance = randint(1, 10)
                if binary_chance > 2:
                    self.genderalign = choice(["trans female", "trans male"])
                else:
                    self.genderalign = choice(enby_fem + enby_masc)
            elif nb_chance == 1:
                intergenderchance = randint(1, 2)
                if intergenderchance == 1:
                    self.genderalign = "intergender"
                else:
                    self.genderalign = choice(nonbiney_list)

        # APPEARANCE
        self.pelt = Pelt.generate_new_pelt(
            self.gender,
            [Cat.fetch_cat(i) for i in (self.parent1, self.parent2) if i],
            self.age,
        )

        # Personality
        self.personality = Personality(kit_trait=self.age.is_baby())

        # experience and current patrol status
        if self.age.is_baby():
            self.experience = 0
        elif self.age == CatAge.ADOLESCENT:
            m = self.moons
            self.experience = 0
            while m > Cat.age_moons[CatAge.ADOLESCENT][0]:
                ran = constants.CONFIG["graduation"]["base_app_timeskip_ex"]
                exp = choice(
                    list(range(ran[0][0], ran[0][1] + 1))
                    + list(range(ran[1][0], ran[1][1] + 1))
                )
                self.experience += exp + 3
                m -= 1
        elif self.age in (CatAge.YOUNG_ADULT, CatAge.ADULT):
            self.experience = randint(
                Cat.experience_levels_range["prepared"][0],
                Cat.experience_levels_range["proficient"][1],
            )
        elif self.age == CatAge.SENIOR_ADULT:
            self.experience = randint(
                Cat.experience_levels_range["competent"][0],
                Cat.experience_levels_range["expert"][1],
            )
        elif self.age == CatAge.SENIOR:
            self.experience = randint(
                Cat.experience_levels_range["competent"][0],
                Cat.experience_levels_range["master"][1],
            )
        else:
            self.experience = 0

        if not skill_dict:
            self.skills = CatSkills.generate_new_catskills(self.status.rank, self.moons)

    def __repr__(self):
        return "CAT OBJECT:" + self.ID

    def __eq__(self, other):
        return False if not isinstance(other, Cat) else self.ID == other.ID

    def __hash__(self):
        return hash(self.ID)

    @property
    def dead(self) -> bool:
        return self.status.group and self.status.group.is_afterlife()

    @dead.setter
    def dead(self, die: bool):
        if die:
            if self.status.group and self.status.group.is_afterlife():
                print(
                    f"WARNING: Tried to kill {self.name} ID: {self.ID} but this cat is already dead!"
                )
                return
            self.status.send_to_afterlife()

    @property
    def dead_for(self) -> int:
        return sum(
            entry.get("moons_as")
            for entry in self.status.group_history
            if entry.get("group")
            in (CatGroup.STARCLAN, CatGroup.UNKNOWN_RESIDENCE, CatGroup.DARK_FOREST)
        )

    @dead_for.setter
    def dead_for(self, moons: int):
        self.status.change_current_moons_as(moons)

    @property
    def mentor(self):
        """Return managed attribute '_mentor', which is the ID of the cat's mentor."""
        return self._mentor

    @mentor.setter
    def mentor(self, mentor_id: Any):
        """Makes sure `Cat.mentor` can only be None (no mentor) or a string (mentor ID)."""
        if mentor_id is None or isinstance(mentor_id, str):
            self._mentor = mentor_id
        else:
            print(
                f"Mentor ID {mentor_id} of type {type(mentor_id)} isn't valid :("
                "\nCat.mentor has to be either None (no mentor) or the mentor's ID as a string."
            )

    @property
    def pronouns(self) -> List[Dict[str, Union[str, int]]]:
        """
        Loads the correct pronouns for the loaded language.
        :return: List of dicts for the cat's pronouns
        """
        if self.faded:
            value = pronouns.get_new_pronouns("nonbinary")
            return [value]

        queer_list = ["intersex", "intergender", "trans male", "trans female", "nonbinary", "genderfluid", "demigirl",
                      "demiboy", "genderfae", "genderfaun", "bigender", "genderqueer", "agender", "???",
                      "deminonbinary", "trigender", "genderflux", "polygender"]
        enby_masc = ["demiboy", "genderfaun", "trans masc"]
        enby_fem = ["demigirl", "genderfae", "trans femme"]
        
        she_him = randint(1, 5)
        neo_chance = constants.CONFIG["cat_generation"]["neopronoun_chance"]
        second_set = constants.CONFIG["cat_generation"]["multiple_pronouns_chance"]
        if self.genderalign in queer_list:
            neo_chance = int(neo_chance / 2)
            second_set = int(second_set / 4)
        neos = randint(1, neo_chance)
        seconds = randint(1, second_set)
        
        locale = i18n.config.get("locale")
        value = self._pronouns.get(locale)
        if value is None:
            self._pronouns[locale] = pronouns.get_new_pronouns(self.genderalign)

            if self.genderalign in enby_masc and she_him < 4:
                self._pronouns[locale] += pronouns.get_new_pronouns("male")
            elif self.genderalign in enby_fem and she_him < 4:
                self._pronouns[locale] += pronouns.get_new_pronouns("female")
            elif neos == 1:
                self._pronouns[locale] += pronouns.get_new_pronouns("neos")

            if seconds == 1:
                pronoun_gender = randint(1, 10)
                if pronoun_gender < 6:
                    # add he, she, or they
                    self._pronouns[locale] += pronouns.get_new_pronouns(choice(["male", "female", "nonbinary"]))
                else:
                    # add neos
                    self._pronouns[locale] += pronouns.get_new_pronouns("neos")

            if len(self._pronouns[locale]) > 1:
                if self._pronouns[locale][0]["subject"] == self._pronouns[locale][1]["subject"]:
                    self._pronouns[locale] = [self._pronouns[locale][0]]
                    # print(self._pronouns[locale])
            value = self._pronouns[locale]

        return value

    @pronouns.setter
    def pronouns(
        self,
        val: Union[
            Dict[str, List[Dict[str, Union[str, int]]]],
            List[Dict[str, Union[str, int]]],
        ],
    ):
        """
        Sets the pronouns for the cat. Contains protection for "old-style" pronouns
        :param val:
        :return:
        """
        if isinstance(val, dict):
            self._pronouns = val
            return
        elif isinstance(val, list):
            # possibly old-style pronouns
            self._pronouns[i18n.config.get("locale")] = val
            return

    @property
    def history(self) -> History:
        """load history if it is None"""
        if self._history is None:
            self.load_history()
        return self._history

    @history.setter
    def history(self, val: History):
        self._history = val

    def get_genderalign_string(self):
        # translate it if it's default
        if self.genderalign in (
            "female",
            "male",
            "trans female",
            "trans male",
            "nonbinary",
        ):
            return i18n.t(f"general.{self.genderalign}")
        # otherwise, it's custom - just return it directly
        return self.genderalign

    def get_gender_string(self):
        return i18n.t(f"general.{self.gender}")

    def is_alive(self):
        """Check if this cat is alive

        :return: True if alive, False if dead
        """
        return not self.dead

    def die(self, body: bool = True):
        """Kills cat.

        body - defaults to True, use this to mark if the body was recovered so
        that grief messages will align with body status
        - if it is None, a lost cat died and therefore not trigger grief, since the clan does not know
        """
        if (
            self.status.is_leader
            and "pregnant" in self.injuries
            and game.clan.leader_lives > 0
        ):
            self.illnesses.clear()

            self.injuries = {
                key: value
                for (key, value) in self.injuries.items()
                if key == "pregnant"
            }
        else:
            self.injuries.clear()
            self.illnesses.clear()
            
        if self.immortality:
            print("haha can't kill me :3")
            return
        
        if self.dead:
            print("you can't die twice...")
            return

        # Deal with leader death
        text = ""
        darkforest = game.clan.instructor.status.group == CatGroup.DARK_FOREST
        isoutside = self.status.is_outsider and not self.status.is_lost(
            CatGroup.PLAYER_CLAN
        )
        if self.status.is_leader:
            if game.clan.leader_lives > 0:
                lives_left = game.clan.leader_lives
                death_thought = Thoughts.leader_death_thought(
                    self, lives_left, darkforest
                )
                final_thought = event_text_adjust(self, death_thought, main_cat=self)
                self.thought = final_thought
                return ""
            elif game.clan.leader_lives <= 0:
                self.dead = True
                game.just_died.append(self.ID)
                game.clan.leader_lives = 0
                death_thought = Thoughts.leader_death_thought(self, 0, darkforest)
                final_thought = event_text_adjust(self, death_thought, main_cat=self)
                self.thought = final_thought
                if not darkforest:
                    text = (
                        "They've lost their last life and have travelled to StarClan."
                    )
                else:
                    text = "They've lost their last life and have travelled to the Dark Forest."
        else:
            self.dead = True
            game.just_died.append(self.ID)
            death_thought = Thoughts.new_death_thought(self, darkforest, isoutside)
            final_thought = event_text_adjust(self, death_thought, main_cat=self)
            self.thought = final_thought

        for app in self.apprentice.copy():
            fetched_cat = Cat.fetch_cat(app)
            if fetched_cat:
                fetched_cat.update_mentor()
        self.update_mentor()

        # handle grief
        # since we just yeeted them to their afterlife, we gotta check their previous group affiliation, not current
        if game.clan and self.status.get_last_living_group() == CatGroup.PLAYER_CLAN:
            self.grief(body)
            Cat.dead_cats.append(self)

        # mark the sprite as outdated
        self.pelt.rebuild_sprite = True

        # exiled cats are special, cus they get kicked out a heaven
        if isoutside and self.status.is_exiled():
            self.status.add_to_group(CatGroup.UNKNOWN_RESIDENCE)

        return

    def exile(self):
        """This is used to send a cat into exile."""

        self.status.exile_from_group()

        bitter_traits = ["vengeful", "bloodthirsty", "cunning", "intense", "destructive", "spiteful",
                         "remorseless", "antagonistic", "malicious", "sadistic"]
        if self.personality.trait in bitter_traits or self.personality.trait2 in bitter_traits:
            self.thought = "Swears their revenge for being exiled"
        else:
            self.thought = "Is shocked that they have been exiled"
        for app in self.apprentice:
            fetched_cat = Cat.fetch_cat(app)
            if fetched_cat:
                fetched_cat.update_mentor()
        self.update_mentor()

    def grief(self, body: bool):
        """
        compiles grief moon event text
        """
        if body:
            body_status = "body"
        else:
            body_status = "no_body"

        # Keep track is the body was treated with rosemary.
        body_treated = False
        text = None

        load_grief_reactions()

        # apply grief to cats with high positive relationships to dead cat
        for cat in Cat.all_cats.values():
            if cat.dead or cat.status.is_outsider or cat.moons < 1:
                continue

            to_self = cat.relationships.get(self.ID)
            if not isinstance(to_self, Relationship):
                continue

            family_relation = self.familial_grief(living_cat=cat)
            very_high_values = []
            high_values = []

            if to_self.romantic_love > 55:
                very_high_values.append("romantic")
            if to_self.romantic_love > 40:
                high_values.append("romantic")

            if to_self.platonic_like > 50:
                very_high_values.append("platonic")
            if to_self.platonic_like > 30:
                high_values.append("platonic")

            if to_self.admiration > 70:
                very_high_values.append("admiration")
            if to_self.admiration > 50:
                high_values.append("admiration")

            if to_self.comfortable > 60:
                very_high_values.append("comfort")
            if to_self.comfortable > 40:
                high_values.append("comfort")

            if to_self.trust > 70:
                very_high_values.append("trust")
            if to_self.trust > 50:
                high_values.append("trust")

            major_chance = 0
            if very_high_values:
                # major grief eligible cats.

                major_chance = 3
                if cat.personality.stability < 5:
                    major_chance -= 1

                # decrease major grief chance if grave herbs are used
                if (
                    body
                    and not body_treated
                    and "rosemary" in game.clan.herb_supply.entire_supply
                ):
                    body_treated = True
                    game.clan.herb_supply.remove_herb("rosemary", -1)
                    game.herb_events_list.append(
                        f"Rosemary was used for {self.name}'s body."
                    )

                if body_treated:
                    major_chance -= 1

            # If major_chance is not 0, there is a chance for major grief
            grief_type = None
            if major_chance and not int(random() * major_chance):
                grief_type = "major"

                possible_strings = []
                for x in very_high_values:
                    possible_strings.extend(
                        self.generate_events.possible_death_reactions(
                            family_relation, x, choice([cat.personality.trait, cat.personality.trait2]), body_status
                        )
                    )

                if not possible_strings:
                    print("No grief strings")
                    continue

                text = choice(possible_strings)
                text += " " + choice(MINOR_MAJOR_REACTION["major"])
                text = event_text_adjust(Cat, text=text, main_cat=self, random_cat=cat)

                cat.get_ill("grief stricken", event_triggered=True, severity="major")

            # If major grief fails, but there are still very_high or high values,
            # it can fail to to minor grief. If they have a family relation, bypass the roll.
            elif (very_high_values or high_values) and (
                family_relation != "general" or not int(random() * 5)
            ):
                grief_type = "minor"

                # These minor grief message will be applied as thoughts.
                minor_grief_messages = (
                    "Told a fond story at r_c's vigil",
                    "Bargains with StarClan, begging them to send r_c back",
                    "Sat all night at r_c's vigil",
                    "Will never forget r_c",
                    "Prays that r_c is safe in StarClan",
                    "Misses the warmth that r_c brought to {PRONOUN/m_c/poss} life",
                    "Is mourning r_c",
                    "Can't stop coming to tears each time r_c is mentioned",
                    "Stayed the longest at r_c's vigil",
                    "Left r_c's vigil early due to grief",
                    "Lashes out at any cat who checks on {PRONOUN/m_c/object} after r_c's death",
                    "Took a long walk on {PRONOUN/m_c/poss} own to mourn r_c in private",
                    "Is busying {PRONOUN/m_c/self} with too much work to forget about r_c's death",
                    "Does {PRONOUN/m_c/poss} best to console {PRONOUN/m_c/poss} clanmates about r_c's death",
                    "Takes a part of r_c's nest to put with {PRONOUN/m_c/poss} own, clinging to the fading scent",
                    "Sleeps in r_c's nest tonight",
                    "Defensively states that {PRONOUN/m_c/subject} {VERB/m_c/don't/doesn't} need any comfort about r_c's death",
                    "Wonders why StarClan had to take r_c so soon",
                    "Still needs r_c even though they're gone",
                    "Doesn't think {PRONOUN/m_c/subject} will ever be the same without r_c",
                    "Was seen crying in {PRONOUN/m_c/poss} nest after r_c's vigil",
                    "Is hiding {PRONOUN/m_c/poss} tears as {PRONOUN/m_c/subject} {VERB/m_c/comfort/comforts} the others about r_c's passing",
                )

                if body:
                    minor_grief_messages += (
                        "Helped bury r_c, leaving {PRONOUN/r_c/poss} favorite prey at the grave",
                        "Slips out of camp to visit r_c's grave",
                        "Clung so desperately to r_c's body that {PRONOUN/m_c/subject} had to be dragged away",
                        "Hides a scrap of r_c's fur under {PRONOUN/m_c/poss} nest to cling to",
                        "Can't stand the sight of r_c's body in camp",
                        "Hissed at anyone who got too close to r_c's body, refusing to let go",
                        "Spent a long time grooming r_c's fur for their vigil",
                        "Arranged the flowers for r_c's vigil",
                        "Picked the best spot in the burial grounds for r_c",
                        "Keeps thinking that r_c is only sleeping",
                        "Is in denial of r_c's death, despite the ongoing vigil",
                        "Insists that r_c isn't gone",
                        "Begs r_c not to leave them all",
                        "Sleeps next to r_c for the entire vigil one last time",
                        "Ran out of camp the moment {PRONOUN/m_c/subject} saw r_c's body",
                        "Sang a song in memory of r_c at the vigil",
                        "Stares at r_c's vigil longingly, but doesn't feel the right to join in",
                    )

                text = choice(minor_grief_messages)

            if grief_type:
                # Generate the event:
                if cat.ID not in Cat.grief_strings:
                    Cat.grief_strings[cat.ID] = []

                Cat.grief_strings[cat.ID].append((text, (self.ID, cat.ID), grief_type))
                continue

            # Negative "grief" messages are just for flavor.
            high_values = []
            very_high_values = []
            if to_self.dislike > 50:
                high_values.append("dislike")

            if to_self.jealousy > 50:
                high_values.append("jealousy")

            if high_values:
                # Generate the event:
                possible_strings = []
                for x in high_values:
                    possible_strings.extend(
                        self.generate_events.possible_death_reactions(
                            family_relation, x, choice([cat.personality.trait, cat.personality.trait2]), body_status
                        )
                    )

                text = event_text_adjust(
                    Cat, choice(possible_strings), main_cat=self, random_cat=cat
                )
                if cat.ID not in Cat.grief_strings:
                    Cat.grief_strings[cat.ID] = []

                Cat.grief_strings[cat.ID].append((text, (self.ID, cat.ID), "negative"))

    def familial_grief(self, living_cat: Cat):
        """
        returns relevant grief strings for family members, if no relevant strings then returns None
        """
        dead_cat = self

        if dead_cat.is_parent(living_cat):
            return "child"
        elif living_cat.is_parent(dead_cat):
            return "parent"
        elif dead_cat.is_sibling(living_cat):
            return "sibling"
        else:
            return "general"

    def become_lost(self):
        """Makes a Clan cat a lost cat. Makes status changes and removes apprentices."""

        self.status.become_lost(
            new_social_status=choice([CatSocial.KITTYPET, CatSocial.LONER])
        )

        for app in self.apprentice.copy():
            app_ob = Cat.fetch_cat(app)
            if app_ob:
                app_ob.update_mentor()

        self.update_mentor()

        for x in self.apprentice:
            Cat.fetch_cat(x).update_mentor()

    def add_to_clan(self) -> list:
        """Makes an "outside cat" a Clan cat. Returns a list of IDs for any additional cats that
        are coming with them."""

        if not self.status.is_exiled(CatGroup.PLAYER_CLAN):
            self.history.add_beginning()

        self.status.add_to_group(new_group=CatGroup.PLAYER_CLAN, age=self.age)

        game.clan.add_to_clan(self)

        # check if there are kits under 12 moons with this cat and also add them to the clan
        children = self.get_children()
        ids = []
        for child_id in children:
            child = Cat.all_cats[child_id]
            if (
                not child.dead
                and not child.status.is_exiled(CatGroup.PLAYER_CLAN)
                and child.moons < 12
            ):
                child.status.add_to_group(new_group=CatGroup.PLAYER_CLAN, age=self.age)
                child.add_to_clan()
                child.history.add_beginning()
                ids.append(child_id)

        return ids

    def rank_change(self, new_rank: CatRank, resort=False):
        """Changes the status of a cat. Additional functions are needed if you want to make a cat a leader or deputy.
        :param new_rank: CatRank that the cat is becoming
        :param resort: If sorting type is 'rank', and resort is True, it will resort the cat list. This should
                only be true for non-timeskip status changes."""

        old_rank = self.status.rank

        # this is a private function, but it's meant to be used here.
        self.status._change_rank(new_rank)  # pylint: disable=protected-access

        self.name.status = new_rank

        self.update_mentor()
        for app in self.apprentice.copy():
            fetched_cat = Cat.fetch_cat(app)
            if isinstance(fetched_cat, Cat):
                fetched_cat.update_mentor()

        # If they have any apprentices, make sure they are still valid:
        if old_rank == CatRank.MEDICINE_CAT:
            game.clan.remove_med_cat(self)

        # updates mentors
        if self.status.rank.is_any_apprentice_rank() or self.status.rank == CatRank.MEDIATOR:
            pass

        elif self.status.rank == CatRank.WARRIOR:
            if old_rank == CatRank.LEADER and (
                game.clan.leader and game.clan.leader.ID == self.ID
            ):
                game.clan.leader = None
                game.clan.leader_predecessors += 1
            if game.clan and game.clan.deputy and game.clan.deputy.ID == self.ID:
                game.clan.deputy = None
                game.clan.deputy_predecessors += 1

        elif self.status.rank == CatRank.MEDICINE_CAT:
            if game.clan is not None:
                game.clan.new_medicine_cat(self)

        elif self.status.rank == CatRank.ELDER:
            if (
                old_rank == CatRank.LEADER
                and game.clan.leader
                and game.clan.leader.ID == self.ID
            ):
                game.clan.leader = None
                game.clan.leader_predecessors += 1

            if game.clan.deputy and game.clan.deputy.ID == self.ID:
                game.clan.deputy = None
                game.clan.deputy_predecessors += 1

        # update class dictionary
        self.all_cats[self.ID] = self

        # If we have it sorted by rank, we also need to re-sort
        if switch_get_value(Switch.sort_type) == "rank" and resort:
            Cat.sort_cats()

    def rank_change_traits_skill(self, mentor):
        """Updates trait and skill upon ceremony"""

        if self.status.rank in (
            CatRank.WARRIOR,
            CatRank.MEDICINE_CAT,
            CatRank.MEDIATOR,
        ):
            # Give a couple doses of mentor influence:
            if mentor:
                max_influence = randint(0, 2)
                i = 0
                while max_influence > i:
                    i += 1
                    affect_personality = self.personality.mentor_influence(
                        Cat.fetch_cat(mentor).personality
                    )
                    affect_skills = self.skills.mentor_influence(Cat.fetch_cat(mentor))
                    if affect_personality:
                        self.history.add_facet_mentor_influence(
                            mentor.ID,
                            affect_personality[0],
                            affect_personality[1],
                        )
                    if affect_skills:
                        self.history.add_skill_mentor_influence(
                            affect_skills[0], affect_skills[1], affect_skills[2]
                        )

            self.history.add_mentor_skill_influence_strings()
            self.history.add_mentor_facet_influence_strings()
        return

    def change_name(self, new_prefix=None, new_suffix=None):
        self.name = Name(
            prefix=new_prefix,
            suffix=new_suffix,
            biome=game.clan.biome,
            secondary_biome=game.clan.secondary_biome,
            tertiary_biome=game.clan.tertiary_biome,
            secondary_biome_weight=game.clan.secondary_biome_weight,
            tertiary_biome_weight=game.clan.tertiary_biome_weight,
            specsuffix_hidden=self.specsuffix_hidden,
            cat=self,
        )

    def manage_outside_trait(self):
        """To be run every moon on outside cats
        to keep trait and skills making sense."""
        if not self.status.is_outsider:
            return

        self.personality.set_kit(self.age.is_baby())  # Update kit trait stuff

    def describe_cat(self, short=False):
        """Generates a string describing the cat's appearance and gender.

        :param short: Whether to truncate the output, default False
        :type short: bool
        """
        output = Pelt.describe_appearance(self, short)
        # Add "a" or "an"
        if i18n.config.get("locale") == "en":
            output = f"an {output}" if output[0].lower() in "aeiou" else f"a {output}"
        # else:
        #     output = i18n.t("utility.indefinite", text=output, m_c=self)
        event_text_adjust(Cat, output, main_cat=self)
        return output
    
    def describe_skin(self):
        """Get a human-readable description of this cat's skin colour"""
        skin = str(self.pelt.skin).lower()

        if skin == "darkbrown":
            skin = "dark brown"
        elif skin == "lightbrown":
            skin = "light brown"
        elif skin == "darkgrey":
            skin = "dark grey"
        elif skin == "darksalmon":
            skin = "dark salmon"
        elif skin == "darkmarbled":
            skin = "dark marbled"
        elif skin == "lightmarbled":
            skin = "light marbled"
        elif skin == "darkblue":
            skin = "dark blue"
        elif skin == "lightblue":
            skin = "light blue"
        return skin

    def describe_eyes(self):
        """Get a human-readable description of this cat's eye colour"""
        colour = str(self.pelt.eye_colour).lower()
        colour2 = str(self.pelt.eye_colour2).lower()

        if colour == "palegreen":
            colour = "pale green"
        elif colour == "darkblue":
            colour = "dark blue"
        elif colour == "paleblue":
            colour = "pale blue"
        elif colour == "paleyellow":
            colour = "pale yellow"
        elif colour == "heatherblue":
            colour = "heather blue"
        elif colour == "blue2":
            colour = "blue"
        elif colour == "sunlitice":
            colour = "sunlit ice"
        elif colour == "greenyellow":
            colour = "green-yellow"
        elif colour == "violet2":
            colour = "blackberry"
        elif colour == "turquoise2":
            colour = "dark turquoise"
        elif colour == "rose2":
            colour = "dark rose"
        if self.pelt.eye_colour2:
            if colour2 == "palegreen":
                colour2 = "pale green"
            if colour2 == "darkblue":
                colour2 = "dark blue"
            if colour2 == "paleblue":
                colour2 = "pale blue"
            if colour2 == "paleyellow":
                colour2 = "pale yellow"
            if colour2 == "heatherblue":
                colour2 = "heather blue"
            if colour2 == "sunlitice":
                colour2 = "sunlit ice"
            if colour2 == "greenyellow":
                colour2 = "green-yellow"
            colour = f"{colour} and {colour2}"
        return colour

    def convert_history(self, died_by, scar_events):
        """
        Handle old history save conversions
        """
        deaths = []
        if died_by:
            deaths.extend(
                {"involved": None, "text": death, "moon": "?"} for death in died_by
            )
        scars = []
        if scar_events:
            scars.extend(
                {"involved": None, "text": scar, "moon": "?"} for scar in scar_events
            )
        self.history = History(died_by=deaths, scar_events=scars, cat=self)

    def load_history(self):
        """Load this cat's history"""
        if self._history:
            return

        try:
            if switch_get_value(Switch.clan_name) != "":
                clanname = switch_get_value(Switch.clan_name)
            else:
                clanname = switch_get_value(Switch.clan_list)[0]
        except IndexError:
            print("WARNING: History failed to load, no Clan in switches?")
            return

        history_directory = f"{get_save_dir()}/{clanname}/history/"
        cat_history_directory = history_directory + self.ID + "_history.json"

        if not os.path.exists(cat_history_directory):
            self._history = History(
                beginning={},
                mentor_influence={},
                app_ceremony={},
                lead_ceremony=None,
                possible_history={},
                died_by=[],
                scar_events=[],
                murder={},
                cat=self,
            )
            return
        try:
            with open(cat_history_directory, "r", encoding="utf-8") as read_file:
                history_data = ujson.loads(read_file.read())

                self._history = History(
                    beginning=(
                        history_data["beginning"] if "beginning" in history_data else {}
                    ),
                    mentor_influence=(
                        history_data["mentor_influence"]
                        if "mentor_influence" in history_data
                        else {}
                    ),
                    app_ceremony=(
                        history_data["app_ceremony"]
                        if "app_ceremony" in history_data
                        else {}
                    ),
                    lead_ceremony=(
                        history_data["lead_ceremony"]
                        if "lead_ceremony" in history_data
                        else None
                    ),
                    possible_history=(
                        history_data["possible_history"]
                        if "possible_history" in history_data
                        else {}
                    ),
                    died_by=(
                        history_data["died_by"] if "died_by" in history_data else []
                    ),
                    scar_events=(
                        history_data["scar_events"]
                        if "scar_events" in history_data
                        else []
                    ),
                    murder=history_data["murder"] if "murder" in history_data else {},
                    cat=self,
                )
        except Exception:
            self._history = None
            print(
                f"WARNING: There was an error reading the history file of cat #{self} or their history file was "
                f"empty. Default history info was given. Close game without saving if you have save information "
                f"you'd like to preserve!"
            )

    def save_history(self, history_dir):
        """Save this cat's history.

        :param history_dir: Directory to save cat's history to
        :type history_dir: str
        """
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)

        history_dict = self.history.make_dict()
        try:
            safe_save(f"{history_dir}/{self.ID}_history.json", history_dict)
        except:
            self.history = History(
                beginning={},
                mentor_influence={},
                app_ceremony={},
                lead_ceremony=None,
                possible_history={},
                died_by=[],
                scar_events=[],
                murder={},
                cat=self,
            )

            print(f"WARNING: saving history of cat #{self.ID} didn't work")

    def generate_lead_ceremony(self):
        """Create a leader ceremony and add it to the history"""

        load_leader_ceremonies()

        # determine which dict we're pulling from
        if game.clan.instructor.status.group == CatGroup.DARK_FOREST:
            starclan = False
            ceremony_dict: Dict = LEAD_CEREMONY_DF
        else:
            starclan = True
            ceremony_dict: Dict = LEAD_CEREMONY_SC

        # ---------------------------------------------------------------------------- #
        #                                    INTRO                                     #
        # ---------------------------------------------------------------------------- #
        all_intros = ceremony_dict["intros"]

        # filter the intros
        possible_intros = []
        for intro in all_intros:
            tags = all_intros[intro]["tags"]

            if game.clan.age != 0 and "new_clan" in tags:
                continue
            elif game.clan.age == 0 and "new_clan" not in tags:
                continue

            if (
                all_intros[intro]["lead_trait"]
                and self.personality.trait not in all_intros[intro]["lead_trait"]
            ):
                continue
            possible_intros.append(all_intros[intro])

        if chosen_intro := choice(possible_intros):
            intro = choice(chosen_intro["text"])
            intro = leader_ceremony_text_adjust(
                Cat,
                intro,
                self,
            )
        else:
            intro = "this should not appear"

        # ---------------------------------------------------------------------------- #
        #                                 LIFE GIVING                                  #
        # ---------------------------------------------------------------------------- #
        life_givers = []
        dead_relations = []
        life_giving_leader = None

        # grab life givers that the cat actually knew in life and sort by amount of relationship!
        relationships = self.relationships.values()

        for rel in relationships:
            kitty = self.fetch_cat(rel.cat_to)
            if kitty and kitty.dead and kitty.status.rank != CatRank.NEWBORN:
                # check where they reside
                if starclan:
                    if kitty.status.group != CatGroup.STARCLAN:
                        continue
                else:
                    if kitty.status.group != CatGroup.DARK_FOREST:
                        continue
                # guides aren't allowed here
                if kitty == game.clan.instructor:
                    continue
                else:
                    dead_relations.append(rel)

        # sort relations by the strength of their relationship
        dead_relations.sort(
            key=lambda rel: rel.romantic_love
            + rel.platonic_like
            + rel.admiration
            + rel.comfortable
            + rel.trust,
            reverse=True,
        )

        # if we have relations, then make sure we only take the top 8
        if dead_relations:
            for i, rel in enumerate(dead_relations):
                if i == 8:
                    break
                if rel.cat_to.status.is_leader:
                    life_giving_leader = rel.cat_to
                    continue
                life_givers.append(rel.cat_to.ID)

        cats_in_afterlife = [
            self.fetch_cat(i)
            for i in game.clan.clan_cats
            if self.fetch_cat(i)
            and i not in life_givers
            and self.fetch_cat(i).status.group
            == (CatGroup.STARCLAN if starclan else CatGroup.DARK_FOREST)
        ]

        # check amount of life givers, if we need more, then grab from the other dead cats
        if len(life_givers) < 8:
            amount = 8 - len(life_givers)

            possible_dead_cats = [
                i
                for i in cats_in_afterlife
                if i.status.rank not in (CatRank.LEADER, CatRank.NEWBORN)
            ]
            # this part just checks how many cats are available, if there aren't enough to fill all the slots,
            # then we just take however many are available

            if len(possible_dead_cats) - 1 < amount:
                extra_givers = possible_dead_cats
            else:
                extra_givers = sample(possible_dead_cats, k=amount)

            life_givers.extend(extra_givers)

        # making sure we have a leader at the end
        ancient_leader = False
        leaders = [x for x in cats_in_afterlife if x.status.is_leader]
        if not life_giving_leader and leaders:
            # choosing if the life giving leader will be the oldest leader or previous leader
            coin_flip = randint(1, 2)
            if coin_flip == 1:
                # pick the oldest leader
                leaders.sort(key=lambda x: -1 * int(x.dead_for))
                ancient_leader = True
                life_giving_leader = leaders[0]
            else:
                # pick previous leader
                leaders.sort(key=lambda x: int(Cat.fetch_cat(x).dead_for))
                life_giving_leader = leaders[0]

        if life_giving_leader:
            life_givers.append(life_giving_leader)

        # check amount again, if more are needed then we'll add the ghost-y cats at the end
        if len(life_givers) < 9:
            unknown_blessing = True
        else:
            unknown_blessing = False
        extra_lives = str(9 - len(life_givers))
        possible_lives = ceremony_dict["lives"]
        lives = []
        used_lives = []
        used_virtues = []
        for giver in life_givers:
            giver_cat = self.fetch_cat(giver)
            if not giver_cat:
                continue
            life_list = []
            for life in possible_lives:
                tags = possible_lives[life]["tags"]
                rank = giver_cat.status.rank

                if "unknown_blessing" in tags:
                    continue

                if "guide" in tags and giver_cat != game.clan.instructor:
                    continue
                if game.clan.age != 0 and "new_clan" in tags:
                    continue
                elif game.clan.age == 0 and "new_clan" not in tags:
                    continue
                if "old_leader" in tags and not ancient_leader:
                    continue
                if "leader_parent" in tags and giver_cat.ID not in self.get_parents():
                    continue
                elif "leader_child" in tags and giver_cat.ID not in self.get_children():
                    continue
                elif (
                    "leader_sibling" in tags and giver_cat.ID not in self.get_siblings()
                ):
                    continue
                elif "leader_mate" in tags and giver_cat.ID not in self.mate:
                    continue
                elif (
                    "leader_former_mate" in tags
                    and giver_cat.ID not in self.previous_mates
                ):
                    continue
                if "leader_mentor" in tags and giver_cat.ID not in self.former_mentor:
                    continue
                if (
                    "leader_apprentice" in tags
                    and giver_cat.ID not in self.former_apprentices
                ):
                    continue
                if (
                    possible_lives[life]["rank"]
                    and rank not in possible_lives[life]["rank"]
                ):
                    continue
                if (
                    possible_lives[life]["lead_trait"]
                    and self.personality.trait not in possible_lives[life]["lead_trait"]
                ):
                    continue
                if possible_lives[life]["star_trait"] and (
                    giver_cat.personality.trait
                    not in possible_lives[life]["star_trait"]
                ):
                    continue
                life_list.extend(list(possible_lives[life]["life_giving"]))

            i = 0
            chosen_life = {}
            while i < 10:
                attempted = []
                if life_list:
                    chosen_life = choice(life_list)
                    if chosen_life not in used_lives and chosen_life not in attempted:
                        break
                    attempted.append(chosen_life)
                    i += 1
                else:
                    print(
                        f"WARNING: life list had no items for giver #{giver_cat.ID}. Using default life. "
                        f"If you are a beta tester, please report and ping scribble along with "
                        f"all the info you can about the giver cat mentioned in this warning."
                    )
                    chosen_life = ceremony_dict["default_life"]
                    break

            used_lives.append(chosen_life)
            if "virtue" in chosen_life:
                poss_virtues = [
                    i for i in chosen_life["virtue"] if i not in used_virtues
                ] or ["faith", "friendship", "love", "strength"]
                virtue = choice(poss_virtues)
                used_virtues.append(virtue)
            else:
                virtue = None

            lives.append(
                leader_ceremony_text_adjust(
                    Cat,
                    chosen_life["text"],
                    leader=self,
                    life_giver=giver,
                    virtue=virtue,
                )
            )
        if unknown_blessing:
            possible_blessing = []
            for life in possible_lives:
                tags = possible_lives[life]["tags"]

                if "unknown_blessing" not in tags:
                    continue

                if (
                    possible_lives[life]["lead_trait"]
                    and self.personality.trait not in possible_lives[life]["lead_trait"]
                ):
                    continue
                possible_blessing.append(possible_lives[life])
            chosen_blessing = choice(possible_blessing)
            chosen_text = choice(chosen_blessing["life_giving"])
            lives.append(
                leader_ceremony_text_adjust(
                    Cat,
                    chosen_text["text"],
                    leader=self,
                    virtue=chosen_text["virtue"],
                    extra_lives=extra_lives,
                )
            )
        all_lives = "<br><br>".join(lives)

        # ---------------------------------------------------------------------------- #
        #                                    OUTRO                                     #
        # ---------------------------------------------------------------------------- #

        # get the outro
        all_outros = ceremony_dict["outros"]

        possible_outros = []
        for outro in all_outros:
            tags = all_outros[outro]["tags"]

            if game.clan.age != 0 and "new_clan" in tags:
                continue
            elif game.clan.age == 0 and "new_clan" not in tags:
                continue

            if (
                all_outros[outro]["lead_trait"]
                and self.personality.trait not in all_outros[outro]["lead_trait"]
            ):
                continue
            possible_outros.append(all_outros[outro])

        chosen_outro = choice(possible_outros)

        if chosen_outro:
            if life_givers:
                giver = life_givers[-1]
            else:
                giver = None
            outro = choice(chosen_outro["text"])
            outro = leader_ceremony_text_adjust(
                Cat,
                outro,
                leader=self,
                life_giver=giver,
            )
        else:
            outro = "this should not appear"

        full_ceremony = "<br><br>".join([intro, all_lives, outro])
        self.history.lead_ceremony = full_ceremony

    # ---------------------------------------------------------------------------- #
    #                              moon skip functions                             #
    # ---------------------------------------------------------------------------- #

    def one_moon(self):
        """Handles a moon skip for an alive cat."""
        old_age = self.age
        if not self.immortality:
            self.moons += 1
        if self.moons > 0 and self.status.rank == CatRank.NEWBORN:
            self.status._change_rank(CatRank.KITTEN)
        self.in_camp = 1

        if not self.status.alive_in_player_clan:
            # this is handled in events.py
            self.personality.set_kit(self.age.is_baby())
            self.thoughts()
            return

        if self.dead and not self.faded:
            self.thoughts()
            return

        if old_age != self.age:
            # Things to do if the age changes
            self.personality.facet_wobble(facet_max=2)
            self.pelt.rebuild_sprite = True

        # Set personality to correct type
        self.personality.set_kit(self.age.is_baby())
        # Upon age-change

        if self.status.rank.is_any_apprentice_rank():
            self.update_mentor()

    def thoughts(self):
        """Generates a thought for the cat, which displays on their profile."""
        all_cats = self.all_cats
        other_cat = choice(list(all_cats.keys()))
        game_mode = switch_get_value(Switch.game_mode)
        biome = switch_get_value(Switch.biome)
        camp = switch_get_value(Switch.camp_bg)
        secondary_biome = switch_get_value(Switch.secondary_biome)
        tertiary_biome = switch_get_value(Switch.tertiary_biome)
        secondary_biome_weight = switch_get_value(Switch.secondary_biome_weight)
        tertiary_biome_weight = switch_get_value(Switch.tertiary_biome_weight)

        try:
            season = game.clan.current_season
        except Exception:
            season = None

        # this figures out where the cat is
        where_kitty = None
        if self.dead:
            if self.status.group == CatGroup.DARK_FOREST:
                where_kitty = "hell"
            elif self.status.group == CatGroup.UNKNOWN_RESIDENCE:
                where_kitty = "UR"
            else:
                where_kitty = "starclan"

        elif self.status.is_outsider:
            where_kitty = "outside"
        else:
            where_kitty = "inside"

        # get other cat
        i = 0
        # for cats inside the clan
        if where_kitty == "inside":
            dead_chance = getrandbits(4)
            while (
                other_cat == self.ID
                and len(all_cats) > 1
                or (all_cats.get(other_cat).dead and dead_chance != 1)
                or (other_cat not in self.relationships)
            ):
                other_cat = choice(list(all_cats.keys()))
                i += 1
                if i > 100:
                    other_cat = None
                    break
        # for dead cats
        elif where_kitty in ("starclan", "hell", "UR"):
            while other_cat == self.ID and len(all_cats) > 1:
                other_cat = choice(list(all_cats.keys()))
                i += 1
                if i > 100:
                    other_cat = None
                    break
        # for cats currently outside
        # it appears as for now, kittypets and loners can only think about outsider cats
        elif where_kitty == "outside":
            while (
                other_cat == self.ID
                and len(all_cats) > 1
                or (other_cat not in self.relationships)
            ):
                other_cat = choice(list(all_cats.keys()))
                i += 1
                if i > 100:
                    other_cat = None
                    break

        other_cat = all_cats.get(other_cat)

        # get chosen thought
        chosen_thought = Thoughts.get_chosen_thought(
            self, other_cat, game_mode, biome, secondary_biome, tertiary_biome, secondary_biome_weight, tertiary_biome_weight, season, camp
        )

        chosen_thought = event_text_adjust(
            self.__class__,
            chosen_thought,
            main_cat=self,
            random_cat=other_cat,
            clan=game.clan,
        )

        # insert thought
        self.thought = str(chosen_thought)

    def relationship_interaction(self):
        """Randomly choose a cat of the Clan and have an interaction with them."""
        cats_to_choose = [
            iter_cat
            for iter_cat in Cat.all_cats.values()
            if iter_cat.ID != self.ID and iter_cat.status.alive_in_player_clan
        ]
        # if there are no cats to interact, stop
        if not cats_to_choose:
            return

        chosen_cat = choice(cats_to_choose)
        if chosen_cat.ID not in self.relationships:
            self.create_one_relationship(chosen_cat)
        relevant_relationship = self.relationships[chosen_cat.ID]
        relevant_relationship.start_interaction()

        # handle contact with ill cat if
        if self.is_ill():
            relevant_relationship.cat_to.contact_with_ill_cat(self)
        if relevant_relationship.cat_to.is_ill():
            self.contact_with_ill_cat(relevant_relationship.cat_to)

    def moon_skip_illness(self, illness):
        """handles the moon skip for illness"""
        if not self.is_ill():
            return True
        
        if illness == "rampaging":
            if self.guided:
                self.guided = False
                self.healed_condition = True
                return False
            # COME BACK HERE

        if self.illnesses[illness]["event_triggered"]:
            self.illnesses[illness]["event_triggered"] = False
            return True

        mortality = self.illnesses[illness]["mortality"]

        # leader should have a higher chance of death
        if self.status.is_leader and mortality != 0:
            mortality = int(mortality * 0.7)
            if mortality == 0:
                mortality = 1

        if mortality and not int(random() * mortality):
            if self.status.is_leader:
                self.leader_death_heal = True
                game.clan.leader_lives -= 1

            self.die()
            return False

        moons_with = game.clan.age - self.illnesses[illness]["moon_start"]

        # focus buff
        moons_prior = constants.CONFIG["focus"]["rest and recover"][
            "moons_earlier_healed"
        ]

        if self.illnesses[illness]["duration"] - moons_with <= 0:
            self.healed_condition = True
            return False

        # CLAN FOCUS! - if the focus 'rest and recover' is selected
        elif (
            get_clan_setting("rest and recover")
            and self.illnesses[illness]["duration"] + moons_prior - moons_with <= 0
        ):
            self.healed_condition = True
            return False

    def moon_skip_injury(self, injury):
        """handles the moon skip for injury"""
        if not self.is_injured():
            return True

        if self.injuries[injury]["event_triggered"] is True:
            self.injuries[injury]["event_triggered"] = False
            return True

        mortality = self.injuries[injury]["mortality"]

        # leader should have a higher chance of death
        if self.status.is_leader and mortality != 0:
            mortality = int(mortality * 0.7)
            if mortality == 0:
                mortality = 1

        if mortality and not int(random() * mortality):
            if self.status.is_leader:
                game.clan.leader_lives -= 1
            self.die()
            return False

        moons_with = game.clan.age - self.injuries[injury]["moon_start"]

        # focus buff
        moons_prior = constants.CONFIG["focus"]["rest and recover"][
            "moons_earlier_healed"
        ]

        # if the cat has an infected wound, the wound shouldn't heal till the illness is cured
        if (
            not self.injuries[injury]["complication"]
            and self.injuries[injury]["duration"] - moons_with <= 0
        ):
            self.healed_condition = True
            return False

        # CLAN FOCUS! - if the focus 'rest and recover' is selected
        elif (
            not self.injuries[injury]["complication"]
            and get_clan_setting("rest and recover")
            and self.injuries[injury]["duration"] + moons_prior - moons_with <= 0
        ):
            self.healed_condition = True
            return False
        
    def system_core(self):
        template = {
            "ID": "0",
            "name": "",
            "gender": "",
            "personality": "",
            "role": "host",
            "other": "core",
            "origin": "core",
            "splits": []
        }
        if game.clan:
            if self.name:
                template["name"] = self.name.prefix + self.name.suffix
                template["gender"] = self.genderalign
                # it annoyed me that the host's personality was at the end cause it's not initially set here
                # so now it is
                template["personality"] = choice(self.all_adult_personalities)
        self.alters.append(template)

    def add_split(self, new_alter, origin):
        if len(self.alters) > 0:
            if self.alters[new_alter]:
                self.alters[new_alter]["splits"].append(origin)

    def new_alter(self, condition):
        template = {
            "ID": "",
            "name": "",
            "gender": "",
            "personality": "",
            "role": "",
            "other": "cat",
            "origin": "core",
            "splits": []
        }
        adult_canon = [
            "Fireheart", "Graystripe", "Sandstorm", "Squirrelflight", "Brambleclaw", "Hollyleaf", "Jayfeather",
            "Lionblaze", "Dovewing", "Ivypool", "Yellowfang", "Ravenpaw", "Bristlefrost", "Ashfur", "Cinderpelt",
            "Alderheart", "Needletail", "Hawkfrost", "Mothwing", "Leafpool", "Crowfeather", "Nightheart", "Willowpelt",
            "Shadowsight", "Tigerheart", "Grey Wing", "River", "Night", "Violetshine", "Twigbranch",  "Sol",
            "Mapleshade", "Moth Flight", "Cinderheart", "Tall Shadow", "Talltail", "Onewhisker", "Darktail",
            "Tigerclaw", "Scourge", "Brightheart", "Briarlight", "Cloudtail", "Thunder", "Feathertail", "Spottedleaf",
            "Bluefur", "Bumblestripe", "Poppyfrost", "Stormfur", "Mistyfoot", "Star Flower", "Fallen Leaves",
            "Berrynose", "Tawnypelt", "Webfoot", "Jake", "Sparkpelt", "Rootspring", "Nightcloud"
        ]
        # oh jesus TODO: add more adol names D:
        adol_canon = [
            # from Mapleshade's Vengeance
            "Flowerpaw",

            # from DotC
            # NOTE: since Tiny Branch was 5 moons old when he died, doesn't have "-kit" in his name, and there aren't
            # many adolescent names, I decided to include him in both lists
            "Tiny Branch",

            # Ferncloud's relatives
            "Cherrypaw"
        ]

        kit_canon = [
            # category-less cats
            "Snowkit", "Mosskit", "Lynxkit", "Galekit", "Haze", "Stream", "Tadpole",

            # from Mapleshade's Vengeance
            "Petalkit", "Patchkit",

            # from DotC
            "Fluttering Bird", "Emberkit", "Morning Whisker", "Bramble", "Tiger Tail", "Pale Sky", "Tiny Branch",
            "Rumble", "Lightning",

            # Ferncloud's relatives
            "Hollykit", "Tulipkit", "Elderkit", "Chestnutkit", "Rowankit",

            # victims of Brokenstar's reign
            "Blossomkit", "Swampkit", "Marigoldkit", "Mintkit", "Mosspaw", "Badgerfang",

            # names that belong to multiple cats
            "Larchkit"
        ]

        template["ID"] = str(len(self.alters) + 1)
        template["role"] = choice(["co-host", "caregiver", "little", "protector", "trauma holder", "persecutor"])
        alter_personality = choice(self.all_adult_personalities)

        if condition in ["budding spirit", "shattered soul"]:
            extra = randint(1, 5)
            if extra == 1:
                template["other"] = choice(["noncat", "loner", "rogue", "kittypet", "otherclan", "fictive", "factive",
                                            "fuzztive"])

            rng = randint(1, 10)
            is_intersex = True if (randint(1, 25) < 3 and self.gender == "intersex") else False
            if rng <= 2:
                genderqueer_list = ["nonbinary", "neutrois", "agender", "genderqueer", "demigirl", "demiboy",
                                    "demienby", "genderfluid", "genderfae", "genderfaun", "genderflor", "bigender",
                                    "pangender", "???"]
                if is_intersex:
                    genderqueer_list.append("intergender")
                gender = choice(genderqueer_list)
            else:
                if is_intersex:
                    gender = "intersex"
                elif randint(1, 2) == 1:
                    gender = "female"
                else:
                    gender = "male"
            template["gender"] = gender
        
            if os.path.exists('resources/dicts/names/names.json'):
                with open('resources/dicts/names/names.json') as read_file:
                    names_dict = ujson.loads(read_file.read())
            if template["other"] == "fictive" or template["other"] == "fuzztive":
                canon_chance = randint(1, 5)
                if canon_chance == 1:
                    alter_name = choice(adult_canon)
                else:
                    alter_name = choice(names_dict["normal_prefixes"])
            else:
                alter_name = choice(names_dict["normal_prefixes"])

            if template["role"] == "little":
                if template["other"] in ["fictive", "fuzztive"]:
                    canon_chance = randint(1, 5)
                    if canon_chance == 1:
                        rng = randint(1, 2)
                        if rng == 1:
                            alter_name = choice(adol_canon)
                            alter_personality = choice(self.all_adult_personalities)
                        else:
                            alter_name = choice(kit_canon)
                            alter_personality = choice(self.all_kit_personalities)
                    else:
                        alter_name = choice(names_dict["normal_prefixes"])
                        rng = randint(1, 2)
                        if rng == 1:
                            alter_name += "paw"
                            alter_personality = choice(self.all_adult_personalities)
                        else:
                            alter_name += "kit"
                            alter_personality = choice(self.all_kit_personalities)
                else:
                    alter_name = choice(names_dict["normal_prefixes"])
                    rng = randint(1, 2)
                    if rng == 1:
                        alter_name += "paw"
                    else:
                        alter_name += "kit"
                        alter_personality = choice(self.all_kit_personalities)
            elif template["other"] == "cat" or template["other"] == "otherclan" or template["other"] == "factive":
                alter_name += choice(names_dict["normal_suffixes"])
            if template["other"] == "rogue" or template["other"] == "loner" or template["other"] == "kittypet":
                alter_name = choice(names_dict["loner_names"])
            if template["other"] == "fuzztive" and randint(1, 2) == 1:  # feline addition
                alter_name += choice(names_dict["normal_suffixes"])
        else:  # fractured spirit alter
            extra = randint(1, 20)
            if extra == 1:
                template["other"] = choice(["noncat", "rogue", "loner", "kittypet", "otherclan", "fictive", "factive",
                                            "fuzztive"])
            different_gender = randint(1, 5)
            gender = None
            if different_gender == 1:
                rng = randint(1, 10)
                is_intersex = True if (randint(1, 25) < 3 and self.gender == "intersex") else False
                if rng <= 2:
                    genderqueer_list = ["nonbinary", "neutrois", "agender", "genderqueer", "demigirl", "demiboy",
                                        "demienby", "genderfluid", "genderfae", "genderfaun", "genderflor", "bigender",
                                        "pangender", "???"]
                    if is_intersex:
                        genderqueer_list.append("intergender")
                    gender = choice(genderqueer_list)
                else:
                    if is_intersex:
                        gender = "intersex"
                    elif randint(1, 2) == 1:
                        gender = "female"
                    else:
                        gender = "male"
            
            if gender:
                template["gender"] = gender
            else:
                template["gender"] = str(self.genderalign)

            if os.path.exists('resources/dicts/names/names.json'):
                with open('resources/dicts/names/names.json') as read_file:
                    names_dict = ujson.loads(read_file.read())
            different_name = randint(1, 5)
            if different_name == 1:  # different name entirely
                if template["other"] == "fictive" or template["other"] == "fuzztive":
                    canon_chance = randint(1, 5)
                    if canon_chance == 1:
                        alter_name = choice(adult_canon)
                    else:
                        alter_name = choice(names_dict["normal_prefixes"])
                        different_personality = randint(1, 5)
                        if different_personality == 1:
                            alter_personality = choice(self.all_adult_personalities)
                        else:
                            alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
                else:
                    alter_name = choice(names_dict["normal_prefixes"])
                    different_personality = randint(1, 5)
                    if different_personality == 1:
                        alter_personality = choice(self.all_adult_personalities)
                    else:
                        alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
                if template["role"] == "little":
                    if template["other"] in ["fictive", "fuzztive"]:
                        canon_chance = randint(1, 5)
                        different_personality = randint(1, 5)
                        if canon_chance == 1:
                            rng = randint(1, 2)
                            if rng == 1:
                                alter_name = choice(adol_canon)
                                if different_personality == 1:
                                    alter_personality = choice(self.all_adult_personalities)
                                else:
                                    alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
                            else:
                                alter_name = choice(kit_canon)
                                alter_personality = choice(self.all_kit_personalities)
                        else:
                            alter_name = choice(names_dict["normal_prefixes"])
                            rng = randint(1, 2)
                            if rng == 1:
                                alter_name += "paw"
                                if different_personality == 1:
                                    alter_personality = choice(self.all_adult_personalities)
                                else:
                                    alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
                            else:
                                alter_name += "kit"
                                alter_personality = choice(self.all_kit_personalities)
                    else:
                        alter_name = choice(names_dict["normal_prefixes"])
                        rng = randint(1, 2)
                        if rng == 1:
                            alter_name += "paw"
                            different_personality = randint(1, 5)
                            if different_personality == 1:
                                alter_personality = choice(self.all_adult_personalities)
                            else:
                                alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
                        else:
                            alter_name += "kit"
                            alter_personality = choice(self.all_kit_personalities)
                # if not little
                elif template["other"] == "cat" or template["other"] == "otherclan" or template["other"] == "factive":
                    alter_name += choice(names_dict["normal_suffixes"])
                    different_personality = randint(1, 5)
                    if different_personality == 1:
                        alter_personality = choice(self.all_adult_personalities)
                    else:
                        alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
                if template["other"] == "rogue" or template["other"] == "loner" or template["other"] == "kittypet":
                    alter_name = choice(names_dict["loner_names"])
                    different_personality = randint(1, 5)
                    if different_personality == 1:
                        alter_personality = choice(self.all_adult_personalities)
                    else:
                        alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
            elif different_name == 2:  # different prefix
                alter_name = choice(names_dict["normal_prefixes"])
                if template["role"] == "little":
                    rng = randint(1, 2)
                    if rng == 1:
                        alter_name += "paw"
                        different_personality = randint(1, 5)
                        if different_personality == 1:
                            alter_personality = choice(self.all_adult_personalities)
                        else:
                            alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
                    else:
                        alter_name += "kit"
                        alter_personality = choice(self.all_kit_personalities)
                else:
                    if template["other"] == "cat" or template["other"] == "otherclan":
                        alter_name += self.name.suffix
                    different_personality = randint(1, 5)
                    if different_personality == 1:
                        alter_personality = choice(self.all_adult_personalities)
                    else:
                        alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
            elif different_name == 3 or different_name == 4:  # different suffix
                alter_name = self.name.prefix
                if template["role"] == "little":
                    rng = randint(1, 2)
                    if rng == 1:
                        alter_name += "paw"
                        different_personality = randint(1, 5)
                        if different_personality == 1:
                            alter_personality = choice(self.all_adult_personalities)
                        else:
                            alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
                    else:
                        alter_name += "kit"
                        alter_personality = choice(self.all_kit_personalities)
                else:
                    if template["other"] == "cat" or template["other"] == "otherclan":
                        alter_name += choice(names_dict["normal_suffixes"])
                    different_personality = randint(1, 5)
                    if different_personality == 1:
                        alter_personality = choice(self.all_adult_personalities)
                    else:
                        alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
            else:  # same name
                alter_name = self.name.prefix
                if template["role"] == "little":
                    rng = randint(1, 2)
                    if rng == 1:
                        alter_name += "paw"
                        different_personality = randint(1, 5)
                        if different_personality == 1:
                            alter_personality = choice(self.all_adult_personalities)
                        else:
                            alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])
                    else:
                        alter_name += "kit"
                        alter_personality = choice(self.all_kit_personalities)
                else:
                    if template["other"] == "cat" or template["other"] == "otherclan":
                        alter_name += self.name.suffix
                    different_personality = randint(1, 5)
                    if different_personality == 1:
                        alter_personality = choice(self.all_adult_personalities)
                    else:
                        alter_personality = choice([str(self.personality.trait), str(self.personality.trait2)])

        template["personality"] = alter_personality
        template["name"] = alter_name
        if template["ID"] != "1":
            splitrng = randint(1, (len(self.alters) + 1))
            if splitrng < (len(self.alters) + 1):
                template["origin"] = self.alters[(splitrng - 1)]['name']
                self.add_split((splitrng - 1), template["name"])
        if template["origin"] == "core":
            self.add_split(0, template["name"])
        self.alters.append(template)

    def moon_skip_permanent_condition(self, condition):
        """handles the moon skip for permanent conditions"""
        if not self.is_disabled():
            return "skip"

        if self.permanent_condition[condition]["event_triggered"]:
            self.permanent_condition[condition]["event_triggered"] = False
            return "skip"

        mortality = self.permanent_condition[condition]["mortality"]
        moons_until = self.permanent_condition[condition]["moons_until"]
        born_with = self.permanent_condition[condition]["born_with"]
        
        if self.permanent_condition[condition]["moons_until"] == -2:
            # correcting misdiagnoses
            if self.permanent_condition[condition]["misdiagnosis"] is not False:
                exp_bonus = 0
                meds = find_alive_cats_with_rank(Cat, [CatRank.MEDICINE_CAT, CatRank.MEDICINE_APPRENTICE], sort=True)
                if len(meds) > 0:
                    for med in meds:
                        if med._experience > 75:
                            exp_bonus += 3
                        elif med._experience > 50:
                            exp_bonus += 1
                        elif med._experience > 25:
                            exp_bonus -= 1
                        else:
                            exp_bonus -= 3
                else:
                    exp_bonus -= 5
                correct_chance = randint(0, 20) + exp_bonus
                if correct_chance > 18:
                    text1 = str(self.name) + " has come to realize that " + self.pronouns[0]["poss"] + " " + self.permanent_condition[condition]["misdiagnosis"] + " is actually " + condition + "."
                    text2 = str(self.name) + " always felt that " + self.permanent_condition[condition]["misdiagnosis"] + " didn't fit " + self.pronouns[0]["poss"] + " experience, but " + condition + " fits perfectly!"
                    text3 = str(self.name) + " was optimistic for a new diagnosis, but now fears that " + condition + " is wrong too."
                    text = choice([text1, text2, text3])
                    if not game_setting_get("warriorified names"):
                        if condition in Cat.dad_names:
                            text = text.replace(condition, Cat.dad_names.get(condition))
                        if self.permanent_condition[condition]["misdiagnosis"] in Cat.dad_names:
                            text = text.replace(self.permanent_condition[condition]["misdiagnosis"], Cat.dad_names.get(self.permanent_condition[condition]["misdiagnosis"]))
                    game.cur_events_list.append(Single_Event(text, ["misc"], [self.ID]))
                    self.permanent_condition[condition]["misdiagnosis"] = False
        
        # chance of splitting if plural
        if condition in ["shattered soul", "budding spirit", "fractured spirit"]:
            splitting = randint(1, 100)
            if len(self.alters) < 1:
                self.new_alter(condition)
            if splitting < 15:
                if len(self.alters) < constants.CONFIG["condition_related"]["max_alters"]:
                    num_splits = 1
                    if constants.CONFIG["condition_related"]["max_splits"] > 1:
                        num_splits = randint(1, constants.CONFIG["condition_related"]["max_splits"])
                    for i in range(num_splits):
                        self.new_alter(condition)
            can_front = []
            if self.alters[0]["ID"] != "0":
                can_front = [str(self.name)]
            for alter in self.alters:
                if "recovering from birth" in self.injuries or "faux pregnant" in self.injuries or "pregnant" in self.injuries or "turmoiled litter" in self.illnesses:
                    if alter["role"] != "little":
                        can_front.append(alter["name"])
                else:
                    can_front.append(alter["name"])
            self.front = choice(can_front)
            if self.moons > 12 and not self.status.rank.is_any_apprentice_rank():
                if get_clan_setting("plural names"):
                    # chance of cat choosing a plural name: 1 in 100 default
                    if constants.CONFIG["condition_related"]["plural_names"] > 1:
                        chance = randint(1, constants.CONFIG["condition_related"]["plural_names"])
                        if chance == 1:
                            # CHOOSE PLURAL NAME
                            if os.path.exists('resources/dicts/names/names.json'):
                                with open('resources/dicts/names/names.json') as read_file:
                                    names_dict = ujson.loads(read_file.read())
                                    if self.name.suffix not in names_dict["normal_plural_suffixes"] and self.name.suffix not in names_dict["leader_plural_suffixes"]:
                                        self.name.specsuffix_hidden = True
                                        plural = choice(names_dict["normal_plural_suffixes"])
                                        old_suffix = self.name.suffix
                                        if self.status == "leader":
                                            plural = choice(names_dict["leader_plural_suffixes"])
                                            old_suffix = "star"
                                        self.name.suffix = plural
                                        text = f"{self.name.prefix}{old_suffix}'s headmates have discussed things, and they've decided that a collective name will suit them better, like {self.name.prefix}{self.name.suffix}!"
                                        game.cur_events_list.append(Single_Event(text, ["misc"], [self.ID]))

        # handling the countdown till a congenital condition is revealed
        if moons_until is not None and moons_until >= 0 and born_with is True:
            self.permanent_condition[condition]["moons_until"] = int(moons_until - 1)
            self.permanent_condition[condition]["moons_with"] = 0
            if self.permanent_condition[condition]["moons_until"] != -1:
                return "skip"
        if (
            self.permanent_condition[condition]["moons_until"] == -1
            and self.permanent_condition[condition]["born_with"] is True
        ):
            self.permanent_condition[condition]["moons_until"] = -2
            return "reveal"

        # leader should have a higher chance of death
        if self.status.is_leader and mortality != 0:
            mortality = int(mortality * 0.7)
            if mortality == 0:
                mortality = 1

        if mortality and not int(random() * mortality):
            if self.status.is_leader:
                game.clan.leader_lives -= 1
            self.die()
            return "continue"

    # ---------------------------------------------------------------------------- #
    #                                   relative                                   #
    # ---------------------------------------------------------------------------- #
    def get_parents(self):
        """Returns list containing parents of cat(id)."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return self.inheritance.parents.keys()

    def get_siblings(self):
        """Returns list of the siblings(id)."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return self.inheritance.siblings.keys()

    def get_children(self):
        """Returns list of the children (ids)."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return self.inheritance.kits.keys()

    def is_grandparent(self, other_cat: Cat):
        """Check if the cat is the grandparent of the other cat."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return other_cat.ID in self.inheritance.grand_kits.keys()

    def is_parent(self, other_cat: Cat):
        """Check if the cat is the parent of the other cat."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return other_cat.ID in self.inheritance.kits.keys()

    def is_sibling(self, other_cat: Cat):
        """Check if the cats are siblings."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return other_cat.ID in self.inheritance.siblings.keys()

    def is_littermate(self, other_cat: Cat):
        """Check if the cats are littermates."""
        if other_cat.ID not in self.inheritance.siblings.keys():
            return False
        litter_mates = [
            key
            for key, value in self.inheritance.siblings.items()
            if "litter mates" in value["additional"]
        ]
        return other_cat.ID in litter_mates

    def is_uncle_aunt(self, other_cat: Cat):
        """Check if the cats are related as uncle/aunt and niece/nephew."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return other_cat.ID in self.inheritance.siblings_kits.keys()

    def is_cousin(self, other_cat: Cat):
        """Check if this cat and other_cat are cousins."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        return other_cat.ID in self.inheritance.cousins.keys()

    def is_related(self, other_cat, cousin_allowed):
        """Checks if the given cat is related to the current cat, according to the inheritance."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        if cousin_allowed:
            return other_cat.ID in self.inheritance.all_but_cousins
        return other_cat.ID in self.inheritance.all_involved

    def get_relatives(self, cousin_allowed=True) -> list:
        """Returns a list of ids of all nearly related ancestors."""
        if not self.inheritance:
            self.inheritance = Inheritance(self)
        if cousin_allowed:
            return self.inheritance.all_involved
        return self.inheritance.all_but_cousins

    # ---------------------------------------------------------------------------- #
    #                                  conditions                                  #
    # ---------------------------------------------------------------------------- #

    def get_reincarnation(self):
        if self.status.group == CatGroup.DARK_FOREST:
            backstory = "reincarnation_df"
        elif self.status.group == CatGroup.UNKNOWN_RESIDENCE:
            backstory = "reincarnation_unknown"
        else:
            backstory = "reincarnation_starclan"
        reincarnation = Cat(parent1=self.ID, parent2=self.ID, prefix=self.name.prefix, status="newborn", moons=0, backstory=backstory, gender=self.gender, past_life=self.ID)
        game.clan.add_cat(reincarnation)
        # we use self as both parents to increase similarity, but obviously
        # we dont want that to stay as the parents LOL
        reincarnation.parent1 = None
        reincarnation.parent2 = None
        reincarnation.history.add_beginning(clan_born=False)
        reincarnation.past_life = self.ID
        self.reincarnation = reincarnation.ID
        # if game.clan.clan_settings["reincarnation_autofade"]:
        # self.faded = True
        '''
        
        "reincarnation_autofade": [
            "Cats fade upon reincarnation",
            "After reincarnation, a cat will automatically fade.",
            false
        ],
        '''
    
    def get_ill(self, name, event_triggered=False, lethal=True, severity="default"):
        """Add an illness to this cat.

        :param name: name of the illness (str)
        :param event_triggered: Whether to have this illness skip `moon_skip_illness` for 1 moon, default `False` (bool)
        :param lethal: Allow lethality, default `True` (bool)
        :param severity: Override severity, default `'default'` (str, accepted values `'minor'`, `'major'`, `'severe'`)
        """
        if self.dead:
            return

        if name not in ILLNESSES:
            print(f"WARNING: {name} is not in the illnesses collection.")
            return
        if name == "kittencough" and self.status.rank != CatRank.KITTEN:
            return

        if constants.CONFIG["event_generation"]["max_illnesses"] > 0:
            if len(self.illnesses) == constants.CONFIG["event_generation"]["max_illnesses"]:
                return
        
        eating_disorders = ["anorexia", "ARFID", "bulimia", "binge-eating disorder", "food hoarding", "pica"]
        self_harm = ["harmful stims"]
        dissociation = ["derealization", "depersonalization", "amnesia"]
        psychosis = ["delusions", "psychotic episode", "hostile hallucinations", "paranoia", "ongoing psychosis"]
        night_dirtmaking_n_nest_wetting = ["night dirtmaking", "nest wetting"]
        all_triggers = eating_disorders + self_harm + dissociation + psychosis + night_dirtmaking_n_nest_wetting
        if not game_setting_get("allow_triggers") and name in all_triggers:
            return
        else:
            if not game_setting_get("eating_disorders") and name in eating_disorders:
                return
            if not game_setting_get("self_harm") and name in self_harm:
                return
            if not game_setting_get("dissociation") and name in dissociation:
                return
            if not game_setting_get("psychosis") and name in psychosis:
                return
            if not game_setting_get("intrusive_thoughts_TWO_woaw") and name in night_dirtmaking_n_nest_wetting:
                return
            if name in all_triggers:
                print("triggering condition: " + name)

        if name == "rampaging":
            if not self.awakened:
                return
            elif self.awakened["type"] == "guide":
                return
                
        illness = ILLNESSES[name]
        mortality = illness["mortality"][self.age.value]
        med_mortality = illness["medicine_mortality"][self.age.value]
        illness_severity = illness["severity"] if severity == "default" else severity
        duration = illness["duration"]
        med_duration = illness["medicine_duration"]

        amount_per_med = get_amount_cat_for_one_medic(game.clan)

        if medicine_cats_can_cover_clan(Cat.all_cats.values(), amount_per_med):
            duration = med_duration
        if severity != "minor":
            duration += randrange(-1, 1)
        if duration == 0:
            duration = 1

        if game.clan and game.clan.game_mode == "cruel season" and mortality != 0:
            mortality = int(mortality * 0.5)
            med_mortality = int(med_mortality * 0.5)

            # to prevent an illness gets no mortality, check and set it to 1 if needed
            if mortality == 0 or med_mortality == 0:
                mortality = 1
                med_mortality = 1
        if lethal is False:
            mortality = 0

        new_illness = Illness(
            name=name,
            severity=illness_severity,
            mortality=mortality,
            infectiousness=illness["infectiousness"],
            duration=duration,
            medicine_duration=illness["medicine_duration"],
            medicine_mortality=med_mortality,
            risks=illness["risks"],
            event_triggered=event_triggered,
        )

        if new_illness.name not in self.illnesses:
            self.illnesses[new_illness.name] = {
                "severity": new_illness.severity,
                "mortality": new_illness.current_mortality,
                "infectiousness": new_illness.infectiousness,
                "duration": new_illness.duration,
                "moon_start": game.clan.age if game.clan else 0,
                "risks": new_illness.risks,
                "event_triggered": new_illness.new,
            }

    def get_injured(self, name, event_triggered=False, lethal=True, severity="default"):
        """Add an injury to this cat.

        :param name: The injury to add
        :type name: str
        :param event_triggered: Whether to process healing immediately, defaults to False
        :type event_triggered: bool, optional
        :param lethal: _description_, defaults to True
        :type lethal: bool, optional
        :param severity: _description_, defaults to 'default'
        :type severity: str, optional
        """
        if self.dead:
            return

        eating_disorders = ["anorexia", "ARFID", "bulimia", "binge-eating disorder", "food hoarding", "pica"]
        self_harm = ["harmful stims"]
        dissociation = ["derealization", "depersonalization", "amnesia"]
        psychosis = ["delusions", "psychotic episode", "hostile hallucinations", "paranoia", "ongoing psychosis"]
        night_dirtmaking_n_nest_wetting = ["night dirtmaking", "nest wetting"]
        all_triggers = eating_disorders + self_harm + dissociation + psychosis + night_dirtmaking_n_nest_wetting
        if not game_setting_get("allow_triggers") and name in all_triggers:
            return
        else:
            if not game_setting_get("eating_disorders") and name in eating_disorders:
                return
            if not game_setting_get("self_harm") and name in self_harm:
                return
            if not game_setting_get("dissociation") and name in dissociation:
                return
            if not game_setting_get("psychosis") and name in psychosis:
                return
            if not game_setting_get("intrusive_thoughts_TWO_woaw") and name in night_dirtmaking_n_nest_wetting:
                return
            if name in all_triggers:
                print("triggering condition: " + name)

        if name not in INJURIES:
            print(f"WARNING: {name} is not in the injuries collection.")
            return

        if name == "mangled tail" and "NOTAIL" in self.pelt.scars:
            return
        if name == "torn ear" and "NOEAR" in self.pelt.scars:
            return

        injury = INJURIES[name]
        mortality = injury["mortality"][self.age.value]
        duration = injury["duration"]
        med_duration = injury["medicine_duration"]

        injury_severity = injury["severity"] if severity == "default" else severity
        if medicine_cats_can_cover_clan(
            Cat.all_cats.values(), get_amount_cat_for_one_medic(game.clan)
        ):
            duration = med_duration
        if severity != "minor":
            duration += randrange(-1, 1)
        if duration == 0:
            duration = 1

        if mortality != 0 and (game.clan and game.clan.game_mode == "cruel season"):
            mortality = int(mortality * 0.5)

            if mortality == 0:
                mortality = 1
        if lethal is False:
            mortality = 0

        new_injury = Injury(
            name=name,
            severity=injury_severity,
            duration=injury["duration"],
            medicine_duration=duration,
            mortality=mortality,
            risks=injury["risks"],
            illness_infectiousness=injury["illness_infectiousness"],
            also_got=injury["also_got"],
            cause_permanent=injury["cause_permanent"],
            event_triggered=event_triggered,
        )

        if new_injury.name not in self.injuries:
            self.injuries[new_injury.name] = {
                "severity": new_injury.severity,
                "mortality": new_injury.current_mortality,
                "duration": new_injury.duration,
                "moon_start": game.clan.age if game.clan else 0,
                "illness_infectiousness": new_injury.illness_infectiousness,
                "risks": new_injury.risks,
                "complication": None,
                "cause_permanent": new_injury.cause_permanent,
                "event_triggered": new_injury.new,
            }

        if len(new_injury.also_got) > 0 and not int(random() * 5):
            avoided = False
            if (
                "blood loss" in new_injury.also_got
                and len(
                    find_alive_cats_with_rank(Cat, [CatRank.MEDICINE_CAT], working=True)
                )
                != 0
            ):
                clan_herbs = set(game.clan.herb_supply.entire_supply.keys())
                needed_herbs = {"horsetail", "raspberry", "marigold", "cobwebs"}
                usable_herbs = list(needed_herbs.intersection(clan_herbs))

                if usable_herbs:
                    # deplete the herb
                    herb_used = choice(usable_herbs)
                    game.clan.herb_supply.remove_herb(herb_used, -1)
                    avoided = True
                    text = i18n.t("screens.med_den.blood_loss", name=self.name)
                    game.herb_events_list.append(text)

            if not avoided:
                self.also_got = True
                additional_injury = choice(new_injury.also_got)
                if additional_injury in INJURIES:
                    self.additional_injury(additional_injury)
                else:
                    self.get_ill(additional_injury, event_triggered=True)
        else:
            self.also_got = False

    def additional_injury(self, injury):
        self.get_injured(injury, event_triggered=True)

    def congenital_condition(self, cat):
        possible_conditions = []
        multiple_condition_chance = constants.CONFIG["cat_generation"]["multiple_permanent_conditions"]
        max_conditions = constants.CONFIG["cat_generation"]["max_conditions_born_with"]
        comorbidity_chance = constants.CONFIG["cat_generation"]["comorbidity_chance"]
        conditions = 1
        count = 1
        possible_comorbidities = []
        try:
            with open("resources/dicts/conditions/comorbid_conditions.json", 'r') as read_file:
                comorbid_conditions = ujson.loads(read_file.read())
        except IOError:
            comorbid_conditions = {
                "paralyzed": [
                    "curved spine"
                ],
                "constant joint pain": [
                    "curved spine"
                ],
                "seizure prone": [
                    "confused body", "curved spine", "face blindness", "parrot chatter"
                ],
                "prismatic mind": [
                    "comet spirit", "burning light", "jumbled noise", "disrupted senses", "confused body",
                    "jumbled mind", "counting fog", "spirited heart", "puzzled heart", "face blindness",
                    "parrot chatter", "selective mutism", "thought blind"
                ],
                "obsessive mind": [
                    "spirited heart"
                ],
                "weighted heart": [
                    "shattered soul", "budding spirit"
                ],
                "comet spirit": [
                    "prismatic mind", "burning light", "jumbled noise", "disrupted senses", "confused body",
                    "jumbled mind", "counting fog", "spirited heart", "parrot chatter"
                ],
                "antisocial": [
                    "shattered soul", "budding spirit", "puzzled heart"
                ],
                "anxiety": [
                    "shattered soul", "budding spirit", "selective mutism"
                ],
                "constant roaming pain": [
                    "jellyfish joints", "loose body", "curved spine"
                ],
                "thunderous spirit": [
                    "shattered soul", "budding spirit", "spirited heart", "puzzled heart"
                ],
                "otherworldly mind": [
                    "shattered soul", "budding spirit"
                ],
                "irritable bowels": [
                    "jellyfish joints", "loose body"
                ],
                "jellyfish joints": [
                    "constant roaming pain", "irritable bowels", "loose body"
                ],
                "loose body": [
                    "constant roaming pain", "irritable bowels", "jellyfish joints"
                ],
                "burning light": [
                    "prismatic mind", "comet spirit", "jumbled noise", "disrupted senses"
                ],
                "jumbled noise": [
                    "prismatic mind", "comet spirit", "burning light", "disrupted senses"
                ],
                "disrupted senses": [
                    "prismatic mind", "comet spirit", "burning light", "jumbled noise"
                ],
                "confused body": [
                    "seizure prone", "prismatic mind", "comet spirit", "parrot chatter"
                ],
                "shattered soul": [
                    "weighted heart", "antisocial", "anxiety", "thunderous spirit", "otherworldly mind"
                ],
                "budding spirit": [
                    "weighted heart", "antisocial", "anxiety", "thunderous spirit", "otherworldly mind"
                ],
                "testosterone deficiency": [
                    "infertile"
                ],
                "excess testosterone": [
                    "pcos", "infertile"
                ],
                "aneuploidy": [
                    "infertile"
                ],
                "mosaicism": [
                    "infertile"
                ],
                "chimerism": [
                    "infertile"
                ],
                "pcos": [
                    "infertile"
                ],
                "curved spine": [
                    "paralyzed", "constant joint pain", "seizure prone", "constant roaming pain"
                ],
                "jumbled mind": [
                    "prismatic mind", "comet spirit", "counting fog"
                ],
                "counting fog": [
                    "prismatic mind", "comet spirit", "jumbled mind"
                ],
                "spirited heart": [
                    "prismatic mind", "obsessive mind", "comet spirit", "thunderous spirit"
                ],
                "puzzled heart": [
                    "prismatic mind", "antisocial", "thunderous spirit"
                ],
                "face blindness": [
                    "seizure prone", "prismatic mind", "thought blind"
                ],
                "parrot chatter": [
                    "seizure prone", "prismatic mind", "comet spirit", "confused body"
                ],
                "selective mutism": [
                    "prismatic mind", "anxiety"
                ],
                "thought blind": [
                    "prismatic mind", "face blindness"
                ]
            }

        for condition in PERMANENT:
            possible = PERMANENT[condition]
            if possible["congenital"] in ("always", "sometimes"):
                possible_conditions.append(condition)

        if cat.gender == "male":
            possible_conditions.remove("pcos")

        while count <= max_conditions:
            if randint(1, multiple_condition_chance) == 1:
                conditions += 1
            count += 1

        while conditions > 1:
            for entry in comorbid_conditions:
                if entry in cat.permanent_condition:
                    possible_comorbidities.append(comorbid_conditions.get(entry))

            new_condition = choice(possible_conditions)
            if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                new_condition = choice(choice(possible_comorbidities))

            while new_condition in cat.permanent_condition:
                new_condition = choice(possible_conditions)
                if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                    new_condition = choice(choice(possible_comorbidities))

            if new_condition == "blind" and "failing eyesight" in cat.permanent_condition:
                while new_condition == "blind":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))
            if new_condition == "failing eyesight" and "blind" in cat.permanent_condition:
                while new_condition == "failing eyesight":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))

            if new_condition == "deaf" and "partial hearing loss" in cat.permanent_condition:
                while new_condition == "deaf":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))
            if new_condition == "partial hearing loss" and "deaf" in cat.permanent_condition:
                while new_condition == "partial hearing loss":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))

            if new_condition == "spirited heart" and "puzzled heart" in cat.permanent_condition:
                while new_condition == "spirited heart":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))
            if new_condition == "puzzled heart" and "spirited heart" in cat.permanent_condition:
                while new_condition == "puzzled heart":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))

            if new_condition == "fractured spirit" and "budding spirit" in cat.permanent_condition:
                while new_condition == "fractured spirit":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))
            if new_condition == "fractured spirit" and "shattered soul" in cat.permanent_condition:
                while new_condition == "fractured spirit":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))

            if new_condition == "shattered soul" and "fractured spirit" in cat.permanent_condition:
                while new_condition == "shattered soul":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))
                            
            if new_condition == "budding spirit" and "fractured spirit" in cat.permanent_condition:
                while new_condition == "budding spirit":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))

            if new_condition == "mute" and "selective mutism" in cat.permanent_condition:
                while new_condition == "mute":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))
            if new_condition == "selective mutism" and "mute" in cat.permanent_condition:
                while new_condition == "selective mutism":
                    new_condition = choice(possible_conditions)
                    while new_condition in cat.permanent_condition:
                        new_condition = choice(possible_conditions)
                        if randint(1, comorbidity_chance) == 1 and possible_comorbidities:
                            new_condition = choice(choice(possible_comorbidities))

            if new_condition == "born without a leg":
                cat.pelt.scars.append("NOPAW")
            elif new_condition == "born without a tail":
                cat.pelt.scars.append("NOTAIL")
            elif new_condition == "lazy eye":
                cat.pelt.lazy_eye = cat.pelt.eye_colour
                if not cat.pelt.eye_colour2:
                    cat.pelt.lazy_eye = cat.pelt.eye_colour2

            self.get_permanent_condition(new_condition, born_with=True)
            conditions -= 1
            possible_comorbidities = []  # Reset possible_comorbidities so that the chances stay equal for each comorbidity

    def update_alters(self):
        if self.alters:
            for alter in self.alters:
                if "origin" not in alter:
                    alter["origin"] = "core"
                    alter["splits"] = []
                if "personality" not in alter:
                    alter["personality"] = choice(self.all_adult_personalities)

    def get_permanent_condition(self, name, born_with=False, event_triggered=False, starting_moon=0):
        if self.dead:
            return

        eating_disorders = ["anorexia", "ARFID", "bulimia", "binge-eating disorder", "food hoarding", "pica"]
        self_harm = ["harmful stims"]
        dissociation = ["derealization", "depersonalization", "amnesia"]
        psychosis = ["delusions", "psychotic episode", "hostile hallucinations", "paranoia", "ongoing psychosis"]
        night_dirtmaking_n_nest_wetting = ["night dirtmaking", "nest wetting"]
        all_triggers = eating_disorders + self_harm + dissociation + psychosis + night_dirtmaking_n_nest_wetting
        if not game_setting_get("allow_triggers") and name in all_triggers:
            return
        else:
            if not game_setting_get("eating_disorders") and name in eating_disorders:
                return
            if not game_setting_get("self_harm") and name in self_harm:
                return
            if not game_setting_get("dissociation") and name in dissociation:
                return
            if not game_setting_get("psychosis") and name in psychosis:
                return
            if not game_setting_get("intrusive_thoughts_TWO_woaw") and name in night_dirtmaking_n_nest_wetting:
                return
            if name in all_triggers:
                print("triggering condition: " + name)

        if name not in PERMANENT:
            print(
                self.name,
                f"WARNING: {name} is not in the permanent conditions collection.",
            )
            return

        if "blind" in self.permanent_condition and name == "failing eyesight":
            return
        if "deaf" in self.permanent_condition and name == "partial hearing loss":
            return

        if constants.CONFIG["event_generation"]["max_perm_conditions"] > 2:
            if len(self.permanent_condition) >= constants.CONFIG["event_generation"]["max_perm_conditions"]:
                return

        # remove accessories if need be
        if "NOTAIL" in self.pelt.scars or "HALFTAIL" in self.pelt.scars:
            self.pelt.accessory = [
                acc
                for acc in self.pelt.accessory
                if acc
                not in (
                    "RED FEATHERS",
                    "BLUE FEATHERS",
                    "JAY FEATHERS",
                    "GULL FEATHERS",
                    "SPARROW FEATHERS",
                    "CLOVERTAIL",
                    "DAISYTAIL",
                    'SEAWEED',
                    'DAISY CORSAGE',
                    "SNAKE",
                    "OLD SILVER WATCH",
                    "OLD GOLD WATCH",
                    "BAUBLES",
                    "SEAWEED",
                    "WISTERIA2",
                    "ROSE MALLOW",
                    "PICKLEWEED",
                    "GOLDEN CREEPING JENNY",
                )
            ]

        intersex_exclusive = ["excess testosterone", "aneuploidy", "testosterone deficiency", "chimerism", "mosaicism"]
        if self.gender != "intersex":
            if name in intersex_exclusive:
                return
        if name in intersex_exclusive and self.gender != "intersex":
            return

        if name == "failing eyesight" and "blind" in self.permanent_condition:
            return

        if name == "partial hearing loss" and "deaf" in self.permanent_condition:
            return

        plural_conditions = ["shattered soul", "budding spirit", "fractured spirit"]
        
        if self.is_plural() and name in plural_conditions:
            return

        if name == "spirited heart" and "puzzled heart" in self.permanent_condition:
            return
        if name == "puzzled heart" and "spirited heart" in self.permanent_condition:
            return

        if name == "mute" and "selective mutism" in self.permanent_condition:
            return
        if name == "selective mutism" and "mute" in self.permanent_condition:
            return
        
        misdiagnosis = False
        try:
            with open("resources/dicts/conditions/misdiagnoses.json", 'r', encoding="utf-8") as read_file:
                misdiagnoses = ujson.loads(read_file.read())
        except Exception as e:
            print(
                f"WARNING: There was an error reading the misdiagnoses file.\n",
                e,
            )
        if game_setting_get("allow_triggers"):
            # check for trigger toggle
            if game_setting_get("misdiagnosis"):
                # check for misdiagnosis
                exp_bonus = 0
                meds = find_alive_cats_with_rank(Cat, [CatRank.MEDICINE_CAT, CatRank.MEDICINE_APPRENTICE], sort=True)
                if len(meds) > 0:
                    for med in meds:
                        if med._experience > 75:
                            exp_bonus += 3
                        elif med._experience > 50:
                            exp_bonus += 1
                        elif med._experience > 25:
                            exp_bonus -= 1
                        else:
                            exp_bonus -= 3
                else:
                    exp_bonus -= 5
                misdiagnosis_chance = randint(0, 10) + exp_bonus
                if misdiagnosis_chance < 5:
                    # print("Misdiagnosis alert!")
                    if name in misdiagnoses:
                        misdiagnosis = choice(misdiagnoses[name])
                        print(name + " misdiagnosed as: " + misdiagnosis)
                        if misdiagnosis in self.permanent_condition:
                            misdiagnosis = False
                            # print ("False alarm.")
                    # else:
                        # print ("no possible misdiagnoses...it's your med cat's lucky break!")

        condition = PERMANENT[name]
        new_condition = False
        mortality = condition["mortality"][self.age.value]
        if mortality != 0 and (game.clan and game.clan.game_mode == "cruel season"):
            mortality = int(mortality * 0.65)

        if condition["congenital"] == "always":
            born_with = True
        moons_until = condition["moons_until"]
        if born_with and moons_until != 0:
            if name == "budding spirit":
                moons_until = randint(moons_until - 1, moons_until + 12)
            if name == "shattered soul":
                moons_until = randint(moons_until - 1, moons_until + 12)
            if name == "prismatic mind":
                moons_until = randint(moons_until - 1, moons_until + 10)
            if name == "comet spirit":
                moons_until = randint(moons_until - 1, moons_until + 10)
            if name == "loose body":
                moons_until = randint(moons_until - 1, moons_until + 6)
            if name == "jellyfish joints":
                moons_until = randint(moons_until - 1, moons_until + 6)
            if name == "constant joint pain":
                moons_until = randint(moons_until - 1, moons_until + 5)
            if name == "body biter":
                moons_until = randint(moons_until - 1, moons_until + 4)
            if name == "thunderous spirit":
                moons_until = randint(moons_until - 1, moons_until + 4)
            if name == "otherworldly mind":
                moons_until = randint(moons_until - 1, moons_until + 4)
            if name == "jumbled noise":
                moons_until = randint(moons_until - 1, moons_until + 4)
            if name == "obsessive mind":
                moons_until = randint(moons_until - 1, moons_until + 3)
            if name == "falling paws":
                moons_until = randint(moons_until - 1, moons_until + 3)
            if name == "weighted heart":
                moons_until = randint(moons_until - 1, moons_until + 2)
            if name == "anxiety":
                moons_until = randint(moons_until - 1, moons_until + 2)
            if name == "snow vision":
                moons_until = randint(moons_until - 1, moons_until + 2)
            else:
                moons_until = randint(
                    moons_until - 1, moons_until + 1
                )  # creating a range in which a condition can present
            if moons_until < 0:
                moons_until = 0

        if born_with and not self.status.rank.is_baby():
            moons_until = -2
        elif born_with is False:
            moons_until = 0

        if name == "paralyzed":
            self.pelt.paralyzed = True
            
        if condition["risks"] is not None:
            for risk in condition["risks"]:
                risk["chance"] = randint(int(risk["chance"] / 2), int(risk["chance"] * 2))

        new_perm_condition = PermanentCondition(
            name=name,
            severity=condition["severity"],
            congenital=condition["congenital"],
            moons_until=moons_until,
            moon_start=starting_moon,
            mortality=mortality,
            risks=condition["risks"],
            illness_infectiousness=condition["illness_infectiousness"],
            event_triggered=event_triggered,
            misdiagnosis=misdiagnosis
        )

        if new_perm_condition.name not in self.permanent_condition:
            self.permanent_condition[new_perm_condition.name] = {
                "severity": new_perm_condition.severity,
                "born_with": born_with,
                "moons_until": new_perm_condition.moons_until,
                "moon_start": game.clan.age if game.clan else 0,
                "mortality": new_perm_condition.current_mortality,
                "illness_infectiousness": new_perm_condition.illness_infectiousness,
                "risks": new_perm_condition.risks,
                "complication": None,
                "event_triggered": new_perm_condition.new,
                "misdiagnosis": new_perm_condition.misdiagnosis
            }
            
            if self.is_plural():
                if len(self.alters) < 1:
                    self.system_core()
                    self.new_alter(new_perm_condition.name)
                    
            new_condition = True
        return new_condition

    def not_working(self):
        """returns True if the cat cannot work, False if the cat can work"""
        for illness in self.illnesses:
            if self.illnesses[illness]["severity"] != "minor":
                return True
        return any(
            self.injuries[injury]["severity"] != "minor" for injury in self.injuries
        )

    def not_work_because_hunger(self):
        """returns True if the only condition, why the cat cannot work is because of starvation"""
        non_minor_injuries = [
            injury
            for injury in self.injuries
            if self.injuries[injury]["severity"] != "minor"
        ]
        if len(non_minor_injuries) > 0:
            return False
        non_minor_illnesses = [
            illness
            for illness in self.illnesses
            if self.illnesses[illness]["severity"] != "minor"
        ]
        return "starving" in non_minor_illnesses and len(non_minor_illnesses) == 1

    def retire_cat(self):
        """This is only for cats that retire due to health condition"""

        # There are some special tasks we need to do for apprentice
        # Note that although you can un-retire cats, they will be a full warrior/med_cat/mediator
        if self.moons > 6 and self.status.rank.is_any_apprentice_rank():
            _ment = Cat.fetch_cat(self.mentor) if self.mentor else None
            self.rank_change(
                CatRank.WARRIOR
            )  # Temp switch them to warrior, so the following step will work
            self.rank_change_traits_skill(_ment)

        self.rank_change(CatRank.ELDER)
        return

    def is_ill(self):
        """Returns true if the cat is ill."""
        return len(self.illnesses) > 0

    def is_injured(self):
        """Returns true if the cat is injured."""
        return len(self.injuries) > 0
    
    def is_awakened(self):
        awakened = False
        if self.awakened:
            awakened = True
        return awakened

    def is_disabled(self):
        """Returns true if the cat have permanent condition"""
        return len(self.permanent_condition) > 0

    def available_to_work(self):
        return self.status.alive_in_player_clan and not self.not_working()

    def contact_with_ill_cat(self, cat: Cat):
        """handles if one cat had contact with an ill cat"""

        current_denkeepers = find_alive_cats_with_rank(Cat, [CatRank.DENKEEPER, CatRank.DENKEEPER_APPRENTICE])

        infectious_illnesses = []
        if self.is_ill() or cat is None or not cat.is_ill():
            return
        elif cat.is_ill():
            for illness in cat.illnesses:
                if cat.illnesses[illness]["infectiousness"] != 0:
                    infectious_illnesses.append(illness)
            if len(infectious_illnesses) == 0:
                return

        for illness in infectious_illnesses:
            illness_name = illness
            rate = cat.illnesses[illness]["infectiousness"]
            if self.is_injured():
                for y in self.injuries:
                    illness_infect = list(
                        filter(
                            lambda ill: ill["name"] == illness_name,
                            self.injuries[y]["illness_infectiousness"],
                        )
                    )
                    if illness_infect is not None and len(illness_infect) > 0:
                        illness_infect = illness_infect[0]
                        rate -= illness_infect["lower_by"]

                    # prevent rate lower 0 and print warning message
                    if rate < 0:
                        print(
                            f"WARNING: injury {self.injuries[y]['name']} has lowered \
                            chance of {illness_name} infection to {rate}"
                        )
                        rate = 1
            
            if len(current_denkeepers) > 0:
                for keeper in current_denkeepers:
                    rate = int(rate * 1.5)

            if not random() * rate:
                text = f"{self.name} had contact with {cat.name} and now has {illness_name}."
                # game.health_events_list.append(text)
                game.cur_events_list.append(
                    Single_Event(text, "health", cat_dict={"m_c": self})
                )
                self.get_ill(illness_name)
    
    def is_plural(self):
        is_plural = False
        if "budding spirit" in self.permanent_condition or "shattered soul" in self.permanent_condition or "fractured spirit" in self.permanent_condition:
            is_plural = True
        return is_plural

    def save_condition(self):
        # save conditions for each cat
        clanname = None
        if switch_get_value(Switch.clan_name) != "":
            clanname = switch_get_value(Switch.clan_name)
        elif len(switch_get_value(Switch.clan_list)) > 0:
            clanname = switch_get_value(Switch.clan_list)[0]
        elif game.clan is not None:
            clanname = game.clan.name

        condition_directory = get_save_dir() + "/" + clanname + "/conditions"
        condition_file_path = condition_directory + "/" + self.ID + "_conditions.json"

        if (
            (not self.is_ill() and not self.is_injured() and not self.is_disabled() and not self.is_awakened())
        ):
            if os.path.exists(condition_file_path):
                os.remove(condition_file_path)
            return

        conditions = {}

        if self.is_ill():
            conditions["illnesses"] = self.illnesses

        if self.is_injured():
            conditions["injuries"] = self.injuries

        if self.is_disabled():
            conditions["permanent conditions"] = self.permanent_condition

        if self.is_plural():
            self.update_alters()
            conditions["alters"] = self.alters
            
        if self.is_awakened():
            conditions["awakened"] = self.awakened

        safe_save(condition_file_path, conditions)

    def load_conditions(self):
        if switch_get_value(Switch.clan_name) != "":
            clanname = switch_get_value(Switch.clan_name)
        else:
            clanname = switch_get_value(Switch.clan_list)[0]

        condition_directory = get_save_dir() + "/" + clanname + "/conditions/"
        condition_cat_directory = condition_directory + self.ID + "_conditions.json"
        if not os.path.exists(condition_cat_directory):
            return

        try:
            with open(condition_cat_directory, "r", encoding="utf-8") as read_file:
                rel_data = ujson.loads(read_file.read())
                self.illnesses = rel_data.get("illnesses", {})
                self.injuries = rel_data.get("injuries", {})
                self.permanent_condition = rel_data.get("permanent conditions", {})
                for con in self.permanent_condition:
                    if "misdiagnosis" not in con:
                        self.permanent_condition[con]["misdiagnosis"] = False
                if self.is_plural():
                    self.alters = rel_data["alters"]
                    self.update_alters()
                if "awakened" in rel_data:
                    if rel_data["awakened"]["type"] in ["esper", "guide", "enhanced esper"]:
                        self.awakened = rel_data["awakened"]

            if "paralyzed" in self.permanent_condition and not self.pelt.paralyzed:
                self.pelt.paralyzed = True
            if "stimming" in self.illnesses and not self.pelt.blep:
                self.pelt.blep = True
            else:
                self.pelt.blep = False

            if "starwalker" in self.permanent_condition:
                del self.permanent_condition["starwalker"]
                self.get_permanent_condition("prismatic mind", born_with=True)

        except Exception as e:
            print(
                f"WARNING: There was an error reading the condition file of cat #{self}.\n",
                e,
            )

    # ---------------------------------------------------------------------------- #
    #                                    mentor                                    #
    # ---------------------------------------------------------------------------- #

    def is_valid_mentor(self, potential_mentor: Cat):
        # If not an app, don't need a mentor
        if not self.status.rank.is_any_apprentice_rank():
            return False

        # App and mentor must be members of the same clan
        if self.status.group != potential_mentor.status.group:
            return False

        # Match jobs
        if (
            self.status.rank == CatRank.MEDICINE_APPRENTICE
            and potential_mentor.status.rank != CatRank.MEDICINE_CAT
        ):
            return False
        if (
            self.status.rank == CatRank.APPRENTICE
            and potential_mentor.status.rank
            not in [CatRank.LEADER, CatRank.DEPUTY, CatRank.WARRIOR]
        ):
            return False
        if (
            self.status.rank == CatRank.MEDIATOR_APPRENTICE
            and potential_mentor.status.rank != CatRank.MEDIATOR
        ):
            return False
        if (
            self.status.rank == CatRank.CARETAKER_APPRENTICE
            and potential_mentor.status.rank != CatRank.CARETAKER
        ):
            return False
        if (
            self.status.rank == CatRank.DENKEEPER_APPRENTICE
            and potential_mentor.status.rank != CatRank.DENKEEPER
        ):
            return False
        if (
            self.status.rank == CatRank.GARDENER_APPRENTICE
            and potential_mentor.status.rank != CatRank.GARDENER
        ):
            return False
        if (
            self.status.rank == CatRank.MESSENGER_APPRENTICE
            and potential_mentor.status.rank != CatRank.MESSENGER
        ):
            return False
        if (
            self.status.rank == CatRank.STORYTELLER_APPRENTICE
            and potential_mentor.status.rank != CatRank.STORYTELLER
        ):
            return False

        return True

    def __remove_mentor(self):
        """Should only be called by update_mentor, also sets fields on mentor."""
        if not self.mentor:
            return
        mentor_cat = Cat.fetch_cat(self.mentor)
        if not mentor_cat:
            return
        if self.ID in mentor_cat.apprentice:
            mentor_cat.apprentice.remove(self.ID)
        if self.moons > 6:
            if self.ID not in mentor_cat.former_apprentices:
                mentor_cat.former_apprentices.append(self.ID)
            if mentor_cat.ID not in self.former_mentor:
                self.former_mentor.append(mentor_cat.ID)
        self.mentor = None

    def __add_mentor(self, new_mentor_id: str):
        """Should only be called by update_mentor, also sets fields on mentor."""
        # reset patrol number
        self.patrol_with_mentor = 0
        self.mentor = new_mentor_id
        mentor_cat = Cat.fetch_cat(self.mentor)
        if not mentor_cat:
            return
        if self.ID not in mentor_cat.apprentice:
            mentor_cat.apprentice.append(self.ID)

    def update_mentor(self, new_mentor: Any = None):
        """Takes mentor's ID as argument, mentor could just be set via this function."""
        # No !!
        if isinstance(new_mentor, Cat):
            print("Everything is terrible!! (new_mentor {new_mentor} is a Cat D:)")
            return

        # Check if cat can have a mentor
        if (
            self.dead
            or self.status.is_outsider
            or not self.status.rank.is_any_apprentice_rank()
        ):
            self.__remove_mentor()
            return

        # If eligible, cat should get a mentor.
        if new_mentor:
            self.__remove_mentor()
            self.__add_mentor(new_mentor)

        # Check if current mentor is valid
        if self.mentor:
            mentor_cat = Cat.fetch_cat(
                self.mentor
            )  # This will return None if there is no current mentor
            if mentor_cat and not self.is_valid_mentor(mentor_cat):
                self.__remove_mentor()

        # Need to pick a random mentor if not specified
        if not self.mentor:
            potential_mentors = []
            priority_mentors = []
            for cat in self.all_cats.values():
                if self.is_valid_mentor(cat):
                    potential_mentors.append(cat)
                    if not cat.apprentice and not cat.not_working():
                        priority_mentors.append(cat)
            # First try for a cat who currently has no apprentices and is working
            if priority_mentors:  # length of list > 0
                new_mentor = choice(priority_mentors)
            elif potential_mentors:  # length of list > 0
                new_mentor = choice(potential_mentors)
            if new_mentor:
                self.__add_mentor(new_mentor.ID)

    # ---------------------------------------------------------------------------- #
    #                                 relationships                                #
    # ---------------------------------------------------------------------------- #
    def is_potential_mate(
        self,
        other_cat: Cat,
        for_love_interest: bool = False,
        age_restriction: bool = True,
        first_cousin_mates: bool = False,
        ignore_no_mates: bool = False,
    ):
        """
        Checks if this cat is potential mate for the other cat.
        There are no restrictions if the current cat already has a mate or not (this allows poly-mates).
        """

        try:
            first_cousin_mates = get_clan_setting("first cousin mates")
        except:
            if "unittest" not in sys.modules:
                raise

        # just to be sure, check if it is not the same cat
        if self.ID == other_cat.ID:
            return False

        # No Mates Check
        if not ignore_no_mates and (self.no_mates or other_cat.no_mates):
            return False

        # Inheritance check
        if self.is_related(other_cat, first_cousin_mates):
            return False

        # check dead cats
        if self.dead != other_cat.dead:
            return False

        # check that outside status is the same
        if self.status.is_outsider != other_cat.status.is_outsider:
            return False

        # check for age
        if age_restriction:
            if (self.moons < 14 or other_cat.moons < 14) and not for_love_interest:
                return False

            # the +1 is necessary because both might not already be aged up
            # if only one is aged up at this point, later they are more moons apart than the setting defined
            # constants.CONFIG boolean "override_same_age_group" disables the same-age group check.
            if (
                constants.CONFIG["mates"].get("override_same_age_group", False)
                or self.age != other_cat.age
            ) and (
                abs(self.moons - other_cat.moons)
                > constants.CONFIG["mates"]["age_range"] + 1
            ):
                return False

        if (
            not self.age.can_have_mate() or not other_cat.age.can_have_mate()
        ) and self.age != other_cat.age:
            return False

        # check for mentor

        # Current mentor
        if other_cat.ID in self.apprentice or self.ID in other_cat.apprentice:
            return False
        
        # Current bestie
        if other_cat.ID in self.bestie or self.ID in other_cat.bestie:
            return False
        
        if other_cat.ID in self.enemy or self.ID in other_cat.enemy:
            return False

        # Former mentor
        is_former_mentor = (
            other_cat.ID in self.former_apprentices
            or self.ID in other_cat.former_apprentices
        )
        return bool(
            not is_former_mentor or get_clan_setting("romantic with former mentor")
        )
    
    def is_potential_bestie(
        self,
        other_cat: Cat
    ):
        """
        Checks if this cat is potential mate for the other cat.
        There are no restrictions if the current cat already has a mate or not (this allows poly-mates).
        """

        # just to be sure, check if it is not the same cat
        if self.ID == other_cat.ID:
            return False
        
        if other_cat.ID in self.enemy or self.ID in other_cat.enemy:
            return False

        # check dead cats
        if self.dead != other_cat.dead:
            return False
        
        return True
    
    def is_potential_enemy(
        self,
        other_cat: Cat
    ):
        """
        Checks if this cat is potential mate for the other cat.
        There are no restrictions if the current cat already has a mate or not (this allows poly-mates).
        """

        # just to be sure, check if it is not the same cat
        if self.ID == other_cat.ID:
            return False

        # check dead cats
        if self.dead != other_cat.dead:
            return False
        
        # can't be friends and enemies
        if other_cat.ID in self.bestie or self.ID in other_cat.bestie:
            return False
        
        # cant be mates and enemies
        if other_cat.ID in self.mate or self.ID in other_cat.mate:
            return False

        return True

    def unset_mate(self, other_cat: Cat, breakup: bool = False, fight: bool = False):
        """Unset the mate from both self and other_cat"""
        if not other_cat:
            return

        # Both cats must have mates for this to work
        if len(self.mate) < 1 or len(other_cat.mate) < 1:
            return

        # AND they must be mates with each other.
        if self.ID not in other_cat.mate or other_cat.ID not in self.mate:
            print(
                f"Unsetting mates: These {self.name} and {other_cat.name} are not mates!"
            )
            return

        # If only deal with relationships if this is a breakup.
        if breakup:
            self_relationship = None
            if not self.dead:
                if other_cat.ID not in self.relationships:
                    self.create_one_relationship(other_cat)
                    self.relationships[other_cat.ID].mates = True
                self_relationship = self.relationships[other_cat.ID]
                self_relationship.romantic_love -= randint(20, 60)
                self_relationship.comfortable -= randint(10, 30)
                self_relationship.trust -= randint(5, 15)
                self_relationship.mates = False
                if fight:
                    self_relationship.romantic_love -= randint(10, 30)
                    self_relationship.platonic_like -= randint(15, 45)

            if not other_cat.dead:
                if self.ID not in other_cat.relationships:
                    other_cat.create_one_relationship(self)
                    other_cat.relationships[self.ID].mates = True
                other_relationship = other_cat.relationships[self.ID]
                other_relationship.romantic_love -= 40
                other_relationship.comfortable -= 20
                other_relationship.trust -= 10
                other_relationship.mates = False
                if fight:
                    self_relationship.romantic_love -= 20
                    other_relationship.platonic_like -= 30

        self.mate.remove(other_cat.ID)
        other_cat.mate.remove(self.ID)

        # Handle previous mates:
        if other_cat.ID not in self.previous_mates:
            self.previous_mates.append(other_cat.ID)
        if self.ID not in other_cat.previous_mates:
            other_cat.previous_mates.append(self.ID)

        if other_cat.inheritance:
            other_cat.inheritance.update_all_mates()
        if self.inheritance:
            self.inheritance.update_all_mates()
    
    def unset_bestie(self, other_cat: Cat, breakup: bool = False, fight: bool = False):
        """Unset the mate from both self and other_cat"""
        if not other_cat:
            return

        # Both cats must have mates for this to work
        if len(self.bestie) < 1 or len(other_cat.bestie) < 1:
            return

        # AND they must be mates with each other.
        if self.ID not in other_cat.bestie or other_cat.ID not in self.bestie:
            print(
                f"Unsetting besties: These {self.name} and {other_cat.name} are not besties!"
            )
            return

        # If only deal with relationships if this is a breakup.
        if breakup:
            self_relationship = None
            if not self.dead:
                if other_cat.ID not in self.relationships:
                    self.create_one_relationship(other_cat)
                    self.relationships[other_cat.ID].besties = True
                self_relationship = self.relationships[other_cat.ID]
                self_relationship.romantic_love -= randint(20, 60)
                self_relationship.comfortable -= randint(10, 30)
                self_relationship.trust -= randint(5, 15)
                self_relationship.besties = False
                if fight:
                    self_relationship.romantic_love -= randint(10, 30)
                    self_relationship.platonic_like -= randint(15, 45)

            if not other_cat.dead:
                if self.ID not in other_cat.relationships:
                    other_cat.create_one_relationship(self)
                    other_cat.relationships[self.ID].besties = True
                other_relationship = other_cat.relationships[self.ID]
                other_relationship.romantic_love -= 40
                other_relationship.comfortable -= 20
                other_relationship.trust -= 10
                other_relationship.besties = False
                if fight:
                    self_relationship.romantic_love -= 20
                    other_relationship.platonic_like -= 30

        self.bestie.remove(other_cat.ID)
        other_cat.bestie.remove(self.ID)

        # Handle previous mates:
        if other_cat.ID not in self.previous_besties:
            self.previous_besties.append(other_cat.ID)
        if self.ID not in other_cat.previous_besties:
            other_cat.previous_besties.append(self.ID)

    def unset_enemy(self, other_cat: Cat, breakup: bool = False, fight: bool = False):
        """Unset the mate from both self and other_cat"""
        if not other_cat:
            return

        # Both cats must have mates for this to work
        if len(self.enemy) < 1 or len(other_cat.enemy) < 1:
            return

        # AND they must be mates with each other.
        if self.ID not in other_cat.enemy or other_cat.ID not in self.enemy:
            print(
                f"Unsetting mates: These {self.name} and {other_cat.name} are not enemies!"
            )
            return

        # If only deal with relationships if this is a breakup.
        if breakup:
            self_relationship = None
            if not self.dead:
                if other_cat.ID not in self.relationships:
                    self.create_one_relationship(other_cat)
                    self.relationships[other_cat.ID].enemies = True
                self_relationship = self.relationships[other_cat.ID]
                self_relationship.dislike -= randint(20, 60)
                self_relationship.jealousy -= randint(10, 30)
                self_relationship.like += randint(5, 15)
                self_relationship.enemies = False
                if fight:
                    self_relationship.romantic_love -= randint(10, 30)
                    self_relationship.platonic_like -= randint(15, 45)

            if not other_cat.dead:
                if self.ID not in other_cat.relationships:
                    other_cat.create_one_relationship(self)
                    other_cat.relationships[self.ID].enemies = True
                other_relationship = other_cat.relationships[self.ID]
                other_relationship.dislike -= 40
                other_relationship.jealousy -= 20
                other_relationship.like += 10
                other_relationship.enemies = False
                if fight:
                    self_relationship.romantic_love -= 20
                    other_relationship.platonic_like -= 30

        self.enemy.remove(other_cat.ID)
        other_cat.enemy.remove(self.ID)

        # Handle previous mates:
        if other_cat.ID not in self.previous_enemies:
            self.previous_enemies.append(other_cat.ID)
        if self.ID not in other_cat.previous_enemies:
            other_cat.previous_enemies.append(self.ID)

    def set_mate(self, other_cat: Cat):
        """Sets up a mate relationship between self and other_cat."""
        if other_cat.ID not in self.mate:
            self.mate.append(other_cat.ID)
        if self.ID not in other_cat.mate:
            other_cat.mate.append(self.ID)

        # If the current mate was in the previous mate list, remove them.
        if other_cat.ID in self.previous_mates:
            self.previous_mates.remove(other_cat.ID)
        if self.ID in other_cat.previous_mates:
            other_cat.previous_mates.remove(self.ID)

        if other_cat.inheritance:
            other_cat.inheritance.update_all_mates()
        if self.inheritance:
            self.inheritance.update_all_mates()

        # Set starting relationship values
        if not self.dead:
            if other_cat.ID not in self.relationships:
                self.create_one_relationship(other_cat)
                self.relationships[other_cat.ID].mates = True
            self_relationship = self.relationships[other_cat.ID]
            self_relationship.romantic_love += 20
            self_relationship.comfortable += 20
            self_relationship.trust += 10
            self_relationship.mates = True

        if not other_cat.dead:
            if self.ID not in other_cat.relationships:
                other_cat.create_one_relationship(self)
                other_cat.relationships[self.ID].mates = True
            other_relationship = other_cat.relationships[self.ID]
            other_relationship.romantic_love += 20
            other_relationship.comfortable += 20
            other_relationship.trust += 10
            other_relationship.mates = True
    
    def set_bestie(self, other_cat: Cat):
        """Sets up a best friend relationship between self and other_cat."""
        if other_cat.ID not in self.bestie:
            self.bestie.append(other_cat.ID)
        if self.ID not in other_cat.bestie:
            other_cat.bestie.append(self.ID)
        
        # If the current bestie was in the previous mate list, remove them.
        if other_cat.ID in self.previous_besties:
            self.previous_besties.remove(other_cat.ID)
        if self.ID in other_cat.previous_besties:
            other_cat.previous_besties.remove(self.ID)
        
        # Set starting relationship values
        if not self.dead:
            if other_cat.ID not in self.relationships:
                self.create_one_relationship(other_cat)
            self_relationship = self.relationships[other_cat.ID]
            self_relationship.platonic_like += 20
            self_relationship.comfortable += 20
            self_relationship.trust += 10
            self_relationship.besties = True

        if not other_cat.dead:
            if self.ID not in other_cat.relationships:
                other_cat.create_one_relationship(self)
            other_relationship = other_cat.relationships[self.ID]
            other_relationship.platonic_like += 20
            other_relationship.comfortable += 20
            other_relationship.trust += 10
            other_relationship.besties = True
            
    def set_enemy(self, other_cat: Cat):
        """Sets up a sworn enemy relationship between self and other_cat."""
        if other_cat.ID not in self.enemy:
            self.enemy.append(other_cat.ID)
        if self.ID not in other_cat.enemy:
            other_cat.enemy.append(self.ID)
        
        # If the current bestie was in the previous mate list, remove them.
        if other_cat.ID in self.previous_enemies:
            self.previous_enemies.remove(other_cat.ID)
        if self.ID in other_cat.previous_enemies:
            other_cat.previous_enemies.remove(self.ID)
        
        # Set starting relationship values
        if not self.dead:
            if other_cat.ID not in self.relationships:
                self.create_one_relationship(other_cat)
            self_relationship = self.relationships[other_cat.ID]
            self_relationship.platonic_like -= 20
            self_relationship.comfortable -= 20
            self_relationship.trust -= 10
            self_relationship.jealousy += 10
            self_relationship.dislike += 20
            self_relationship.enemies = True

        if not other_cat.dead:
            if self.ID not in other_cat.relationships:
                other_cat.create_one_relationship(self)
            other_relationship = other_cat.relationships[self.ID]
            other_relationship.platonic_like -= 20
            other_relationship.comfortable -= 20
            other_relationship.trust -= 10
            other_relationship.jealousy += 10
            other_relationship.dislike += 20
            other_relationship.enemies = True
            
    def unset_adoptive_parent(self, other_cat: Cat):
        """Unset the adoptive parent from self"""
        self.adoptive_parents.remove(other_cat.ID)
        self.create_inheritance_new_cat()
        other_cat.create_inheritance_new_cat()
        if not self.dead:
            if other_cat.ID not in self.relationships:
                self.create_one_relationship(other_cat)
            self_relationship = self.relationships[other_cat.ID]
            self_relationship.platonic_like -= randint(10, 30)
            self_relationship.comfortable -= randint(10, 30)
            self_relationship.trust -= randint(5, 15)

        if not other_cat.dead:
            if self.ID not in other_cat.relationships:
                other_cat.create_one_relationship(self)
            other_relationship = other_cat.relationships[self.ID]
            other_relationship.platonic_like -= 20
            other_relationship.comfortable -= 20
            other_relationship.trust -= 10

    def set_adoptive_parent(self, other_cat: Cat):
        """Sets up a parent-child relationship between self and other_cat."""
        self.adoptive_parents.append(other_cat.ID)
        self.create_inheritance_new_cat()

        # Set starting relationship values
        if not self.dead:
            if other_cat.ID not in self.relationships:
                self.create_one_relationship(other_cat)
            self_relationship = self.relationships[other_cat.ID]
            self_relationship.platonic_like += 20
            self_relationship.comfortable += 20
            self_relationship.trust += 10

        if not other_cat.dead:
            if self.ID not in other_cat.relationships:
                other_cat.create_one_relationship(self)
            other_relationship = other_cat.relationships[self.ID]
            other_relationship.platonic_like += 20
            other_relationship.comfortable += 20
            other_relationship.trust += 10

    def create_inheritance_new_cat(self):
        """Creates the inheritance class for a new cat."""
        # set the born status to true, just for safety
        self.inheritance = Inheritance(self, True)

    def create_one_relationship(self, other_cat: Cat):
        """Create a new relationship between current cat and other cat. Returns: Relationship"""
        if other_cat.ID in self.relationships:
            return self.relationships[other_cat.ID]

        if other_cat.ID == self.ID:
            print(
                f"Attempted to create a relationship with self: {self.name}. Please report as a bug!"
            )
            return None

        self.relationships[other_cat.ID] = Relationship(self, other_cat)
        return self.relationships[other_cat.ID]

    def create_relationships_new_cat(self):
        """Create relationships for a new generated cat."""
        for inter_cat in Cat.all_cats.values():
            # the inter_cat is the same as the current cat
            if inter_cat.ID == self.ID:
                continue
            # if the cat already has (somehow) a relationship with the inter cat
            if inter_cat.ID in self.relationships:
                continue
            # if they dead (dead cats have no relationships)
            if self.dead or inter_cat.dead:
                continue
            # if they are not outside of the Clan at the same time
            if self.status.group != inter_cat.status.group:
                continue
            inter_cat.relationships[self.ID] = Relationship(inter_cat, self)
            self.relationships[inter_cat.ID] = Relationship(self, inter_cat)

    def init_all_relationships(self):
        """Create Relationships to all current Clancats."""
        for ID in self.all_cats:
            the_cat = self.all_cats.get(ID)
            if the_cat.ID is not self.ID:
                mates = the_cat.ID in self.mate
                are_parents = False
                parents = False
                siblings = False

                if (
                    self.parent1 is not None
                    and self.parent2 is not None
                    and the_cat.parent1 is not None
                    and the_cat.parent2 is not None
                ):
                    are_parents = the_cat.ID in (self.parent1, self.parent2)
                    parents = are_parents or self.ID in (
                        the_cat.parent1,
                        the_cat.parent2,
                    )
                    siblings = self.parent1 in (
                        the_cat.parent1,
                        the_cat.parent2,
                    ) or self.parent2 in (the_cat.parent1, the_cat.parent2)

                related = parents or siblings

                # set the different stats
                romantic_love = 0
                like = 0
                dislike = 0
                admiration = 0
                comfortable = 0
                jealousy = 0
                trust = 0
                if game_setting_get("random relation"):
                    if (
                        game.clan
                        and the_cat == game.clan.instructor
                        and game.clan.instructor.dead_for >= self.moons
                    ):
                        pass
                    elif randint(1, 20) == 1 and romantic_love < 1:
                        dislike = randint(10, 25)
                        jealousy = randint(5, 15)
                        if randint(1, 30) == 1:
                            trust = randint(1, 10)
                    else:
                        like = randint(0, 35)
                        comfortable = randint(0, 25)
                        trust = randint(0, 15)
                        admiration = randint(0, 20)
                        if (
                            randint(1, 100 - like) == 1
                            and self.moons > 11
                            and the_cat.moons > 11
                            and self.age == the_cat.age
                        ):
                            romantic_love = randint(15, 30)
                            comfortable = int(comfortable * 1.3)
                            trust = int(trust * 1.2)

                if are_parents and like < 60:
                    like = 60
                if siblings and like < 30:
                    like = 30

                rel = Relationship(
                    cat_from=self,
                    cat_to=the_cat,
                    mates=mates,
                    family=related,
                    romantic_love=romantic_love,
                    platonic_like=like,
                    dislike=dislike,
                    admiration=admiration,
                    comfortable=comfortable,
                    jealousy=jealousy,
                    trust=trust,
                )
                self.relationships[the_cat.ID] = rel

    def save_relationship_of_cat(self, relationship_dir):
        # save relationships for each cat

        rel = []
        for r in self.relationships.values():
            r_data = {
                "cat_from_id": r.cat_from.ID,
                "cat_to_id": r.cat_to.ID,
                "mates": r.mates,
                "besties": r.besties,
                "enemies": r.enemies,
                "family": r.family,
                "romantic_love": r.romantic_love,
                "platonic_like": r.platonic_like,
                "dislike": r.dislike,
                "admiration": r.admiration,
                "comfortable": r.comfortable,
                "jealousy": r.jealousy,
                "trust": r.trust,
                "log": r.log,
            }
            rel.append(r_data)

        safe_save(f"{relationship_dir}/{self.ID}_relations.json", rel)

    def load_relationship_of_cat(self):
        if switch_get_value(Switch.clan_name) != "":
            clanname = switch_get_value(Switch.clan_name)
        else:
            clanname = switch_get_value(Switch.clan_list)[0]

        relation_directory = get_save_dir() + "/" + clanname + "/relationships/"
        relation_cat_directory = relation_directory + self.ID + "_relations.json"

        self.relationships = {}
        if os.path.exists(relation_directory):
            if not os.path.exists(relation_cat_directory):
                self.init_all_relationships()
                for cat in Cat.all_cats.values():
                    cat.create_one_relationship(self)
                return
            try:
                with open(relation_cat_directory, "r", encoding="utf-8") as read_file:
                    rel_data = ujson.loads(read_file.read())
                    for rel in rel_data:
                        cat_to = self.all_cats.get(rel["cat_to_id"])
                        if cat_to is None or rel["cat_to_id"] == self.ID:
                            continue
                        if "besties" in rel and "enemies" in rel:    
                            new_rel = Relationship(
                                cat_from=self,
                                cat_to=cat_to,
                                mates=rel["mates"] or False,
                                besties=rel["besties"] or False,
                                enemies=rel["enemies"] or False,
                                family=rel["family"] or False,
                                romantic_love=(rel["romantic_love"] or 0),
                                platonic_like=(rel["platonic_like"] or 0),
                                dislike=rel["dislike"] or 0,
                                admiration=rel["admiration"] or 0,
                                comfortable=rel["comfortable"] or 0,
                                jealousy=rel["jealousy"] or 0,
                                trust=rel["trust"] or 0,
                                log=rel["log"],
                            )
                        elif "besties" in rel:
                            new_rel = Relationship(
                                cat_from=self,
                                cat_to=cat_to,
                                mates=rel["mates"] or False,
                                besties=rel["besties"] or False,
                                enemies=False,
                                family=rel["family"] or False,
                                romantic_love=(rel["romantic_love"] or 0),
                                platonic_like=(rel["platonic_like"] or 0),
                                dislike=rel["dislike"] or 0,
                                admiration=rel["admiration"] or 0,
                                comfortable=rel["comfortable"] or 0,
                                jealousy=rel["jealousy"] or 0,
                                trust=rel["trust"] or 0,
                                log=rel["log"],
                            )
                            self.relationships[rel["cat_to_id"]] = new_rel
                        else:
                            new_rel = Relationship(
                                cat_from=self,
                                cat_to=cat_to,
                                mates=rel["mates"] or False,
                                besties=False,
                                enemies=False,
                                family=rel["family"] or False,
                                romantic_love=(rel["romantic_love"] or 0),
                                platonic_like=(rel["platonic_like"] or 0),
                                dislike=rel["dislike"] or 0,
                                admiration=rel["admiration"] or 0,
                                comfortable=rel["comfortable"] or 0,
                                jealousy=rel["jealousy"] or 0,
                                trust=rel["trust"] or 0,
                                log=rel["log"],
                            )
                        self.relationships[rel["cat_to_id"]] = new_rel
            except:
                print(
                    f"WARNING: There was an error reading the relationship file of cat #{self}."
                )

    @staticmethod
    def mediate_relationship(mediator, cat1, cat2, allow_romantic, sabotage=False):
        # Gather some important info

        # Gathering the relationships.
        if cat1.ID in cat2.relationships:
            rel1 = cat1.relationships[cat2.ID]
        else:
            rel1 = cat1.create_one_relationship(cat2)

        if cat2.ID in cat1.relationships:
            rel2 = cat2.relationships[cat1.ID]
        else:
            rel2 = cat2.create_one_relationship(cat1)

        # Output string.
        output = ""

        # Determine the chance of failure.
        if mediator.experience_level == "untrained":
            chance = 15
        elif mediator.experience_level == "trainee":
            # Negative bonus for very low.
            chance = 20
        elif mediator.experience_level == "prepared":
            chance = 35
        elif mediator.experience_level == "proficient":
            chance = 55
        elif mediator.experience_level == "expert":
            chance = 70
        elif mediator.experience_level == "master":
            chance = 100
        else:
            chance = 40

        compat = get_personality_compatibility(cat1, cat2)
        if compat is True:
            chance += 10
        elif compat is False:
            chance -= 5

        # Cat's compatibility with mediator also has an effect on success chance.
        for cat in (cat1, cat2):
            if get_personality_compatibility(cat, mediator) is True:
                chance += 5
            elif get_personality_compatibility(cat, mediator) is False:
                chance -= 5

        # Determine chance to fail, turning sabotage into mediate and mediate into sabotage
        if not int(random() * chance):
            apply_bonus = False
            if sabotage:
                output += "Sabotage Failed!\n"
                sabotage = False
            else:
                output += "Mediate Failed!\n"
                sabotage = True
        else:
            apply_bonus = True
            # EX gain on success
            if mediator.status.rank == CatRank.MEDIATOR:
                exp_gain = randint(10, 24)

                gm_modifier = 1
                if game.clan and game.clan.game_mode == "expanded":
                    gm_modifier = 3
                elif game.clan and game.clan.game_mode == "cruel season":
                    gm_modifier = 6

                if mediator.experience_level == "proficient":
                    lvl_modifier = 1.25
                elif mediator.experience_level == "expert":
                    lvl_modifier = 1.75
                elif mediator.experience_level == "master":
                    lvl_modifier = 2
                else:
                    lvl_modifier = 1
                mediator.experience += exp_gain / lvl_modifier / gm_modifier

        if mediator.status.rank == CatRank.MEDIATOR_APPRENTICE:
            mediator.experience += max(randint(1, 6), 1)

        # determine the traits to effect
        # Are they mates?
        mates = rel1.cat_from.ID in rel1.cat_to.mate

        pos_traits = ["platonic", "respect", "comfortable", "trust"]
        if allow_romantic and (mates or cat1.is_potential_mate(cat2, for_love_interest=True)):
            pos_traits.append("romantic")

        neg_traits = ["dislike", "jealousy"]

        # Determine the number of positive traits to effect, and choose the traits
        chosen_pos = sample(pos_traits, k=randint(2, len(pos_traits)))

        # Determine negative trains effected
        neg_traits = sample(neg_traits, k=randint(1, 2))

        if compat is True:
            personality_bonus = 2
        elif compat is False:
            personality_bonus = -2
        else:
            personality_bonus = 0

        # Effects on traits
        for trait in chosen_pos + neg_traits:
            # The EX bonus in not applied upon a fail.
            if apply_bonus:
                if mediator.experience_level == "very low":
                    # Negative bonus for very low.
                    bonus = randint(-2, -1)
                elif mediator.experience_level == "low":
                    bonus = randint(-2, 0)
                elif mediator.experience_level == "high":
                    bonus = randint(1, 3)
                elif mediator.experience_level == "master":
                    bonus = randint(3, 4)
                elif mediator.experience_level == "max":
                    bonus = randint(4, 5)
                else:
                    bonus = 0  # Average gets no bonus.
            else:
                bonus = 0

            decrease: bool = sabotage

            if trait == "romantic":
                if mates:
                    ran = (5, 10)
                else:
                    ran = (4, 6)

                if sabotage:
                    rel1.romantic_love = Cat.effect_relation(
                        rel1.romantic_love,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.romantic_love = Cat.effect_relation(
                        rel2.romantic_love,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                else:
                    rel1.romantic_love = Cat.effect_relation(
                        rel1.romantic_love,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.romantic_love = Cat.effect_relation(
                        rel2.romantic_love,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )

            elif trait == "platonic":
                ran = (4, 6)

                if sabotage:
                    rel1.platonic_like = Cat.effect_relation(
                        rel1.platonic_like,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.platonic_like = Cat.effect_relation(
                        rel2.platonic_like,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                else:
                    rel1.platonic_like = Cat.effect_relation(
                        rel1.platonic_like,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.platonic_like = Cat.effect_relation(
                        rel2.platonic_like,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )

            elif trait == "respect":
                ran = (4, 6)

                if sabotage:
                    rel1.admiration = Cat.effect_relation(
                        rel1.admiration,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.admiration = Cat.effect_relation(
                        rel2.admiration,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                else:
                    rel1.admiration = Cat.effect_relation(
                        rel1.admiration,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.admiration = Cat.effect_relation(
                        rel2.admiration,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )

            elif trait == "comfortable":
                ran = (4, 6)

                if sabotage:
                    rel1.comfortable = Cat.effect_relation(
                        rel1.comfortable,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.comfortable = Cat.effect_relation(
                        rel2.comfortable,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                else:
                    rel1.comfortable = Cat.effect_relation(
                        rel1.comfortable,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.comfortable = Cat.effect_relation(
                        rel2.comfortable,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )

            elif trait == "trust":
                ran = (4, 6)

                if sabotage:
                    rel1.trust = Cat.effect_relation(
                        rel1.trust,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.trust = Cat.effect_relation(
                        rel2.trust,
                        -(randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                else:
                    rel1.trust = Cat.effect_relation(
                        rel1.trust,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )
                    rel2.trust = Cat.effect_relation(
                        rel2.trust,
                        (randint(ran[0], ran[1]) + bonus) + personality_bonus,
                    )

            elif trait == "dislike":
                ran = (4, 9)
                if sabotage:
                    rel1.dislike = Cat.effect_relation(
                        rel1.dislike,
                        (randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    rel2.dislike = Cat.effect_relation(
                        rel2.dislike,
                        (randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                else:
                    rel1.dislike = Cat.effect_relation(
                        rel1.dislike,
                        -(randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    rel2.dislike = Cat.effect_relation(
                        rel2.dislike,
                        -(randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )

                decrease = not decrease

            elif trait == "jealousy":
                ran = (4, 6)

                if sabotage:
                    rel1.jealousy = Cat.effect_relation(
                        rel1.jealousy,
                        (randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    rel2.jealousy = Cat.effect_relation(
                        rel2.jealousy,
                        (randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                else:
                    rel1.jealousy = Cat.effect_relation(
                        rel1.jealousy,
                        -(randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )
                    rel2.jealousy = Cat.effect_relation(
                        rel2.jealousy,
                        -(randint(ran[0], ran[1]) + bonus) - personality_bonus,
                    )

                decrease = not decrease

            if decrease:
                output += i18n.t(
                    "screens.mediation.output_decrease",
                    trait=i18n.t(f"screens.mediation.{trait}"),
                )
            else:
                output += i18n.t(
                    "screens.mediation.output_increase",
                    trait=i18n.t(f"screens.mediation.{trait}"),
                )

        return output

    @staticmethod
    def effect_relation(current_value, effect):
        return clamp(current_value + effect, 0, 100)

    def set_faded(self):
        """This function is for cats that are faded. It will set the sprite and the faded tag"""
        self.faded = True

        # Silhouette sprite
        if self.age == CatAge.NEWBORN:
            file_name = "faded_newborn"
        elif self.age == CatAge.KITTEN:
            file_name = "faded_kitten"
        elif self.age in [
            CatAge.ADULT,
            CatAge.YOUNG_ADULT,
            CatAge.SENIOR_ADULT,
        ]:
            file_name = "faded_adult"
        elif self.age == CatAge.ADOLESCENT:
            file_name = "faded_adol"
        else:
            file_name = "faded_senior"

        if self.status.group == CatGroup.DARK_FOREST:
            file_name += "_df"

        file_name += ".png"

        self.sprite = image_cache.load_image(
            f"sprites/faded/{file_name}"
        ).convert_alpha()

    @staticmethod
    def fetch_cat(ID: str):
        """Fetches a cat object. Works for both faded and non-faded cats. Returns none if no cat was found."""
        if not ID or isinstance(ID, Cat):  # Check if argument is None or Cat.
            return ID
        elif not isinstance(ID, str):  # Invalid type
            return None
        if ID in Cat.all_cats:
            return Cat.all_cats[ID]
        else:
            return ob if (ob := Cat.load_faded_cat(ID)) else None

    @staticmethod
    def load_faded_cat(cat: str):
        """Loads a faded cat, returning the cat object. This object is saved nowhere else."""

        # just preventing any attempts to load something that isn't a cat ID
        if not cat.isdigit():
            return

        try:
            # todo: why can't this be `get_switch(Switch.clan_name)`?
            clan = (
                switch_get_value(Switch.clan_list)[0]
                if game.clan is None
                else game.clan.name
            )

            with open(
                get_save_dir() + "/" + clan + "/faded_cats/" + cat + ".json",
                "r",
                encoding="utf-8",
            ) as read_file:
                cat_info = ujson.loads(read_file.read())
                # If loading cats is attempted before the Clan is loaded, we would need to use this.

        except (
            AttributeError
        ):  # NOPE, cats are always loaded before the Clan, so doesn't make sense to throw an error
            with open(
                get_save_dir()
                + "/"
                + switch_get_value(Switch.clan_list)[0]
                + "/faded_cats/"
                + cat
                + ".json",
                "r",
                encoding="utf-8",
            ) as read_file:
                cat_info = ujson.loads(read_file.read())
        except:
            print("ERROR: in loading faded cat")
            return False

        if isinstance(cat_info["status"], str):
            status_dict = {"rank": cat_info["status"]}
        else:
            status_dict = cat_info["status"]

        cat_ob = Cat(
            ID=cat_info["ID"],
            prefix=cat_info["name_prefix"],
            suffix=cat_info["name_suffix"],
            status_dict=status_dict,
            moons=cat_info["moons"],
            faded=True,
        )
        if cat_info["parent1"]:
            cat_ob.parent1 = cat_info["parent1"]
        if cat_info["parent2"]:
            cat_ob.parent2 = cat_info["parent2"]
        cat_ob.faded_offspring = cat_info["faded_offspring"]
        cat_ob.adoptive_parents = (
            cat_info["adoptive_parents"] if "adoptive_parents" in cat_info else []
        )
        cat_ob.faded = True

        if cat_info.get("df"):
            cat_ob.status.send_to_afterlife(target=CatGroup.DARK_FOREST)
        elif isinstance(cat_info["status"], str):
            cat_ob.status.send_to_afterlife(target=CatGroup.STARCLAN)

        cat_ob.dead_for = cat_info["dead_for"] if "dead_for" in cat_info else 1

        return cat_ob

    # ---------------------------------------------------------------------------- #
    #                                  Sorting                                     #
    # ---------------------------------------------------------------------------- #

    @staticmethod
    def sort_cats(given_list=None):
        # disable unnecessary lambda in this function
        # pylint: disable=unnecessary-lambda
        if given_list is None:
            given_list = []
        if not given_list:
            given_list = Cat.all_cats_list
        sort_type = switch_get_value(Switch.sort_type)
        if sort_type == "age":
            given_list.sort(key=lambda x: Cat.get_adjusted_age(x))
        elif sort_type == "reverse_age":
            given_list.sort(key=lambda x: Cat.get_adjusted_age(x), reverse=True)
        elif sort_type == "id":
            given_list.sort(key=lambda x: int(x.ID))
        elif sort_type == "reverse_id":
            given_list.sort(key=lambda x: int(x.ID), reverse=True)
        elif sort_type == "rank":
            given_list.sort(
                key=lambda x: (Cat.rank_order(x), Cat.get_adjusted_age(x)), reverse=True
            )
        elif sort_type == "exp":
            given_list.sort(key=lambda x: x.experience, reverse=True)
        elif sort_type == "death":
            given_list.sort(key=lambda x: -1 * int(x.dead_for))

        return

    @staticmethod
    def insert_cat(c: Cat):
        sort_type = switch_get_value(Switch.sort_type)
        try:
            if sort_type == "age":
                bisect.insort(
                    Cat.all_cats_list, c, key=lambda x: Cat.get_adjusted_age(x)
                )
            elif sort_type == "reverse_age":
                bisect.insort(
                    Cat.all_cats_list, c, key=lambda x: -1 * Cat.get_adjusted_age(x)
                )
            elif sort_type == "rank":
                bisect.insort(
                    Cat.all_cats_list,
                    c,
                    key=lambda x: (
                        -1 * Cat.rank_order(x),
                        -1 * Cat.get_adjusted_age(x),
                    ),
                )
            elif sort_type == "exp":
                bisect.insort(Cat.all_cats_list, c, key=lambda x: x.experience)
            elif sort_type == "id":
                bisect.insort(Cat.all_cats_list, c, key=lambda x: int(x.ID))
            elif sort_type == "reverse_id":
                bisect.insort(Cat.all_cats_list, c, key=lambda x: -1 * int(x.ID))
            elif sort_type == "death":
                bisect.insort(Cat.all_cats_list, c, key=lambda x: -1 * int(x.dead_for))
        except (TypeError, NameError):
            # If you are using python 3.8, key is not a supported parameter into insort. Therefore, we'll need to
            # do the slower option of adding the cat, then resorting
            Cat.all_cats_list.append(c)
            Cat.sort_cats()

    @staticmethod
    def rank_order(cat: Cat):
        if cat.status.rank in Cat.rank_sort_order:
            return Cat.rank_sort_order.index(cat.status.rank)
        else:
            return 0

    @staticmethod
    def get_adjusted_age(cat: Cat):
        """Returns the moons + dead_for moons rather than the moons at death for dead cats, so dead cats are sorted by
        total age, rather than age at death"""
        if cat.dead:
            if constants.CONFIG["sorting"]["sort_rank_by_death"]:
                if switch_get_value(Switch.sort_type) == "rank":
                    return cat.dead_for
                else:
                    if constants.CONFIG["sorting"]["sort_dead_by_total_age"]:
                        return cat.dead_for + cat.moons
                    else:
                        return cat.moons
            else:
                if constants.CONFIG["sorting"]["sort_dead_by_total_age"]:
                    return cat.dead_for + cat.moons
                else:
                    return cat.moons
        else:
            return cat.moons

    # ---------------------------------------------------------------------------- #
    #                                  properties                                  #
    # ---------------------------------------------------------------------------- #

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, exp: int):
        exp = min(exp, self.experience_levels_range["grandmaster"][1])
        self._experience = int(exp)

        for x in self.experience_levels_range:
            if (
                self.experience_levels_range[x][0]
                <= exp
                <= self.experience_levels_range[x][1]
            ):
                self.experience_level = x
                break

    @property
    def moons(self):
        return self._moons

    @moons.setter
    def moons(self, value: int):
        self._moons = value

        updated_age = False
        for key_age in self.age_moons.keys():
            if self._moons in range(
                self.age_moons[key_age][0], self.age_moons[key_age][1] + 1
            ):
                updated_age = True
                self.age = key_age
        try:
            if not updated_age and self.age is not None:
                self.age = CatAge.SENIOR
        except AttributeError:
            print(f"ERROR: cat has no age attribute! Cat ID: {self.ID}")

    @property
    def sprite(self):
        if self.faded:
            return self._sprite

        # Update the sprite
        if self.pelt.rebuild_sprite or self.not_working() != self._sprite_working:
            self.pelt.rebuild_sprite = False
            self._sprite_working = self.not_working()
            update_sprite(self)
            update_mask(self)
        return self._sprite

    @sprite.setter
    def sprite(self, new_sprite):
        self._sprite = new_sprite

    @property
    def sprite_mask(self):
        if (
            scripts.game_structure.screen_settings.screen_scale
            != self.pelt.screen_scale
        ):
            self.pelt.screen_scale = scripts.game_structure.screen_settings.screen_scale
            update_mask(self)
        return self._sprite_mask

    @sprite_mask.setter
    def sprite_mask(self, val):
        self._sprite_mask = val

    # ---------------------------------------------------------------------------- #
    #                                  other                                       #
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def change_condition_name(condition):
        if not game_setting_get("warriorified names"):
            if condition in Cat.dad_names:
                condition = condition.replace(condition, Cat.dad_names.get(condition))

        return condition
    
    def get_info_block(self, *, make_clan=False, patrol=False, relationship=False):
        dadm_text = ""
        if len(self.pronouns) == 1:
            if self.pronouns[0].get("subject") == self.pronouns[0].get("object"):
                dadm_text += self.pronouns[0].get("subject") + "/" + self.pronouns[0].get("poss")
            else:
                dadm_text += self.pronouns[0].get("subject") + "/" + self.pronouns[0].get("object")
        else:
            for pronoun in self.pronouns:
                dadm_text += pronoun.get("subject") + "/"
            if dadm_text[-1] == "/":
                dadm_text = dadm_text[:-1]
                    
        awakened_text = ""        
        if self.awakened:
            if self.awakened["type"] in ["esper", "guide"]:
                awakened_text = self.awakened["class"] + "-class " + self.awakened["type"] + "\n"
                if self.awakened["type"] == "esper":
                    awakened_text += "power: " + self.awakened["ability"] + "\n"
            else:
                class1 = self.awakened["class"][0]
                class2 = self.awakened["class"][1]
                total_class = class1
                if class1 == "C" and class2 in ["B","A","S"]:
                    total_class = class2
                elif class1 == "B" and class2 in ["A","S"]:
                    total_class = class2
                elif class1 == "A" and class2 in ["S"]:
                    total_class = class2
                awakened_text = total_class + "-class " + self.awakened["type"] + "\n"
                awakened_text += "powers: " + self.awakened["ability"][0] + " and " + self.awakened["ability"][1] + "\n"

        if self.permanent_condition:
            dadm_text += "\n\ncondition"
            if len(self.permanent_condition) > 1:
                dadm_text += "s:\n"
            else:
                dadm_text += ":\n"
            for condition in self.permanent_condition:
                dadm_text += self.change_condition_name(str(condition)) + "\n"
            dadm_text = dadm_text[:-1]
                
        trait_text = i18n.t(f"cat.personality.{self.personality.trait}")
        if self.personality.trait != self.personality.trait2:
            trait_text += " & " + i18n.t(f"cat.personality.{self.personality.trait2}")
        if make_clan:
            return "\n".join(
                [
                    self.genderalign,
                    i18n.t(
                        (
                            f"general.{self.age}"
                            if self.age != "kitten"
                            else "general.kitten_profile"
                        ),
                        count=1,
                    ),
                    trait_text,
                    self.skills.skill_string(),
                    dadm_text,
                    awakened_text,
                ]
            )
        elif patrol:
            return "<br>".join(
                [
                    i18n.t(f"general.{self.status.rank.lower()}", count=1),
                    trait_text,
                    self.skills.skill_string(short=True),
                    i18n.t(f"cat.skills.{self.experience_level}")
                    + (
                        f" ({str(self.experience)})\n"
                        if get_clan_setting("showxp")
                        else "\n"
                    ),
                ]
            )
        elif relationship:
            return " - ".join(
                [
                    i18n.t("general.moons_age", count=self.moons),
                    self.genderalign,
                    trait_text,
                ]
            )

        return "\n".join(
            [
                i18n.t("general.moons_age", count=self.moons),
                i18n.t(f"general.{self.status.rank.lower()}", count=1),
                self.genderalign,
                trait_text,
                self.skills.skill_string(short=True),
            ]
        )

    def get_save_dict(self, faded=False):
        if faded:
            return {
                "ID": self.ID,
                "name_prefix": self.name.prefix,
                "name_suffix": self.name.suffix,
                "status": self.status.get_status_dict(),
                "moons": self.moons,
                "dead_for": self.dead_for,
                "parent1": self.parent1,
                "parent2": self.parent2,
                "past_life": self.past_life,
                "reincarnation": self.reincarnation,
                "adoptive_parents": self.adoptive_parents,
                "faded_offspring": self.faded_offspring,
            }
        else:
            return {
                "ID": self.ID,
                "name_prefix": self.name.prefix,
                "name_suffix": self.name.suffix,
                "specsuffix_hidden": self.name.specsuffix_hidden,
                "gender": self.gender,
                "gender_align": self.genderalign,
                "pronouns": (
                    self._pronouns
                    if self._pronouns is not None
                    else {i18n.config.get("locale"): self.pronouns}
                ),
                "birth_cooldown": self.birth_cooldown,
                "status": self.status.get_status_dict(),
                "backstory": self.backstory or None,
                "moons": self.moons,
                "trait": self.personality.trait,
                "trait2": self.personality.trait2,
                "facets": self.personality.get_facet_string(),
                "parent1": self.parent1,
                "parent2": self.parent2,
                "past_life": self.past_life,
                "reincarnation": self.reincarnation,
                "adoptive_parents": self.adoptive_parents,
                "mentor": self.mentor or None,
                "former_mentor": (
                    list(self.former_mentor) if self.former_mentor else []
                ),
                "patrol_with_mentor": (self.patrol_with_mentor or 0),
                "mate": self.mate,
                "bestie": self.bestie,
                "enemy": self.enemy,
                "previous_mates": self.previous_mates,
                "previous_besties": self.previous_besties,
                "previous_enemies": self.previous_enemies,
                "dead": self.dead,
                "paralyzed": self.pelt.paralyzed,
                "no_kits": self.no_kits,
                "no_retire": self.no_retire,
                "no_mates": self.no_mates,
                "pelt_name": self.pelt.name,
                "pelt_color": self.pelt.colour,
                "pelt_length": self.pelt.length,
                "sprite_kitten": self.pelt.cat_sprites["kitten"],
                "sprite_adolescent": self.pelt.cat_sprites["adolescent"],
                "sprite_adult": self.pelt.cat_sprites["adult"],
                "sprite_senior": self.pelt.cat_sprites["senior"],
                "sprite_para_adult": self.pelt.cat_sprites["para_adult"],
                "eye_colour": self.pelt.eye_colour,
                "eye_colour2": (self.pelt.eye_colour2 or None),
                "reverse": self.pelt.reverse,
                "white_patches": self.pelt.white_patches,
                "vitiligo": self.pelt.vitiligo,
                "points": self.pelt.points,
                "white_patches_tint": self.pelt.white_patches_tint if (type(self.pelt.white_patches_tint) == list) else [self.pelt.white_patches_tint],
                "pattern": self.pelt.pattern,
                "tortie_base": self.pelt.tortiebase,
                "tortie_color": self.pelt.tortiecolour,
                "tortie_pattern": self.pelt.tortiepattern,
                "tortie_tint": self.pelt.tortie_tint if (type(self.pelt.tortie_tint) == list) else [self.pelt.tortie_tint],
                "displays_2nd_tortie": self.pelt.displays_2nd_tortie,
                "pattern_2": self.pelt.pattern2,
                "tortie_color_2": self.pelt.tortiecolour2,
                "tortie_pattern_2": self.pelt.tortiepattern2,
                "tortie_tint_2": self.pelt.tortie_tint2 if (type(self.pelt.tortie_tint2) == list) else [self.pelt.tortie_tint2],
                "skin": self.pelt.skin,
                "tint": self.pelt.tint if (type(self.pelt.tint) == list) else [self.pelt.tint],
                "skill_dict": self.skills.get_skill_dict(),
                "physical_trait_1": self.pelt.physical_trait_1,
                "physical_trait_2": self.pelt.physical_trait_2,
                "physical_trait_3": self.pelt.physical_trait_3,
                "physical_trait_4": self.pelt.physical_trait_4,
                "physical_trait_hidden": self.pelt.physical_trait_hidden,
                "physical_trait_hidden_2": self.pelt.physical_trait_hidden_2,
                "physical_trait_hidden_3": self.pelt.physical_trait_hidden_3,
                "physical_trait_hidden_4": self.pelt.physical_trait_hidden_4,
                "scars": self.pelt.scars or [],
                "accessory": self.pelt.accessory,
                "experience": self.experience,
                "dead_moons": self.dead_for,
                "current_apprentice": list(self.apprentice),
                "former_apprentices": list(self.former_apprentices),
                "faded_offspring": self.faded_offspring,
                "opacity": self.pelt.opacity,
                "prevent_fading": self.prevent_fading,
                "immortality": self.immortality,
                "favourite": self.favourite,
                "favourite_moon": self.favourite_moon,
                "favourite_star": self.favourite_star,
                "fur_texture": self.pelt.fur_texture,
                "height": self.pelt.height,
                "build": self.pelt.build
               
            }

    def determine_next_and_previous_cats(
        self, filter_func: Callable[[Cat], bool] = None
    ):
        """Determines where the next and previous buttons point to, relative to this cat.

        :param filter_func: Allows you to constrain the list by any attribute of
            the Cat object. Takes a function which takes in a Cat instance and
            returns a boolean.
        """
        sorted_specific_list = [
            check_cat
            for check_cat in Cat.all_cats_list
            if check_cat.dead == self.dead
            and check_cat.status.is_outsider == self.status.is_outsider
            and not check_cat.faded
        ]

        if filter_func is not None:
            sorted_specific_list = [
                check_cat
                for check_cat in sorted_specific_list
                if filter_func(check_cat)
            ]

        if game.clan.instructor in sorted_specific_list:
            sorted_specific_list.remove(game.clan.instructor)
            sorted_specific_list.insert(0, game.clan.instructor)

        idx = sorted_specific_list.index(self)

        return (
            (
                sorted_specific_list[idx + 1].ID
                if len(sorted_specific_list) > idx + 1
                else 0
            ),
            sorted_specific_list[idx - 1].ID if idx - 1 >= 0 else 0,
        )


# ---------------------------------------------------------------------------- #
#                               END OF CAT CLASS                               #
# ---------------------------------------------------------------------------- #


# Creates a random cat
def create_cat(rank, moons=None, biome=None, secondary_biome=None, tertiary_biome=None, secondary_biome_weight=None, tertiary_biome_weight=None):
    status_dict = {"rank": rank}

    new_cat = Cat(status_dict=status_dict, biome=biome, secondary_biome=secondary_biome, tertiary_biome=tertiary_biome, secondary_biome_weight=secondary_biome_weight, tertiary_biome_weight=tertiary_biome_weight)

    if moons is not None:
        new_cat.moons = moons
    elif new_cat.moons >= 160:
        new_cat.moons = randint(120, 155)
    elif new_cat.moons == 0 and randint(1, 20) != 1:
        new_cat.moons = randint(1, 2)

    not_allowed_scars = [
        "NOPAW",
        "NOTAIL",
        "HALFTAIL",
        "NOEAR",
        "BOTHBLIND",
        "RIGHTBLIND",
        "LEFTBLIND",
        "BRIGHTHEART",
        "NOLEFTEAR",
        "NORIGHTEAR",
        "MANLEG",
    ]

    for scar in new_cat.pelt.scars:
        if scar in not_allowed_scars:
            new_cat.pelt.scars.remove(scar)
    
    if randint(1, constants.CONFIG["cat_generation"]["base_permanent_condition_two"]) <= constants.CONFIG["cat_generation"]["base_permanent_condition_one"]:
        new_cat.congenital_condition(new_cat)

    return new_cat


# Twelve example cats
def create_example_cats():
    warrior_indices = sample(range(12), 3)

    for cat_index in range(12):
        if cat_index in warrior_indices:
            game.choose_cats[cat_index] = create_cat(rank=CatRank.WARRIOR)
        else:
            random_rank = choice(
                [
                    CatRank.KITTEN,
                    CatRank.APPRENTICE,
                    CatRank.WARRIOR,
                    CatRank.WARRIOR,
                    CatRank.ELDER,
                ]
            )
            game.choose_cats[cat_index] = create_cat(rank=random_rank)


def create_option_preview_cat(scar: str = None, acc: str = None):
    """
    Creates a cat with the specified scar
    """
    new_cat = Cat(
        loading_cat=True,
        pelt=Pelt(
            name="SingleColour",
            length="short",
            colour="WHITE",
            white_patches=None,
            eye_color="GREY",
            eye_colour2=None,
            tortiebase=None,
            tortiecolour=None,
            pattern=None,
            tortiepattern=None,
            tortie_tint=["none"],
            displays_2nd_tortie=False,
            vitiligo=None,
            points=None,
            physical_trait_1=None,
            physical_trait_2=None,
            physical_trait_3=None,
            physical_trait_4=None,
            accessory=[acc] if acc else [],
            paralyzed=False,
            opacity=100,
            scars=[scar] if scar else [],
            tint=["none"],
            skin="BLACK",
            white_patches_tint=["none"],
            adult_sprite=8,
            reverse=False,
        ),
    )
    new_cat.age = CatAge.ADULT

    return new_cat


# CAT CLASS ITEMS
cat_class = Cat(example=True)
game.cat_class = cat_class

# ---------------------------------------------------------------------------- #
#                                load json files                               #
# ---------------------------------------------------------------------------- #

resource_directory = "resources/dicts/conditions/"
with open(f"{resource_directory}illnesses.json", "r", encoding="utf-8") as read_file:
    ILLNESSES = ujson.loads(read_file.read())

with open(f"{resource_directory}injuries.json", "r", encoding="utf-8") as read_file:
    INJURIES = ujson.loads(read_file.read())

with open(
    f"{resource_directory}permanent_conditions.json", "r", encoding="utf-8"
) as read_file:
    PERMANENT = ujson.loads(read_file.read())

MINOR_MAJOR_REACTION: Optional[Dict] = None
grief_lang: Optional[str] = None


def load_grief_reactions():
    global MINOR_MAJOR_REACTION, grief_lang
    if grief_lang == i18n.config.get("locale"):
        return
    MINOR_MAJOR_REACTION = load_lang_resource(
        "events/death/death_reactions/minor_major.json"
    )
    grief_lang = i18n.config.get("locale")


load_grief_reactions()

LEAD_CEREMONY_SC: Optional[Dict] = None
LEAD_CEREMONY_DF: Optional[Dict] = None
lead_ceremony_lang = None


def load_leader_ceremonies():
    global LEAD_CEREMONY_SC, LEAD_CEREMONY_DF, lead_ceremony_lang
    if lead_ceremony_lang == i18n.config.get("locale"):
        return
    LEAD_CEREMONY_SC = load_lang_resource("events/lead_ceremony_sc.json")
    LEAD_CEREMONY_DF = load_lang_resource("events/lead_ceremony_df.json")
    lead_ceremony_lang = i18n.config.get("locale")


load_leader_ceremonies()

with open("resources/dicts/backstories.json", "r", encoding="utf-8") as read_file:
    BACKSTORIES = ujson.loads(read_file.read())
