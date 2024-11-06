# app/utils/id_converter.py

from typing import Union
import uuid


def validate_and_convert_product_id(product_id: Union[str, uuid.UUID]) -> str:
    return str(product_id) if isinstance(product_id, uuid.UUID) else product_id
