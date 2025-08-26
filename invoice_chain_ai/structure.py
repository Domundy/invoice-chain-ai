from __future__ import annotations
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

# Add this datatype only if there is no QR detection
class PaymentInformation(BaseModel):
    """Payment information block (creditor details, IBAN, etc.)."""
    creditor_name: Optional[str] = Field(None, description="Name of the creditor/payee.")
    street: Optional[str] = Field(None, description="Street address of the creditor.")
    city_zip: Optional[str] = Field(None, description="City and postal code of the creditor. Swiss ZIP codes are 4 digits.")
    iban: Optional[str] = Field(None, description="IBAN used for the payment.")
    reference: Optional[str] = Field(None, description="Payment/reference number (structured reference).")
    source: Optional[str] = Field(None, description="Source of payment information (e.g., QR, invoice).")

# Add this datatype only if there is no QR detection
class Provider(BaseModel):
    """Provider/issuer of the invoice (company issuing the invoice)."""
    name: Optional[str] = Field(None, description="Provider name (company). Must include name and VAT number.")
    address_line1: Optional[str] = Field(None, description="Primary address line of the provider.")
    city_zip: Optional[str] = Field(None, description="City and postal code for the provider. Swiss ZIP codes are 4 digits.")

class Header(BaseModel):
    """Top-level invoice header information."""
    invoice_number: Optional[int] = Field(None, description="Invoice number as numeric value only.")
    invoice_date: Optional[str] = Field(None, description="Invoice date in exact format: dd.mm.yyyy")
    due_date: Optional[str] = Field(None, description="Payment due date in exact format: dd.mm.yyyy")
    invoice_type: Optional[str] = Field(None, description="Invoice type classification. Map both 'Akontorechnung' and 'facture d'acompte' to 'Akontorechnung'.")
    invoice_language: Optional[str] = Field(None, description="Invoice language as two-letter code: 'de'=German, 'fr'=French, 'it'=Italian")
    customer_number: Optional[str] = Field(None, description="Customer number or identifier exactly as shown on invoice.")
    contract_number: Optional[int] = Field(None, description="Contract number as numeric value only.")
    address_reference_line: Optional[str] = Field(None, description="Address reference line. Standard format: 'Primeo Energie AG, Ref. {this_value}, Überlandstrasse 2, 8953 Dietikon'")
    vat_number: Optional[str] = Field(None, description="VAT identification number exactly as displayed starting with 'CHE'.")
    billing_period: Optional[str] = Field(None, description="Billing period timeframe. When billing differs from delivery period, extract the billing period here.")
    total_amount_excl_vat: Optional[float] = Field(None, description="Total pre-VAT amount in CHF, formatted to exactly 2 decimal places.")
    total_amount_excl_vat_unit: Optional[str] = Field(None, description="Currency unit (always 'CHF' for Swiss bills).")
    vat_amount: Optional[float] = Field(None, description="VAT amount in CHF, formatted to exactly 2 decimal places. Extract only if explicitly stated.")
    vat_amount_unit: Optional[str] = Field(None, description="Currency unit (always 'CHF' for Swiss bills).")
    total_amount_incl_vat: Optional[float] = Field(None, description="Total post-VAT amount in CHF, formatted to exactly 2 decimal places.")
    total_amount_incl_vat_unit: Optional[str] = Field(None, description="Currency unit (always 'CHF' for Swiss bills).")
    rounding_difference: Optional[float] = Field(None, description="Rounding adjustment in CHF, formatted to exactly 2 decimal places.")
    rounding_difference_unit: Optional[str] = Field(None, description="Currency unit (always 'CHF' for Swiss bills).")
    payable_amount: Optional[float] = Field(None, description="Final payable amount in CHF, formatted to exactly 2 decimal places.")
    payable_amount_unit: Optional[str] = Field(None, description="Currency unit (always 'CHF' for Swiss bills).")
    #provider: Optional[Provider] = Field(None, description="Provider/issuer company details.")
    #payment_information: Optional[PaymentInformation] = Field(None, description="Payment and creditor details.")

