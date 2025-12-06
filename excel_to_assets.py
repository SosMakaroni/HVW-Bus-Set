#!/usr/bin/env python3
import os
import sys
import argparse
import shutil
import pandas as pd

def find_column(columns, keyword):
    """
    Visszaadja azt az oszlopnevet, amelynek a neve tartalmazza
    a keyword-et (kis-nagybetű-független).
    Ha nem talál megfelelőt, None-t ad vissza.
    """
    keyword = keyword.lower()
    for col in columns:
        if keyword in str(col).lower():
            return col
    return None

def safe_val(row, col):
    """Sor-dictből lekér egy oszlopot, NaN helyett üres stringet ad."""
    if not col or col not in row:
        return ''
    v = row[col]
    return '' if pd.isna(v) else str(v).strip()

def generate_nml(row, cm):
    """
    Létrehozza az egy sorhoz tartozó .nml tartalmat,
    a cm (col_map) alapján kinyeri az értékeket.
    """
    # értékek lekérése
    Fuel         = safe_val(row, cm['Fuel'])
    ItemID       = safe_val(row, cm['ItemID'])
    Color        = safe_val(row, cm['Color'])
    MDate        = safe_val(row, cm['MDate'])
    MPeroid      = safe_val(row, cm['MPeroid'])
    VLife        = safe_val(row, cm['VLife'])
    Reli         = safe_val(row, cm['Reli'])
    LoadingSpeed = safe_val(row, cm['LoadingSpeed'])
    PurchaseRow  = safe_val(row, cm['PurchasePrice'])
    MaintenanceRow = safe_val(row, cm['Maintenance'])
    Speed        = safe_val(row, cm['Speed'])
    Power        = safe_val(row, cm['Power'])
    Weight       = safe_val(row, cm['Weight'])
    Capacity     = safe_val(row, cm['Capacity'])
    Comfort      = safe_val(row, cm['Comfort'])
    Hossz1       = safe_val(row, cm['Hossz1'])
    Hossz2       = safe_val(row, cm['Hossz2'])
    Hossz3       = safe_val(row, cm['Hossz3'])
    Hossz4       = safe_val(row, cm['Hossz4'])
    Hossz5       = safe_val(row, cm['Hossz5'])
    Hossz6       = safe_val(row, cm['Hossz6'])
    Pos1       = safe_val(row, cm['Pos1'])
    Pos2       = safe_val(row, cm['Pos2'])
    Pos3       = safe_val(row, cm['Pos3'])
    PFolder      = safe_val(row, cm['PFolder'])
    Usage        = safe_val(row, cm['Usage'])
    Flag         = safe_val(row, cm['Flag'])

    # kerekített számok
    try:
        PurchasePrice = str(round(float(PurchaseRow or 0)))
    except ValueError:
        PurchasePrice = PurchaseRow
    try:
        Maintenance = str(round(float(MaintenanceRow or 0)))
    except ValueError:
        Maintenance = MaintenanceRow

    # szín és zászló logika
    Alapszin = '// ' if Color == 'CC1' else ''
    if 'CC' in Color:
        FlagCC = 'ROADVEH_FLAG_2CC, '
        Recolor = ''
    else:
        FlagCC = ''
        Recolor = 'colour_mapping:\tPALETTE_IDENTITY;'

    # badges mappelés
    badge_fuel = {
        'diesel':   ', "power/diesel"',
        'hybrid':   ', "power/steam"',
        'cng':      ', "power/naturgas"',
        'electric': ', "power/battery"',
        'petrol':   ', "power/diesel"',
        'hydrogen':   ', "power/hydrogen"',
    }
    BadgeFuel = badge_fuel.get(Fuel, '')

    badge_flag = {
        'CC':         ', "flag/flag_CC"',
        'Europe':     ', "flag/europe"',
        'Austria':', "flag/AT"',
        'Australia':', "flag/AU"',
        'Canada':', "flag/CA"',
        'Czech':', "flag/CZ"',
        'France':', "flag/FR"',
        'Germany':', "flag/DE"',
        'United Kingdom':', "flag/GB"',
        'Hungary':    ', "flag/HU"',
        'Romania':    ', "flag/RO"',
        'Russia':    ', "flag/RU"',
        'Slovenia':', "flag/SI"',
        'Slovakia':', "flag/SK"',
        'Switzerland':', "flag/CH"',
        'USA':', "flag/US"',
    }
    BadgeFlag = badge_flag.get(Flag, '')

    badge_usage = {
        'City':      ', "usage/city"',
        'Suburb':    ', "usage/suburb"',
        'Regional':  ', "usage/regional"',
        'Intercity': ', "usage/intercity"',
        'Tourist':   ', "usage/tourist"',
    }
    BadgeUsage = badge_usage.get(Usage, '')

    # spritesetek
    cs_graph1 = [] # grafika switch tartalma
    cs_graph2 = []
    cs_graph3 = []
    cs_graph4 = []
    cs_graph5 = []
    cs_graph6 = []

    pspr1 = [
        f"spriteset(ss_{ItemID}_{Color}_purchase, \"src/{PFolder}/{ItemID}_{Color}_8bpp.png\")\t\t{{tmpl{Pos1}_purchase()}}",
    ]
    spr1 = [
        f"spriteset(ss_{ItemID}_{Color}, \"src/{PFolder}/{ItemID}_{Color}_8bpp.png\")\t\t{{tmpl{Pos1}_1()}}",
        f"alternative_sprites(ss_{ItemID}_{Color}, ZOOM_LEVEL_IN_2X, BIT_DEPTH_8BPP, \"src/{PFolder}/{ItemID}_{Color}_8bpp.png\") {{tmpl{Pos1}_2()}}",
        f"alternative_sprites(ss_{ItemID}_{Color}, ZOOM_LEVEL_IN_4X, BIT_DEPTH_8BPP, \"src/{PFolder}/{ItemID}_{Color}_8bpp.png\") {{tmpl{Pos1}_4()}}",
    ]
    spr2 = []
    spr3 = []
    cs_graph1 = [
        f"\tss_{ItemID}_{Color};", # grafika switch
    ]
    if float(Hossz2 or 0) > 0:
        cs_graph1 = [
            f"\tss_toldat;", # grafika switch
        ]
        cs_graph2 = [
            f"\t1: ss_{ItemID}_{Color};", # grafika switch
        ]
        if float(Hossz3 or 0) > 0:
            pspr1 = [
                f"spriteset(ss_{ItemID}_{Color}_purchase, \"src/{PFolder}/{ItemID}_{Color}_8bpp.png\")\t\t{{tmpl25_purchase()}}",
            ]
            spr1 = [
                f"spriteset(ss_{ItemID}_{Color}_a, \"src/{PFolder}/{ItemID}_{Color}_a_8bpp.png\")\t\t{{tmpl{Pos1}_1()}}",
                f"alternative_sprites(ss_{ItemID}_{Color}_a, ZOOM_LEVEL_IN_2X, BIT_DEPTH_8BPP, \"src/{PFolder}/{ItemID}_{Color}_a_8bpp.png\") {{tmpl{Pos1}_2()}}",
                f"alternative_sprites(ss_{ItemID}_{Color}_a, ZOOM_LEVEL_IN_4X, BIT_DEPTH_8BPP, \"src/{PFolder}/{ItemID}_{Color}_a_8bpp.png\") {{tmpl{Pos1}_4()}}",
            ]
            spr2 = [
                f"spriteset(ss_{ItemID}_{Color}_b, \"src/{PFolder}/{ItemID}_{Color}_b_8bpp.png\")\t\t{{tmpl{Pos2}_1()}}",
                f"alternative_sprites(ss_{ItemID}_{Color}_b, ZOOM_LEVEL_IN_2X, BIT_DEPTH_8BPP, \"src/{PFolder}/{ItemID}_{Color}_b_8bpp.png\") {{tmpl{Pos2}_2()}}",
                f"alternative_sprites(ss_{ItemID}_{Color}_b, ZOOM_LEVEL_IN_4X, BIT_DEPTH_8BPP, \"src/{PFolder}/{ItemID}_{Color}_b_8bpp.png\") {{tmpl{Pos2}_4()}}",
            ]
            cs_graph2 = [
                f"\t1: ss_{ItemID}_{Color}_a;", # grafika switch
            ]
            cs_graph3 = [
                f"\t2: ss_{ItemID}_{Color}_b;", # grafika switch
            ]
            if float(Hossz4 or 0) > 0:
                cs_graph3 = [
                    f"\t2: ss_toldat;", # grafika switch
                ]
                cs_graph4 = [
                    f"\t3: ss_{ItemID}_{Color}_b;", # grafika switch
                ]
                if float(Hossz5 or 0) > 0:
                    spr3 = [
                        f"spriteset(ss_{ItemID}_{Color}_c, \"src/{PFolder}/{ItemID}_{Color}_c_8bpp.png\")\t\t{{tmpl{Pos3}_1()}}",
                        f"alternative_sprites(ss_{ItemID}_{Color}_c, ZOOM_LEVEL_IN_2X, BIT_DEPTH_8BPP, \"src/{PFolder}/{ItemID}_{Color}_c_8bpp.png\") {{tmpl{Pos3}_2()}}",
                        f"alternative_sprites(ss_{ItemID}_{Color}_c, ZOOM_LEVEL_IN_4X, BIT_DEPTH_8BPP, \"src/{PFolder}/{ItemID}_{Color}_c_8bpp.png\") {{tmpl{Pos3}_4()}}",
                    ]
                    cs_graph5 = [
                        f"\t4: ss_{ItemID}_{Color}_c;", # grafika switch
                    ]
                    if float(Hossz6 or 0) > 0:
                        cs_graph5 = [
                            f"\t4: ss_toldat;", # grafika switch
                        ]
                        cs_graph6 = [
                            f"\t5: ss_{ItemID}_{Color}_c;", # grafika switch
                        ]

    csuk1 = []
    if float(Hossz2 or 0) > 0:
        csuk1 = [
            "// Csukló item",
            f"item(FEAT_ROADVEHS, item_{ItemID}_{Color}_t) {{",
            f"  property {{",
            "      name:							string(STR_BUG);",
            "      climates_available:				bitmask(NO_CLIMATE);",
            "      introduction_date:				date(4999999,01,01);",
            "      cargo_allow_refit:				[PASS,TOUR];",
            "      loading_speed:					0;",
            "      cost_factor:					0;",
            "      running_cost_factor:			0;",
            "      sprite_id:						SPRITE_ID_NEW_ROADVEH;",
            f"      misc_flags:						bitmask({FlagCC}ROADVEH_FLAG_SPRITE_STACK);",
            "      refit_cost:						0;",
            "      running_cost_base:				RUNNING_COST_NONE;",
            "      power:							0 kW;",
            "      weight:							0 ton;",
            "      cargo_capacity:					0;",
            "      cargo_age_period:				0;",
            "   }",
            "   graphics {",
            f"      default:						sw_{ItemID}_{Color};",
            f"      {Recolor}",
            f"      length:							sw_{ItemID}_{Color}_length;",
            "   }",
            "}",
        ]
    """
   
    # csukló-lista és hossz-cases
    cs_graph = []
    if float(Hossz2 or 0) > 0: cs_graph.append(f"\t1: ss_toldat;")
    if float(Hossz3 or 0) > 0: cs_graph.append(f"\t2: ss_{ItemID}_{Color}_b;")
    if float(Hossz4 or 0) > 0: cs_graph.append(f"\t3: ss_toldat;")
    if float(Hossz5 or 0) > 0: cs_graph.append(f"\t4: ss_{ItemID}_{Color}_c;")
    if float(Hossz6 or 0) > 0: cs_graph.append(f"\t5: ss_toldat;")
    cs_grap1 = "_a" if float(Hossz3 or 0) > 0 else ""
    cs_graph.append(f"\tss_{ItemID}_{Color}{cs_grap1};")
    """

    length_cases = []
    if float(Hossz2 or 0) > 0: length_cases.append(f"\t1: return {Hossz2};")
    if float(Hossz3 or 0) > 0: length_cases.append(f"\t2: return {Hossz3};")
    if float(Hossz4 or 0) > 0: length_cases.append(f"\t3: return {Hossz4};")
    if float(Hossz5 or 0) > 0: length_cases.append(f"\t4: return {Hossz5};")
    if float(Hossz6 or 0) > 0: length_cases.append(f"\t5: return {Hossz6};")

    articu_parts = []
    if float(Hossz2 or 0) > 0: articu_parts.append(f"\t1: item_{ItemID}_{Color}_t;")
    if float(Hossz3 or 0) > 0: articu_parts.append(f"\t2: item_{ItemID}_{Color}_t;")
    if float(Hossz4 or 0) > 0: articu_parts.append(f"\t3: item_{ItemID}_{Color}_t;")
    if float(Hossz5 or 0) > 0: articu_parts.append(f"\t4: item_{ItemID}_{Color}_t;")
    if float(Hossz6 or 0) > 0: articu_parts.append(f"\t5: item_{ItemID}_{Color}_t;")

    # összerakjuk a .nml listát
    lines = []
    lines.append(f"// ---------- {ItemID}_{Color}")
    lines.append("")
    lines.extend(pspr1)
    lines.append("")
    lines.extend(spr1)
    if spr2:
        lines.append("")
        lines.extend(spr2)
    if spr3:
        lines.append("")
        lines.extend(spr3)
    lines.append("")
    lines.append("")
    lines.append("// Játékban grafika")
    lines.append(f"switch (FEAT_ROADVEHS, SELF, sw_{ItemID}_{Color}, position_in_consist ) {{")
    lines.extend(cs_graph2)
    lines.extend(cs_graph3)
    lines.extend(cs_graph4)
    lines.extend(cs_graph5)
    lines.extend(cs_graph6)
    lines.extend(cs_graph1)
    lines.append("}")
    lines.append("")
    lines.append("// Csuklosítás")
    lines.append(f"switch (FEAT_ROADVEHS, SELF, sw_{ItemID}_{Color}_articulated, extra_callback_info1) {{")
    lines.append(f"\t0: item_{ItemID}_{Color};")
    lines.extend(articu_parts)
    lines.append("    CB_RESULT_NO_MORE_ARTICULATED_PARTS;")
    lines.append("}")
    lines.append("")
    lines.append("// Modelhossz")
    lines.append(f"switch (FEAT_ROADVEHS, SELF, sw_{ItemID}_{Color}_length, position_in_consist) {{")
    lines.extend(length_cases)
    lines.append(f"    return {Hossz1};")
    lines.append("}")
    lines.append("")
    lines.append("// Szövegek")
    lines.append(f"switch(FEAT_ROADVEHS, SELF, sw_{ItemID}_{Color}_names, (extra_callback_info1 >> 8) & 0xFFFF) {{")
    lines.append(f"\t1: return string(STR_{ItemID}_{Color}_NAME2); // Almenü 1 név")
    lines.append(f"\treturn CB_RESULT_NO_TEXT;")
    lines.append("}")
    lines.append("")
    lines.append(f"switch(FEAT_ROADVEHS, SELF, sw_{ItemID}_{Color}_texts, extra_callback_info1 & 0xFF) {{")
    lines.append(f"\t0x11: return string(STR_{ItemID}_{Color}_INFO); // Jármű infóban név")
    lines.append(f"\t0x20: sw_{ItemID}_{Color}_names; // Vásárlási lista név")
    lines.append(f"\t0x21: return string(STR_{ItemID}_{Color}_NAME); // Elővásárlási név")
    lines.append(f"\treturn CB_RESULT_NO_TEXT;")
    lines.append("}")
    lines.append("")
    lines.append("// Item")
    lines.append(f"item(FEAT_ROADVEHS, item_{ItemID}_{Color}) {{")
    lines.append("    property {")
    props = [
        f"        name:                          string(STR_{ItemID}_{Color}_NAME);",
        "        climates_available:            bitmask(CLIMATE_TEMPERATE, CLIMATE_ARCTIC, CLIMATE_TROPICAL);",
        f"        introduction_date:             date({MDate},01,01);",
        f"        model_life:                    {MPeroid};",
        f"        vehicle_life:                  {VLife};",
        f"        reliability_decay:             {Reli};",
        "        cargo_allow_refit:             [PASS,TOUR];",
        f"        loading_speed:                 {LoadingSpeed};",
        "        sprite_id:                     SPRITE_ID_NEW_ROADVEH;",
        f"        speed:                    {Speed} km/h;",
        f"        misc_flags:                    bitmask({FlagCC}ROADVEH_FLAG_SPRITE_STACK);",
        "        refit_cost:                    0;",
        "        running_cost_base:             RUNNING_COST_ROADVEH;",
        f"        power:                         {Power} kW;",
        f"        weight:                        {Weight} ton;",
        f"        cargo_capacity:                {Capacity};",
        f"        cargo_age_period:              {Comfort};",
        "        sound_effect:                  SOUND_DEPARTURE_MODERN_BUS;",
        f"        {Alapszin}variant_group:                   item_{ItemID}_CC1;",
        f"        badges:                        [\"type/bus\"{BadgeFuel}{BadgeFlag}{BadgeUsage}];",
    ]
    lines.extend(props)
    lines.append("    }")
    lines.append("    graphics {")
    gfx = [
        f"        default:                       sw_{ItemID}_{Color};",
        f"        {Recolor}",
        f"        purchase:                      ss_{ItemID}_{Color}_purchase;",
        f"        articulated_part:             sw_{ItemID}_{Color}_articulated;",
        f"        length:                       sw_{ItemID}_{Color}_length;",
        f"        cost_factor:                  {PurchasePrice} * parapuco;",
        f"        running_cost_factor:          {Maintenance} * pararuco;",
        f"        additional_text:              string(STR_{ItemID}_{Color}_DATA);",
        f"        name:                         sw_{ItemID}_{Color}_texts;",
    ]
    lines.extend(gfx)
    lines.append("    }")
    lines.append("}")
    if csuk1:
        lines.append("")
        lines.extend(csuk1)
    lines.append(f"// ---------- {ItemID}_{Color} --- End")
    lines.append("")
    lines.append("")
    return "\n".join(lines)

