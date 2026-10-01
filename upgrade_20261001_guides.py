"""SEO round 2026-10-01 (Edwin, Tony's "ta gärna en djup extra runda"). ONE-SHOT, not idempotent.

Research (Serper, gl=se, 2026-10-01): head terms like "boende Piteå" are held by OTAs, but intent pages
with weak SERPs exist — long stays for work (långtidsboende/personalboende/Markbygden), northern
lights (informational, builds on our #1 for "northern lights apartment Piteå"), and the big summer
events (Piteå Summer Games, PDOL) where no accommodation page competes.

Does:
 1. Six guide pages (SV + EN x 3), each a real guide with only facts already on the site or verified today.
 2. Internal links to them from all six home pages (footer) + a guide block in SV/EN "things to do".
 3. Fact fix on all six languages: Markbygden is WEST of Piteå, not north (Wikipedia + coordinates:
    ~34 km crow-fly from our geo to the wind farm's centroid, mostly west).
 4. Optimised summer exterior photo (images/full/exterior-summer.{jpg,webp}) for the events page.
 5. sitemap.xml + llms.txt entries.
"""
import json
import re
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).parent
TODAY = "2026-10-01"
BASE = "https://stationshotellet.com"
BEACON = """<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "56268582f31646be956658d1aaefaab9"}'></script><!-- End Cloudflare Web Analytics -->"""

CSS = """
:root{--bg:#faf7f2;--text:#2c2416;--heading:#1a150d;--accent:#7d5e08;--accent-hover:#5e4806;--dark:#2c2416;--warm:#f5ede0;--card:#fff;--border:#e0d5c4;--muted:#7a6e5d;
--font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;--serif:Charter,'Bitstream Charter','Sitka Text',Cambria,Georgia,'Times New Roman',serif}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:var(--font);color:var(--text);background:var(--bg);line-height:1.65;font-size:1.05rem}
nav{background:var(--dark);position:sticky;top:0;z-index:10}
.nav-inner{max-width:1100px;margin:0 auto;padding:.8rem 1.25rem;display:flex;gap:1rem;align-items:center;justify-content:space-between;flex-wrap:wrap}
nav a{color:#f5ede0;text-decoration:none}nav a:hover{color:#fff;text-decoration:underline}
.nav-logo{font-family:var(--serif);font-size:1.2rem;font-weight:700}
.nav-links{display:flex;gap:1rem;flex-wrap:wrap;font-size:.95rem}
.hero{position:relative;color:#fff;background:#2c2416}
.hero img{width:100%;height:clamp(220px,42vw,420px);object-fit:cover;display:block;opacity:.72}
.hero-text{position:absolute;inset:auto 0 0 0;padding:1.5rem 1.25rem;background:linear-gradient(transparent,rgba(20,15,8,.85))}
.hero-text>div{max-width:820px;margin:0 auto}
h1{font-family:var(--serif);font-size:clamp(1.7rem,4vw,2.5rem);line-height:1.2;margin:0 0 .4rem}
.hero p{margin:0;font-size:1.1rem}
main{max-width:820px;margin:0 auto;padding:1.5rem 1.25rem 3rem}
h2{font-family:var(--serif);color:var(--heading);font-size:1.55rem;margin:2.2rem 0 .6rem;line-height:1.25}
h3{color:var(--heading);font-size:1.15rem;margin:1.4rem 0 .3rem}
a{color:var(--accent)}a:hover{color:var(--accent-hover)}
a:focus-visible,button:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.crumbs{font-size:.9rem;color:var(--muted);margin-bottom:1rem}.crumbs a{color:var(--muted)}
table{width:100%;border-collapse:collapse;margin:1rem 0;background:var(--card)}
th,td{text-align:left;padding:.6rem .75rem;border-bottom:1px solid var(--border)}th{background:var(--warm)}
ul{padding-left:1.2rem}li{margin:.3rem 0}
.box{background:var(--warm);border:1px solid var(--border);border-radius:8px;padding:1rem 1.25rem;margin:1.5rem 0}
.cta{display:inline-block;background:var(--accent);color:#fff;padding:.8rem 1.4rem;border-radius:8px;text-decoration:none;font-weight:700;margin:.5rem .5rem 0 0}
.cta:hover{background:var(--accent-hover);color:#fff}
.cta.alt{background:transparent;color:var(--accent);border:2px solid var(--accent)}
.muted{color:var(--muted);font-size:.92rem}
footer{background:var(--dark);color:#e0d5c4;text-align:center;padding:2rem 1.25rem;font-size:.92rem}
footer a{color:#f5ede0}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

# ---------------------------------------------------------------- the pages
# key: (lang, slug-path) ; pair = the other-language twin (hreflang)
PAGES = [
    {
        "lang": "sv", "path": "/sv/langtidsboende-pitea/", "pair": "/long-stay-pitea/",
        "title": "Långtidsboende i Piteå — möblerad lägenhet per vecka/månad",
        "desc": "Hel möblerad lägenhet i Öjebyn, Piteå för jobb och projekt: 6 200 kr/vecka, 23 800 kr/månad, upp till 5 personer. Kök, tvättmaskin, parkering, städning ingår.",
        "img": ("kitchen-dining-wide", "Kök och matplats i lägenheten på Stations Hotellet i Öjebyn"),
        "h1": "Långtidsboende i Piteå — en hel möblerad lägenhet för jobbet",
        "lead": "Vecka eller månad i gamla järnvägsstationen i Öjebyn, fem minuter från centrala Piteå.",
        "crumb": "Långtidsboende",
        "body": """
