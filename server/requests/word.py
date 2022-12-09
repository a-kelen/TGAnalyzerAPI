from pydantic import BaseModel

class CompareChannelsByWord(BaseModel):
    channel_left_id: str
    channel_right_id: str
    word: str

class WordReq(BaseModel):
    word: str

class GetWordStatsByChannel(BaseModel):
    channel_id: str
    word: str
