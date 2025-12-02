# Konzeptdokument: Home Assistant Integration `solstice_season`

**Version:** 1.1
**Datum:** 2. Dezember 2025  
**Zielplattform:** Home Assistant Custom Integration  
**Entwicklungssprache:** Englisch (Code, Kommentare, Variablen)  
**Übersetzungen:** Englisch (Fallback), Deutsch

---

## 1. Projektübersicht

### 1.1 Zielsetzung

Die Integration `solstice_season` stellt präzise, tagesgenaue saisonale Informationen als Sensoren in Home Assistant bereit. Im Gegensatz zur bestehenden `season`-Integration bietet sie:

- Exakte Zeitstempel für alle astronomischen Ereignisse (Sonnenwenden & Tagundnachtgleichen)
- Einen Tageslichttrend-Sensor (werden die Tage länger oder kürzer?)
- Volle Mehrsprachigkeit über das HA-Translationssystem
- Unterstützung für mehrere Instanzen (z.B. für verschiedene Standorte)

### 1.2 Inspiration & Referenz

Die Integration orientiert sich an der bestehenden `season`-Integration im Home Assistant Core:

- **Dokumentation:** https://www.home-assistant.io/integrations/season/
- **Quellcode:** https://github.com/home-assistant/core/tree/dev/homeassistant/components/season

### 1.3 Namenskonvention

- **Domain:** `solstice_season`
- **Entity-Präfix:** Vom User im ConfigFlow festgelegter Name (z.B. "Home" → `sensor.home_*`)

---

## 2. Sensoren im Detail

Die Integration stellt **7 Sensoren** bereit. Alle Sensoren gehören zu einem gemeinsamen Device, das den vom User gewählten Namen trägt.

### 2.1 `current_season` – Aktuelle Jahreszeit

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_current_season` |
| **Device Class** | `None` (kein Standard-Device-Class passend) |
| **State Class** | `None` |
| **State** | `spring` \| `summer` \| `autumn` \| `winter` |
| **Icon** | Dynamisch je nach State (siehe unten) |

#### State-Werte und Icons

| State | Icon | DE Translation | EN Translation |
|-------|------|----------------|----------------|
| `spring` | `mdi:flower` | Frühling | Spring |
| `summer` | `mdi:white-balance-sunny` | Sommer | Summer |
| `autumn` | `mdi:leaf` | Herbst | Autumn |
| `winter` | `mdi:snowflake` | Winter | Winter |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `mode` | `str` | `astronomical` oder `meteorological` – der gewählte Berechnungsmodus |
| `hemisphere` | `str` | `northern` oder `southern` – die gewählte Hemisphäre |
| `spring_start` | `str` (ISO 8601) | Datum des Frühlingsanfangs im aktuellen Jahr |
| `summer_start` | `str` (ISO 8601) | Datum des Sommeranfangs im aktuellen Jahr |
| `autumn_start` | `str` (ISO 8601) | Datum des Herbstanfangs im aktuellen Jahr |
| `winter_start` | `str` (ISO 8601) | Datum des Winteranfangs im aktuellen Jahr |

#### Berechnungslogik

**Astronomischer Modus:**
- Basiert auf den exakten Zeitpunkten der Sonnenwenden und Tagundnachtgleichen
- Verwendet die `ephem`-Library (PyEphem) zur Berechnung

**Meteorologischer (Kalendarischer) Modus:**
- Nordhalbkugel: Frühling ab 1. März, Sommer ab 1. Juni, Herbst ab 1. September, Winter ab 1. Dezember
- Südhalbkugel: Frühling ab 1. September, Sommer ab 1. Dezember, Herbst ab 1. März, Winter ab 1. Juni

---

### 2.2 `spring_equinox` – Frühlingsanfang

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_spring_equinox` |
| **Device Class** | `timestamp` |
| **State Class** | `None` |
| **State** | ISO 8601 Timestamp (z.B. `2026-03-20T09:01:00+00:00`) |
| **Icon** | `mdi:flower` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `days_until` | `int` | Verbleibende Tage bis zum Ereignis (0 am Tag selbst) |

#### Verhalten

