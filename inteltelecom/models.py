from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date


class CallerID(BaseModel):
    name: str
    number: str


class DialplanCEP(BaseModel):
    context: str = Field(..., description="Context in the dialplan")
    exten: str = Field(..., description="Extension in the dialplan")
    priority: int = Field(..., description="Priority in the dialplan")
    app_name: str = Field(..., description="Name of current dialplan application")
    app_data: str = Field(..., description="Parameter of current dialplan application")


class Channel(BaseModel):
    id: str = Field(..., description="Unique identifier of the channel. Same as the Uniqueid field in AMI")
    name: str = Field(..., description="Name of the channel (e.g., SIP/foo-0000a7e3)")
    state: Literal[
        'Down', 'Rsrved', 'OffHook', 'Dialing', 'Ring', 'Ringing', 'Up', 'Busy', 'Dialing Offhook', 'Pre-ring', 'Unknown'
    ] = Field(..., description="State of the channel")
    caller: CallerID = Field(..., description="Caller ID information")
    connected: CallerID = Field(..., description="Connected party ID information")
    accountcode: str = Field(..., description="Account code associated with the channel")
    dialplan: DialplanCEP = Field(..., description="Current location in the dialplan")
    creationtime: date = Field(..., description="Timestamp when channel was created")
    language: str = Field(..., description="Default spoken language")
    channelvars: Optional[dict] = Field(None, description="Channel variables (optional)")


class Bridge(BaseModel):
    id: str = Field(..., description="Unique identifier for this bridge")
    technology: str = Field(..., description="Name of the current bridging technology")
    bridge_type: Literal['mixing', 'holding'] = Field(..., description="Type of bridge technology")
    bridge_class: str = Field(..., description="Bridging class")
    creator: str = Field(..., description="Entity that created the bridge")
    name: str = Field(..., description="Name the creator gave the bridge")
    channels: List[str] = Field(..., description="Ids of channels participating in this bridge")
    video_mode: Optional[Literal['none', 'talker', 'sfu', 'single']] = Field(
        None, description="The video mode the bridge is using. One of 'none', 'talker', 'sfu', or 'single'"
    )
    video_source_id: Optional[str] = Field(
        None, description="The ID of the channel that is the source of video in this bridge, if one exists"
    )
    creationtime: date = Field(..., description="Timestamp when bridge was created")


class StoredRecording(BaseModel):
    name: str = Field(..., description="Name of the stored recording")
    format: str = Field(..., description="Format of the stored recording")


class FormatLangPair(BaseModel):
    format: str = Field(..., description="Format of the sound")
    language: str = Field(..., description="Language of the sound")


class Sound(BaseModel):
    id: str = Field(..., description="Sound's identifier")
    text: Optional[str] = Field(None, description="Text description of the sound, usually the words spoken")
    formats: List[FormatLangPair] = Field(..., description="The formats and languages in which this sound is available")


class Playback(BaseModel):
    id: str = Field(..., description="ID for this playback operation")
    media_uri: str = Field(..., description="The URI for the media currently being played back")
    next_media_uri: Optional[str] = Field(
        None, description="If a list of URIs is being played, the next media URI to be played back"
    )
    target_uri: str = Field(..., description="URI for the channel or bridge to play the media on")
    language: Optional[str] = Field(
        None, description="For media types that support multiple languages, the language requested for playback"
    )
    state: Literal['queued', 'playing', 'continuing', 'done', 'failed'] = Field(
        ..., description="Current state of the playback operation"
    )


class DeviceState(BaseModel):
    name: str = Field(..., description="Name of the device")
    state: Literal[
        'UNKNOWN', 'NOT_INUSE', 'INUSE', 'BUSY', 'INVALID', 'UNAVAILABLE', 'RINGING', 'RINGINUSE', 'ONHOLD'
    ] = Field(..., description="Device's state")


class Mailbox(BaseModel):
    name: str = Field(..., description="Name of the mailbox")
    old_messages: int = Field(..., description="Count of old messages in the mailbox")
    new_messages: int = Field(..., description="Count of new messages in the mailbox")


class Message(BaseModel):
    type: str = Field(..., description="Indicates the type of this message")
    asterisk_id: Optional[str] = Field(None, description="The unique ID for the Asterisk instance that raised this event")


class Application(BaseModel):
    name: str = Field(..., description="Name of this application")
    channel_ids: List[str] = Field(..., description="IDs for channels subscribed to")
    bridge_ids: List[str] = Field(..., description="IDs for bridges subscribed to")
    endpoint_ids: List[str] = Field(..., description="{tech}/{resource} for endpoints subscribed to")
    device_names: List[str] = Field(..., description="Names of the devices subscribed to")
    events_allowed: List[object] = Field(..., description="Event types sent to the application")
    events_disallowed: List[object] = Field(..., description="Event types not sent to the application")