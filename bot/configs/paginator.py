import aioredis

'''
# Функция для установки соединения с Redis
async def connect_to_redis():
    return await aioredis.create_redis_pool('redis://localhost')


# Установка начального значения индекса вопроса
async def set_initial_question_index(user_id, redis):
    await redis.hset('current_question_index', user_id, 0)

# Получение текущего вопроса по индексу
async def get_current_question_index(user_id, redis):
    return int(await redis.hget('current_question_index', user_id, encoding='utf-8'))

# Увеличение индекса вопроса
async def increment_question_index(user_id, redis):
    current_index = await get_current_question_index(user_id, redis)
    await redis.hset('current_question_index', user_id, current_index + 1)
'''
