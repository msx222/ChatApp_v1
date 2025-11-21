from collections import defaultdict
from langchain_core.documents import Document


def dummy_search_law(query: str):
    docs = [
        Document(
            page_content="前照灯は白色の光を発すること。",
            metadata={"article": "第32条", "article_title": "前照灯", "clause": "第1項",
                      "page": 10, "pdf_url": "https://example.com/32.pdf"}
        ),
        Document(
            page_content="前照灯の光度は10000cd以上であること。",
            metadata={"article": "第32条", "article_title": "前照灯", "clause": "第2項",
                      "page": 11, "pdf_url": "https://example.com/32.pdf"}
        ),
    ]
    return docs


def group_by_article(docs):
    grouped = defaultdict(lambda: defaultdict(list))
    titles = {}
    pdf_urls = {}

    for doc in docs:
        md = doc.metadata
        art = md["article"]
        clause = md["clause"]
        grouped[art][clause].append(doc)
        titles[art] = md["article_title"]
        pdf_urls[art] = md.get("pdf_url")

    result = []
    for art, clauses in grouped.items():
        result.append({
            "article": art,
            "title": titles[art],
            "pdf_url": pdf_urls.get(art),
            "clauses": [
                {"clause": cl, "chunks": chunk_list}
                for cl, chunk_list in clauses.items()
            ],
        })

    return result
