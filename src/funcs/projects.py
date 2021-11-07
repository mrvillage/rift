from __future__ import annotations

from ..data.classes import Resources

__all__ = ("PROJECTS",)


PROJECTS = {
    "Advanced Engineering Corps": (
        "adv_engineering_corps",
        Resources(uranium=1000, munitions=10000, gasoline=10000, money=50000000),
    ),
    "Advanced Urban Planning": (
        "adv_city_planning",
        Resources(
            uranium=10000, aluminum=40000, steel=20000, munitions=20000, food=2500000
        ),
    ),
    "Arable Land Agency": (
        "arable_land_agency",
        Resources(coal=1500, lead=1500, money=3000000),
    ),
    "Arms Stockpile": (
        "armss",
        Resources(aluminum=125, steel=125, money=4000000),
    ),
    "Bauxiteworks": (
        "bauxitew",
        Resources(steel=750, gasoline=1500, money=5000000),
    ),
    "Center for Civil Engineering": (
        "cfce",
        Resources(oil=1000, iron=1000, bauxite=1000, money=3000000),
    ),
    "Clinical Research Center": (
        "clinical_research_center",
        Resources(food=100000, money=10000000),
    ),
    "Emergency Gasoline Reserve": (
        "egr",
        Resources(aluminum=125, steel=125, money=4000000),
    ),
    "Green Technologies": (
        "green_tech",
        Resources(
            iron=10000, steel=10000, aluminum=10000, food=250000, money=100000000
        ),
    ),
    "Intelligence Agency": ("cia", Resources(steel=500, gasoline=500, money=5000000)),
    "International Trade Center": (
        "itc",
        Resources(
            aluminum=2500,
            steel=2500,
            gasoline=5000,
            money=45000000,
        ),
    ),
    "Iron Dome": (
        "irond",
        Resources(aluminum=500, steel=1250, gasoline=500, money=6000000),
    ),
    "Ironworks": (
        "ironw",
        Resources(aluminum=750, gasoline=1500, money=5000000),
    ),
    "Mass Irrigation": ("massirr", Resources(aluminum=500, steel=500, money=3000000)),
    "Missile Launch Pad": ("mlp", Resources(steel=1000, gasoline=350, money=3000000)),
    "Moon Landing": (
        "moon_landing",
        Resources(
            oil=5000,
            munitions=5000,
            gasoline=5000,
            steel=5000,
            aluminum=5000,
            uranium=10000,
            money=50000000,
        ),
    ),
    "Nuclear Research Facility": (
        "nrf",
        Resources(steel=5000, gasoline=7500, money=50000000),
    ),
    "Pirate Economy": (
        "pirate_economy",
        Resources(
            aluminum=10000, munitions=10000, gasoline=10000, steel=10000, money=25000000
        ),
    ),
    "Propaganda Bureau": ("propb", Resources(aluminum=1500, money=15000000)),
    "Recycling Initiative": (
        "recycling_initiative",
        Resources(food=100000, money=10000000),
    ),
    "Space Program": (
        "space_program",
        Resources(
            uranium=20000,
            oil=20000,
            iron=10000,
            gasoline=5000,
            steel=1000,
            aluminum=1000,
            money=40000000,
        ),
    ),
    "Specialized Police Training Program": (
        "specialized_police_training",
        Resources(food=100000, money=10000000),
    ),
    "Spy Satellite": (
        "spy_satellite",
        Resources(
            oil=10000,
            iron=10000,
            lead=10000,
            bauxite=10000,
            uranium=10000,
            money=20000000,
        ),
    ),
    "Telecommunication Satellite": (
        "telecom_satellite",
        Resources(
            uranium=10000, iron=10000, oil=10000, aluminum=10000, money=300000000
        ),
    ),
    "Uranium Enrichment Program": (
        "uap",
        Resources(aluminum=1000, gasoline=1000, uranium=500, money=21000000),
    ),
    "Urban Planning": (
        "city_planning",
        Resources(
            coal=10000,
            oil=10000,
            aluminum=20000,
            munitions=10000,
            gasoline=10000,
            food=1000000,
        ),
    ),
    "Vital Defense System": (
        "vds",
        Resources(aluminum=3000, steel=6500, gasoline=5000, money=40000000),
    ),
}