class Category(str, Enum):
    """Category classification for a line item."""
    energie = "Energie"
    netznutzung = "Netznutzung" 
    rest = "Rest"

class Utility(str, Enum):
    """Utility type for energy-related items."""
    elektrizitaet = "E"  # Electricity
    wasser = "W"  # Water
    fernwaerme = "F"  # District heating
    erdgas = "G"  # Natural gas
    abwasser = "A"  # Waste water
    fernkaelte = "FK"  # District cooling
    heizoel = "O"  # Heating oil
    abfall = "K"  # Waste
    recycling = "R"  # Recycling

class LineItem(BaseModel):
    """Single invoice line item. Extract each item individually, never summarize."""
    line_items_description: Optional[str] = Field(None, description="Line item description exactly as shown")
    delivery_period: Optional[str] = Field(None, description="Service/delivery period in format: dd.mm.yyyy-dd.mm.yyyy with zero whitespace. Example: '01.03.2024-31.03.2024'")
    quantity: Optional[float] = Field(None, description="Measured quantity for this line item.")
    quantity_unit: Optional[str] = Field(None, description="Unit of measurement (kWh, kW, m³, etc.).")
    unit_price: Optional[float] = Field(None, description="Price per unit, formatted to exactly 2 decimal places.")
    #unit_price_unit: Optional[str] = Field(None, description="Currency unit (always 'CHF' for Swiss bills).")
    total_price: Optional[float] = Field(None, description="Line total excluding VAT in CHF, formatted to exactly 2 decimal places. Use 0.00 for items without monetary value.")
    #total_price_unit: Optional[str] = Field(None, description="Currency unit (always 'CHF' for Swiss bills).")
    vat_amount: Optional[float] = Field(None, description="VAT amount for this line in CHF, formatted to exactly 2 decimal places. CONSTRAINT: Only extract if explicitly shown - never calculate.")
    #vat_amount_unit: Optional[str] = Field(None, description="Currency unit (always 'CHF' for Swiss bills).")
    vat_rate: Optional[float] = Field(None, description="VAT rate as decimal (0.081 = 8.1%, 0.077 = 7.7%).")
    total_price_incl_vat: Optional[float] = Field(None, description="Line total including VAT, formatted to exactly 2 decimal places.")
    #total_price_incl_vat_unit: Optional[str] = Field(None, description="Currency unit (always 'CHF' for Swiss bills).")
    meter_point: Optional[str] = Field(None, description="Metering point ID - exactly 33 characters starting with 'CH' or 'LI'.")
    meter_number: Optional[str] = Field(None, description="Physical meter number exactly as displayed.")
    utility: Optional[Utility] = Field(None, description="Utility classification: E=Electricity, W=Water, F=District heating, G=Natural gas, A=Waste water, FK=District cooling, O=Heating oil, K=Waste, R=Recycling")
    category: Optional[Category] = Field(None, description="Line category: 'Energie'=Energy supply, 'Netznutzung'=Network usage, 'Rest'=Other charges")
    tarif_product: Optional[str] = Field(None, description="Tariff or product name exactly as shown.")
    VS_Adr: Optional[str] = Field(None, description="Supply address - street and number only (e.g., 'Wehrstrasse 47'). Do not include city or postal code.")
    VS_Ort: Optional[str] = Field(None, description="Supply location - city with 4-digit Swiss postal code (e.g., '3203 Mühleberg'). Non-Swiss locations may have different postal code lengths.")

class EnergyBill(BaseModel):
    """Top-level energy invoice schema containing header and line items."""
    header: Optional[Header] = Field(None, description="Invoice header containing totals and provider info.")
    line_items: Optional[List[LineItem]] = Field(None, description="List of individual line items on the invoice.")