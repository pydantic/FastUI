import asyncio
from itertools import chain
from typing import AsyncIterable

from fastapi import APIRouter
from fastui import FastUI
from fastui import components as c
from starlette.responses import StreamingResponse

router = APIRouter()


async def ai_response_generator() -> AsyncIterable[str]:
    prompt = '**User:** What is SSE? Please include a javascript code example.\n\n**AI:** '
    output = ''
    for time, text in chain([(1.0, prompt)], CANNED_RESPONSE):
        output += text
        m = FastUI(root=[c.Markdown(text=output)])
        yield f'data: {m.model_dump_json(by_alias=True, exclude_none=True)}\n\n'
        await asyncio.sleep(time)

    # avoid the browser reconnecting
    m = FastUI(root=[c.Markdown(text=output)])
    final_response = f'data: {m.model_dump_json(by_alias=True, exclude_none=True)}\n\n'
    while True:
        yield final_response
        await asyncio.sleep(10)


@router.get('/sse')
async def sse_ai_response() -> StreamingResponse:
    return StreamingResponse(ai_response_generator(), media_type='text/event-stream')


async def run_openai():
    from time import perf_counter

    from openai import AsyncOpenAI

    messages = [
        {'role': 'system', 'content': 'please response in markdown only.'},
        {'role': 'user', 'content': 'What is SSE? Please include a javascript code example.'},
    ]
    chunks = await AsyncOpenAI().chat.completions.create(
        model='gpt-4',
        messages=messages,
        stream=True,
    )

    last = None
    result_chunks = []
    async for chunk in chunks:
        now = perf_counter()
        if last is not None:
            t = now - last
        else:
            t = 0
        text = chunk.choices[0].delta.content
        print(repr(text), t)
        if text is not None:
            result_chunks.append((t, text))
        last = now

    print(result_chunks)
    text = ''.join(text for _, text in result_chunks)
    print(text)


if __name__ == '__main__':
    asyncio.run(run_openai())


