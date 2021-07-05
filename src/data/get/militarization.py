def get_nation_militarization(nation):
    militarization = {
        "soldiers": nation.soldiers / (nation.cities * 15000),
        "tanks": nation.tanks / (nation.cities * 1250),
        "aircraft": nation.aircraft / (nation.cities * 75),
        "ships": nation.ships / (nation.cities * 15),
    }
    militarization["total"] = sum(militarization.values()) / 4
    return militarization
