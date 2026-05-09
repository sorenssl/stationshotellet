"""Add Business name field + receipt overlay to all 6 booking forms.

Security:
- All user input rendered via textContent, never innerHTML
- No eval/Function calls
- Date parsing strictly via Date constructor (returns NaN on invalid)
- Form falls back to native HTML submit if JS disabled — Formspree
  still receives the booking, just no receipt overlay
- No new external resource loads (no CDN scripts, no fonts)
- Honeypot field added to filter bot submissions

Run: python add_booking_receipt.py
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent

# Per-language translated strings.
# Keep keys identical across files so the script logic stays uniform.
STRINGS = {
    "index.html": {
        "lang": "en",
        "business_label": "Business name (optional)",
        "business_placeholder": "Company name (if applicable)",
        "receipt_title": "Booking Request Received",
        "receipt_subtitle": "Thank you. Here's a copy of what you submitted.",
        "receipt_property": "Stations Hotellet",
        "receipt_address": "Västra Järnvägsgatan 5, 943 31 Öjebyn, Sweden",
        "receipt_nights_label": "Nights",
        "receipt_status_pending": "Sending…",
        "receipt_status_sent": "✓ Booking request sent — we'll confirm by email within 24 hours",
        "receipt_status_failed": "⚠️ Send failed — please email posetivemind67@gmail.com or call Sören 070-671 81 85",
        "receipt_note": "This is a booking <strong>request</strong>, not a confirmed booking. We'll reply within 24 hours to confirm availability and arrange payment. Save this page or print it for your records.",
        "receipt_print": "Print / Save as PDF",
        "receipt_close": "Close",
        "anchor_form_action": 'action="https://formspree.io/f/xkoyoery"',
    },
    "sv/index.html": {
        "lang": "sv",
        "business_label": "Företagsnamn (valfritt)",
        "business_placeholder": "Företagsnamn (om tillämpligt)",
        "receipt_title": "Bokningsförfrågan mottagen",
        "receipt_subtitle": "Tack. Här är en kopia av det du skickade.",
        "receipt_property": "Stations Hotellet",
        "receipt_address": "Västra Järnvägsgatan 5, 943 31 Öjebyn, Sverige",
        "receipt_nights_label": "Nätter",
        "receipt_status_pending": "Skickar…",
        "receipt_status_sent": "✓ Bokningsförfrågan skickad — vi bekräftar via e-post inom 24 timmar",
        "receipt_status_failed": "⚠️ Sändning misslyckades — kontakta posetivemind67@gmail.com eller ring Sören 070-671 81 85",
        "receipt_note": "Detta är en bokningsför<strong>frågan</strong>, inte en bekräftad bokning. Vi svarar inom 24 timmar för att bekräfta tillgänglighet och ordna betalning. Spara denna sida eller skriv ut den för din dokumentation.",
        "receipt_print": "Skriv ut / Spara som PDF",
        "receipt_close": "Stäng",
        "anchor_form_action": 'action="https://formspree.io/f/xkoyoery"',
    },
    "fr/index.html": {
        "lang": "fr",
        "business_label": "Nom d'entreprise (facultatif)",
        "business_placeholder": "Nom de la société (le cas échéant)",
        "receipt_title": "Demande de réservation reçue",
        "receipt_subtitle": "Merci. Voici une copie de ce que vous avez soumis.",
        "receipt_property": "Stations Hotellet",
        "receipt_address": "Västra Järnvägsgatan 5, 943 31 Öjebyn, Suède",
        "receipt_nights_label": "Nuits",
        "receipt_status_pending": "Envoi…",
        "receipt_status_sent": "✓ Demande envoyée — nous confirmerons par e-mail sous 24 heures",
        "receipt_status_failed": "⚠️ Échec de l'envoi — contactez posetivemind67@gmail.com ou appelez Sören 070-671 81 85",
        "receipt_note": "Ceci est une <strong>demande</strong> de réservation, pas une réservation confirmée. Nous répondrons sous 24 heures pour confirmer la disponibilité et organiser le paiement. Sauvegardez cette page ou imprimez-la pour vos archives.",
        "receipt_print": "Imprimer / Enregistrer en PDF",
        "receipt_close": "Fermer",
        "anchor_form_action": 'action="https://formspree.io/f/xkoyoery"',
    },
    "de/index.html": {
        "lang": "de",
        "business_label": "Firmenname (optional)",
        "business_placeholder": "Firmenname (falls zutreffend)",
        "receipt_title": "Buchungsanfrage erhalten",
        "receipt_subtitle": "Vielen Dank. Hier ist eine Kopie Ihrer Eingabe.",
        "receipt_property": "Stations Hotellet",
        "receipt_address": "Västra Järnvägsgatan 5, 943 31 Öjebyn, Schweden",
        "receipt_nights_label": "Nächte",
        "receipt_status_pending": "Wird gesendet…",
        "receipt_status_sent": "✓ Anfrage gesendet — wir bestätigen per E-Mail innerhalb von 24 Stunden",
        "receipt_status_failed": "⚠️ Senden fehlgeschlagen — bitte E-Mail an posetivemind67@gmail.com oder Sören 070-671 81 85",
        "receipt_note": "Dies ist eine Buchungs<strong>anfrage</strong>, keine bestätigte Buchung. Wir antworten innerhalb von 24 Stunden, um Verfügbarkeit zu bestätigen und Zahlung zu vereinbaren. Speichern oder drucken Sie diese Seite für Ihre Unterlagen.",
        "receipt_print": "Drucken / Als PDF speichern",
        "receipt_close": "Schließen",
        "anchor_form_action": 'action="https://formspree.io/f/xkoyoery"',
    },
    "pl/index.html": {
        "lang": "pl",
        "business_label": "Nazwa firmy (opcjonalnie)",
        "business_placeholder": "Nazwa firmy (jeśli dotyczy)",
        "receipt_title": "Zapytanie o rezerwację otrzymane",
        "receipt_subtitle": "Dziękujemy. Oto kopia Twojego zapytania.",
        "receipt_property": "Stations Hotellet",
        "receipt_address": "Västra Järnvägsgatan 5, 943 31 Öjebyn, Szwecja",
        "receipt_nights_label": "Noce",
        "receipt_status_pending": "Wysyłanie…",
        "receipt_status_sent": "✓ Zapytanie wysłane — potwierdzimy e-mailem w ciągu 24 godzin",
        "receipt_status_failed": "⚠️ Wysłanie nie powiodło się — napisz na posetivemind67@gmail.com lub zadzwoń do Sörena 070-671 81 85",
        "receipt_note": "To jest <strong>zapytanie</strong> o rezerwację, a nie potwierdzona rezerwacja. Odpowiemy w ciągu 24 godzin, aby potwierdzić dostępność i ustalić płatność. Zapisz tę stronę lub wydrukuj ją dla swojej dokumentacji.",
        "receipt_print": "Drukuj / Zapisz jako PDF",
        "receipt_close": "Zamknij",
        "anchor_form_action": 'action="https://formspree.io/f/xkoyoery"',
    },
    "ro/index.html": {
        "lang": "ro",
        "business_label": "Nume firmă (opțional)",
        "business_placeholder": "Numele companiei (dacă este cazul)",
        "receipt_title": "Cerere de rezervare primită",
        "receipt_subtitle": "Mulțumim. Iată o copie a datelor trimise.",
        "receipt_property": "Stations Hotellet",
        "receipt_address": "Västra Järnvägsgatan 5, 943 31 Öjebyn, Suedia",
        "receipt_nights_label": "Nopți",
        "receipt_status_pending": "Se trimite…",
        "receipt_status_sent": "✓ Cerere trimisă — vom confirma prin e-mail în 24 de ore",
        "receipt_status_failed": "⚠️ Trimitere eșuată — contactați posetivemind67@gmail.com sau sunați-l pe Sören 070-671 81 85",
        "receipt_note": "Aceasta este o <strong>cerere</strong> de rezervare, nu o rezervare confirmată. Vom răspunde în 24 de ore pentru a confirma disponibilitatea și a aranja plata. Salvați această pagină sau imprimați-o pentru documentele dvs.",
        "receipt_print": "Imprimă / Salvează ca PDF",
        "receipt_close": "Închide",
        "anchor_form_action": 'action="https://formspree.io/f/xkoyoery"',
    },
}


# Anchor: name input field (every language has same structure, just translated label)
# We insert the new business field AFTER the name input's closing </div>.
NAME_FIELD_PATTERN = re.compile(
    r'(<div class="form-group">\s*<label for="name">[^<]*</label>\s*'
    r'<input type="text" id="name" name="name" required[^>]*></div>)',
    re.DOTALL,
)

# Honeypot: a hidden field bots fill but humans never see. Form-handler ignores
# submissions where this is non-empty.
HONEYPOT_HTML = (
    '\n                <input type="text" name="_gotcha" tabindex="-1" '
    'autocomplete="off" style="position:absolute;left:-9999px;visibility:hidden" '
    'aria-hidden="true">'
)


def build_business_field(s: dict) -> str:
    return (
        '<div class="form-group">\n'
        f'                    <label for="business">{s["business_label"]}</label>\n'
        f'                    <input type="text" id="business" name="business" '
        f'placeholder="{s["business_placeholder"]}">\n'
        '                </div>'
    )


def build_receipt_overlay(s: dict) -> str:
    # Static parts have language-specific text. User data inserted via textContent
    # at runtime — safe from XSS. The `innerHTML` here only contains TRUSTED static text.
    # The receipt_note contains a <strong> tag (trusted, hard-coded).
    return f'''
<!-- Booking receipt overlay (built by JS on form submit) -->
<div id="booking-receipt" class="booking-receipt" hidden role="dialog" aria-modal="true" aria-labelledby="receipt-title">
    <div class="receipt-card">
        <div class="receipt-header">
            <h2 id="receipt-title">{s["receipt_title"]}</h2>
            <p class="receipt-subtitle">{s["receipt_subtitle"]}</p>
        </div>
        <div class="receipt-property">
            <strong>{s["receipt_property"]}</strong><br>
            {s["receipt_address"]}
        </div>
        <dl id="receipt-fields" class="receipt-fields"></dl>
        <p id="receipt-status" class="receipt-status receipt-status-pending">{s["receipt_status_pending"]}</p>
        <p class="receipt-note">{s["receipt_note"]}</p>
        <div class="receipt-actions">
            <button type="button" class="btn" onclick="window.print()">{s["receipt_print"]}</button>
            <button type="button" class="btn btn-outline receipt-close-btn">{s["receipt_close"]}</button>
        </div>
    </div>
</div>
'''


RECEIPT_CSS = '''
        /* --- Booking receipt overlay --- */
        .booking-receipt {
            position: fixed; inset: 0; z-index: 1000;
            background: rgba(26, 21, 13, 0.7);
            display: flex; align-items: flex-start; justify-content: center;
            padding: 2rem 1rem; overflow-y: auto;
        }
        .booking-receipt[hidden] { display: none; }
        .receipt-card {
            background: var(--color-card);
            border-radius: 8px;
            max-width: 600px; width: 100%;
            padding: 2rem 2rem 1.5rem; margin-top: 2rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        .receipt-header { text-align: center; margin-bottom: 1.2rem; }
        .receipt-header h2 {
            color: var(--color-heading);
            font-size: 1.4rem; margin-bottom: 0.3rem;
        }
        .receipt-subtitle {
            color: var(--color-muted); font-size: 0.95rem;
        }
        .receipt-property {
            background: var(--color-warm);
            border-left: 3px solid var(--color-accent);
            padding: 0.75rem 1rem;
            border-radius: 4px;
            margin-bottom: 1.25rem;
            font-size: 0.95rem;
        }
        .receipt-fields {
            display: grid;
            grid-template-columns: max-content 1fr;
            gap: 0.4rem 1rem;
            margin-bottom: 1.25rem;
            font-size: 0.95rem;
        }
        .receipt-fields dt {
            color: var(--color-muted);
            font-weight: 500;
        }
        .receipt-fields dd {
            color: var(--color-text);
            word-break: break-word;
        }
        .receipt-status {
            text-align: center;
            padding: 0.6rem 1rem;
            border-radius: 4px;
            font-size: 0.92rem;
            margin-bottom: 1.25rem;
        }
        .receipt-status-pending { background: #f5ede0; color: var(--color-muted); }
        .receipt-status-sent    { background: #e6f3e6; color: #2d6e2d; }
        .receipt-status-failed  { background: #fbeaea; color: #a23b3b; }
        .receipt-note {
            font-size: 0.88rem;
            color: var(--color-text);
            line-height: 1.5;
            margin-bottom: 1.5rem;
            padding: 0.75rem 1rem;
            background: var(--color-warm);
            border-radius: 4px;
        }
        .receipt-actions {
            display: flex; gap: 0.75rem;
            flex-wrap: wrap; justify-content: center;
        }
        @media print {
            body > *:not(#booking-receipt) { display: none !important; }
            .booking-receipt {
                position: static; background: white; padding: 0;
            }
            .receipt-card {
                box-shadow: none; max-width: none;
                margin: 0; padding: 1rem;
            }
            .receipt-actions, .receipt-status { display: none; }
        }
'''


# JS — universal across languages. Reads field labels from existing <label>
# elements (already translated). Uses textContent for all user input → XSS-safe.
RECEIPT_JS = '''
<script>
    /* --- Booking-form receipt overlay (XSS-safe via textContent) --- */
    (function() {
        var form = document.querySelector('form.form-grid');
        var overlay = document.getElementById('booking-receipt');
        if (!form || !overlay) return;

        var fieldsDl = overlay.querySelector('#receipt-fields');
        var statusEl = overlay.querySelector('#receipt-status');
        var closeBtn = overlay.querySelector('.receipt-close-btn');
        var statusPendingText = statusEl.textContent;
        var statusSentText = statusEl.getAttribute('data-sent') || '';
        var statusFailText = statusEl.getAttribute('data-failed') || '';

        function getLabel(inputId) {
            var lbl = form.querySelector('label[for="' + inputId + '"]');
            return lbl ? lbl.textContent.trim() : inputId;
        }

        function appendRow(label, value) {
            var dt = document.createElement('dt');
            dt.textContent = label;          // SAFE: textContent
            var dd = document.createElement('dd');
            dd.textContent = value;          // SAFE: textContent — XSS-protected
            fieldsDl.appendChild(dt);
            fieldsDl.appendChild(dd);
        }

        function calcNights(ci, co) {
            if (!ci || !co) return 0;
            var d1 = new Date(ci);
            var d2 = new Date(co);
            if (isNaN(d1) || isNaN(d2)) return 0;
            var n = Math.round((d2 - d1) / 86400000);
            return n > 0 ? n : 0;
        }

        function buildReceipt(fd) {
            // Clear any previous receipt content
            while (fieldsDl.firstChild) fieldsDl.removeChild(fieldsDl.firstChild);
            // Field order matches form, business inserted after name
            var order = [
                ['name', null],
                ['business', null],
                ['email', null],
                ['phone', null],
                ['guests', null],
                ['checkin', null],
                ['checkout', null],
                ['message', null]
            ];
            order.forEach(function(pair) {
                var key = pair[0];
                var val = (fd.get(key) || '').toString().trim();
                if (!val) return;
                appendRow(getLabel(key), val);
            });
            // Computed: # nights
            var n = calcNights(fd.get('checkin'), fd.get('checkout'));
            if (n > 0) {
                var nightsLabel = overlay.getAttribute('data-nights-label') || 'Nights';
                appendRow(nightsLabel, String(n));
            }
        }

        form.addEventListener('submit', function(ev) {
            // Honeypot check — bots fill _gotcha; humans never see it
            var honey = form.querySelector('[name="_gotcha"]');
            if (honey && honey.value) {
                // Silently let the submission go through to Formspree (which
                // also has spam filtering); just don't show our overlay.
                return;
            }
            ev.preventDefault();
            var fd = new FormData(form);
            buildReceipt(fd);
            statusEl.textContent = statusPendingText;
            statusEl.className = 'receipt-status receipt-status-pending';
            overlay.hidden = false;

            // Submit to Formspree via AJAX
            fetch(form.action, {
                method: 'POST',
                body: fd,
                headers: { 'Accept': 'application/json' }
            }).then(function(r) {
                if (r.ok) {
                    statusEl.textContent = statusSentText;
                    statusEl.className = 'receipt-status receipt-status-sent';
                    form.reset();
                } else {
                    statusEl.textContent = statusFailText;
                    statusEl.className = 'receipt-status receipt-status-failed';
                }
            }).catch(function() {
                statusEl.textContent = statusFailText;
                statusEl.className = 'receipt-status receipt-status-failed';
            });
        });

        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                overlay.hidden = true;
            });
        }
    })();
</script>
'''


def process(path: Path, key: str) -> dict:
    text = path.read_text(encoding="utf-8")
    s = STRINGS[key]
    changes = []

    # 1) Add Business name field after the name field (idempotent)
    if 'name="business"' not in text:
        m = NAME_FIELD_PATTERN.search(text)
        if m:
            insert = '\n                ' + build_business_field(s)
            text = text[:m.end()] + insert + HONEYPOT_HTML + text[m.end():]
            changes.append("business+honeypot")

    # 2) Add receipt overlay before </body> (idempotent)
    if 'id="booking-receipt"' not in text:
        overlay = build_receipt_overlay(s)
        # Inject data attributes for JS to read translated status messages
        # We do this by adding data-* attrs to existing tags.
        # Easier: inline into the receipt-status element directly.
        overlay = overlay.replace(
            '<p id="receipt-status"',
            f'<p id="receipt-status" data-sent="{s["receipt_status_sent"]}" '
            f'data-failed="{s["receipt_status_failed"]}"',
        )
        # Add data-nights-label to overlay root
        overlay = overlay.replace(
            '<div id="booking-receipt"',
            f'<div id="booking-receipt" data-nights-label="{s["receipt_nights_label"]}"',
        )
        # Inject before </body>
        text = text.replace("</body>", overlay + "\n</body>", 1)
        changes.append("overlay")

    # 3) Add CSS (idempotent)
    if ".booking-receipt {" not in text:
        # Find the end of the <style> block — insert before </style>
        text = text.replace("</style>", RECEIPT_CSS + "    </style>", 1)
        changes.append("css")

    # 4) Add JS in its OWN <script> (lesson learned from earlier injection bug)
    # Insert just before the existing slideshow-handler <script> (or any first <script>
    # in body) — actually let's be careful: insert before the FIRST <script> tag in body.
    # Simpler: insert just before the Cloudflare WA comment.
    if 'Booking-form receipt overlay' not in text:
        cf_marker = "<!-- Cloudflare Web Analytics -->"
        if cf_marker in text:
            text = text.replace(cf_marker, RECEIPT_JS + "\n" + cf_marker, 1)
        else:
            # Fallback: just before </body>
            text = text.replace("</body>", RECEIPT_JS + "\n</body>", 1)
        changes.append("js")

    if changes:
        path.write_text(text, encoding="utf-8")
    return {"file": key, "changes": changes}


def main():
    print("=" * 60)
    for key in STRINGS:
        result = process(REPO / key, key)
        ops = ", ".join(result["changes"]) if result["changes"] else "(no change)"
        marker = "✅" if result["changes"] else "⏭"
        print(f"{marker} {result['file']:25s} → {ops}")
    print("=" * 60)


if __name__ == "__main__":
    main()