- Zeigt immer das **nächste** Frühlingsanfangs-Datum
- Nach Eintritt des Ereignisses springt der Sensor automatisch zum nächsten Jahr
- Die Hemisphären-Zuordnung ist dynamisch:
  - **Nordhalbkugel:** März-Tagundnachtgleiche
  - **Südhalbkugel:** September-Tagundnachtgleiche

---

### 2.3 `summer_solstice` – Sommeranfang

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_summer_solstice` |
| **Device Class** | `timestamp` |
| **State Class** | `None` |
| **State** | ISO 8601 Timestamp |
| **Icon** | `mdi:white-balance-sunny` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `days_until` | `int` | Verbleibende Tage bis zum Ereignis |

#### Hemisphären-Zuordnung

- **Nordhalbkugel:** Juni-Sonnenwende
- **Südhalbkugel:** Dezember-Sonnenwende

---

### 2.4 `autumn_equinox` – Herbstanfang

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_autumn_equinox` |
| **Device Class** | `timestamp` |
| **State Class** | `None` |
| **State** | ISO 8601 Timestamp |
| **Icon** | `mdi:leaf` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `days_until` | `int` | Verbleibende Tage bis zum Ereignis |

#### Hemisphären-Zuordnung

- **Nordhalbkugel:** September-Tagundnachtgleiche
- **Südhalbkugel:** März-Tagundnachtgleiche

---

### 2.5 `winter_solstice` – Winteranfang

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_winter_solstice` |
| **Device Class** | `timestamp` |
| **State Class** | `None` |
| **State** | ISO 8601 Timestamp |
| **Icon** | `mdi:snowflake` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `days_until` | `int` | Verbleibende Tage bis zum Ereignis |

#### Hemisphären-Zuordnung

- **Nordhalbkugel:** Dezember-Sonnenwende
- **Südhalbkugel:** Juni-Sonnenwende

---

### 2.6 `daylight_trend` – Tageslichttrend

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_daylight_trend` |
| **Device Class** | `enum` |
| **State Class** | `None` |
| **State** | `days_getting_longer` \| `days_getting_shorter` \| `solstice_today` |
| **Icon** | Dynamisch (siehe unten) |

#### State-Werte und Icons

| State | Icon | DE Translation | EN Translation |
|-------|------|----------------|----------------|
| `days_getting_longer` | `mdi:arrow-right-bold-outline` | Tage werden länger | Days getting longer |
| `days_getting_shorter` | `mdi:arrow-left-bold-outline` | Tage werden kürzer | Days getting shorter |
| `solstice_today` | `mdi:arrow-left-right-bold-outline` | Sonnenwende heute | Solstice today |

#### Attributes

Keine zusätzlichen Attribute.

#### Berechnungslogik

- Nach der **Wintersonnenwende** bis zur **Sommersonnenwende**: `days_getting_longer`
- Nach der **Sommersonnenwende** bis zur **Wintersonnenwende**: `days_getting_shorter`
- Am Tag einer **Sonnenwende**: `solstice_today`

**Wichtig:** Die Logik ist hemisphären-unabhängig, da sie sich nur auf die Sonnenwenden bezieht (nicht auf deren saisonale Bedeutung).

---

### 2.7 `next_daylight_trend_change` – Nächste Trendwende

| Eigenschaft | Wert |
|-------------|------|
| **Entity ID Pattern** | `sensor.{prefix}_next_daylight_trend_change` |
| **Device Class** | `timestamp` |
| **State Class** | `None` |
| **State** | ISO 8601 Timestamp der nächsten Sonnenwende |
| **Icon** | `mdi:sun-clock` |

#### Attributes

| Attribut | Typ | Beschreibung |
|----------|-----|--------------|
| `days_until` | `int` | Verbleibende Tage bis zur nächsten Sonnenwende |
| `event_type` | `str` | `summer_solstice` oder `winter_solstice` (bezogen auf die Hemisphäre) |

#### Verhalten

Zeigt immer die **nächste Sonnenwende** an, da diese den Wendepunkt im Tageslichttrend markiert.

---

## 3. ConfigFlow

### 3.1 Übersicht

Die Integration wird ausschließlich über die UI konfiguriert (kein YAML-Support). Der ConfigFlow besteht aus einem einzigen Schritt.

