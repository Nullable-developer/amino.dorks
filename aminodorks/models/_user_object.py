from msgspec import Struct, field
from typing import Optional, Any


class Account(Struct, kw_only=True):
    username:           Optional[Any] 
    uid:                Optional[str]  
    email:              Optional[str] 
    nickname:           Optional[str]
    role:               Optional[int] 
    icon:               Optional[Any]


class UserProfile(Struct, kw_only=True):
    role:               Optional[int]
    icon:               Optional[str]
    level:              Optional[int]
    nickname:           Optional[str]
    mood_sticker:       Optional[Any]   =   field(name="moodSticker") 
    items_count:        Optional[int]   =   field(name="itemsCount") 
    modified_time:      Optional[str]   =   field(name="modifiedTime") 
    following_status:   Optional[int]   =   field(name="followingStatus")
    posts_count:        Optional[int]   =   field(name="postsCount") 
    members_count:      Optional[int]   =   field(name="membersCount") 
    media_list:         Optional[Any]   =   field(name="mediaList") 
    ndc_id:             Optional[int]   =   field(name="ndcId")
    stories_count:      Optional[int]   =   field(name="storiesCount") 


class UserObject(Struct, kw_only=True):
    auid:           Optional[str]           =   None
    secret:         Optional[str]           =   None
    sid:            Optional[str]           =   None
    account:        Optional[Account]       =   None
    user_profile:   Optional[UserProfile]   =   field(name="userProfile")
