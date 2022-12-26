from fastapi import FastAPI
from fastapi.responses import JSONResponse

from server.services import channelService, wordService
from server.requests.channel import CompareChannels, GetChannelWordLine
from server.requests.word import CompareChannelsByWord, WordReq, GetWordStatsByChannel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### Channels ###

@app.get('/channels', tags=['GetChannels'])
async def get_channels():
    channels = channelService.get_channels()
    return JSONResponse(content=channels)


@app.get('/channels/{channel_id}/top-words', tags=['GetChannelTopWords'])
async def get_channel_top_words(channel_id, page: int = 1, page_size: int = 30, sort_type: str = 'cont'):
    words = channelService.get_channel_top(channel_id=channel_id, page=page, page_size=page_size, type=sort_type)
    return JSONResponse(content=words)


@app.post('/channels/word-line', tags=['GetWordLine'])
async def get_channel_word_line(req: GetChannelWordLine):
    line = channelService.get_channel_word_line(req.channel_id, req.word)
    return JSONResponse(content=line)


@app.post('/channels/vocabular-comparision', tags=['CompareByVocabular'])
async def compare_by_vocabular(compare: CompareChannels):
    val = channelService.channel_vocabular_compare(compare.channel_left_id, compare.channel_right_id)
    return JSONResponse(content=val)


@app.post('/channels/word-comparision', tags=['CompareByWord'])
async def compare_by_word(compare: CompareChannelsByWord):
    val = channelService.compare_channels_by_word(compare.channel_left_id, compare.channel_right_id, compare.word)
    return JSONResponse(content=val)

### Words ###

@app.get('/all-words', tags=['GetAllWords'])
async def get_all_words():
    words = wordService.get_all_words()
    return JSONResponse(content=words)


@app.get('/words', tags=['GetWords'])
async def get_words(page: int = 1, page_size: int = 30, sort_type: int = 0):
    words = wordService.get_words(page, page_size, sort_type)
    return JSONResponse(content=words)


@app.post('/words/global-line', tags=['GlobalWordLine'])
async def word_stats(req: WordReq):
    res = wordService.get_global_word_line(req.word)
    return JSONResponse(content=res)


@app.post('/words/stats', tags=['WordStats'])
async def word_stats(req: WordReq):
    res = wordService.get_global_word_stats(req.word)
    return JSONResponse(content=res)


@app.post('/words/channel/stats', tags=['WordStatsByChannel'])
async def word_stats_by_channel(req: GetWordStatsByChannel):
    res = channelService.get_channel_word_stats(req.channel_id, req.word)
    return JSONResponse(content=res)
