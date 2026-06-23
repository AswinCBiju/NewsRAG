from database import save_article

article_id = save_article(
    "Test",
    "Me",
    "http://test.com",
    "2026-06-23",
    "Hello world"
)

print(article_id)