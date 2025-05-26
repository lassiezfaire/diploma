from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.search_indexes import (
    HybridSearchIndexType,
    TextSearchIndexType,
    StaticIndexChunkingStrategy,
    ReciprocalRankFusionIndexCombinationStrategy,
)

from app.configs.config import settings

query = (
    "Сгенерируй JSON дашборд для Grafana HTTP API с единственной панелью, отображающей загрузку оперативной памяти "
    "Linux-сервера."
)
instruction = """Ты высококвалифицированный специалист по Grafana. Твоя задача помогать системному администратору 
генерировать JSON дашборды для Grafana HTTP API. На вход тебе будут даны несколько JSON дашбордов, на основе данных 
дашбордов нужно составить ответ на запрос системного администратора. PromQL queries бери из предоставленных дашбордов.
В ответ давай дашборд, отвечай только в JSON-формате. Не забывай про ключ Dashboard и про обязательные поля.
"""


def main():
    sdk = YCloudML(
        folder_id=settings.folder_id,
        auth=settings.yc_api_key,
    )

    target_dashboard = sdk.files.upload("Target dashboard-1748287715219.json")

    operation = sdk.search_indexes.create_deferred(
        [target_dashboard],
        index_type=HybridSearchIndexType(
            chunking_strategy=StaticIndexChunkingStrategy(
                max_chunk_size_tokens=1024,
                chunk_overlap_tokens=512,
            ),
            combination_strategy=ReciprocalRankFusionIndexCombinationStrategy(),
        ),
    )
    hybrid_index = operation.wait()
    hybrid_tool = sdk.tools.search_index(hybrid_index)
    model = sdk.models.completions("yandexgpt", model_version="rc")
    model = model.configure(temperature=0.1)
    assistant = sdk.assistants.create(
        model, tools=[hybrid_tool], instruction=instruction
    )
    hybrid_index_thread = sdk.threads.create()

    hybrid_index_thread.write(query)
    print(query)
    run = assistant.run(hybrid_index_thread)
    result = run.wait().message
    for part in result.parts:
        print(part)
    print("\n")


if __name__ == "__main__":
    main()