### 3.2 Konfigurationsparameter

| Parameter | Typ | Pflicht | Default | Beschreibung |
|-----------|-----|---------|---------|--------------|
| `name` | `str` | Ja | `Home` | Name der Instanz, wird zum Entity-Präfix |
| `hemisphere` | `select` | Ja | `northern` | Hemisphäre: `northern` oder `southern` |
| `mode` | `select` | Ja | `astronomical` | Berechnungsmodus: `astronomical` oder `meteorological` |

### 3.3 Unique ID

Die Unique ID basiert auf dem slugifizierten Namen:
```python
unique_id = slugify(user_input[CONF_NAME])
```

Dies ermöglicht mehrere Instanzen mit unterschiedlichen Namen, verhindert aber Duplikate mit gleichem Namen.

### 3.4 ConfigFlow-Ablauf

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

---

## 4. Dateistruktur

```
custom_components/
└── solstice_season/
    ├── __init__.py              # Integration Setup & Entry Points
    ├── manifest.json            # Metadaten, Dependencies, Version
    ├── const.py                 # Konstanten (Domain, Keys, Defaults)
    ├── config_flow.py           # UI-Konfiguration
    ├── coordinator.py           # DataUpdateCoordinator für tägliche Updates
    ├── sensor.py                # Sensor-Entitäten
    ├── calculations.py          # Astronomische Berechnungslogik
    └── translations/
        ├── en.json              # Englische Übersetzungen (Fallback)
        └── de.json              # Deutsche Übersetzungen
```

---

## 5. Technische Implementierung

### 5.1 Dependencies

#### Externe Libraries

| Library | Verwendung | In HA Core? |
|---------|------------|-------------|
| `ephem` | Berechnung der Sonnenwenden/Tagundnachtgleichen | ✅ Ja (von season-Integration verwendet) |

Die `ephem`-Library (PyEphem) wird auch von der Home Assistant Core `season`-Integration verwendet. Sie berechnet astronomische Ereignisse lokal ohne Internetverbindung.

**Referenz:** https://rhodesmill.org/pyephem/

#### Home Assistant Helpers

```python
from homeassistant.util import dt as dt_util  # Zeitfunktionen
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
```

### 5.2 Update-Intervall

```python
from datetime import timedelta

SCAN_INTERVAL = timedelta(days=1)
```

Die Daten werden einmal täglich aktualisiert. Ein häufigeres Update ist nicht notwendig, da sich die Werte nur tagesweise ändern.

**Empfehlung:** Update um Mitternacht UTC triggern, um saubere Tageswechsel zu gewährleisten.

### 5.3 DataUpdateCoordinator

Die Integration verwendet einen `DataUpdateCoordinator` für effizientes, zentralisiertes Daten-Update:

```python
class SolsticeSeasonCoordinator(DataUpdateCoordinator):
    """Coordinator for solstice season data."""
    
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(days=1),
        )
        self.hemisphere = config_entry.data[CONF_HEMISPHERE]
        self.mode = config_entry.data[CONF_MODE]
    
    async def _async_update_data(self) -> dict:
        """Fetch data from calculations."""
        return await self.hass.async_add_executor_job(
            calculate_season_data,
            self.hemisphere,
            self.mode,
        )
```

### 5.4 Device-Registrierung

Alle Sensoren werden unter einem gemeinsamen Device gruppiert:

```python
@property
def device_info(self) -> DeviceInfo:
    """Return device information."""
    return DeviceInfo(
        identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
        name=self.coordinator.config_entry.data[CONF_NAME],
        manufacturer="Solstice Season",
        model="Astronomical Calculator",
        sw_version="1.0.0",
    )
```

### 5.5 Zeitberechnung

Alle Zeiten werden in **UTC** berechnet und gespeichert. Home Assistant konvertiert diese automatisch in die lokale Zeitzone des Users für die Anzeige.

```python
from homeassistant.util import dt as dt_util

# Aktuelles Datum in UTC
now = dt_util.utcnow()

# Timestamp für Sensor-State
timestamp = event_datetime.isoformat()
```

**Referenz:** https://developers.home-assistant.io/docs/core/helpers/datetime/

---

