def egyptian_fraction(numerator, denominator):
    result = []
    
    while numerator != 0:
        # Find the smallest unit fraction
        unit_fraction_denom = (denominator + numerator - 1) // numerator  # Ceiling of denominator/numerator
        
        result.append(unit_fraction_denom)
        
        # Update numerator and denominator
        numerator = numerator * unit_fraction_denom - denominator
        denominator *= unit_fraction_denom
    
    return result

# Example usage
numerator = 5
denominator = 6
fractions = egyptian_fraction(numerator, denominator)

print("Egyptian Fraction representation of {}/{}: ".format(numerator, denominator), end="")
for denom in fractions:
    print(f"1/{denom}", end=" + " if denom != fractions[-1] else "")
