"""Ecommerce modeling with attrs example."""

from __future__ import annotations

from datetime import date
from typing import TypeVar

from attrs import define, field, validators

Attribute = TypeVar("Attribute", bound=str)


def positive_number(
    instance: Product, attribute: Attribute, value: int | float
) -> None:
    """Custom check whether an attribute of an instance has a positive value assingned."""
    class_name = instance.__class__.__name__
    if value <= 0:
        raise ValueError(
            f"{class_name} {attribute.name} attribute must be greater then zero."
        )


def percentage_value(instance: Product, attribute: str, value: float) -> None:
    """Custom check whether an attribute of an instance has a percentage assigned."""
    class_name = instance.__class__.__name__
    if not 0 < value < 1:
        raise ValueError(
            f"{class_name} {attribute.name} attribute must be between 0 and 1."
        )


@define
class Product:
    """Product in ecommerce chart."""

    name: str = field(eq=str.lower)
    category: str = field(eq=str.lower)
    shipping_weight: float = field(
        validator=[validators.instance_of(float), positive_number], eq=False
    )
    unit_price: int = field(
        validator=[validators.instance_of(int), positive_number], eq=False
    )
    tax_percent: float = field(
        validator=[validators.instance_of(float), percentage_value], eq=False
    )


@define(kw_only=True)
class Order:
    """Order in ecommerce website."""

    status: str
    creation_date: date = date.today()
    products: list[Product] = field(factory=list)

    def add_item(self, product: Product) -> None:
        """Insert one product into order."""
        self.products.append(product)

    def calculate_sub_total(self) -> int:
        """Total order price without taxes."""
        return sum((p.unit_price for p in self.products))

    def calculate_tax(self) -> float:
        """Total paid in taxes."""
        return sum((p.unit_price * p.tax_percent for p in self.products))

    def calculate_total(self) -> float:
        """Total order price considering taxes."""
        return self.calculate_sub_total() + self.calculate_tax()

    @property
    def total_weight(self) -> float:
        """Total weight of order."""
        return sum((p.shipping_weight for p in self.products))


def main() -> None:
    banana = Product(
        name="banana",
        category="fruit",
        shipping_weight=0.5,
        unit_price=215,
        tax_percent=0.07,
    )

    mango = Product(
        name="mango",
        category="fruit",
        shipping_weight=2.0,
        unit_price=319,
        tax_percent=0.11,
    )

    expensive_mango = Product(
        name="Mango",
        category="Fruit",
        shipping_weight=4.0,
        unit_price=800,
        tax_percent=0.20,
    )

    order = Order(creation_date=date.today(), status="openned")

    order.add_item(banana)
    order.add_item(mango)
    order.add_item(expensive_mango)

    print(f"Comparison bewteen mango and expensive mango: {mango == expensive_mango}")

    print(f"Total order price: ${order.calculate_total()/100:.2f}")
    print(f"Subtotal order price: ${order.calculate_sub_total()/100:.2f}")
    print(f"Value paid in taxes: ${order.calculate_tax()/100:.2f}")
    print(f"Total weight order: {order.total_weight} kg")


if __name__ == "__main__":
    main()