<p>Jobbar du i Piteå en period — som montör, vårdpersonal, konsult eller i ett bygg- eller vindkraftsprojekt? Då kan du bo i en <strong>hel lägenhet</strong> i stället för ett hotellrum: två sovrum, eget kök och tvättmaskin, och ett pris för hela lägenheten oavsett om ni är en eller fem.</p>

<h2>Pris för vecka och månad</h2>
<table>
<tr><th>Vistelse</th><th>Pris för hela lägenheten</th><th>Per natt</th></tr>
<tr><td>Månad (30 nätter)</td><td><strong>23 800 kr</strong> — städning varje vecka ingår</td><td>ca 793 kr</td></tr>
<tr><td>Vecka (7 nätter)</td><td><strong>6 200 kr</strong></td><td>ca 886 kr</td></tr>
<tr><td>Enstaka natt</td><td>990 kr</td><td>990 kr</td></tr>
</table>
<p>Priset gäller hela lägenheten, upp till 5 personer — inte per person. Delar ett arbetslag på fem på en månad blir det <strong>4 760 kr per person och månad</strong>. Lakan, handdukar, Wi-Fi och parkering ingår. Priset du ser är priset du betalar.</p>

<h2>Det här gör lägenheten bra för en arbetsperiod</h2>
<ul>
<li><strong>Två sovrum, plats för 5</strong> — kollegor kan dela utan att dela rum med främlingar.</li>
<li><strong>Fullt utrustat kök</strong> — laga egen mat i stället för att äta ute varje kväll. ICA och Coop i Öjebyn ligger på gångavstånd.</li>
<li><strong>Tvättmaskin</strong> — arbetskläderna rena utan tvättstuga.</li>
<li><strong>Egen gratis parkering</strong> och nära E4.</li>
<li><strong>Självincheckning med nyckelbox</strong> — kom när skiftet är slut, koden mejlas före ankomst.</li>
<li><strong>Kassaskåp</strong> och separat dusch.</li>
</ul>

<h2>Läget — nära jobben i Piteå</h2>
<ul>
<li>Centrala Piteå: ca 5 minuter med bil.</li>
<li>Piteå sjukhus: ca 5 km.</li>
<li>Markbygdens vindkraftsområde: väster om Piteå, drygt 30 km fågelvägen till områdets mitt.</li>
<li>Luleå Airport: ca 50 km, 40–45 minuter via E4.</li>
</ul>

<h2>Avbokning</h2>
<p>Veckovistelser: gratis avbokning upp till 7 dagar före ankomst. Månadsvistelser: en månads deposition, som återbetalas helt vid avbokning 30 dagar eller mer före ankomst. Hela villkoren står i <a href="/terms.html">bokningsvillkoren</a>.</p>

