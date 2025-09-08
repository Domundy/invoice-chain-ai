# COMPITO
Dato i dettagli di una voce di bolletta energetica, determina il 'BZArt' (tipo di riga di consumo) corretto tra le seguenti opzioni per ogni voce.
Considera descrizione, unità di quantità e categoria. Restituisci un array JSON dei valori BZArt nello stesso ordine delle voci. Se non è possibile assegnare, restituisci 'UNKNOWN'.

#Mappatura di riferimento:
BZArt: Anz_U
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Riporto
-------------------
BZArt: Akonto
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Pagamento acconto
-------------------
BZArt: AkontoV
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Pagamento acconto prima del contratto Primeo
-------------------
BZArt: ALVST
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Imposta a monte estere
-------------------
BZArt: Anz_Rab
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Ribasso
-------------------
BZArt: Clearinggebühr
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Tassa clearing
-------------------
BZArt: CO2_Erdgas
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): CO2 tassa federale sul gas
-------------------
BZArt: CO2_FW
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): CO2 tassa federale sul teleriscaldamento
-------------------
BZArt: DL_Akonto_L
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Pagamento acconto
-------------------
BZArt: DL_Akonto_LV
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Pagamento acconto potenza
-------------------
BZArt: DL_Geb
Tipo: Netznutzung
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa base
-------------------
BZArt: DL_HT
Tipo: Netznutzung
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Rete.diurna
-------------------
BZArt: DL_Leistung
Tipo: Netznutzung
Unità di quantità: kW
Unità di prezzo: CHF/kW
- Descrizione (it): Potenza rete
-------------------
BZArt: DL_Netzverlust_HT
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Perdita rete diurna
-------------------
BZArt: DL_Netzverlust_L
Unità di quantità: kW
Unità di prezzo: CHF/kW
- Descrizione (it): Perdita rete potenza
-------------------
BZArt: DL_Netzverlust_NT
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Perdita rete notturna
-------------------
BZArt: DL_NT
Tipo: Netznutzung
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Rete.notturna
-------------------
BZArt: DL_P
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Transito, forfettario
-------------------
BZArt: DL_Rabatt
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Ribasso utilizzo rete
-------------------
BZArt: EC
Unità di quantità: 
Unità di prezzo: CHF/kWh.
- Descrizione (it): Contracting
-------------------
BZArt: EDM
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Manutenzione
-------------------
BZArt: EffBonus
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF
- Descrizione (it): Bonus efficienza
-------------------
BZArt: EinspVerguetung_HT
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Spese per fornitura di energia diurna
-------------------
BZArt: EinspVerguetung_NT
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Spese per fornitura di energia notturna
-------------------
BZArt: Entwässerung
Tipo: Energie
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Prosciugamento/drenaggio
-------------------
BZArt: EPK
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Correzione prezzo energia
-------------------
BZArt: EPK_DL
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Correzione prezzo transito rete
-------------------
BZArt: EPK_DL_Leistung
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Correzione prezzo potenza rete
-------------------
BZArt: EPK_Leistung
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Correzione prezzo potenza
-------------------
BZArt: EPK_SA
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Correzione contributi ai comuni
-------------------
BZArt: ERA_M
Tipo: Netznutzung
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Riserva di energia
-------------------
BZArt: ERA_M
Tipo: Rest
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Riserva di energia
-------------------
BZArt: Erdgas_Geb
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Componente base gas
-------------------
BZArt: Erdgas_kWh
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Consumo gas
-------------------
BZArt: ERg
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Sconto per trasmissione dei dati elettronici
-------------------
BZArt: FK_Geb
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa refrigerazione
-------------------
BZArt: FK_kWh
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Refrigerazione kWh
-------------------
BZArt: FW_Geb
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa teleriscaldamento
-------------------
BZArt: FW_kWh
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Teleriscaldamento kWh
-------------------
BZArt: Geb
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa generale
-------------------
BZArt: Geb_E
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa unica
-------------------
BZArt: Geb_FA
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Incentivo energia rinnovabile
-------------------
BZArt: Geb_G
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa base
-------------------
BZArt: Geb_KZ
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa di concessione
-------------------
BZArt: Geb_KZM
Tipo: Netznutzung
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa di concessione
-------------------
BZArt: Geb_KZR
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Sconto concessione
-------------------
BZArt: Geb_LA
Tipo: Netznutzung
Unità di quantità: kWh
Unità di prezzo: CHF
- Descrizione (it): Incentivo fondo risparmio energetico
-------------------
BZArt: Geb_M
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Spese di sollecito
-------------------
BZArt: Geb_Mob_Srv
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Mobilitätsdienstleistung
-------------------
BZArt: Geb_MV
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Spese di sollecito da mettere in conto
-------------------
BZArt: Geb_NKU
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Gebühr (NK-unfähig)_it
-------------------
BZArt: Geb_TBAK
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Gebühren BAKOM
-------------------
BZArt: Geb_TK
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa telecomunicazione
-------------------
BZArt: Geb_TNet
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Gebühren Internet
-------------------
BZArt: Geb_TT
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Gebühren Telefon
-------------------
BZArt: Geb_TV
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Gebühren Cable/TV
-------------------
BZArt: Geb_W
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa acqua
-------------------
BZArt: Geb_Z
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa contatore
-------------------
BZArt: Geb_ZFA
Tipo: Netznutzung
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Tassa per telelettura
-------------------
BZArt: HT
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Ener.diurna
-------------------
BZArt: KEV
Tipo: Netznutzung
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Contributo federale energie rinnovabili
-------------------
BZArt: KEVV_BE
Tipo: Netznutzung
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Retribuzione energie prodotta (RPC)
-------------------
BZArt: KEVV_BEA
Tipo: Netznutzung
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): KEV Bew.-Entgelt DV
-------------------
BZArt: KEVV_EP
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Retribuzione energie prodotta (RPC)
-------------------
BZArt: KEVV_RM
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Retribuzione energie prodotta (RPC)
-------------------
BZArt: KLeistung
Unità di quantità: 
Unità di prezzo: CHF.
- Descrizione (it): Contatore controllo (potenza)
-------------------
BZArt: KZH
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Contatore controllo diurna
-------------------
BZArt: KZLH
Unità di quantità: 
Unità di prezzo: CHF.
- Descrizione (it): Contatore controllo potenza
-------------------
BZArt: KZLN
Unità di quantità: 
Unità di prezzo: CHF.
- Descrizione (it): Contatore controllo potenza
-------------------
BZArt: KZN
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Contatore controllo notturna
-------------------
BZArt: Leistung
Tipo: Energie
Unità di quantità: kW
Unità di prezzo: CHF/kW
- Descrizione (it): Potenza
-------------------
BZArt: LHT
Unità di quantità: kW
Unità di prezzo: CHF/kW
- Descrizione (it): Potenza diurna
-------------------
BZArt: LNT
Unità di quantità: kW
Unità di prezzo: CHF/kW
- Descrizione (it): Potenza notturna
-------------------
BZArt: Material_K
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Costi materiale
-------------------
BZArt: MessungFuellstandL
Tipo: Energie
Unità di quantità: 
Unità di prezzo: CHF/L
- Descrizione (it): Rilevamento kWh
-------------------
BZArt: MessungkWh
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Rilevamento kWh
-------------------
BZArt: MessungkWh_HT
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Rilevamento diurna
-------------------
BZArt: MessungkWh_NT
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Rilevamento nott.
-------------------
BZArt: Minimal_DLK
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Importo minimo rete
-------------------
BZArt: Minimal_EK
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Importo minimo energia
-------------------
BZArt: MWST_EUR
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): IVA Billing EUR
-------------------
BZArt: NDL_HT
Tipo: Netznutzung
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Transito energia nazionale diurna
-------------------
BZArt: NDL_Leistung
Unità di quantità: kW
Unità di prezzo: CHF/kW
- Descrizione (it): Transito energia nazionale potenza
-------------------
BZArt: NDL_NT
Tipo: Netznutzung
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Transito energia nazionale notturna
-------------------
BZArt: NDL_System
Tipo: Netznutzung
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Prestazioni di sistema generale Swissgrid
-------------------
BZArt: NT
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Ener.notturna
-------------------
BZArt: P
Unità di quantità: kWh
Unità di prezzo: CHF
- Descrizione (it): Forfettario
-------------------
BZArt: P_Mehrfach
Unità di quantità: kWh
Unità di prezzo: CHF
- Descrizione (it): Forfettario multiplo
-------------------
BZArt: PPV_ET
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Energia locale
-------------------
BZArt: Rab_Einm
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Riduzione unica
-------------------
BZArt: RabattMenge
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF
- Descrizione (it): Ribasso
-------------------
BZArt: RVArealNetz
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Rimborso rete areale
-------------------
BZArt: SA_L
Tipo: Netznutzung
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Contributi ai comuni
-------------------
BZArt: SA_Z
Tipo: Netznutzung
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Contributi ai comuni relativi al tempo
-------------------
BZArt: SF_kWh
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Tariffa servizio energia
-------------------
BZArt: Skonto
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Sconto
-------------------
BZArt: SpotEinkaufHT
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Spot tariffa alta
-------------------
BZArt: SpotEinkaufNT
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Spot tariffa bassa
-------------------
BZArt: Stromzertifikate
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Certificato per migliorameno qualita energia
-------------------
BZArt: TF
Tipo: Energie
Unità di quantità: 
Unità di prezzo: CHF/L
- Descrizione (it): Pieno, serbatoio
-------------------
BZArt: Verguetung_Mob_Ergy
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Remunerazione
-------------------
BZArt: Verz_ZS
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Interesse di mora
-------------------
BZArt: XS
Unità di quantità: 
Unità di prezzo: CHF
- Descrizione (it): Spese splitting
-------------------
BZArt: ZEE
Tipo: Energie
Unità di quantità: kWh
Unità di prezzo: CHF/kWh
- Descrizione (it): Supplemento energia rinnovabile
-------------------

