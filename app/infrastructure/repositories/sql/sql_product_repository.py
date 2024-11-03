# # app/infrastructure/repositories/sql/sql_product_repository.py
#
# from typing import List, Optional
# from sqlalchemy.orm import Session
# from domain.entities.product import Product
# from application.interfaces.product_repository_interface import ProductRepositoryInterface
# from domain.exceptions.product_exceptions import ProductNotFoundException
# from infrastructure.database.models import ProductModel
# from domain.values.price import Price
# from domain.values.quantity import Quantity
# from domain.values.discount import Discount
#
# class SQLProductRepository(ProductRepositoryInterface):
#     def __init__(self, session: Session):
#         self.session = session
#
#     def add(self, product: Product) -> Product:
#         product_model = ProductModel(
#             oid=product.oid,
#             name=product.name,
#             category_id=product.category_id,
#             price=product.price.value,
#             stock=product.stock.value,
#             discount=product.discount.value if product.discount else 0.0,
#             created_at=product.created_at
#         )
#         self.session.add(product_model)
#         self.session.commit()
#         return product
#
#     def get_by_id(self, product_id: str) -> Optional[Product]:
#         product_model = self.session.query(ProductModel).filter_by(oid=product_id).first()
#         if not product_model:
#             raise ProductNotFoundException(product_id=product_id)
#         return self._model_to_entity(product_model)
#
#     def update(self, product: Product) -> Product:
#         product_model = self.session.query(ProductModel).filter_by(oid=product.oid).first()
#         if not product_model:
#             raise ProductNotFoundException(product_id=product.oid)
#         product_model.name = product.name
#         product_model.category_id = product.category_id
#         product_model.price = product.price.value
#         product_model.stock = product.stock.value
#         product_model.discount = product.discount.value if product.discount else 0.0
#         self.session.commit()
#         return product
#
#     def delete(self, product_id: str) -> None:
#         product_model = self.session.query(ProductModel).filter_by(oid=product_id).first()
#         if not product_model:
#             raise ProductNotFoundException(product_id=product_id)
#         self.session.delete(product_model)
#         self.session.commit()
#
#     def get_all(self) -> List[Product]:
#         product_models = self.session.query(ProductModel).all()
#         return [self._model_to_entity(pm) for pm in product_models]
#
#     def _model_to_entity(self, model: ProductModel) -> Product:
#         return Product(
#             oid=model.oid,
#             name=model.name,
#             category_id=model.category_id,
#             price=Price(model.price),
#             stock=Quantity(model.stock),
#             discount=Discount(model.discount) if model.discount else None,
#             created_at=model.created_at
#         )
