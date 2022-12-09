from pydantic import BaseModel

class CompareChannels(BaseModel):
    channel_left_id: str
    channel_right_id: str

class GetChannelWordLine(BaseModel):
    channel_id: str
    word: str