<h2>Vanliga frågor</h2>
<h3>Hur många kan bo i lägenheten?</h3>
<p>Upp till 5 personer, i två sovrum.</p>
<h3>Ingår städning när man bor en månad?</h3>
<p>Ja, städning varje vecka ingår i månadspriset.</p>
<h3>Kan jag checka in sent på kvällen?</h3>
<p>Ja. Incheckningen sker med nyckelbox från 15:00, så du kan komma när det passar. Utcheckning senast 11:00.</p>
<h3>Finns det parkering?</h3>
<p>Ja, egen parkering ingår utan extra kostnad.</p>
""",
        "faq": [
            ("Hur många kan bo i lägenheten?", "Upp till 5 personer, i två sovrum."),
            ("Ingår städning när man bor en månad?", "Ja, städning varje vecka ingår i månadspriset 23 800 kr."),
            ("Kan jag checka in sent på kvällen?", "Ja. Incheckningen sker med nyckelbox från 15:00, så du kan komma när det passar. Utcheckning senast 11:00."),
            ("Finns det parkering?", "Ja, egen parkering ingår utan extra kostnad."),
        ],
    },
    {
        "lang": "en", "path": "/long-stay-pitea/", "pair": "/sv/langtidsboende-pitea/",
        "title": "Long-Stay Accommodation in Piteå — Weekly & Monthly Rates",
        "desc": "Whole furnished 2-bedroom apartment in Öjebyn, Piteå for work stays: 6,200 kr/week, 23,800 kr/month, up to 5 people. Kitchen, washer, parking, cleaning included.",
        "img": ("kitchen-dining-wide", "Kitchen and dining area in the apartment at Stations Hotellet, Öjebyn"),
        "h1": "Long-Stay Accommodation in Piteå — a Whole Furnished Apartment for Work",
        "lead": "Weekly or monthly in the old railway station in Öjebyn, five minutes from central Piteå.",
        "crumb": "Long stays",
        "body": """
<p>Working in Piteå for a while — as a technician, healthcare professional, consultant, or on a construction or wind-farm project? Stay in a <strong>whole apartment</strong> instead of a hotel room: two bedrooms, your own kitchen and washing machine, and one price for the whole place whether you are one person or five.</p>

<h2>Weekly and monthly rates</h2>
<table>
<tr><th>Stay</th><th>Price for the whole apartment</th><th>Per night</th></tr>
<tr><td>Month (30 nights)</td><td><strong>23,800 kr</strong> — weekly cleaning included</td><td>approx. 793 kr</td></tr>
<tr><td>Week (7 nights)</td><td><strong>6,200 kr</strong></td><td>approx. 886 kr</td></tr>
<tr><td>Single night</td><td>990 kr</td><td>990 kr</td></tr>
</table>
<p>Prices are for the whole apartment, up to 5 people — not per person. A crew of five sharing for a month pays <strong>4,760 kr per person per month</strong>. Linens, towels, Wi-Fi and parking are included. The price you see is the price you pay.</p>

<h2>Why it works for a work assignment</h2>
<ul>
<li><strong>Two bedrooms, sleeps 5</strong> — colleagues can share without sharing a room with strangers.</li>
<li><strong>Fully equipped kitchen</strong> — cook your own meals instead of eating out every night. ICA and Coop in Öjebyn are within walking distance.</li>
<li><strong>Washing machine</strong> — clean work clothes without a laundromat.</li>
<li><strong>Free private parking</strong>, close to the E4.</li>
<li><strong>Self check-in with a key box</strong> — arrive when your shift ends; the code is emailed before arrival.</li>
<li><strong>In-room safe</strong> and a separate shower room.</li>
</ul>

<h2>Location — close to work in Piteå</h2>
<ul>
<li>Central Piteå: about 5 minutes by car.</li>
<li>Piteå hospital: about 5 km.</li>
<li>Markbygden wind farm area: west of Piteå, a little over 30 km as the crow flies to the centre of the area.</li>
<li>Luleå Airport: about 50 km, 40–45 minutes via the E4.</li>
</ul>

<h2>Cancellation</h2>
<p>Weekly stays: free cancellation up to 7 days before arrival. Monthly stays: one month's deposit, fully refunded if you cancel 30 days or more before arrival. Full details in our <a href="/terms.html">booking terms</a>.</p>