CANNED_RESPONSE: list[tuple[float, str]] = [
    (0, ''),
    (0.07685, 'Server'),
    (0.00111, '-S'),
    (0.00081, 'ent'),
    (0.10528, ' Events'),
    (0.00109, ' ('),
    (0.00062, 'S'),
    (0.10290, 'SE'),
    (0.00075, ')'),
    (0.00091, ' is'),
    (0.10360, ' a'),
    (0.00089, ' standard'),
    (0.00054, ' that'),
    (0.19121, ' allows'),
    (0.00088, ' web'),
    (0.00067, ' servers'),
    (0.22486, ' to'),
    (0.00101, ' push'),
    (0.00057, ' updates'),
    (0.10352, ' to'),
    (0.00148, ' the'),
    (0.00084, ' client'),
    (0.10238, '-side'),
    (0.00090, '.'),
    (0.00104, ' Unlike'),
    (0.10156, ' WebSocket'),
    (0.00109, ' communication'),
    (0.00063, ','),
    (0.10474, ' SSE'),
    (0.00080, ' is'),
    (0.00085, ' un'),
    (0.10158, 'id'),
    (0.00080, 'irectional'),
    (0.00097, ','),
    (0.10401, ' meaning'),
    (0.00099, ' the'),
    (0.00104, ' updates'),
    (0.11338, ' flow'),
    (0.00078, ' from'),
    (0.00080, ' server'),
    (0.09008, ' to'),
    (0.00072, ' client'),
    (0.00105, ' and'),
    (0.10391, ' not'),
    (0.00084, ' the'),
    (0.00080, ' other'),
    (0.10613, ' way'),
    (0.00110, ' around'),
    (0.00080, '.\n\n'),
    (0.10567, 'S'),
    (0.00076, 'SE'),
    (0.00085, ' is'),
    (0.09538, ' generally'),
    (0.00134, ' used'),
    (0.00052, ' for'),
    (0.10731, ' real'),
    (0.00108, '-time'),
    (0.00079, ' applications'),
    (0.09934, ' where'),
    (0.00065, ' updates'),
    (0.00061, ' from'),
    (0.10913, ' the'),
    (0.00111, ' server'),
    (0.00071, ' are'),
    (0.09556, ' needed'),
    (0.00065, ' periodically'),
    (0.00103, ','),
    (0.10564, ' for'),
    (0.00184, ' example'),
    (0.00077, ','),
    (0.17375, ' live'),
    (0.00067, ' news'),
    (0.00073, ' updates'),
    (0.02926, ','),
    (0.00084, ' real'),
    (0.00052, '-time'),
    (0.10552, ' monitoring'),
    (0.00080, ','),
    (0.00063, ' etc'),
    (0.10336, '.'),
    (0.00087, ' It'),
    (0.00095, ' is'),
    (0.10473, ' based'),
    (0.00100, ' on'),
    (0.00058, ' HTTP'),
    (0.10139, ' protocol'),
    (0.00096, ' and'),
    (0.00049, ' provides'),
    (0.14795, ' a'),
    (0.00073, ' simpler'),
    (0.00088, ' alternative'),
    (0.10304, ' to'),
    (0.00092, ' Web'),
    (0.00055, 'S'),
    (0.10849, 'ockets'),
    (0.00076, ' for'),
    (0.00096, ' use'),
    (0.09727, ' cases'),
    (0.00087, ' where'),
    (0.00080, ' you'),
    (0.11029, ' do'),
    (0.00060, ' not'),
    (0.00046, ' require'),
    (0.12591, ' bid'),
    (0.00084, 'irectional'),
    (0.00064, ' communication'),
    (0.07139, '.\n\n'),
    (0.00082, '**'),
    (0.00064, 'JavaScript'),
    (0.10693, ' Example'),
    (0.00078, '**\n\n'),
    (0.00064, '```'),
    (0.14820, 'javascript'),
    (0.00102, '\n'),
    (0.00066, 'let'),
    (0.10841, ' event'),
    (0.00073, 'Source'),
    (0.00112, ' ='),
    (0.09982, ' new'),
    (0.00171, ' Event'),
    (0.00087, 'Source'),
    (0.10119, '("'),
    (0.00129, 'https'),
    (0.00078, '://'),
    (0.10253, 'api'),
    (0.00080, '.example'),
    (0.00086, '.com'),
    (0.10223, '/stream'),
    (0.00069, '");\n\n'),
    (0.00051, 'event'),
    (0.10391, 'Source'),
    (0.00082, '.on'),
    (0.00090, 'message'),
    (0.10570, ' ='),
    (0.00286, ' function'),
    (0.00061, '(event'),
    (0.08790, ')'),
    (0.00098, ' {\n'),
    (0.00058, '   '),
    (0.09117, ' console'),
    (0.00061, '.log'),
    (0.00118, '("'),
    (0.14843, 'New'),
    (0.00085, ' event'),
    (0.00054, ' received'),
    (0.09681, ':'),
    (0.00078, ' ",'),
    (0.00092, ' event'),
    (0.09540, '.data'),
    (0.00075, ');\n'),
    (0.00077, '};\n\n'),
    (0.10102, 'event'),
    (0.00096, 'Source'),
    (0.00058, '.onerror'),
    (0.09409, ' ='),
    (0.00088, ' function'),
    (0.00063, '(err'),
    (0.10187, ')'),
    (0.00080, ' {\n'),
    (0.00062, '   '),
    (0.10227, ' console'),
    (0.00098, '.error'),
    (0.00062, '("'),
    (0.09445, 'Event'),
    (0.00103, 'Source'),
    (0.00080, ' failed'),
    (0.10366, ':",'),
    (0.00073, ' err'),
    (0.00101, ');\n'),
    (0.09442, '};\n'),
    (0.00088, '``'),
    (0.00051, '`\n\n'),
    (0.10121, 'Here'),
    (0.00156, ','),
    (0.00077, ' `'),
    (0.09582, 'https'),
    (0.00072, '://'),
    (0.00083, 'api'),
    (0.09987, '.example'),
    (0.00082, '.com'),
    (0.00088, '/stream'),
    (0.10323, '`'),
    (0.00070, ' is'),
    (0.00075, ' the'),
    (0.09308, ' endpoint'),
    (0.00118, ' which'),
    (0.00080, ' sends'),
    (0.10005, ' the'),
    (0.00091, ' updates'),
    (0.00091, '.\n\n'),
    (0.09656, '**'),
    (0.00272, 'Fast'),
    (0.00068, 'API'),
    (0.10638, ' Example'),
    (0.00069, '**\n\n'),
    (0.00068, '```'),
    (0.09220, 'python'),
    (0.00068, '\n'),
    (0.00102, 'from'),
    (0.16155, ' fast'),
    (0.00082, 'api'),
    (0.00054, ' import'),
    (0.09223, ' Fast'),
    (0.00075, 'API'),
    (0.00064, '\n'),
    (0.09892, 'from'),
    (0.00071, ' fast'),
    (0.00051, 'api'),
    (0.00075, '.responses'),
    (0.00071, ' import'),
    (0.00058, ' Streaming'),
    (0.00081, 'Response'),
    (0.00052, '\n\n'),
    (0.10306, 'app'),
    (0.00075, ' ='),
    (0.00088, ' Fast'),
    (0.09503, 'API'),
    (0.00260, '()\n\n'),
    (0.00054, 'def'),
    (0.09160, ' event'),
    (0.00075, '_generator'),
    (0.00067, '():\n'),
    (0.09801, '   '),
    (0.00080, ' yield'),
    (0.00086, " {'"),
    (0.07686, 'data'),
    (0.00125, "':"),
    (0.00087, " '"),
    (0.08182, 'Initial'),
    (0.00086, ' message'),
    (0.00052, "'}\n"),
    (0.16532, '   '),
    (0.00114, ' for'),
    (0.00058, ' i'),
    (0.10338, ' in'),
    (0.00080, ' range'),
    (0.00082, '('),
    (0.10311, '5'),
    (0.00075, '):\n'),
    (0.00066, '       '),
    (0.09347, ' yield'),
    (0.00080, " {'"),
    (0.00060, 'data'),
    (0.10470, "':"),
    (0.00077, ' f'),
    (0.00052, "'M"),
    (0.10310, 'essage'),
    (0.00070, ' {'),
    (0.00103, 'i'),
    (0.09362, "}'"),
    (0.00091, '}\n\n'),
    (0.00068, '@app'),
    (0.09475, '.get'),
    (0.00078, '("/'),
    (0.00078, 'stream'),
    (0.08145, '")\n'),
    (0.00064, 'async'),
    (0.00067, ' def'),
    (0.08127, ' get'),
    (0.00141, '_event'),
    (0.00049, '_stream'),
    (0.08973, '():\n'),
    (0.00095, '   '),
    (0.00089, ' return'),
    (0.07297, ' Streaming'),
    (0.00092, 'Response'),
    (0.19895, '(event'),
    (0.00075, '_generator'),
    (0.00049, '(),'),
    (0.00092, ' media_type'),
    (0.00066, '='),
    (0.00052, "'text/"),
    (0.00073, "event-stream'"),
    (0.00050, ')\n'),
    (0.07387, '``'),
    (0.00066, '`\n\n'),
    (0.00054, 'In'),
    (0.08289, ' the'),
    (0.00088, ' Fast'),
    (0.00093, 'API'),
    (0.14361, ' example'),
    (0.00087, ','),
    (0.00060, ' the'),
    (0.01910, ' client'),
    (0.00074, ' would'),
    (0.00059, ' receive'),
    (0.08010, ' an'),
    (0.00232, ' event'),
    (0.00059, ' with'),
    (0.07788, " '"),
    (0.00101, 'Initial'),
    (0.00061, ' message'),
    (0.50112, "',"),
    (0.00061, ' followed'),
    (0.00049, ' by'),
    (0.05819, " '"),
    (0.00072, 'Message'),
    (0.00060, ' '),
    (0.11164, '0'),
    (0.00075, "',"),
    (0.00096, " '"),
    (0.10626, 'Message'),
    (0.00081, ' '),
    (0.00051, '1'),
    (0.11977, "',"),
    (0.00071, ' ...,'),
    (0.00051, " '"),
    (0.11939, 'Message'),
    (0.00081, ' '),
    (0.00059, '4'),
    (0.11833, "'."),
    (0.00059, ' Each'),
    (0.00025, ' message'),
    (0.11457, ' is'),
    (0.00063, ' an'),
    (0.00058, ' individual'),
    (0.11788, ' Server'),
    (0.00084, '-S'),
    (0.00037, 'ent'),
    (0.00046, ' Event'),
    (0.00026, '.'),
]
