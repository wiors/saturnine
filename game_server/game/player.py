from lib.proto import Vector,EnterType,PlayerEnterSceneNotify, AvatarTeam, AvatarInfo, AvatarType, PropValue, AvatarFetterInfo
from game_server.utils.time import current_milli_time
from game_server.resource.enums import PropType
from game_server.game.world import World
from game_server.game.entity.avatar import AvatarEntity
from game_server.resource.enums import PropType, FightProp
from game_server.resource import resources
import dataclasses

@dataclasses.dataclass()
class Player:
    uid: int
    name: str
    avatar_id: int = 10000005
    world: World = World()

    scene_id: int = 0
    pos: Vector = dataclasses.field(default_factory=Vector)

    prop_map: dict[PropType, int] = dataclasses.field(default_factory=dict)
    next_guid: int = 0

    teams: dict[int, AvatarTeam] = dataclasses.field(default_factory=dict)

    avatars: list[AvatarEntity] = dataclasses.field(default_factory=list)
    cur_avatar_guid: int = 0
    cur_avatar_team_id: int = 0

    def init_default(self):
        self.prop_map = {
            PropType.PROP_IS_SPRING_AUTO_USE: 1,
            PropType.PROP_SPRING_AUTO_USE_PERCENT: 50,
            PropType.PROP_IS_FLYABLE: 1,
            PropType.PROP_IS_TRANSFERABLE: 1,
            PropType.PROP_CUR_PERSIST_STAMINA: 24000,
            PropType.PROP_MAX_STAMINA: 24000,
            PropType.PROP_PLAYER_LEVEL: 60,
            PropType.PROP_PLAYER_EXP: 0,
            PropType.PROP_PLAYER_HCOIN: 10,
        }
        self.teams = {
            0: AvatarTeam(avatar_guid_list=[], team_name="Team 1"),
            1: AvatarTeam(avatar_guid_list=[], team_name="Team 2"),
            2: AvatarTeam(avatar_guid_list=[], team_name="Team 3"),
            3: AvatarTeam(avatar_guid_list=[], team_name="Team 4"),
        }
        traveler = AvatarInfo()
        traveler.avatar_id = 10000005
        traveler.avatar_type = AvatarType.AVATAR_TYPE_FORMAL
        traveler.skill_depot_id = 504
        traveler.talent_id_list = []
        traveler.prop_map = {
            PropType.PROP_LEVEL._value_: PropValue(type=PropType.PROP_LEVEL._value_, val=80, ival=80),
            PropType.PROP_EXP._value_: PropValue(type=PropType.PROP_EXP._value_, val=0, ival=0),
            PropType.PROP_BREAK_LEVEL._value_: PropValue(type=PropType.PROP_BREAK_LEVEL._value_, val=4, ival=4),
        }

        traveler.fight_prop_map = {
                FightProp.FIGHT_PROP_BASE_HP._value_: 20000,
                FightProp.FIGHT_PROP_MAX_HP._value_: 20000,
                FightProp.FIGHT_PROP_BASE_DEFENSE._value_: 3000,
                FightProp.FIGHT_PROP_BASE_ATTACK._value_: 3000,
                FightProp.FIGHT_PROP_CRITICAL._value_: 1,
                FightProp.FIGHT_PROP_CRITICAL_HURT._value_: 2,
                FightProp.FIGHT_PROP_CHARGE_EFFICIENCY._value_: 2,
                FightProp.FIGHT_PROP_MAX_ROCK_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_MAX_ICE_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_MAX_WATER_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_MAX_FIRE_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_MAX_ELEC_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_MAX_GRASS_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_MAX_WIND_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_CUR_ROCK_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_CUR_ICE_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_CUR_WATER_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_CUR_ELEC_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_CUR_FIRE_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_CUR_WIND_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_CUR_GRASS_ENERGY._value_: 1,
                FightProp.FIGHT_PROP_CUR_HP._value_: 20000,
                FightProp.FIGHT_PROP_CUR_DEFENSE._value_: 3000,
                FightProp.FIGHT_PROP_CUR_ATTACK._value_: 3000,
                FightProp.FIGHT_PROP_SPEED_PERCENT._value_: 2,
                FightProp.FIGHT_PROP_SKILL_CD_MINUS_RATIO._value_: 1,
        }

        traveler.fetter_info = AvatarFetterInfo(exp_level=10, exp_number=10)
        traveler.equip_guid_list = []
        traveler.proud_skill_extra_level_map = {}
        traveler.inherent_proud_skill_list = []
        traveler.skill_level_map = {}
        traveler.life_state = 1
        traveler.core_proud_skill_level = 0
        traveler.guid = self.get_next_guid()
        self.avatars.append(AvatarEntity(self.world, traveler, self.pos))
        self.teams[self.cur_avatar_team_id].avatar_guid_list.append(traveler.guid)
        self.cur_avatar_guid = traveler.guid
        self.add_all_avatars()
    
    def add_all_avatars(self):
        for avatar_id, avatar_data in resources.excels.avatar_datas.items():
            print(avatar_id)
            print(avatar_data)
            if avatar_id == 10000005:
                continue
            skill_depot = resources.excels.avatar_skill_depot_datas[avatar_data.skill_depot_id]
            print(skill_depot)
            talents = skill_depot.talent_groups
            talents.append(skill_depot.leader_talent)
            avatar = AvatarInfo()
            avatar.avatar_id = int(avatar_id)
            avatar.avatar_type = AvatarType.AVATAR_TYPE_FORMAL
            avatar.skill_depot_id = int(avatar_data.skill_depot_id)
            avatar.talent_id_list = []
            avatar.prop_map = {
                PropType.PROP_LEVEL._value_: PropValue(type=PropType.PROP_LEVEL._value_, val=80, ival=80),
                PropType.PROP_EXP._value_: PropValue(type=PropType.PROP_EXP._value_, val=0, ival=0),
                PropType.PROP_BREAK_LEVEL._value_: PropValue(type=PropType.PROP_BREAK_LEVEL._value_, val=4, ival=4),
            }
            avatar.fight_prop_map = {
                    FightProp.FIGHT_PROP_BASE_HP._value_: 20000,
                    FightProp.FIGHT_PROP_MAX_HP._value_: 20000,
                    FightProp.FIGHT_PROP_BASE_DEFENSE._value_: 3000,
                    FightProp.FIGHT_PROP_BASE_ATTACK._value_: 3000,
                    FightProp.FIGHT_PROP_CRITICAL._value_: 1,
                    FightProp.FIGHT_PROP_CRITICAL_HURT._value_: 2,
                    FightProp.FIGHT_PROP_CHARGE_EFFICIENCY._value_: 2,
                    FightProp.FIGHT_PROP_MAX_ROCK_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_MAX_ICE_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_MAX_WATER_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_MAX_FIRE_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_MAX_ELEC_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_MAX_GRASS_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_MAX_WIND_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_CUR_ROCK_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_CUR_ICE_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_CUR_WATER_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_CUR_ELEC_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_CUR_FIRE_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_CUR_WIND_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_CUR_GRASS_ENERGY._value_: 1,
                    FightProp.FIGHT_PROP_CUR_HP._value_: 20000,
                    FightProp.FIGHT_PROP_CUR_DEFENSE._value_: 3000,
                    FightProp.FIGHT_PROP_CUR_ATTACK._value_: 3000,
                    FightProp.FIGHT_PROP_SPEED_PERCENT._value_: 2,
                    FightProp.FIGHT_PROP_SKILL_CD_MINUS_RATIO._value_: 1,
            }
            avatar.fetter_info = AvatarFetterInfo(exp_level=10, exp_number=10)
            avatar.equip_guid_list = []
            avatar.proud_skill_extra_level_map = {}
            avatar.inherent_proud_skill_list = []
            avatar.skill_level_map = {}
            avatar.life_state = 1
            avatar.core_proud_skill_level = 0
            avatar.guid = self.get_next_guid()
            self.avatars.append(AvatarEntity(self.world, avatar, self.pos))

    def get_cur_avatar(self):
        return self.get_avatar_by_guid(self.cur_avatar_guid)

    def get_avatar_by_guid(self, guid: int):
        for avatar_entity in self.avatars: 
            if avatar_entity.guid == guid:
                return avatar_entity

    def get_avatar_by_entity_id(self, entity_id: int):
        for avatar_entity in self.avatars: 
            if avatar_entity.entity_id == entity_id:
                return avatar_entity

    def get_teleport_packet(self, scene_id: int, pos: Vector, enter_type: EnterType = EnterType.ENTER_SELF):
        player_enter_scene_notify = PlayerEnterSceneNotify()
        player_enter_scene_notify.scene_id = scene_id
        player_enter_scene_notify.pos = pos
        player_enter_scene_notify.scene_begin_time = current_milli_time()
        player_enter_scene_notify.type = enter_type
        player_enter_scene_notify.enter_scene_token = 1000
        player_enter_scene_notify.world_level = 8
        player_enter_scene_notify.target_uid = self.uid
        return player_enter_scene_notify
    
    def get_next_guid(self):
        self.next_guid += 1
        return self.next_guid
        