<h2>Frequently asked questions</h2>
<h3>How many people can stay?</h3>
<p>Up to 5 people, in two bedrooms.</p>
<h3>Is cleaning included on a monthly stay?</h3>
<p>Yes, weekly cleaning is included in the monthly rate.</p>
<h3>Can I check in late at night?</h3>
<p>Yes. Self check-in with a key box from 15:00, so you can arrive whenever suits you. Check-out by 11:00.</p>
<h3>Is there parking?</h3>
<p>Yes, private parking is included at no extra cost.</p>
""",
        "faq": [
            ("How many people can stay?", "Up to 5 people, in two bedrooms."),
            ("Is cleaning included on a monthly stay?", "Yes, weekly cleaning is included in the monthly rate of 23,800 kr."),
            ("Can I check in late at night?", "Yes. Self check-in with a key box from 15:00, so you can arrive whenever suits you. Check-out by 11:00."),
            ("Is there parking?", "Yes, private parking is included at no extra cost."),
        ],
    },
    {
        "lang": "sv", "path": "/sv/norrsken-pitea/", "pair": "/northern-lights-pitea/",
        "title": "Norrsken i Piteå — när, var och hur du ser det bäst",
        "desc": "Så ser du norrsken i Piteå: säsong september–mars, bästa tiden på kvällen, var du ska stå, prognoser och fototips. Från en värd som ser det från sin egen gata.",
        "img": ("exterior-aurora", "Norrsken över Stations Hotellet i Öjebyn, Piteå"),
        "h1": "Norrsken i Piteå — när, var och hur du ser det",
        "lead": "Bilden ovan är tagen från vår egen gata i Öjebyn. Så här ökar du chansen att se det själv.",
        "crumb": "Norrsken i Piteå",
        "body": """
<p>Piteå ligger runt 65 grader nord, drygt 13 mil söder om polcirkeln — tillräckligt långt norrut för att norrskenet ofta syns rakt ovanför staden. Du behöver inte åka till fjällen: det som avgör är mörker, klar himmel och lite tålamod.</p>

<h2>När syns norrskenet i Piteå?</h2>
<ul>
<li><strong>Säsong: ungefär september till mars.</strong> Under midnattssolens sommar är det för ljust — norrskenet finns där, men syns inte.</li>
<li><strong>Tid på dygnet:</strong> titta från runt klockan 21 och några timmar framåt. Aktiviteten kommer ofta i vågor — har det varit lugnt en stund kan det plötsligt ta fart.</li>
<li><strong>Vädret avgör mest.</strong> Molnen är den vanligaste orsaken till att man missar ett norrsken. Kolla molnprognosen lika noga som norrskensprognosen.</li>
</ul>

<h2>Var ska man stå?</h2>
<ul>
<li><strong>Bort från gatubelysningen.</strong> Ett par hundra meter från lampor gör stor skillnad — låt ögonen vänja sig vid mörkret i 10–15 minuter.</li>
<li><strong>Titta mot norr</strong> och upp. Ett starkt norrsken kan täcka hela himlen.</li>
<li><strong>Öppna platser</strong> som fält och stränder ger fri sikt mot horisonten. Gå aldrig ut på is du inte vet är säker.</li>
<li>Från Stations Hotellet kan det visa sig direkt från dörrtröskeln — bilden högst upp är tagen här.</li>
</ul>

<h2>Prognoser — så läser du dem</h2>
<p>Norrskensappar och sajter visar ett <strong>Kp-värde</strong> (0–9) som mäter hur stor störningen i jordens magnetfält är. Ju längre norrut man är, desto lägre Kp behövs. På vår breddgrad kan norrsken synas även när Kp-värdet är måttligt — så ge inte upp en klar kväll bara för att siffran är låg. Kombinera med en molnprognos, till exempel från SMHI.</p>

<h2>Fotografera norrskenet</h2>
<ul>
<li><strong>Mobil:</strong> nattläget i moderna telefoner fångar ofta mer färg än ögat ser. Håll telefonen stilla mot något fast.</li>
<li><strong>Kamera:</strong> stativ, manuell fokus på oändligt, öppen bländare, ISO runt 1600–3200 och 5–15 sekunders slutartid. Kortare tid när norrskenet rör sig snabbt.</li>
<li>Kyla tömmer batterier fort — ha ett extra i innerfickan.</li>
</ul>

<h2>Klä dig för väntan</h2>
<p>Mitt i vintern kan det bli 20 minusgrader eller kallare. Lager på lager, varma skor, mössa och vantar — man står stilla längre än man tror. En termos med något varmt gör väntan bättre.</p>

