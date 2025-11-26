# helpers.py
def generate_query_variants(product_name: str, n: int = 3):
    base = f"{product_name} launch"
    variants = [f"{base} strategy", f"{base} competitors", f"{base} positioning"]
    return variants[:n]

def short_summary(texts):
    # placeholder summary
    return " | ".join([t[:120] for t in texts[:3]])