# Esempi (descrizione voce -> BZArt):
- "Lavoro tariffa alta" -> "HT"
- "Lavoro tariffa bassa" -> "NT"
- "Energia attiva HT" -> "DL_HT"
- "Energia attiva NT" -> "DL_NT"
- "Tariffa base" -> "DL_Geb"
- "Tariffa potenza" -> "DL_Leistung"
- "Servizi di sistema Swissgrid" -> "NDL_System"
- "Tassa legale di promozione" -> "KEV"
- "Tasse e prestazioni al comune" -> "SA_L"
- "Riserva elettrica" -> "ERA_M"

# Line item:
- Description: Quota fissa | quantity_unit: mese | category: Netznutzung | meter_point=CH10109012345CS000000000000000420 ; VS_Adr=Via Pianoni 7
- Description: Tariffa trasporto energia diurna | quantity_unit: kWh | category: Netznutzung | meter_point=CH10109012345CS000000000000000420 ; VS_Adr=Via Pianoni 7
- Description: Tariffa trasporto energia notturna | quantity_unit: kWh | category: Netznutzung | meter_point=CH10109012345CS000000000000000420 ; VS_Adr=Via Pianoni 7
- Description: Tassa di potenza misurata | quantity_unit: kW | category: Netznutzung | meter_point=CH10109012345CS000000000000000420 ; VS_Adr=Via Pianoni 7
- Description: Totale utilizzo rete (CHF) | quantity_unit:  | category: Netznutzung
- Description: Prestazioni di sistema generale Swissgrid | quantity_unit: kWh | category: Rest | meter_point=CH10109012345CS000000000000000420 ; VS_Adr=Via Pianoni 7
- Description: Contributo federale energie rinnovabili | quantity_unit: kWh | category: Rest | meter_point=CH10109012345CS000000000000000420 ; VS_Adr=Via Pianoni 7
- Description: Risanamento ecologico impianti idroelettrici | quantity_unit: kWh | category: Rest | meter_point=CH10109012345CS000000000000000420 ; VS_Adr=Via Pianoni 7
- Description: Tassa per l ' utilizzo del demanio pubblico | quantity_unit: kWh | category: Rest | meter_point=CH10109012345CS000000000000000420 ; VS_Adr=Via Pianoni 7
- Description: Fondo cantonale per le energie rinnovabili | quantity_unit: kWh | category: Rest | meter_point=CH10109012345CS000000000000000420 ; VS_Adr=Via Pianoni 7
- Description: Totale tasse (CHF) | quantity_unit:  | category: Rest