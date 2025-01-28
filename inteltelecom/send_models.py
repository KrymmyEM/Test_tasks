from pydantic import BaseModel, Field
from typing import Optional

class RecordingConfig(BaseModel):
    name: str = Field(..., description="Recording's filename")
    format: str = Field(..., description="Format to encode audio in")
    maxDurationSeconds: Optional[int] = Field(0, ge=0, description="Maximum duration of the recording, in seconds. 0 for no limit.")
    maxSilenceSeconds: Optional[int] = Field(0, ge=0, description="Maximum duration of silence, in seconds. 0 for no limit.")
    ifExists: Optional[str] = Field("fail", description="Action to take if a recording with the same name already exists.",
                                    enum=["fail", "overwrite", "append"])
    beep: Optional[bool] = Field(False, description="Play beep when recording begins")
    terminateOn: Optional[str] = Field("none", description="DTMF input to terminate recording.",
                                       enum=["none", "any", "*", "#"])


class MediaPlaybackConfig(BaseModel):
    media: str = Field(..., description="Media URIs to play. Allows comma separated values.")
    lang: Optional[str] = Field(None, description="For sounds, selects language for sound.")
    offsetms: Optional[int] = Field(0, ge=0, description="Number of milliseconds to skip before playing. Only applies to the first URI if multiple media URIs are specified.")
    skipms: Optional[int] = Field(3000, ge=0, description="Number of milliseconds to skip for forward/reverse operations. Default: 3000.")
    playbackId: Optional[str] = Field(None, description="Playback ID.")


class CallConfig(BaseModel):
    endpoint: str = Field(..., description="Endpoint to call.")
    extension: Optional[str] = Field(None, description="The extension to dial after the endpoint answers. Mutually exclusive with 'app'.")
    context: Optional[str] = Field("default", description="The context to dial after the endpoint answers. If omitted, uses 'default'. Mutually exclusive with 'app'.")
    priority: Optional[int] = Field(1, ge=1, description="The priority to dial after the endpoint answers. If omitted, uses 1. Mutually exclusive with 'app'.")
    label: Optional[str] = Field(None, description="The label to dial after the endpoint answers. Will supersede 'priority' if provided. Mutually exclusive with 'app'.")
    app: Optional[str] = Field(None, description="The application that is subscribed to the originated channel. Mutually exclusive with 'context', 'extension', 'priority', and 'label'.")
    appArgs: Optional[str] = Field(None, description="The application arguments to pass to the Stasis application provided by 'app'. Mutually exclusive with 'context', 'extension', 'priority', and 'label'.")
    callerId: Optional[str] = Field(None, description="CallerID to use when dialing the endpoint or extension.")
    timeout: Optional[int] = Field(30, ge=-1, description="Timeout (in seconds) before giving up dialing, or -1 for no timeout. Default: 30.")
    channelId: Optional[str] = Field(None, description="The unique id to assign the channel on creation.")
    otherChannelId: Optional[str] = Field(None, description="The unique id to assign the second channel when using local channels.")
    originator: Optional[str] = Field(None, description="The unique id of the channel which is originating this one.")
    formats: Optional[str] = Field(None, description="The format name capability list to use if originator is not specified. Ex. 'ulaw,slin16'.")