## 6. Berechnungslogik

### 6.1 Astronomische Ereignisse mit `ephem`

```python
import ephem
from datetime import datetime, timezone

def _ephem_date_to_datetime(ephem_date: ephem.Date) -> datetime:
    """Convert an ephem.Date to a timezone-aware UTC datetime."""
    return ephem_date.datetime().replace(tzinfo=timezone.utc)

def get_astronomical_events(year: int) -> dict:
    """Get all astronomical events for a given year."""
    jan_first = ephem.Date(f"{year}/1/1")

    return {
        "march_equinox": _ephem_date_to_datetime(ephem.next_vernal_equinox(jan_first)),
        "june_solstice": _ephem_date_to_datetime(ephem.next_summer_solstice(jan_first)),
        "september_equinox": _ephem_date_to_datetime(ephem.next_autumnal_equinox(jan_first)),
        "december_solstice": _ephem_date_to_datetime(ephem.next_winter_solstice(jan_first)),
    }
```

### 6.2 Hemisphären-Mapping

Die astronomischen Ereignisse sind fix (März, Juni, September, Dezember), aber ihre saisonale Bedeutung hängt von der Hemisphäre ab:

```python
# Mapping: Welches astronomische Ereignis markiert welchen Jahreszeitenanfang?

SEASON_MAPPING = {
    "northern": {
        "spring": "march_equinox",      # Frühlingsanfang = März-Tagundnachtgleiche
        "summer": "june_solstice",       # Sommeranfang = Juni-Sonnenwende
        "autumn": "september_equinox",   # Herbstanfang = September-Tagundnachtgleiche
        "winter": "december_solstice",   # Winteranfang = Dezember-Sonnenwende
    },
    "southern": {
        "spring": "september_equinox",   # Frühlingsanfang = September-Tagundnachtgleiche
        "summer": "december_solstice",   # Sommeranfang = Dezember-Sonnenwende
        "autumn": "march_equinox",       # Herbstanfang = März-Tagundnachtgleiche
        "winter": "june_solstice",       # Winteranfang = Juni-Sonnenwende
    },
}
```

### 6.3 Meteorologische Saisonberechnung

```python
METEOROLOGICAL_SEASONS = {
    "northern": {
        "spring": (3, 1),   # 1. März
        "summer": (6, 1),   # 1. Juni
        "autumn": (9, 1),   # 1. September
        "winter": (12, 1),  # 1. Dezember
    },
    "southern": {
        "spring": (9, 1),   # 1. September
        "summer": (12, 1),  # 1. Dezember
        "autumn": (3, 1),   # 1. März
        "winter": (6, 1),   # 1. Juni
    },
}
```

### 6.4 Berechnung `days_until`

```python
from datetime import date

def calculate_days_until(target_date: date) -> int:
    """Calculate days until a target date."""
    today = dt_util.utcnow().date()
    delta = target_date - today
    return max(0, delta.days)
```

### 6.5 Berechnung des Tageslichttrends

```python
def calculate_daylight_trend(
    hemisphere: str,
    now: datetime,
    june_solstice: datetime,
    december_solstice: datetime,
) -> str:
    """Determine if days are getting longer or shorter."""
    
    # Am Tag einer Sonnenwende
    if now.date() == june_solstice.date() or now.date() == december_solstice.date():
        return "solstice_today"
    
    # Nordhalbkugel:
    # - Nach Dezember-Sonnenwende bis Juni-Sonnenwende: Tage werden länger
    # - Nach Juni-Sonnenwende bis Dezember-Sonnenwende: Tage werden kürzer
    
    # Südhalbkugel: Gleiche Logik, da es um absolute Tageslänge geht,
    # nicht um die saisonale Bedeutung
    
    year = now.year
    
    # Finde die relevanten Sonnenwenden
    if now < june_solstice:
        # Wir sind vor der Juni-Sonnenwende -> Tage werden länger
        return "days_getting_longer"
    elif now < december_solstice:
        # Wir sind nach Juni, vor Dezember -> Tage werden kürzer
        return "days_getting_shorter"
    else:
        # Wir sind nach der Dezember-Sonnenwende -> Tage werden länger
        return "days_getting_longer"
```

---

