import asyncio
import httpx
from app.configs.yandex_config import settings
import logging

api_url = 'https://rest-assistant.api.cloud.yandex.net/assistants/v1'


async def _delete_assistant(assistant_id: str):
    """Удаление ассистента через REST API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{api_url}/assistants/{assistant_id}",
                params={"assistantId": assistant_id},
                headers={"Authorization": f"Api-Key {settings.yc_api_key}"}
            )
            response.raise_for_status()

            logging.info(f"Successfully deleted search assistant {assistant_id}")
            print(f"\nУспех! Ассистент {assistant_id} был полностью удалён с сервера Yandex Cloud")

            return True

    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to delete assistant {assistant_id}:")
        logging.error(f"Status code: {e.response.status_code}")
        logging.error(f"Response: {e.response.text}")
    except Exception as e:
        logging.error(f"Unknown error while deleting assistant {assistant_id}: {str(e)}")

    return False


async def _delete_thread(thread_id: str):
    """Удаление треда через REST API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{api_url}/threads/{thread_id}",
                params={"threadId": thread_id},
                headers={"Authorization": f"Api-Key {settings.yc_api_key}"}
            )

            logging.info(f"Successfully deleted thread {thread_id}")
            print(f"\nУспех! Тред {thread_id} был полностью удалён с сервера Yandex Cloud")

            return True

    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to delete thread {thread_id}:")
        logging.error(f"Status code: {e.response.status_code}")
        logging.error(f"Response: {e.response.text}")
    except Exception as e:
        logging.error(f"Unknown error while deleting thread {thread_id}: {str(e)}")

    return False


async def _delete_search_index(search_index_id: str):
    """Удаление поискового индекса через REST API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{api_url}/searchIndex/{search_index_id}",
                params={"searchIndexId": search_index_id},
                headers={"Authorization": f"Api-Key {settings.yc_api_key}"}
            )
            response.raise_for_status()

            logging.info(f"Successfully search index {search_index_id}")
            print(f"\nУспех! Поисковой индекс {search_index_id} был полностью удалён с сервера Yandex Cloud")

            return True

    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to delete search index {search_index_id}:")
        logging.error(f"Status code: {e.response.status_code}")
        logging.error(f"Response: {e.response.text}")
    except Exception as e:
        logging.error(f"Unknown error while deleting search index {search_index_id}: {str(e)}")

    return False


async def main():
    # assistant_id = 'fvt05b6v04k55ijcn7gk'
    # await _delete_assistant(assistant_id)

    # thread_id = 'fvtl35ti9358nie7dcqs'
    # await _delete_thread(thread_id)

    # search_index_id = 'fvt485cpv7dts0hllcvf'
    # await _delete_search_index(search_index_id)

    


if __name__ == "__main__":
    asyncio.run(main())
