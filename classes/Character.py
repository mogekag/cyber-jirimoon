import numpy as np


class Character:

    def __init__(self, character_class=None):
        self.level = 1
        self.experience = 0
        # self.class = class  # TODO: implement classes and skills
        '''
        Player Variable Statuses

        Physical Offensive Statuses
            Strength (STR)      : Will affect attack of physical weapons, mainly melee.
            Dexterity (DEX)     : Will affect attack of physical weapons, mainly ranged.

        Magical Offensive Statuses
            Intellect (INT)     : Will affect mainly the damage output of ranged magical weapons and spells.
            Knowledge (KWL)     : Will affect the damage output of melee magical weapons and spells.

        Physical Defensive Statuses
            Vitality (VIT)      : Will affect the player's health and also the hard defense against physical attacks.
            Agility (AGI)       : Will affect the player's flee rate and also adds a possibility of not being hit by the full attack damage.

        Magical Defensive Statuses
            Perception (PCN)    : Straight up adds to magical defense.
            OBS: Other statuses will influence the calculation of magical defense, such as dexterity, vitality, agility and knowledge.

        Miscellaneous Statuses
            Luck (LUK)          : Will benefit the player with all the probabilities calculations for non-permanent statuses, critical hits and crafting success rates.
        '''
        self.status = {
            # physical offensive status
            'STR'   : 1,
            'DEX'   : 1,
            # magical offensive status
            'INT'   : 1,
            'KWL'   : 1,
            # physical defense status
            'VIT'   : 1,
            'AGI'   : 1,
            # magical defense status
            'PCN'   : 1,
            # miscellaneous status
            'LUK'   : 1
        }

        # TODO: equip_item(), unequip_item(), implement bag and picking and
        # dropping items.
        # Once items are done, equip a basic set of items for starters based on
        # the characters class.
        self.equipment = {
            'upper_headgear'    :   None,
            'middle_headgear'   :   None,
            'lower_headgear'    :   None,
            'shoulder'          :   None,
            'upper_body'        :   None,
            'main_hand'         :   None,
            'off_hand'          :   None,
            'main_hand_opt'     :   None,
            'off_hand_opt'      :   None,
            'belt'              :   None,
            'lower_body'        :   None,
            'shoes'             :   None,
            'earing'            :   None,
            'necklace'          :   None,
            'rings'             :   [None, None],
            'bracelets'         :   [None, None]
        }

        self.attributes = {
            'MCW'   :   self.calculate_mcw(),
            'ATK'   :   self.calculate_atk(),
            'MATK'  :   self.calculate_matk(),
            'ACC'   :   self.calculate_acc(),
            'FLEE'  :   self.calculcate_flee(),
            'DEF'   :   self.calculate_def(),
            'MDEF'  :   self.calculate_mdef(),
            'MSPD'  :   self.calculate_mspd(),
            'ASPD'  :   self.calculate_asped(),
            'CSPD'  :   self.calculate_cspd(),
            'SCLD'  :   self.calculate_scld(),
            'maximum_hp'    :   self.calculate_maxhp(),
            'current_hp'    :   self.attributes['maximum_hp'],
            'regen_hp'      :   10,
            'maximum_mp'    :   self.calculate_maxmp(),
            'current_mp'    :   self.attributes['maximum_mp'],
            'regen_mp'      :   3,
            'maximum_sp'    :   self.calculate_maxsp(),
            'current_sp'    :   self.attributes['maximum_sp'],
            'regen_sp'      :   3,
        }

        # Buffs and Debuffs
        # TODO: apply_modifiers() and update_modifiers()
        self.modifiers = list()

    '''
    Constants used for calculating experience curve.
    '''
    @staticmethod
    def exp_constants():
        base = 20
        offset = 10

        return base, offset

    '''
    Experience curve for leveling a character. Every character
    starts at level 1 and max level is 99.
    '''
    @staticmethod
    def experience_curve(level):
        if level > 99:
            level = 99
        elif level < 1:
            level = 1

        base, offset = self.exp_constants()

        return np.exp((level * base) + offset)

    '''
    Maximum Carrying Weight (MCW)
    Players will have a maximum weight capacity that will be calculated base in
    their statuses. I am thinking about considering a multiple of player's STR,
    but also based on what type of bag and enchantments the player has.
    '''
    def calculate_mcw(self):
        return self.status['strength'] * 100 # Kilograms

    '''
    Attack (ATK)
    Will be calculated based on the weapon that is being used with the following
    formulae (MAX-MIN 10% range):
        Melee physical weapons:
            [(STR*LVL/5) + (DEX/7)]*(Weapon Physical ATK)
        Ranged physical weapons:
            [(DEX*LVL/5) + (STR/10)]*(Weapon Physical ATK)
    '''
    def calculate_atk(self):
        # TODO: requires the implementation of weapons
        pass

    '''
    Magical Attack (MATK)
    Will be calculated based on the weapom type and status, but even non-magical
    characters will have some MATK.
        Melee magical weapons:
            [(STR/8) + (KWL*LVL/3)]*(Weapon Magical ATK)
        Ranged magical weapons:
            [(DEX/6) + (INT*LVL/5)]*(Weapon Magical ATK)
    '''
    def calculate_matk(self):
        # TODO: requires the implementation of weapons
        pass

    '''
    Accuracy (ACC)
    Accuracy will influence if the player hits the target, if the ACC is within
    10% range of FLEE there will be a calculation based on LUK to hit. Higher
    than FLEE is a hit with LUK calculation of miss, lower than FLEE is a 99%
    miss with LUK calculation of hit.

    ACC = []*(Player LVL) - []*(Enemy LVL)
    Therefore ACC depends on what enemy you're fighting, but the displayed value
    will be the calculation considering an EnemyLVL=0
    '''
    def calculate_acc(self, enemy=False):
        # TODO: requires the implementation of weapons
        pass

    '''
    Flee Rate (FLEE)
    This will need to be tweaked later, since Accuracy will have a different
    formula based on different attributes, but they shall have values within the
    same range. Perhaps introducing a maximum value for FLEE and ACC.
    '''
    def calculcate_flee(self):
        # TODO: requires the implementation of equipment
        pass

    '''
    Defense (DEF)
    The damage mitigation of physical attacks. Once the attack is calculated and
    passes the FLEE, i.e. a hit will be performed, a calculation using DEF
    mitigate the damage received. There shall be two types of hard defense.

        Melee DEF:
        Defense mitigation of melee type ATK. The player will be inflicted
        DMG * (1-DEF), e.g. a player that has 20% DEF will receive only 80% of
        the ATK as DMG.

        Ranged DEF:
        Defense against projectiles, does not consider magical projectiles, but
        is calculated prior to magical damage when using elemental projectiles.
        (Does not apply to spell projectiles, e.g. elemental bolts, MDEF will be
        applied.)

     Equipments may add bonuses for Melee or Ranged DEF, for example, plate
     armors have high melee DEF but decrease ranged DEF, thus receiving more DMG
     from arrows and projectiles.

     OBS: Defense and Magical Defense may be negative, this shall amplify damage
     received, the values represent percentages of damage reduction and is
     calculated prior to buffs and debuffs.

    '''
    def calculate_def(self):
        # TODO: requires the implementation of equipment
        pass

    '''
    Magical Defense (MDEF)
    Defense against magical attacks and spells. MDEF is used to calculate
    magical DMG from magical projectiles, once the physical projectile is
    accounted for, the magical DMG is considered after. This means a player
    may receive no DMG whatsoever from the physical projectile, but receives
    magical damage from the element of the projectile. Bonuses of elemental dmg
    are applied before considering MDEF.
    '''
    def calculate_mdef(self):
        # TODO: requires the implementation of equipment
        pass

    '''
    Movement Speed (MSPD)
    The character MSPD will be pretty much the same for all, monsters and
    enemies will have varying MSPD and will  be able to debuff characters in
    order to move slower. Buffs may be applied to increase MSPD and a few
    equipments may add up to increase MSPD.
    '''
    def calculate_mspd(self):
        # TODO: requires the implementation of equipment and buffs
        return 100

    '''
    Attack Speed (ASPD)
    ASPD is the amount of attacks in a given second, based purely on AGI and
    DEX, the ASPD maximum of a player in a give time will be the one calculated
    without any weapon equipped. Every weapon has a different penalty for ASPD
    and equipments may increase/decrease a given percentage of ASPD, never
    surpassing the weaponless limit.

    There will be de(buffs) for ASPD.
    '''
    def calculate_aspd(self):
        # TODO: requires the implementation of weapons
        pass

    '''
    Cast Speed (CSPD)
    Some skills and spells will have cast time, some of them are fixed cast
    times and there is no way to get through the time. The skills and spells
    that allow variable cast time will have a maximum and minimum cast time
    limit, but will calculate the CSPD based on player attributes.

        DEX and AGI will influence skill CSPD.
        INT and KWL will influence spell CSPD.
    '''
    def calculate_scpd(self):
        # TODO: requires the implementation of skills
        pass

    '''
    Cooldown (CLD)
    Cooldown is the time a player will have to wait in order to use skills
    and/or spells after casting any of them. There will be two types of CLD:

        Hard Cooldown (HCLD)
            Hard cooldown is the time delay to use the same spell/skill again,
            this is based on the cooldown listed for the respective action and
            will be taken care by the skill engine itself.

        Soft Cooldown (SCLD)
            Soft cooldown is the time delay to cast any spell/skill other than
            the one that was just casted. This is a character property.

    Some skills/spells have no CLD timer, but a player cannot cast more than one
    spell/skill at time.

    '''
    def calculate_scld(self):
        # TODO: requires the implementation of skills
        pass