## 7. Übersetzungen

### 7.1 Struktur der `strings.json` / `en.json`

```json
{
  "config": {
    "step": {
      "user": {
        "title": "Configure Solstice Season",
        "description": "Set up astronomical season tracking",
        "data": {
          "name": "Name",
          "hemisphere": "Hemisphere",
          "mode": "Calculation mode"
        }
      }
    },
    "error": {
      "already_configured": "An instance with this name already exists"
    },
    "abort": {
      "already_configured": "This instance is already configured"
    }
  },
  "selector": {
    "hemisphere": {
      "options": {
        "northern": "Northern Hemisphere",
        "southern": "Southern Hemisphere"
      }
    },
    "mode": {
      "options": {
        "astronomical": "Astronomical",
        "meteorological": "Meteorological (Calendar-based)"
      }
    }
  },
  "entity": {
    "sensor": {
      "current_season": {
        "name": "Current Season",
        "state": {
          "spring": "Spring",
          "summer": "Summer",
          "autumn": "Autumn",
          "winter": "Winter"
        }
      },
      "spring_equinox": {
        "name": "Spring Equinox"
      },
      "summer_solstice": {
        "name": "Summer Solstice"
      },
      "autumn_equinox": {
        "name": "Autumn Equinox"
      },
      "winter_solstice": {
        "name": "Winter Solstice"
      },
      "daylight_trend": {
        "name": "Daylight Trend",
        "state": {
          "days_getting_longer": "Days getting longer",
          "days_getting_shorter": "Days getting shorter",
          "solstice_today": "Solstice today"
        }
      },
      "next_daylight_trend_change": {
        "name": "Next Trend Change"
      }
    }
  }
}
```

### 7.2 Deutsche Übersetzung (`de.json`)

```json
{
  "config": {
    "step": {
      "user": {
        "title": "Solstice Season konfigurieren",
        "description": "Astronomische Jahreszeitenerfassung einrichten",
        "data": {
          "name": "Name",
          "hemisphere": "Hemisphäre",
          "mode": "Berechnungsmodus"
        }
      }
    },
    "error": {
      "already_configured": "Eine Instanz mit diesem Namen existiert bereits"
    },
    "abort": {
      "already_configured": "Diese Instanz ist bereits konfiguriert"
    }
  },
  "selector": {
    "hemisphere": {
      "options": {
        "northern": "Nordhalbkugel",
        "southern": "Südhalbkugel"
      }
    },
    "mode": {
      "options": {
        "astronomical": "Astronomisch",
        "meteorological": "Kalendarisch (Meteorologisch)"
      }
    }
  },
  "entity": {
    "sensor": {
      "current_season": {
        "name": "Aktuelle Jahreszeit",
        "state": {
          "spring": "Frühling",
          "summer": "Sommer",
          "autumn": "Herbst",
          "winter": "Winter"
        }
      },
      "spring_equinox": {
        "name": "Frühlingsanfang"
      },
      "summer_solstice": {
        "name": "Sommeranfang"
      },
      "autumn_equinox": {
        "name": "Herbstanfang"
      },
      "winter_solstice": {
        "name": "Winteranfang"
      },
      "daylight_trend": {
        "name": "Tageslichttrend",
        "state": {
          "days_getting_longer": "Tage werden länger",
          "days_getting_shorter": "Tage werden kürzer",
          "solstice_today": "Sonnenwende heute"
        }
      },
      "next_daylight_trend_change": {
        "name": "Nächste Trendwende"
      }
    }
  }
}
```

### 7.3 Translation Key Verwendung in Sensoren

```python
class CurrentSeasonSensor(CoordinatorEntity, SensorEntity):
    """Sensor for current season."""
    
    _attr_has_entity_name = True
    _attr_translation_key = "current_season"
    
    # Der Name wird automatisch aus translations geladen
```

**Referenz:** https://developers.home-assistant.io/docs/internationalization/core/#name-of-entities

---

## 8. manifest.json

```json
{
  "domain": "solstice_season",
  "name": "Solstice Season",
  "codeowners": ["@moerk-o"],
  "config_flow": true,
  "documentation": "https://github.com/moerk-o/ha-solstice_season",
  "integration_type": "service",
  "iot_class": "calculated",
  "issue_tracker": "https://github.com/moerk-o/ha-solstice_season/issues",
  "requirements": ["ephem>=4.1.0"],
  "version": "1.1.0"
}
```

