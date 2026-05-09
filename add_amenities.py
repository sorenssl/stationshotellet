"""Add 'What this place offers' amenities section to all 6 language files.

Layout:
  - 8 highlight cards (icon + bold title) in 4-col responsive grid
  - <details> expandable: full 52-item list grouped by 12 categories (zero JS)

Placement: between Accommodation (gallery) and Prices.
Anchor:  <section id="prices">  (universal across all 6 langs)

Idempotent: re-run is safe (checks for id="amenities" marker).

Run from repo root:
    python add_amenities.py
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent

# 8 highlights (top grid). Keys map into per-lang title strings below.
HIGHLIGHTS = [
    {"icon": "&#128246;",  "key": "h_wifi"},     # signal bars - wifi
    {"icon": "&#128663;",  "key": "h_parking"},  # car
    {"icon": "&#128273;",  "key": "h_checkin"},  # key
    {"icon": "&#127869;",  "key": "h_kitchen"},  # cooked food
    {"icon": "&#129516;",  "key": "h_washer"},   # bucket - laundry stand-in
    {"icon": "&#10052;",   "key": "h_ac"},       # snowflake
    {"icon": "&#128188;",  "key": "h_workspace"},# briefcase
    {"icon": "&#128197;",  "key": "h_longterm"}, # calendar
]

# Full categorized list. icon + i18n key for category name + list of item keys.
CATEGORIES = [
    {"icon": "&#128703;", "key": "cat_bathroom",
     "items": ["i_hairdryer", "i_cleaning", "i_shampoo", "i_bodysoap", "i_hotwater"]},
    {"icon": "&#128719;", "key": "cat_bedroom",
     "items": ["i_washer_unit", "i_dryer", "i_essentials", "i_hangers", "i_bedlinens",
               "i_cottonlinens", "i_extrabedding", "i_blackoutshades", "i_iron",
               "i_dryingrack", "i_safe", "i_closet"]},
    {"icon": "&#128250;", "key": "cat_entertainment",
     "items": ["i_ethernet", "i_tv", "i_console_ps3"]},
    {"icon": "&#128118;", "key": "cat_family",
     "items": ["i_windowguards", "i_outletcovers"]},
    {"icon": "&#10052;",  "key": "cat_climate",
     "items": ["i_ac", "i_heating"]},
    {"icon": "&#128737;", "key": "cat_safety",
     "items": ["i_securitycams", "i_outdoorwebcams", "i_smokealarm",
               "i_fireextinguisher", "i_firstaid"]},
    {"icon": "&#128241;", "key": "cat_internet",
     "items": ["i_fastwifi", "i_workspace_common"]},
    {"icon": "&#127869;", "key": "cat_kitchen",
     "items": ["i_kitchen_cook", "i_fridge", "i_microwave", "i_cookingbasics",
               "i_dishes", "i_freezer", "i_dishwasher", "i_stove", "i_oven",
               "i_kettle", "i_coffeemaker", "i_wineglasses", "i_toaster",
               "i_ricemaker", "i_diningtable", "i_coffee"]},
    {"icon": "&#128205;", "key": "cat_location",
     "items": ["i_privateentrance"]},
    {"icon": "&#127795;", "key": "cat_outdoor",
     "items": ["i_patio", "i_outdoorfurniture"]},
    {"icon": "&#128663;", "key": "cat_parking",
     "items": ["i_freeparking"]},
    {"icon": "&#128296;", "key": "cat_services",
     "items": ["i_longterm", "i_selfcheckin"]},
]

TOTAL_ITEMS = sum(len(c["items"]) for c in CATEGORIES)  # = 52

# Per-language strings. Keys are referenced by HIGHLIGHTS, CATEGORIES, and section chrome.
I18N = {
    "index.html": {
        "section_label": "Amenities",
        "section_title": "What this place offers",
        "section_subtitle": "Everything you need for a comfortable stay &mdash; verified by 63 guests on Airbnb.",
        "show_all": f"Show all {TOTAL_ITEMS} amenities &darr;",
        # highlight titles
        "h_wifi": "Fast Wi-Fi 75&nbsp;Mbps",
        "h_parking": "Free parking on site",
        "h_checkin": "Self check-in (lockbox)",
        "h_kitchen": "Full kitchen &amp; dishwasher",
        "h_washer": "Washer &amp; dryer in unit",
        "h_ac": "Air conditioning &amp; heating",
        "h_workspace": "Dedicated workspace",
        "h_longterm": "Long-term stays welcome",
        # category headings
        "cat_bathroom": "Bathroom",
        "cat_bedroom": "Bedroom &amp; laundry",
        "cat_entertainment": "Entertainment",
        "cat_family": "Family",
        "cat_climate": "Heating &amp; cooling",
        "cat_safety": "Home safety",
        "cat_internet": "Internet &amp; workspace",
        "cat_kitchen": "Kitchen &amp; dining",
        "cat_location": "Location features",
        "cat_outdoor": "Outdoor",
        "cat_parking": "Parking",
        "cat_services": "Services",
        # items
        "i_hairdryer": "Hair dryer",
        "i_cleaning": "Cleaning products",
        "i_shampoo": "Shampoo",
        "i_bodysoap": "Body soap",
        "i_hotwater": "Hot water",
        "i_washer_unit": "Free washer (in unit)",
        "i_dryer": "Dryer",
        "i_essentials": "Essentials &mdash; towels, bed sheets, soap, toilet paper",
        "i_hangers": "Hangers",
        "i_bedlinens": "Bed linens",
        "i_cottonlinens": "Cotton linens",
        "i_extrabedding": "Extra pillows and blankets",
        "i_blackoutshades": "Room-darkening shades",
        "i_iron": "Iron",
        "i_dryingrack": "Drying rack for clothing",
        "i_safe": "Safe",
        "i_closet": "Clothing storage: closet and wardrobe",
        "i_ethernet": "Ethernet connection",
        "i_tv": "TV",
        "i_console_ps3": "Game console: PlayStation 3",
        "i_windowguards": "Window guards",
        "i_outletcovers": "Outlet covers",
        "i_ac": "Air conditioning",
        "i_heating": "Heating",
        "i_securitycams": "Exterior security cameras on property",
        "i_outdoorwebcams": "Outdoor webcams &mdash; parking and arrivals",
        "i_smokealarm": "Smoke alarm",
        "i_fireextinguisher": "Fire extinguisher",
        "i_firstaid": "First aid kit",
        "i_fastwifi": "Fast Wi-Fi 75&nbsp;Mbps &mdash; verified, streams 4K and video calls",
        "i_workspace_common": "Dedicated workspace (in a common space)",
        "i_kitchen_cook": "Kitchen &mdash; cook your own meals",
        "i_fridge": "Electrolux refrigerator",
        "i_microwave": "Microwave",
        "i_cookingbasics": "Cooking basics &mdash; pots, pans, oil, salt, pepper",
        "i_dishes": "Dishes &amp; silverware &mdash; bowls, chopsticks, plates, cups",
        "i_freezer": "Freezer",
        "i_dishwasher": "Dishwasher",
        "i_stove": "Stove",
        "i_oven": "Electrolux oven",
        "i_kettle": "Hot water kettle",
        "i_coffeemaker": "Drip coffee maker",
        "i_wineglasses": "Wine glasses",
        "i_toaster": "Toaster",
        "i_ricemaker": "Rice cooker",
        "i_diningtable": "Dining table",
        "i_coffee": "Coffee",
        "i_privateentrance": "Private entrance &mdash; separate street or building entrance",
        "i_patio": "Shared patio or balcony",
        "i_outdoorfurniture": "Outdoor furniture",
        "i_freeparking": "Free parking on premises",
        "i_longterm": "Long-term stays allowed (28 days or more)",
        "i_selfcheckin": "Self check-in with lockbox",
    },
    "sv/index.html": {
        "section_label": "Bekv&auml;mligheter",
        "section_title": "Vad detta boende erbjuder",
        "section_subtitle": "Allt du beh&ouml;ver f&ouml;r en bekv&auml;m vistelse &mdash; verifierat av 63 g&auml;ster p&aring; Airbnb.",
        "show_all": f"Visa alla {TOTAL_ITEMS} bekv&auml;mligheter &darr;",
        "h_wifi": "Snabbt Wi-Fi 75&nbsp;Mbps",
        "h_parking": "Gratis parkering p&aring; plats",
        "h_checkin": "Sj&auml;lvincheckning (nyckelsk&aring;p)",
        "h_kitchen": "Fullt utrustat k&ouml;k &amp; diskmaskin",
        "h_washer": "Tv&auml;ttmaskin &amp; torktumlare",
        "h_ac": "Luftkonditionering &amp; v&auml;rme",
        "h_workspace": "Dedikerad arbetsplats",
        "h_longterm": "L&aring;ngtidsboende v&auml;lkomna",
        "cat_bathroom": "Badrum",
        "cat_bedroom": "Sovrum &amp; tv&auml;tt",
        "cat_entertainment": "Underh&aring;llning",
        "cat_family": "Familj",
        "cat_climate": "Uppv&auml;rmning &amp; kyla",
        "cat_safety": "S&auml;kerhet",
        "cat_internet": "Internet &amp; arbete",
        "cat_kitchen": "K&ouml;k &amp; matsal",
        "cat_location": "Plats",
        "cat_outdoor": "Utomhus",
        "cat_parking": "Parkering",
        "cat_services": "Tj&auml;nster",
        "i_hairdryer": "H&aring;rtork",
        "i_cleaning": "Rengöringsprodukter",
        "i_shampoo": "Schampo",
        "i_bodysoap": "Duschtv&aring;l",
        "i_hotwater": "Varmvatten",
        "i_washer_unit": "Tv&auml;ttmaskin (i l&auml;genheten)",
        "i_dryer": "Torktumlare",
        "i_essentials": "B&auml;ddset &mdash; handdukar, lakan, tv&aring;l, toalettpapper",
        "i_hangers": "Galgar",
        "i_bedlinens": "S&auml;ngkl&auml;der",
        "i_cottonlinens": "Bomullslinne",
        "i_extrabedding": "Extra kuddar och filtar",
        "i_blackoutshades": "M&ouml;rkl&auml;ggningsgardiner",
        "i_iron": "Strykj&auml;rn",
        "i_dryingrack": "Tork&auml;ll",
        "i_safe": "Kassask&aring;p",
        "i_closet": "F&ouml;rvaring: garderob",
        "i_ethernet": "Ethernet-anslutning",
        "i_tv": "TV",
        "i_console_ps3": "Spelkonsol: PlayStation 3",
        "i_windowguards": "F&ouml;nstersp&auml;rrar",
        "i_outletcovers": "Eluttagsskydd",
        "i_ac": "Luftkonditionering",
        "i_heating": "Uppv&auml;rmning",
        "i_securitycams": "Utomhus&ouml;vervakningskameror",
        "i_outdoorwebcams": "Utomhuswebbkameror &mdash; parkering och ankomster",
        "i_smokealarm": "Brandvarnare",
        "i_fireextinguisher": "Brandsl&auml;ckare",
        "i_firstaid": "F&ouml;rsta hj&auml;lpen-set",
        "i_fastwifi": "Snabbt Wi-Fi 75&nbsp;Mbps &mdash; verifierat, str&ouml;mma 4K och videosamtal",
        "i_workspace_common": "Dedikerad arbetsplats (i ett gemensamt utrymme)",
        "i_kitchen_cook": "K&ouml;k &mdash; laga din egen mat",
        "i_fridge": "Electrolux kylsk&aring;p",
        "i_microwave": "Mikrov&aring;gsugn",
        "i_cookingbasics": "Matlagningsgrunder &mdash; kastruller, stekpannor, olja, salt, peppar",
        "i_dishes": "Porslin &amp; bestick &mdash; sk&aring;lar, &auml;tpinnar, tallrikar, koppar",
        "i_freezer": "Frys",
        "i_dishwasher": "Diskmaskin",
        "i_stove": "Spis",
        "i_oven": "Electrolux ugn",
        "i_kettle": "Vattenkokare",
        "i_coffeemaker": "Kaffebryggare",
        "i_wineglasses": "Vinglas",
        "i_toaster": "Br&ouml;drost",
        "i_ricemaker": "Riskokare",
        "i_diningtable": "Matbord",
        "i_coffee": "Kaffe",
        "i_privateentrance": "Privat ing&aring;ng &mdash; separat gata eller byggnadsing&aring;ng",
        "i_patio": "Delad uteplats eller balkong",
        "i_outdoorfurniture": "Utem&ouml;bler",
        "i_freeparking": "Gratis parkering p&aring; plats",
        "i_longterm": "L&aring;ngtidsuthyrning till&aring;ten (28 dagar eller mer)",
        "i_selfcheckin": "Sj&auml;lvincheckning med nyckelsk&aring;p",
    },
    "fr/index.html": {
        "section_label": "&Eacute;quipements",
        "section_title": "Ce que ce logement propose",
        "section_subtitle": "Tout ce qu&rsquo;il vous faut pour un s&eacute;jour confortable &mdash; v&eacute;rifi&eacute; par 63 voyageurs sur Airbnb.",
        "show_all": f"Afficher les {TOTAL_ITEMS} &eacute;quipements &darr;",
        "h_wifi": "Wi-Fi rapide 75&nbsp;Mbps",
        "h_parking": "Parking gratuit sur place",
        "h_checkin": "Auto-enregistrement (bo&icirc;te &agrave; cl&eacute;s)",
        "h_kitchen": "Cuisine &eacute;quip&eacute;e &amp; lave-vaisselle",
        "h_washer": "Lave-linge &amp; s&egrave;che-linge",
        "h_ac": "Climatisation &amp; chauffage",
        "h_workspace": "Espace de travail d&eacute;di&eacute;",
        "h_longterm": "S&eacute;jours longue dur&eacute;e bienvenus",
        "cat_bathroom": "Salle de bain",
        "cat_bedroom": "Chambre &amp; buanderie",
        "cat_entertainment": "Divertissement",
        "cat_family": "Famille",
        "cat_climate": "Chauffage &amp; climatisation",
        "cat_safety": "S&eacute;curit&eacute;",
        "cat_internet": "Internet &amp; espace de travail",
        "cat_kitchen": "Cuisine &amp; salle &agrave; manger",
        "cat_location": "Emplacement",
        "cat_outdoor": "Ext&eacute;rieur",
        "cat_parking": "Parking",
        "cat_services": "Services",
        "i_hairdryer": "S&egrave;che-cheveux",
        "i_cleaning": "Produits d&rsquo;entretien",
        "i_shampoo": "Shampooing",
        "i_bodysoap": "Savon corporel",
        "i_hotwater": "Eau chaude",
        "i_washer_unit": "Lave-linge (dans le logement)",
        "i_dryer": "S&egrave;che-linge",
        "i_essentials": "Essentiels &mdash; serviettes, draps, savon, papier toilette",
        "i_hangers": "Cintres",
        "i_bedlinens": "Linge de lit",
        "i_cottonlinens": "Linge de lit en coton",
        "i_extrabedding": "Oreillers et couvertures suppl&eacute;mentaires",
        "i_blackoutshades": "Stores occultants",
        "i_iron": "Fer &agrave; repasser",
        "i_dryingrack": "&Eacute;tendoir &agrave; linge",
        "i_safe": "Coffre-fort",
        "i_closet": "Rangement: placard et armoire",
        "i_ethernet": "Connexion Ethernet",
        "i_tv": "T&eacute;l&eacute;vision",
        "i_console_ps3": "Console de jeu: PlayStation 3",
        "i_windowguards": "Garde-fen&ecirc;tres",
        "i_outletcovers": "Cache-prises",
        "i_ac": "Climatisation",
        "i_heating": "Chauffage",
        "i_securitycams": "Cam&eacute;ras de s&eacute;curit&eacute; ext&eacute;rieures",
        "i_outdoorwebcams": "Webcams ext&eacute;rieures &mdash; parking et arriv&eacute;es",
        "i_smokealarm": "D&eacute;tecteur de fum&eacute;e",
        "i_fireextinguisher": "Extincteur",
        "i_firstaid": "Trousse de premiers secours",
        "i_fastwifi": "Wi-Fi rapide 75&nbsp;Mbps &mdash; v&eacute;rifi&eacute;, 4K et appels vid&eacute;o",
        "i_workspace_common": "Espace de travail d&eacute;di&eacute; (espace commun)",
        "i_kitchen_cook": "Cuisine &mdash; pr&eacute;parez vos propres repas",
        "i_fridge": "R&eacute;frig&eacute;rateur Electrolux",
        "i_microwave": "Micro-ondes",
        "i_cookingbasics": "Bases pour cuisiner &mdash; casseroles, po&ecirc;les, huile, sel, poivre",
        "i_dishes": "Vaisselle &amp; couverts &mdash; bols, baguettes, assiettes, tasses",
        "i_freezer": "Cong&eacute;lateur",
        "i_dishwasher": "Lave-vaisselle",
        "i_stove": "Cuisini&egrave;re",
        "i_oven": "Four Electrolux",
        "i_kettle": "Bouilloire",
        "i_coffeemaker": "Cafeti&egrave;re filtre",
        "i_wineglasses": "Verres &agrave; vin",
        "i_toaster": "Grille-pain",
        "i_ricemaker": "Cuiseur &agrave; riz",
        "i_diningtable": "Table &agrave; manger",
        "i_coffee": "Caf&eacute;",
        "i_privateentrance": "Entr&eacute;e priv&eacute;e &mdash; rue ou b&acirc;timent s&eacute;par&eacute;",
        "i_patio": "Terrasse ou balcon partag&eacute;",
        "i_outdoorfurniture": "Mobilier d&rsquo;ext&eacute;rieur",
        "i_freeparking": "Parking gratuit sur place",
        "i_longterm": "S&eacute;jours longue dur&eacute;e autoris&eacute;s (28 jours ou plus)",
        "i_selfcheckin": "Auto-enregistrement avec bo&icirc;te &agrave; cl&eacute;s",
    },
    "de/index.html": {
        "section_label": "Ausstattung",
        "section_title": "Was diese Unterkunft bietet",
        "section_subtitle": "Alles, was Sie f&uuml;r einen komfortablen Aufenthalt brauchen &mdash; best&auml;tigt von 63 G&auml;sten auf Airbnb.",
        "show_all": f"Alle {TOTAL_ITEMS} Ausstattungen anzeigen &darr;",
        "h_wifi": "Schnelles WLAN 75&nbsp;Mbps",
        "h_parking": "Kostenlose Parkpl&auml;tze",
        "h_checkin": "Selbstanreise (Schl&uuml;sselsafe)",
        "h_kitchen": "Voll ausgestattete K&uuml;che &amp; Sp&uuml;lmaschine",
        "h_washer": "Waschmaschine &amp; Trockner",
        "h_ac": "Klimaanlage &amp; Heizung",
        "h_workspace": "Arbeitsplatz",
        "h_longterm": "Langzeitaufenthalte willkommen",
        "cat_bathroom": "Badezimmer",
        "cat_bedroom": "Schlafzimmer &amp; W&auml;sche",
        "cat_entertainment": "Unterhaltung",
        "cat_family": "Familie",
        "cat_climate": "Heizung &amp; K&uuml;hlung",
        "cat_safety": "Sicherheit",
        "cat_internet": "Internet &amp; Arbeitsplatz",
        "cat_kitchen": "K&uuml;che &amp; Essbereich",
        "cat_location": "Lage",
        "cat_outdoor": "Drau&szlig;en",
        "cat_parking": "Parkplatz",
        "cat_services": "Service",
        "i_hairdryer": "F&ouml;hn",
        "i_cleaning": "Reinigungsprodukte",
        "i_shampoo": "Shampoo",
        "i_bodysoap": "Duschseife",
        "i_hotwater": "Warmwasser",
        "i_washer_unit": "Waschmaschine (in der Wohnung)",
        "i_dryer": "Trockner",
        "i_essentials": "Grundausstattung &mdash; Handt&uuml;cher, Bettw&auml;sche, Seife, Toilettenpapier",
        "i_hangers": "Kleiderb&uuml;gel",
        "i_bedlinens": "Bettw&auml;sche",
        "i_cottonlinens": "Baumwoll-Bettw&auml;sche",
        "i_extrabedding": "Zus&auml;tzliche Kissen und Decken",
        "i_blackoutshades": "Verdunklungsrollos",
        "i_iron": "B&uuml;geleisen",
        "i_dryingrack": "W&auml;schest&auml;nder",
        "i_safe": "Tresor",
        "i_closet": "Aufbewahrung: Kleiderschrank",
        "i_ethernet": "Ethernet-Anschluss",
        "i_tv": "Fernseher",
        "i_console_ps3": "Spielkonsole: PlayStation 3",
        "i_windowguards": "Fenstersicherungen",
        "i_outletcovers": "Steckdosenschutz",
        "i_ac": "Klimaanlage",
        "i_heating": "Heizung",
        "i_securitycams": "&Uuml;berwachungskameras au&szlig;en",
        "i_outdoorwebcams": "Webcams au&szlig;en &mdash; Parkplatz und Ank&uuml;nfte",
        "i_smokealarm": "Rauchmelder",
        "i_fireextinguisher": "Feuerl&ouml;scher",
        "i_firstaid": "Erste-Hilfe-Set",
        "i_fastwifi": "Schnelles WLAN 75&nbsp;Mbps &mdash; verifiziert, 4K-Streaming und Videocalls",
        "i_workspace_common": "Arbeitsplatz (in einem Gemeinschaftsbereich)",
        "i_kitchen_cook": "K&uuml;che &mdash; selbst kochen",
        "i_fridge": "Electrolux K&uuml;hlschrank",
        "i_microwave": "Mikrowelle",
        "i_cookingbasics": "Kochgrundausstattung &mdash; T&ouml;pfe, Pfannen, &Ouml;l, Salz, Pfeffer",
        "i_dishes": "Geschirr &amp; Besteck &mdash; Sch&uuml;sseln, Essst&auml;bchen, Teller, Tassen",
        "i_freezer": "Gefrierschrank",
        "i_dishwasher": "Sp&uuml;lmaschine",
        "i_stove": "Herd",
        "i_oven": "Electrolux Backofen",
        "i_kettle": "Wasserkocher",
        "i_coffeemaker": "Filterkaffeemaschine",
        "i_wineglasses": "Weingl&auml;ser",
        "i_toaster": "Toaster",
        "i_ricemaker": "Reiskocher",
        "i_diningtable": "Esstisch",
        "i_coffee": "Kaffee",
        "i_privateentrance": "Privater Eingang &mdash; eigener Stra&szlig;en- oder Geb&auml;udezugang",
        "i_patio": "Gemeinschaftliche Terrasse oder Balkon",
        "i_outdoorfurniture": "Au&szlig;enm&ouml;bel",
        "i_freeparking": "Kostenlose Parkpl&auml;tze",
        "i_longterm": "Langzeitaufenthalte erlaubt (28 Tage oder mehr)",
        "i_selfcheckin": "Selbstanreise mit Schl&uuml;sselsafe",
    },
    "pl/index.html": {
        "section_label": "Udogodnienia",
        "section_title": "Co oferuje to miejsce",
        "section_subtitle": "Wszystko, czego potrzebujesz na komfortowy pobyt &mdash; potwierdzone przez 63 go&#347;ci na Airbnb.",
        "show_all": f"Poka&#380; wszystkie {TOTAL_ITEMS} udogodnie&#324; &darr;",
        "h_wifi": "Szybkie Wi-Fi 75&nbsp;Mbps",
        "h_parking": "Bezp&#322;atny parking",
        "h_checkin": "Samodzielne zameldowanie (skrytka)",
        "h_kitchen": "Pe&#322;na kuchnia &amp; zmywarka",
        "h_washer": "Pralka &amp; suszarka",
        "h_ac": "Klimatyzacja &amp; ogrzewanie",
        "h_workspace": "Miejsce do pracy",
        "h_longterm": "Pobyty d&#322;ugoterminowe mile widziane",
        "cat_bathroom": "&#321;azienka",
        "cat_bedroom": "Sypialnia &amp; pranie",
        "cat_entertainment": "Rozrywka",
        "cat_family": "Rodzina",
        "cat_climate": "Ogrzewanie &amp; klimatyzacja",
        "cat_safety": "Bezpiecze&#324;stwo",
        "cat_internet": "Internet &amp; praca",
        "cat_kitchen": "Kuchnia &amp; jadalnia",
        "cat_location": "Lokalizacja",
        "cat_outdoor": "Na zewn&#261;trz",
        "cat_parking": "Parking",
        "cat_services": "Us&#322;ugi",
        "i_hairdryer": "Suszarka do w&#322;os&oacute;w",
        "i_cleaning": "&#346;rodki czysto&#347;ci",
        "i_shampoo": "Szampon",
        "i_bodysoap": "Mydeko do cia&#322;a",
        "i_hotwater": "Gor&#261;ca woda",
        "i_washer_unit": "Pralka (w mieszkaniu)",
        "i_dryer": "Suszarka",
        "i_essentials": "Podstawowe &mdash; r&#281;czniki, po&#347;ciel, myd&#322;o, papier toaletowy",
        "i_hangers": "Wieszaki",
        "i_bedlinens": "Po&#347;ciel",
        "i_cottonlinens": "Po&#347;ciel bawe&#322;niana",
        "i_extrabedding": "Dodatkowe poduszki i koce",
        "i_blackoutshades": "Zas&#322;ony zaciemniaj&#261;ce",
        "i_iron": "&#379;elazko",
        "i_dryingrack": "Suszarka na pranie",
        "i_safe": "Sejf",
        "i_closet": "Przechowywanie: szafa i garderoba",
        "i_ethernet": "Po&#322;&#261;czenie Ethernet",
        "i_tv": "Telewizor",
        "i_console_ps3": "Konsola do gier: PlayStation 3",
        "i_windowguards": "Zabezpieczenia okien",
        "i_outletcovers": "Os&#322;ony gniazdek",
        "i_ac": "Klimatyzacja",
        "i_heating": "Ogrzewanie",
        "i_securitycams": "Zewn&#281;trzne kamery bezpiecze&#324;stwa",
        "i_outdoorwebcams": "Kamery zewn&#281;trzne &mdash; parking i przyjazdy",
        "i_smokealarm": "Czujnik dymu",
        "i_fireextinguisher": "Ga&#347;nica",
        "i_firstaid": "Apteczka pierwszej pomocy",
        "i_fastwifi": "Szybkie Wi-Fi 75&nbsp;Mbps &mdash; zweryfikowane, 4K i rozmowy wideo",
        "i_workspace_common": "Miejsce do pracy (we wsp&oacute;lnej przestrzeni)",
        "i_kitchen_cook": "Kuchnia &mdash; gotuj samodzielnie",
        "i_fridge": "Lod&oacute;wka Electrolux",
        "i_microwave": "Mikrofal&oacute;wka",
        "i_cookingbasics": "Podstawy kuchenne &mdash; garnki, patelnie, olej, s&oacute;l, pieprz",
        "i_dishes": "Naczynia &amp; sztu&#263;ce &mdash; miski, pa&#322;eczki, talerze, kubki",
        "i_freezer": "Zamra&#380;arka",
        "i_dishwasher": "Zmywarka",
        "i_stove": "Kuchenka",
        "i_oven": "Piekarnik Electrolux",
        "i_kettle": "Czajnik",
        "i_coffeemaker": "Ekspres przelewowy",
        "i_wineglasses": "Kieliszki do wina",
        "i_toaster": "Toster",
        "i_ricemaker": "Maszynka do ry&#380;u",
        "i_diningtable": "St&oacute;&#322; jadalniany",
        "i_coffee": "Kawa",
        "i_privateentrance": "Prywatne wej&#347;cie &mdash; oddzielna ulica lub wej&#347;cie do budynku",
        "i_patio": "Wsp&oacute;lny taras lub balkon",
        "i_outdoorfurniture": "Meble ogrodowe",
        "i_freeparking": "Bezp&#322;atny parking",
        "i_longterm": "Pobyty d&#322;ugoterminowe dozwolone (28 dni lub wi&#281;cej)",
        "i_selfcheckin": "Samodzielne zameldowanie ze skrytk&#261;",
    },
    "ro/index.html": {
        "section_label": "Dot&#259;ri",
        "section_title": "Ce ofer&#259; aceast&#259; loca&#539;ie",
        "section_subtitle": "Tot ce ai nevoie pentru un sejur confortabil &mdash; verificat de 63 de oaspe&#539;i pe Airbnb.",
        "show_all": f"Arat&#259; toate cele {TOTAL_ITEMS} dot&#259;ri &darr;",
        "h_wifi": "Wi-Fi rapid 75&nbsp;Mbps",
        "h_parking": "Parcare gratuit&#259;",
        "h_checkin": "Self check-in (cutie cu cheie)",
        "h_kitchen": "Buc&#259;t&#259;rie complet&#259; &amp; ma&#537;in&#259; de sp&#259;lat vase",
        "h_washer": "Ma&#537;in&#259; de sp&#259;lat &amp; usc&#259;tor",
        "h_ac": "Aer condi&#539;ionat &amp; &icirc;nc&#259;lzire",
        "h_workspace": "Spa&#539;iu de lucru",
        "h_longterm": "Sejururi lungi binevenite",
        "cat_bathroom": "Baie",
        "cat_bedroom": "Dormitor &amp; sp&#259;l&#259;torie",
        "cat_entertainment": "Divertisment",
        "cat_family": "Familie",
        "cat_climate": "&Icirc;nc&#259;lzire &amp; r&#259;cire",
        "cat_safety": "Siguran&#539;&#259;",
        "cat_internet": "Internet &amp; spa&#539;iu de lucru",
        "cat_kitchen": "Buc&#259;t&#259;rie &amp; sufragerie",
        "cat_location": "Loca&#539;ie",
        "cat_outdoor": "Exterior",
        "cat_parking": "Parcare",
        "cat_services": "Servicii",
        "i_hairdryer": "Usc&#259;tor de p&#259;r",
        "i_cleaning": "Produse de cur&#259;&#539;enie",
        "i_shampoo": "&#350;ampon",
        "i_bodysoap": "S&#259;pun de corp",
        "i_hotwater": "Ap&#259; cald&#259;",
        "i_washer_unit": "Ma&#537;in&#259; de sp&#259;lat (&icirc;n unitate)",
        "i_dryer": "Usc&#259;tor",
        "i_essentials": "Esen&#539;iale &mdash; prosoape, lenjerie, s&#259;pun, h&acirc;rtie igienic&#259;",
        "i_hangers": "Umera&#537;e",
        "i_bedlinens": "Lenjerie de pat",
        "i_cottonlinens": "Lenjerie din bumbac",
        "i_extrabedding": "Perne &#537;i p&#259;turi suplimentare",
        "i_blackoutshades": "Jaluzele opace",
        "i_iron": "Fier de c&#259;lcat",
        "i_dryingrack": "Uscator de rufe",
        "i_safe": "Seif",
        "i_closet": "Depozitare: dulap &#537;i &#537;ifonier",
        "i_ethernet": "Conexiune Ethernet",
        "i_tv": "Televizor",
        "i_console_ps3": "Consol&#259; de jocuri: PlayStation 3",
        "i_windowguards": "Sisteme de siguran&#539;&#259; pentru ferestre",
        "i_outletcovers": "Capace pentru prize",
        "i_ac": "Aer condi&#539;ionat",
        "i_heating": "&Icirc;nc&#259;lzire",
        "i_securitycams": "Camere de securitate exterioare",
        "i_outdoorwebcams": "Camere web exterioare &mdash; parcare &#537;i sosiri",
        "i_smokealarm": "Detector de fum",
        "i_fireextinguisher": "Stingator de incendiu",
        "i_firstaid": "Trus&#259; de prim ajutor",
        "i_fastwifi": "Wi-Fi rapid 75&nbsp;Mbps &mdash; verificat, 4K &#537;i apeluri video",
        "i_workspace_common": "Spa&#539;iu de lucru dedicat (&icirc;n spa&#539;iu comun)",
        "i_kitchen_cook": "Buc&#259;t&#259;rie &mdash; g&#259;te&#537;te-&#539;i mesele",
        "i_fridge": "Frigider Electrolux",
        "i_microwave": "Cuptor cu microunde",
        "i_cookingbasics": "Elemente de baz&#259; &mdash; oale, tig&#259;i, ulei, sare, piper",
        "i_dishes": "Vesel&#259; &amp; tac&acirc;muri &mdash; boluri, be&#539;i&#537;oare, farfurii, ce&#537;ti",
        "i_freezer": "Congelator",
        "i_dishwasher": "Ma&#537;in&#259; de sp&#259;lat vase",
        "i_stove": "Aragaz",
        "i_oven": "Cuptor Electrolux",
        "i_kettle": "Fierb&#259;tor de ap&#259;",
        "i_coffeemaker": "Cafetier&#259; cu filtru",
        "i_wineglasses": "Pahare de vin",
        "i_toaster": "Pr&#259;jitor de p&acirc;ine",
        "i_ricemaker": "Aparat pentru orez",
        "i_diningtable": "Mas&#259; de luat masa",
        "i_coffee": "Cafea",
        "i_privateentrance": "Intrare privat&#259; &mdash; strad&#259; sau cl&#259;dire separat&#259;",
        "i_patio": "Teras&#259; sau balcon comun",
        "i_outdoorfurniture": "Mobilier de exterior",
        "i_freeparking": "Parcare gratuit&#259; pe proprietate",
        "i_longterm": "Sejururi lungi permise (28 de zile sau mai mult)",
        "i_selfcheckin": "Self check-in cu cutie cu cheie",
    },
}

NEW_CSS = """
        /* Amenities section */
        #amenities {
            background: var(--color-bg);
            padding: 5rem 0;
        }
        .amenities-highlights {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.2rem;
            margin-top: 2.5rem;
            margin-bottom: 2.5rem;
        }
        .amenity-highlight {
            background: var(--color-card);
            padding: 1.4rem 1rem;
            border-radius: 10px;
            border: 1px solid var(--color-border);
            text-align: center;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .amenity-highlight:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        }
        .amenity-highlight-icon {
            font-size: 2rem;
            display: block;
            margin-bottom: 0.5rem;
        }
        .amenity-highlight-title {
            font-size: 0.92rem;
            font-weight: 600;
            color: var(--color-heading);
            line-height: 1.35;
        }
        .amenities-details {
            margin-top: 1rem;
            border-top: 1px solid var(--color-border);
            padding-top: 1.5rem;
        }
        .amenities-details > summary {
            cursor: pointer;
            color: var(--color-accent);
            font-weight: 500;
            font-size: 1rem;
            padding: 0.5rem 0;
            list-style: none;
            text-align: center;
        }
        .amenities-details > summary::-webkit-details-marker { display: none; }
        .amenities-details > summary:hover { color: var(--color-accent-hover); }
        .amenities-details[open] > summary { margin-bottom: 1.5rem; }
        .amenities-categories {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem 2rem;
        }
        .amenity-category h3 {
            font-size: 1rem;
            color: var(--color-heading);
            margin: 0 0 0.7rem;
            padding-bottom: 0.4rem;
            border-bottom: 1px solid var(--color-border);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .amenity-category ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .amenity-category li {
            padding: 0.25rem 0;
            font-size: 0.9rem;
            color: var(--color-text);
            line-height: 1.45;
        }
        .amenity-category li::before {
            content: "\\2713";
            color: var(--color-accent);
            margin-right: 0.5rem;
            font-weight: bold;
        }
"""


def build_section(t: dict) -> str:
    # Highlights grid
    highlights_html = "\n".join(
        f'            <div class="amenity-highlight">\n'
        f'                <span class="amenity-highlight-icon">{h["icon"]}</span>\n'
        f'                <div class="amenity-highlight-title">{t[h["key"]]}</div>\n'
        f'            </div>'
        for h in HIGHLIGHTS
    )

    # Categorized full list
    cats_html_parts = []
    for c in CATEGORIES:
        items_html = "\n".join(
            f'                    <li>{t[item_key]}</li>' for item_key in c["items"]
        )
        cats_html_parts.append(
            f'            <div class="amenity-category">\n'
            f'                <h3><span>{c["icon"]}</span>{t[c["key"]]}</h3>\n'
            f'                <ul>\n{items_html}\n                </ul>\n'
            f'            </div>'
        )
    cats_html = "\n".join(cats_html_parts)

    return (
        '<!-- Amenities -->\n'
        '<section id="amenities">\n'
        '    <div class="section-inner">\n'
        f'        <span class="section-label">{t["section_label"]}</span>\n'
        f'        <h2 class="section-title">{t["section_title"]}</h2>\n'
        f'        <p class="section-subtitle">{t["section_subtitle"]}</p>\n'
        '        <div class="amenities-highlights">\n'
        f'{highlights_html}\n'
        '        </div>\n'
        '        <details class="amenities-details">\n'
        f'            <summary>{t["show_all"]}</summary>\n'
        '            <div class="amenities-categories">\n'
        f'{cats_html}\n'
        '            </div>\n'
        '        </details>\n'
        '    </div>\n'
        '</section>\n\n'
    )


PRICES_ANCHOR = '<section id="prices">'
STYLE_CLOSE = '</style>'


def process(path: Path, key: str) -> dict:
    text = path.read_text(encoding="utf-8")
    t = I18N[key]
    before = text
    ops = []

    # CSS injection — exactly one <style> block, marker = .amenity-highlight
    if ".amenity-highlight" in text:
        ops.append("css-skip")
    else:
        n = text.count(STYLE_CLOSE)
        if n == 1:
            text = text.replace(STYLE_CLOSE, NEW_CSS + "    " + STYLE_CLOSE, 1)
            ops.append("css")
        else:
            ops.append(f"!css-aborted-{n}-style-tags")

    # Amenities section — insert before <section id="prices">
    if 'id="amenities"' in text:
        ops.append("section-skip")
    elif PRICES_ANCHOR in text:
        text = text.replace(PRICES_ANCHOR, build_section(t) + PRICES_ANCHOR, 1)
        ops.append("section")
    else:
        ops.append("!prices-anchor-missing")

    if text != before:
        path.write_text(text, encoding="utf-8")
        return {"file": key, "changed": True, "ops": ops}
    return {"file": key, "changed": False, "ops": ops}


def main():
    print("=" * 78)
    print(f"Building amenities section: 8 highlights + {len(CATEGORIES)} categories ({TOTAL_ITEMS} items)")
    print("=" * 78)
    for key in I18N:
        result = process(REPO / key, key)
        marker = "OK " if result["changed"] else "-- "
        ops = ", ".join(result["ops"])
        print(f"{marker} {result['file']:25s} -> {ops}")
    print("=" * 78)


if __name__ == "__main__":
    main()
