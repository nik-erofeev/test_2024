from uuid import UUID

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: UUID

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)


class ProductQueryParams(ProductUpdate):
    pass


class ProductUpdateResponse(BaseModel):
    product_id: UUID
    message: str


class ProductDeleteResponse(BaseModel):
    id: UUID
    message: str
