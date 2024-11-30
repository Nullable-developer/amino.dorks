from msgspec import Struct, field
from typing import Optional, List


class AvatarFrame(Struct, kw_only=True):
    status:             int
    ownershipStatus:    int
    version:            int
    resourceUrl:        str
    name:               str
    icon:               str
    frameType:          int
    frameId:            str


class MemberListItem(Struct, kw_only=True):
    status:                     int
    isNicknameVerified:         bool
    uid:                        str
    level:                      int
    accountMembershipStatus:    int
    membershipStatus:           int
    reputation:                 int
    role:                       int
    nickname:                   str
    icon:                       Optional[str]
    avatarFrame:                Optional[AvatarFrame]   =   None


class MembersObject(Struct, kw_only=True):
    member_list:       Optional[List[MemberListItem]]    =   field(name="memberList")
