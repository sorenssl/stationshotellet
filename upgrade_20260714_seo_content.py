# -*- coding: utf-8 -*-
"""Tourist-SEO + content upgrade, 2026-07-14 — applies to all 6 language versions.

What it does (per file):
  HEAD:  new <title> + <meta description> with Swedish Lapland tourist keywords;
         og:image / twitter:image -> aurora share card (1200x630);
         favicon + apple-touch-icon links; preload of the new hero image.
  JSON-LD: EN: patch LodgingBusiness (real logo, sameAs Airbnb, hasMap, aurora image)
              + append 3 tourist Q&As to FAQPage.
           SV/FR/DE/PL/RO: replace the thin legacy LodgingBusiness with the full
              enriched schema (translated description) + add a translated FAQPage
              (these pages never got the May 2026 enrichment — EN-only back then).
  BODY:  hero badge + hero paragraph (northern lights / Pite Havsbad / Lapland);
         experiences intro rewritten with tourist keywords;
         Pite Havsbad distance corrected: ~5 km -> ~15 km (real driving distance
         from Öjebyn — verified 2026-07-14; 5 km was the distance from central Piteå);
         new visible FAQ section (6 Q&As, matches FAQPage schema);
         entrance-veranda photo added to gallery + slideshow;
         aurora photo added to slideshow; hero click now opens it.
  SITEMAP: lastmod bumped.

Usage: python upgrade_20260714_seo_content.py    (run from repo root)
NOT idempotent — run exactly once on the pre-upgrade tree (tag: pre-upgrade-2026-07-14).
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
SITE = "https://stationshotellet.com"
OG_IMAGE = f"{SITE}/images/og-image-aurora.jpg"
LASTMOD = "2026-07-14T17:15:00Z"

ERRORS = []


def sub1(text, pattern, repl, desc, fname, flags=0):
    """Replace exactly one occurrence or record an error."""
    new, n = re.subn(pattern, lambda m: repl, text, flags=flags)
    if n != 1:
        ERRORS.append(f"{fname}: {desc} matched {n} times (expected 1)")
        return text
    return new


def js_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


# ---------------------------------------------------------------- language data
L = {
    "en": dict(
        file="index.html",
        title="Stations Hotellet — Apartment in Öjebyn, Piteå · Swedish Lapland",
        desc="2-bedroom apartment in a converted railway station in Öjebyn, Piteå. Northern lights in winter, Pite Havsbad beach in summer. From 990 kr/night all-inclusive.",
        og_alt="Northern lights over the street at Stations Hotellet in Öjebyn, Piteå — Swedish Lapland",
        badge="Historic Railway Station · Öjebyn, Piteå · Swedish Lapland",
        hero_p="The lowest rates in Öjebyn for a 2-bedroom apartment, sleeps 5. From <strong>990&nbsp;kr/night all-inclusive</strong> — cleaning, Wi-Fi and parking included. Your base for northern lights, Pite Havsbad beaches and Swedish Lapland adventures.",
        exp_sub="Stations Hotellet is your base on the Swedish Lapland coast — northern lights and dog sledding in winter, midnight sun and Pite Havsbad beaches in summer, Piteå old town all year round. Most of it within a 15-minute drive.",
        havsbad_p="Sweden's largest beach resort, ~15 km from us (about 15 min by car). Water park, white sand beach, summer activities for all ages.",
        faq_label="FAQ",
        faq_title="Good to know — questions &amp; answers",
        faq=[
            ("Can you see the northern lights at Stations Hotellet?",
             "Yes — from about September to March, on clear nights, the aurora can appear right over Öjebyn. The photo at the top of this page was taken from our street. Tip: check an aurora forecast app and look up after 21:00, away from street lights."),
            ("How far is Pite Havsbad?",
             "About 15 km — roughly 15 minutes by car. Sweden's largest beach resort (water park, white-sand beach, summer events) makes an easy day trip, and you sleep here for a fraction of the resort price."),
            ("How do I get here from Luleå Airport?",
             "The drive is about 50 km — 40–45 minutes via the E4. All major car-rental brands operate at the airport, and there are direct buses to Piteå; from central Piteå we are a 5-minute drive."),
            ("What is included in the price?",
             "Everything: cleaning, linens, towels, Wi-Fi and private parking. From 990 kr per night for the whole apartment, up to 5 guests. The price you see is the price you pay."),
            ("How does check-in work?",
             "Self check-in with a lockbox at the door — arrive whenever it suits you. The code is emailed before arrival. Check-in from 15:00, check-out by 11:00."),
            ("Can I cancel for free?",
             "Nightly stays: free cancellation up to 3 days before arrival. Weekly stays: up to 7 days before. Monthly stays: 1-month deposit, fully refundable up to 30 days before arrival."),
        ],
        slide_aurora="Northern lights over Öjebyn — photographed from our street",
        slide_entrance="Your private entrance — veranda in summer",
        gal_alt="Private entrance with summer veranda — red wooden railway station building",
        gal_aria="View private entrance photo",
        lodging_desc="Stations Hotellet is a 2-bedroom apartment inside a beautifully converted railway station in Öjebyn, near Piteå in northern Sweden — the Swedish Lapland coast. Sleeps up to 5 guests with full kitchen, two bathrooms, washing machine, in-room safe, free Wi-Fi and parking. Northern lights in winter, Pite Havsbad beach in summer. Lowest direct-book rates in Öjebyn — from 990 kr per night, all-inclusive (cleaning, linens, towels and Wi-Fi included).",
    ),
    "sv": dict(
        file="sv/index.html",
        title="Stations Hotellet — Lägenhet i Öjebyn, Piteå · Norrbotten",
        desc="Lägenhet med 2 sovrum i en ombyggd järnvägsstation i Öjebyn, Piteå. Norrsken på vintern, Pite Havsbad på sommaren. Från 990 kr/natt — allt ingår.",
        og_alt="Norrsken över gatan vid Stations Hotellet i Öjebyn, Piteå",
        badge="Historisk järnvägsstation · Öjebyn, Piteå · Norrbotten",
        hero_p="Lägsta priset i Öjebyn för en lägenhet med 2 sovrum, upp till 5 gäster. Från <strong>990&nbsp;kr/natt — allt ingår</strong>: städning, Wi-Fi och parkering. Perfekt bas för norrsken, Pite Havsbad och äventyr i Norrbotten.",
        exp_sub="Stations Hotellet är din bas vid Norrbottenskusten — norrsken och hundspann på vintern, midnattssol och Pite Havsbads stränder på sommaren, Piteås gamla stad året om. Det mesta inom 15 minuter med bil.",
        havsbad_p="Sveriges största havsbad, ca 15 km från oss (ca 15 min med bil). Äventyrsbad, sandstrand och sommaraktiviteter för alla åldrar.",
        faq_label="Vanliga frågor",
        faq_title="Bra att veta — frågor &amp; svar",
        faq=[
            ("Kan man se norrsken vid Stations Hotellet?",
             "Ja — från ungefär september till mars kan norrskenet visa sig rakt över Öjebyn under klara nätter. Bilden högst upp på sidan är tagen från vår gata. Tips: kolla en norrskensprognos-app och titta upp efter kl 21, en bit från gatubelysningen."),
            ("Hur långt är det till Pite Havsbad?",
             "Cirka 15 km — ungefär 15 minuter med bil. Sveriges största havsbad (äventyrsbad, sandstrand, sommarevenemang) som dagsutflykt — och du bor här för en bråkdel av priset."),
            ("Hur tar jag mig hit från Luleå Airport?",
             "Bilresan är cirka 50 km — 40–45 minuter via E4. Alla stora hyrbilsfirmor finns på flygplatsen, och det går direktbussar till Piteå; från centrala Piteå är det 5 minuter med bil."),
            ("Vad ingår i priset?",
             "Allt: städning, lakan, handdukar, Wi-Fi och egen parkering. Från 990 kr per natt för hela lägenheten, upp till 5 gäster. Priset du ser är priset du betalar."),
            ("Hur fungerar incheckningen?",
             "Självincheckning med nyckelbox vid dörren — kom när det passar dig. Koden mejlas före ankomst. Incheckning från 15:00, utcheckning senast 11:00."),
            ("Kan jag avboka gratis?",
             "Enstaka nätter: gratis avbokning upp till 3 dagar före ankomst. Veckovistelser: upp till 7 dagar före. Månadsvistelser: 1 månads deposition, återbetalas helt vid avbokning 30+ dagar före ankomst."),
        ],
        slide_aurora="Norrsken över Öjebyn — fotograferat från vår gata",
        slide_entrance="Din egen entré — verandan på sommaren",
        gal_alt="Egen entré med sommarveranda — den röda järnvägsstationsbyggnaden",
        gal_aria="Visa bild på egen entré",
        lodging_desc="Stations Hotellet är en lägenhet med 2 sovrum i en vackert ombyggd järnvägsstation i Öjebyn, nära Piteå i Norrbotten. Upp till 5 gäster, fullt utrustat kök, två badrum, tvättmaskin, kassaskåp, gratis Wi-Fi och parkering. Norrsken på vintern, Pite Havsbad på sommaren. Lägsta direktbokningspriserna i Öjebyn — från 990 kr per natt, allt ingår (städning, lakan, handdukar och Wi-Fi).",
    ),
    "fr": dict(
        file="fr/index.html",
        title="Stations Hotellet — Appartement à Piteå · Laponie suédoise",
        desc="Appartement 2 chambres dans une ancienne gare rénovée à Öjebyn, Piteå. Aurores boréales en hiver, plage de Pite Havsbad en été. Dès 990 kr/nuit, tout inclus.",
        og_alt="Aurores boréales au-dessus de la rue du Stations Hotellet à Öjebyn, Piteå — Laponie suédoise",
        badge="Gare historique · Öjebyn, Piteå · Laponie suédoise",
        hero_p="Le meilleur tarif d'Öjebyn pour un appartement 2 chambres, jusqu'à 5 personnes. Dès <strong>990&nbsp;kr/nuit tout inclus</strong> — ménage, Wi-Fi et parking compris. Votre camp de base pour les aurores boréales, Pite Havsbad et la Laponie suédoise.",
        exp_sub="Stations Hotellet est votre camp de base sur la côte de la Laponie suédoise — aurores boréales et chiens de traîneau en hiver, soleil de minuit et plages de Pite Havsbad en été, vieille ville de Piteå toute l'année. L'essentiel à moins de 15 minutes en voiture.",
        havsbad_p="La plus grande station balnéaire de Suède, à ~15 km (env. 15 min en voiture). Parc aquatique, plage de sable blanc, activités estivales pour tous les âges.",
        faq_label="FAQ",
        faq_title="Bon à savoir — questions &amp; réponses",
        faq=[
            ("Peut-on voir des aurores boréales au Stations Hotellet ?",
             "Oui — de septembre à mars environ, par nuit claire, les aurores peuvent apparaître juste au-dessus d'Öjebyn. La photo en haut de cette page a été prise depuis notre rue. Astuce : consultez une appli de prévision d'aurores et levez les yeux après 21 h, à l'écart des lampadaires."),
            ("À quelle distance se trouve Pite Havsbad ?",
             "Environ 15 km — 15 minutes en voiture. La plus grande station balnéaire de Suède (parc aquatique, plage de sable blanc, animations estivales) en excursion à la journée, tout en logeant ici pour une fraction du prix."),
            ("Comment venir depuis l'aéroport de Luleå ?",
             "Environ 50 km — 40 à 45 minutes par la E4. Toutes les grandes agences de location de voitures sont à l'aéroport, et des bus directs desservent Piteå ; depuis le centre de Piteå, nous sommes à 5 minutes en voiture."),
            ("Que comprend le prix ?",
             "Tout : ménage, draps, serviettes, Wi-Fi et parking privé. Dès 990 kr la nuit pour l'appartement entier, jusqu'à 5 personnes. Le prix affiché est le prix payé."),
            ("Comment se passe l'arrivée ?",
             "Arrivée autonome avec boîte à clés à la porte — arrivez quand cela vous convient. Le code est envoyé par e-mail avant l'arrivée. Arrivée à partir de 15 h, départ avant 11 h."),
            ("Puis-je annuler gratuitement ?",
             "Séjours à la nuit : annulation gratuite jusqu'à 3 jours avant l'arrivée. Séjours à la semaine : jusqu'à 7 jours avant. Séjours au mois : dépôt d'un mois, intégralement remboursable jusqu'à 30 jours avant l'arrivée."),
        ],
        slide_aurora="Aurores boréales au-dessus d'Öjebyn — photographiées depuis notre rue",
        slide_entrance="Votre entrée privée — la véranda en été",
        gal_alt="Entrée privée avec véranda en été — bâtiment en bois rouge de la gare",
        gal_aria="Voir la photo de l'entrée privée",
        lodging_desc="Stations Hotellet est un appartement de 2 chambres dans une gare magnifiquement rénovée à Öjebyn, près de Piteå, sur la côte de la Laponie suédoise. Jusqu'à 5 personnes, cuisine équipée, deux salles d'eau, lave-linge, coffre-fort, Wi-Fi et parking gratuits. Aurores boréales en hiver, plage de Pite Havsbad en été. Les meilleurs tarifs en réservation directe à Öjebyn — dès 990 kr la nuit, tout inclus (ménage, draps, serviettes et Wi-Fi).",
    ),
    "de": dict(
        file="de/index.html",
        title="Stations Hotellet — Ferienwohnung Piteå · Schwedisch-Lappland",
        desc="Ferienwohnung mit 2 Schlafzimmern im umgebauten Bahnhof in Öjebyn bei Piteå. Polarlichter im Winter, Pite Havsbad im Sommer. Ab 990 kr/Nacht, alles inklusive.",
        og_alt="Polarlichter über der Straße am Stations Hotellet in Öjebyn, Piteå — Schwedisch-Lappland",
        badge="Historischer Bahnhof · Öjebyn, Piteå · Schwedisch-Lappland",
        hero_p="Der günstigste Preis in Öjebyn für eine Wohnung mit 2 Schlafzimmern, bis zu 5 Gäste. Ab <strong>990&nbsp;kr/Nacht, alles inklusive</strong> — Reinigung, WLAN und Parkplatz inbegriffen. Ihre Basis für Polarlichter, Pite Havsbad und Schwedisch-Lappland.",
        exp_sub="Stations Hotellet ist Ihre Basis an der Küste Schwedisch-Lapplands — Polarlichter und Hundeschlitten im Winter, Mitternachtssonne und die Strände von Pite Havsbad im Sommer, Piteås Altstadt das ganze Jahr. Das meiste in 15 Autominuten erreichbar.",
        havsbad_p="Schwedens größtes Strandresort, ca. 15 km entfernt (rund 15 Autominuten). Erlebnisbad, weißer Sandstrand, Sommeraktivitäten für alle Altersgruppen.",
        faq_label="FAQ",
        faq_title="Gut zu wissen — Fragen &amp; Antworten",
        faq=[
            ("Kann man am Stations Hotellet Polarlichter sehen?",
             "Ja — etwa von September bis März können die Polarlichter in klaren Nächten direkt über Öjebyn erscheinen. Das Foto oben auf dieser Seite wurde von unserer Straße aus aufgenommen. Tipp: Aurora-Vorhersage-App prüfen und nach 21 Uhr abseits der Straßenlaternen nach oben schauen."),
            ("Wie weit ist Pite Havsbad entfernt?",
             "Etwa 15 km — rund 15 Minuten mit dem Auto. Schwedens größtes Strandresort (Erlebnisbad, weißer Sandstrand, Sommerprogramm) als Tagesausflug — und Sie übernachten hier für einen Bruchteil des Resortpreises."),
            ("Wie komme ich vom Flughafen Luleå hierher?",
             "Die Fahrt beträgt etwa 50 km — 40–45 Minuten über die E4. Alle großen Mietwagenfirmen sind am Flughafen vertreten, außerdem fahren Direktbusse nach Piteå; vom Zentrum Piteås sind es 5 Minuten mit dem Auto."),
            ("Was ist im Preis enthalten?",
             "Alles: Endreinigung, Bettwäsche, Handtücher, WLAN und Privatparkplatz. Ab 990 kr pro Nacht für die ganze Wohnung, bis zu 5 Gäste. Der angezeigte Preis ist der Endpreis."),
            ("Wie funktioniert der Check-in?",
             "Self-Check-in mit Schlüsselbox an der Tür — reisen Sie an, wann es Ihnen passt. Der Code kommt vor der Anreise per E-Mail. Check-in ab 15:00, Check-out bis 11:00."),
            ("Kann ich kostenlos stornieren?",
             "Einzelnächte: kostenlose Stornierung bis 3 Tage vor Anreise. Wochenaufenthalte: bis 7 Tage vorher. Monatsaufenthalte: 1 Monatsmiete Kaution, bis 30 Tage vor Anreise voll erstattet."),
        ],
        slide_aurora="Polarlichter über Öjebyn — von unserer Straße aus fotografiert",
        slide_entrance="Ihr privater Eingang — Veranda im Sommer",
        gal_alt="Privater Eingang mit Veranda im Sommer — rotes Holzgebäude des Bahnhofs",
        gal_aria="Foto des privaten Eingangs ansehen",
        lodging_desc="Stations Hotellet ist eine Ferienwohnung mit 2 Schlafzimmern in einem schön umgebauten Bahnhof in Öjebyn bei Piteå, an der Küste Schwedisch-Lapplands. Bis zu 5 Gäste, voll ausgestattete Küche, zwei Bäder, Waschmaschine, Safe, kostenloses WLAN und Parken. Polarlichter im Winter, Pite Havsbad im Sommer. Die günstigsten Direktbuchungspreise in Öjebyn — ab 990 kr pro Nacht, alles inklusive (Reinigung, Bettwäsche, Handtücher und WLAN).",
    ),
    "pl": dict(
        file="pl/index.html",
        title="Stations Hotellet — Apartament Piteå · Szwedzka Laponia",
        desc="Apartament z 2 sypialniami w dawnym dworcu kolejowym w Öjebyn koło Piteå. Zorza polarna zimą, plaża Pite Havsbad latem. Od 990 kr/noc, wszystko w cenie.",
        og_alt="Zorza polarna nad ulicą przy Stations Hotellet w Öjebyn, Piteå — szwedzka Laponia",
        badge="Zabytkowy dworzec kolejowy · Öjebyn, Piteå · Szwedzka Laponia",
        hero_p="Najniższa cena w Öjebyn za apartament z 2 sypialniami, do 5 gości. Od <strong>990&nbsp;kr/noc, wszystko w cenie</strong> — sprzątanie, Wi-Fi i parking. Idealna baza na zorzę polarną, Pite Havsbad i przygody w szwedzkiej Laponii.",
        exp_sub="Stations Hotellet to Twoja baza na wybrzeżu szwedzkiej Laponii — zorza polarna i psie zaprzęgi zimą, słońce o północy i plaże Pite Havsbad latem, stare miasto Piteå przez cały rok. Większość atrakcji w 15 minut samochodem.",
        havsbad_p="Największy nadmorski kurort Szwecji, ok. 15 km od nas (ok. 15 min autem). Park wodny, biała plaża i letnie atrakcje dla każdego.",
        faq_label="FAQ",
        faq_title="Warto wiedzieć — pytania i odpowiedzi",
        faq=[
            ("Czy przy Stations Hotellet widać zorzę polarną?",
             "Tak — mniej więcej od września do marca, w pogodne noce, zorza potrafi pojawić się wprost nad Öjebyn. Zdjęcie na górze tej strony zostało zrobione z naszej ulicy. Wskazówka: sprawdź aplikację z prognozą zorzy i spójrz w niebo po 21:00, z dala od latarni."),
            ("Jak daleko jest Pite Havsbad?",
             "Około 15 km — mniej więcej 15 minut samochodem. Największy nadmorski kurort Szwecji (park wodny, biała plaża, letnie wydarzenia) na wycieczkę na cały dzień, a nocujesz u nas za ułamek ceny kurortu."),
            ("Jak dojechać z lotniska Luleå?",
             "Trasa to około 50 km — 40–45 minut drogą E4. Na lotnisku działają wszystkie duże wypożyczalnie aut, kursują też bezpośrednie autobusy do Piteå; z centrum Piteå jesteśmy 5 minut samochodem."),
            ("Co jest wliczone w cenę?",
             "Wszystko: sprzątanie, pościel, ręczniki, Wi-Fi i prywatny parking. Od 990 kr za noc za cały apartament, do 5 gości. Cena, którą widzisz, to cena, którą płacisz."),
            ("Jak wygląda zameldowanie?",
             "Samodzielne zameldowanie — skrytka na klucze przy drzwiach, przyjedź o dowolnej porze. Kod wysyłamy e-mailem przed przyjazdem. Zameldowanie od 15:00, wymeldowanie do 11:00."),
            ("Czy mogę bezpłatnie anulować?",
             "Pojedyncze noce: bezpłatne anulowanie do 3 dni przed przyjazdem. Pobyty tygodniowe: do 7 dni. Pobyty miesięczne: kaucja w wysokości 1 miesiąca, w pełni zwracana do 30 dni przed przyjazdem."),
        ],
        slide_aurora="Zorza polarna nad Öjebyn — sfotografowana z naszej ulicy",
        slide_entrance="Twoje prywatne wejście — weranda latem",
        gal_alt="Prywatne wejście z werandą latem — czerwony drewniany budynek dworca",
        gal_aria="Zobacz zdjęcie prywatnego wejścia",
        lodging_desc="Stations Hotellet to apartament z 2 sypialniami w pięknie przebudowanym dworcu kolejowym w Öjebyn koło Piteå, na wybrzeżu szwedzkiej Laponii. Do 5 gości, w pełni wyposażona kuchnia, dwie łazienki, pralka, sejf, bezpłatne Wi-Fi i parking. Zorza polarna zimą, Pite Havsbad latem. Najniższe ceny rezerwacji bezpośredniej w Öjebyn — od 990 kr za noc, wszystko w cenie (sprzątanie, pościel, ręczniki i Wi-Fi).",
    ),
    "ro": dict(
        file="ro/index.html",
        title="Stations Hotellet — Apartament Piteå · Laponia Suedeză",
        desc="Apartament cu 2 dormitoare într-o gară renovată din Öjebyn, lângă Piteå. Aurora boreală iarna, plaja Pite Havsbad vara. De la 990 kr/noapte, totul inclus.",
        og_alt="Aurora boreală deasupra străzii de la Stations Hotellet din Öjebyn, Piteå — Laponia suedeză",
        badge="Gară istorică · Öjebyn, Piteå · Laponia Suedeză",
        hero_p="Cel mai bun preț din Öjebyn pentru un apartament cu 2 dormitoare, până la 5 oaspeți. De la <strong>990&nbsp;kr/noapte, totul inclus</strong> — curățenie, Wi-Fi și parcare. Baza ta pentru aurora boreală, Pite Havsbad și aventuri în Laponia suedeză.",
        exp_sub="Stations Hotellet este baza ta pe coasta Laponiei suedeze — aurora boreală și săniile trase de câini iarna, soarele de la miezul nopții și plajele Pite Havsbad vara, orașul vechi Piteå tot anul. Aproape totul la 15 minute cu mașina.",
        havsbad_p="Cea mai mare stațiune de plajă din Suedia, la ~15 km de noi (circa 15 min cu mașina). Parc acvatic, plajă cu nisip alb, activități de vară pentru toate vârstele.",
        faq_label="Întrebări frecvente",
        faq_title="Bine de știut — întrebări și răspunsuri",
        faq=[
            ("Se poate vedea aurora boreală la Stations Hotellet?",
             "Da — cam din septembrie până în martie, în nopțile senine, aurora poate apărea chiar deasupra Öjebyn. Fotografia din partea de sus a paginii a fost făcută de pe strada noastră. Sfat: verifică o aplicație de prognoză a aurorei și privește cerul după ora 21:00, departe de felinare."),
            ("Cât de departe este Pite Havsbad?",
             "Circa 15 km — aproximativ 15 minute cu mașina. Cea mai mare stațiune de plajă din Suedia (parc acvatic, plajă cu nisip alb, evenimente de vară) într-o excursie de o zi, iar tu dormi aici la o fracțiune din prețul stațiunii."),
            ("Cum ajung de la aeroportul Luleå?",
             "Drumul are circa 50 km — 40–45 de minute pe E4. Toate marile firme de închirieri auto sunt la aeroport și există autobuze directe spre Piteå; din centrul orașului Piteå suntem la 5 minute cu mașina."),
            ("Ce este inclus în preț?",
             "Totul: curățenie, lenjerie, prosoape, Wi-Fi și parcare privată. De la 990 kr pe noapte pentru întregul apartament, până la 5 oaspeți. Prețul afișat este prețul plătit."),
            ("Cum funcționează check-in-ul?",
             "Self check-in cu cutie de chei la ușă — sosește când îți convine. Codul se trimite pe e-mail înainte de sosire. Check-in de la 15:00, check-out până la 11:00."),
            ("Pot anula gratuit?",
             "Nopți individuale: anulare gratuită cu până la 3 zile înainte de sosire. Sejururi de o săptămână: cu până la 7 zile înainte. Sejururi lunare: garanție de o lună, rambursată integral cu 30+ zile înainte de sosire."),
        ],
        slide_aurora="Aurora boreală deasupra Öjebyn — fotografiată de pe strada noastră",
        slide_entrance="Intrarea ta privată — veranda vara",
        gal_alt="Intrare privată cu verandă vara — clădirea roșie din lemn a gării",
        gal_aria="Vezi fotografia intrării private",
        lodging_desc="Stations Hotellet este un apartament cu 2 dormitoare într-o gară frumos renovată din Öjebyn, lângă Piteå, pe coasta Laponiei suedeze. Până la 5 oaspeți, bucătărie complet utilată, două băi, mașină de spălat, seif, Wi-Fi și parcare gratuite. Aurora boreală iarna, Pite Havsbad vara. Cele mai bune prețuri la rezervare directă în Öjebyn — de la 990 kr pe noapte, totul inclus (curățenie, lenjerie, prosoape și Wi-Fi).",
    ),
}


# ------------------------------------------------------- enriched LodgingBusiness
def lodging_schema(lang, desc):
    return {
        "@context": "https://schema.org",
        "@type": "LodgingBusiness",
        "@id": f"{SITE}/#lodging",
        "name": "Stations Hotellet",
        "alternateName": "Stations Hotellet Öjebyn",
        "slogan": "A unique stay in a converted railway station near Piteå",
        "description": desc,
        "inLanguage": lang,
        "url": f"{SITE}/",
        "sameAs": [
            "https://www.airbnb.com/h/big-apartment-free-parking-6-beds-host-soren-doushka"
        ],
        "hasMap": "https://www.google.com/maps?q=V%C3%A4stra+J%C3%A4rnv%C3%A4gsgatan+5,+943+31+%C3%96jebyn,+Sweden",
        "image": [
            f"{SITE}/images/full/exterior-aurora.jpg",
            f"{SITE}/images/full/kitchen-dining-wide.jpg",
            f"{SITE}/images/full/master-bedroom.jpg",
            f"{SITE}/images/full/living-room-2.jpg",
        ],
        "logo": f"{SITE}/images/brand/logo-256.png",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Västra Järnvägsgatan 5",
            "addressLocality": "Öjebyn",
            "addressRegion": "Norrbotten",
            "postalCode": "943 31",
            "addressCountry": "SE",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 65.3541171, "longitude": 21.3795471},
        "telephone": ["+46706718185", "+46721865083"],
        "email": "posetivemind67@gmail.com",
        "priceRange": "990–14000 SEK",
        "currenciesAccepted": "SEK, EUR",
        "paymentAccepted": "Bank transfer, Swish, Cash",
        "checkinTime": "15:00",
        "checkoutTime": "11:00",
        "numberOfRooms": 2,
        "numberOfBedrooms": 2,
        "occupancy": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 5},
        "petsAllowed": False,
        "smokingAllowed": False,
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": n, "value": True}
            for n in [
                "Free Wi-Fi", "Free private parking", "Fully equipped kitchen",
                "Washing machine", "Separate shower room", "In-room safe",
                "Fresh linens and towels", "Self check-in", "Cleaning included",
            ]
        ],
        "makesOffer": [
            {
                "@type": "Offer",
                "name": "Nightly rate",
                "description": "Whole apartment, up to 5 guests, all-inclusive (cleaning, linens, Wi-Fi and parking)",
                "price": "990", "priceCurrency": "SEK",
                "priceSpecification": {
                    "@type": "UnitPriceSpecification", "price": "990",
                    "priceCurrency": "SEK", "unitCode": "DAY", "unitText": "per night",
                },
            },
            {
                "@type": "Offer",
                "name": "Weekly rate",
                "description": "7-night stay, whole apartment, save 21% vs nightly",
                "price": "5500", "priceCurrency": "SEK",
                "priceSpecification": {
                    "@type": "UnitPriceSpecification", "price": "5500",
                    "priceCurrency": "SEK", "unitCode": "WEE", "unitText": "per week",
                },
            },
            {
                "@type": "Offer",
                "name": "Monthly rate",
                "description": "30-night stay for corporate / healthcare guests, weekly cleaning included",
                "price": "14000", "priceCurrency": "SEK",
                "priceSpecification": {
                    "@type": "UnitPriceSpecification", "price": "14000",
                    "priceCurrency": "SEK", "unitCode": "MON", "unitText": "per month",
                },
            },
        ],
        "containsPlace": {
            "@type": "Apartment",
            "name": "Stations Hotellet — 2-bedroom railway station apartment",
            "numberOfRooms": 2,
            "occupancy": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 5},
            "floorSize": {"@type": "QuantitativeValue", "unitCode": "MTK", "value": 75},
            "amenityFeature": [
                {"@type": "LocationFeatureSpecification", "name": n, "value": True}
                for n in [
                    "Master bedroom (double bed)", "Second bedroom (double bed + bunk bed)",
                    "Bathroom", "Separate shower room with washing machine",
                ]
            ],
        },
    }


def faq_schema(faq):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }


def dump_ld(obj):
    return json.dumps(obj, ensure_ascii=False, indent=4)


HEAD_LINKS = """    <link rel="icon" href="/favicon.ico" sizes="48x48">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="preload" as="image" href="/images/full/exterior-aurora.webp" type="image/webp" fetchpriority="high">"""


def build_faq_section(d):
    items = "\n".join(
        f"""            <details class="faq-item">
                <summary>{q}</summary>
                <p>{a}</p>
            </details>"""
        for q, a in d["faq"]
    )
    return f"""<!-- FAQ -->
