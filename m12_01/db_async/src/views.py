import aiohttp_jinja2
import aiohttp.web
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models import Note, Tag


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db_session'] as session:
        result = await session.execute(select(Note))
        notes = result.scalars().all()
    return {"notes": notes}


@aiohttp_jinja2.template('tag.html')
async def tag(request):
    return {}


async def create_tag(request):
    data = await request.post()
    async with request.app['db_session'] as session:
        tag = Tag(name=data["name"])
        session.add(tag)
        await session.commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())


@aiohttp_jinja2.template('note.html')
async def note(request):
    async with request.app['db_session'] as session:
        result = await session.execute(select(Tag))
        tags = result.scalars().all()
    return {"tags": tags}


async def create_note(request):
    data = await request.post()
    name = data["name"]
    description = data["description"]
    tags = data.getall("tags")
    async with request.app['db_session'] as session:
        tags_obj = []
        for tag in tags:
            t = await session.execute(select(Tag).filter(Tag.name == tag))
            tags_obj.append(t.scalars().first())

        note = Note(name=name, description=description, tags=tags_obj)
        session.add(note)
        await session.commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())


@aiohttp_jinja2.template('detail.html')
async def detail(request):
    note_id = int(request.match_info.get('note_id'))
    async with request.app['db_session'] as session:
        r = await session.execute(select(Note).filter(Note.id == note_id).options(selectinload(Note.tags)))
        note = r.scalars().first()
    if not note:
        return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())
    return {"note": note}


async def delete_note(request):
    note_id = int(request.match_info.get('note_id'))
    async with request.app['db_session'] as session:
        r = await session.execute(select(Note).filter(Note.id == note_id))
        await session.delete(r.scalars().first())
        await session.commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())


async def done_note(request):
    note_id = int(request.match_info.get('note_id'))
    async with request.app['db_session'] as session:
        r = await session.execute(select(Note).filter(Note.id == note_id))
        note = r.scalars().first()
        note.done = True
        await session.commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())