<div class="box"><strong>Bo där norrskenet syns.</strong> Stations Hotellet är en hel lägenhet med två sovrum för upp till 5 gäster i Öjebyn, Piteå — från 990 kr per natt, allt ingår. Gå ut på gatan när himlen tänds, och in i värmen när du frusit klart.</div>
""",
        "faq": None,
    },
    {
        "lang": "en", "path": "/northern-lights-pitea/", "pair": "/sv/norrsken-pitea/",
        "title": "Northern Lights in Piteå — When, Where and How to See Them",
        "desc": "How to see the northern lights in Piteå: the September–March season, best time of night, where to stand, forecasts and photo tips — from hosts who see them at home.",
        "img": ("exterior-aurora", "Northern lights over Stations Hotellet in Öjebyn, Piteå"),
        "h1": "Northern Lights in Piteå — When, Where and How to See Them",
        "lead": "The photo above was taken from our own street in Öjebyn. Here is how to improve your chances.",
        "crumb": "Northern lights in Piteå",
        "body": """
<p>Piteå lies at about 65° north, a little over 130 km south of the Arctic Circle — far enough north that the aurora often appears right above town. You do not need to travel to the mountains: what matters is darkness, a clear sky and a little patience.</p>

<h2>When can you see the northern lights in Piteå?</h2>
<ul>
<li><strong>Season: roughly September to March.</strong> In the midnight-sun summer it is too light — the aurora is there, you just cannot see it.</li>
<li><strong>Time of night:</strong> start looking from around 9 pm and for a few hours after. Activity often comes in waves — a quiet sky can suddenly come alive.</li>
<li><strong>Weather matters most.</strong> Cloud is the most common reason people miss the aurora. Check the cloud forecast as carefully as the aurora forecast.</li>
</ul>

<h2>Where should you stand?</h2>
<ul>
<li><strong>Away from street lights.</strong> A couple of hundred metres from lamps makes a big difference — give your eyes 10–15 minutes to adjust to the dark.</li>
<li><strong>Look north</strong> and up. A strong display can fill the whole sky.</li>
<li><strong>Open spaces</strong> such as fields and shorelines give a clear view of the horizon. Never walk onto ice you do not know is safe.</li>
<li>At Stations Hotellet it can appear right outside the door — the photo at the top was taken here.</li>
</ul>

<h2>Reading the forecasts</h2>
<p>Aurora apps and websites show a <strong>Kp index</strong> (0–9) for how disturbed Earth's magnetic field is. The further north you are, the lower the Kp you need. At our latitude the aurora can show even when the Kp value is moderate — so do not give up on a clear evening just because the number is low. Combine it with a cloud forecast.</p>

<h2>Photographing the aurora</h2>
<ul>
<li><strong>Phone:</strong> the night mode on modern phones often captures more colour than the eye sees. Rest the phone on something steady.</li>
<li><strong>Camera:</strong> tripod, manual focus at infinity, wide aperture, ISO around 1600–3200 and 5–15 second exposures. Shorter when the aurora moves fast.</li>
<li>Cold drains batteries fast — keep a spare in an inside pocket.</li>
</ul>

<h2>Dress for the wait</h2>
<p>In midwinter it can drop to −20 °C or colder. Layers, warm boots, hat and mittens — you stand still longer than you think. A thermos of something hot makes the wait better.</p>

<div class="box"><strong>Stay where the aurora shows up.</strong> Stations Hotellet is a whole two-bedroom apartment for up to 5 guests in Öjebyn, Piteå — from 990 kr per night, all-inclusive. Step out onto the street when the sky lights up, and back into the warmth when you have had enough of the cold.</div>
""",
        "faq": None,
    },
    {
        "lang": "sv", "path": "/sv/boende-pitea-summer-games/", "pair": "/pitea-summer-games-accommodation/",
        "title": "Boende Piteå Summer Games & PDOL — hel lägenhet för 5",
        "desc": "Boende under Piteå Summer Games och Piteå Dansar och Ler: hel lägenhet med 2 sovrum för upp till 5 i Öjebyn, Piteå. Kök, tvättmaskin, parkering. Från 990 kr/natt.",
        "img": ("exterior-summer", "Stations Hotellet i Öjebyn en sommardag"),
        "h1": "Boende under Piteå Summer Games och Piteå Dansar och Ler",
        "lead": "En hel lägenhet för laget, familjen eller kompisgänget — fem minuter från centrala Piteå.",
        "crumb": "Boende Summer Games & PDOL",
        "body": """
<p>Två gånger varje sommar fylls Piteå av besökare. Då är en hel lägenhet med eget kök ofta både billigare och bekvämare än flera hotellrum — särskilt om ni är flera.</p>

