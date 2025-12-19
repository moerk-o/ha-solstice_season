# Konzeptdokument: Home Assistant Integration `solstice_season`

**Version:** 1.5.0
**Datum:** 19. Dezember 2025
**Status:** ✅ Implementiert
**Zielplattform:** Home Assistant Custom Integration
**Entwicklungssprache:** Englisch (Code, Kommentare, Variablen)
**Übersetzungen:** Englisch (Fallback), Deutsch, Niederländisch
**Repository:** https://github.com/moerk-o/ha-solstice_season

---

## 1. Projektübersicht

### 1.1 Zielsetzung

Die Integration `solstice_season` stellt präzise, tagesgenaue saisonale Informationen als Sensoren in Home Assistant bereit. Im Gegensatz zur bestehenden `season`-Integration bietet sie:

- Aktuelle Jahreszeit
- Exakte Zeitstempel für alle vier Jahreszeitenwechsel (Sonnenwenden & Tagundnachtgleichen) inkl. Countdown
- Nächster Jahreszeitenwechsel mit Datum und Countdown
- Wahlweise astronomische oder meteorologische (kalendarische) Berechnung
- Tageslichttrend-Sensor (werden die Tage länger oder kürzer?) inkl. Countdown zur nächsten Trendwende
- Unterstützung für Nord- und Südhalbkugel
- Volle Mehrsprachigkeit über das HA-Translationssystem
- Unterstützung mehrerer Instanzen (z.B. für verschiedene Standorte oder Berechnungsmodi)

### 1.2 Inspiration & Referenz

Die Integration orientiert sich an der bestehenden `season`-Integration im Home Assistant Core:

- **Dokumentation:** https://www.home-assistant.io/integrations/season/
- **Quellcode:** https://github.com/home-assistant/core/tree/dev/homeassistant/components/season

### 1.3 Namenskonvention

- **Domain:** `solstice_season`
- **Entity-Präfix:** Vom User im ConfigFlow festgelegter Name (z.B. "Home" → `sensor.home_*`)

---

## 2. Berechnungsgrundlagen

### 2.1 Astronomischer vs. Meteorologischer Modus

Die Integration bietet zwei verschiedene Berechnungsmodi, die grundlegend unterschiedliche Ansätze zur Definition von Jahreszeiten verfolgen.

#### Astronomischer Modus

Der astronomische Modus basiert auf der tatsächlichen Position der Erde relativ zur Sonne. Die Erdachse ist um etwa 23,4° geneigt – diese Neigung ist der Grund, warum wir überhaupt Jahreszeiten haben. Im Laufe eines Jahres ändert sich dadurch der Winkel, in dem die Sonnenstrahlen auf verschiedene Regionen der Erde treffen.

**Die vier astronomischen Schlüsselereignisse:**

| Ereignis | Zeitraum | Was passiert |
|----------|----------|--------------|
| **März-Tagundnachtgleiche** | ca. 19.-21. März | Die Sonne steht exakt über dem Äquator. Tag und Nacht sind überall auf der Erde ungefähr gleich lang. |
| **Juni-Sonnenwende** | ca. 20.-22. Juni | Die Sonne erreicht ihren nördlichsten Punkt. Längster Tag auf der Nordhalbkugel, kürzester auf der Südhalbkugel. |
| **September-Tagundnachtgleiche** | ca. 21.-23. September | Die Sonne steht wieder exakt über dem Äquator. Erneut sind Tag und Nacht etwa gleich lang. |
| **Dezember-Sonnenwende** | ca. 20.-23. Dezember | Die Sonne erreicht ihren südlichsten Punkt. Kürzester Tag auf der Nordhalbkugel, längster auf der Südhalbkugel. |

Die exakten Zeitpunkte dieser Ereignisse variieren jedes Jahr um einige Stunden, da ein Sonnenjahr nicht exakt 365 Tage dauert. Die Integration berechnet diese Zeitpunkte mit der PyEphem-Bibliothek auf die Minute genau.

#### Meteorologischer Modus

