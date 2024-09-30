import perlin
import matplotlib.pyplot as plt

# Initialize Perlin noise with seed
p = perlin2.Perlin(6789)

# Generate values for x1 and x2
x1 = []
x2 = []
for i in range(1000):
    x1.append(p.fade(p.two_octave(i, 1)))
    x2.append(p.fade(p.one_octave(i, 1)))

# Create a figure to plot both x1 and x2
plt.figure(figsize=(12, 6))

# Plot x1 and x2 on the same graph
plt.plot(x1, label="Two Octaves", color="blue")
plt.plot(x2, label="One Octave", color="red")

# Add title, labels, and legend
plt.title("Perlin Noise - Two Octaves vs One Octave")
plt.xlabel("Position")
plt.ylabel("Height")
plt.legend()

# Display the plot
plt.show()