<h2>Piteå Summer Games</h2>
<p>Piteå Summer Games är en av Sveriges största fotbollsturneringar för ungdomar, med hundratals lag från hela världen. Turneringen spelas helgen efter midsommar på planer i och runt Piteå — och tack vare midnattssolen spelas matcher även sent på kvällen. Exakta datum och spelschema finns på <a href="https://piteasummergames.se/" rel="noopener">piteasummergames.se</a>.</p>

<h2>Piteå Dansar och Ler (PDOL)</h2>
<p>PDOL är Piteås stora stadsfestival i slutet av juli, med konserter och tivoli i centrum — och gratis inträde. Program och datum finns på <a href="https://pdol.se/" rel="noopener">pdol.se</a>.</p>

<h2>Varför en hel lägenhet under evenemangen?</h2>
<ul>
<li><strong>Plats för 5 i två sovrum</strong> — ett pris för hela lägenheten, inte per person.</li>
<li><strong>Eget kök</strong> — frukost och middag hemma i stället för restaurang varje måltid.</li>
<li><strong>Tvättmaskin</strong> — matchställen rena till nästa dag.</li>
<li><strong>Egen gratis parkering</strong> — inget letande efter parkering i stan under festivalveckan.</li>
<li><strong>Självincheckning</strong> med nyckelbox — kom när ni kommer.</li>
</ul>

<h2>Vad kostar det?</h2>
<table>
<tr><th>Exempel</th><th>Hela lägenheten</th><th>Per person om ni är 5</th></tr>
<tr><td>3 nätter</td><td>2 970 kr</td><td>594 kr</td></tr>
<tr><td>7 nätter (veckopris)</td><td>6 200 kr</td><td>1 240 kr</td></tr>
</table>
<p>Städning, lakan, handdukar, Wi-Fi och parkering ingår. Enstaka nätter går att avboka gratis upp till 3 dagar före ankomst.</p>

<h2>Läget</h2>
<ul>
<li>Centrala Piteå, där PDOL hålls: ca 5 minuter med bil.</li>
<li>Pite Havsbad: ca 15 km, ungefär 15 minuter med bil.</li>
<li>Mataffärer i Öjebyn på gångavstånd.</li>
</ul>

<div class="box"><strong>Boka tidigt.</strong> Det är många som vill bo i Piteå de veckorna. Skicka en förfrågan med era datum så svarar vi om lägenheten är ledig.</div>
""",
        "faq": None,
    },
    {
        "lang": "en", "path": "/pitea-summer-games-accommodation/", "pair": "/sv/boende-pitea-summer-games/",
        "title": "Piteå Summer Games Accommodation — Whole Apartment for 5",
        "desc": "Accommodation for Piteå Summer Games and the PDOL festival: whole 2-bedroom apartment for up to 5 in Öjebyn, Piteå. Kitchen, washing machine, parking. From 990 kr/night.",
        "img": ("exterior-summer", "Stations Hotellet in Öjebyn on a summer day"),
        "h1": "Accommodation for Piteå Summer Games and Piteå Dansar och Ler",
        "lead": "A whole apartment for the team, the family or a group of friends — five minutes from central Piteå.",
        "crumb": "Summer Games & PDOL",
        "body": """
<p>Twice every summer Piteå fills up with visitors. A whole apartment with its own kitchen is then often both cheaper and more comfortable than several hotel rooms — especially for a group.</p>

<h2>Piteå Summer Games</h2>
<p>Piteå Summer Games is one of Sweden's largest youth football tournaments, with hundreds of teams from around the world. It is played the weekend after Midsummer on pitches in and around Piteå — and thanks to the midnight sun, matches run late into the evening. Exact dates and schedules are at <a href="https://piteasummergames.se/" rel="noopener">piteasummergames.se</a>.</p>

<h2>Piteå Dansar och Ler (PDOL)</h2>
<p>PDOL is Piteå's big town festival at the end of July, with concerts and a funfair in the centre — and free entry. Programme and dates are at <a href="https://pdol.se/" rel="noopener">pdol.se</a>.</p>

<h2>Why a whole apartment for the events?</h2>
<ul>
<li><strong>Sleeps 5 in two bedrooms</strong> — one price for the whole apartment, not per person.</li>
<li><strong>Your own kitchen</strong> — breakfast and dinner at home instead of eating out every meal.</li>
<li><strong>Washing machine</strong> — kits clean for the next match.</li>
<li><strong>Free private parking</strong> — no hunting for a space in town during festival week.</li>
<li><strong>Self check-in</strong> with a key box — arrive when you arrive.</li>
</ul>