### Erklärung der Felder

| Feld | Wert | Erklärung |
|------|------|-----------|
| `domain` | `solstice_season` | Eindeutiger Identifier der Integration |
| `config_flow` | `true` | Integration nutzt UI-Konfiguration |
| `integration_type` | `service` | Keine Hardware, reiner Service |
| `iot_class` | `calculated` | Daten werden lokal berechnet, kein Netzwerk nötig |
| `requirements` | `["ephem>=4.1.0"]` | PyEphem für astronomische Berechnungen |

**Referenz:** https://developers.home-assistant.io/docs/creating_integration_manifest/

---

## 9. Konstanten (`const.py`)

```python
"""Constants for the Solstice Season integration."""
from typing import Final

DOMAIN: Final = "solstice_season"

# Configuration keys
CONF_NAME: Final = "name"
CONF_HEMISPHERE: Final = "hemisphere"
CONF_MODE: Final = "mode"

# Default values
DEFAULT_NAME: Final = "Home"

# Hemisphere options
HEMISPHERE_NORTHERN: Final = "northern"
HEMISPHERE_SOUTHERN: Final = "southern"

# Mode options
MODE_ASTRONOMICAL: Final = "astronomical"
MODE_METEOROLOGICAL: Final = "meteorological"

# Season states
SEASON_SPRING: Final = "spring"
SEASON_SUMMER: Final = "summer"
SEASON_AUTUMN: Final = "autumn"
SEASON_WINTER: Final = "winter"

# Daylight trend states
TREND_LONGER: Final = "days_getting_longer"
TREND_SHORTER: Final = "days_getting_shorter"
TREND_SOLSTICE: Final = "solstice_today"

# Sensor keys
SENSOR_CURRENT_SEASON: Final = "current_season"
SENSOR_SPRING_EQUINOX: Final = "spring_equinox"
SENSOR_SUMMER_SOLSTICE: Final = "summer_solstice"
SENSOR_AUTUMN_EQUINOX: Final = "autumn_equinox"
SENSOR_WINTER_SOLSTICE: Final = "winter_solstice"
SENSOR_DAYLIGHT_TREND: Final = "daylight_trend"
SENSOR_NEXT_TREND_CHANGE: Final = "next_daylight_trend_change"

# Icons
ICON_SPRING: Final = "mdi:flower"
ICON_SUMMER: Final = "mdi:white-balance-sunny"
ICON_AUTUMN: Final = "mdi:leaf"
ICON_WINTER: Final = "mdi:snowflake"
ICON_TREND_LONGER: Final = "mdi:arrow-right-bold-outline"
ICON_TREND_SHORTER: Final = "mdi:arrow-left-bold-outline"
ICON_TREND_SOLSTICE: Final = "mdi:arrow-left-right-bold-outline"
```

---

## 10. Relevante Links & Dokumentation

### Home Assistant Entwicklung

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

### Astronomische Referenzen

| Thema | Link |
|-------|------|
| Jahreszeiten (Wikipedia DE) | https://de.wikipedia.org/wiki/Jahreszeit |
| Sonnenwende (Wikipedia DE) | https://de.wikipedia.org/wiki/Sonnenwende |
| Tagundnachtgleiche (Wikipedia DE) | https://de.wikipedia.org/wiki/Tagundnachtgleiche |
| PyEphem Library | https://rhodesmill.org/pyephem/ |

### Referenz-Integrationen

| Integration | Link | Relevanz |
|-------------|------|----------|
| Season (HA Core) | https://github.com/home-assistant/core/tree/dev/homeassistant/components/season | Direkte Inspiration |
| Sun (HA Core) | https://github.com/home-assistant/core/tree/dev/homeassistant/components/sun | Astronomische Berechnungen |
| Moon (HA Core) | https://github.com/home-assistant/core/tree/dev/homeassistant/components/moon | Ähnliche Sensor-Struktur |

### Python Referenzen

