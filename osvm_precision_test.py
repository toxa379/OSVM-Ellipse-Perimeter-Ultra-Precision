import matplotlib.pyplot as plt
import numpy as np
from scipy.special import ellipe

print("OSVM Manifest: Running stress-test on 1,000,000 ellipses...")
N = 1_000_000
a = 1.0
b = np.random.uniform(0.0, 1.0, N)

pi = np.pi

# 1. Parameter of space deformation (Almansi finite strain tensor)
h = ((a - b) / (a + b)) ** 2

# 2. First basis: Ramanujan's second formula
P_ramanujan = pi * (a + b) * (1 + (3 * h) / (10 + np.sqrt(4 - 3 * h)))

# 3. OSVM Calibrated Resonance Constants (10 decimal places)
C1 =  0.0000211665
C2 =  0.0001537074
C3 =  0.0000462509
C4 =  0.0002842561

# 4. Multi-stage interference wave damper
correction = pi * (a + b) * (C1 * (h**4) + C2 * (h**8) + C3 * (h**12) + C4 * (h**16))

# Total perimeter of OSVM Monolithic model
P_osvm = P_ramanujan + correction

# 5. Reference values via Gauss Elliptic Integral
e_sq = 1 - (b / a) ** 2
P_exact = 4 * a * ellipe(e_sq)

# 6. Calculate relative error in %
errors = ((P_osvm - P_exact) / P_exact) * 100

print("\n--- OSVM MONOLITH PRECISION RESULTS ---")
print(f"Max relative error: {np.max(np.abs(errors)):.8f}%")
print(f"Min relative error: {np.min(np.abs(errors)):.8f}%")
print(f"Root Mean Square Error (RMS): {np.mean(np.abs(errors)):.8f}%")

# Plotting the flat horizon
sort_idx = np.argsort(b)
plt.figure(figsize=(11, 6))
plt.plot(b[sort_idx], errors[sort_idx], color="indigo", linewidth=2.5, label="OSVM Model")
plt.axhline(0, color="black", linestyle="--", alpha=0.6)
plt.title("OSVM Manifest: Flattened Horizon of Precision")
plt.xlabel("Aspect ratio b/a (1.0 = Circle, 0.0 = Line)")
plt.ylabel("Formula Error (%)")
plt.grid(True, which='both', linestyle=':', alpha=0.5)
plt.xlim(1.0, 0.0)
plt.ylim(-0.001, 0.001)
plt.legend()
plt.show()
