from msgspec import Struct, field 
from typing import Optional, List


class CommunityList(Struct, kw_only=True):
    link:               Optional[str] 
    icon:               Optional[str]
    name:               Optional[str]
    endpoint:           Optional[str]
    ndc_id:             Optional[int]   =   field(name="ndcId")
    modified_time:      Optional[str]   =   field(name="modifiedTime")
    primary_language:   Optional[str]   =   field(name="primaryLanguage")
    join_type:          Optional[int]   =   field(name="joinType")


class CommunitiesObject(Struct, kw_only=True):
    community_list:     Optional[List[CommunityList]]   =   field(name="communityList")