<h2>What does it cost?</h2>
<table>
<tr><th>Example</th><th>Whole apartment</th><th>Per person for 5</th></tr>
<tr><td>3 nights</td><td>2,970 kr</td><td>594 kr</td></tr>
<tr><td>7 nights (weekly rate)</td><td>6,200 kr</td><td>1,240 kr</td></tr>
</table>
<p>Cleaning, linens, towels, Wi-Fi and parking are included. Single nights can be cancelled free of charge up to 3 days before arrival.</p>

<h2>Location</h2>
<ul>
<li>Central Piteå, where PDOL takes place: about 5 minutes by car.</li>
<li>Pite Havsbad beach resort: about 15 km, roughly 15 minutes by car.</li>
<li>Supermarkets in Öjebyn within walking distance.</li>
</ul>

<div class="box"><strong>Book early.</strong> Many people want to stay in Piteå during those weeks. Send a request with your dates and we will tell you whether the apartment is free.</div>
""",
        "faq": None,
    },
]

UI = {
    "sv": {"home": "/sv/", "prices": "Priser", "book": "Boka", "contact": "Kontakt", "start": "Startsida",
           "cta": "Skicka bokningsförfrågan", "cta2": "Se priser och bilder", "updated": "Uppdaterad",
           "hosts": "Värdade av Doushka &amp; Sören Stenvall", "terms": "Bokningsvillkor",
           "addr": "Västra Järnvägsgatan 5, Öjebyn, 943 31, Sverige", "guides": "Guider",
           "langname": "English", "langcode": "EN", "locale": "sv_SE"},
    "en": {"home": "/", "prices": "Prices", "book": "Book", "contact": "Contact", "start": "Home",
           "cta": "Send a booking request", "cta2": "See prices and photos", "updated": "Updated",
           "hosts": "Hosted by Doushka &amp; Sören Stenvall", "terms": "Booking terms",
           "addr": "Västra Järnvägsgatan 5, Öjebyn, 943 31, Sweden", "guides": "Guides",
           "langname": "Svenska", "langcode": "SV", "locale": "en_US"},
}


def guide_links(lang):
    return [(p["path"], p["crumb"]) for p in PAGES if p["lang"] == lang]


def render(p):
    u = UI[p["lang"]]
    url = BASE + p["path"]
    en_url = BASE + (p["path"] if p["lang"] == "en" else p["pair"])
    sv_url = BASE + (p["path"] if p["lang"] == "sv" else p["pair"])
    img, alt = p["img"]
    ld = [
        {"@context": "https://schema.org", "@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["title"],
         "description": p["desc"], "inLanguage": p["lang"], "dateModified": TODAY,
         "primaryImageOfPage": f"{BASE}/images/full/{img}.jpg",
         "about": {"@id": f"{BASE}/#lodging"},
         "isPartOf": {"@type": "WebSite", "name": "Stations Hotellet", "url": BASE + "/"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Stations Hotellet", "item": BASE + u["home"]},
            {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url}]},
    ]
    if p["faq"]:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]})
    ld_html = "\n".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=1)}\n</script>' for x in ld)
    others = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in guide_links(p["lang"]) if h != p["path"])
    other_lang = p["pair"]
    return f"""<!DOCTYPE html>
