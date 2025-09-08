# AUFGABE
Gegeben die Details einer Energiebillenzeile, bestimme die korrekte 'BZArt' (Bezugszeilenart) aus den folgenden Optionen pro line Item.
Berücksichtige Beschreibung, Mengeneinheit und Kategorie. Gib ein JSON-Array der BZArt-Werte in derselben Reihenfolge wie die Zeilen zurück. Falls keine Zuordnung möglich, gib 'UNKNOWN' zurück.

#Referenzmapping:
BZArt: Clearinggebühr
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Clearinggebühr Swissgrid
-------------------
BZArt: CO2_Erdgas
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): CO2 Abgabe auf Erdgas
-------------------
BZArt: CO2_FW
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): CO2 Abgabe auf Fernwärme
-------------------
BZArt: DL_HT
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Netz HT
-------------------
BZArt: DL_Netzverlust_HT
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): DL_Netzverlust HT
-------------------
BZArt: DL_Netzverlust_NT
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): DL_Netzverlust NT
-------------------
BZArt: DL_NT
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Netz NT
-------------------
BZArt: DL_P
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Durchleitung Pauschale
-------------------
BZArt: EffBonus
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF
- Beschreibung (de): Effizienzbonus
-------------------
BZArt: EinspVerguetung_HT
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Einspeisevergütung HT
-------------------
BZArt: EinspVerguetung_NT
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Einspeisevergütung NT
-------------------
BZArt: ERA_M
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Energiereserve
-------------------
BZArt: ERA_M
Typ: Rest
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Energiereserve
-------------------
BZArt: Erdgas_kWh
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Erdgas kWh
-------------------
BZArt: FK_kWh
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Fernkälte kWh
-------------------
BZArt: FW_kWh
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Fernwärme kWh
-------------------
BZArt: Geb_LA
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF
- Beschreibung (de): Lenkungsabgabe BS
-------------------
BZArt: HT
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Energie HT
-------------------
BZArt: KEV
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): KEV
-------------------
BZArt: KEVV_BE
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): KEV Bew.-Entgelt DV
-------------------
BZArt: KEVV_BEA
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): KEV Anteil Bew.-Entgelt DV
-------------------
BZArt: KEVV_EP
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): KEV Einspeiseprämie
-------------------
BZArt: KEVV_RM
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): KEV Vergütung Ref.marktpreis
-------------------
BZArt: KZH
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Kontrollz. HT
-------------------
BZArt: KZN
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Kontrollz. NT
-------------------
BZArt: MessungkWh
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Messung kWh
-------------------
BZArt: MessungkWh_HT
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Messung HT
-------------------
BZArt: MessungkWh_NT
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Messung NT
-------------------
BZArt: NDL_HT
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Nationale Durchleitung HT
-------------------
BZArt: NDL_NT
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Nationale Durchleitung NT
-------------------
BZArt: NDL_System
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Systemdienstleistungen
-------------------
BZArt: NT
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Energie NT
-------------------
BZArt: P
Einheit Menge: kWh
Einheit Preis: CHF
- Beschreibung (de): Pauschale (verr.bar)
-------------------
BZArt: P_Mehrfach
Einheit Menge: kWh
Einheit Preis: CHF
- Beschreibung (de): Pauschale mehrfach (verr.bar)
-------------------
BZArt: PPV_ET
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Lokale Eigenproduktion
-------------------
BZArt: RabattMenge
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF
- Beschreibung (de): Rabatt auf Menge
-------------------
BZArt: RVArealNetz
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Rückvergütung Arealnetz
-------------------
BZArt: SA_L
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Steuern/Abg
-------------------
BZArt: SF_kWh
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Service Fees Energie
-------------------
BZArt: SpotEinkaufHT
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Einkauf Spot Hochtarif
-------------------
BZArt: SpotEinkaufNT
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Einkauf Spot NT
-------------------
BZArt: Stromzertifikate
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Zertifikate zur Verbesserung der Stromqualität
-------------------
BZArt: Verguetung_Mob_Ergy
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Vergütung
-------------------
BZArt: ZEE
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Zuschlag Energiequalität
-------------------

# Beispiele (line item description -> BZArt):
- "Arbeit Hochtarif" -> "HT"
- "Arbeit Niedertarif" -> "NT"
- "Wirkenergie HT" -> "DL_HT"
- "Wirkenergie NT" -> "DL_NT"
- "Grundtarif" -> "DL_Geb"
- "Leistungstarif" -> "DL_Leistung"
- "Systemdienstleistungen Swissgrid" -> "NDL_System"
- "Gesetzliche Förderabgabe" -> "KEV"
- "Abgaben und Leistungen an die Gemeinde" -> "SA_L"
- "Stromreserve" -> "ERA_M"

# Line item:
- Description: 01.03.2024 bis 31.03.2024 (31 Tage) ewz.tranche ET | quantity_unit: kWh | category: Energie | meter_point=CH1019901234500000000000000041085 ; VS_Adr=St. Leonhard-Strasse 3