def generate_lng(rows, cm):
    """
    Egyetlen jarmuszovegek.lng tartalom előállítása
    """
    """
    FuelCol     = cm['Fuel']
    ItemIDCol   = cm['ItemID']
    ColorCol    = cm['Color']
    LoadCol     = cm['LoadingSpeed']
    T1Col       = cm['TextType']
    TS1Col      = cm['TextSType1']
    TS2Col      = cm['TextSType2']
    TO1Col      = cm['TextOther1']
    TO2Col      = cm['TextOther2']
    """
    lines = []
    for row in rows:
        Fuel    = safe_val(row, cm['Fuel'])
        ItemID  = safe_val(row, cm['ItemID'])
        Color   = safe_val(row, cm['Color'])
        LiveryText   = safe_val(row, cm['LiveryText'])
        Loading = safe_val(row, cm['LoadingSpeed'])
        T1      = safe_val(row, cm['TextType'])
        TS1     = safe_val(row, cm['TextSType1'])
        TS2     = safe_val(row, cm['TextSType2'])
        TO1     = safe_val(row, cm['TextOther1'])
        TO2     = safe_val(row, cm['TextOther2'])
        # üres kapcsoló ha nincs subtype 1-2 szöveg
        comma1 = f"{TS1} " if TS1 else ""
        comma2 = f"{TS2}, " if TS2 else ""
        comma3 = f"{TS2} " if TS2 else ""
        # hajtás kapcsoló
        fuel_fmt = {
            'diesel':   '{GRAY}Diesel{BLACK}',
            'hybrid':   '{BLUE}Hybrid{BLACK}',
            'cng':      '{ORANGE}CNG{BLACK}',
            'electric': '{GREEN}Electric{BLACK}',
            'petrol':   '{GRAY}Petrol{BLACK}',
        }.get(Fuel, '')
        # maga a kiírás
        lines.append(f"")
        lines.append(f"# ---- {T1} {comma1}{comma3}{Color}")
        lines.append(f"STR_{ItemID}_{Color}_NAME\t\t:{T1} {comma1}{TS2}")
        lines.append(f"STR_{ItemID}_{Color}_NAME2\t:{LiveryText} livery")
        lines.append(
            f"STR_{ItemID}_{Color}_DATA\t\t:Loading speed: {{GOLD}}{Loading}{{BLACK}}{{}}"
            f"{{GOLD}}----------{{BLACK}}{{}}Type: {{GOLD}}{comma2}{TO2}, {TO1}{{BLACK}}{{}}{{STRING}}"
        )
        lines.append(f"STR_{ItemID}_{Color}_INFO\t\t:{T1} {{LTBLUE}}{comma3}- {TO1}{{BLACK}}")
    return "\n".join(lines)

