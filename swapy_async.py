'https://swapi.dev/people/1'
import aiohttp
import asyncio

import asyncpg
from more_itertools import chunked
import time
import config


async def get_person(session: aiohttp, person_id: int) -> dict:
    async with session.get(f'https://swapi.dev/api/people/{person_id}') as resp:
        return await resp.json()


def gen_data(persons):
    for i in range(len(persons)):
        yield (
            list(persons[i].values())
        )


async def insert_users(pool: asyncpg.Pool, data):
    query = f'INSERT INTO persons_starwars (name, height, mass, hair_color, skin_color, eye_color, birth_year, gender,'\
            f' homeworld, films, species, vehicles, starships, created, edited, url)' \
            f' VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)'
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(query, data)


async def main():
    start = time.time()
    pool = await asyncpg.create_pool(config.PG_DSN, min_size=20, max_size=20)
    async with aiohttp.ClientSession() as session:
        for chunk in chunked(range(1, 84), 15):
            person_coroutine_list = [get_person(session, i) for i in chunk]
            # person_coroutine_list = []
            # for i in chunk:
            #     person_coroutine = get_person(session, i)
            #     person_coroutine_list.append(person_coroutine)
            persons = await asyncio.gather(*person_coroutine_list)
            # print(persons)
            # print(len(persons))
            for i in range(len(persons)):
                for k, v in persons[i].items():
                    if type(v) == list:
                        persons[i][k] = ', '.join(v)
            print('\n persons  -----  ', persons)
            data = gen_data(persons)
            # print(data)
            tasks = [asyncio.create_task(insert_users(pool, data))]
            print(len(persons))
        await asyncio.gather(*tasks)
        await pool.close()
        # print()

    print('Время работы: ', time.time() - start)


if __name__ == '__main__':
    asyncio.run(main())


