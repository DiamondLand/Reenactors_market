import asyncio
import asyncpg
import configparser

config = configparser.ConfigParser()
config.read("configs/config.ini")

async def main():
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute("DROP TABLE IF EXISTS buyers")
            await connection.execute("DROP TABLE IF EXISTS products")
            await connection.execute("DROP TABLE IF EXISTS orders")
            await connection.execute("DROP TABLE IF EXISTS staff")

            await connection.execute(
                """
                CREATE TABLE buyers (
                    user_id BIGINT UNIQUE,
                    username VARCHAR(50),
                    purchased INTEGER
                )
                """
            )

            await connection.execute(
                """
                CREATE TABLE products (
                    product_id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    description VARCHAR(100),
                    price INTEGER,
                    amount INTEGER,
                    category VARCHAR(50),
                    subcategory VARCHAR(50),
                    subsubcategory VARCHAR(50),
                    image_url VARCHAR,
                    company_name VARCHAR(50),
                    moderation BOOLEAN,
                    moderation_comment VARCHAR(50)
                )
                """
            )

            await connection.execute(
                """
                CREATE TABLE orders (
                    order_id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    company_name VARCHAR(50),
                    price INTEGER,
                    username VARCHAR(50),
                    order_date DATE,
                    order_status BOOLEAN
                )
                """
            )

            await connection.execute(
                """
                CREATE TABLE staff (
                    user_id BIGINT UNIQUE,
                    username VARCHAR(50),
                    company_name VARCHAR(50),
                    phone VARCHAR(15),
                    sold INTEGER,
                    post VARCHAR(50)
                )
                """
            )

async def create_db_pool():
    try:
        pool = await asyncpg.create_pool(
            host=config["DATABASE"]["host"],
            port=config["DATABASE"]["port"],
            user=config["DATABASE"]["user"],
            password=config["DATABASE"]["password"],
            database=config["DATABASE"]["database"]
        )
        return pool
    except asyncpg.PostgresError as _ex:
        print("Ошибка при подключении к базе данных: ", _ex)
        return None

if __name__ == "__main__":
    asyncio.run(main())
