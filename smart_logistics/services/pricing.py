from abc import ABC, abstractmethod
import math


class PricingStrategy(ABC):

    @abstractmethod
    def calculate_base_charge(self):
        pass


class StandardPricing(PricingStrategy):

    def calculate_base_charge(self):
        return 60


class ExpressPricing(PricingStrategy):

    def calculate_base_charge(self):
        return 110


class PricingService:

    def calculate_price(self, weight, service_type, zone, is_fragile=False):

        # Base charge
        if service_type == "Standard":
            strategy = StandardPricing()

        elif service_type == "Express":
            strategy = ExpressPricing()

        else:
            raise ValueError("Invalid service type")

        base_charge = strategy.calculate_base_charge()

        # Weight charge
        extra_units = max(0, math.ceil((weight - 0.5) / 0.5))
        weight_charge = extra_units * 25

        # Zone charge
        zone_charges = {
            "Local": 0,
            "Within State": 40,
            "Interstate": 90
        }

        if zone not in zone_charges:
            raise ValueError("Invalid zone")

        zone_charge = zone_charges[zone]

        # Fragile charge
        fragile_charge = 35 if is_fragile else 0

        total = (
            base_charge
            + weight_charge
            + zone_charge
            + fragile_charge
        )

        return {
            "base_charge": base_charge,
            "weight_charge": weight_charge,
            "zone_charge": zone_charge,
            "fragile_charge": fragile_charge,
            "total": total
        }