<html lang="{p['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{p['title']}</title>
<meta name="description" content="{p['desc']}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="sv" href="{sv_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Stations Hotellet">
<meta property="og:locale" content="{u['locale']}">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/images/full/{img}.jpg">
<meta property="og:image:alt" content="{alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2c2416">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" as="image" href="/images/full/{img}.webp" type="image/webp" fetchpriority="high">
{ld_html}
<style>{CSS}</style>
</head>
<body>
<nav>
<div class="nav-inner">
<a href="{u['home']}" class="nav-logo">Stations Hotellet</a>
<div class="nav-links">
<a href="{u['home']}#prices">{u['prices']}</a>
<a href="{u['home']}#booking">{u['book']}</a>
<a href="{u['home']}#contact">{u['contact']}</a>
<a href="{other_lang}" hreflang="{'en' if p['lang'] == 'sv' else 'sv'}" lang="{'en' if p['lang'] == 'sv' else 'sv'}">{u['langcode']}</a>
</div>
</div>
</nav>
<header class="hero">
<picture><source srcset="/images/full/{img}.webp" type="image/webp"><img src="/images/full/{img}.jpg" alt="{alt}" width="1600" height="900" fetchpriority="high"></picture>
<div class="hero-text"><div>
<h1>{p['h1']}</h1>
<p>{p['lead']}</p>
</div></div>
</header>
<main>
<p class="crumbs"><a href="{u['home']}">{u['start']}</a> › {p['crumb']}</p>
{p['body'].strip()}
<p><a class="cta" href="{u['home']}#booking">{u['cta']}</a><a class="cta alt" href="{u['home']}#prices">{u['cta2']}</a></p>
<h2>{u['guides']}</h2>
<ul>{others}</ul>
<p class="muted">{u['updated']} {TODAY}</p>
</main>
<footer>
<p>&copy; 2026 Stations Hotellet &middot; {u['addr']}</p>
<p style="margin-top:.5rem">{u['hosts']}</p>
<p style="margin-top:.5rem"><a href="/terms.html">{u['terms']}</a> &middot; <a href="{other_lang}" hreflang="{'en' if p['lang'] == 'sv' else 'sv'}">{u['langname']}</a></p>
</footer>
{BEACON}
</body>
</html>
"""


def must_replace(text, old, new, f, count=1):
    n = text.count(old)
    if n != count:
        raise SystemExit(f"STOPP {f}: väntade {count} träff(ar) på {old[:60]!r}, fick {n}")
    return text.replace(old, new)


def main():
    # 4. summer photo, optimised like the rest (images/full, JPEG + WebP, 1280 px)
    src = ROOT / "images/full/exterior_summer.jpg"
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    th = int(w * 9 / 16)
    top = max(0, (h - th) // 2 - h // 10)
    im = im.crop((0, top, w, top + th)).resize((1280, 720), Image.LANCZOS)
    im.save(ROOT / "images/full/exterior-summer.jpg", quality=72, optimize=True, progressive=True)
    im.save(ROOT / "images/full/exterior-summer.webp", quality=68, method=6)

    # 1. pages
    for p in PAGES:
        out = ROOT / p["path"].strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(p), encoding="utf-8")
        print("skrev", out.relative_to(ROOT))

    # 3. Markbygden: west, not north (all six languages)
    fix = {
        "index.html": ("30 km north — one of", "~30 km west — one of"),
        "sv/index.html": ("30 km norrut — en av", "~30 km västerut — en av"),
        "de/index.html": ("30 km nördlich — einer", "~30 km westlich — einer"),
        "fr/index.html": ("30 km au nord — un des", "~30 km à l'ouest — un des"),
        "pl/index.html": ("30 km na północ — jeden", "~30 km na zachód — jeden"),
        "ro/index.html": ("30 km nord — unul", "~30 km vest — unul"),
    }
    # 2. footer links to the guides on every home page (SV home -> SV guides, others -> EN guides)
    for f, (old, new) in fix.items():
        path = ROOT / f
        s = path.read_text(encoding="utf-8")
        s = must_replace(s, old, new, f)
        lang = "sv" if f.startswith("sv/") else "en"
        label = UI[lang]["guides"]
        links = " &middot; ".join(f'<a href="{h}">{t}</a>' for h, t in guide_links(lang))
        s = must_replace(s, "\n</footer>", f'\n    <p style="margin-top: 0.5rem;">{label}: {links}</p>\n</footer>', f)
        path.write_text(s, encoding="utf-8")
        print("ändrade", f)

    # 5. sitemap + llms.txt
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    entries = ""
    for p in PAGES:
        en = BASE + (p["path"] if p["lang"] == "en" else p["pair"])
        sv = BASE + (p["path"] if p["lang"] == "sv" else p["pair"])
        entries += f"""  <url>
    <loc>{BASE}{p['path']}</loc>
    <xhtml:link rel="alternate" hreflang="sv" href="{sv}" />
    <xhtml:link rel="alternate" hreflang="en" href="{en}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{en}" />
    <lastmod>{TODAY}T09:00:00Z</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.7</priority>
  </url>
"""
    sm = must_replace(sm, "</urlset>", entries + "</urlset>", "sitemap.xml")
    (ROOT / "sitemap.xml").write_text(sm, encoding="utf-8")

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8").rstrip("\n")
    llms += "\n\n## Guides\n" + "".join(f"- [{p['title']}]({BASE}{p['path']}): {p['desc']}\n" for p in PAGES)
    (ROOT / "llms.txt").write_text(llms, encoding="utf-8")
    print("sitemap.xml + llms.txt uppdaterade")


if __name__ == "__main__":
    main()