<section id="faq">
    <div class="section-inner">
        <span class="section-label">{d["faq_label"]}</span>
        <h2 class="section-title">{d["faq_title"]}</h2>
        <div class="faq-list">
{items}
        </div>
    </div>
</section>

"""


def gallery_item(d):
    return f"""
            <div class="gallery-item" onclick="openSlideshow(15)" role="button" tabindex="0" aria-label="{d["gal_aria"]}">
                <picture>
                    <source srcset="/images/thumb/entrance-veranda.webp" type="image/webp">
                    <img src="/images/thumb/entrance-veranda.jpg" alt="{d["gal_alt"]}" loading="lazy">
                </picture>
            </div>"""


def ld_blocks(text):
    """Return list of (start, end, inner) for every ld+json script block."""
    out = []
    for m in re.finditer(
        r'<script type="application/ld\+json">([\s\S]*?)</script>', text
    ):
        out.append((m.start(), m.end(), m.group(1)))
    return out


def process(lang, d):
    path = REPO / d["file"]
    text = path.read_text(encoding="utf-8")
    fname = d["file"]

    # ---- head
    text = sub1(text, r"<title>[\s\S]*?</title>", f"<title>{d['title']}</title>",
                "title", fname)
    text = sub1(text, r'<meta name="description" content="[^"]*">',
                f'<meta name="description" content="{d["desc"]}">', "description", fname)
    text = sub1(text, r'<meta property="og:image" content="[^"]*">',
                f'<meta property="og:image" content="{OG_IMAGE}">', "og:image", fname)
    text = sub1(text, r'<meta property="og:image:alt" content="[^"]*">',
                f'<meta property="og:image:alt" content="{d["og_alt"]}">', "og:image:alt", fname)
    text = sub1(text, r'<meta name="twitter:image" content="[^"]*">',
                f'<meta name="twitter:image" content="{OG_IMAGE}">', "twitter:image", fname)
    if 'og:image:width' not in text:
        text = sub1(text, r'(<meta property="og:image:alt" content="[^"]*">)',
                    f'<meta property="og:image:alt" content="{d["og_alt"]}">\n'
                    '    <meta property="og:image:width" content="1200">\n'
                    '    <meta property="og:image:height" content="630">',
                    "og:image dimensions insert", fname)
    text = sub1(text, r'(<meta name="theme-color" content="[^"]*">)',
                '<meta name="theme-color" content="#2c2416">\n' + HEAD_LINKS,
                "favicon/preload links", fname)

    # ---- JSON-LD
    blocks = ld_blocks(text)
    if lang == "en":
        if len(blocks) != 3:
            ERRORS.append(f"{fname}: expected 3 ld+json blocks, found {len(blocks)}")
        else:
            lodging = json.loads(blocks[0][2])
            lodging["description"] = d["lodging_desc"]
            lodging["inLanguage"] = "en"
            lodging["logo"] = f"{SITE}/images/brand/logo-256.png"
            lodging["sameAs"] = [
                "https://www.airbnb.com/h/big-apartment-free-parking-6-beds-host-soren-doushka"
            ]
            lodging["hasMap"] = "https://www.google.com/maps?q=V%C3%A4stra+J%C3%A4rnv%C3%A4gsgatan+5,+943+31+%C3%96jebyn,+Sweden"
            lodging["image"] = [f"{SITE}/images/full/exterior-aurora.jpg"] + lodging["image"]
            faq = json.loads(blocks[1][2])
            extra = faq_schema(d["faq"][:3])["mainEntity"]  # 3 new tourist Q&As
            faq["mainEntity"] = faq["mainEntity"] + extra
            # splice back (reverse order so offsets stay valid)
            s0, e0, _ = blocks[0]
            s1, e1, _ = blocks[1]
            new_faq = f'<script type="application/ld+json">\n{dump_ld(faq)}\n    </script>'
            text = text[:s1] + new_faq + text[e1:]
            new_lodging = f'<script type="application/ld+json">\n{dump_ld(lodging)}\n    </script>'
            text = text[:s0] + new_lodging + text[e0:]
    else:
        if len(blocks) != 1:
            ERRORS.append(f"{fname}: expected 1 ld+json block, found {len(blocks)}")
        else:
            s0, e0, _ = blocks[0]
            new = (
                f'<script type="application/ld+json">\n'
                f'{dump_ld(lodging_schema(lang, d["lodging_desc"]))}\n    </script>\n'
                f'    <script type="application/ld+json">\n'
                f'{dump_ld(faq_schema(d["faq"]))}\n    </script>'
            )
            text = text[:s0] + new + text[e0:]

    # ---- body
    text = sub1(text, r'(<span class="hero-badge">)[\s\S]*?(</span>)',
                f'<span class="hero-badge">{d["badge"]}</span>', "hero badge", fname)
    # hero paragraph — keep group 1 via function
    new, n = re.subn(
        r'(<section class="hero"[\s\S]*?<h1>[\s\S]*?</h1>\s*<p>)[\s\S]*?(</p>)',
        lambda m: m.group(1) + d["hero_p"] + m.group(2),
        text, count=1)
    if n != 1:
        ERRORS.append(f"{fname}: hero paragraph matched {n}")
    text = new

    new, n = re.subn(r'onclick="openSlideshow\(0\)"', 'onclick="openSlideshow(14)"', text)
    if n != 1:
        ERRORS.append(f"{fname}: hero onclick matched {n}")
    text = new

    new, n = re.subn(
        r'(id="experiences">[\s\S]*?<p class="section-subtitle">)[\s\S]*?(</p>)',
        lambda m: m.group(1) + d["exp_sub"] + m.group(2), text, count=1)
    if n != 1:
        ERRORS.append(f"{fname}: experiences subtitle matched {n}")
    text = new

    new, n = re.subn(
        r'(<h3>Pite Havsbad</h3>\s*<p>)[\s\S]*?(</p>)',
        lambda m: m.group(1) + d["havsbad_p"] + m.group(2), text, count=1)
    if n != 1:
        ERRORS.append(f"{fname}: Pite Havsbad card matched {n}")
    text = new

    new, n = re.subn(
        r'(<div class="gallery-item" onclick="openSlideshow\(13\)"[\s\S]*?</picture>\s*</div>)',
        lambda m: m.group(1) + gallery_item(d), text, count=1)
    if n != 1:
        ERRORS.append(f"{fname}: gallery insert matched {n}")
    text = new

    slide_add = (
        ",\n        { full: '/images/full/exterior-aurora.jpg', caption: '"
        + js_escape(d["slide_aurora"]) + "' },\n"
        + "        { full: '/images/full/entrance-veranda.jpg', caption: '"
        + js_escape(d["slide_entrance"]) + "' }"
    )
    new, n = re.subn(
        r"(\{ full: '/images/full/living-room-3\.jpg'[^}]*\})",
        lambda m: m.group(1) + slide_add, text, count=1)
    if n != 1:
        ERRORS.append(f"{fname}: slides append matched {n}")
    text = new

    new, n = re.subn(
        r'(<section class="contact-section" id="contact">)',
        lambda m: build_faq_section(d) + m.group(1), text, count=1)
    if n != 1:
        ERRORS.append(f"{fname}: FAQ section insert matched {n}")
    text = new

    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"  OK {fname}")


def bump_sitemap():
    p = REPO / "sitemap.xml"
    t = p.read_text(encoding="utf-8")
    t, n = re.subn(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{LASTMOD}</lastmod>", t)
    p.write_text(t, encoding="utf-8", newline="\n")
    print(f"  OK sitemap.xml ({n} lastmod entries -> {LASTMOD})")


def validate():
    print("--- validation ---")
    for lang, d in L.items():
        path = REPO / d["file"]
        text = path.read_text(encoding="utf-8")
        for i, (_, _, inner) in enumerate(ld_blocks(text)):
            try:
                json.loads(inner)
            except json.JSONDecodeError as e:
                ERRORS.append(f"{d['file']}: ld+json block {i} invalid: {e}")
        for needle, want in [
            ('id="faq"', 1), ("exterior-aurora.webp", 1), ("entrance-veranda", 3),
            ("og-image-aurora.jpg", 2), ('openSlideshow(14)', 1), ('openSlideshow(15)', 1),
            ("favicon.ico", 1), ("apple-touch-icon", 2),  # rel= + href= in one tag
        ]:
            got = text.count(needle)
            if got != want:
                ERRORS.append(f"{d['file']}: '{needle}' count {got}, expected {want}")
        print(f"  checked {d['file']}")


def main():
    for lang, d in L.items():
        process(lang, d)
    bump_sitemap()
    validate()
    if ERRORS:
        print("\n!!! ERRORS:")
        for e in ERRORS:
            print("  -", e)
        sys.exit(1)
    print("\nALL GOOD")


if __name__ == "__main__":
    main()
