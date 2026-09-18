from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="文档管理 API",
    description="FastAPI 基础学习项目",
    version="1.0.0",
)


# 创建文档时，客户端需要提交的数据
class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


# 修改文档时，所有字段都可以不传
class DocumentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)


# 返回给客户端的完整数据
class Document(BaseModel):
    id: int
    title: str
    content: str


# 暂时用字典模拟数据库
documents: dict[int, Document] = {}
next_id = 1

#POST：创建文档
@app.post(
    "/documents",
    response_model=Document,
    status_code=status.HTTP_201_CREATED,
)
def create_document(data: DocumentCreate):
    global next_id

    document = Document(
        id=next_id,
        title=data.title,
        content=data.content,
    )

    documents[next_id] = document
    next_id += 1

    return document


#GET：查询全部文档
@app.get("/documents", response_model=list[Document])
def list_documents(keyword: str | None = None):
    result = list(documents.values())

    if keyword:
        result = [
            document
            for document in result
            if keyword.lower() in document.title.lower()
        ]

    return result

#GET：根据 ID 查询文档
@app.get("/documents/{document_id}", response_model=Document)
def get_document(document_id: int):
    document = documents.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文档不存在",
        )

    return document


#PUT：修改文档
@app.put("/documents/{document_id}", response_model=Document)
def update_document(
    document_id: int,
    data: DocumentUpdate,
):
    document = documents.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文档不存在",
        )

    update_data = data.model_dump(exclude_unset=True)
    updated_document = document.model_copy(update=update_data)

    documents[document_id] = updated_document

    return updated_document

#DELETE：删除文档
@app.delete(
    "/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(document_id: int):
    if document_id not in documents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文档不存在",
        )

    del documents[document_id]

    return Response(status_code=status.HTTP_204_NO_CONTENT)