def generate_sort(rows, cm):
    """
    Egyetlen sort.nml tartalom előállítása
    """
    ItemIDCol = cm['ItemID']
    ColorCol  = cm['Color']
    lines = []
    for row in rows:
        ItemID = safe_val(row, ItemIDCol)
        Color  = safe_val(row, ColorCol)
        lines.append(f"\titem_{ItemID}_{Color},")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="Excel → Generated (NML / LNG / SORT) fájlok"
    )
    parser.add_argument("excel", help="Bemeneti Excel fájl (.xlsx/.xls)")
    parser.add_argument("--nml",  action="store_true", help="külön .nml fájlok")
    parser.add_argument("--lng",  action="store_true", help="jarmuszovegek.lng")
    parser.add_argument("--sort", action="store_true", help="sort.nml")
    args = parser.parse_args()

    excel_path = os.path.abspath(args.excel)
    if not os.path.isfile(excel_path):
        sys.exit(f"Hiba: nem találom a fájlt: {args.excel}")

    # ha nincs kapcsoló, mindegyiket generáljuk
    if not (args.nml or args.lng or args.sort):
        args.nml = args.lng = args.sort = True

    # ----------------------------------------------------------------------------
    # Generated mappa előkészítése (tartalma törlődik, mappa megmarad)
    base_dir = os.path.dirname(excel_path)
    gen_dir  = os.path.join(base_dir, "Generated")
    if not os.path.isdir(gen_dir):
        os.makedirs(gen_dir, exist_ok=True)
    else:
        for entry in os.scandir(gen_dir):
            try:
                if entry.is_file() or entry.is_symlink():
                    os.remove(entry.path)
                elif entry.is_dir():
                    shutil.rmtree(entry.path)
            except Exception as e:
                print(f"FIGYELMEZTETÉS: nem sikerült törölni '{entry.name}': {e}")
    # ----------------------------------------------------------------------------

    # pandas – fejléc = első sor
    df = pd.read_excel(excel_path, header=0, dtype=str)
    df.fillna('', inplace=True)

    # oszlopnevek részleges egyezés alapján (substring)
    cols = df.columns.tolist()
    col_map = {
        'Fuel':           find_column(cols, 'fuel'),
        'ItemID':         find_column(cols, 'itemid'),
        'Color':          find_column(cols, 'color'),
        'LiveryText':     find_column(cols, 'liverytext'),
        'MDate':          find_column(cols, 'mdate'),
        'MPeroid':        find_column(cols, 'mperoid'),
        'VLife':          find_column(cols, 'vlife'),
        'Reli':           find_column(cols, 'reli'),
        'LoadingSpeed':   find_column(cols, 'tlspeed'),       # ha az oszlop neve 'Tlspeed'
        'PurchasePrice':  find_column(cols, 'purchaseprice'),  # pl. 'PurchasePrice'
        'Maintenance':    find_column(cols, 'maintenance'),
        'Speed':          find_column(cols, 'maxspeed'),       # pl. 'Maxspeed'
        'Power':          find_column(cols, 'powerkw'),        # pl. 'PowerkW'
        'Weight':         find_column(cols, 'weight'),
        'Capacity':       find_column(cols, 'tcapacity'),      # pl. 'Tcapacity'
        'Comfort':        find_column(cols, 'comfort'),
        'Hossz1':         find_column(cols, 'h1'),
        'Hossz2':         find_column(cols, 'h2'),
        'Hossz3':         find_column(cols, 'h3'),
        'Hossz4':         find_column(cols, 'h4'),
        'Hossz5':         find_column(cols, 'h5'),
        'Hossz6':         find_column(cols, 'h6'),
        'Pos1':           find_column(cols, 'pos1'),
        'Pos2':           find_column(cols, 'pos2'),
        'Pos3':           find_column(cols, 'pos3'),
        'PFolder':        find_column(cols, 'pfolder'),
        'Usage':          find_column(cols, 'usage'),
        'Flag':           find_column(cols, 'flag'),
        'TextType':       find_column(cols, 'type'),
        'TextSType1':     find_column(cols, 'Subtype1'),
        'TextSType2':     find_column(cols, 'Subtype2'),
        'TextOther1':     find_column(cols, 'Other1'),
        'TextOther2':     find_column(cols, 'Other2'),
    }

    # kiszűrjük az üres sorokat és azt, ahol nincs ItemID
    valid_df = df[df[col_map['ItemID']].str.strip().astype(bool)]
    valid_df = valid_df[valid_df.apply(lambda r: any(str(v).strip() for v in r), axis=1)]
    rows = valid_df.to_dict(orient='records')

    # .nml fájlok
    if args.nml:
        for r in rows:
            content = generate_nml(r, col_map)
            fname   = f"{safe_val(r, col_map['ItemID'])}_{safe_val(r, col_map['Color'])}.nml"
            with open(os.path.join(gen_dir, fname), 'w', encoding='utf-8') as f:
                f.write(content)
        print(f"[NML] {len(rows)} fájl → {gen_dir}")

    # .lng fájl
    if args.lng:
        lng_text = generate_lng(rows, col_map)
        outpath = os.path.join(gen_dir, '00_jarmuszovegek.lng')
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(lng_text)
        print("[LNG] jarmuszovegek.lng kész")

    # sort.nml
    if args.sort:
        sort_text = generate_sort(rows, col_map)
        outpath = os.path.join(gen_dir, '00_sort.nml')
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(sort_text)
        print("[SORT] sort.nml kész")

if __name__ == "__main__":
    main()
