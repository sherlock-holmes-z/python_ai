"""Path 路径参数验证示例。

启动后访问 http://127.0.0.1:8000/docs，可直接在 Swagger UI 中测试。
路径参数必须出现在路由路径中，且不能设置默认值，因此它始终是必填参数。
验证失败时，FastAPI 会自动返回 422 Unprocessable Entity。
"""

from enum import StrEnum
from typing import Annotated
from uuid import UUID

import uvicorn
from pydantic import AfterValidator

from fastapi import FastAPI, Path

app = FastAPI()


# 1. 自动类型转换：/orders/100 会转换为 int；/orders/abc 会验证失败
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return {"order_id": order_id, "type": type(order_id).__name__}


# 2. 数值范围：gt、ge、lt、le 与 multiple_of
# /products/10
@app.get("/products/{product_id}")
def get_product(
    product_id: Annotated[
        int,
        Path(gt=0, le=1000, multiple_of=5, description="1~1000 的正整数，且为 5 的倍数"),
    ],
):
    return {"product_id": product_id}


# 3. 字符串验证：min_length、max_length 与 pattern（正则表达式）
# /articles/fastapi-path-demo
@app.get("/articles/{slug}")
def get_article(
    slug: Annotated[
        str,
        Path(
            min_length=3,
            max_length=50,
            pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
            description="3~50 位小写 slug，只能使用小写字母、数字和连字符",
        ),
    ],
):
    return {"slug": slug}


# 4. 枚举验证：只能匹配已定义的路径值，model_name只能传以下三个值
class ModelName(StrEnum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# /models/resnet；/models/other 会验证失败
@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    return {"model_name": model_name, "value": model_name.value}


# 5. UUID 验证：/users/123e4567-e89b-12d3-a456-426614174000
@app.get("/users/{user_id}")
def get_user(user_id: UUID):
    return {"user_id": user_id}


# 创建自定义的验证别名
def validate(value):
    if value.startswith("@"):
        raise ValueError("不能以@开头")
    return value


# 输入格式有问题或需要转换 → BeforeValidator,可以接受入参还未转换的原始数据，比如'123'还未转换成123
# 类型没问题，但不符合业务规则 → AfterValidator，这里只能接受符合类型的数据123
my_validate = Annotated[str, AfterValidator(validate)]


@app.get("/start_with/{user_name}")
def start_with(user_name: my_validate):
    return {"user_name": user_name}


if __name__ == "__main__":
    uvicorn.run("06_Path请求方式:app", host="127.0.0.1", port=8000, reload=True)