Meteorologen und Klimaforscher verwenden einen vereinfachten Ansatz: Jahreszeiten beginnen immer am 1. des jeweiligen Monats. Dies hat praktische Gründe – es erleichtert statistische Auswertungen und den Vergleich von Klimadaten über Jahre hinweg erheblich.

**Meteorologische Jahreszeitengrenzen:**

| Jahreszeit | Nordhalbkugel | Südhalbkugel |
|------------|---------------|--------------|
| Frühling | 1. März | 1. September |
| Sommer | 1. Juni | 1. Dezember |
| Herbst | 1. September | 1. März |
| Winter | 1. Dezember | 1. Juni |

### 2.2 Hemisphären-Zuordnung

Da die Erdachse geneigt ist, erleben Nord- und Südhalbkugel die Jahreszeiten genau entgegengesetzt. Wenn auf der Nordhalbkugel Sommer ist, ist auf der Südhalbkugel Winter – und umgekehrt.

Die astronomischen Ereignisse selbst sind global identisch (die Juni-Sonnenwende findet weltweit zum selben Zeitpunkt statt), aber ihre **saisonale Bedeutung** unterscheidet sich:

| Astronomisches Ereignis | Nordhalbkugel | Südhalbkugel |
|------------------------|---------------|--------------|
| März-Tagundnachtgleiche | Frühlingsanfang | Herbstanfang |
| Juni-Sonnenwende | Sommeranfang | Winteranfang |
| September-Tagundnachtgleiche | Herbstanfang | Frühlingsanfang |
| Dezember-Sonnenwende | Winteranfang | Sommeranfang |

### 2.3 Der Tageslichttrend

Unabhängig von der saisonalen Zuordnung gibt es eine physikalische Realität: Nach der Dezember-Sonnenwende werden die Tage länger, nach der Juni-Sonnenwende werden sie kürzer. Dies gilt für beide Hemisphären gleichermaßen – es ist eine direkte Folge der Erdbahn um die Sonne.

Die Kalenderdaten des 1. Juni oder 1. Dezember haben keinen Einfluss auf die tatsächliche Tageslänge.

---

## 3. Sensoren im Detail

Die Integration stellt **8 Sensoren** bereit. Alle Sensoren gehören zu einem gemeinsamen Device, das den vom User gewählten Namen trägt.

### 3.1 `current_season` – Aktuelle Jahreszeit

#### Beschreibung

Zeigt die aktuell laufende Jahreszeit.

#### Berechnungslogik

