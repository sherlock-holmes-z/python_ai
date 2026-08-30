from typing import Annotated

import uvicorn
from fastapi.params import Depends

from fastapi import FastAPI, Query

app = FastAPI()


def comm_page(page: int = Query(1, ge=1, le=100), page_size: int = Query(10)):
    return {"page": page, "page_size": page_size}


CommPageParams = Annotated[dict[str, int], Depends(comm_page)]


@app.get("/get")
def home(page_params: CommPageParams) -> dict:
    print(page_params)
    return page_params


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