| Thema | Link |
|-------|------|
| datetime Modul | https://docs.python.org/3/library/datetime.html |
| typing Modul | https://docs.python.org/3/library/typing.html |

---

## 11. Entwicklungshinweise für Claude CLI

### 11.1 Reihenfolge der Implementierung

1. **`const.py`** – Alle Konstanten definieren
2. **`calculations.py`** – Reine Berechnungslogik (ohne HA-Dependencies)
3. **`manifest.json`** – Metadaten
4. **`config_flow.py`** – UI-Konfiguration
5. **`coordinator.py`** – DataUpdateCoordinator
6. **`sensor.py`** – Sensor-Entitäten
7. **`__init__.py`** – Integration Setup
8. **`translations/en.json`** – Englische Übersetzungen
9. **`translations/de.json`** – Deutsche Übersetzungen

### 11.2 Code-Style

- **Sprache:** Englisch für alle Variablen, Funktionen, Kommentare, Docstrings
- **Type Hints:** Überall verwenden
- **Docstrings:** Google-Style
- **Formatierung:** Black, isort
- **Linting:** Pylint, Flake8

### 11.3 Best Practices

```python
# Immer Type Hints verwenden
def calculate_days_until(target_date: date) -> int:
    """Calculate days until a target date.
    
    Args:
        target_date: The target date to calculate days until.
        
    Returns:
        Number of days until the target date, minimum 0.
    """
    ...

# Konstanten aus const.py importieren
from .const import DOMAIN, CONF_NAME, CONF_HEMISPHERE

# Logging verwenden
import logging
_LOGGER = logging.getLogger(__name__)

# has_entity_name für moderne Entity-Struktur
class MySensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "my_sensor"
```

### 11.4 Testing

Für zukünftige Tests können folgende Szenarien relevant sein:

1. **Hemisphären-Test:** Verifizieren, dass die Sensoren auf Nord- und Südhalbkugel korrekte Werte zeigen
2. **Jahreswechsel-Test:** Verhalten zum Jahresende prüfen
3. **Sonnenwende-Tag-Test:** Sonderfälle am Tag der Sonnenwende
4. **ConfigFlow-Test:** Validierung der Eingaben, Duplikat-Erkennung

---

## 12. Beispiel-Ausgabe

Nach erfolgreicher Installation und Konfiguration mit Name "Home", Nordhalbkugel, Astronomisch:

### Entities im Developer Tools

```yaml
sensor.home_current_season:
  state: "winter"
  attributes:
    mode: "astronomical"
    hemisphere: "northern"
    spring_start: "2025-03-20"
    summer_start: "2025-06-21"
    autumn_start: "2025-09-22"
    winter_start: "2024-12-21"
    friendly_name: "Home Aktuelle Jahreszeit"
    icon: "mdi:snowflake"

sensor.home_spring_equinox:
  state: "2025-03-20T09:01:00+00:00"
  attributes:
    days_until: 108
    device_class: "timestamp"
    friendly_name: "Home Frühlingsanfang"
    icon: "mdi:flower"

sensor.home_daylight_trend:
  state: "days_getting_longer"
  attributes:
    friendly_name: "Home Tageslichttrend"
    icon: "mdi:arrow-right-bold-outline"

sensor.home_next_daylight_trend_change:
  state: "2025-06-21T02:42:00+00:00"
  attributes:
    days_until: 201
    event_type: "summer_solstice"
    device_class: "timestamp"
    friendly_name: "Home Nächste Trendwende"
    icon: "mdi:sun-clock"
```

---

## 13. Checkliste für die Entwicklung

- [ ] `const.py` erstellen
- [ ] `calculations.py` erstellen und testen
- [ ] `manifest.json` erstellen
- [ ] `config_flow.py` implementieren
- [ ] `coordinator.py` implementieren
- [ ] `sensor.py` mit allen 7 Sensoren implementieren
- [ ] `__init__.py` für Integration Setup
- [ ] `translations/en.json` erstellen
- [ ] `translations/de.json` erstellen
- [ ] Manuelle Tests in Home Assistant
- [ ] README.md für GitHub erstellen

---

*Dieses Konzeptdokument dient als vollständige Spezifikation für die Entwicklung der `solstice_season` Home Assistant Integration.*
