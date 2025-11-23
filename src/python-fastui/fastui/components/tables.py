import typing as _t

import pydantic
import typing_extensions as _te
from pydantic_core import core_schema as _core_schema

from .. import class_name as _class_name
from .. import types as _types
from ..base import BaseModel
from . import display

# TODO allow dataclasses and typed dicts here too


# In Python 3.14, when evaluating the annotation of field `data_model`, `type` would refer
# to the assigned value to the field `type` (of value `'Table'`):
type_ = type


class Table(BaseModel, extra='forbid'):
    """Table component."""

    data: pydantic.SkipValidation[_t.Sequence[pydantic.SerializeAsAny[_types.DataModel]]]
    """Sequence of data models to display in the table."""

    columns: list[display.DisplayLookup] | None = None
    """List of columns to display in the table. If not provided, columns will be inferred from the data model."""

    data_model: _t.Any = pydantic.Field(default=None, exclude=True)
    """Data model to use for the table. If not provided, the model will be inferred from the first data item."""

    no_data_message: str | None = None
    """Message to display when there is no data."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the paragraph's HTML component."""

    type: _t.Literal['Table'] = 'Table'
    """The type of the component. Always 'Table'."""

    @pydantic.model_validator(mode='after')
    def _fill_columns(self) -> _te.Self:
        if self.data_model:
            data_model_type = self.data_model
        else:
            try:
                data_model_type = type(self.data[0])
            except IndexError:
                raise ValueError('Cannot infer model from empty data, please set `Table(..., model=MyModel)`')

        if self.columns is None:
            self.columns = []
            # use TypeAdapter to get the json schema for the model, then extract properties
            # this works for pydantic models, dataclasses and typed dicts
            # mode='serialization' is needed to include computed fields
            json_schema = pydantic.TypeAdapter(data_model_type).json_schema(mode='serialization')
            # if the model is a reference, we need to look it up in $defs
            if '$ref' in json_schema:
                ref = json_schema['$ref'].split('/')[-1]
                properties = json_schema.get('$defs', {}).get(ref, {}).get('properties', {})
            else:
                properties = json_schema.get('properties', {})

            for name, prop in properties.items():
                title = prop.get('title')
                # If it's a Pydantic model, we only want to use the title if it was explicitly set
                # otherwise we let the frontend decide (or use the field name)
                # TypeAdapter generates titles automatically (e.g. 'id' -> 'Id'), which we don't want for Pydantic models
                # to maintain backward compatibility
                if isinstance(data_model_type, type) and issubclass(data_model_type, pydantic.BaseModel):
                    field = data_model_type.model_fields.get(name)
                    if field:
                        if field.title is None:
                            title = None
                    else:
                        # check computed fields
                        computed = data_model_type.model_computed_fields.get(name)
                        if computed:
                            if computed.title is None:
                                title = None
                
                self.columns.append(display.DisplayLookup(field=name, title=title))
        else:
            # add pydantic titles to columns that don't have them
            # for pydantic models, we can use model_fields to get the title
            # but for dataclasses and typed dicts, we need to use the json schema
            # so we just use the json schema for everything
            json_schema = pydantic.TypeAdapter(data_model_type).json_schema(mode='serialization')
            if '$ref' in json_schema:
                ref = json_schema['$ref'].split('/')[-1]
                properties = json_schema.get('$defs', {}).get(ref, {}).get('properties', {})
            else:
                properties = json_schema.get('properties', {})

            for column in (c for c in self.columns if c.title is None):
                prop = properties.get(column.field)
                if prop and 'title' in prop:
                    # Same logic for existing columns: only use title if explicit for BaseModel
                    if isinstance(data_model_type, type) and issubclass(data_model_type, pydantic.BaseModel):
                        field = data_model_type.model_fields.get(column.field)
                        if field:
                            if field.title is None:
                                continue
                        else:
                            computed = data_model_type.model_computed_fields.get(column.field)
                            if computed:
                                if computed.title is None:
                                    continue
                    column.title = prop['title']
        return self

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: _core_schema.CoreSchema, handler: pydantic.GetJsonSchemaHandler
    ) -> _t.Any:
        json_schema = handler(core_schema)
        schema_def = handler.resolve_ref_schema(json_schema)
        # columns are filled by `_fill_columns`
        schema_def['required'].append('columns')
        return json_schema


class Pagination(BaseModel):
    """Pagination component to use with tables."""

    page: int
    """The current page number."""

    page_size: int
    """The number of items per page."""

    total: int
    """The total number of items."""

    page_query_param: str = 'page'
    """The query parameter to use for the page number."""

    class_name: _class_name.ClassNameField = None
    """Optional class name to apply to the pagination's HTML component."""

    type: _t.Literal['Pagination'] = 'Pagination'
    """The type of the component. Always 'Pagination'."""

    @pydantic.computed_field(alias='pageCount')
    def page_count(self) -> int:
        return (self.total - 1) // self.page_size + 1
