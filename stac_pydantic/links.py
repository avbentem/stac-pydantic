from enum import auto
from typing import Any, Dict, Iterator, List, Optional, Union
from urllib.parse import urljoin

from pydantic import BaseModel, Field

from stac_pydantic.utils import AutoValueEnum


class PaginationMethods(str, AutoValueEnum):
    """
    https://github.com/radiantearth/stac-api-spec/blob/master/api-spec.md#paging-extension
    """

    GET = auto()
    POST = auto()


class PaginationRelations(str, AutoValueEnum):
    """
    https://github.com/radiantearth/stac-api-spec/blob/master/api-spec.md#paging-extension
    """

    next = auto()
    previous = auto()


class Link(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0/collection-spec/collection-spec.md#link-object
    """

    href: str = Field(..., alias="href", min_length=1)
    rel: str = Field(..., alias="rel", min_length=1)
    type: Optional[str]
    title: Optional[str]
    # Label extension
    label: Optional[str] = Field(None, alias="label:assets")

    class Config:
        use_enum_values = True

    def resolve(self, base_url: str) -> None:
        """resolve a link to the given base URL"""
        self.href = urljoin(base_url, self.href)


class PaginationLink(Link):
    """
    https://github.com/radiantearth/stac-api-spec/blob/master/api-spec.md#paging-extension
    """

    rel: PaginationRelations
    method: PaginationMethods
    body: Optional[Dict[Any, Any]]
    merge: bool = False


class Links(BaseModel):
    __root__: List[Union[PaginationLink, Link]]

    def link_iterator(self) -> Iterator[Link]:
        """Produce iterator to iterate through links"""
        return iter(self.__root__)

    def resolve(self, base_url: str) -> None:
        """resolve all links to the given base URL"""
        for link in self.link_iterator():
            link.resolve(base_url)

    def append(self, link: Link) -> None:
        self.__root__.append(link)

    def __len__(self) -> int:
        return len(self.__root__)

    def __getitem__(self, idx: int) -> Union[PaginationLink, Link]:
        return self.__root__[idx]


class Relations(str, AutoValueEnum):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0/collection-spec/collection-spec.md#relation-types
    """

    self = auto()
    root = auto()
    parent = auto()
    child = auto()
    children = auto()
    item = auto()
    license = auto()
    derived_from = auto()
    collection = auto()
    alternate = auto()
    previous = auto()
    next = auto()
    conformance = auto()
    docs = auto()
    tiles = auto()
    search = auto()
    preview = auto()
    canonical = auto()
    service_desc = "service-desc"
    service_doc = "service-doc"
    queryables = "http://www.opengis.net/def/rel/ogc/1.0/queryables"
