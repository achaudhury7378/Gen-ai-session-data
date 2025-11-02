import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Helper Functions ---
def random_date(start, end):
    return start + timedelta(days=random.randint(0, int((end - start).days)))

def random_delay_reason():
    return random.choice(["Weather", "Customs", "Machine Breakdown", "Port Congestion", "None"])

# --- 1. Supplier Dataset ---
num_suppliers = 10
materials = [f"M{str(i).zfill(3)}" for i in range(1, 16)]

supplier_df = pd.DataFrame({
    "supplier_id": [f"S{i:03d}" for i in range(1, num_suppliers+1)],
    "supplier_name": [f"Supplier_{i}" for i in range(1, num_suppliers+1)],
    "material_id": np.random.choice(materials, num_suppliers),
    "avg_lead_time_days": np.random.randint(5, 20, num_suppliers),
    "on_time_delivery_rate": np.random.uniform(0.7, 0.98, num_suppliers).round(2),
    "current_delay_flag": np.random.choice([True, False], num_suppliers, p=[0.3, 0.7]),
    "delay_reason": [random_delay_reason() for _ in range(num_suppliers)],
    "reliability_score": np.random.uniform(0.6, 1.0, num_suppliers).round(2)
})

# --- 2. Procurement Dataset ---
num_pos = 30
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 3, 1)

procurement_df = pd.DataFrame({
    "po_id": [f"PO{1000+i}" for i in range(num_pos)],
    "material_id": np.random.choice(materials, num_pos),
    "supplier_id": np.random.choice(supplier_df["supplier_id"], num_pos),
    "order_date": [random_date(start_date, end_date).strftime("%Y-%m-%d") for _ in range(num_pos)],
    "expected_delivery_date": [(random_date(start_date, end_date) + timedelta(days=random.randint(5,15))).strftime("%Y-%m-%d") for _ in range(num_pos)],
    "quantity_ordered": np.random.randint(100, 1000, num_pos),
    "unit_price": np.random.uniform(10, 100, num_pos).round(2),
    "expedite_option": np.random.choice([True, False], num_pos, p=[0.4, 0.6]),
    "alternate_supplier_ids": [",".join(np.random.choice(supplier_df["supplier_id"], random.randint(1,3))) for _ in range(num_pos)]
})
# --- 3. Plant Dataset ---
plant_list = [
    {"plant_id": "P001", "plant_location": "Pune", "plant_name": "Pune Assembly"},
    {"plant_id": "P002", "plant_location": "Delhi", "plant_name": "Delhi Components"},
    {"plant_id": "P003", "plant_location": "Hyderabad", "plant_name": "Hyd Parts Plant"},
    {"plant_id": "P004", "plant_location": "Kolkata", "plant_name": "Kolkata Finishing"}
]

plant_df = pd.DataFrame(plant_list)

# --- 3. Logistics Dataset ---
# --- 4. Logistics Dataset ---
num_shipments = 25

# Randomly assign each shipment to one of the plants
logistics_records = []
for i in range(num_shipments):
    plant = random.choice(plant_list)
    po = random.choice(procurement_df["po_id"])
    status = np.random.choice(["In Transit", "Delayed", "Delivered"], p=[0.4, 0.2, 0.4])
    logistics_records.append({
        "shipment_id": f"SH{2000+i}",
        "po_id": po,
        "plant_id": plant["plant_id"],  # 🔗 Connects to Plant
        "destination": plant["plant_location"],
        "origin": random.choice(["Mumbai", "Chennai", "Shanghai", "Singapore", "Dubai"]),
        "route_id": f"R{random.randint(1,5)}",
        "carrier_id": f"C{random.randint(100,200)}",
        "status": status,
        "estimated_arrival": (datetime.now() + timedelta(days=random.randint(1,10))).strftime("%Y-%m-%d"),
        "delay_reason": random_delay_reason() if status == "Delayed" else "None",
        "reroute_possible": np.random.choice([True, False], p=[0.5, 0.5]),
        "lead_time_days": random.randint(3, 10)
    })

logistics_df = pd.DataFrame(logistics_records)


# --- 4. Production Dataset ---
plants = ["P001", "P002", "P003"]
production_df = pd.DataFrame({
    "plant_id": np.random.choice(plants, len(materials)),
    "material_id": materials,
    "inventory_level": np.random.randint(1000, 10000, len(materials)),
    "daily_consumption_rate": np.random.randint(50, 300, len(materials)),
    "criticality_score": np.random.uniform(0.5, 1.0, len(materials)).round(2),
    "current_status": np.random.choice(["Running", "Low Material", "Paused"], len(materials), p=[0.6, 0.3, 0.1])
})

# --- 5. Material Master Dataset ---
material_df = pd.DataFrame({
    "material_id": materials,
    "material_name": [f"Material_{i}" for i in range(1, len(materials)+1)],
    "category": np.random.choice(["Raw Material", "Packaging", "Component"], len(materials))
})

# --- Save to CSV ---
supplier_df.to_csv("supplier.csv", index=False)
procurement_df.to_csv("procurement.csv", index=False)
logistics_df.to_csv("logistics.csv", index=False)
production_df.to_csv("production.csv", index=False)
material_df.to_csv("material.csv", index=False)

print("✅ Synthetic supply chain data generated successfully!")
