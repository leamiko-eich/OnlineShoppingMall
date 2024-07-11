from pydantic import BaseModel, Field
from typing import Optional


"""
========================================
产品分类 数据的验证和序列化
========================================
"""


class ProdCagBase(BaseModel):
    name: str
    sort: int
    state: bool


class ProdCagCreate(ProdCagBase):
    name: str = "test"
    sort: int = 50
    state: bool = True


class ProdCagUpdate(BaseModel):
    id: int = 1
    name: Optional[str] = Field(default="测试分类")
    sort: Optional[int] = Field(default=None)
    state: Optional[bool] = Field(default=None)


class ProdCagResponse(ProdCagBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class ProdCagDelete(BaseModel):
    id: int


"""
========================================
产品信息 数据的验证和序列化
========================================
"""


class ProdInfoBase(BaseModel):
    name: str  # 必填
    prod_price: float  # 必填
    auto: bool  # 必填
    state: bool  # 必填


class ProdInfoCreate(ProdInfoBase):
    prod_cag_name: Optional[str] = Field(None, description="产品分类名称")
    prod_info: Optional[str] = Field(None, description="产品信息")
    prod_img_url: Optional[str] = Field(None, description="产品图片url")
    prod_discription: Optional[str] = Field(None, description="产品描述")
    prod_price_wholesale: Optional[str] = Field(None, description="产品批发价格")
    prod_sales: Optional[int] = Field(None, description="产品销量")
    prod_tag: Optional[str] = Field(None, description="产品标签")
    sort: Optional[int] = Field(None, description="排序")


class ProdInfoUpdate(BaseModel):
    id: int = 1  # 必填
    name: Optional[str] = Field(None, description="产品名称")
    prod_cag_name: Optional[str] = Field(None, description="产品分类名称")
    prod_info: Optional[str] = Field(None, description="产品信息")
    prod_img_url: Optional[str] = Field(None, description="产品图片url")
    prod_discription: Optional[str] = Field(None, description="产品描述")
    prod_price: Optional[float] = Field(None, description="产品价格")
    prod_price_wholesale: Optional[str] = Field(None, description="产品批发价格")
    prod_sales: Optional[int] = Field(None, description="产品销量")
    prod_tag: Optional[str] = Field(None, description="产品标签")
    auto: Optional[bool] = Field(None, description="是否自动上架")
    sort: Optional[int] = Field(None, description="排序")
    state: Optional[bool] = Field(None, description="是否上架")


class ProdInfoResponse(ProdInfoBase):
    id: int
    prod_cag_name: Optional[str] = None
    prod_info: Optional[str] = None
    prod_img_url: Optional[str] = None
    prod_discription: Optional[str] = None
    prod_price_wholesale: Optional[str] = None
    prod_sales: Optional[int] = None
    prod_tag: Optional[str] = None
    sort: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True


class ProdInfoDelete(BaseModel):
    id: int  # 必填