Die aktuelle Jahreszeit wird je nach konfiguriertem Modus berechnet – siehe [Abschnitt 2.1](#21-astronomischer-vs-meteorologischer-modus) für Details zu den Unterschieden.

#### State-Werte und Icons

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_current_season` |
| **Device Class** | `enum` |
| **State Class** | `None` |

| State | Format | Icon |
|-------|--------|------|
| `spring` | enum | `mdi:flower` |
| `summer` | enum | `mdi:white-balance-sunny` |
| `autumn` | enum | `mdi:leaf` |
| `winter` | enum | `mdi:snowflake` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `mode` | `str` | `astronomical` oder `meteorological` – der gewählte Berechnungsmodus |
| `hemisphere` | `str` | `northern` oder `southern` – die gewählte Hemisphäre |
| `spring_start` | `str` (ISO 8601) | Datum des Frühlingsanfangs im laufenden Kalenderjahr |
| `summer_start` | `str` (ISO 8601) | Datum des Sommeranfangs im laufenden Kalenderjahr |
| `autumn_start` | `str` (ISO 8601) | Datum des Herbstanfangs im laufenden Kalenderjahr |
| `winter_start` | `str` (ISO 8601) | Datum des Winteranfangs im laufenden Kalenderjahr |
| `season_age` | `int` | Tage seit Beginn der aktuellen Jahreszeit (auch über Jahreswechsel korrekt) |

*Hinweis: Die `*_start`-Attribute beziehen sich immer auf das aktuelle Kalenderjahr. Am 1. Januar springt z.B. `winter_start` auf das Dezember-Datum des neuen Jahres, obwohl der laufende Winter noch aus dem Vorjahr stammt. Für eine zuverlässige Ermittlung, wie lange die aktuelle Jahreszeit schon andauert, sollte stattdessen `season_age` verwendet werden.*

---

### 3.2 `spring_equinox` – Frühlingsanfang

#### Beschreibung

Zeigt das Datum des nächsten Frühlingsanfangs. Nach Eintritt des Ereignisses springt der Sensor automatisch zum nächsten Jahr.

#### Berechnungslogik

Je nach Hemisphäre wird die März-Tagundnachtgleiche (Nord) oder September-Tagundnachtgleiche (Süd) verwendet – siehe [Abschnitt 2.2](#22-hemisphären-zuordnung).

#### State-Werte und Icons

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_spring_equinox` |
| **Device Class** | `timestamp` |
| **State Class** | `None` |

| State | Format | Icon |
|-------|--------|------|
| `<Sensorwert>` | string (ISO 8601) | `mdi:flower` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `days_until` | `int` | Verbleibende Tage bis zum Ereignis (0 am Tag selbst) |

---

### 3.3 `summer_solstice` – Sommeranfang

#### Beschreibung

Zeigt das Datum des nächsten Sommeranfangs. Nach Eintritt des Ereignisses springt der Sensor automatisch zum nächsten Jahr.

#### Berechnungslogik

Je nach Hemisphäre wird die Juni-Sonnenwende (Nord) oder Dezember-Sonnenwende (Süd) verwendet – siehe [Abschnitt 2.2](#22-hemisphären-zuordnung).

#### State-Werte und Icons

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_summer_solstice` |
| **Device Class** | `timestamp` |
| **State Class** | `None` |

| State | Format | Icon |
|-------|--------|------|
| `<Sensorwert>` | string (ISO 8601) | `mdi:white-balance-sunny` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `days_until` | `int` | Verbleibende Tage bis zum Ereignis |

---

### 3.4 `autumn_equinox` – Herbstanfang

#### Beschreibung

Zeigt das Datum des nächsten Herbstanfangs. Nach Eintritt des Ereignisses springt der Sensor automatisch zum nächsten Jahr.

#### Berechnungslogik

Je nach Hemisphäre wird die September-Tagundnachtgleiche (Nord) oder März-Tagundnachtgleiche (Süd) verwendet – siehe [Abschnitt 2.2](#22-hemisphären-zuordnung).

#### State-Werte und Icons

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_autumn_equinox` |
| **Device Class** | `timestamp` |
| **State Class** | `None` |

| State | Format | Icon |
|-------|--------|------|
| `<Sensorwert>` | string (ISO 8601) | `mdi:leaf` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `days_until` | `int` | Verbleibende Tage bis zum Ereignis |

---

### 3.5 `winter_solstice` – Winteranfang

#### Beschreibung

Zeigt das Datum des nächsten Winteranfangs. Nach Eintritt des Ereignisses springt der Sensor automatisch zum nächsten Jahr.

#### Berechnungslogik

Je nach Hemisphäre wird die Dezember-Sonnenwende (Nord) oder Juni-Sonnenwende (Süd) verwendet – siehe [Abschnitt 2.2](#22-hemisphären-zuordnung).

#### State-Werte und Icons

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_winter_solstice` |
| **Device Class** | `timestamp` |
| **State Class** | `None` |

| State | Format | Icon |
|-------|--------|------|
| `<Sensorwert>` | string (ISO 8601) | `mdi:snowflake` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `days_until` | `int` | Verbleibende Tage bis zum Ereignis |

---

### 3.6 `daylight_trend` – Tageslichttrend

#### Beschreibung

Zeigt an, ob die Tage gerade länger oder kürzer werden.

#### Berechnungslogik

Dieser Sensor verwendet **immer astronomische Solstices**, auch im meteorologischen Modus – siehe [Abschnitt 2.3](#23-der-tageslichttrend) für die Begründung.

#### State-Werte und Icons

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_daylight_trend` |
| **Device Class** | `enum` |
| **State Class** | `None` |

| State | Format | Icon |
|-------|--------|------|
| `days_getting_longer` | enum | `mdi:arrow-right-bold-outline` |
| `days_getting_shorter` | enum | `mdi:arrow-left-bold-outline` |
| `solstice_today` | enum | `mdi:arrow-left-right-bold-outline` |

#### Attributes

Keine zusätzlichen Attribute.

---

### 3.7 `next_daylight_trend_change` – Nächste Trendwende

#### Beschreibung

Zeigt das Datum der nächsten Sonnenwende an, da diese den Wendepunkt im Tageslichttrend markiert.

#### Berechnungslogik

Dieser Sensor verwendet **immer astronomische Solstices**, auch im meteorologischen Modus – siehe [Abschnitt 2.3](#23-der-tageslichttrend).

#### State-Werte und Icons

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_next_daylight_trend_change` |
| **Device Class** | `timestamp` |
| **State Class** | `None` |

| State | Format | Icon |
|-------|--------|------|
| `<Sensorwert>` | string (ISO 8601) | `mdi:sun-clock` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `days_until` | `int` | Verbleibende Tage bis zur nächsten Sonnenwende |
| `event_type` | `str` | `summer_solstice` oder `winter_solstice` (bezogen auf die Hemisphäre) |

---

### 3.8 `next_season_change` – Nächster Jahreszeitenwechsel

#### Beschreibung

Zeigt das Datum des nächsten Jahreszeitenwechsels und welche Jahreszeit dann beginnt.

#### Berechnungslogik

Verwendet den konfigurierten Modus (astronomisch oder meteorologisch) – siehe [Abschnitt 2.1](#21-astronomischer-vs-meteorologischer-modus).

#### State-Werte und Icons

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_next_season_change` |
| **Device Class** | `timestamp` |
| **State Class** | `None` |

| State | Format | Icon |
|-------|--------|------|
| `<Sensorwert>` | string (ISO 8601) | `mdi:timelapse` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `days_until` | `int` | Verbleibende Tage bis zum nächsten Jahreszeitenwechsel |
| `event_type` | `str` | `spring`, `summer`, `autumn`, oder `winter` – die kommende Jahreszeit |

---

## 4. ConfigFlow

### 4.1 Übersicht

Die Integration wird ausschließlich über die UI konfiguriert (kein YAML-Support). Der ConfigFlow besteht aus einem einzigen Schritt.

### 4.2 Konfigurationsparameter

| Parameter | Typ | Pflicht | Default | Beschreibung |
|-----------|-----|---------|---------|--------------|
| `name` | `str` | Ja | `Home` | Name der Instanz, wird zum Entity-Präfix |
| `hemisphere` | `select` | Ja | Wird aus der Home Assistant Home-Location vorbelegt | Hemisphäre: `northern` oder `southern` |
| `mode` | `select` | Ja | `astronomical` | Berechnungsmodus: `astronomical` oder `meteorological` |

---

## 5. Technische Referenz

Dieses Kapitel enthält technische Implementierungsdetails für Entwickler.

### 5.1 Projektsprache & Code-Style

Die gesamte Entwicklung erfolgt in **Englisch** – Code, Kommentare, Commit-Messages, Issues, Release Notes und Dokumentation. Dies ermöglicht globale Nutzung und Beiträge.

Bei der Entwicklung soll sich an folgenden Punkten orientiert werden:

- **Sprache:** Englisch für alle Variablen, Funktionen, Kommentare, Docstrings
- **Type Hints:** Überall verwenden
- **Docstrings:** Google-Style
- **Formatierung:** Black, isort
- **Linting:** Pylint, Flake8

### 5.2 Unique ID & Duplikat-Verhinderung

Die Unique ID basiert auf dem slugifizierten Namen:
```python
unique_id = slugify(user_input[CONF_NAME])
```

Dies ermöglicht mehrere Instanzen mit unterschiedlichen Namen, verhindert aber Duplikate mit gleichem Namen.

### 5.3 ConfigFlow-Ablauf

```
┌─────────────────────────────────────┐
│         async_step_user             │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ Name: [Home____________]    │    │
│  │                             │    │
│  │ Hemisphäre: [Nordhalbkugel▼]│    │
│  │             ├─Nordhalbkugel │    │
│  │             └─Südhalbkugel  │    │
│  │                             │    │
│  │ Modus: [Astronomisch    ▼]  │    │
│  │        ├─Astronomisch       │    │
│  │        └─Kalendarisch       │    │
│  └─────────────────────────────┘    │
│                                     │
│           [Absenden]                │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│      async_create_entry             │
│                                     │
│  - Unique ID setzen                 │
│  - Config Entry erstellen           │
│  - Integration Setup starten        │
└─────────────────────────────────────┘
```

### 5.4 Dateistruktur

```
solstice_season/
├── custom_components/
│   └── solstice_season/
│       ├── <Python-Module>      # Quellcode der Integration
│       └── translations/
│           └── <Sprachdateien>  # Übersetzungen (en.json, de.json, nl.json, ...)
├── assets/
│   └── <Grafiken>               # Icons und Logos (für HA Brands, HACS)
├── .github/
│   └── workflows/
│       └── <GitHub Actions>     # CI/CD Workflows (Validierung, Releases)
└── <Projekt-Root>               # Konfiguration, Dokumentation, Lizenz
```

### 5.5 Dependencies

#### Externe Libraries

| Library | Verwendung | In HA Core? |
|---------|------------|-------------|
| `ephem` | Berechnung der Sonnenwenden/Tagundnachtgleichen | ✅ Ja (von season-Integration verwendet) |

Die `ephem`-Library (PyEphem) wird auch von der Home Assistant Core `season`-Integration verwendet. Sie berechnet astronomische Ereignisse lokal ohne Internetverbindung.

**Referenz:** https://rhodesmill.org/pyephem/

#### Home Assistant Helpers

| Import | Verwendung |
|--------|------------|
| `homeassistant.core` | HomeAssistant-Instanz |
| `homeassistant.config_entries` | ConfigEntry, ConfigFlow |
| `homeassistant.components.sensor` | SensorEntity, SensorDeviceClass |
| `homeassistant.helpers.update_coordinator` | DataUpdateCoordinator, CoordinatorEntity |
| `homeassistant.helpers.device_registry` | DeviceInfo für Device-Gruppierung |
| `homeassistant.helpers.selector` | UI-Selektoren für ConfigFlow |
| `homeassistant.util.dt` | Zeitfunktionen (UTC-Handling) |
| `homeassistant.util.slugify` | Normalisierung von Namen zu IDs |

### 5.6 DataUpdateCoordinator

Die Integration verwendet den Home Assistant `DataUpdateCoordinator` für zentralisiertes Daten-Management. Alle 8 Sensoren beziehen ihre Daten aus einer einzigen Datenquelle, die vom Coordinator verwaltet wird.

**Update-Intervall:** 24 Stunden, beginnend ab dem Zeitpunkt des HA-Starts bzw. Integration-Ladens. Die Werte ändern sich nur tagesweise, häufigere Updates wären sinnlos.

**Berechnung:** Die Berechnungslogik (`calculate_season_data`) wird in einem Executor ausgeführt, um den Event Loop nicht zu blockieren. Die Funktion erhält `hemisphere` und `mode` aus der Config Entry.

### 5.7 Device-Registrierung

Alle 8 Sensoren einer Integration-Instanz werden unter einem gemeinsamen Device gruppiert, um sie in der Home Assistant UI logisch zusammenzufassen.

| Feld | Wert |
|------|------|
| **Name** | Vom User gewählter Name (z.B. "Home") |
| **Manufacturer** | "Solstice Season" |
| **Model** | Dynamisch: "Astronomical Calculator" oder "Meteorological Calculator" je nach Modus |
| **Software Version** | Version aus `manifest.json` |
| **Identifier** | `entry_id` der Config Entry |

### 5.8 Zeitberechnung

Alle Zeiten werden in **UTC** berechnet und gespeichert – das ist HA-Standard. Home Assistant konvertiert diese automatisch in die lokale Zeitzone des Users für die Anzeige. Siehe [HA DateTime Helpers](https://developers.home-assistant.io/docs/core/helpers/datetime/).

### 5.9 Berechnungslogik

Die fachlichen Grundlagen (astronomisch vs. meteorologisch, Hemisphären-Mapping, Tageslichttrend) sind in [Kapitel 2 – Berechnungsgrundlagen](#2-berechnungsgrundlagen) dokumentiert.

#### ephem-Bibliothek

Die `ephem`-Bibliothek berechnet die exakten Zeitpunkte der vier astronomischen Schlüsselereignisse. Die Ergebnisse werden in UTC-aware Datetimes konvertiert.

| ephem-Funktion | Ereignis |
|----------------|----------|
| `next_vernal_equinox` | März-Tagundnachtgleiche |
| `next_summer_solstice` | Juni-Sonnenwende |
| `next_autumnal_equinox` | September-Tagundnachtgleiche |
| `next_winter_solstice` | Dezember-Sonnenwende |

### 5.10 Übersetzungen

Die Integration nutzt das HA-Translationssystem mit `translation_key` auf Sensor-Ebene. Aktuell unterstützte Sprachen: **Englisch** (Fallback), **Deutsch**, **Niederländisch**.

#### Dateiformat

Übersetzungen liegen im Ordner `translations/` als JSON-Dateien. Pro Sprache eine Datei mit dem **ISO 639-1 Sprachcode** als Dateiname:

- `translations/en.json` – Englisch (Fallback)
- `translations/de.json` – Deutsch
- `translations/nl.json` – Niederländisch
- `translations/fr.json` – Französisch (Beispiel für neue Sprache)

Die Struktur innerhalb der JSON-Datei muss bei allen Sprachen identisch sein – nur die Textwerte werden übersetzt.

#### Übersetzte Bereiche

| JSON-Pfad | Beschreibung |
|-----------|--------------|
| `config.step.user` | ConfigFlow-Dialog (Titel, Beschreibung, Feldnamen) |
| `config.error` / `config.abort` | Fehlermeldungen im ConfigFlow |
| `selector.hemisphere` / `selector.mode` | Dropdown-Optionen |
| `entity.sensor.<key>.name` | Sensor-Namen |
| `entity.sensor.<key>.state` | State-Werte für ENUM-Sensoren |

#### Neue Sprache hinzufügen

1. Bestehende Datei kopieren: `cp translations/en.json translations/fr.json`
2. Alle Textwerte übersetzen (Schlüssel unverändert lassen)
3. Home Assistant neu starten

**Referenz:** [HA Internationalisierung](https://developers.home-assistant.io/docs/internationalization/core/)

### 5.11 manifest.json

Die `manifest.json` definiert die Metadaten der Integration. Relevante Felder:

| Feld | Wert | Erklärung |
|------|------|-----------|
| `domain` | `solstice_season` | Eindeutiger Identifier der Integration |
| `config_flow` | `true` | Integration nutzt UI-Konfiguration |
| `integration_type` | `service` | Keine Hardware, reiner Service |
| `iot_class` | `calculated` | Daten werden lokal berechnet, kein Netzwerk nötig |
| `requirements` | `["ephem>=4.1.0"]` | PyEphem für astronomische Berechnungen |
| `version` | `x.y.z` | Aktuelle Version (wird bei Releases aktualisiert) |

**Referenz:** [HA Integration Manifest](https://developers.home-assistant.io/docs/creating_integration_manifest/)

---

## 6. Ressourcen

#### Home Assistant Entwicklung

| Thema | Link |
|-------|------|
| Entwickler-Dokumentation (Einstieg) | https://developers.home-assistant.io/ |
| Integration Manifest | https://developers.home-assistant.io/docs/creating_integration_manifest/ |
| ConfigFlow | https://developers.home-assistant.io/docs/config_entries_config_flow_handler/ |
| Sensor Entity | https://developers.home-assistant.io/docs/core/entity/sensor/ |
| Internationalisierung | https://developers.home-assistant.io/docs/internationalization/core/ |
| Translation Keys | https://developers.home-assistant.io/docs/internationalization/core/#name-of-entities |
| DataUpdateCoordinator | https://developers.home-assistant.io/docs/integration_fetching_data/#coordinated-single-api-poll-for-data-for-all-entities |
| Zeit-Helpers | https://developers.home-assistant.io/docs/core/helpers/datetime/ |

#### Astronomische Referenzen

| Thema | Link |
|-------|------|
| Season (Wikipedia EN) | https://en.wikipedia.org/wiki/Season |
| Solstice (Wikipedia EN) | https://en.wikipedia.org/wiki/Solstice |
| Equinox (Wikipedia EN) | https://en.wikipedia.org/wiki/Equinox |
| PyEphem Library | https://rhodesmill.org/pyephem/ |

#### Referenz-Integrationen

| Integration | Link | Relevanz |
|-------------|------|----------|
| Season (HA Core) | https://github.com/home-assistant/core/tree/dev/homeassistant/components/season | Direkte Inspiration |
| Sun (HA Core) | https://github.com/home-assistant/core/tree/dev/homeassistant/components/sun | Astronomische Berechnungen |
| Moon (HA Core) | https://github.com/home-assistant/core/tree/dev/homeassistant/components/moon | Ähnliche Sensor-Struktur |

#### Python Referenzen

| Thema | Link |
|-------|------|
| datetime Modul | https://docs.python.org/3/library/datetime.html |
| typing Modul | https://docs.python.org/3/library/typing.html |

---

## 7. Release-Prozess

### Vor dem Release

- Alle Änderungen sind in `main` gemergt
- Version in `custom_components/solstice_season/manifest.json` erhöhen
- `RELEASENOTES.md` aktualisieren:
  - Neuen Versionsabschnitt oben hinzufügen
  - Issue-Nummern verlinken: `[#123](https://github.com/moerk-o/ha-solstice_season/issues/123)`
  - Vorherige Versionen darunter behalten
  - Einheitliche Abschnittsüberschriften und Icons aus vorherigen Releases verwenden:
    - ✨ New Features
    - 🐞 Bug Fixes
    - 🔧 Infrastructure
    - 📝 Documentation
    - 💬 Feedback Needed!
  - Bei neuen Abschnittstypen erst absprechen
- README.md bei Bedarf aktualisieren (neue Features/Attribute dokumentieren)
- Änderungen committen und pushen

### Release erstellen

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file RELEASENOTES.md
```

### Nach dem Release

- GitHub Workflow (`release.yml`) erstellt automatisch `solstice_season.zip` und hängt es an das Release an
- Prüfen, ob ZIP in den Release-Assets vorhanden ist

### Workflows

Folgende GitHub Actions Workflows laufen automatisch:

- **validate.yaml** - Läuft bei jedem Push/PR, validiert Home Assistant (Hassfest) und HACS-Kompatibilität. Erforderlich für HACS-Listing.
- **release.yml** - Läuft wenn ein Release veröffentlicht wird, erstellt und lädt das ZIP-Asset hoch.

---

## 8. Versionshistorie

Diese Tabelle bietet eine technische Übersicht der Änderungen pro Version. Für **user-freundliche Release Notes** mit detaillierten Beschreibungen, Issue-Links und Kategorisierung siehe [`RELEASENOTES.md`](RELEASENOTES.md).

| Version | Datum | Änderungen |
|---------|-------|------------|
| 1.0.0 | 02.12.2025 | Initiale Implementierung |
| 1.1.0 | 02.12.2025 | Wechsel von astral zu ephem Library |
| 1.1.1 | 02.12.2025 | Bugfix: Meteorologischer Modus verwendet jetzt Kalenderdaten für Timestamps |
| 1.2.0 | 09.12.2025 | Neuer Sensor: `next_season_change` |
| 1.3.0 | 12.12.2025 | Niederländische Übersetzung hinzugefügt |
| 1.4.0 | 17.12.2025 | Hemisphere Auto-Detection basierend auf Home-Location; Device Version zeigt Integration-Version |
| 1.5.0 | 19.12.2025 | Neues Attribut `season_age`; Bugfix: Daylight Trend im meteorologischen Modus (#3); Bugfix: Device Model zeigt korrekten Modus (#5) |

---

*Dieses Konzeptdokument dient als vollständige Spezifikation und Dokumentation der `solstice_season` Home Assistant Integration.*
