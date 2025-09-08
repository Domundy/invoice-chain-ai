# AUFGABE
Gegeben die Details einer Energiebillenzeile, bestimme die korrekte 'BZArt' (Bezugszeilenart) aus den folgenden Optionen pro line Item.
Berücksichtige Beschreibung, Mengeneinheit und Kategorie. Gib ein JSON-Array der BZArt-Werte in derselben Reihenfolge wie die Zeilen zurück. Falls keine Zuordnung möglich, gib 'UNKNOWN' zurück.

#Referenzmapping:
BZArt: Anz_U
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Übertrag / Vortrag
-------------------
BZArt: Akonto
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Akontozahlung
-------------------
BZArt: AkontoV
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Akonto-Zahlung vor Primeo-Vertrag
-------------------
BZArt: ALVST
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Ausländische Vorsteuer
-------------------
BZArt: Anz_Rab
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Rabatt
-------------------
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
BZArt: DL_Akonto_L
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Akontozahlung
-------------------
BZArt: DL_Akonto_LV
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Akontozahlung Leistung
-------------------
BZArt: DL_Geb
Typ: Netznutzung
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Netz Gebühren
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
BZArt: DL_Rabatt
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Rabatt Netznutzung
-------------------
BZArt: EC
Einheit Menge: 
Einheit Preis: CHF/kWh.
- Beschreibung (de): Contracting
-------------------
BZArt: EDM
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Betrieb & Instandhaltung TS
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
BZArt: Entwässerung
Typ: Energie
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Entwässerung/Meteorwasser
-------------------
BZArt: EPK
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Energie Preis Korrektur
-------------------
BZArt: EPK_DL
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Durchleitungspreis Korrektur
-------------------
BZArt: EPK_DL_Leistung
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Preiskorrektur Netz Leistung
-------------------
BZArt: EPK_Leistung
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Preiskorrektur Leistung
-------------------
BZArt: EPK_SA
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Korrektur Steuern&Abgaben
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
BZArt: Erdgas_Geb
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Erdgas Gebühren
-------------------
BZArt: Erdgas_kWh
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Erdgas kWh
-------------------
BZArt: ERg
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Rabatt Elektronische Datenübermittlung
-------------------
BZArt: FK_Geb
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Fernkälte Gebühren
-------------------
BZArt: FK_kWh
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Fernkälte kWh
-------------------
BZArt: FW_Geb
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Fernwärme Gebühren
-------------------
BZArt: FW_kWh
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Fernwärme kWh
-------------------
BZArt: Geb
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Gebühr Allg.
-------------------
BZArt: Geb_E
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Einmalgebühren
-------------------
BZArt: Geb_FA
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Förderabgabe BS
-------------------
BZArt: Geb_G
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Grundgebühr
-------------------
BZArt: Geb_KZ
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Konzessionsgebühr
-------------------
BZArt: Geb_KZM
Typ: Netznutzung
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Konzessionsgebühr
-------------------
BZArt: Geb_KZR
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Konzessionsrabatt
-------------------
BZArt: Geb_LA
Typ: Netznutzung
Einheit Menge: kWh
Einheit Preis: CHF
- Beschreibung (de): Lenkungsabgabe BS
-------------------
BZArt: Geb_M
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Mahngebühren
-------------------
BZArt: Geb_Mob_Srv
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Mobilitätsdienstleistung
-------------------
BZArt: Geb_MV
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Mahngebühren verrechenbar
-------------------
BZArt: Geb_NKU
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Gebühr (NK-unfähig)
-------------------
BZArt: Geb_TBAK
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Gebühren BAKOM
-------------------
BZArt: Geb_TK
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Gebühren Telekommunikation
-------------------
BZArt: Geb_TNet
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Gebühren Internet
-------------------
BZArt: Geb_TT
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Gebühren Telefon
-------------------
BZArt: Geb_TV
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Gebühren Cable/TV
-------------------
BZArt: Geb_W
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Gebühr Wasser
-------------------
BZArt: Geb_Z
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Zählermiete
-------------------
BZArt: Geb_ZFA
Typ: Netznutzung
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Gebühr für Zählerfernauslesung
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
BZArt: KLeistung
Einheit Menge: 
Einheit Preis: CHF.
- Beschreibung (de): Kontrollzähler (Leistung)
-------------------
BZArt: KZH
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Kontrollz. HT
-------------------
BZArt: KZLH
Einheit Menge: 
Einheit Preis: CHF.
- Beschreibung (de): Kontrollz. Leist.
-------------------
BZArt: KZLN
Einheit Menge: 
Einheit Preis: CHF.
- Beschreibung (de): Kontrollz. Leist
-------------------
BZArt: KZN
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Kontrollz. NT
-------------------
BZArt: Material_K
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Materialkosten
-------------------
BZArt: MessungFuellstandL
Typ: Energie
Einheit Menge: 
Einheit Preis: CHF/L
- Beschreibung (de): Messung Füllstand L
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
BZArt: Minimal_DLK
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Minimalbetrag Durchleitunskosten
-------------------
BZArt: Minimal_EK
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Minimalbetrag Energiekosten
-------------------
BZArt: MWST_EUR
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): MWST Billing EUR
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
BZArt: Rab_Einm
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Einmal-Rabatt
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
BZArt: SA_Z
Typ: Netznutzung
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Steuern/Abgaben auf Strom Zeitbezogen
-------------------
BZArt: SF_kWh
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Service Fees Energie
-------------------
BZArt: Skonto
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Skonto
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
BZArt: TF
Typ: Energie
Einheit Menge: 
Einheit Preis: CHF/L
- Beschreibung (de): Tankfüllung
-------------------
BZArt: Verguetung_Mob_Ergy
Typ: Energie
Einheit Menge: kWh
Einheit Preis: CHF/kWh
- Beschreibung (de): Vergütung
-------------------
BZArt: Verz_ZS
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Verzugszinsen
-------------------
BZArt: XS
Einheit Menge: 
Einheit Preis: CHF
- Beschreibung (de): Splittinggebühr
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
- Description: Solarstrom | quantity_unit: kWh | category: Energie | meter_point=CH99999904055ZEV00000000000000360 ; VS_Adr=Im Westfeld 30
- Description: Netzstrom | quantity_unit: kWh | category: Energie | meter_point=CH99999904055ZEV00000000000000360 ; VS_Adr=Im Westfeld 30
- Description: Mess- und Abrechnungsdienstleistung 01.10.23-31.12.23 | quantity_unit: kWh | category: Rest | meter_point=CH99999904055ZEV00000000000000360 ; VS_Adr=Im Westfeld 30
- Description: MWST(siehe Details) | quantity_unit:  | category: Rest