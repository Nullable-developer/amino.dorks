from msgspec import Struct, field 
from typing import Optional, List, Any


class ThreadList(Struct, kw_only=True):
    type:           Optional[int]
    status:         Optional[int]
    icon:           Optional[str]
    uid:            Optional[str]
    title:          Optional[str]
    content:        Optional[Any]
    keywords:       Optional[Any]
    ndc_id:         Optional[int]   =   field(name="ndcId")
    thread_id:      Optional[str]   =   field(name="threadId")
    created_time:   Optional[Any]   =   field(name="createdTime")


class ThreadsObject(Struct, kw_only=True):
    thread_list:    Optional[List[ThreadList]]  =   field(name="threadList")
