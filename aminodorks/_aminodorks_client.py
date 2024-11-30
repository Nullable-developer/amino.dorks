from time import time
from asyncio import AbstractEventLoop
from msgspec.json import encode, decode

from typing import (
    List,
    Tuple,
    Mapping,
    Optional,
    BinaryIO,
    MutableMapping
)

from aiohttp import (
    TraceConfig,
    TCPConnector,
    ClientSession
)

from ._utils import (
    generate_device_id,
    generate_signature,
    session_id_to_user_id
)

from .models import (
    UserObject,
    CommunitiesObject,
    ThreadsObject,
    ThreadList,
    MembersObject
)


class ADorksClient:
    __slots__: Tuple = (
        "_loop",
        "_proxy",
        "_session",
        "_connector",
        "_user_object",
        "_device_id", 
        "_session_id", 
        "_trace_configs",
        "_mutable_headers",
    )

    def __init__(
        self, 
        device_id: Optional[str] = None,
        session_id: Optional[str] = None,
        *,
        proxy: Optional[str] = None,
        loop: Optional[AbstractEventLoop] = None, 
        connector: Optional[TCPConnector] = None, 
        trace_configs: Optional[List[TraceConfig]] = None
    ) -> None:
        self._device_id: Optional[str] = device_id
        self._session_id: Optional[str] = session_id
        self._proxy: Optional[str] = proxy
        self._loop: Optional[AbstractEventLoop] = loop
        self._connector: Optional[TCPConnector] = connector
        self._trace_configs: Optional[List[TraceConfig]] = trace_configs
        self._session: Optional[ClientSession] = None
        self._user_object: Optional[UserObject] = None

    @property
    def device_id(self) -> str:
        if not self._device_id:
            self._device_id = generate_device_id() 

        return self._device_id 
    
    @property
    def session_id(self) -> Optional[str]:
        return self._session_id 
    
    @property
    def headers(self) -> MutableMapping[str, str]:
        return {
            "Accept-Language": "en-US",
            "User-Agent": "Apple iPhone13,4 iOS v15.6.1 Main/3.12.9",
            "Host": "service.aminoapps.com",
            "NDCDEVICEID": self.device_id,
            "NDCAUTH": f"sid={self.session_id}"
        }
    
    @property
    def session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                connector=self._connector,
                trace_configs=self._trace_configs,
                base_url="https://service.aminoapps.com"
            )
        
        return self._session
    
    @property
    def media_types(self) -> Mapping[str, str]:
        return {
            "audio": "audio/aac",
            "image": "image/jpg"
        }

    async def _request(
            self, 
            method: str, 
            path: str, 
            headers: MutableMapping[str, str],
            data: Optional[bytes] = None,
        ) -> Mapping:
        if data:
            headers["NDC-MSG-SIG"] = generate_signature(data) 
            
        async with self.session.request(method=method, url=path, headers=headers, proxy=self._proxy, data=data) as response:
            if response.status != 200:
                raise Exception(await response.text())
            
            return await response.text()
    
    async def login(self, email: str, password: str) -> UserObject:
        data = encode({
            "email": email,
            "v": 2,
            "secret": f"0 {password}",
            "deviceID": self.device_id,
            "clientType": 100,
            "action": "normal",
            "timestamp": int(time() * 1000)
        })
        
        response = await self._request("POST", "/api/v1/g/s/auth/login", data=data, headers=self.headers)
        self._user_object = decode(response, type=UserObject)
        self._session_id = self._user_object.sid
        return self._user_object

    async def login_on_session_id(self, session_id: str) -> UserObject:
        self._session_id = session_id
        self._user_object = await self.get_user(session_id_to_user_id(session_id))
        return self._user_object
    
    async def upload_media(self, file: BinaryIO, file_type: str = "image") -> None:
        headers = self.headers
        headers["Content-Type"] = self.media_types[file_type]
        response = await self._request("POST", "/api/v1/g/s/media/upload", data=file.read(), headers=self.headers)
    
    async def get_communities(self) -> CommunitiesObject:
        response = await self._request("GET", "/api/v1/g/s/community/joined?v=1&start=0&size=100", headers=self.headers)
        return decode(response, type=CommunitiesObject)
    
    async def get_user(self, user_id: str) -> UserObject:
        response = await self._request("GET", f"/api/v1/g/s/user-profile/{user_id}", headers=self.headers)
        return decode(response, type=UserObject)
    
    async def get_threads(self) -> ThreadsObject:
        response = await self._request("GET", f"/api/v1/g/s/chat/thread?type=joined-me&start=0&size=100", headers=self.headers)
        return decode(response, type=ThreadsObject)
    
    async def get_thread(self, thread_id: str) -> ThreadList:
        response = await self._request("GET", f"/api/v1/g/s/chat/thread/{thread_id}", headers=self.headers)
        return decode(response, type=ThreadList)

    async def get_thread_users(self, thread_id: int) -> MembersObject:
        response = await self._request("GET", f"/api/v1/g/s/chat/thread/{thread_id}/member?start=0&size=100&type=default&cv=1.2", headers=self.headers)
        return decode(response, type=MembersObject)
    
    async def join_thread(self, thread_id: str) -> None:
        headers = self.headers
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        await self._request("POST", f"/api/v1/g/s/chat/thread/{thread_id}/member/{self._user_object.auid}", headers=headers)

    async def leave_thread(self, thread_id: str) -> None:
        await self._request("DELETE", f"/api/v1/g/s/chat/thread/{thread_id}/member/{self._user_object.auid}", headers=self.headers)

    async def invite_to_thread(self, thread_id: str, user_ids: List[str]) -> None:
        await self._request(
            method="POST",
            path=f"/api/v1/g/s/chat/thread/{thread_id}/member/invite",
            headers=self.headers,
            data=encode({
                "uids": user_ids,
                "timestamp": int(time() * 1000)
            })
        )
